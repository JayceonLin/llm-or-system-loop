# 大綱 v3：怎麼做出一個用到 LLM 的 OR 系統

## 怎麼做出一個用到 LLM 的 OR 系統 {role=cover wiki=overview.md}
- **作業研究**（OR）系統把排產、配送、選址這類問題寫成數學模型，再算出最好的做法
- 加入大型語言模型（LLM）之後，系統可以自己讀懂文字、寫出模型與程式
- 教材來源：本專案的 Wiki，整理自來源論文與自製範例

## 學習目標：看完這份簡報，你能做到的事 {role=goals wiki=overview.md points=K01}
- 說出用到 LLM 的 OR 系統有哪五站，每一站在做什麼
- 用自製的手搖飲範例，看懂一題怎麼從文字走到答案，再回答 what-if（如果改成這樣會怎樣）
- 分辨 LLM 在系統裡的三種角色：翻譯者、最佳化器、解說員
- 說出怎麼評估一個系統，以及做這種系統的限制與設計建議

## 先備知識：模型有三個部分，交給求解器來算 {role=prereq wiki=system/02-modeling.md system/03-code-and-solver.md topics/glossary.md points=K07 K10 K02}
- **決策變數**：我們能決定的量，例如每天做幾杯紅茶
- **目標函數**：想讓它越大或越小越好的式子，例如利潤
- **限制式**：不能違反的條件，例如茶葉每天只有這麼多
- **求解器**：專門解最佳化模型的軟體，例如 Gurobi；它保證算出最好的答案，或告訴你這題無解
- **線性規劃**（LP）：目標函數和限制式都是一次式，變數可以是小數；**混合整數規劃**再規定某些變數只能是整數（自製術語表）

## 用到 LLM 的 OR 系統可以拆成五站 {role=concept wiki=overview.md points=K01}
- 過去寫模型需要專家，Gurobi 的使用者有 81% 具研究所學歷；加入 LLM 後，系統可以自己讀懂文字、寫出模型與程式
- 流程：問題輸入 → 建模 → 寫程式交給求解器 → 驗證與修正 → 解釋結果與 what-if（如果改成這樣會怎樣）

## 第 1 站：把文字題整理成有結構的資料 {role=concept wiki=system/01-problem-input.md topics/glossary.md points=K05 K06 K02}
- NL4Opt 競賽：標出 6 種元素：變數、參數（題目給的數字）、目標方向、目標名稱、限制方向、限制上限
- 這一項的第一名，**F1** 分數是 0.939；F1 同時考慮「標得準」和「沒漏標」，越接近 1 越好
- OptiMUS：使用者填 6 個欄位的 **SNOP**，數值另存成 **JSON** 檔（用「名稱：值」存資料的格式，自製術語表）
- 好處：長數據表不用塞進提示；代價：不能用一般文字輸入
- OptiMUS 把資料分開放，就是在做**抽象模型**：參數先用符號表示，數據之後再給

## 第 2 站：把元素寫成模型的三種做法 {role=concept wiki=system/02-modeling.md points=K08 K09}
- NL4Opt：先產生**意義表示**（邏輯形式的中間表示），再轉成求解器能讀的格式
- OptiMUS：LLM 寫出變數、限制式與目標，輸出給人和下一站都看得懂
- Chain-of-Experts：術語解釋、各部分擷取、建模知識補充、建模專家等好幾位專家分工；建模專家寫出完整的數學模型，通常是混合整數規劃
- NL4Opt 的準確率：建模第一名 UIUC-NLP 0.899、ChatGPT（gpt-3.5-turbo）合併任務 0.927
- 版本差異：依論文表格的數字，ChatGPT 比第一名高 2.8 個百分點；論文討論段寫的是高 2 個百分點

## 第 3 站：LLM 寫程式，真正的計算交給求解器 {role=concept wiki=system/03-code-and-solver.md topics/glossary.md points=K10 K11 K02}
- 為什麼這樣分工：LLM 擅長讀懂文字，求解器擅長精確計算
- 流程：LLM 寫呼叫求解器的程式 → 求解器精確計算
- OptiMUS 用 Gurobi 或 cvxpy 寫 Python 程式；Chain-of-Experts 寫 **LP 格式檔**（求解器可以直接讀的模型文字檔，自製術語表）與 Gurobi 程式；OptiGuide 的 **Coder** 把問題、背景與範例組成提示，讓 LLM 寫程式
- LLM 會算錯，也會重複產生以前的解；讓 LLM 直接找解的 OPRO，問題變大後就輸給專門的方法
- 成本：OptiMUS 成功的執行，不含求解器時間，每次都在 7 分鐘內完成；平均用掉 4117.1 ± 1509.7 個 **token**（LLM 讀寫文字時的計算單位，自製術語表）

## 第 4 站：錯了就帶著錯誤訊息重寫，但只修得了小錯 {role=concept wiki=system/04-verify-and-repair.md system/02-modeling.md topics/glossary.md points=K12 K13 K02}
- OptiMUS：LLM 自己產生**單元測試**（自動檢查結果的一小段程式，自製術語表），把執行錯誤與沒通過的測試交回 LLM 修正
- Chain-of-Experts：**評估器**（不是 LLM）執行程式與測試案例；錯了用**反向反思**，把專家倒過來逐一檢查
- OptiGuide：**Safeguard** 檢查 LLM 產生的程式，觸發自我除錯，或停下來回報錯誤
- 極限：漏掉限制式、語法錯誤修得好；一開始就想錯的模型修不了
- 其他極限：用 GPT-3.5 時，自動產生的測試常常誤導；多做一兩次改寫或除錯後，效果就不太再提升

## 第 5 站：把結果翻成白話，回答 what-if 問題 {role=concept wiki=system/05-explain-and-whatif.md points=K14 K15}
例如：某個需求改向供應商 B，成本會怎麼變？
- 流程：使用者用文字發問 → LLM 寫程式 → 求解器或資料庫執行 → **Interpreter** 讀取執行紀錄，寫成回答
註：寫程式前由 **Coder** 組提示，執行前由 **Safeguard** 檢查
- GPT-4 準確率：沒有給範例 59%；同類型題目給 5 或 10 個範例 92–93%；不同類型題目給 10 個範例 84%（隨機挑）、80%（挑最相近的）
- 實際部署：用在 Azure 的伺服器供應鏈；以前回答一個 what-if 問題，需要超過 3 位作業人員加上 1 位待命工程師

## 多代理人：讓好幾個代理人各負責一件事 {role=concept wiki=topics/multi-agent.md topics/glossary.md points=K17 K24 K02}
**代理人**是會自己決定下一步、使用工具的 AI 程式
OptiMUS：一個代理人照固定流程做：寫模型、寫程式、執行、測試、修正
- 流程：Chain-of-Experts 的**指揮者**（一個 LLM）依序挑專家 → 專家留下意見 → **彙整器**合成最後答案 → **評估器**（不是 LLM）執行程式與測試案例，把結果轉成回饋
- 代價：專家意見多了，會超過**上下文長度**（LLM 一次能讀進來的文字上限，自製術語表）
- 步驟越多，推理時間與 **API 呼叫**（程式透過網路請 LLM 服務做一次工作，自製術語表）越多

## LLM 的三種角色：翻譯者、最佳化器、解說員 {role=concept wiki=topics/llm-roles.md points=K16}
- **翻譯者**：把文字題變成模型與程式，交給求解器算；第 1～3 站，例如 NL4Opt、OptiMUS、Chain-of-Experts
- **最佳化器**：不寫模型，自己提出解，看分數再改進；不走五站，例如 OPRO
- **解說員**：模型已經有了，幫不會寫程式的人問 what-if，再翻成白話；第 3～5 站，例如 OptiGuide
- 設計時先決定角色：新問題要從頭建模用翻譯者；只能評分的問題可以考慮最佳化器，但它在大問題上有限制；公司已經有模型用解說員
- 三種角色都有「試、檢查、再改」的回圈
- 這個分法是本 Wiki 的整理，不是某一篇論文提出的

## 另一條路：OPRO 讓 LLM 直接提出解，看分數再改進 {role=concept wiki=topics/llm-as-optimizer.md system/03-code-and-solver.md points=K18}
- **元提示**裡放問題描述，以及之前產生過的解和分數
- 流程：LLM 根據元提示產生新的解，每一步最多 8 個 → 計算新解的分數 → 把新解與分數加進元提示
- **旅行推銷員問題**（拜訪每個城市一次、總路程最短）和最佳解的差距，越小越好：10 個城市 OPRO（gpt-4）0.0%、最遠插入法 3.2%；50 個城市 OPRO 11.0%、最遠插入法 9.8%；小問題表現不錯，從 20 個城市開始，最遠插入法比較好
- 主要用途是最佳化提示詞；作者說它不是要贏過專門的求解器，大問題也放不進提示

## 另一條研究路線：訓練 LLM 本身更會建模 {role=concept wiki=topics/training-and-data.md topics/evaluation.md overview.md points=K23}
- **資料合成**：自動產生更多「題目＋模型」的練習資料
- **監督式微調**：用這些資料再訓練 LLM
- **對齊**：讓模型的輸出更符合偏好
- 綜述（整理整個領域的方法、資料集與未來方向的論文）以統一方式重測，微調過的 ORLM-LLaMA-3 8B 在 IndustryOR 得到 42.9%、在 ComplexLP 得到 59.5%（兩份都是評估用的考卷），在較難的資料集上勝過 Chain-of-Experts
- 還沒解決：長的推理過程很難標註；針對最佳化建模的訓練技術研究還不夠

## 自製範例：手搖飲店一題走完五站 {role=example wiki=examples/tea-shop.md topics/glossary.md points=K03 K04}
- 題目（自製）：紅茶每杯利潤 20 元、奶茶每杯 30 元；每杯都用 10 公克茶葉，每天最多 5,000 公克；奶茶每杯另要 150 毫升鮮奶，每天最多 30,000 毫升
- 第 1 站標出變數、目標方向、參數與限制；第 2 站：x₁ = 紅茶杯數，x₂ = 奶茶杯數；最大化 20x₁ + 30x₂，限制 10x₁ + 10x₂ ≤ 5000、150x₂ ≤ 30000、x₁, x₂ ≥ 0，是一個**線性規劃**
- 第 3 站：求解器算出每天做紅茶 300 杯、奶茶 200 杯，利潤 12,000 元；程式用 PuLP 3.3.2 實際執行過
- 第 4 站：把答案代回去，茶葉和鮮奶都剛好用完
- 第 5 站 what-if：茶葉每天多進到 6,000 公克，紅茶變成 400 杯、奶茶仍是 200 杯，利潤變成 14,000 元

## 系統比較：沒有一個系統五站全包 {role=compare wiki=comparisons/systems.md overview.md points=K22}
- NL4Opt 做第 1、2 站，OptiMUS 做第 1～4 站，Chain-of-Experts 做第 2～4 站，OptiGuide 做第 3～5 站，OPRO 不走這五站
- 代表數字：OptiMUS 解出的題目接近基本提示的兩倍
- 版本差異：v1 摘要寫多解出 67%，v2 摘要寫接近兩倍，內文寫提高 91%
- 做系統時，可以從不同來源借每一站的做法
- 各系統的數字來自不同考卷、不同 LLM，不能拿來比誰比較強

## 評估：考卷不一定可靠，數字不能直接比 {role=pitfall wiki=topics/evaluation.md points=K19 K20 K21}
- **基準資料集**是大家共用的考卷；綜述請 11 位專家重新檢查
- 錯誤率至少有 NL4Opt 26.4%、IndustryOR 54.0%；除了 EasyLP，每個資料集都超過 15%
- 錯誤來源：題目有邏輯漏洞、參數定義不清、標準答案本身是錯的
- 判斷對錯：**比目標值**只比最佳值，模型錯了也可能剛好算出相同的值；**比模型**比較係數或相似分數
- Chain-of-Experts 的準確率：原論文用 GPT-4，基礎題 LPWP 64.2%、複雜題 ComplexOR 31.4%；綜述改用 GPT-4o 重測，EasyLP 94.4%
- 用的 LLM、考卷不同，數字不能直接比。先確認考卷可不可靠，再說明用了哪個 LLM、哪份考卷

## 限制與設計建議：計算交給求解器，驗證交給程式 {role=pitfall wiki=topics/risks-and-design.md points=K24 K25}
- 限制：模型可能一開始就想錯；題目越複雜，正確率越低
- 把公司資料直接交給 LLM 有外流風險；OptiGuide 讓資料留在求解器與資料庫
- 建議：計算交給求解器，不讓 LLM 心算；驗證交給不是 LLM 的程式；錯了要帶著錯誤訊息重做
- 設定重試上限、能停下來回報、保留人的判斷，並用可靠的題目評估
- 做這份簡報的流程也照這些建議設計：產生者和驗證者分開、每一步都有重做次數上限、關鍵處停下來給人確認

## 小測驗：計算、驗證與評估 {role=quiz wiki=system/03-code-and-solver.md system/04-verify-and-repair.md system/02-modeling.md topics/evaluation.md points=K10 K13 K21}
- Q1　LLM 寫好程式之後，為什麼真正的計算要交給求解器？答案：LLM 擅長讀懂文字，求解器擅長精確計算；LLM 會算錯
- Q2　驗證回圈修得好哪種錯、修不了哪種錯？答案：漏掉限制式、語法錯誤修得好；一開始就想錯的模型修不了
- Q3　兩篇論文的準確率，可以直接拿來比誰比較強嗎？答案：不行。用的 LLM 不同、考卷不同，數字不能直接比

## 總結：做 LLM × OR 系統的五個重點 {role=summary wiki=overview.md system/03-code-and-solver.md system/04-verify-and-repair.md topics/risks-and-design.md topics/llm-roles.md topics/evaluation.md points=K01 K10 K13 K25 K16 K21}
- 用到 LLM 的 OR 系統可以拆成五站：問題輸入、建模、寫程式交給求解器、驗證與修正、解釋結果與 what-if
- LLM 擅長讀懂文字，負責寫模型與程式；計算交給求解器，不讓 LLM 心算
- 驗證回圈只修得了小錯，一開始就想錯的模型修不了
- 驗證交給不是 LLM 的程式，設定重試上限、能停下來回報，保留人的判斷
- 設計時先決定 LLM 當翻譯者、最佳化器還是解說員；評估時先確認考卷可不可靠，數字不能直接比

## 資料來源：6 篇來源，加上自製的範例與術語表 {role=refs wiki=references.md overview.md examples/tea-shop.md topics/glossary.md}
- S1 綜述：Ziyang Xiao 等，“A Survey of Optimization Modeling Meets LLMs: Progress and Future Directions”，IJCAI 2025，arXiv:2508.10047
- S2 NL4Opt 競賽：Rindranirina Ramamonjison 等，“NL4Opt Competition: Formulating Optimization Problems Based on Their Natural Language Descriptions”，NeurIPS 2022 競賽報告，arXiv:2303.08233
- S3 OptiMUS：Ali AhmadiTeshnizi 等，“OptiMUS: Optimization Modeling Using MIP Solvers and large language models”，arXiv:2310.06116（2023）；後續版本發表於 ICML 2024
- S4 Chain-of-Experts：Ziyang Xiao 等，“Chain-of-Experts: When LLMs Meet Complex Operations Research Problems”，ICLR 2024
- S5 OPRO：Chengrun Yang 等，“Large Language Models as Optimizers”，Google DeepMind，arXiv:2309.03409（2023）
- S6 OptiGuide：Beibin Li 等，“Large Language Models for Supply Chain Optimization”，Microsoft，arXiv:2307.03875（2023）
註：手搖飲範例與新手術語表是自製內容，不是來自這 6 篇來源
