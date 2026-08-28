#!/usr/bin/env python3
"""新規ブランドの調査結果を検証して data/brands/<slug>.json を新規作成する。

STAGING/newbrand/*.json を読み、既存ブランドと同じスキーマ・同じ検証ルールを
通したものだけを取り込む。捏造対策として、出典ホストが許可リストにないもの、
日付形式が不正なもの、実投稿URLでない質問は**除外して理由を出力**する。

  export STAGING=/path/to/staging
  python3 tools/merge_new_brand.py            # 既存slugがあればスキップ
  python3 tools/merge_new_brand.py --force    # 既存slugを上書き
"""
import json
import os
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

SRC = Path(os.environ.get("STAGING", "./staging")) / "newbrand"
BR = Path(__file__).resolve().parent.parent / "data" / "brands"
CHK = "2026-08-28"
FORCE = "--force" in sys.argv

SECTIONS = [
    "企業プロフィール", "日本での事業体制", "規制・安全性",
    "保証・アフターサービス", "製品ラインと価格帯",
]
# 既存ブランドと揃える標準ラベル。欠けているものは「未確認」で補い、
# ページ上で赤字表示されるようにする(何が未整備かを隠さないため)。
CANONICAL = {
    "企業プロフィール": ["正式社名", "本社所在地", "創業年", "創業者", "上場状況",
                         "従業員数", "年間売上規模", "主な事業領域"],
    "日本での事業体制": ["日本法人", "法人番号(13桁)", "日本法人設立年", "日本法人所在地",
                         "日本参入年", "直営店", "販売チャネル", "日本語公式サイト"],
    "規制・安全性": ["技適(技術基準適合証明)", "PSE(電気用品安全法)", "リコール・自主回収履歴",
                     "その他の法規制", "公的機関からの指摘", "データの保存先・越境移転"],
    "保証・アフターサービス": ["保証期間", "延長保証制度", "修理体制", "日本語サポート窓口",
                               "サポート受付時間", "消耗品・交換部品の入手性"],
    "製品ラインと価格帯": ["主力カテゴリ", "主な価格帯", "主要製品ライン", "日本での主な競合"],
}

# ブランドごとの公式ドメイン。そのドメイン自身とサブドメインを許可する
# (support. / help. / terms. / store. など、公式のサブドメインは多岐にわたるため)。
# 調査結果側から拡張させないため、ここで slug ごとに固定する。
OFFICIAL = {
    "irobot": {"irobot-jp.com", "irobot.com"},
    "ecovacs": {"ecovacs.com", "ecovacs.co.jp"},
    "nature-remo": {"nature.global"},
    "ugreen": {"ugreen.com"},
    "elecom": {"elecom.co.jp", "elecom-shop.jp"},
    "gopro": {"gopro.com"},
}
GOV = {"www.houjin-bangou.nta.go.jp", "houjin-bangou.nta.go.jp", "www.nta.go.jp",
       "www.tele.soumu.go.jp", "www.soumu.go.jp", "www.meti.go.jp", "www.caa.go.jp",
       "www.recall.caa.go.jp", "www.nite.go.jp", "www.ppc.go.jp", "www.mlit.go.jp",
       "www.ipa.go.jp", "www.jcpra.or.jp", "info.gbiz.go.jp",
       # 海外の法定開示。企業自身の提出書類なので一次情報として扱う
       "www.sec.gov", "sec.gov"}
NEWS = {"prtimes.jp", "www.itmedia.co.jp", "ascii.jp", "news.mynavi.jp",
        "www.nikkei.com", "japan.cnet.com", "gizmodo.jp", "www.gizmodo.jp",
        "robotstart.info", "gigazine.net", "kakaku.com", "news.kakaku.com",
        "www.phileweb.com", "toyokeizai.net", "www.reuters.com", "jp.reuters.com",
        "www.bloomberg.co.jp", "www.jiji.com", "www.rbbtoday.com", "www.techno-edge.net"}
SUFFIX = (".impress.co.jp", ".itmedia.co.jp", ".ascii.jp", ".nikkei.com",
          ".mynavi.jp", ".go.jp")
QA_HOSTS = {"detail.chiebukuro.yahoo.co.jp", "jp.quora.com", "oshiete.goo.ne.jp",
            "okwave.jp", "bbs.kakaku.com", "kakaku.com", "note.com", "b.hatena.ne.jp"}

# 調査結果のラベル表記ゆれを標準ラベルへ寄せる
ALIASES = {
    "法人番号": "法人番号(13桁)",
    "法人番号（13桁）": "法人番号(13桁)",
    "技適": "技適(技術基準適合証明)",
    "技適（技術基準適合証明）": "技適(技術基準適合証明)",
    "PSE": "PSE(電気用品安全法)",
    "PSE（電気用品安全法）": "PSE(電気用品安全法)",
    "日本での競合": "日本での主な競合",
    "価格帯": "主な価格帯",
}

TODAY = date.today().isoformat()


def host_ok(url, slug):
    h = urlparse(url or "").netloc
    if not h:
        return False
    if any(h == d or h.endswith("." + d) for d in OFFICIAL.get(slug, set())):
        return True
    return h in GOV or h in NEWS or any(h.endswith(s) for s in SUFFIX)


def is_unverified(v):
    return "【要確認】" in v or "未確認" in v


def houjin_bangou_ok(num):
    """国税庁の検査用数字アルゴリズムで法人番号13桁を検算する(merge_official.py と同一)。"""
    if not re.fullmatch(r"\d{13}", num):
        return False
    base = num[1:]
    tot = sum(int(base[12 - n]) * (1 if n % 2 else 2) for n in range(1, 13))
    return int(num[0]) == 9 - tot % 9


def check_brand(b, problems):
    """スキーマ検証。致命的な問題があれば False を返す。"""
    slug = b.get("slug", "")
    ok = True
    if not re.fullmatch(r"[a-z0-9-]+", slug):
        problems.append(f"slug形式不正 {slug!r}"); return False
    if slug not in OFFICIAL:
        problems.append(f"{slug}: 公式ホスト定義なし。OFFICIALに追加してから再実行"); return False
    for k in ("name", "name_en", "country", "summary"):
        if not str(b.get(k, "")).strip():
            problems.append(f"{slug}: {k} が空"); ok = False
    if len(str(b.get("summary", ""))) < 40:
        problems.append(f"{slug}: summary が短すぎる({len(str(b.get('summary','')))}字)"); ok = False
    return ok


def main():
    if not SRC.exists():
        print(f"入力なし: {SRC}"); return
    total_new = 0
    for p in sorted(SRC.glob("*.json")):
        problems = []
        try:
            b = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"{p.name}: JSONパース失敗 {e}"); continue
        if not check_brand(b, problems):
            print(f"\n=== {p.name}: 取り込み中止 ===")
            for x in problems: print("  -", x)
            continue
        slug = b["slug"]
        dest = BR / f"{slug}.json"
        if dest.exists() and not FORCE:
            print(f"{slug}: 既に存在するためスキップ(--force で上書き)"); continue

        # --- sections ---
        by_title = {}
        for s in b.get("sections", []):
            t = s.get("title", "")
            if t not in CANONICAL:
                problems.append(f"セクション名が規定外のため破棄: {t!r}"); continue
            by_title.setdefault(t, []).extend(s.get("facts", []))

        fallback_url = ""
        for fs in by_title.values():
            for f in fs:
                if not fallback_url and host_ok(f.get("source_url", ""), slug):
                    fallback_url = f["source_url"]
        if not fallback_url:
            problems.append("有効な出典URLが1件もない"); 
            print(f"\n=== {slug}: 取り込み中止 ===")
            for x in problems: print("  -", x)
            continue

        sections, n_drop = [], 0
        for title in SECTIONS:
            kept, seen = [], set()
            for f in by_title.get(title, []):
                label = str(f.get("label", "")).strip()
                label = ALIASES.get(label, label)
                value = str(f.get("value", "")).strip()
                if not label or not value:
                    problems.append(f"[{title}] label/value欠落"); n_drop += 1; continue
                if label in seen:
                    problems.append(f"[{title}] ラベル重複 {label}"); n_drop += 1; continue
                # 法人番号は検査用数字で検算し、合わないものは未確認に戻す
                if "法人番号" in label and not is_unverified(value):
                    m = re.search(r"\d{13}", value)
                    if not m or not houjin_bangou_ok(m.group(0)):
                        problems.append(f"[{title}] {label}: 検査用数字が不一致のため未確認へ "
                                        f"{m.group(0) if m else '13桁なし'}")
                        value = "未確認 — 国税庁法人番号公表サイトで法人名検索により取得可能。"
                url = str(f.get("source_url", "")).strip()
                if not host_ok(url, slug):
                    # 出典が使えない値は事実として採用せず、未確認として残す
                    problems.append(f"[{title}] {label}: 出典ホスト不正 "
                                    f"{urlparse(url).netloc!r} → 未確認に降格")
                    value = (value.rstrip("。") + "【要確認】") if not is_unverified(value) else value
                    url, src = fallback_url, "一次情報での確認待ち"
                    n_drop += 1
                else:
                    src = str(f.get("source", "")).strip() or "公式サイト"
                seen.add(label)
                kept.append({"label": label, "value": value, "source": src,
                             "source_url": url, "checked": f.get("checked") or CHK})
            # 標準ラベルの欠落を未確認で補う
            for label in CANONICAL[title]:
                if label not in seen:
                    kept.append({"label": label, "value": "未確認 — 一次情報での確認待ち",
                                 "source": "未確認", "source_url": fallback_url,
                                 "checked": CHK})
                    problems.append(f"[{title}] {label}: 調査結果になく未確認で補完")
            order = {l: i for i, l in enumerate(CANONICAL[title])}
            kept.sort(key=lambda f: (order.get(f["label"], 999), f["label"]))
            sections.append({"title": title, "facts": kept})

        # --- faq ---
        faqs, seen_slug, seen_q, seen_url = [], set(), set(), set()
        for i, q in enumerate(b.get("faq", [])):
            tag = f"faq[{i}]"
            if not isinstance(q, dict):
                continue
            miss = [k for k in ("slug", "question", "answer") if not q.get(k)]
            if miss:
                problems.append(f"{tag}: キー不足 {miss}"); continue
            if not re.fullmatch(r"[a-z0-9-]+", q["slug"]):
                problems.append(f"{tag}: slug形式不正 {q['slug']!r}"); continue
            if q["slug"] in seen_slug or q["question"] in seen_q:
                problems.append(f"{tag}: 重複"); continue
            s = q.get("source") or {}
            h = urlparse(s.get("url", "")).netloc
            if h not in QA_HOSTS:
                problems.append(f"{tag}: 質問URLのホスト不正 {h!r}"); continue
            if s["url"] in seen_url:
                problems.append(f"{tag}: 同じ元投稿URLが既出"); continue
            facts = [f for f in (q.get("facts") or [])
                     if host_ok(f.get("source_url", ""), slug)
                     and str(f.get("label", "")).strip() and str(f.get("value", "")).strip()]
            if len(facts) != len(q.get("facts") or []):
                problems.append(f"{tag}: 出典不正のfactを{len(q.get('facts') or []) - len(facts)}件除外")
            if not facts:
                problems.append(f"{tag}: 有効なfactsが0件のため除外"); continue
            for f in facts:
                f.setdefault("checked", CHK)
            seen_slug.add(q["slug"]); seen_q.add(q["question"]); seen_url.add(s["url"])
            faqs.append({"slug": q["slug"], "question": q["question"],
                         "source": {"platform": s.get("platform", ""), "url": s["url"],
                                    "original": s.get("original", "")},
                         "answer": q["answer"], "facts": facts})

        # --- updates ---
        ups, seen_t = [], set()
        for i, uu in enumerate(b.get("updates", [])):
            tag = f"updates[{i}]"
            if not isinstance(uu, dict):
                continue
            d = str(uu.get("date", ""))
            if not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", d):
                problems.append(f"{tag}: 日付形式不正 {d!r}"); continue
            if not uu.get("title") or not uu.get("body"):
                problems.append(f"{tag}: title/body欠落"); continue
            if not host_ok(uu.get("source_url", ""), slug):
                problems.append(f"{tag}: 出典ホスト不正 "
                                f"{urlparse(uu.get('source_url','')).netloc!r}"); continue
            if uu["title"] in seen_t:
                problems.append(f"{tag}: タイトル重複"); continue
            seen_t.add(uu["title"])
            ups.append({"date": d, "title": uu["title"], "body": uu["body"],
                        "impact": uu.get("impact", ""), "source": uu.get("source", ""),
                        "source_url": uu["source_url"]})
        ups.sort(key=lambda x: x["date"], reverse=True)

        out = {"slug": slug, "name": b["name"], "name_en": b["name_en"],
               "country": b["country"], "summary": b["summary"],
               "sample_notice": bool(b.get("sample_notice", True)),
               "faq": faqs, "sections": sections, "updates": ups}
        dest.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        total_new += 1
        nf = sum(len(s["facts"]) for s in sections)
        nok = sum(1 for s in sections for f in s["facts"] if not is_unverified(f["value"]))
        print(f"\n=== {slug} を作成: {dest} ===")
        print(f"  事実 {nok}/{nf} 項目が出典つきで確認済み ({nok/nf:.0%}) / "
              f"FAQ {len(faqs)}件 / タイムライン {len(ups)}件"
              + (f" ({ups[-1]['date']}〜{ups[0]['date']})" if ups else ""))
        if problems:
            print(f"  検証で除外・降格・補完したもの {len(problems)}件:")
            for x in problems[:30]:
                print("    -", x)
            if len(problems) > 30:
                print(f"    ... 他 {len(problems) - 30}件")

    print(f"\n新規ブランド {total_new}件を作成")


if __name__ == "__main__":
    main()
