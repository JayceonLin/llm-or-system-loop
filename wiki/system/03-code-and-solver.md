---
title: 第 3 站 寫程式，交給求解器
type: step
sources: [S3, S4, S5, S6]
updated: 2026-11-19
---

# 第 3 站 寫程式，交給求解器

## 這一站要做什麼

模型寫好之後，要有人真的把它算出來。**求解器（solver）**是專門解最佳化模型的軟體，例如 Gurobi [S3]。它保證算出最好的答案，或告訴你這題無解。

在大多數系統裡，LLM 不自己算答案，而是寫一段呼叫求解器的程式。

## 三個系統的做法

| 系統 | LLM 寫什麼 | 誰負責計算 |
| --- | --- | --- |
| OptiMUS | 用 Gurobi 或 cvxpy 寫 Python 程式，提示裡附上針對求解器的指示，減少常見錯誤 [S3] | 求解器；程式讀入資料、求解，結果存成 JSON [S3] |
| Chain-of-Experts | LP 檔產生專家寫求解器讀的 LP 格式檔；程式專家寫 Gurobi 的 Python 程式；程式審查專家檢查錯誤與效率 [S4] | 求解器 |
| OptiGuide | Coder 把問題加上應用背景、範例與重寫後的問題組成提示，LLM 依此寫出程式 [S6] | 求解器或資料庫 [S6] |

## 為什麼不讓 LLM 自己算

- LLM 擅長讀懂文字，求解器擅長精確計算，分工後各做擅長的事。
- 讓 LLM 直接找解的 OPRO，在小問題上表現不錯，問題變大後就輸給專門的方法，作者也說它不是要贏過求解器 [S5]，見[另一條路](../topics/llm-as-optimizer.md)。
- LLM 會算錯，也會重複產生以前的解 [S5]。

## 資料不必交給 LLM

OptiGuide 讓資料一直留在求解器與資料庫，只有問題與 LLM 產生的程式會經過 LLM [S6]。公司的專有資料不會送出去，見[解釋結果與 what-if](05-explain-and-whatif.md)。

## 成本

OptiMUS 成功的執行平均用掉 4117.1 ± 1509.7 個 token，不含求解器時間，每次都在 7 分鐘內完成 [S3]。

上一站：[建模](02-modeling.md)　下一站：[驗證與修正](04-verify-and-repair.md)。

**來源：** [S3](../../sources/S3-optimus-2023.md)、[S4](../../sources/S4-chain-of-experts-2024.md)、[S5](../../sources/S5-opro-2023.md)、[S6](../../sources/S6-optiguide-2023.md)
