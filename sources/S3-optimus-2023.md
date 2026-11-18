---
id: S3
title: "OptiMUS: Optimization Modeling Using MIP Solvers and large language models"
authors: Ali AhmadiTeshnizi, Wenzhi Gao, Madeleine Udell
affiliation: 史丹佛大學 管理科學與工程系
year: 2023
venue: arXiv:2310.06116（v1 2023-10-09、v2 2023-10-30）；後續版本 "OptiMUS: Scalable Optimization Modeling with (MI)LP Solvers and Large Language Models"，ICML 2024，arXiv:2402.10172（2024-02-15）
url: https://arxiv.org/abs/2310.06116
license: 頁面未標示，視為一般著作權
read: arXiv 摘要頁與 v2 內文、ICML 2024 摘要
captured: 2026-11-18
---

# S3 擷取筆記（不可修改）

## 是什麼
- 以 LLM 為核心的代理人（agent），能把自然語言描述的（混合整數）線性規劃問題寫成數學模型、寫並除錯求解器程式、產生測試，並檢查解是否有效。
- 目的是讓請不起最佳化專家的組織也能使用最佳化。

## 流程（2023 版）
1. 輸入：結構化的題目描述 SNOP（Structured Natural language Optimization Problem），有 6 個欄位。數值資料另外存成 JSON 檔，只把資料格式交給 LLM。
2. 建模：LLM 用 Markdown 寫出變數、限制式與目標。
3. 寫程式：LLM 用 Gurobi 或 cvxpy 寫 Python 程式，並附上針對求解器的指示來減少常見錯誤。
4. 執行：程式讀入資料、求解，結果存成 JSON。
5. 測試與修正：LLM 產生單元測試，檢查輸出格式、限制是否滿足、結果是否自相矛盾；執行錯誤與沒通過的測試會回饋給 LLM 修正。
6. 改寫題目：把題目換句話說多次、各跑一遍，任一版本成功就算解出。

## 資料集 NLP4LP（2023 版）
- 52 題：41 題 LP、11 題 MILP，取自最佳化教科書與講義。
- 每題附 SNOP、驗證測試、範例資料檔、最佳值與範例輸出。

## 結果
- v1 摘要：比基本提示策略多解出 67% 的題目。
- v2 摘要：解出的題目接近基本提示策略的兩倍；內文寫完整流程比直接提示的解題率提高 91%。
- 成功的執行平均產生 4117.1 ± 1509.7 個 token。
- 不含求解器時間，每次執行都在 7 分鐘內完成。
- 多做一兩次改寫或除錯後，效果就不太再提升。
- ICML 2024 版：在簡單資料集上比當時最好的方法高 20% 以上，在困難資料集上（包含新版 NLP4LP，題目較長、較複雜）高 30% 以上。

## 限制
- 除錯只修得了小錯，例如漏掉限制式或語法錯誤，修不了根本的建模錯誤。
- 一旦卡在錯誤的解空間，再多試幾次也很少有用。
- 用 GPT-3.5 時，自動產生的測試常常誤導，反而降低表現。
- 輸入必須是結構化的 SNOP，不能直接用一般文字。
- 資料集小，教科書題目可能已經出現在 LLM 的訓練資料中。
- 作者自稱這是概念驗證，未來要做微調與更大的資料集。

## 版本差異（閱讀時發現）
- 進步幅度：v1 寫 67%，v2 寫將近兩倍（內文 91%）。
- NLP4LP 題數：本論文 2023 版是 52 題，S1 綜述的表格列 269 題；ICML 2024 版提到新版 NLP4LP。
