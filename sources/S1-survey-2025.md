---
id: S1
title: "A Survey of Optimization Modeling Meets LLMs: Progress and Future Directions"
authors: Ziyang Xiao, Jingrong Xie, Lilin Xu 等 18 位（通訊作者 Dongxiang Zhang）
affiliation: 浙江大學、華為諾亞方舟實驗室、新加坡新躍社會科學大學
year: 2025
venue: IJCAI 2025（頁 10742–10750，doi:10.24963/IJCAI.2025/1192）；arXiv:2508.10047（2025-08-12）
url: https://arxiv.org/abs/2508.10047
license: CC BY 4.0
read: arXiv HTML 全文
captured: 2026-11-18
---

# S1 擷取筆記（不可修改）

## 任務定義
- 最佳化建模：把自然語言的問題描述轉成數學模型。
- 標準形式：決策變數 x、要最小化的目標 f(x)、不等式限制 g_i(x) ≤ 0、等式限制 h_j(x) = 0。
- 區分兩種模型：抽象模型（參數用符號，數據之後再給）與具體模型（數值直接寫在題目裡）。
- LLM 的輸出可以是可執行的求解器程式，也可以是結構化的模型文件。
- 綜述把整個流程分成四步：資料準備與微調、推論、基準測試、評估。
- Gurobi 的使用者調查：81% 有研究所學歷，將近一半專攻作業研究。

## 方法分類與代表系統
- 資料合成
  - 以問題為中心：OR-Instruct、LLMOPT、Evo-Step-Instruct。
  - 以模型為中心：MILP-Evolve、OptiBench、ReSocratic。
- 微調
  - 監督式微調：ORLM、RareMIP、Evo-Step-Instruct。
  - 對齊：LLMOPT 使用 KTO。
- 推論
  - 提示類：NL4Opt 是第一個用 ChatGPT 提示的方法，其他還有 ORLM、LLMOPT 等。
  - X-of-Thought 類：思維鏈（Chain-of-Thought）、思維樹、思維圖、CAFA、Autoformulation（蒙地卡羅樹搜尋）。
  - 多專家（多代理人）類：OptiMUS、Chain-of-Experts、OptiGuide、OptLLM、EOR。

## 基準資料集與錯誤率（綜述表 1）

| 資料集 | 題數 | 平均複雜度 | 錯誤率（至少） |
| --- | --- | --- | --- |
| NL4Opt | 289 | 5.59 | 26.4% |
| IndustryOR | 100 | 14.06 | 54.0% |
| EasyLP（MAMO） | 652 | 7.12 | 8.13% |
| ComplexLP（MAMO） | 211 | 13.35 | 23.7% |
| ReSocratic | 605 | 7.45 | 16.0% |
| NLP4LP | 269 | 5.58 | 21.7% |
| ComplexOR | 37 | 5.98 | 24.3% |

- 除了 EasyLP，每個資料集的錯誤率都超過 15%，綜述認為因此不適合直接拿來評估。
- 錯誤的來源：題目敘述有邏輯漏洞、參數定義不清、標準答案本身是錯的。
- 由 11 位專家找錯，每一題至少 3 人交叉確認。
- 大部分題目屬於簡單或中等複雜度，複雜度超過 10 的很少。
- 其他資料集：OptiBench（816 題抽象模型，沒有錯誤率）、WIQOR（what-if 分析）。

## 評估方式
- 比目標值：只比較求解器算出的最佳值和標準答案（來自 Chain-of-Experts）。缺點是模型錯了也可能剛好算出相同的值。
- 比模型：比較係數矩陣（來自 NL4Opt），或用圖編輯距離算出 0 到 1 的分數。
- 綜述的統一重測以 GPT-4o 為基礎模型，報告準確率。
- 重測結果
  - Chain-of-Experts：EasyLP 94.4%、NLP4LP 87.4%。
  - ORLM-LLaMA-3 8B：IndustryOR 42.9%、ComplexLP 59.5%，在較難的資料集上勝過 Chain-of-Experts。
  - 思維鏈有時反而比一般提示差。

## 限制與未來方向
- 推理模型：長思維鏈資料很難標註，建議用求解器回饋當強化學習的獎勵。
- 可解釋性：多數方法是端到端的黑箱，需要更可信、更好用的框架。
- 領域知識：如何結合知識圖譜仍待研究。
- 人機協作：系統要能判斷何時需要人介入，並讓專家方便補充知識。
- 基準與評估：資料品質差、複雜題少、評估方式不一致，開源資源也有限。
- 訓練方法：針對最佳化建模的新訓練技術研究不足。
