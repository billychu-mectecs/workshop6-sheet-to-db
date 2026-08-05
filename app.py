import os
import threading
import time
from datetime import datetime
from zoneinfo import ZoneInfo

import gspread
import requests
from flask import Flask, jsonify, request, send_from_directory
from google.oauth2.service_account import Credentials
from gspread.exceptions import APIError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "")
TAIPEI = ZoneInfo("Asia/Taipei")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
REMAINING_COL = 4  # D欄：剩餘庫存

# Cosmetic-only metadata not stored in the sheet, keyed by 品項ID.
DRINK_META = {
    "A001": {"emoji": "🍵", "desc": "清爽回甘的招牌茶底"},
    "A002": {"emoji": "🍹", "desc": "香氣濃郁的經典紅茶"},
    "A003": {"emoji": "🥥", "desc": "珍珠＋波霸＋椰果三重口感"},
    "A004": {"emoji": "🥤", "desc": "大顆波霸更有嚼勁"},
    "A005": {"emoji": "🧋", "desc": "Q彈珍珠配濃醇奶茶"},
}
DEFAULT_META = {"emoji": "🥤", "desc": ""}

app = Flask(__name__, static_folder=None)

# Serializes every order/delete/reset so two people ordering at the same
# instant are still processed one-at-a-time, in the order their request
# reached this server (i.e. earliest timestamp wins the last cup).
order_lock = threading.Lock()

_client = None
_spreadsheet = None
_inventory_ws = None
_orders_ws = None
_schema_ready = False


def sheet_call(fn, *args, **kwargs):
    """Call a gspread method, retrying briefly on Google's per-minute quota
    error (429) or a transient network/SSL hiccup instead of failing the
    whole order outright."""
    for attempt in range(3):
        try:
            return fn(*args, **kwargs)
        except APIError as e:
            status = getattr(e.response, "status_code", None)
            if status == 429 and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < 2:
                time.sleep(1 * (attempt + 1))
                continue
            raise


def get_client():
    global _client
    if _client is None:
        if not CREDENTIALS_PATH or not SHEET_ID:
            raise RuntimeError(
                "尚未設定 Google Sheet。請先交給 AI 閱讀 README.md，"
                "不要把憑證或 Sheet ID 寫進程式碼。"
            )
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        _client = gspread.authorize(creds)
    return _client


def inventory_ws():
    global _spreadsheet, _inventory_ws
    if _inventory_ws is None:
        if _spreadsheet is None:
            _spreadsheet = sheet_call(get_client().open_by_key, SHEET_ID)
        _inventory_ws = sheet_call(_spreadsheet.get_worksheet, 0)  # Inventory（庫存表）
    return _inventory_ws


def orders_ws():
    global _spreadsheet, _orders_ws
    if _orders_ws is None:
        if _spreadsheet is None:
            _spreadsheet = sheet_call(get_client().open_by_key, SHEET_ID)
        _orders_ws = sheet_call(_spreadsheet.get_worksheet, 1)  # Orders（訂單紀錄）
    return _orders_ws


def ensure_inventory_schema():
    """Make sure the Inventory sheet has a D欄「剩餘庫存」 that mirrors 總庫存
    until an order eats into it. Runs once per server process."""
    global _schema_ready
    if _schema_ready:
        return
    ws = inventory_ws()
    values = sheet_call(ws.get_all_values)
    header = values[0] if values else []
    if len(header) < REMAINING_COL or header[REMAINING_COL - 1] != "剩餘庫存":
        sheet_call(ws.update_cell, 1, REMAINING_COL, "剩餘庫存")

    fills = []  # (row_num, total) pairs still missing 剩餘庫存
    for row_num, row in enumerate(values[1:], start=2):
        total = int(row[2]) if len(row) > 2 and row[2] else 0
        remaining = row[REMAINING_COL - 1] if len(row) >= REMAINING_COL else ""
        if remaining in ("", None):
            fills.append((row_num, total))
    if fills:
        sheet_call(
            ws.batch_update,
            [
                {"range": f"D{row_num}", "values": [[total]]}
                for row_num, total in fills
            ],
        )
    _schema_ready = True


def inventory_rows():
    """List of {row, id, name, total, remaining} straight from the sheet."""
    ensure_inventory_schema()
    values = sheet_call(inventory_ws().get_all_values)
    rows = []
    for row_num, r in enumerate(values[1:], start=2):
        if not r or not r[0]:
            continue
        total = int(r[2]) if len(r) > 2 and r[2] else 0
        remaining = int(r[3]) if len(r) > 3 and r[3] != "" else total
        rows.append({
            "row": row_num,
            "id": str(r[0]),
            "name": r[1],
            "total": total,
            "remaining": remaining,
        })
    return rows


def read_menu():
    menu = []
    for item in inventory_rows():
        meta = DRINK_META.get(item["id"], DEFAULT_META)
        menu.append({
            "id": item["id"],
            "name": item["name"],
            "emoji": meta["emoji"],
            "desc": meta["desc"],
            "total": item["total"],
            "remaining": item["remaining"],
            "sold": item["total"] - item["remaining"],
        })
    return menu


def read_orders():
    records = sheet_call(orders_ws().get_all_records)
    return [
        {
            "row": idx + 2,  # header is row 1, data starts row 2
            "time": r["時間"],
            "name": r["姓名"],
            "itemId": str(r["品項ID"]),
            "itemName": r["品項名稱"],
        }
        for idx, r in enumerate(records)
    ]


@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/api/menu")
def api_menu():
    return jsonify(read_menu())


@app.route("/api/orders")
def api_orders():
    orders = read_orders()
    orders.reverse()
    return jsonify(orders)


@app.route("/api/order", methods=["POST"])
def api_create_order():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    item_id = str(data.get("itemId", "")).strip()

    if not name:
        return jsonify({"error": "請輸入姓名才能送出訂單"}), 400

    with order_lock:
        item = next((r for r in inventory_rows() if r["id"] == item_id), None)
        if item is None:
            return jsonify({"error": "找不到此品項"}), 404
        if item["remaining"] <= 0:
            return jsonify({"error": "此品項已售完，請選擇其他品項"}), 409

        timestamp = datetime.now(TAIPEI).strftime("%Y-%m-%d %H:%M:%S")
        sheet_call(inventory_ws().update_cell, item["row"], REMAINING_COL, item["remaining"] - 1)
        sheet_call(
            orders_ws().append_row,
            [timestamp, name, item_id, item["name"]],
            value_input_option="USER_ENTERED",
        )
        menu = read_menu()
        orders = list(reversed(read_orders()))

    return jsonify({"ok": True, "menu": menu, "orders": orders})


@app.route("/api/orders/<int:row>", methods=["DELETE"])
def api_delete_order(row):
    if row < 2:
        return jsonify({"error": "無效的資料列"}), 400

    with order_lock:
        order_row = sheet_call(orders_ws().row_values, row)
        if not order_row:
            return jsonify({"error": "找不到這筆訂單"}), 404
        item_id = order_row[2] if len(order_row) > 2 else None
        sheet_call(orders_ws().delete_rows, row)

        if item_id:
            item = next((r for r in inventory_rows() if r["id"] == item_id), None)
            if item:
                restored = min(item["total"], item["remaining"] + 1)
                sheet_call(inventory_ws().update_cell, item["row"], REMAINING_COL, restored)

        menu = read_menu()
        orders = list(reversed(read_orders()))

    return jsonify({"ok": True, "menu": menu, "orders": orders})


@app.route("/api/reset", methods=["POST"])
def api_reset():
    with order_lock:
        rows = inventory_rows()
        if rows:
            sheet_call(
                inventory_ws().batch_update,
                [
                    {"range": f"D{item['row']}", "values": [[item["total"]]]}
                    for item in rows
                ],
            )

        ws = orders_ws()
        last_row = len(sheet_call(ws.get_all_values))
        if last_row >= 2:
            sheet_call(ws.delete_rows, 2, last_row)

        menu = read_menu()

    return jsonify({"ok": True, "menu": menu, "orders": []})


if __name__ == "__main__":
    app.run(debug=False, port=5000, threaded=True)
