# 内容生産パイプライン

調査結果(JSON)を検証してブランドデータへ取り込むスクリプト群。
サブエージェントに調査させた結果を、捏造チェックを通してから `data/brands/*.json` に反映する。

## 使い方

調査結果を置くディレクトリを `STAGING` で指定する(既定は `./staging`)。

```bash
export STAGING=/path/to/staging
python3 tools/merge_official.py   # STAGING/official/*.json  → 事実フィールドを公式サイト出典で上書き
python3 tools/merge_social.py     # STAGING/social/*.json    → 実ユーザー投稿ベースのFAQを追記
python3 tools/merge_monthly.py    # STAGING/monthly/*.json   → 月次動向をタイムラインへ追記
python3 tools/merge_fresh.py      # STAGING/fresh/*.json     → 制度変更等をタイムライン+時事FAQへ
python3 tools/merge_new_brand.py  # STAGING/newbrand/*.json  → 新規ブランドを data/brands/ に作成
python3 build.py                  # docs/ を再生成
```

`merge_new_brand.py` だけは既存ブランドへの追記ではなく**新規ファイルの作成**を行う。
既に同じ slug がある場合はスキップし、`--force` を付けたときだけ上書きする。

## 検証ルール(捏造対策)

各スクリプトは取り込み前に以下を検証し、通らないものは**除外して理由を出力**する。

| 項目 | ルール |
|---|---|
| 質問の出典URL | Yahoo!知恵袋・価格.com・教えて!goo・OKWAVE・Quora日本版・note・はてブ のみ |
| 事実の出典URL | 各ブランド公式ドメイン、政府機関(go.jp)、主要報道機関のみ。個人ブログは事実の根拠として不可 |
| タイムラインの日付 | `YYYY-MM-DD` 形式かつ根拠のあるものだけ。推定日付は不可 |
| 重複 | slug・質問文・元投稿URL・タイトルで判定 |
| 新規ブランドのセクション | 規定の5セクション名と完全一致するもののみ。それ以外は破棄 |
| 新規ブランドの標準31項目 | 調査結果に無い項目は削除せず「未確認」で補完し、ページ上で赤字表示する |
| 新規ブランドの公式ホスト | `merge_new_brand.py` の `OFFICIAL` に slug ごとに定義する。調査結果側からは拡張できない |

ホストのホワイトリストは各スクリプト冒頭にある。正規の公式サブドメイン
(`support.dji.com`、`faq.balmuda.com` 等)や系列メディア(`*.impress.co.jp` 等)が
弾かれた場合はここに追加する。

## 調査を依頼するときの注意

- この環境ではWebFetchによる直接取得がegress proxyでブロックされる。
  公式サイトの内容は **WebSearch の `allowed_domains` でドメインを絞る** ことで
  検索スニペット経由で取得する。最も価値が高いのは各社の
  **「特定商取引法に基づく表記」**ページ(法人名・所在地・代表者が法定公示される)。
- WebSearch にはセッションあたりの回数上限がある。1セッションで10ブランド分を
  網羅しようとすると枯渇するため、ブランドを分けて依頼する。
- 金額・台数・件数は記事に明記がある場合のみ記載させる。不明なら `【要確認】`。
  サイト側はこれを赤字表示して人間の確認待ちであることを示す。
