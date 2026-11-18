---
title: LLM 的三種角色：翻譯者、最佳化器、解說員
type: topic
sources: [S2, S3, S4, S5, S6]
updated: 2026-11-19
---

# LLM 的三種角色：翻譯者、最佳化器、解說員

[總覽](../overview.md)是照系統的五站整理。另一種整理方式，是看 LLM 在系統裡扮演什麼角色。這個分法是本 Wiki 的整理，不是某一篇論文提出的。

| 角色 | 做什麼 | 對應的站 | 代表系統 |
| --- | --- | --- | --- |
| 翻譯者 | 把文字題變成模型與程式，交給求解器算 | 第 1～3 站 | NL4Opt [S2]、OptiMUS [S3]、Chain-of-Experts [S4] |
| 最佳化器 | 不寫模型，自己提出解，看分數再改進 | 不走五站 | OPRO [S5] |
| 解說員 | 模型已經有了，幫不會寫程式的人問 what-if，再翻成白話 | 第 3～5 站 | OptiGuide [S6] |

## 共同點

- 除了最佳化器，LLM 都不自己算答案，而是寫程式交給求解器，見[寫程式交給求解器](../system/03-code-and-solver.md)。
- 三種角色都有「試、檢查、再改」的回圈，見[驗證與修正](../system/04-verify-and-repair.md)。

## 怎麼用這張表

設計一個 OR 系統時，先決定 LLM 要當哪一種角色：

- 使用者有一個新問題、需要從頭建模：用翻譯者。
- 問題很難寫成模型、只能評分：可以考慮最佳化器，但要知道它在大問題上的限制，見[另一條路](llm-as-optimizer.md)。
- 公司已經有模型，想讓更多人自己查詢：用解說員，見[解釋結果與 what-if](../system/05-explain-and-whatif.md)。

**來源：** [S2](../../sources/S2-nl4opt-2022.md)、[S3](../../sources/S3-optimus-2023.md)、[S4](../../sources/S4-chain-of-experts-2024.md)、[S5](../../sources/S5-opro-2023.md)、[S6](../../sources/S6-optiguide-2023.md)
