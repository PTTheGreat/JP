#!/usr/bin/env python3
"""社媒由来の新規FAQを検証してブランドJSONへ追記する。"""
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

SRC = Path(os.environ.get("STAGING", "./staging")) / "social"
BR = Path(__file__).resolve().parent.parent / "data" / "brands"

QA_HOSTS = {"detail.chiebukuro.yahoo.co.jp", "jp.quora.com", "oshiete.goo.ne.jp",
            "okwave.jp", "bbs.kakaku.com", "note.com", "b.hatena.ne.jp",
            "kakaku.com"}
FACT_HOSTS = {
    "www.ankerjapan.com", "corp.ankerjapan.com", "lp.ankerjapan.com", "ankerjapan.com",
    "www.mi.com", "www.switchbot.jp", "www.roborock.jp", "jp.roborock.com",
    "www.dji.com", "store.dji.com", "www.insta360.com", "store.insta360.com",
    "connectinternationalone.co.jp", "www.balmuda.com", "corp.balmuda.com",
    "tech.balmuda.com", "www.shark.co.jp", "www.ninja.co.jp", "sharkninja.com",
    "www.sharkninja.jp", "www.dyson.co.jp", "www.irobot-jp.com", "www.ecovacs.com",
    "nature.global", "jp.shop.gopro.com", "theta360.com", "www.aladdin-aic.com",
    "www.anker.com", "www.archisite.co.jp", "archisite.co.jp",
    "www.houjin-bangou.nta.go.jp", "www.tele.soumu.go.jp", "www.recall.caa.go.jp",
    "www.meti.go.jp", "www.mlit.go.jp", "www.ossportal.dips.mlit.go.jp",
    "www.soumu.go.jp", "www.ipa.go.jp", "www.gfk.com", "www.idc.com",
    "panasonic.jp", "my-best.com", "www.nite.go.jp", "www.ppc.go.jp",
    "www.jcpra.or.jp", "www.itmedia.co.jp", "www.nikkei.com",
    # 各ブランドの公式サブドメイン(サポート・修理・直販・FAQ)
    "support.dji.com", "repair.dji.com", "www.dji.com",
    "direct.shark.co.jp", "support.switch-bot.com", "switch-bot.com",
    "files.roborock.com", "faq.balmuda.com", "support.insta360.com",
    "www.rakuten.ne.jp",
    # 追加ブランドの公式ホスト
    "www.irobot-jp.com", "irobot-jp.com", "store.irobot-jp.com", "www.irobot.com",
    "jp.ecovacs.com", "www.ecovacs.co.jp", "nature.global", "shop.nature.global",
    "jp.ugreen.com", "www.ugreen.com", "www.elecom.co.jp", "elecom-shop.jp",
    "gopro.com", "jp.gopro.com", "jp.shop.gopro.com",
}

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
            h = urlparse(q["source"].get("url", "")).netloc
            if h not in QA_HOSTS:
                problems.append(f"{tag}: 質問URLのホスト不正 {h!r}")
                continue
            if q["source"]["url"] in seen_url:
                problems.append(f"{tag}: 同じ元投稿URLが既出")
                continue
            bad = [f.get("source_url") for f in q["facts"]
                   if urlparse(f.get("source_url", "")).netloc not in FACT_HOSTS]
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
