# 個人資料庫安全連線流程

這份文件是給 AI 執行的。學員不需要回答部門、工號，也不需要知道連線技術。可使用的資料庫範圍已由個人安裝包與 SQL Login 決定。

## 對學員的原則

不要詢問或要求學員輸入部門、工號、主機、資料庫名稱、帳號、密碼或 connection string。口頭回答不能授權，也不能改變資料庫範圍。

## AI 的連線前檢查

1. 確認 `%LOCALAPPDATA%\Medtecs\DbAccess\config.json`、`credential.bin`、`Invoke-WithDbAccess.ps1` 都存在。不可直接讀取或解密 `credential.bin`。
2. 建立一個不輸出設定值的連線檢查程式，再透過 helper 執行：

   ```powershell
   & "$env:LOCALAPPDATA\Medtecs\DbAccess\Invoke-WithDbAccess.ps1" `
     -FilePath "uv" `
     -ArgumentList @("run", "python", "<連線檢查程式>")
   ```

   實際執行時使用學員作品內的檔案路徑，不把密碼放在命令列。
3. 在 helper 啟動的子程序內確認必要的 `MEDTECS_DB_*` 設定齊全，只回報「完整、缺少、範圍不明或權限不符」，不要輸出任何實際值。
4. 子程序只能從 `MEDTECS_DB_*` 環境變數使用個人 SQL Login，不向學員索取密碼，不把密碼寫進 `.env`、程式、命令列、Git 或 log。
5. 只連線到 `MEDTECS_DB_DATABASE` 與 `MEDTECS_DB_SCHEMA` 指定的範圍，不列出或嘗試其他資料庫或 schema。
6. 成功後只回報：「已連到你的個人練習資料庫。」不要顯示伺服器、資料庫、連線字串或登入資訊。

## 權限如何決定

```text
個人工號安裝包
  -> Windows DPAPI 保護的 credential.bin
  -> Invoke-WithDbAccess.ps1
  -> 個人 SQL Login
  -> 已核發的資料庫
  -> 自己的工號 schema
```

權限只由已核發的個人 SQL Login、資料庫與工號 schema 決定。helper 只把連線資料短暫交給它啟動的子程序；學員或 AI 的文字回答不可用來擴大權限。

## 缺少設定時

只告訴學員：

> 這台電腦尚未完成 DB 連線安裝。請執行個人 install-db-access.bat，完成後再回到目前的 Claude Code 繼續。

不要請學員自行填值，也不要把秘密寫進 `.env` 或程式碼。
