# Workshop 6：把 Sheet 版作品搬到資料庫

這是 Workshop 6 的官方公開練習 Repo。它保留上週「飲料訂購系統」的 Sheet 版本，讓你把 Repo 交給 AI，再用自然語言完成資料庫改造。

你不需要會寫 SQL，也不需要記指令。你的工作是說清楚需求、確認 AI 的計畫，最後實際操作看看成果。

## 先確認不是釣魚 Repo

開始前只看三件事：

1. 網址開頭必須是 `https://github.com/`
2. 帳號必須是 `billychu-mectecs`
3. Repo 名稱必須是 `workshop6-sheet-to-db`

正確網址只有這個：

`https://github.com/billychu-mectecs/workshop6-sheet-to-db`

若帳號、拼字或網址不同，先不要下載、不要執行，請講師確認。GitHub 上有很多公開作品，公開不代表安全。

## 課堂怎麼開始

先在「你上週完成的作品資料夾」開啟 Claude Code，再把正確網址與下面這段話貼給它。官方 Repo 是 AI 的參考資料，真正要修改的是你自己的作品。

```text
請先確認這是講師提供的官方 Repo：
https://github.com/billychu-mectecs/workshop6-sheet-to-db

我目前開啟的資料夾是上週完成的作品，這才是要修改的目標。請先確認目前位置與主要檔案；若不像一個現有專案，請停止並提醒我選對資料夾。

請把官方 Repo 下載到另外的暫存參考位置，讀完 README.md、CLAUDE.md 與 prompts/sheet-to-db.md。不要執行官方 Repo，不要用範例檔案覆蓋我的作品，也不要改動暫存參考資料。
讀完後，第一題只問我：「你是哪個部門？」我的回答只用來確認，不可拿來決定或擴大資料庫權限。
先不要執行或修改。先用繁體中文告訴我：
1. 我的作品位置與官方參考 Repo 位置
2. 我的作品目前資料怎麼流動
3. 會保留哪些既有功能，準備修改哪些地方
4. 完成後怎麼驗證
等我確認後再開始。
```

AI 會先把官方規則與你的作品互相比對，再陪你把自己作品的資料從 Google Sheet 搬到課堂提供的資料庫。你原本改過的畫面、文字與功能都應保留；你只要回答它一次一個的小問題。

## 這堂課會完成什麼

- 保留目前能用的飲料訂購畫面
- 把訂單與庫存搬到資料庫
- 同一筆訂購一起完成「扣庫存」與「新增訂單」
- 確認搬家前後的資料筆數與功能
- 用 Git 保存程式修改紀錄
- 最後由你確認後，再決定是否上傳 GitHub

簡單分工：GitHub 保存「作品怎麼做」，資料庫保存「大家實際使用的資料」。

## 公開 Repo 不可放的東西

- 密碼、API Key、Token、憑證檔
- 公司內部位址、資料庫連線字串
- 真實員工、客戶、訂單或營運資料
- 任何 `.env` 實際內容

這個 Repo 只放假資料與欄位名稱。實際連線由電腦環境提供，使用者不需要看見帳號密碼。

## Repo 地圖

- `app.py`、`index.html`：上週 Sheet 版飲料訂購系統
- `CLAUDE.md`：AI 必須遵守的課堂規則
- `prompts/sheet-to-db.md`：完整的 Sheet 轉資料庫任務
- `docs/current-system.md`：目前作品的白話說明
- `docs/data-dictionary.md`：資料欄位與規則
- `docs/connection-flow.md`：AI 使用的安全連線流程
- `sample-data/`：可公開使用的假資料
- `migrations/`：AI 之後放資料庫改造紀錄的位置

> 本 Repo 是教學起點，不含公司正式環境，也不是可直接部署的正式系統。
