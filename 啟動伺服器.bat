@echo off
cd /d "%~dp0"
echo 正在啟動飲料訂購練習系統...
echo 啟動後，瀏覽器會顯示本機網址。
uv run python app.py
pause
