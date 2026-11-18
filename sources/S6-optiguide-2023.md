---
id: S6
title: "Large Language Models for Supply Chain Optimization"（OptiGuide）
authors: Beibin Li, Konstantina Mellou, Bo Zhang, Jeevan Pathuri, Ishai Menache
affiliation: Microsoft Research；Microsoft Cloud Supply Chain
year: 2023
venue: arXiv:2307.03875（v1 2023-07-08，v2 2023-07-13）
url: https://arxiv.org/abs/2307.03875
license: 頁面未標示，視為一般著作權
read: arXiv PDF 全文
captured: 2026-11-18
---

# S6 擷取筆記（不可修改）

## 是什麼
- OptiGuide：讓使用者用一般文字發問，取得關於最佳化結果的解釋，幫助利害關係人理解並信任供應鏈決策。
- 主要回答 what-if 問題。論文的例子：如果某個需求改向供應商 B 而不是供應商 A 進貨，成本會怎麼變？
- 它沿用既有的組合最佳化技術，不是取代它。

## 組成
- Coder：把使用者的問題加上應用背景、範例與重寫後的問題，組成給 LLM 的提示。
- Safeguard：檢查 LLM 產生的程式。可以觸發自我除錯，或停止並回報錯誤。
- Interpreter：讀取求解器或資料庫的輸出（紀錄、表格、圖），寫成人看得懂的回答。
- 應用端：資料庫、最佳化求解器（例如 Gurobi）、工程師寫的輔助函式、文件。

## 流程
1. 使用者發問。
2. Coder 組出提示。
3. LLM 寫出回答問題用的程式。
4. Safeguard 檢查程式，再交給求解器或資料庫執行。
5. 執行結果被記錄下來。
6. 第 2 到 5 步可以重複，直到結果令人滿意。
7. LLM 讀取紀錄，寫出回答，交回給使用者。

## 隱私
- 資料留在求解器與資料庫，只有問題與產生的程式會經過 LLM，所以專有資料不會送給 LLM。

## 評估
- 5 個情境：設施選址、多商品網路流、人力指派、旅行推銷員問題、咖啡配送。
- 每個情境做 10 次實驗，每個情境至少 10 組問題，每組通常 10 到 30 題；論文沒有給總題數。
- 問題由團隊自己撰寫，避免 LLM 在訓練時看過。
- GPT-4 準確率
  - 沒有範例：59%。
  - 同類型題目，給 5 或 10 個範例：92–93%。
  - 不同類型題目，給 10 個範例：84%（隨機挑範例）、80%（挑最相近的範例）。
  - 5 個情境平均：93%。

## 部署
- 用在 Azure 的伺服器供應鏈：Intelligent Fulfillment System，負責把伺服器從倉庫分配、運送到資料中心。
- 透過 Azure OpenAI 使用 GPT-4。
- 初步評估中，同類型題目的準確率超過 90%。
- 規劃人員與工程師的初步回饋正面。規劃人員喜歡 what-if 分析，因為可以自己查，減少待命工程師的負擔。
- 論文指出：以前回答一個 what-if 問題，需要超過 3 位作業人員加上 1 位待命工程師。
