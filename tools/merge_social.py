#!/usr/bin/env python3
"""社媒由来の新規FAQを検証してブランドJSONへ追記する。"""
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sources import host_ok, qa_ok  # noqa: E402

SRC = Path(os.environ.get("STAGING", "./staging")) / "social"
BR = Path(__file__).resolve().parent.parent / "data" / "brands"

problems, added = [], 0

for p in sorted(SRC.glob("*.json")):
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        problems.append(f"{p.name}: JSONパース失敗 {e}")
        continue

    for slug, items in data.items():
        bp = BR / f"{slug}.json"
        if not bp.exists() or not isinstance(items, list):
            continue
        b = json.loads(bp.read_text(encoding="utf-8"))
        faqs = b.get("faq", [])
        seen_slug = {f["slug"] for f in faqs}
        seen_url = {f["source"]["url"] for f in faqs if f.get("source")}
        seen_q = {f["question"] for f in faqs}
        n = 0

        for i, q in enumerate(items):
            tag = f"{slug}[{i}]"
            if not isinstance(q, dict):
                continue
            miss = [k for k in ("slug", "question", "source", "answer", "facts") if k not in q]
            if miss:
                problems.append(f"{tag}: キー不足 {miss}")
                continue
            if not re.fullmatch(r"[a-z0-9-]+", q["slug"]):
                problems.append(f"{tag}: slug形式不正 {q['slug']!r}")
                continue
            if q["slug"] in seen_slug:
                problems.append(f"{tag}: slug重複 {q['slug']}")
                continue
            if q["question"] in seen_q:
                problems.append(f"{tag}: 質問文が既存と重複")
                continue
            if not qa_ok(q["source"].get("url", "")):
                problems.append(f"{tag}: 質問URLのホストが信源登記にない "
                                f"{urlparse(q['source'].get('url', '')).netloc!r}")
                continue
            if q["source"]["url"] in seen_url:
                problems.append(f"{tag}: 同じ元投稿URLが既出")
                continue
            bad = [f.get("source_url") for f in q["facts"]
                   if not host_ok(f.get("source_url", ""), slug)]
            if bad:
                problems.append(f"{tag}: facts出典URL不正 {bad}")
                continue
            if not q["facts"]:
                problems.append(f"{tag}: factsが空")
                continue
            seen_slug.add(q["slug"])
            seen_url.add(q["source"]["url"])
            seen_q.add(q["question"])
            faqs.append(q)
            n += 1
            added += 1

        b["faq"] = faqs
        bp.write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{slug}: +{n}件 (合計 {len(faqs)}件)")

print(f"\n新規追加 合計 {added}件")
if problems:
    print(f"\n除外 {len(problems)}件:")
    for x in problems[:25]:
        print("  -", x)
