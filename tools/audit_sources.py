#!/usr/bin/env python3
"""既存データの出典を信源登記(sources.py)に照らして監査する。

取り込みスクリプトは新規データしか見ない。登記簿を作る前に入ったデータが
残っているため、全ブランドを走査して区分ごとに集計し、登記外のホストを
一覧する。--list で該当箇所を全部出す。

  python3 tools/audit_sources.py
  python3 tools/audit_sources.py --list
"""
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sources import classify, host  # noqa: E402

BR = Path(__file__).resolve().parent.parent / "data" / "brands"
LIST = "--list" in sys.argv


def entries(b):
    """(区分ラベル, URL, 説明) を全部返す。質問の出典は別枠。"""
    slug = b["slug"]
    for s in b.get("sections", []):
        for f in s["facts"]:
            yield "fact", f["source_url"], f"{slug} 事実「{f['label']}」"
    for q in b.get("faq", []):
        for f in q.get("facts", []):
            yield "fact", f.get("source_url", ""), f"{slug} FAQ {q['slug']} の根拠"
        for r in q.get("sources", []):
            yield "fact", r.get("url", ""), f"{slug} FAQ {q['slug']} の参照"
        if q.get("source"):
            yield "question", q["source"]["url"], f"{slug} FAQ {q['slug']} の元投稿"
    for u in b.get("updates", []):
        yield "fact", u["source_url"], f"{slug} 年表「{u['title'][:28]}」"


def main():
    kinds = collections.Counter()
    bad_hosts = collections.Counter()
    bad_rows, bad_q = [], []
    per_brand = collections.Counter()

    for p in sorted(BR.glob("*.json")):
        b = json.loads(p.read_text(encoding="utf-8"))
        for kind, url, where in entries(b):
            c = classify(url, b["slug"])
            if kind == "question":
                kinds[f"question:{c}"] += 1
                if c != "qa":
                    bad_q.append((where, host(url)))
                continue
            kinds[c] += 1
            if c in ("unlisted", "qa", "empty"):
                bad_hosts[host(url) or "(空)"] += 1
                per_brand[b["slug"]] += 1
                bad_rows.append((where, host(url) or "(空)", c))

    total = sum(v for k, v in kinds.items() if not k.startswith("question:"))
    ok = total - len(bad_rows)
    print(f"事実の出典 {total}件 / 信源登記に適合 {ok}件 ({ok / total:.1%})\n")
    print("区分ごとの内訳:")
    for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
        print(f"  {v:5d}  {k}")

    if bad_rows:
        print(f"\n登記外の出典 {len(bad_rows)}件 / ホスト {len(bad_hosts)}種:")
        for h, n in bad_hosts.most_common(30):
            print(f"  {n:4d}  {h}")
        print("\nブランド別:")
        for s, n in per_brand.most_common():
            print(f"  {n:4d}  {s}")
    if bad_q:
        print(f"\n質問の出典が QA プラットフォームでないもの {len(bad_q)}件:")
        for w, h in bad_q[:20]:
            print(f"  {h:32s} {w}")
    if LIST and bad_rows:
        print(f"\n--- 該当箇所 {len(bad_rows)}件 ---")
        for w, h, c in bad_rows:
            print(f"  [{c:8s}] {h:34s} {w}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:   # head などでパイプが閉じられた場合
        sys.stderr.close()
