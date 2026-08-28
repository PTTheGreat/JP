#!/usr/bin/env python3
"""公式サイト由来の事実をブランドJSONへ反映する。

- 既存ラベルと一致 → value/source/source_url を上書き(赤字が黒字になる)
- 新規ラベル → キーワードで該当セクションへ追加
- evidence は data には入れず、検証ログとして出力する
"""
import json
import os
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

SRC = Path(os.environ.get("STAGING", "./staging")) / "official"
BR = Path(__file__).resolve().parent.parent / "data" / "brands"
CHK = os.environ.get("CHECKED_DATE") or date.today().isoformat()

SECTION_KEYS = [
    ("企業プロフィール", ["社名", "本社", "創業", "設立年", "上場", "従業員", "売上",
                          "事業領域", "沿革", "資本金", "代表者"]),
    ("日本での事業体制", ["日本法人", "法人番号", "所在地", "参入", "直営店", "店舗",
                          "販売チャネル", "販売先", "公式サイト", "拠点"]),
    ("規制・安全性", ["技適", "PSE", "リコール", "回収", "法規", "公的機関", "認証",
                      "セキュリティ", "脆弱性", "データの保存", "越境"]),
    ("保証・アフターサービス", ["保証", "修理", "サポート", "消耗品", "部品", "返品",
                                "送料", "問い合わせ", "受付", "交換", "並行輸入"]),
    ("製品ラインと価格帯", ["カテゴリ", "価格", "製品ライン", "競合", "主力"]),
]


def pick_section(label):
    for name, keys in SECTION_KEYS:
        if any(k in label for k in keys):
            return name
    return "企業プロフィール"


def is_unverified(v):
    return "【要確認】" in v or "未確認" in v


def houjin_bangou_ok(num):
    """国税庁の検査用数字アルゴリズムで法人番号13桁を検算する。

    検査用数字 = 9 - (Σ[n=1..12] Pn × Qn) mod 9
      Pn: 下12桁の下からn桁目、Qn: n が奇数なら1・偶数なら2
    調査結果に紛れ込んだ「桁数だけ合っている番号」を弾くための捏造対策。
    """
    if not re.fullmatch(r"\d{13}", num):
        return False
    base = num[1:]
    tot = sum(int(base[12 - n]) * (1 if n % 2 else 2) for n in range(1, 13))
    return int(num[0]) == 9 - tot % 9


updated = added = skipped = 0
log = []

for p in sorted(SRC.glob("*.json")):
    data = json.loads(p.read_text(encoding="utf-8"))
    for slug, items in data.items():
        bp = BR / f"{slug}.json"
        if not bp.exists() or not isinstance(items, list):
            continue
        b = json.loads(bp.read_text(encoding="utf-8"))
        secs = b.get("sections", [])
        by_label = {}
        for s in secs:
            for f in s["facts"]:
                by_label.setdefault(f["label"], (s, f))

        for it in items:
            if not isinstance(it, dict):
                continue
            label = (it.get("label") or "").strip()
            value = (it.get("value") or "").strip()
            url = (it.get("source_url") or "").strip()
            src = (it.get("source") or "公式サイト").strip()
            if not label or not value or not urlparse(url).scheme.startswith("http"):
                skipped += 1
                continue

            # 法人番号は検査用数字で検算し、合わないものは取り込まない
            if "法人番号" in label and not is_unverified(value):
                m = re.search(r"\d{13}", value)
                if not m:
                    log.append(f"  {slug}: 法人番号に13桁が見当たらないため除外")
                    skipped += 1
                    continue
                if not houjin_bangou_ok(m.group(0)):
                    log.append(f"  {slug}: 法人番号の検査用数字が不一致のため除外 "
                               f"{m.group(0)}")
                    skipped += 1
                    continue

            if label in by_label:
                sec, fact = by_label[label]
                was_red = is_unverified(fact["value"])
                fact["value"] = value
                fact["source"] = src
                fact["source_url"] = url
                fact["checked"] = CHK
                updated += 1
                if was_red and not is_unverified(value):
                    log.append(f"  {slug}: 赤→黒 {label}")
            else:
                target = pick_section(label)
                sec = next((s for s in secs if s["title"] == target), None)
                if sec is None:
                    continue
                sec["facts"].append({"label": label, "value": value, "source": src,
                                     "source_url": url, "checked": CHK})
                by_label[label] = (sec, sec["facts"][-1])
                added += 1

        b["sections"] = secs
        bp.write_text(json.dumps(b, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(f"上書き {updated}件 / 新規追加 {added}件 / スキップ {skipped}件")
if log:
    print(f"\n変更・除外の記録 ({len(log)}件):")
    for x in log[:40]:
        print(x)

print("\n各ブランドの確認率:")
for p in sorted(BR.glob("*.json")):
    b = json.loads(p.read_text(encoding="utf-8"))
    fs = [f for s in b.get("sections", []) for f in s["facts"]]
    unv = sum(1 for f in fs if is_unverified(f["value"]))
    ok = len(fs) - unv
    print(f"  {b['slug']:12s} {ok:2d}/{len(fs):2d} ({ok / len(fs):.0%})")
