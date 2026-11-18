#!/usr/bin/env python3
"""LLM Wiki → 教學簡報 Loop 的程式檢查。驗證者（V1、V2）與 Agent C 會呼叫這些指令，規則見 loop/LOOP.md。

用法（都可以加 --run runs/<run>，結果會附加到該次執行的 checks.jsonl）：
  python3 loop/check.py new-run                              建立 runs/<日期>-run-NN/
  python3 loop/check.py lint                                 P0：Wiki 健康檢查（連結、目錄、引用核對）
  python3 loop/check.py check-keypoints <重點清單>            V1：重點清單的格式、可追溯與頁面涵蓋
  python3 loop/check.py check-outline <大綱> --keypoints <重點清單>
                                                             V2：大綱的結構、份量、可追溯與重點涵蓋
  python3 loop/check.py check-slide <單張投影片> --keypoints <重點清單>
                                                             V2：單張投影片的 S1、S2、S4、S5
  python3 loop/check.py build --run <run>                    C：把 <run>/slides/ 組成 slides/index.html
  python3 loop/check.py check-slides --keypoints <重點清單>   V2：整份簡報的結構、重複與重點涵蓋
  python3 loop/check.py render                               V2：桌面 1280×720 與手機版面，加 --run 時存截圖
"""
import datetime as dt
import html as htmllib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "sources"
SLIDES = ROOT / "slides" / "index.html"
TYPES = {"step", "topic", "comparison", "example", "overview", "index", "log"}
ROLE_ORDER = ["cover", "goals", "prereq", "concept", "example", "compare", "pitfall", "quiz", "summary", "refs"]
NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")


# ---------- 共用 ----------
def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def body_of(text):
    return re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)


def wiki_pages():
    return sorted(p for p in WIKI.rglob("*.md"))


def rel(p):
    return p.relative_to(ROOT).as_posix()


def numbers_in(text):
    return {n.replace(",", "") for n in NUM_RE.findall(text)}


def record(run_dir, node, errors, extra=None):
    status = "pass" if not errors else "fail"
    print(f"\n[{node}] {'✓ 通過' if not errors else f'✗ {len(errors)} 個錯誤'}")
    for e in errors:
        print("  ✗", e)
    if run_dir:
        d = ROOT / run_dir
        d.mkdir(parents=True, exist_ok=True)
        rec = {
            "time": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "node": node,
            "status": status,
            "n_errors": len(errors),
            "errors": errors,
        }
        if extra:
            rec.update(extra)
        with open(d / "checks.jsonl", "a", encoding="utf8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return 0 if not errors else 1


# ---------- N4：Wiki lint ----------
def lint():
    errors = []
    pages = wiki_pages()
    raw_ids = sorted(p.name.split("-")[0] for p in RAW.glob("S*.md"))
    link_targets = {}  # page -> set of pages linking to it
    raw_nums = {p.name.split("-")[0]: numbers_in(p.read_text(encoding="utf8")) for p in RAW.glob("S*.md")}

    for p in pages:
        text = p.read_text(encoding="utf8")
        name = rel(p)
        fm = front_matter(text)
        if fm is None:
            errors.append(f"{name}：缺少 front matter（AGENTS.md 第 3 節）")
            continue
        for key in ("title", "type", "sources", "updated"):
            if key not in fm:
                errors.append(f"{name}：front matter 缺少 {key}")
        if fm.get("type") and fm["type"] not in TYPES:
            errors.append(f"{name}：type「{fm['type']}」不合法")
        for sid in re.findall(r"S\d+|自製", fm.get("sources", "")):
            if sid != "自製" and sid not in raw_ids:
                errors.append(f"{name}：front matter 引用了不存在的來源 {sid}")

        body = body_of(text)
        # 連結
        for target in re.findall(r"\]\(([^)\s]+)\)", body):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            path = (p.parent / target.split("#")[0]).resolve()
            if not path.exists():
                errors.append(f"{name}：連結 {target} 不存在")
            elif path.suffix == ".md" and WIKI in path.parents:
                link_targets.setdefault(path, set()).add(p.resolve())
        # 引用：含數字的句子要標來源（範例頁可用 [自製]）
        in_code = False
        for i, line in enumerate(body.splitlines(), 1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code or not line.strip() or line.lstrip().startswith("#") or re.match(r"^\|?\s*-+", line):
                continue
            if fm.get("type") in ("index", "log"):
                continue
            scrub = re.sub(r"^\s*(>\s*)?\d+\.\s", "", line)     # 編號清單的「1. 」
            scrub = re.sub(r"\]\([^)]*\)", "]", scrub)        # 連結網址
            scrub = re.sub(r"\[[^\]]*(/|\.md)[^\]]*\]", "", scrub)  # 連結文字是檔名或路徑
            scrub = re.sub(r"第 ?\d+ ?(到|、|～) ?第? ?\d+ ?站", "", scrub)  # 「第 1 到第 5 站」
            scrub = re.sub(r"第 ?\d+ ?[步課節列張站]", "", scrub)    # 「第 4 步」「第 1 站」這類序號
            scrub = re.sub(r"NL4Opt|NLP4LP|LLaMA-\d", "", scrub)     # 名稱裡的數字
            scrub = re.sub(r"`[^`]*`", "", scrub)               # 行內程式碼
            scrub = re.sub(r"\[(S\d+|自製)\]", "", scrub)        # 引用標記本身
            scrub = re.sub(r"\bS\d+\b", "", scrub)              # 來源編號
            scrub = re.sub(r"GPT-\d(\.\d)?|LLaMA-\d|Claude\d|gpt-\d(\.\d)?(-turbo)?|o1|4o", "", scrub)
            if re.search(r"\d", scrub) and not re.search(r"\[(S\d+|自製)\]", line):
                errors.append(f"{name}:{i}：含數字但沒有標來源 → {line.strip()[:50]}")
            # 引用核對：句子裡的數字必須出現在它引用的 raw/ 資料卡（自製內容除外）
            cites = set(re.findall(r"\[(S\d+)\]", line))
            if cites and "[自製]" not in line:
                pool = set().union(*(raw_nums.get(c, set()) for c in cites))
                miss = sorted(n for n in numbers_in(scrub) if n not in pool)
                if miss:
                    errors.append(f"{name}:{i}：數字 {'、'.join(miss)} 不在引用的資料卡 {'、'.join(sorted(cites))} 裡 → {line.strip()[:40]}")

    # 孤兒頁與 index
    index = WIKI / "index.md"
    index_links = set()
    if index.exists():
        for target in re.findall(r"\]\(([^)\s]+)\)", index.read_text(encoding="utf8")):
            index_links.add((WIKI / target.split("#")[0]).resolve())
    else:
        errors.append("wiki/index.md 不存在")
    for p in pages:
        rp = p.resolve()
        if p.name in ("index.md",):
            continue
        if rp not in index_links:
            errors.append(f"{rel(p)}：沒有列在 index.md")
        if p.name == "log.md":
            continue
        others = {q for q in link_targets.get(rp, set()) if q.name not in ("index.md", "log.md") and q != rp}
        if not others:
            errors.append(f"{rel(p)}：孤兒頁，除了 index.md 之外沒有任何頁面連到它")

    # raw → sources → log
    log_text = (WIKI / "log.md").read_text(encoding="utf8") if (WIKI / "log.md").exists() else ""
    for sid in raw_ids:
        if not re.search(rf"^## \[\d{{4}}-\d\d-\d\d\] ingest \| {sid}\b", log_text, re.M):
            errors.append(f"sources/{sid}：log.md 沒有「## [日期] ingest | {sid} …」紀錄")
    return errors


# ---------- 簡報解析 ----------
REPO_BLOB = "https://github.com/JayceonLin/llm-or-system-loop/blob/main/wiki/"
SECTION_RE = re.compile(r'<section class="slide"([^>]*)>(.*?)</section>', re.S)


def attr(attrs, name):
    m = re.search(rf'{name}="([^"]*)"', attrs)
    return m.group(1) if m else ""


def parse_slides(html_text):
    slides = []
    for m in SECTION_RE.finditer(html_text):
        attrs, inner = m.group(1), m.group(2)
        footer = (re.search(r'<footer class="slide-src">(.*?)</footer>', inner, re.S) or [None, ""])[1]
        main = re.sub(r'<footer class="slide-src">.*?</footer>', " ", inner, flags=re.S)
        text = htmllib.unescape(re.sub(r"<[^>]+>", " ", main))
        strongs = [htmllib.unescape(re.sub(r"<[^>]+>", "", s)).strip() for s in re.findall(r"<strong>(.*?)</strong>", main, re.S)]
        title = htmllib.unescape(re.sub(r"<[^>]+>", "", (re.search(r"<h[12][^>]*>(.*?)</h[12]>", main, re.S) or [None, ""])[1])).strip()
        slides.append({"role": attr(attrs, "data-role"), "wiki": attr(attrs, "data-wiki").split(),
                       "points": attr(attrs, "data-points").split(), "footer": footer, "text": text,
                       "strong": strongs, "bullets": len(re.findall(r"<li[\s>]", main)), "title": title,
                       "inline_style": bool(re.search(r"\sstyle=", main)), "script": "<script" in main})
    return slides


def trace_errors(label, text, strongs, wiki_paths):
    """S2：數字與粗體術語必須出現在列出的 Wiki 頁面（只比對正文，不含連結路徑與來源標記）。"""
    errors = []
    corpus = ""
    for w in wiki_paths:
        f = WIKI / w
        if f.exists():
            corpus += body_of(f.read_text(encoding="utf8")) + "\n"
    scrub = re.sub(r"\]\([^)]*\)", "]", corpus)
    scrub = re.sub(r"\[[^\]]*(/|\.md)[^\]]*\]", "", scrub)
    scrub = re.sub(r"\[S\d\]|\bS\d\b", "", scrub)
    corpus_nums = numbers_in(scrub)
    for n in sorted(numbers_in(text)):
        if n not in corpus_nums:
            errors.append(f"{label}：數字 {n} 不在列出的 Wiki 頁面裡（S2）")
    for s in strongs:
        if s and s.lower() not in corpus.lower():
            errors.append(f"{label}：術語「{s}」不在列出的 Wiki 頁面裡（S2）")
    return errors


def structure_errors(roles, label="簡報"):
    """S3：教學結構。"""
    errors = []
    if not roles:
        return [f"{label}：沒有任何投影片"]
    if roles[0] != "cover":
        errors.append(f"{label}：第 1 張必須是 cover")
    if len(roles) < 2 or roles[1] != "goals":
        errors.append(f"{label}：第 2 張必須是 goals（學習目標）")
    for r in ROLE_ORDER:
        if r not in roles:
            errors.append(f"{label}：缺少 {r} 投影片（S3）")
    if roles.count("concept") < 3:
        errors.append(f"{label}：concept 至少要 3 張，目前 {roles.count('concept')} 張（S3）")
    for r in roles:
        if r not in ROLE_ORDER:
            errors.append(f"{label}：未知的 data-role「{r}」")
    if "prereq" in roles and "concept" in roles and roles.index("prereq") > roles.index("concept"):
        errors.append(f"{label}：prereq 要放在第一張 concept 之前（S3）")
    tail = [r for r in roles if r in ("quiz", "summary", "refs")]
    if tail != ["quiz", "summary", "refs"] or roles[-1] != "refs":
        errors.append(f"{label}：最後三種投影片的順序要是 quiz → summary → refs（S3）")
    return errors


def slide_errors(label, s, key_ids=None):
    """單張投影片的 S1、S2、S4 檢查（V2 的程式部分）。"""
    errors = []
    if s["role"] not in ROLE_ORDER:
        errors.append(f"{label}：data-role「{s['role']}」不合法（S3）")
    if not s["wiki"]:
        errors.append(f"{label}：沒有 data-wiki（S1）")
    for w in s["wiki"]:
        if not (WIKI / w).exists():
            errors.append(f"{label}：data-wiki 的 {w} 不存在（S1）")
    if s["role"] not in ("cover", "refs") and not s["points"]:
        errors.append(f"{label}：沒有 data-points，看不出這張講哪些重點（S1）")
    if key_ids is not None:
        for k in s["points"]:
            if k not in key_ids:
                errors.append(f"{label}：data-points 的 {k} 不在重點清單裡（S1）")
    errors += trace_errors(label, s["text"], s["strong"], s["wiki"])
    if s["bullets"] > 6:
        errors.append(f"{label}：{s['bullets']} 個列點，最多 6 個（S4）")
    cjk = len(re.findall(r"[一-鿿]", s["text"]))
    if cjk > 180:
        errors.append(f"{label}：中文 {cjk} 字，最多 180 字（S4）")
    if s["inline_style"] or s["script"]:
        errors.append(f"{label}：不能寫 style 屬性或 <script>，只能用規定的元件（S5）")
    return errors


# ---------- 重點清單 ----------
KEY_RE = re.compile(r"^## (K\d{2}) (.+?)\s*\{wiki=([^}]*)\}\s*$")


def parse_keypoints(text):
    points, cur = [], None
    for line in text.splitlines():
        m = KEY_RE.match(line)
        if m:
            cur = {"id": m.group(1), "title": m.group(2).strip(), "wiki": m.group(3).split(), "lines": []}
            points.append(cur)
        elif cur is not None and line.strip().startswith("- "):
            cur["lines"].append(line.strip()[2:])
    return points


def load_key_ids(path):
    if not path:
        return None
    f = ROOT / path
    return [k["id"] for k in parse_keypoints(f.read_text(encoding="utf8"))] if f.exists() else []


def check_keypoints(path):
    f = ROOT / path
    if not f.exists():
        return [f"{path} 不存在"]
    points = parse_keypoints(f.read_text(encoding="utf8"))
    errors = []
    if not points:
        return [f"{path}：找不到任何「## Kxx 標題 {{wiki=頁面}}」格式的重點"]
    seen = set()
    used_pages = set()
    for k in points:
        label = f"重點 {k['id']}「{k['title'][:14]}」"
        if k["id"] in seen:
            errors.append(f"{label}：編號重複")
        seen.add(k["id"])
        if not k["wiki"]:
            errors.append(f"{label}：沒有 wiki=")
        for w in k["wiki"]:
            if not (WIKI / w).exists():
                errors.append(f"{label}：wiki 頁面 {w} 不存在")
            used_pages.add(w)
        if not k["lines"]:
            errors.append(f"{label}：底下沒有任何「- 」說明")
        text = k["title"] + "\n" + "\n".join(k["lines"])
        errors += trace_errors(label, text.replace("**", ""), re.findall(r"\*\*(.+?)\*\*", text), k["wiki"])
    for p in wiki_pages():
        fm = front_matter(p.read_text(encoding="utf8")) or {}
        if fm.get("type") in ("index", "log"):
            continue
        r = p.relative_to(WIKI).as_posix()
        if r not in used_pages:
            errors.append(f"wiki/{r}：沒有任何重點引用這一頁（完整度）")
    return errors


# ---------- 大綱 ----------
OUTLINE_SLIDE = re.compile(r"^## (.+?)\s*\{([^}]*)\}\s*$")


def parse_outline(text):
    """大綱格式：每張投影片一個「## 標題 {role=… wiki=頁面 頁面 points=K01 K02}」，底下用「- 」寫列點。
    「- 流程：A → B → C」這種流程圖，每一步都算一個列點。"""
    slides, cur = [], None
    for line in text.splitlines():
        m = OUTLINE_SLIDE.match(line)
        if m:
            a = m.group(2)
            role = (re.search(r"role=(\S+)", a) or [None, ""])[1]
            wiki = (re.search(r"wiki=(.*?)(?=\s+points=|$)", a) or [None, ""])[1].split()
            pts = (re.search(r"points=(.*)$", a) or [None, ""])[1].split()
            cur = {"title": m.group(1).strip(), "role": role, "wiki": wiki, "points": pts, "lines": [], "items": 0}
            slides.append(cur)
        elif cur is not None and line.strip():
            body = line.strip()
            if body.startswith("- "):
                body = body[2:]
                if re.match(r"^流程[：:]", body):
                    cur["items"] += len(re.split(r"\s*[→↺]\s*", re.sub(r"^流程[：:]", "", body).strip(" →↺")))
                else:
                    cur["items"] += 1
            cur["lines"].append(body)
    return slides


def check_outline(path, keypoints=None):
    f = ROOT / path
    if not f.exists():
        return [f"{path} 不存在"]
    slides = parse_outline(f.read_text(encoding="utf8"))
    key_ids = load_key_ids(keypoints)
    errors = []
    covered = set()
    for i, s in enumerate(slides, 1):
        label = f"大綱第 {i} 張「{s['title'][:16]}」"
        text = s["title"] + "\n" + "\n".join(s["lines"])
        strongs = re.findall(r"\*\*(.+?)\*\*", text)
        plain = text.replace("**", "")
        if not s["wiki"]:
            errors.append(f"{label}：沒有 wiki=（S1）")
        for w in s["wiki"]:
            if not (WIKI / w).exists():
                errors.append(f"{label}：wiki 頁面 {w} 不存在（S1）")
        if s["role"] not in ("cover", "refs") and not s["points"]:
            errors.append(f"{label}：沒有 points=（S1）")
        for k in s["points"]:
            covered.add(k)
            if key_ids is not None and k not in key_ids:
                errors.append(f"{label}：points 的 {k} 不在重點清單裡")
        errors += trace_errors(label, plain, strongs, s["wiki"])
        if s["items"] > 6:
            errors.append(f"{label}：{s['items']} 個列點（流程每一步都算），最多 6 個（S4）")
        cjk = len(re.findall(r"[一-鿿]", plain))
        if cjk > 180:
            errors.append(f"{label}：中文 {cjk} 字，最多 180 字（S4）")
    if key_ids:
        for k in key_ids:
            if k not in covered:
                errors.append(f"重點 {k} 沒有出現在任何一張投影片的 points（完整度）")
    errors += structure_errors([s["role"] for s in slides], "大綱")
    return errors


# ---------- 單張、組裝、整份 ----------
def check_slide(path, keypoints=None):
    f = ROOT / path
    if not f.exists():
        return [f"{path} 不存在"]
    slides = parse_slides(f.read_text(encoding="utf8"))
    if len(slides) != 1:
        return [f"{path}：一個檔案只能有一個 <section class=\"slide\">，目前 {len(slides)} 個"]
    return slide_errors(f"{f.name}「{slides[0]['title'][:16]}」", slides[0], load_key_ids(keypoints))


def footer_for(wiki_paths):
    links = "".join(f'<a href="{REPO_BLOB}{w}">{w}</a>' for w in wiki_paths)
    return f'<footer class="slide-src">依據 Wiki：{links}</footer>'


def build(run_dir):
    """把 runs/<run>/slides/NN.html 依編號組進 slides/template.html，輸出 slides/index.html，頁尾由 data-wiki 自動產生。"""
    if not run_dir:
        return ["build 需要 --run DIR"]
    frag_dir = ROOT / run_dir / "slides"
    frags = sorted(frag_dir.glob("[0-9][0-9]*.html"))
    if not frags:
        return [f"{rel(frag_dir)} 裡沒有投影片"]
    tpl = ROOT / "slides" / "template.html"
    if not tpl.exists():
        return ["slides/template.html 不存在"]
    parts = []
    for fp in frags:
        h = fp.read_text(encoding="utf8").strip()
        m = SECTION_RE.search(h)
        if not m:
            return [f"{rel(fp)}：找不到 <section class=\"slide\">"]
        wiki = attr(m.group(1), "data-wiki").split()
        h = re.sub(r'<footer class="slide-src">.*?</footer>', "", h, flags=re.S)
        h = h.replace("</section>", "  " + footer_for(wiki) + "\n</section>", 1)
        parts.append(h)
    out = tpl.read_text(encoding="utf8").replace("<!-- SLIDES -->", "\n\n".join(parts))
    SLIDES.write_text(out, encoding="utf8")
    print(f"已組裝 {len(parts)} 張 → slides/index.html")
    return []


def check_slides(keypoints=None):
    errors = []
    if not SLIDES.exists():
        return ["slides/index.html 不存在"]
    slides = parse_slides(SLIDES.read_text(encoding="utf8"))
    key_ids = load_key_ids(keypoints)
    covered = set()
    titles = {}
    for i, s in enumerate(slides, 1):
        label = f"第 {i} 張「{s['title'][:16]}」"
        errors += slide_errors(label, s, key_ids)
        for w in s["wiki"]:
            if w not in s["footer"]:
                errors.append(f"{label}：底部沒有顯示 {w} 的連結（S1）")
        covered.update(s["points"])
        if s["title"] in titles:
            errors.append(f"{label}：標題和第 {titles[s['title']]} 張重複")
        titles.setdefault(s["title"], i)
    if key_ids:
        for k in key_ids:
            if k not in covered:
                errors.append(f"重點 {k} 沒有出現在任何一張投影片（完整度）")
    errors += structure_errors([s["role"] for s in slides])
    return errors


# ---------- N9：版面檢查 ----------
DESKTOP_JS = """i => {
  const s = document.querySelectorAll('section.slide')[i];
  const body = s.querySelector('.slide-body') || s;
  const foot = s.querySelector('.slide-src');
  const deck = document.querySelector('.deck') || document.body;
  const stage = deck.getBoundingClientRect();
  // 只取文字本身的方框（Range 會連元素的外框一起算，所以逐一走訪文字節點）
  const textRects = el => { const out = []; const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    for (let t = tw.nextNode(); t; t = tw.nextNode()) { if (!t.textContent.trim()) continue;
      const r = document.createRange(); r.selectNodeContents(t);
      for (const x of r.getClientRects()) if (x.width > 0 && x.height > 0) out.push(x); }
    return out; };
  const lines = el => new Set(textRects(el).map(x => Math.round(x.top / 4))).size;
  const hit = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
  // 操作元件：標了 data-ui 的元素，以及 body 底下除了投影片以外、看得到的元素
  const ui = Array.from(document.querySelectorAll('[data-ui], body > *:not(.deck):not(script)'))
    .filter(e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden');
  const slideText = textRects(s);
  const overlap = [];
  ui.forEach(u => { const ur = u.getBoundingClientRect();
    if (slideText.some(t => hit(ur, t))) overlap.push('.' + (u.id || u.className || u.tagName)); });
  // 操作元件的文字對比（文字色 vs. 它底下實際的背景色）
  const rgb = c => (c.match(/[\\d.]+/g) || [0, 0, 0, 0]).map(Number);
  const lum = c => { const v = rgb(c).slice(0, 3).map(x => { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); });
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
  const opaque = c => { const a = rgb(c); return a.length < 4 || a[3] > 0.5; };
  const bgOf = el => { const r = el.getBoundingClientRect();
    for (let n = el; n; n = n.parentElement) { const b = getComputedStyle(n).backgroundColor; if (opaque(b) && rgb(b)[3] !== 0) return b; if (n.matches('[data-ui], body > *')) break; }
    for (const e of document.elementsFromPoint(r.left + r.width / 2, r.top + r.height / 2)) {
      if (el.contains(e) || e.contains(el)) continue;
      for (let n = e; n; n = n.parentElement) { const b = getComputedStyle(n).backgroundColor; if (opaque(b) && rgb(b)[3] !== 0) return b; }
    }
    return 'rgb(255, 255, 255)'; };
  const lowContrast = [];
  ui.forEach(u => u.querySelectorAll('*').length >= 0 && [u].concat(Array.from(u.querySelectorAll('*'))).forEach(e => {
    const own = Array.from(e.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own || !e.getClientRects().length) return;
    const a = lum(getComputedStyle(e).color), b = lum(bgOf(e));
    const ratio = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
    if (ratio < 4.5 && !e.closest('button:disabled')) lowContrast.push((e.id ? '#' + e.id : e.tagName.toLowerCase() + '.' + e.className) + ' ' + ratio.toFixed(1) + ':1');
  }));
  // run-02 看截圖發現：「GPT-4o」在連字號斷行、螢光筆標的詞被拆成兩行
  const split = [];
  const pat = /[A-Za-z]+-[0-9][0-9A-Za-z.]*|\\d[\\d,]*(?:\\.\\d+)?%?/g;
  const tw2 = document.createTreeWalker(body, NodeFilter.SHOW_TEXT);
  for (let t = tw2.nextNode(); t; t = tw2.nextNode()) {
    if (t.parentElement.closest('pre')) continue;
    let m; pat.lastIndex = 0;
    while ((m = pat.exec(t.textContent))) {
      const r = document.createRange(); r.setStart(t, m.index); r.setEnd(t, m.index + m[0].length);
      if (new Set(Array.from(r.getClientRects()).filter(x => x.width > 0).map(x => Math.round(x.top / 4))).size > 1) split.push(m[0]);
    }
  }
  body.querySelectorAll('mark').forEach(mk => { if (lines(mk) > 1) split.push(mk.textContent.trim()); });
  const footClip = foot ? foot.scrollWidth - foot.clientWidth : 0;
  const outside = slideText.filter(t => t.bottom > stage.bottom + 1 || t.right > stage.right + 1).length;
  const kids = Array.from(body.querySelectorAll('*')).filter(e => e.getClientRects().length);
  const br = body.getBoundingClientRect();
  const bottom = kids.length ? Math.max(...kids.map(e => e.getBoundingClientRect().bottom)) : br.top;
  return {h: body.scrollHeight - body.clientHeight, w: body.scrollWidth - body.clientWidth,
          title: (s.querySelector('h1,h2') || {}).textContent || '',
          footLines: foot ? lines(foot) : 0, footClip, split, overlap, lowContrast, outside,
          fill: (bottom - br.top) / br.height};
}"""

MOBILE_CELLS_JS = """() => {
  const out = [];
  document.querySelectorAll('section.slide').forEach((s, k) => s.querySelectorAll('td, th').forEach(td => {
    const t = td.textContent.trim();
    const r = document.createRange(); r.selectNodeContents(td);
    const n = new Set(Array.from(r.getClientRects()).filter(x => x.width > 0).map(x => Math.round(x.top / 4))).size;
    if (t.length >= 2 && t.length <= 6 && n >= 2) out.push([k + 1, t]);
  }));
  return out;
}"""


def make_sheets(shots):
    """把每張桌面截圖合成 6 張一頁的總覽圖，手機長截圖切段並排，方便驗證者看圖。"""
    try:
        from PIL import Image
    except ImportError:
        return
    for old in shots.glob("*sheet*.png"):
        old.unlink()
    files = sorted(shots.glob("desktop-*.png"))
    W, H = 640, 360
    for k in range(0, len(files), 6):
        sheet = Image.new("RGB", (W * 2, H * 3), "white")
        for j, fp in enumerate(files[k:k + 6]):
            sheet.paste(Image.open(fp).convert("RGB").resize((W, H)), ((j % 2) * W, (j // 2) * H))
        sheet.save(shots / f"sheet-{k // 6 + 1}.png")
    mob = shots / "mobile.png"
    if mob.exists():
        im = Image.open(mob).convert("RGB")
        w, h = im.size
        seg = 2600
        parts = [im.crop((0, y, w, min(h, y + seg))) for y in range(0, h, seg)]
        for k in range(0, len(parts), 4):
            group = parts[k:k + 4]
            sheet = Image.new("RGB", (w * len(group), seg), "white")
            for j, part in enumerate(group):
                sheet.paste(part, (j * w, 0))
            sheet.save(shots / f"mobile-sheet-{k // 4 + 1}.png")


def render(run_dir=None, slides_file=None):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return ["需要 playwright：pip install playwright"], []
    errors, warnings = [], []
    target = (ROOT / slides_file) if slides_file else SLIDES
    url = target.resolve().as_uri()
    shots = None
    if run_dir:
        shots = ROOT / run_dir / "screens"
        shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        for (w, h, label) in [(1280, 720, "桌面 1280×720"), (390, 844, "手機 390×844")]:
            page = browser.new_page(viewport={"width": w, "height": h})
            console = []
            page.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: console.append(str(e)))
            page.goto(url)
            page.wait_for_timeout(500)
            n = page.evaluate("document.querySelectorAll('section.slide').length")
            for i in range(n):
                page.evaluate(f"window.deck && window.deck.go({i})")
                page.wait_for_timeout(120)
                if w > 760:
                    o = page.evaluate(DESKTOP_JS, i)
                else:
                    o = page.evaluate("""i => { const s = document.querySelectorAll('section.slide')[i];
                        const c = s.querySelector('.slide-body') || s;
                        const f = s.querySelector('.slide-src');
                        // run-02 看截圖發現：頁尾被截斷、資料來源那張的字在手機上太大
                        const big = Array.from(c.querySelectorAll('p, li, td, summary')).filter(e =>
                            parseFloat(getComputedStyle(e).fontSize) > 20 && !e.closest('.stat')).length;
                        return {h: c.scrollHeight - c.clientHeight, w: c.scrollWidth - c.clientWidth,
                                footClip: f ? f.scrollWidth - f.clientWidth : 0, big,
                                title: (s.querySelector('h1,h2')||{}).textContent || ''}; }""", i)
                tag = f"{label} 第 {i + 1} 張「{o['title'].strip()[:14]}」"
                if o["h"] > 2 or o["w"] > 2:
                    errors.append(f"{tag}內容超出版面（高 {o['h']}px、寬 {o['w']}px）（S5）")
                if o["footClip"] > 1:
                    errors.append(f"{tag}頁尾被截斷，看不到全部的 Wiki 連結（S1、S5）")
                if w <= 760 and o["big"]:
                    warnings.append(f"{tag}有 {o['big']} 段文字在手機上超過 20px")
                if w > 760:
                    for t in sorted(set(o["split"])):
                        errors.append(f"{tag}「{t}」被拆成兩行（S5）")
                    if o["footLines"] > 1:
                        errors.append(f"{tag}頁尾換成 {o['footLines']} 行（S5）")
                    if o["outside"]:
                        errors.append(f"{tag}有文字跑出投影片範圍（S5）")
                    for u in o["overlap"]:
                        errors.append(f"{tag}操作元件「{u}」蓋到投影片文字（S5）")
                    for c in o["lowContrast"]:
                        errors.append(f"{tag}操作元件文字對比不足：{c}（S5）")
                    if o["fill"] < 0.6:
                        warnings.append(f"{tag}內容只用到版面的 {o['fill']:.0%}")
                    if shots:
                        page.screenshot(path=str(shots / f"desktop-{i + 1:02d}.png"))
            if w <= 760:
                narrow = {}
                for k, t in page.evaluate(MOBILE_CELLS_JS):
                    narrow.setdefault(k, [])
                    if t not in narrow[k]:
                        narrow[k].append(t)
                for k, ts in narrow.items():
                    errors.append(f"{label} 第 {k} 張：表格欄太窄，{'、'.join('「' + t + '」' for t in ts[:4])}被拆成好幾行（S5）")
                if shots:
                    page.evaluate("window.scrollTo(0, 0)")
                    page.screenshot(path=str(shots / "mobile.png"), full_page=True)
            if page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1"):
                errors.append(f"{label}：整頁出現橫向捲動（S5）")
            for c in console:
                errors.append(f"{label}：主控台錯誤 {c[:80]}")
            page.close()
        browser.close()
    if shots:
        make_sheets(shots)
    # 同一個操作元件問題在每張投影片都會出現，只保留不重複的訊息
    seen, uniq = set(), []
    for e in errors:
        key = re.sub(r"第 \d+ 張「[^」]*」", "", e)
        if key in seen and ("操作元件" in e):
            continue
        seen.add(key)
        uniq.append(e)
    return uniq, warnings


def main(argv):
    if not argv:
        print(__doc__)
        return 1
    run = None
    if "--run" in argv:
        k = argv.index("--run")
        run = argv[k + 1]
        argv = argv[:k] + argv[k + 2:]
    cmd = argv[0]
    if cmd == "new-run":
        today = dt.date.today().isoformat()
        n = len(list((ROOT / "runs").glob(f"{today}-run-*"))) + 1
        d = ROOT / "runs" / f"{today}-run-{n:02d}"
        d.mkdir(parents=True)
        print(rel(d))
        return 0
    def opt(name):
        return argv[argv.index(name) + 1] if name in argv else None
    kp = opt("--keypoints")
    if cmd == "lint":
        return record(run, "P0 lint", lint())
    if cmd == "check-keypoints":
        return record(run, "V1 check-keypoints", check_keypoints(argv[1]), {"file": argv[1]})
    if cmd == "check-outline":
        return record(run, "V2 check-outline", check_outline(argv[1], kp), {"file": argv[1]})
    if cmd == "check-slide":
        return record(run, "V2 check-slide", check_slide(argv[1], kp), {"file": argv[1]})
    if cmd == "build":
        return record(run, "C build", build(run))
    if cmd == "check-slides":
        return record(run, "V2 check-deck", check_slides(kp))
    if cmd == "render":
        f = argv[1] if len(argv) > 1 and not argv[1].startswith("--") else None
        errs, warns = render(run, f)
        for wmsg in warns:
            print("  ⚠", wmsg)
        return record(run, "V2 render", errs, {"warnings": warns, "file": f or "slides/index.html"})
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
