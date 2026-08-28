#!/usr/bin/env python3
"""月次動向をブランドJSONのupdatesへマージする。"""
import json
import os, re
from pathlib import Path
from urllib.parse import urlparse

SRC = Path(os.environ.get("STAGING", "./staging")) / "monthly"
BR = Path(__file__).resolve().parent.parent / "data" / "brands"

NEWS_HOSTS = {
    "news.kakaku.com", "kakaku.com", "bbs.kakaku.com",
    "kaden.watch.impress.co.jp", "k-tai.watch.impress.co.jp",
    "dc.watch.impress.co.jp", "internet.watch.impress.co.jp",
    "av.watch.impress.co.jp", "pc.watch.impress.co.jp", "www.watch.impress.co.jp",
    "www.itmedia.co.jp", "monoist.itmedia.co.jp", "www.techno-edge.net",
    "ascii.jp", "gigazine.net", "prtimes.jp", "www.nikkei.com",
    "news.mynavi.jp", "www.phileweb.com", "jetstream.blog",
    "www.gizmodo.jp", "gizmodo.jp", "japan.cnet.com", "www.jiji.com",
    "news.yahoo.co.jp", "news.infoseek.co.jp", "toyokeizai.net",
    "www.publickey1.jp", "robotstart.info", "dronetimes.jp", "www.drone.jp",
}
OFFICIAL_HOSTS = {
    "www.ankerjapan.com", "corp.ankerjapan.com", "lp.ankerjapan.com",
    "connectinternationalone.co.jp", "www.mi.com", "www.switchbot.jp",
    "www.roborock.jp", "jp.roborock.com", "www.dji.com", "store.dji.com",
    "support.dji.com", "www.insta360.com", "store.insta360.com",
    "www.balmuda.com", "corp.balmuda.com", "www.dyson.co.jp",
    "www.shark.co.jp", "www.ninja.co.jp", "sharkninja.com", "direct.shark.co.jp",
    "www.archisite.co.jp", "www.irobot-jp.com", "www.ecovacs.com",
    "www.meti.go.jp", "www.caa.go.jp", "www.recall.caa.go.jp",
    "www.soumu.go.jp", "www.mlit.go.jp", "www.nite.go.jp", "www.ipa.go.jp",
    "www.houjin-bangou.nta.go.jp", "www.tele.soumu.go.jp", "www.ppc.go.jp",
    "www.jcpra.or.jp", "www.ossportal.dips.mlit.go.jp",
}
OK = NEWS_HOSTS | OFFICIAL_HOSTS
# 系列メディアはサブドメインが多いため接尾辞でも許可する
OK_SUFFIX = (
    ".impress.co.jp", ".ascii.jp", ".itmedia.co.jp", ".watch.impress.co.jp",
    ".nikkei.com", ".mynavi.jp", ".go.jp",
)
# 専門メディア・公的開示プラットフォーム
OK |= {
    "drone.jp", "www.drone.jp", "dronelife.com", "www.cined.com",
    "www.moguravr.com", "www.traicy.com", "aait.co.jp",
    "dataclouds.cninfo.com.cn", "www.cninfo.com.cn",
    "robotstart.info", "www.rbbtoday.com", "japanese.engadget.com",
    "www.appbank.net", "cas.softbank.jp", "www.kobe-np.co.jp", "www.gdm.or.jp",
}


def host_ok(h):
    return h in OK or any(h.endswith(sfx) for sfx in OK_SUFFIX)

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
            if not u.get("title") or not u.get("body"):
                problems.append(f"{tag}: title/body欠落"); skipped += 1; continue
            url = u.get("source_url", "")
            host = urlparse(url).netloc
            if not host_ok(host):
                problems.append(f"{tag}: 出典ホスト不正 {host!r}"); skipped += 1; continue
            if u["title"] in seen:
                skipped += 1; continue
            seen.add(u["title"])
            ups.append({"date": u["date"], "title": u["title"], "body": u["body"],
                        "impact": u.get("impact", ""), "source": u.get("source", ""),
                        "source_url": url})
            n += 1; added += 1
        b["updates"] = sorted(ups, key=lambda x: x["date"], reverse=True)
        bp.write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{slug}: +{n}件 (合計 {len(ups)}件)")

print(f"\n追加 {added}件 / 除外 {skipped}件")
for x in problems[:20]:
    print("  -", x)
