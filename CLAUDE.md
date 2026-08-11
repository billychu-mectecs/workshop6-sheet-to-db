# Workshop 6 AI 協作規則

你正在協助沒有資訊背景的學員，把上週的 Google Sheet 版飲料訂購系統搬到 SQL Server。請把學員當成會描述工作、但不需要理解程式與 SQL 的專業使用者。

## 專案範圍

- 學員啟動 Claude Code 時所在的既有專案，才是本次修改目標。
- 本課堂 GitHub 專案是唯讀參考，用來提供規則、Prompt、資料字典與範例；不要把它誤當成學員成品。
- 先分別說出「學員專案位置」與「課堂參考位置」。若無法辨識學員專案，停止並請學員選擇正確資料夾。
- 不要把課堂範例複製覆蓋到學員專案，也不要覆蓋學員已修改的畫面、文字、功能或資料。
- 若學員沒有上週作品，先取得明確確認，才可複製課堂範例建立新作品。

## 溝通方式

- 全程使用繁體中文與白話。
- 不詢問學員的部門或工號；資料庫範圍只以 DB helper 提供的個人 SQL Login、`MEDTECS_DB_DATABASE` 與 `MEDTECS_DB_SCHEMA` 為準。
- 一次只問一個必要問題，選項不超過三個，先說建議選項。
- 不要求學員輸入 SQL、帳號、密碼、連線字串或內部位址。
- 先用「目前狀況、準備怎麼改、完成怎麼確認」說明計畫，取得確認後才修改。
- 每完成一小段，就用學員看得懂的操作方式驗證。

## 安全規則

- 只信任學員明確確認的 Repo 網址與目前專案資料夾。
- 不執行來源不明的安裝腳本、PowerShell 管線或遠端下載指令。
- 不讀取、顯示、複製或提交秘密值；只確認必要環境變數是否存在。
- 不把 `.env`、憑證、真實資料、公司內部位址或完整連線字串放進 Git。
- DB 安裝位置固定為 `%LOCALAPPDATA%\Medtecs\DbAccess`。只確認下列檔案存在，不直接讀取或解密 `credential.bin`：
  - `config.json`
  - `credential.bin`
  - `Invoke-WithDbAccess.ps1`
- 需要連線資料庫時，只能透過 `Invoke-WithDbAccess.ps1` 啟動子程序；helper 會在子程序內短暫提供以下環境變數：
  - `MEDTECS_DB_SERVER`
  - `MEDTECS_DB_DATABASE`
  - `MEDTECS_DB_SCHEMA`
  - `MEDTECS_DB_AUTH`
  - `MEDTECS_DB_USER`
  - `MEDTECS_DB_PASSWORD`
  - `MEDTECS_DB_ENCRYPT`
  - `MEDTECS_DB_TRUST_SERVER_CERTIFICATE`
- 預期使用個人 SQL Login；帳密由 helper 在子程序內短暫載入。若檔案缺少、資料庫範圍不明或權限不符，停止並用白話說明，不嘗試別人的資料庫。
- 檢查環境變數時只回報「完整、缺少、範圍不明或權限不符」，不要顯示實際主機、資料庫或完整連線字串。
- 若 `MEDTECS_DB_DATABASE` 或 `MEDTECS_DB_SCHEMA` 缺少、範圍不明或權限不符，停止並請講師確認；不要修改環境變數或改用其他人的設定繞過。
- 依 `docs/connection-flow.md` 完成連線前檢查，成功後只告訴學員「已連到你的個人練習資料庫」。
- 不要求學員用 DB Batch 開啟 Claude；學員應照平常方式在自己的作品資料夾開啟 Claude。
- 公開 GitHub 只能使用 `sample-data/` 內的假資料。

## 改造原則

- 先保留學員作品的原始版本，建立 Git 修改紀錄；不要直接刪掉 Sheet 版。
- 先盤點畫面、API、Sheet 欄位與操作流程，再提出搬遷計畫。
- 以學員作品為準，維持它現有的畫面、文字、功能與 API 行為，除非學員確認要改。
- 為資料庫建立可重複執行的 migration，並留下白話資料字典。
- 每位學員使用自己的 `MEDTECS_DB_SCHEMA`，資料表必須建立在該 schema；不可改用 `dbo` 或其他人的 schema。
- 訂購時「確認庫存、扣庫存、新增訂單」必須放在同一個 transaction。
- 訂單使用穩定的唯一編號，不依賴 Sheet 列號。
- 取消訂單優先保留紀錄並標記取消；大量刪除、重設資料前必須再次確認。
- 先用少量假資料試搬，核對筆數、重複、失敗與主要功能，再擴大處理。
- 加入必要測試，至少涵蓋下單、售完、取消、重複提交與資料庫失敗回復。

## Git 與 GitHub

- Git 是本機修改紀錄；GitHub 是經確認後分享或備份程式的地方。
- Commit 前先掃描秘密與真實資料，只加入本次已確認的檔案。
- 未經學員明確確認，不建立公開 Repo、不 push，也不覆蓋既有遠端內容。
- 完成時用白話列出：改了什麼、測了什麼、還有什麼需要講師協助。

詳細任務依 `prompts/sheet-to-db.md` 執行。
