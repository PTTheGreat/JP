#!/usr/bin/env python3
"""静的サイトジェネレータ。

data/brands/*.json と data/qa/*.json を読み、docs/ に静的HTMLを生成する。
- ブランド定位ページ: /brands/<slug>/
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

SAMPLE_NOTICE = (
    "このページはサンプルコンテンツです。公開前に日本語ネイティブによる校閲と、"
    "各事実の一次情報源での再確認(【要確認】箇所)が必要です。"
)


def esc(s):
    return html.escape(str(s), quote=True)


def crumb(items):
    """パンくずリスト。items: [(label, href|None), ...]"""
    parts = ['<a href="/">ホーム</a>']
    for label, href in items:
        parts.append('<span class="sep">›</span>')
        if href:
            parts.append(f'<a href="{esc(href)}">{esc(label)}</a>')
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
<a class="logo" href="/">{esc(CONFIG['site_name'])}</a>
<span class="tag">すべての記載に出典と確認日を明記 | ブランドの事実だけを集めるサイト</span>
</div></header>
<main>
{body}
</main>
<footer><div class="inner">
<p><a href="/about/">サイトについて・運営方針</a></p>
<p>掲載情報には出典と確認日を明記しています。誤りを見つけた場合は出典とあわせてご指摘ください。
機種ごとの性能比較は行いません(実測レビューは専門メディアをご参照ください)。</p>
</div></footer>
</body>
</html>
"""


def facts_table(facts):
    rows = []
    for f in facts:
        src = (f'<a href="{esc(f["source_url"])}" rel="noopener">{esc(f["source"])}</a>'
               f'<br>確認日: {esc(f["checked"])}')
        rows.append(
            f"<tr><th scope=\"row\">{esc(f['label'])}</th>"
            f"<td>{esc(f['value'])}</td>"
            f'<td class="src">{src}</td></tr>'
        )
    return ('<div class="table-wrap"><table>'
            "<thead><tr><th>項目</th><th>内容</th><th>出典 / 確認日</th></tr></thead>"
            "<tbody>" + "".join(rows) + "</tbody></table></div>")


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
    qas = load_dir("qa")
    qa_by_slug = {q["slug"]: q for q in qas}
    urls = [f"{BASE}/", f"{BASE}/about/"]

    # ブランド定位ページ
    for b in brands:
        url = f"{BASE}/brands/{b['slug']}/"
        urls.append(url)
        updated = max(f["checked"] for f in b["facts"])
        rel_items = [qa_by_slug[s] for s in b.get("related_qa", []) if s in qa_by_slug]

        toc_items = ['<li><a href="#facts">事実一覧</a></li>']
        if rel_items:
            toc_items.append('<li><a href="#faq">よくある質問</a></li>')
        toc = ('<div class="toc"><span class="toc-title">目次</span>'
               f'<ol>{"".join(toc_items)}</ol></div>')

        faq = ""
        if rel_items:
            det = "".join(
                f'<details class="faq"><summary>{esc(q["question"])}</summary>'
                f'<div class="faq-a">{esc(q["answer"])} '
                f'<a href="/qa/{esc(q["slug"])}/">→ 根拠となる事実を見る</a>'
                f"</div></details>"
                for q in rel_items)
            faq = f'<h2 id="faq">よくある質問</h2>{det}'

        notice = f'<p class="notice">{esc(SAMPLE_NOTICE)}</p>' if b.get("sample_notice") else ""
        crumbs = [("ブランド一覧", "/#brands"), (b["name"], None)]
        body = (
            crumb(crumbs)
            + f"<h1>{esc(b['name'])}とはどんなブランドか</h1>"
            + f'<div class="meta">{country_badge(b["country"])}'
            + f'<span class="updated-note">最終確認日: {esc(updated)}</span></div>'
            + f'<p class="summary">{esc(b["summary"])}</p>'
            + toc
            + f'<h2 id="facts">事実一覧</h2>{facts_table(b["facts"])}'
            + faq + notice
            + f'<p style="margin-top:2rem"><a class="back" href="/">← ブランド一覧へ戻る</a></p>'
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
        d = OUT / "brands" / b["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(
            page(f"{b['name']}はどこの国?どんなブランド? | {CONFIG['site_name']}",
                 body, url, b["summary"], lds), encoding="utf-8")

    # 問答ページ
    for q in qas:
        url = f"{BASE}/qa/{q['slug']}/"
        urls.append(url)
        updated = max(f["checked"] for f in q["facts"])
        b = next((x for x in brands if x["slug"] == q.get("brand")), None)
        brand_link = ""
        if b:
            brand_link = (
                '<h2>ブランドの基本情報</h2><ul class="blist"><li>'
                f'<a href="/brands/{esc(b["slug"])}/">{esc(b["name"])}のブランド事実ページ'
                f'<span class="desc">母会社・日本法人・保証・リコール履歴など</span></a>'
                "</li></ul>")
        notice = f'<p class="notice">{esc(SAMPLE_NOTICE)}</p>' if q.get("sample_notice") else ""
        crumbs = [("質問一覧", "/#qa"), (q["question"], None)]
        body = (
            crumb(crumbs)
            + f"<h1>{esc(q['question'])}</h1>"
            + f'<div class="meta"><span class="updated-note">最終確認日: {esc(updated)}</span></div>'
            + f'<p class="answer">{esc(q["answer"])}</p>'
            + f"<h2>根拠となる事実</h2>{facts_table(q['facts'])}"
            + brand_link + notice
            + '<p style="margin-top:2rem"><a class="back" href="/">← 質問一覧へ戻る</a></p>'
        )
        lds = [
            {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "ja",
             "mainEntity": [{"@type": "Question", "name": q["question"],
                             "acceptedAnswer": {"@type": "Answer", "text": q["answer"]}}],
             "url": url},
            crumb_ld(crumbs, url),
        ]
        d = OUT / "qa" / q["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(
            page(f"{q['question']} | {CONFIG['site_name']}",
                 body, url, q["answer"][:120], lds), encoding="utf-8")

    # トップページ
    brand_links = "".join(
        f'<li><a href="/brands/{esc(b["slug"])}/">{country_badge(b["country"])} '
        f'{esc(b["name"])}<span class="desc">{esc(b["summary"][:44])}…</span></a></li>'
        for b in brands)
    qa_links = "".join(
        f'<li><a href="/qa/{esc(q["slug"])}/">{esc(q["question"])}</a></li>' for q in qas)
    body = (
        f"<h1>{esc(CONFIG['site_name'])}</h1>"
        f'<p class="summary">{esc(CONFIG["description"])}</p>'
        f'<h2 id="qa">質問から探す</h2><ul class="qlist">{qa_links}</ul>'
        f'<h2 id="brands">ブランドから探す</h2><ul class="blist">{brand_links}</ul>'
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
    llms += [f"- [{b['name']}]({BASE}/brands/{b['slug']}/): {b['summary'][:60]}" for b in brands]
    llms += ["", "## 問答ページ", ""]
    llms += [f"- [{q['question']}]({BASE}/qa/{q['slug']}/)" for q in qas]
    (OUT / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")

    # sitemap / robots
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"<url><loc>{esc(u)}</loc></url>" for u in urls]
    sm.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (OUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")

    print(f"generated: {len(brands)} brand pages, {len(qas)} qa pages -> {OUT}/")


if __name__ == "__main__":
    build()
