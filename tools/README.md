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

python3 tools/audit_sources.py    # 既存データの出典を信源登記に照らして監査
python3 tools/audit_sources.py --list   # 該当箇所を全部出す
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

## 信源登記(`sources.py`)

出典として認めるドメインは **`tools/sources.py` に一元化**してある。以前は各スクリプトが
自前のホワイトリストを持っていて内容がずれていたため統合した。判定は
「登録ドメイン自身とそのサブドメイン」で行うので、`support.dji.com` や
`faq.balmuda.com` のような公式サブドメインは自動的に通る。

| 区分 | 中身 |
|---|---|
| `GOV` | 日本の省庁・独立行政法人(国税庁、総務省技適、経産省、消費者庁、NITE、国交省、個情委 ほか) |
| `DISCLOSURE` | 法定開示(SEC、EDINET、JPX、HKEX、上交所・深交所、巨潮資訊、英Companies House) |
| `PRESS` | プレスリリース配信(PR TIMES、@Press、共同PRワイヤー ほか) |
| `MEDIA` | 報道機関(Impress系、ITmedia系、ASCII、マイナビ、日経系、CNET、東洋経済 ほか) |
| `RESEARCH` | 調査会社(BCN+R、GfK、IDC、MM総研) |
| `OFFICIAL` | ブランド公式。slug ごとに登録 |
| `CANDIDATE` | 今後追加しそうなブランドの公式ドメインを先回りで登録 |
| `QA` | 質問の出典のみ。**事実の根拠には使えない** |

新ブランドを足すときは `OFFICIAL` に slug と公式ドメインを 1 行足すだけでよい。
`kakaku.com` は子ドメインで扱いが違う(`news.`/`mag.` は事実可、`bbs.` は質問のみ)。

## 調査を依頼するときの注意

- 最も価値が高いのは各社の **「特定商取引法に基づく表記」** ページ。法人名・所在地・
  代表者が法律で公示されるため、「必ず存在し、必ず正しい」唯一のページになる。
  次いで 会社概要 / IR → 保証・修理 → プライバシーポリシー → 重要なお知らせ。
- 金額・台数・件数は記事に明記がある場合のみ記載させる。不明なら `【要確認】`。
  サイト側はこれを赤字表示して人間の確認待ちであることを示す。
- 日付は出典に明記されたものだけ。曜日から年を逆算するのは推定日付にあたるので不可。
- 出典は `sources.py` の登記内に限る。掲示板・個人ブログは事実の根拠にならない
  (質問の出典としては可)。
