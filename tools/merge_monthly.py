#!/usr/bin/env python3
"""月次動向をブランドJSONのupdatesへマージする。"""
import json
import os, re, sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sources import host_ok  # noqa: E402

SRC = Path(os.environ.get("STAGING", "./staging")) / "monthly"
BR = Path(__file__).resolve().parent.parent / "data" / "brands"

added, skipped, problems = 0, 0, []
for p in sorted(SRC.glob("*.json")):
    data = json.loads(p.read_text(encoding="utf-8"))
    for slug, items in data.items():
        bp = BR / f"{slug}.json"
        if not bp.exists() or not isinstance(items, list):
            continue
        b = json.loads(bp.read_text(encoding="utf-8"))
        ups = b.get("updates", [])
        seen = {u["title"] for u in ups}
        n = 0
        for i, u in enumerate(items):
            tag = f"{slug}[{i}]"
            if not isinstance(u, dict):
                continue
            if not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", str(u.get("date", ""))):
                problems.append(f"{tag}: 日付形式不正 {u.get('date')!r}"); skipped += 1; continue
            if u["date"] > date.today().isoformat():
                problems.append(f"{tag}: date が未来日付 {u['date']}。date は発表日・報道日。"
                                "施行日や終了日は effective に入れる"); skipped += 1; continue
            if not u.get("title") or not u.get("body"):
                problems.append(f"{tag}: title/body欠落"); skipped += 1; continue
            url = u.get("source_url", "")
            if not host_ok(url, slug):
                problems.append(f"{tag}: 出典ホストが信源登記にない "
                                f"{urlparse(url).netloc!r}"); skipped += 1; continue
            if u["title"] in seen:
                skipped += 1; continue
            seen.add(u["title"])
            entry = {"date": u["date"], "title": u["title"], "body": u["body"],
                     "impact": u.get("impact", ""), "source": u.get("source", ""),
                     "source_url": url}
            if u.get("effective"):
                entry["effective"] = u["effective"]
                entry["effective_label"] = u.get("effective_label", "施行予定")
            ups.append(entry)
            n += 1; added += 1
        b["updates"] = sorted(ups, key=lambda x: x["date"], reverse=True)
        bp.write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{slug}: +{n}件 (合計 {len(ups)}件)")

print(f"\n追加 {added}件 / 除外 {skipped}件")
for x in problems[:20]:
    print("  -", x)
