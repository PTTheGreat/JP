#!/usr/bin/env python3
"""静的サイトジェネレータ。

data/brands/*.json と data/qa/*.json を読み、docs/ に静的HTMLを生成する。
- ブランド定位ページ: /<slug>/(1ブランド=1スラッグ)
- 問答ページ: /qa/<slug>/
- llms.txt / sitemap.xml / robots.txt / index.html / about

デザインは日本のWeb慣習に準拠:
パンくずリスト、更新日の明示、目次、「結論」先行の回答、
よくある質問のアコーディオン、高めの情報密度、運営者情報。

依存ライブラリなし。実行: python3 build.py
"""

import json
import html
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
OUT = ROOT / CONFIG["output_dir"]
BASE = CONFIG["base_url"].rstrip("/")
# GitHub Pagesのプロジェクトサイト等、サブパス配下で配信する場合の接頭辞。
# base_url のパス部分から自動導出する(例: https://x.github.io/jp → "/jp")。
from urllib.parse import urlparse
PREFIX = urlparse(BASE).path.rstrip("/")


def u(path):
    """サイト内リンクに base path を付与する。"""
    return f"{PREFIX}{path}"

CSS = """
:root { --fg:#222; --muted:#707070; --line:#dcdcdc; --accent:#b71c1c;
        --accent2:#1a237e; --bg:#fff; --bg2:#f7f7f5; --q:#b71c1c; }
* { margin:0; padding:0; box-sizing:border-box; }
html { font-size:15px; }
body { font-family:"Hiragino Kaku Gothic ProN","Hiragino Sans","Noto Sans JP",
       "Yu Gothic Medium","Meiryo",sans-serif; color:var(--fg);
       background:var(--bg); line-height:1.85; }
main { max-width:760px; margin:0 auto; padding:0 1rem 3rem; }
header.site { background:var(--bg); border-bottom:3px solid var(--accent); }
header.site .inner { max-width:760px; margin:0 auto; padding:0.7rem 1rem; }
header.site a.logo { color:var(--fg); text-decoration:none; font-weight:800;
                     font-size:1.15rem; letter-spacing:0.02em; }
header.site .tag { color:var(--muted); font-size:0.72rem; display:block; }
nav.crumb { font-size:0.75rem; color:var(--muted); padding:0.6rem 0 0; }
nav.crumb a { color:var(--accent2); text-decoration:none; }
nav.crumb span.sep { margin:0 0.35rem; }
h1 { font-size:1.45rem; line-height:1.5; margin:0.7rem 0 0.3rem; font-weight:800; }
.meta { font-size:0.75rem; color:var(--muted); margin-bottom:1rem;
        display:flex; gap:0.8rem; flex-wrap:wrap; align-items:center; }
.badge { display:inline-block; font-size:0.72rem; font-weight:700; color:#fff;
         background:var(--accent2); border-radius:3px; padding:0.05rem 0.5rem; }
.badge.jp { background:var(--accent); }
h2 { font-size:1.08rem; margin:2rem 0 0.7rem; padding:0.35rem 0.6rem;
     background:var(--bg2); border-left:5px solid var(--accent); font-weight:700; }
p.answer { background:#fdf6f6; border:1px solid #ecd5d5; border-radius:6px;
           padding:0.9rem 1rem 0.9rem 1rem; margin:0.3rem 0 1rem; }
p.answer::before { content:"結論"; display:inline-block; background:var(--accent);
           color:#fff; font-size:0.72rem; font-weight:700; border-radius:3px;
           padding:0.02rem 0.5rem; margin-right:0.5rem; vertical-align:0.1em; }
p.summary { margin-bottom:0.8rem; }
.toc { border:1px solid var(--line); border-radius:6px; background:var(--bg2);
       padding:0.7rem 1rem; margin:1rem 0; font-size:0.85rem; }
.toc .toc-title { font-weight:700; font-size:0.8rem; color:var(--muted); }
.toc ol { margin:0.2rem 0 0 1.3rem; }
.toc a { color:var(--accent2); text-decoration:none; }
.table-wrap { overflow-x:auto; }
table { width:100%; border-collapse:collapse; font-size:0.86rem; line-height:1.6; }
th, td { text-align:left; padding:0.5rem 0.6rem; border:1px solid var(--line);
         vertical-align:top; }
thead th { background:var(--bg2); color:var(--fg); font-size:0.8rem; }
tbody th { background:var(--bg2); white-space:nowrap; font-weight:600;
           width:9.5em; }
td.src { font-size:0.75rem; color:var(--muted); }
td.src a { color:var(--accent2); }
ul.qlist { list-style:none; }
ul.qlist li { border-bottom:1px dotted var(--line); }
ul.qlist a { display:flex; gap:0.55rem; padding:0.6rem 0.2rem; color:var(--fg);
             text-decoration:none; align-items:baseline; }
ul.qlist a::before { content:"Q"; color:#fff; background:var(--q); font-weight:800;
             font-size:0.78rem; border-radius:3px; padding:0 0.42rem; flex:none; }
ul.qlist a:hover { color:var(--accent); }
ul.blist { list-style:none; }
ul.blist li { border-bottom:1px dotted var(--line); }
ul.blist a { display:flex; gap:0.6rem; padding:0.6rem 0.2rem; color:var(--fg);
             text-decoration:none; align-items:baseline; flex-wrap:wrap; }
ul.blist a:hover { color:var(--accent); }
ul.blist .desc { color:var(--muted); font-size:0.8rem; }
details.faq { border:1px solid var(--line); border-radius:6px; margin:0.5rem 0;
              background:var(--bg); }
details.faq summary { cursor:pointer; padding:0.6rem 0.8rem; font-weight:700;
              font-size:0.92rem; list-style:none; display:flex; gap:0.55rem;
              align-items:baseline; }
details.faq summary::before { content:"Q"; color:#fff; background:var(--q);
              font-weight:800; font-size:0.78rem; border-radius:3px;
              padding:0 0.42rem; flex:none; }
details.faq[open] summary { border-bottom:1px dotted var(--line); }
details.faq .faq-a { padding:0.7rem 0.9rem; font-size:0.9rem; }
details.faq .faq-a a { color:var(--accent2); }
.timeline { list-style:none; border-left:2px solid var(--line); margin:0.6rem 0 0 0.4rem;
            padding-left:0; }
.timeline li { position:relative; padding:0 0 1rem 1.1rem; }
.timeline li::before { content:""; position:absolute; left:-6px; top:0.55rem; width:10px;
            height:10px; border-radius:50%; background:var(--accent); }
.tl-date { font-size:0.75rem; color:var(--muted); font-weight:700; letter-spacing:0.02em; }
.tl-title { font-weight:700; font-size:0.95rem; display:block; margin:0.1rem 0 0.25rem; }
.tl-body { font-size:0.86rem; }
.tl-impact { font-size:0.82rem; background:var(--bg2); border-left:3px solid var(--accent2);
             padding:0.35rem 0.6rem; margin:0.4rem 0 0.3rem; }
.tl-src { font-size:0.75rem; color:var(--muted); }
.tl-src a { color:var(--accent2); }
.tl-brand { font-size:0.75rem; color:var(--accent2); text-decoration:none; font-weight:700; }
.badge-new { display:inline-block; background:var(--accent); color:#fff; font-size:0.65rem;
             font-weight:700; border-radius:3px; padding:0 0.35rem; margin-left:0.35rem;
             vertical-align:0.12em; }
.tldr { border:1px solid #d7c9a7; background:#fdfbf3; border-radius:6px;
        padding:0.75rem 1rem 0.85rem; margin:1rem 0; }
.tldr-t { display:inline-block; background:#8a6d1f; color:#fff; font-size:0.72rem;
          font-weight:700; border-radius:3px; padding:0.05rem 0.55rem; }
.tldr ul { list-style:none; margin:0.5rem 0 0; font-size:0.88rem; }
.tldr li { padding:0.18rem 0; border-bottom:1px dotted #e3d9c0; }
.tldr li:last-child { border-bottom:none; }
.tldr b { display:inline-block; min-width:9em; color:var(--muted); font-weight:600;
          font-size:0.8rem; }
ul.srclist { list-style:none; font-size:0.82rem; columns:2; column-gap:1.5rem; }
ul.srclist li { padding:0.15rem 0; break-inside:avoid; }
ul.srclist a { color:var(--accent2); }
@media (max-width:560px) { ul.srclist { columns:1; } .tldr b { min-width:auto; display:block; } }
.bgrid { display:grid; grid-template-columns:repeat(auto-fill,minmax(215px,1fr));
         gap:0.7rem; }
a.bcard { display:block; border:1px solid var(--line); border-top:3px solid var(--accent2);
          border-radius:6px; padding:0.65rem 0.8rem 0.75rem; text-decoration:none;
          color:var(--fg); background:var(--bg); }
a.bcard.jp { border-top-color:var(--accent); }
a.bcard:hover { background:var(--bg2); }
.bcard .bname { font-weight:800; font-size:1.02rem; display:block; margin:0.3rem 0 0; }
.bcard .ben { color:var(--muted); font-size:0.7rem; letter-spacing:0.05em; }
.bcard .bdesc { font-size:0.76rem; color:var(--muted); line-height:1.65;
                display:block; margin-top:0.35rem; }
.bcard .qcount { display:inline-block; margin-top:0.45rem; font-size:0.7rem;
                 color:var(--accent2); border:1px solid var(--line); border-radius:3px;
                 padding:0 0.4rem; }
.qgroup { margin:1.3rem 0 0.1rem; font-size:0.88rem; font-weight:700; }
.unverified { color:#d32f2f; }
.legend { font-size:0.75rem; color:var(--muted); margin:0.4rem 0 0; }
.legend .unverified { font-weight:700; }
.qsource { font-size:0.8rem; background:var(--bg2); border:1px solid var(--line);
           border-radius:6px; padding:0.5rem 0.8rem; margin:0 0 1rem; color:var(--muted); }
.qsource a { color:var(--accent2); }
.notice { font-size:0.75rem; color:var(--muted); border:1px dashed var(--line);
          border-radius:6px; padding:0.55rem 0.8rem; margin:1.5rem 0 0;
          background:var(--bg2); }
footer { border-top:1px solid var(--line); margin-top:2rem; background:var(--bg2); }
footer .inner { max-width:760px; margin:0 auto; padding:1.2rem 1rem 2.5rem;
                color:var(--muted); font-size:0.75rem; }
footer a { color:var(--accent2); }
a.back { color:var(--accent2); font-size:0.85rem; text-decoration:none; }
.updated-note { font-size:0.75rem; color:var(--muted); }
"""

CHECKED_DEFAULT = "2026-08-27"

SAMPLE_NOTICE = (
    "このページはサンプルコンテンツです。公開前に日本語ネイティブによる校閲と、"
    "各事実の一次情報源での再確認(【要確認】箇所)が必要です。"
)


def esc(s):
    return html.escape(str(s), quote=True)


def crumb(items):
    """パンくずリスト。items: [(label, href|None), ...]"""
    parts = [f'<a href="{u("/")}">ホーム</a>']
    for label, href in items:
        parts.append('<span class="sep">›</span>')
        if href:
            parts.append(f'<a href="{esc(u(href))}">{esc(label)}</a>')
        else:
            parts.append(esc(label))
    return f'<nav class="crumb" aria-label="パンくずリスト">{"".join(parts)}</nav>'


def crumb_ld(items, page_url):
    elems = [{"@type": "ListItem", "position": 1, "name": "ホーム", "item": f"{BASE}/"}]
    for i, (label, href) in enumerate(items, start=2):
        e = {"@type": "ListItem", "position": i, "name": label}
        e["item"] = f"{BASE}{href}" if href else page_url
        elems.append(e)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": elems}


def page(title, body, canonical, description="", jsonld=None):
    lds = jsonld or []
    ld = "".join('<script type="application/ld+json">'
                 + json.dumps(x, ensure_ascii=False) + "</script>" for x in lds)
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<style>{CSS}</style>
{ld}
</head>
<body>
<header class="site"><div class="inner">
<a class="logo" href="{u('/')}">{esc(CONFIG['site_name'])}</a>
<span class="tag">すべての記載に出典と確認日を明記 | ブランドの事実だけを集めるサイト</span>
</div></header>
<main>
{body}
</main>
<footer><div class="inner">
<p><a href="{u('/about/')}">サイトについて・運営方針</a></p>
<p>掲載情報には出典と確認日を明記しています。誤りを見つけた場合は出典とあわせてご指摘ください。
機種ごとの性能比較は行いません(実測レビューは専門メディアをご参照ください)。</p>
</div></footer>
</body>
</html>
"""


def is_unverified(value):
    return "【要確認】" in value or "未確認" in value


def facts_table(facts, legend=True):
    rows = []
    has_unverified = False
    for f in facts:
        src = (f'<a href="{esc(f["source_url"])}" rel="noopener">{esc(f["source"])}</a>'
               f'<br>確認日: {esc(f["checked"])}')
        val = esc(f["value"])
        if is_unverified(f["value"]):
            has_unverified = True
            val = f'<span class="unverified">{val}</span>'
        rows.append(
            f"<tr><th scope=\"row\">{esc(f['label'])}</th>"
            f"<td>{val}</td>"
            f'<td class="src">{src}</td></tr>'
        )
    lg = ""
    if has_unverified and legend:
        lg = ('<p class="legend"><span class="unverified">赤字</span>'
              "は一次情報源での確認が済んでいない項目です。</p>")
    return ('<div class="table-wrap"><table>'
            "<thead><tr><th>項目</th><th>内容</th><th>出典 / 確認日</th></tr></thead>"
            "<tbody>" + "".join(rows) + "</tbody></table></div>" + lg)


def all_facts(b):
    return [f for s in b.get("sections", []) for f in s["facts"]]


def coverage(b):
    """確認済み / 未確認の件数を返す。"""
    fs = all_facts(b)
    unv = sum(1 for f in fs if is_unverified(f["value"]))
    return len(fs), len(fs) - unv, unv


def summary_box(b):
    """「30秒でわかる」要点ボックス。主要フィールドから自動生成する。"""
    lookup = {f["label"]: f["value"] for f in all_facts(b)}
    picks = [
        ("どこの国の会社か", lookup.get("本社所在地", "")),
        ("日本法人", lookup.get("日本法人", "")),
        ("保証期間", lookup.get("保証期間", "")),
        ("価格帯", lookup.get("主な価格帯", "")),
    ]
    lis = []
    for label, val in picks:
        if not val:
            continue
        v = esc(val.split("。")[0])
        if is_unverified(val):
            v = f'<span class="unverified">{v}</span>'
        lis.append(f"<li><b>{esc(label)}</b>{v}</li>")
    total, ok, unv = coverage(b)
    lis.append(f'<li><b>データ整備状況</b>全{total}項目中 {ok}項目が出典つきで確認済み'
               f'(<span class="unverified">未確認 {unv}項目</span>)</li>')
    return ('<div class="tldr"><span class="tldr-t">30秒でわかる</span>'
            f'<ul>{"".join(lis)}</ul></div>')


def timeline(updates, brand_link=None):
    """最新の動向をタイムライン表示する。updatesは日付降順で渡す。"""
    lis = []
    for uitem in updates:
        impact = ""
        if uitem.get("impact"):
            impact = f'<p class="tl-impact"><b>影響:</b> {esc(uitem["impact"])}</p>'
        src = ""
        if uitem.get("source_url"):
            src = (f'<p class="tl-src">出典: <a href="{esc(uitem["source_url"])}" '
                   f'rel="noopener">{esc(uitem.get("source", "出典"))}</a></p>')
        bl = ""
        if brand_link:
            links = " ".join(
                f'<a class="tl-brand" href="{esc(u("/" + s + "/#updates"))}">{esc(n)} →</a>'
                for s, n in uitem["_brands"])
            bl = f'<p class="tl-src">関連ブランド: {links}</p>'
        lis.append(
            f'<li><span class="tl-date">{esc(uitem["date"])}</span>'
            f'<span class="tl-title">{esc(uitem["title"])}</span>'
            f'<span class="tl-body">{esc(uitem["body"])}</span>'
            f"{impact}{src}{bl}</li>")
    return f'<ul class="timeline">{"".join(lis)}</ul>'


def sources_list(b):
    """ページ内で使用した一次情報源の一覧。"""
    seen = {}
    for f in all_facts(b):
        seen.setdefault(f["source"], f["source_url"])
    items = "".join(
        f'<li><a href="{esc(v)}" rel="noopener">{esc(k)}</a></li>'
        for k, v in sorted(seen.items()))
    return f'<ul class="srclist">{items}</ul>'


def qsource_box(q):
    """質問の出所を示すボックス。実投稿ベースと時事ベースで表示を変える。"""
    source = q.get("source")
    if source:
        orig = f"「{esc(source['original'])}」" if source.get("original") else ""
        return ('<p class="qsource">この質問は実際のユーザー投稿に基づいています: '
                f'{esc(source["platform"])} {orig} '
                f'<a href="{esc(source["url"])}" rel="noopener nofollow">元の投稿を見る</a></p>')
    if q.get("topical"):
        return ('<p class="qsource">この質問は、2025年末以降に起きた制度変更・事業動向を'
                "受けて検索が増えている話題を扱っています。根拠となる報道・公的資料は"
                "下部の情報源一覧に記載しています。</p>")
    return ""


def refs_list(sources):
    """参照した情報源(日付つき)の一覧。"""
    items = []
    for s in sources:
        pub = s.get("published") or "日付不明"
        if pub in ("不明", "", None):
            pub = "日付不明"
        cls = ' class="unverified"' if pub == "日付不明" else ""
        items.append(
            f'<li><a href="{esc(s["url"])}" rel="noopener">{esc(s["name"])}</a>'
            f'<span{cls} style="color:var(--muted);font-size:0.78rem"> — {esc(pub)}</span></li>')
    return f'<ul class="srclist">{"".join(items)}</ul>'


def load_dir(subdir):
    return [json.loads(p.read_text(encoding="utf-8"))
            for p in sorted((ROOT / "data" / subdir).glob("*.json"))]


def country_badge(country):
    cls = "badge jp" if country.startswith("日本") else "badge"
    return f'<span class="{cls}">{esc(country)}</span>'


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / ".nojekyll").write_text("")

    brands = load_dir("brands")
    urls = [f"{BASE}/", f"{BASE}/about/"]

    # ブランド定位ページ(1ブランド=1スラッグ。FAQはその配下に生成)
    for b in brands:
        url = f"{BASE}/{b['slug']}/"
        urls.append(url)
        updated = max(f["checked"] for f in all_facts(b))
        rel_items = b.get("faq", [])
        secs = b.get("sections", [])

        ups = sorted(b.get("updates", []), key=lambda x: x["date"], reverse=True)
        toc_items = []
        if ups:
            toc_items.append('<li><a href="#updates">最新の動向</a></li>')
        toc_items += [f'<li><a href="#s{i}">{esc(s["title"])}</a></li>'
                      for i, s in enumerate(secs)]
        if rel_items:
            toc_items.append(f'<li><a href="#faq">よくある質問({len(rel_items)}件)</a></li>')
        toc_items.append('<li><a href="#sources">このページの出典一覧</a></li>')
        toc = ('<div class="toc"><span class="toc-title">目次</span>'
               f'<ol>{"".join(toc_items)}</ol></div>')

        sec_html = "".join(
            f'<h2 id="s{i}">{esc(s["title"])}</h2>'
            + facts_table(s["facts"], legend=(i == 0))
            for i, s in enumerate(secs))

        faq = ""
        if rel_items:
            det = "".join(
                f'<details class="faq"><summary>{esc(q["question"])}</summary>'
                f'<div class="faq-a">{esc(q["answer"])} '
                f'<a href="{u("/" + b["slug"] + "/" + q["slug"] + "/")}">→ 根拠となる事実を見る</a>'
                f"</div></details>"
                for q in rel_items)
            faq = ('<h2 id="faq">よくある質問</h2>'
                   '<p class="legend">質問はYahoo!知恵袋・Quora等に実際に投稿された'
                   "ユーザーの質問に基づいています(各ページに出典リンクあり)。</p>" + det)

        notice = f'<p class="notice">{esc(SAMPLE_NOTICE)}</p>' if b.get("sample_notice") else ""
        crumbs = [(b["name"], None)]
        total, ok, unv = coverage(b)
        body = (
            crumb(crumbs)
            + f"<h1>{esc(b['name'])}とはどんなブランドか</h1>"
            + f'<div class="meta">{country_badge(b["country"])}'
            + f'<span class="updated-note">最終確認日: {esc(updated)}</span>'
            + f'<span class="updated-note">掲載項目: {total}件</span></div>'
            + f'<p class="summary">{esc(b["summary"])}</p>'
            + summary_box(b)
            + toc
            + (('<h2 id="updates">最新の動向</h2>'
                '<p class="legend">このブランドに関する制度変更・事業動向の記録です。'
                "新しい順に並んでいます。</p>" + timeline(ups)) if ups else "")
            + sec_html
            + faq
            + '<h2 id="sources">このページの出典一覧</h2>'
            + '<p class="legend">記載した事実はすべて以下の情報源に基づいています。'
            "確認日時点の情報です。</p>"
            + sources_list(b)
            + notice
            + f'<p style="margin-top:2rem"><a class="back" href="{u("/")}">← ブランド一覧へ戻る</a></p>'
        )
        lds = [
            {"@context": "https://schema.org", "@type": "Article",
             "headline": f"{b['name']}とはどんなブランドか", "inLanguage": "ja",
             "dateModified": updated,
             "about": {"@type": "Brand", "name": b["name_en"]}, "url": url},
            crumb_ld(crumbs, url),
        ]
        if rel_items:
            lds.append({"@context": "https://schema.org", "@type": "FAQPage",
                        "mainEntity": [{"@type": "Question", "name": q["question"],
                                        "acceptedAnswer": {"@type": "Answer",
                                                           "text": q["answer"]}}
                                       for q in rel_items]})
        d = OUT / b["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(
            page(f"{b['name']}はどこの国?どんなブランド? | {CONFIG['site_name']}",
                 body, url, b["summary"], lds), encoding="utf-8")

    # FAQサブページ(ブランドスラッグの配下: /<brand>/<faq>/)
    for b in brands:
        for q in b.get("faq", []):
            path = f"/{b['slug']}/{q['slug']}/"
            url = f"{BASE}{path}"
            urls.append(url)
            updated = (max(f["checked"] for f in q["facts"])
                       if q.get("facts") else CHECKED_DEFAULT)
            total, _, _ = coverage(b)
            brand_link = (
                '<h2>ブランドの基本情報</h2><ul class="blist"><li>'
                f'<a href="{u("/" + b["slug"] + "/")}">{esc(b["name"])}のブランド事実ページ'
                f'<span class="desc">企業プロフィール・日本法人・規制・保証など全{total}項目</span></a>'
                "</li></ul>")
            others = [x for x in b.get("faq", []) if x["slug"] != q["slug"]]
            if others:
                items = "".join(
                    f'<li><a href="{u("/" + b["slug"] + "/" + o["slug"] + "/")}">'
                    f'{esc(o["question"])}</a></li>' for o in others)
                brand_link += (f'<h2>{esc(b["name"])}についての他の質問</h2>'
                               f'<ul class="qlist">{items}</ul>')
            notice = f'<p class="notice">{esc(SAMPLE_NOTICE)}</p>' if b.get("sample_notice") else ""
            crumbs = [(b["name"], f"/{b['slug']}/"),
                      (q["question"], None)]
            newbadge = '<span class="badge-new">最新の話題</span>' if q.get("topical") else ""
            facts_html = (f"<h2>根拠となる事実</h2>{facts_table(q['facts'])}"
                          if q.get("facts") else "")
            refs_html = (f"<h2>参照した情報源</h2>{refs_list(q['sources'])}"
                         if q.get("sources") else "")
            body = (
                crumb(crumbs)
                + f"<h1>{esc(q['question'])}{newbadge}</h1>"
                + f'<div class="meta"><span class="updated-note">最終確認日: {esc(updated)}</span></div>'
                + qsource_box(q)
                + f'<p class="answer">{esc(q["answer"])}</p>'
                + facts_html + refs_html
                + brand_link + notice
                + f'<p style="margin-top:2rem"><a class="back" href="{u("/" + b["slug"] + "/")}">'
                + f"← {esc(b['name'])}のページへ戻る</a></p>"
            )
            qnode = {"@type": "Question", "name": q["question"],
                     "acceptedAnswer": {"@type": "Answer", "text": q["answer"]}}
            if q.get("source"):
                qnode["sameAs"] = q["source"]["url"]
            lds = [
                {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "ja",
                 "mainEntity": [qnode], "url": url},
                crumb_ld(crumbs, url),
            ]
            d = OUT / b["slug"] / q["slug"]
            d.mkdir(parents=True)
            (d / "index.html").write_text(
                page(f"{q['question']} | {CONFIG['site_name']}",
                     body, url, q["answer"][:120], lds), encoding="utf-8")

    # トップページ
    cards = []
    for b in brands:
        n = len(b.get("faq", []))
        total, _, _ = coverage(b)
        cls = "bcard jp" if b["country"].startswith("日本") else "bcard"
        cards.append(
            f'<a class="{cls}" href="{u("/" + b["slug"] + "/")}">'
            f'{country_badge(b["country"])}'
            f'<span class="bname">{esc(b["name"])}</span>'
            f'<span class="ben">{esc(b["name_en"].upper())}</span>'
            f'<span class="bdesc">{esc(b["summary"][:40])}…</span>'
            f'<span class="qcount">事実{total}項目 / Q&amp;A {n}件</span></a>')
    qa_groups = []
    for b in brands:
        faqs = b.get("faq", [])
        if not faqs:
            continue
        items = "".join(
            f'<li><a href="{u("/" + b["slug"] + "/" + q["slug"] + "/")}">{esc(q["question"])}</a></li>'
            for q in faqs)
        qa_groups.append(
            f'<p class="qgroup">{country_badge(b["country"])} {esc(b["name"])}</p>'
            f'<ul class="qlist">{items}</ul>')
    # 全ブランド横断の最新動向(新着情報)。同じ話題は1件にまとめる。
    merged = {}
    for b in brands:
        for uitem in b.get("updates", []):
            key = (uitem["date"], uitem["title"])
            if key not in merged:
                merged[key] = dict(uitem, _brands=[])
            merged[key]["_brands"].append((b["slug"], b["name"]))
    all_ups = sorted(merged.values(), key=lambda x: x["date"], reverse=True)
    news = ""
    if all_ups:
        news = ('<h2 id="news">新着情報 — ブランドをめぐる最新の動き</h2>'
                '<p class="legend">制度変更や事業動向のうち、ブランド選びの判断に関わるものを'
                "新しい順に掲載しています。</p>"
                + timeline(all_ups[:8], brand_link=True))

    body = (
        f"<h1>{esc(CONFIG['site_name'])}</h1>"
        f'<p class="summary">{esc(CONFIG["description"])}</p>'
        + news
        + f'<h2 id="brands">ブランドから探す</h2><div class="bgrid">{"".join(cards)}</div>'
        f'<h2 id="qa">質問から探す</h2>'
        '<p class="legend">質問はYahoo!知恵袋・Quora等に実際に投稿された質問に基づいています。</p>'
        + "".join(qa_groups)
    )
    (OUT / "index.html").write_text(
        page(f"{CONFIG['site_name']} | ブランドの事実データベース", body,
             f"{BASE}/", CONFIG["description"]), encoding="utf-8")

    # サイトについて
    about_body = (
        crumb([("サイトについて", None)])
        + "<h1>サイトについて・運営方針</h1>"
        + "<h2>このサイトは何か</h2>"
        + f'<p class="summary">{esc(CONFIG["description"])} '
        "機種ごとの性能比較や主観的なおすすめは行いません。"
        "「このブランドはどこの国の会社か」「日本法人はあるか」「保証・リコールはどうなっているか」"
        "というブランドレベルの事実に回答を絞ります。</p>"
        + "<h2>情報の確認方法</h2>"
        + "<p>各事実は、国税庁法人番号公表サイト、総務省の技術基準適合証明データベース、"
        "消費者庁リコール情報サイト、および各社公式サイトなどの一次情報源に基づき、"
        "確認日とあわせて掲載しています。情報は確認日時点のものです。</p>"
        + "<h2>訂正について</h2>"
        + "<p>誤りを見つけた場合は、正しい情報の出典とあわせてご連絡ください。確認のうえ速やかに訂正します。</p>"
    )
    d = OUT / "about"
    d.mkdir(parents=True)
    (d / "index.html").write_text(
        page(f"サイトについて | {CONFIG['site_name']}", about_body,
             f"{BASE}/about/", "運営方針と情報の確認方法について"), encoding="utf-8")

    # llms.txt
    llms = [f"# {CONFIG['site_name']} ({CONFIG['site_name_en']})", "",
            f"> {CONFIG['description']}", "",
            "各ページは「1つの質問に1つの直接的な答え」または「1ブランド1ページの事実一覧」で構成され、",
            "すべての事実に出典URLと確認日が付記されています。AIによる引用を歓迎します。", "",
            "## ブランド定位ページ", ""]
    llms += [f"- [{b['name']}]({BASE}/{b['slug']}/): {b['summary'][:60]}"
             f"(事実{coverage(b)[0]}項目・出典つき)" for b in brands]
    llms += ["", "## 問答ページ(実在のユーザー投稿に基づく質問)", ""]
    llms += [f"- [{q['question']}]({BASE}/{b['slug']}/{q['slug']}/)"
             for b in brands for q in b.get("faq", [])]
    (OUT / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")

    # sitemap / robots
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{esc(u)}</loc></url>" for u in urls]
    sm.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")

    n_faq = sum(len(b.get("faq", [])) for b in brands)
    print(f"generated: {len(brands)} brand pages, {n_faq} faq pages -> {OUT}/")


if __name__ == "__main__":
    build()
