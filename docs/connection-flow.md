# 部門資料庫安全連線流程

這份文件是給 AI 執行的。學員只需要回答部門並確認結果，不需要知道連線技術。

## 對學員的第一題

只問：

> 你是哪個部門？

這個答案只用來確認電腦環境是否正確，不能用來取得權限。不要追問主機、資料庫名稱、帳號、密碼或 connection string。

## AI 的連線前檢查

1. 確認 `%LOCALAPPDATA%\Medtecs\DbAccess\config.json`、`credential.bin`、`Invoke-WithDbAccess.ps1` 都存在。不可直接讀取或解密 `credential.bin`。
2. 建立一個不輸出設定值的連線檢查程式，再透過 helper 執行：

   ```powershell
   & "$env:LOCALAPPDATA\Medtecs\DbAccess\Invoke-WithDbAccess.ps1" -FilePath uv run python <連線檢查程式>
   ```

   實際執行時使用學員作品內的檔案路徑，不把密碼放在命令列。
3. 將學員回答的部門與環境指定的部門交叉確認。無法確認或不一致時，停止並請講師協助；不要自行改成其他資料庫。
4. 子程序只能從 `MEDTECS_DB_*` 環境變數使用個人 SQL Login，不向學員索取密碼，不把密碼寫進 `.env`、程式、命令列、Git 或 log。
5. 只連線到環境指定的資料庫與 schema，不列出或嘗試其他部門資料庫。
6. 成功後只回報：「已連到你的部門練習資料庫。」不要顯示伺服器、資料庫、連線字串或登入資訊。

## 權限如何決定

```text
學員回答部門
  -> 只做畫面上的確認

個人 SQL Login
  -> 只映射到所屬部門資料庫
  -> 只允許自己的工號 schema
```

即使有人改動口頭回答，資料庫仍必須依個人 SQL Login 拒絕其他部門資料庫與其他人的 schema。helper 只把已核發的連線資料交給它啟動的子程序，不可用來擴大權限。

## 缺少設定時

只告訴學員：

> 這台電腦尚未完成 DB 連線安裝。請執行個人 install-db-access.bat，完成後再回到目前的 Claude Code 繼續。

不要請學員自行填值，也不要把秘密寫進 `.env` 或程式碼。
