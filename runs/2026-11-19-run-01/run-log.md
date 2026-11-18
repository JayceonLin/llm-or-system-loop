# run-01 執行紀錄（2026-11-19）

由 Agent Whole 記錄。程式檢查的原始結果在 [checks.jsonl](checks.jsonl)，所有草稿在 [attempts/](attempts/)，驗證報告在 [reports/](reports/)。

## P0 取得資料與建立 Wiki

- 沿用 2026-11-18 讀過的 6 篇來源，資料卡放在 `sources/`。
- 先討論、後生成：Loop 設計與 Wiki 組織方式都先和使用者討論，決定內容記在 [wiki/log.md](../../wiki/log.md) 的 discuss 紀錄。
- 生成 Wiki 共 16 頁。
- P0 檢查（lint）：
  - 第 1 次：✗ 8 個錯誤。其中 3 個是檢查規則誤判，表格標題「1 問題輸入」與「第 1 到第 5 站」裡的站別序號，以及「NL4Opt」名稱裡的 4，被當成沒有標來源的數字。修正規則，並把表頭改成不含數字。
  - 另外 5 個是真的問題：OPRO 頁有一行含「8 個」卻沒標 [S5]；總覽頁是孤兒頁，沒有其他頁面連到它；兩頁連到還沒寫的 `loop/LOOP.md`。
  - 第 2、3 次：剩下 3 個、2 個，都是 `loop/LOOP.md` 還不存在。這兩次沒有加 `--run`，所以沒有寫進 checks.jsonl，在這裡手動補記。
  - 寫完 Loop 規範後：✓ 通過，並在開 run 之後再跑一次寫進 checks.jsonl。
- 手搖飲範例的程式用 PuLP 3.3.2 實際執行過，輸出與頁面一致。

## L1 開 run

寫 [plan.md](plan.md)：範圍是 14 頁 Wiki，簡報 14 到 20 張。
