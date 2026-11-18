---
title: 目錄
type: index
sources: [S1, S2, S3, S4, S5, S6]
updated: 2026-11-19
---

# Wiki 目錄：怎麼做出一個用到 LLM 的 OR 系統

每一頁的數字與主張都標了來源 [S1]～[S6]，對應 [`sources/`](../sources/) 的資料卡。所有討論與操作紀錄見 [log.md](log.md)。

## 從這裡開始
- [overview.md](overview.md)：總覽，系統的五站與每篇來源做到哪幾站

## 系統的五站
- [system/01-problem-input.md](system/01-problem-input.md)：第 1 站 問題輸入，從文字到有結構的資料
- [system/02-modeling.md](system/02-modeling.md)：第 2 站 建模，寫出決策變數、目標函數、限制式
- [system/03-code-and-solver.md](system/03-code-and-solver.md)：第 3 站 寫程式，交給求解器
- [system/04-verify-and-repair.md](system/04-verify-and-repair.md)：第 4 站 驗證與修正，以及這個回圈的極限
- [system/05-explain-and-whatif.md](system/05-explain-and-whatif.md)：第 5 站 解釋結果與 what-if

## 跨站的主題
- [topics/multi-agent.md](topics/multi-agent.md)：多代理人怎麼分工，指揮者、彙整器、評估器
- [topics/llm-as-optimizer.md](topics/llm-as-optimizer.md)：另一條路，LLM 直接當最佳化器（OPRO）
- [topics/llm-roles.md](topics/llm-roles.md)：LLM 的三種角色，翻譯者、最佳化器、解說員
- [topics/evaluation.md](topics/evaluation.md)：怎麼評估一個系統，資料集錯誤率與數字怎麼看
- [topics/training-and-data.md](topics/training-and-data.md)：訓練與資料合成，讓 LLM 本身更會建模
- [topics/risks-and-design.md](topics/risks-and-design.md)：限制、風險與設計建議

## 比較與範例
- [comparisons/systems.md](comparisons/systems.md)：系統比較表，每個系統涵蓋哪幾站與代表數字
- [examples/tea-shop.md](examples/tea-shop.md)：自製範例，手搖飲店走完五站（含可執行程式與 what-if）

## 紀錄
- [log.md](log.md)：討論、ingest、檢查的紀錄
