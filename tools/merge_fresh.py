#!/usr/bin/env python3
"""最新情報(fresh/*.json)をブランドJSONへマージする。

- cross_brand_facts → updates(タイムライン)
- 各ブランドの質問 → topical FAQ(実投稿ベースではなく時事ベース)
"""
import json
import os
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlparse

SRC = Path(os.environ.get("STAGING", "./staging")) / "fresh"
BR = Path(__file__).resolve().parent.parent / "data" / "brands"
BRANDS = {p.stem for p in BR.glob("*.json")}

BAD_DATE = {"不明", "", None}


def norm_date(d):
    """YYYY-MM-DD を抽出。取れなければ None。"""
    if not d:
        return None
    m = re.search(r"(20\d{2})[-/](\d{1,2})(?:[-/](\d{1,2}))?", str(d))
    if not m:
        return None
    y, mo, da = m.group(1), int(m.group(2)), int(m.group(3) or 1)
    return f"{y}-{mo:02d}-{da:02d}"


def slugify(text, prefix):
    """日本語の質問から英数字slugを作れないため、連番ベースにする。"""
    h = abs(hash(text)) % 10000
    return f"{prefix}-topic-{h:04d}"


def clean_sources(sources):
    out = []
    for s in sources or []:
        if not isinstance(s, dict) or not s.get("url"):
            continue
        if not urlparse(s["url"]).scheme.startswith("http"):
            continue
        out.append({"name": s.get("name", "出典"), "url": s["url"],
                    "published": norm_date(s.get("published")) or "不明"})
    return out


added_up = added_faq = 0

for p in sorted(SRC.glob("*.json")):
    data = json.loads(p.read_text(encoding="utf-8"))

    # 1) cross_brand_facts → updates
    for c in data.get("cross_brand_facts", []):
        date = norm_date(c.get("effective_date")) or norm_date(
            (clean_sources(c.get("sources")) or [{}])[0].get("published"))
        if not date:
            continue
        srcs = clean_sources(c.get("sources"))
        for slug in c.get("affects", []):
            if slug not in BRANDS:
                continue
            bp = BR / f"{slug}.json"
            b = json.loads(bp.read_text(encoding="utf-8"))
            ups = b.get("updates", [])
            title = c["topic"]
            if any(u["title"] == title for u in ups):
                continue
            ups.append({
                "date": date,
                "title": title,
                "body": c.get("summary_ja", ""),
                "impact": c.get("impact", ""),
                "source": srcs[0]["name"] if srcs else "",
                "source_url": srcs[0]["url"] if srcs else "",
            })
            b["updates"] = ups
            bp.write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
            added_up += 1

    # 2) 各ブランドの質問 → topical FAQ
    for slug, items in data.items():
        if slug not in BRANDS or not isinstance(items, list):
            continue
        bp = BR / f"{slug}.json"
        b = json.loads(bp.read_text(encoding="utf-8"))
        faqs = b.get("faq", [])
        existing_q = {f["question"] for f in faqs}
        existing_s = {f["slug"] for f in faqs}
        for q in items:
            if not isinstance(q, dict):
                continue
            question = (q.get("question_ja") or "").strip()
            answer = (q.get("answer_basis_ja") or "").strip()
            if not question or not answer or question in existing_q:
                continue
            srcs = clean_sources(q.get("sources"))
            if not srcs:
                continue
            s = slugify(question, slug)
            while s in existing_s:
                s += "x"
            existing_s.add(s)
            existing_q.add(question)
            faqs.append({
                "slug": s,
                "question": question,
                "topical": True,
                "answer": answer,
                "sources": srcs,
            })
            added_faq += 1
        b["faq"] = faqs
        bp.write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")

print(f"updates追加: {added_up}件 / topical FAQ追加: {added_faq}件")

for p in sorted(BR.glob("*.json")):
    b = json.loads(p.read_text(encoding="utf-8"))
    nt = sum(1 for f in b.get("faq", []) if f.get("topical"))
    print(f"  {b['slug']:12s} updates={len(b.get('updates', [])):2d} "
          f"faq={len(b.get('faq', led:=[])):3d} (うち最新話題 {nt})"
          if False else
          f"  {b['slug']:12s} updates={len(b.get('updates', [])):2d} "
          f"faq={len(b.get('faq', [])):3d} (うち最新話題 {nt})")
