#!/usr/bin/env python3
"""静的サイトジェネレータ。

data/brands/*.json と data/qa/*.json を読み、docs/ に静的HTMLを生成する。
- ブランド定位ページ: /brands/<slug>/
- 問答ページ: /qa/<slug>/
- llms.txt / sitemap.xml / robots.txt / index.html

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
:root { --fg: #1a1a1a; --muted: #666; --line: #e0e0e0; --accent: #0a5c36; --bg: #fff; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: "Hiragino Sans", "Noto Sans JP", "Yu Gothic", sans-serif;
       color: var(--fg); background: var(--bg); line-height: 1.9; }
main { max-width: 720px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }
header.site { border-bottom: 1px solid var(--line); }
header.site .inner { max-width: 720px; margin: 0 auto; padding: 0.9rem 1.25rem;
                     display: flex; justify-content: space-between; align-items: baseline; }
header.site a { color: var(--fg); text-decoration: none; font-weight: 700; }
header.site .tag { color: var(--muted); font-size: 0.8rem; }
h1 { font-size: 1.5rem; line-height: 1.5; margin: 1.2rem 0 1rem; }
h2 { font-size: 1.1rem; margin: 2.2rem 0 0.8rem; padding-left: 0.6rem;
     border-left: 4px solid var(--accent); }
p.answer { font-size: 1.05rem; background: #f4f8f5; border-radius: 8px;
           padding: 1.1rem 1.2rem; margin-bottom: 1rem; }
p.summary { margin-bottom: 1rem; }
table { width: 100%; border-collapse: collapse; font-size: 0.92rem; }
.table-wrap { overflow-x: auto; }
th, td { text-align: left; padding: 0.6rem 0.7rem; border-bottom: 1px solid var(--line);
         vertical-align: top; }
th { white-space: nowrap; color: var(--muted); font-weight: 600; }
td.src { font-size: 0.82rem; color: var(--muted); white-space: nowrap; }
td.src a { color: var(--accent); }
ul.list { list-style: none; }
ul.list li { border-bottom: 1px solid var(--line); }
ul.list a { display: block; padding: 0.8rem 0.2rem; color: var(--fg); text-decoration: none; }
ul.list a:hover { color: var(--accent); }
.notice { font-size: 0.8rem; color: var(--muted); border: 1px dashed var(--line);
          border-radius: 6px; padding: 0.6rem 0.9rem; margin: 1.5rem 0 0; }
footer { max-width: 720px; margin: 0 auto; padding: 1.5rem 1.25rem 3rem;
         color: var(--muted); font-size: 0.8rem; border-top: 1px solid var(--line); }
a.back { color: var(--accent); font-size: 0.9rem; text-decoration: none; }
"""

SAMPLE_NOTICE = (
    "このページはサンプルコンテンツです。公開前に日本語ネイティブによる校閲と、"
    "各事実の一次情報源での再確認(【要確認】箇所)が必要です。"
)


def esc(s):
    return html.escape(str(s), quote=True)


def page(title, body, canonical, description="", jsonld=None):
    ld = ""
    if jsonld:
        ld = ('<script type="application/ld+json">'
              + json.dumps(jsonld, ensure_ascii=False) + "</script>")
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
<a href="/">{esc(CONFIG['site_name'])}</a>
<span class="tag">出典と確認日つきのブランド事実</span>
</div></header>
<main>
{body}
</main>
<footer>すべての記載には出典と確認日を明記しています。誤りを見つけた場合は出典とあわせてご指摘ください。</footer>
</body>
</html>
"""


def facts_table(facts):
    rows = []
    for f in facts:
        src = f'<a href="{esc(f["source_url"])}" rel="noopener">{esc(f["source"])}</a><br>確認日: {esc(f["checked"])}'
        rows.append(
            f"<tr><th>{esc(f['label'])}</th>"
            f"<td>{esc(f['value'])}</td>"
            f'<td class="src">{src}</td></tr>'
        )
    return ('<div class="table-wrap"><table>'
            "<tr><th>項目</th><th>内容</th><th>出典 / 確認日</th></tr>"
            + "".join(rows) + "</table></div>")


def load_dir(subdir):
    items = []
    for p in sorted((ROOT / "data" / subdir).glob("*.json")):
        items.append(json.loads(p.read_text(encoding="utf-8")))
    return items


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / ".nojekyll").write_text("")

    brands = load_dir("brands")
    qas = load_dir("qa")
    qa_by_slug = {q["slug"]: q for q in qas}
    urls = [f"{BASE}/"]

    # ブランド定位ページ
    for b in brands:
        url = f"{BASE}/brands/{b['slug']}/"
        urls.append(url)
        related = ""
        rel_items = [qa_by_slug[s] for s in b.get("related_qa", []) if s in qa_by_slug]
        if rel_items:
            links = "".join(
                f'<li><a href="/qa/{esc(q["slug"])}/">{esc(q["question"])}</a></li>'
                for q in rel_items
            )
            related = f'<h2>関連する質問</h2><ul class="list">{links}</ul>'
        notice = f'<p class="notice">{esc(SAMPLE_NOTICE)}</p>' if b.get("sample_notice") else ""
        body = (
            f"<h1>{esc(b['name'])}とはどんなブランドか</h1>"
            f'<p class="summary">{esc(b["summary"])}</p>'
            f"<h2>事実一覧</h2>{facts_table(b['facts'])}"
            f"{related}{notice}"
            f'<p style="margin-top:2rem"><a class="back" href="/">← ブランド一覧へ</a></p>'
        )
        jsonld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": f"{b['name']}とはどんなブランドか",
            "inLanguage": "ja",
            "dateModified": max(f["checked"] for f in b["facts"]),
            "about": {"@type": "Brand", "name": b["name_en"]},
            "url": url,
        }
        d = OUT / "brands" / b["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(
            page(f"{b['name']}とはどんなブランドか | {CONFIG['site_name']}",
                 body, url, b["summary"], jsonld),
            encoding="utf-8")

    # 問答ページ
    for q in qas:
        url = f"{BASE}/qa/{q['slug']}/"
        urls.append(url)
        brand_link = ""
        b = next((x for x in brands if x["slug"] == q.get("brand")), None)
        if b:
            brand_link = (f'<h2>ブランド情報</h2><ul class="list"><li>'
                          f'<a href="/brands/{esc(b["slug"])}/">{esc(b["name"])}のブランド定位ページ</a>'
                          f"</li></ul>")
        notice = f'<p class="notice">{esc(SAMPLE_NOTICE)}</p>' if q.get("sample_notice") else ""
        body = (
            f"<h1>{esc(q['question'])}</h1>"
            f'<p class="answer">{esc(q["answer"])}</p>'
            f"<h2>根拠となる事実</h2>{facts_table(q['facts'])}"
            f"{brand_link}{notice}"
            f'<p style="margin-top:2rem"><a class="back" href="/">← 質問一覧へ</a></p>'
        )
        jsonld = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "inLanguage": "ja",
            "mainEntity": [{
                "@type": "Question",
                "name": q["question"],
                "acceptedAnswer": {"@type": "Answer", "text": q["answer"]},
            }],
            "url": url,
        }
        d = OUT / "qa" / q["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(
            page(f"{q['question']} | {CONFIG['site_name']}",
                 body, url, q["answer"][:120], jsonld),
            encoding="utf-8")

    # トップページ
    brand_links = "".join(
        f'<li><a href="/brands/{esc(b["slug"])}/">{esc(b["name"])} — '
        f'{esc(b["country"])}のブランド</a></li>' for b in brands)
    qa_links = "".join(
        f'<li><a href="/qa/{esc(q["slug"])}/">{esc(q["question"])}</a></li>' for q in qas)
    body = (
        f"<h1>{esc(CONFIG['site_name'])}</h1>"
        f'<p class="summary">{esc(CONFIG["description"])}</p>'
        f'<h2>ブランド定位ページ</h2><ul class="list">{brand_links}</ul>'
        f'<h2>質問と答え</h2><ul class="list">{qa_links}</ul>'
    )
    (OUT / "index.html").write_text(
        page(CONFIG["site_name"], body, f"{BASE}/", CONFIG["description"]),
        encoding="utf-8")

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
