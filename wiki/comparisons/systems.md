---
title: 系統比較表：每個系統涵蓋哪幾站
type: comparison
sources: [S2, S3, S4, S5, S6]
updated: 2026-11-19
---

# 系統比較表：每個系統涵蓋哪幾站

## 涵蓋範圍

| 系統 | 問題輸入 | 建模 | 寫程式 | 驗證修正 | 解釋結果 |
| --- | --- | --- | --- | --- | --- |
| NL4Opt | ✓ 標出元素 | ✓ 意義表示 | 轉成求解器格式 | — | — |
| OptiMUS | ✓ 結構化輸入 | ✓ | ✓ | ✓ 單元測試 | — |
| Chain-of-Experts | — | ✓ 多位專家 | ✓ | ✓ 反向反思 | — |
| OptiGuide | 使用者的 what-if 問題 | 沿用既有模型 | ✓ | ✓ Safeguard | ✓ Interpreter |
| OPRO | 不走五站，LLM 直接提出解，用分數回饋 | | | | |

各系統的做法見 [OptiMUS 與 NL4Opt 的輸入](../system/01-problem-input.md)、[建模](../system/02-modeling.md)、[驗證與修正](../system/04-verify-and-repair.md)、[OPRO](../topics/llm-as-optimizer.md)。

## 代表數字

| 系統 | 代表數字 |
| --- | --- |
| NL4Opt | 子任務 2 第一名 0.899，ChatGPT 0.927 [S2] |
| OptiMUS | 解出的題目接近基本提示的兩倍 [S3] |
| Chain-of-Experts | GPT-4：基礎題 64.2%、複雜題 31.4% [S4] |
| OPRO | 10 個城市差距 0.0%，50 個城市差距 11.0% [S5] |
| OptiGuide | 沒有範例 59%，同類型題目給範例 92–93% [S6] |

**版本差異：** OptiMUS 的進步幅度，v1 摘要寫「多解出 67%」，v2 摘要寫「接近兩倍」，內文寫「提高 91%」[S3]。

## 怎麼讀這張表

- 沒有一個系統五站全包。做系統時，可以從不同來源借每一站的做法。
- 各系統的數字來自不同考卷、不同 LLM，**不能拿來比誰比較強**，見[怎麼評估一個系統](../topics/evaluation.md)。

**來源：** [S2](../../sources/S2-nl4opt-2022.md)、[S3](../../sources/S3-optimus-2023.md)、[S4](../../sources/S4-chain-of-experts-2024.md)、[S5](../../sources/S5-opro-2023.md)、[S6](../../sources/S6-optiguide-2023.md)
