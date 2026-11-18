---
title: 訓練與資料合成：讓 LLM 本身更會建模
type: topic
sources: [S1]
updated: 2026-11-19
---

# 訓練與資料合成：讓 LLM 本身更會建模

前面五站都是在「怎麼用」LLM。另一條研究路線是「讓 LLM 本身更會建模」。這一頁只做簡短介紹，內容都來自綜述 [S1]。

## 三種做法

| 做法 | 白話 | 例子 |
| --- | --- | --- |
| 資料合成 | 自動產生更多「題目＋模型」的練習資料 | 以問題為中心：OR-Instruct、LLMOPT；以模型為中心：MILP-Evolve、ReSocratic [S1] |
| 監督式微調 | 用這些資料再訓練 LLM | ORLM、Evo-Step-Instruct [S1] |
| 對齊 | 讓模型的輸出更符合偏好 | LLMOPT 使用 KTO [S1] |

## 效果

綜述以統一方式重測，微調過的 ORLM-LLaMA-3 8B 在 IndustryOR 得到 42.9%、在 ComplexLP 得到 59.5%，在較難的資料集上勝過 Chain-of-Experts [S1]。

## 還沒解決的問題

- 長的推理過程很難標註，綜述建議用求解器的回饋當作強化學習的獎勵 [S1]。
- 針對最佳化建模的訓練技術研究還不夠 [S1]。

和評估有關的問題見[怎麼評估一個系統](evaluation.md)。

**來源：** [S1](../../sources/S1-survey-2025.md)
