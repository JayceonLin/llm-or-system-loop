---
title: 操作紀錄
type: log
sources: [S1, S2, S3, S4, S5, S6]
updated: 2026-11-19
---

# 操作紀錄（只附加，不修改）

## [2026-11-18] fetch | 取得 6 篇來源
- 讀 S1 綜述（arXiv HTML 全文）、S2 NL4Opt（PDF）、S3 OptiMUS（摘要頁與內文）、S4 Chain-of-Experts（ICLR PDF）、S5 OPRO（PDF）、S6 OptiGuide（PDF），寫成 `sources/` 的 6 張資料卡。
- S3 的 arXiv 頁面讀取時兩次被限流，改用搜尋結果補齊 v1、v2 與 ICML 2024 版的書目資訊。

## [2026-11-18] discuss | 第一次討論（前一版專案）
- AI 列出 6 篇的重點與兩處數字矛盾（OptiMUS 67% 或將近兩倍；NLP4LP 52 或 269 題）。
- 使用者決定：數字矛盾兩個版本都記並標出處；加一個標明自製的手搖飲店範例；讀者設定為完全的新手。

## [2026-11-19] discuss | 重新開始：Loop 設計與 Wiki 組織
- 使用者決定重做一個新專案，主題改成「如何製作使用到 LLM 的 OR 系統」，並提出自己的 Loop 構想：Agent Whole 當領導者，Agent B 整理重點、Agent C 管簡報，驗證不過就退回重做。
- AI 建議補充 7 點：補上取得資料、驗證交給獨立的驗證者、退回時附問題清單並設重試上限、寫投影片前先排大綱並驗證、全部寫完後檢查整份、寫清楚完成條件、交接都用檔案存進 `runs/`。
- 使用者決定：沿用 6 篇來源；B、C、驗證者都交給獨立的子 agent 執行；重點清單通過驗證後先停下來給使用者確認；舊 repo 改成私人，新 repo 叫 `llm-or-system-loop`。
- AI 提出 Wiki 改照「系統的五站」組織，三種角色降為其中一頁，另加一頁簡短的訓練與資料合成，並省略每篇來源的摘要頁。使用者回覆「繼續」，照提案進行，前一版的三個決定也沿用。

## [2026-11-19] ingest | S1 A Survey of Optimization Modeling Meets LLMs
- 用在 overview、第 1、2、5 站、多代理人、評估、訓練與資料合成、限制與設計建議。

## [2026-11-19] ingest | S2 NL4Opt Competition
- 用在第 1、2 站、三種角色、評估、比較表、自製範例；記錄「2.8 與 2 個百分點」的版本差異。

## [2026-11-19] ingest | S3 OptiMUS
- 用在第 1～4 站、多代理人、評估、限制與設計建議、比較表；記錄進步幅度與 NLP4LP 題數兩處版本差異。

## [2026-11-19] ingest | S4 Chain-of-Experts
- 用在第 2～4 站、多代理人、評估、限制與設計建議、比較表；記錄「11 位或 12 位專家」的版本差異。

## [2026-11-19] ingest | S5 Large Language Models as Optimizers (OPRO)
- 用在第 3、4 站、另一條路、三種角色、比較表。

## [2026-11-19] ingest | S6 OptiGuide
- 用在第 3～5 站、三種角色、評估、限制與設計建議、比較表、自製範例。
