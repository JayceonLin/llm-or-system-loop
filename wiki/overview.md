---
title: 總覽：怎麼做出一個用到 LLM 的 OR 系統
type: overview
sources: [S1, S2, S3, S4, S5, S6]
updated: 2026-11-19
---

# 總覽：怎麼做出一個用到 LLM 的 OR 系統

## 一句話

作業研究（Operations Research，OR）系統是幫人做決策的程式：把排產、配送、選址這類問題寫成數學模型，再算出最好的做法。過去寫模型需要專家，Gurobi 的使用者有 81% 具研究所學歷 [S1]。大型語言模型（LLM）加進來之後，系統可以自己讀懂文字、寫出模型與程式，再交給求解器計算 [S3]。

## 系統的五站

一個用到 LLM 的 OR 系統，可以拆成五站。每一站都有一頁說明：

1. [問題輸入](system/01-problem-input.md)：把使用者寫的文字題整理成有結構的資料。
2. [建模](system/02-modeling.md)：寫出決策變數、目標函數、限制式。
3. [寫程式交給求解器](system/03-code-and-solver.md)：LLM 寫程式，真正的計算交給求解器。
4. [驗證與修正](system/04-verify-and-repair.md)：執行、檢查，錯了就帶著錯誤訊息重寫。
5. [解釋結果與 what-if](system/05-explain-and-whatif.md)：把結果翻成白話，回答「如果改成這樣會怎樣」。

## 每篇來源做到哪幾站

| 系統 | 涵蓋的站 | 來源 |
| --- | --- | --- |
| NL4Opt 競賽 | 第 1、2 站 | [S2] |
| OptiMUS | 第 1～4 站 | [S3] |
| Chain-of-Experts | 第 2～4 站 | [S4] |
| OptiGuide | 第 3～5 站 | [S6] |
| OPRO | 不走這五站，讓 LLM 直接找解 | [S5] |
| 綜述 | 整理整個領域的方法、資料集與未來方向 | [S1] |

完整比較見[系統比較表](comparisons/systems.md)，所有論文的書目見[資料來源](references.md)。

## 跨站的主題

- [多代理人怎麼分工](topics/multi-agent.md)：讓好幾個 LLM 各負責一站。
- [另一條路：LLM 直接當最佳化器](topics/llm-as-optimizer.md)
- [LLM 的三種角色](topics/llm-roles.md)：翻譯者、最佳化器、解說員。
- [怎麼評估一個系統](topics/evaluation.md)
- [訓練與資料合成](topics/training-and-data.md)：讓 LLM 本身更會建模。
- [限制、風險與設計建議](topics/risks-and-design.md)
- [新手術語表](topics/glossary.md)：自製的白話解釋，遇到看不懂的詞先查這裡。

## 建議閱讀順序

1. 先看[自製範例：手搖飲店](examples/tea-shop.md)，用一題小問題走完五站。
2. 再照第 1 到第 5 站的順序讀。
3. 最後讀[限制、風險與設計建議](topics/risks-and-design.md)。

**來源：** [S1](../sources/S1-survey-2025.md)、[S2](../sources/S2-nl4opt-2022.md)、[S3](../sources/S3-optimus-2023.md)、[S4](../sources/S4-chain-of-experts-2024.md)、[S5](../sources/S5-opro-2023.md)、[S6](../sources/S6-optiguide-2023.md)
