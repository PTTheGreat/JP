#!/usr/bin/env python3
"""信源登記 ― 本サイトが事実の根拠として認めるドメインの一覧。

取り込みスクリプトはすべてここを参照する。以前は各スクリプトが自前の
ホワイトリストを持っていて内容がずれていたため、単一の登記簿に統合した。

判定は「登録ドメイン自身とそのサブドメイン」で行う(`support.` `help.`
`corp.` `terms.` 等、公式のサブドメインは多岐にわたるため)。

  from sources import host_ok, qa_ok, classify
  host_ok("https://www.dyson.co.jp/...", "dyson")   # 事実の出典として可か
  qa_ok("https://detail.chiebukuro.yahoo.co.jp/...") # 質問の出典として可か
  classify(url)  # どの区分に当たるか(監査用)
"""
from urllib.parse import urlparse

# ---------------------------------------------------------------- 公的機関
# 日本の省庁・独立行政法人・法定公示。事実の根拠として最上位。
GOV = {
    # 法人格・登記
    "houjin-bangou.nta.go.jp",      # 国税庁 法人番号公表サイト
    "nta.go.jp",                    # 国税庁
    "info.gbiz.go.jp",              # 経産省 gBizINFO(法人番号ベースの公的DB)
    # 電波・通信
    "tele.soumu.go.jp",             # 総務省 技適(技術基準適合証明等)検索
    "soumu.go.jp",                  # 総務省(電波法・電気通信事業法)
    # 製品安全・リコール
    "meti.go.jp",                   # 経済産業省(電安法PSE・リコール・行政指導)
    "caa.go.jp",                    # 消費者庁
    "recall.caa.go.jp",             # 消費者庁 リコール情報サイト
    "nite.go.jp",                   # NITE 製品評価技術基盤機構(事故情報)
    # 航空・ドローン
    "mlit.go.jp",                   # 国土交通省(航空法)
    "ossportal.dips.mlit.go.jp",    # DIPS ドローン情報基盤システム
    # 個人情報・セキュリティ
    "ppc.go.jp",                    # 個人情報保護委員会(越境移転)
    "ipa.go.jp",                    # IPA(JC-STAR・脆弱性)
    "jpcert.or.jp",                 # JPCERT/CC
    # 競争法・その他
    "jftc.go.jp",                   # 公正取引委員会
    "cao.go.jp",                    # 内閣府
    "env.go.jp",                    # 環境省(資源循環)
    # 準公的団体
    "jcpra.or.jp",                  # 日本容器包装リサイクル協会
    "aeha.or.jp",                   # 家電製品協会
    "jbrc.com",                      # JBRC 小型充電式電池リサイクル
}

# ------------------------------------------------------------ 法定開示・取引所
# 企業自身が法的義務として提出した書類。IR ページより強い。
DISCLOSURE = {
    "sec.gov",                       # 米SEC EDGAR
    "disclosure.edinet-fsa.go.jp",   # 金融庁 EDINET(有価証券報告書)
    "disclosure2.edinet-fsa.go.jp",
    "jpx.co.jp",                     # 日本取引所グループ
    "hkexnews.hk",                   # 香港交易所 開示
    "sse.com.cn",                    # 上海証券取引所
    "szse.cn",                       # 深圳証券取引所
    "cninfo.com.cn",                 # 巨潮資訊(中国上場企業の法定開示)
    "find-and-update.company-information.service.gov.uk",  # 英 Companies House
}

# ---------------------------------------------------------- プレスリリース配信
# 企業が配信した一次リリース。配信日が明記されるため時系列の根拠に強い。
PRESS = {
    "prtimes.jp",
    "atpress.ne.jp",
    "kyodonewsprwire.jp",
    "businesswire.com",
    "prnewswire.com",
}

# ------------------------------------------------------------------ 報道機関
MEDIA = {
    # IT・家電系(日本)
    "impress.co.jp",                 # 家電/PC/AV/ケータイ/DC/Internet Watch 等を包含
    "itmedia.co.jp",
    "ascii.jp",
    "mynavi.jp",
    "nikkei.com",                    # xtech./xtrend. を包含
    "cnet.com", "japan.cnet.com",
    "gizmodo.jp",
    "techno-edge.net",
    "gigazine.net",
    "publickey1.jp",
    "rbbtoday.com",
    "phileweb.com",
    "robotstart.info",
    "moguravr.com",
    "kakaku.com",                    # news./ mag. のみ。掲示板は QA 扱い(下記)
    "bcnretail.com",                 # BCN+R 家電量販POSシェア
    # 総合・経済
    "jiji.com",
    "kyodo.co.jp", "nordot.app",
    "toyokeizai.net",
    "diamond.jp",
    "nikkan.co.jp",                  # 日刊工業新聞
    # 海外
    "reuters.com",
    "bloomberg.co.jp", "bloomberg.com",
    # 専門
    "drone.jp", "dronelife.com", "dronedj.com",
    "cined.com",
    "traicy.com",
}

# ------------------------------------------------------------------ 調査会社
RESEARCH = {
    "gfk.com",
    "idc.com",
    "m2ri.jp",                       # MM総研
    "bcnretail.com",
}

# ------------------------------------------------- 質問の出典(事実の根拠には不可)
# 実在するユーザー投稿であることが FAQ の前提。事実の裏付けには使わない。
QA = {
    "detail.chiebukuro.yahoo.co.jp",
    "bbs.kakaku.com",
    "oshiete.goo.ne.jp",
    "okwave.jp",
    "jp.quora.com",
    "note.com",
    "b.hatena.ne.jp",
}

# ------------------------------------------------------------ ブランド公式ドメイン
# slug → そのブランドの公式ドメイン。サブドメインは自動で許可される。
OFFICIAL = {
    "anker":       ("ankerjapan.com", "anker.com"),
    "balmuda":     ("balmuda.com",),
    "cio":         ("connectinternationalone.co.jp",),
    "dji":         ("dji.com",),
    "dyson":       ("dyson.co.jp", "dyson.com", "dysonrecall.com"),
    "ecovacs":     ("ecovacs.com", "ecovacs.co.jp"),
    "elecom":      ("elecom.co.jp", "elecom-shop.jp"),
    "gopro":       ("gopro.com",),
    "insta360":    ("insta360.com", "archisite.co.jp"),
    "irobot":      ("irobot-jp.com", "irobot.com"),
    "nature-remo": ("nature.global",),
    "roborock":    ("roborock.jp", "roborock.com"),
    "sharkninja":  ("shark.co.jp", "ninja.co.jp", "sharkninja.com", "sharkninja.jp"),
    "switchbot":   ("switchbot.jp", "switch-bot.com"),
    "ugreen":      ("ugreen.com",),
    "xiaomi":      ("mi.com", "xiaomi.com"),
}

# 今後の追加候補。既存ブランドの「日本での主な競合」に出ている先を先回りで登録して
# おく(新規ブランド追加時に毎回ここを直さなくて済むように)。
CANDIDATE = {
    "panasonic":   ("panasonic.jp", "panasonic.com"),
    "hitachi":     ("hitachi.co.jp", "kadenfan.hitachi.co.jp"),
    "sony":        ("sony.jp", "sony.co.jp"),
    "irisohyama":  ("irisohyama.co.jp", "irisplaza.co.jp"),
    "buffalo":     ("buffalo.jp",),
    "sanwa":       ("sanwa.co.jp",),
    "belkin":      ("belkin.com",),
    "aqara":       ("aqara.com",),
    "tplink":      ("tp-link.com",),
    "sesame":      ("candyhouse.co",),
    "ricoh-theta": ("theta360.com", "ricoh-imaging.co.jp"),
    "aladdin":     ("aladdin-aic.com",),
    "makita":      ("makita.co.jp",),
    "tfal":        ("t-fal.co.jp",),
    "recolte":     ("recolte-jp.com",),
}

# すべての公式ドメインの和集合。比較記事など、他ブランドの公式ページを
# 根拠に引くのは正当なので許可する。
ALL_OFFICIAL = {d for v in OFFICIAL.values() for d in v} | \
               {d for v in CANDIDATE.values() for d in v}

FACT_DOMAINS = GOV | DISCLOSURE | PRESS | MEDIA | RESEARCH | ALL_OFFICIAL


def _match(host, domains):
    return any(host == d or host.endswith("." + d) for d in domains)


def host(url):
    return urlparse(url or "").netloc.lower()


def host_ok(url, slug=None):
    """事実の出典として認められるか。slug を渡すと自ブランド公式を優先判定する。"""
    h = host(url)
    if not h:
        return False
    if slug and _match(h, OFFICIAL.get(slug, ())):
        return True
    # 掲示板は事実の根拠にはならない(kakaku.com は news./mag. のみ可)
    if h in QA or h.startswith("bbs."):
        return False
    return _match(h, FACT_DOMAINS)


def qa_ok(url):
    """質問(ユーザー投稿)の出典として認められるか。"""
    return host(url) in QA


def classify(url, slug=None):
    """監査用。出典がどの区分に当たるかを返す。"""
    h = host(url)
    if not h:
        return "empty"
    if slug and _match(h, OFFICIAL.get(slug, ())):
        return "official(self)"
    if h in QA or h.startswith("bbs."):
        return "qa"
    for name, domains in (("gov", GOV), ("disclosure", DISCLOSURE), ("press", PRESS),
                          ("research", RESEARCH), ("media", MEDIA),
                          ("official(other)", ALL_OFFICIAL)):
        if _match(h, domains):
            return name
    return "unlisted"
