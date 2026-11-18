---
id: S4
title: "Chain-of-Experts: When LLMs Meet Complex Operations Research Problems"
authors: Ziyang Xiao, Dongxiang Zhang, Yangjun Wu, Lilin Xu, Yuan Wang, Xiongwei Han, Xiaojin Fu, Tao Zhong, Jia Zeng, Mingli Song, Gang Chen
affiliation: 浙江大學、華為諾亞方舟實驗室、新加坡新躍社會科學大學
year: 2024
venue: ICLR 2024
url: https://proceedings.iclr.cc/paper_files/paper/2024/hash/d45ee77826332c100a1e15f7765b99ff-Abstract-Conference.html
license: 會議論文，視為一般著作權
read: ICLR 論文 PDF 全文
captured: 2026-11-18
---

# S4 擷取筆記（不可修改）

## 是什麼
- 第一個用 LLM 處理「複雜」作業研究問題的方法：多代理人合作框架 Chain-of-Experts（CoE）。
- 每個代理人有特定角色，並具備作業研究的領域知識。

## 角色（論文表 5；內文說 11 位專家，表格列出 12 位）
- 術語解釋專家：補充領域背景。
- 參數、變數、限制、目標擷取專家：分別抽出模型的各個部分。
- 建模知識補充專家：提供建模技巧。
- 建模專家：寫出數學模型，通常是混合整數規劃。
- LP 檔產生專家：寫出求解器讀的 LP 格式檔。
- 限制可行性檢查專家（只出現在表 5）。
- 程式範例提供者：從參考資料提供程式範例。
- 程式專家：寫 Gurobi 的 Python 程式。
- 程式審查專家：檢查程式的錯誤與效率。
- 評估器（Evaluator）：不是 LLM。它執行程式與測試案例，把結果轉成回饋。
- 彙整器（Reducer）：把各專家的意見合成最後答案。

## 指揮者與兩個機制
- 指揮者（Conductor）：一個 LLM，根據題目與目前的意見，決定下一步請哪位專家。它是用提示做的，沒有另外訓練。
- 前向思考建構：指揮者依序挑專家，每位專家留下意見；固定步數後，由彙整器產生答案。
- 反向反思：評估器發現答案錯了，就把專家倒過來逐一檢查，找出並修正錯誤。重複到程式通過，或達到最多次數為止。

## 資料集
- LPWP：1,101 題基礎線性規劃，切成訓練 713、驗證 99、測試 289。
- ComplexOR：37 題複雜問題（4.1 節）。表 6 的結果用的是 20 題，兩個數字對不上。

## 準確率
| 基礎模型 | 資料集 | CoE | Reflexion | 思維鏈 | 一般提示 |
| --- | --- | --- | --- | --- | --- |
| GPT-3.5-turbo | LPWP | 58.9% | 50.7% | 45.8% | 42.4% |
| GPT-3.5-turbo | ComplexOR | 25.9% | 13.5% | 0.5% | 0.5% |
| GPT-4 | LPWP | 64.2% | 53.0% | （未報告） | 47.3% |
| GPT-4 | ComplexOR | 31.4% | 16.8% | （未報告） | 4.9% |
| Claude2 | LPWP | 62.0% | 51.4% | （未報告） | 44.9% |
| Claude2 | ComplexOR | 27.0% | 12.4% | （未報告） | 0.0% |

## 限制（論文沒有獨立的限制章節，以下整理自內文）
- 專家意見多了會超過上下文長度上限。
- 前向鏈越長，推理時間與 API 呼叫越多。
- ComplexOR 很小；用 GPT-3.5 時 CoE 仍有超過七成的複雜題解不出來。
- 測試案例由專家撰寫。
