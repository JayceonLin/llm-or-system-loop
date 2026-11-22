# 生成簡報要遵循的 prompt

這份文件是 Agent C（排大綱）與 Agent B（寫投影片）共同遵循的規則。驗證者 V2 也照這份文件判斷。

---

你要做的是一份**教學 HTML 簡報**，主題是「怎麼做出一個用到 LLM 的作業研究（OR）系統」。

## 1. 讀者與目標

- 讀者是**完全的新手**：用過 ChatGPT，但沒學過作業研究，也沒寫過最佳化模型。
- 看完簡報，讀者要能說出系統的五站在做什麼、看懂一個完整的小例子，並知道做這種系統要注意什麼。
- **唯一的知識來源是 `wiki/`。** 簡報上的每一個數字、每一個專有名詞、每一個主張，都必須寫在你引用的 Wiki 頁面裡。Wiki 沒寫的，就不要寫。

## 2. 教學結構

投影片依序包含下列角色（`data-role`），總共 14 到 20 張：

| 順序 | 角色 | 張數 | 內容 |
| --- | --- | --- | --- |
| 1 | `cover` | 1 | 標題、一句話說明、教材來源 |
| 2 | `goals` | 1 | 學習目標 3 到 5 點，每點都是看完能做到的事 |
| 3 | `prereq` | 1 到 2 | 先備知識：最佳化模型的三個部分、求解器是什麼 |
| 4 | `concept` | 至少 3 | 系統的五站、跨站的主題，一張只講一個概念 |
| 5 | `example` | 1 到 2 | 自製手搖飲範例，並標明「自製」 |
| 6 | `compare` | 1 | 系統比較 |
| 7 | `pitfall` | 1 到 2 | 評估與限制、設計建議 |
| 8 | `quiz` | 1 | 2 到 3 題，點題目才顯示答案 |
| 9 | `summary` | 1 | 3 到 5 點 |
| 10 | `refs` | 1 | 6 篇來源 |

**教學順序：** 先講讀者需要的背景，再講用到它的概念；術語第一次出現時，用一句白話解釋。

## 3. 每張投影片的規則

- **S1 對應 Wiki：** `<section>` 必須有 `data-wiki`（用到的 Wiki 頁面，路徑從 `wiki/` 底下算起）與 `data-points`（這張講的重點編號，例如 `K03 K04`）。封面與資料來源可以不寫 `data-points`。
- **S2 可追溯：** 投影片上的每一個數字，以及每一個 `<strong>` 標出的術語，都必須一字不差地出現在 `data-wiki` 列出的頁面。數字的範圍、單位、版本要和 Wiki 一致，例如 Wiki 寫「92–93%」，就不能寫成「93%」。Wiki 有「版本差異」時，要嘛兩個數字都寫，要嘛都不寫。
- **S4 份量：** 最多 6 個 `<li>`（流程圖的每一步也算一個），中文字不超過 180 字。
- **S5 版面：** 只能用第 4 節的元件，不能寫 `style` 屬性、`<script>`、外部圖片。內容要能放進 1280×720 的畫面，手機上也不能出現整頁橫向捲動。180 字是上限，不是目標；表格、兩欄、流程圖都很佔高度。**每一張都必須通過 `python3 loop/check.py render-slide <檔案>`**，它會把這一張套進外框，實際量桌面與手機版面。
- **S6 重點與圖例（run-02 新增，只適用 `concept`）：**
  - 剛好 1 個重點框 `<p class="key">`，寫這張最該記住的一句話，通常就是標題的白話版或結論。
  - 螢光標示 `<em class="hi">` 最多 2 處，只標關鍵短語（例如「精確計算」「提高到 92–93%」）。**術語仍然用 `<strong>`**，兩者不要混用。
  - 至少一個圖：五站大圖、流程圖、長條圖、兩欄或三欄、表格。能畫成圖的就不要寫成一串列點，例如先後順序畫成流程圖、數字比較畫成長條圖。
  - 標題是「第 N 站：……」的投影片，要在 `<h2>` 上方放五站地圖，`here` 標在這一站，前面的站標 `done`。地圖不算進 180 字。
  - 流程圖的方塊用顏色標出**誰負責**（`llm`、`solver`、`check`、`person`），並在上方放 `<p class="legend">` 說明顏色。顏色要和 Wiki 寫的分工一致，例如 Chain-of-Experts 的評估器不是 LLM，就不能標成 `llm`。
- **一張一件事：** 標題直接說出這張的重點，例如「第 3 站：計算交給求解器」，不要只寫「第 3 站」。

## 4. 可用的元件

每張投影片的外層固定是：

```html
<section class="slide" data-role="concept" data-wiki="system/03-code-and-solver.md" data-points="K07 K08">
  <div class="slide-body">
    <h2>標題</h2>
    ……內容……
  </div>
</section>
```

頁尾的 Wiki 連結會在組裝時自動加上，**不要自己寫 `<footer>`**。

| 元件 | HTML | 用途 |
| --- | --- | --- |
| 封面標題 | `<div class="slide-body cover"><h1>…</h1><p class="sub">…</p>…<p class="meta">…</p></div>` | 只用在 cover |
| 大段落 | `<p class="lead">` | 這張的主要一句話 |
| 補充 | `<p class="note">`、`<p class="small">` | 次要說明、出處說明 |
| 列點 | `<ul>`、`<ol class="steps">` | `steps` 用在有先後順序的步驟 |
| 流程圖 | `<ol class="flow"><li>…</li><li class="solver">…</li></ol>` | 箭頭自動產生；`solver` 是深色方塊；最後一步要回到第一步時用 `<ol class="flow loop">` |
| 兩欄、三欄 | `<div class="cols two">`、`<div class="cols">`，裡面放 `<div class="part">`；要底色加 `soft` | 並列比較 |
| 欄標題 | `<h3>` | 兩欄、三欄裡每一欄的小標題 |
| 模型三部分 | `<div class="part var">`、`part obj`、`part con` | 決策變數、目標、限制式的固定顏色 |
| 螢光筆 | `<mark class="var">`、`obj`、`con` | 在文字裡標出變數、目標、限制 |
| 表格 | `<div class="table-wrap"><table>…</table></div>`；比較表加 `<table class="wide">`；數字欄加 `class="num"` | 資料表 |
| 表格說明 | `<p class="caption">` | 放在表格上方 |
| 大數字 | `<div class="split"><div><div class="stat">81%</div><p class="stat-label">…</p></div><ul>…</ul></div>` | 一張最多一個 |
| 題目框、模型框 | `<p class="problem">`、`<div class="model">` | 例題的題目與數學模型 |
| 程式碼 | `<pre><code>…</code></pre>`，`<` 寫成 `&lt;` | 例題程式 |
| 結論 | `<p class="answer">` | 例題答案、這張的結論 |
| 角色標籤 | `<span class="tag t">翻譯者</span>`、`tag o` 最佳化器、`tag e` 解說員 | 放在 `<h2>` 開頭 |
| 測驗 | `<details><summary>Q1　題目</summary><p>答案與一句理由</p></details>` | 只用在 quiz |
| 書目 | `<ul class="refs">` | 只用在 refs，字比較小 |
| 不換行 | `<span class="nw">GPT-4o</span>` | 型號、帶連字號的名稱 |
| 間距 | 在元素上加 `class="mt"` | 和上一塊拉開距離 |
| 重點框 | `<p class="key">一句話</p>` | 一張一個；畫面上會自動加「重點」標籤（S6） |
| 重點螢光 | `<em class="hi">短語</em>` | 一張最多兩處，不能用在術語上（S6） |
| 五站地圖 | `<div class="map" aria-label="目前在第 3 站"><span class="done">問題輸入</span><span class="done">建模</span><span class="here">寫程式交給求解器</span><span>驗證與修正</span><span>解釋結果</span></div>` | 放在站別投影片的 `<h2>` 上方，5 個 `<span>` 照順序 |
| 五站大圖 | `<div class="stations" role="img" aria-label="…"><div class="llm"><b>站名</b><small>一句說明</small></div>…</div>` | 5 個 `<div>`，編號與箭頭自動產生；`llm`、`solver`、`check`、`person` 標出誰負責 |
| 誰負責 | 流程圖 `<li class="llm">`、`solver`、`check`、`person`，搭配 `<p class="legend"><span class="llm">LLM</span><span class="solver">求解器</span><span class="check">程式檢查</span><span class="person">使用者</span></p>` | 圖例只列這張有用到的顏色；不加 class 的 `<span>` 會畫成白底方塊，用來說明白底的意思 |
| 回圈 | `<ol class="flow loop">` | 下方自動畫一條虛線「回到第一步」，用在會重複的步驟 |
| 長條圖 | `<p class="caption">說明</p><div class="bars" role="img" aria-label="…"><p class="bar v59"><span>標籤</span><i></i><b>59%</b></p>…</div>` | `vNN` 是長條長度（0～100，取整數），`<b>` 寫 Wiki 上的原始數值；最想強調的那一條加 `best`。一張最多 4 條 |

## 5. 文字風格

- 繁體中文、台灣用語、全形標點；中文與英文、數字之間空一個半形空格。
- 對讀者說話，用「你」。句子短，一句只講一件事。
- 不誇大：不用「革命性」「完美」「顯著」這類詞，不用驚嘆號，不用 emoji。
- 自製內容（手搖飲範例）要在投影片上寫出「自製」。
