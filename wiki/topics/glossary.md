---
title: 新手術語表（自製）
type: topic
sources: [自製]
updated: 2026-11-19
---

# 新手術語表（自製）

> **這一頁是自製的白話解釋，不是來自 6 篇來源。** [自製] Wiki 其他頁面用到這些術語，但來源論文沒有替新手解釋。這一頁只給最基本的意思，夠看懂其他頁面就好。

| 術語 | 白話解釋 | 用在哪裡 |
| --- | --- | --- |
| 線性規劃（Linear Programming，LP） | 目標函數和限制式都是一次式的最佳化模型，例如 20x₁ + 30x₂，變數可以是小數。手搖飲範例就是一個線性規劃 [自製] | [建模](../system/02-modeling.md)、[手搖飲範例](../examples/tea-shop.md) |
| 混合整數規劃（Mixed-Integer Programming，MIP） | 在線性規劃上，再規定某些變數只能是整數，例如開幾台機器不能是 2.5 台 [自製] | [建模](../system/02-modeling.md) |
| LP 格式檔 | 把模型寫成文字檔的一種固定格式，求解器可以直接讀 [自製] | [寫程式交給求解器](../system/03-code-and-solver.md) |
| JSON | 一種用文字存資料的通用格式，用「名稱：值」的方式寫，程式和人都讀得懂 [自製] | [問題輸入](../system/01-problem-input.md)、[寫程式交給求解器](../system/03-code-and-solver.md) |
| token | LLM 讀寫文字時的計算單位，大約是一個字或一個詞的一小段。用掉的 token 越多，通常花的時間與費用也越多 [自製] | [寫程式交給求解器](../system/03-code-and-solver.md) |
| API 呼叫 | 程式透過網路請 LLM 服務做一次工作。呼叫次數越多，等待時間與費用通常越多 [自製] | [多代理人怎麼分工](multi-agent.md) |
| 上下文長度 | LLM 一次能讀進來的文字上限，超過的部分它就看不到 [自製] | [多代理人怎麼分工](multi-agent.md)、[另一條路](llm-as-optimizer.md) |
| 單元測試 | 一小段自動檢查的程式，確認某個結果符合預期 [自製] | [驗證與修正](../system/04-verify-and-repair.md) |
