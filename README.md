# 日本AI原生内容平台(jp)

按照《值得买科技-国际事业部-日本AI原生内容平台 说明书》实现的最小可运行版本(v0)。

**一个日语网站,没有App、没有Feed、没有账号体系。** 两类页面:品牌定位页 + 问答页,面向AI引用做结构化设计。

## 与说明书的对应关系

| 说明书模块 | 本仓库实现 |
|---|---|
| 品牌定位页(§5.1) | `data/brands/*.json` → `/brands/<slug>/`,含母公司、价位带、品类、渠道、日本法人(法人番号)、技適、召回、保修、日语客服9个字段,每条事实带出典与确认日 |
| 问答页(§5.1) | `data/qa/*.json` → `/qa/<slug>/`,标题即问题、首屏即答案、下方事实表格 |
| 页面结构(§5.2) | 无侧边栏、无推荐位、无登录入口 |
| AI引用结构化数据(§5.3) | 品牌页 Article + Brand JSON-LD;问答页 FAQPage JSON-LD;`llms.txt`、`sitemap.xml`、`robots.txt` 自动生成 |
| AI引用监测台(§5.1) | `monitor/` 内部脚本:固定日语query集,每日查询 ChatGPT/Perplexity/Gemini,记录是否被引用及被引用片段 |
| 索引率指标(§8) | 生成 sitemap.xml,可直接提交 GSC |

## 使用方法

### 构建站点

```bash
python3 build.py
```

无任何依赖。读取 `data/` 生成静态站到 `docs/`。已生成的 `docs/` 可直接用 GitHub Pages 发布(Settings → Pages → Deploy from branch → `/docs`)。

### 新增内容

- 新增品牌:在 `data/brands/` 加一个 JSON(参考 `anker.json` 的字段),重新构建。
- 新增问答:在 `data/qa/` 加一个 JSON(`question` / `answer` / `facts`),重新构建。
- 域名:在 `config.json` 里把 `base_url` 改为正式域名(当前为占位 `https://example.jp`)。

### AI引用监测

```bash
export OPENAI_API_KEY=...       # 可选
export PERPLEXITY_API_KEY=...   # 可选
export GEMINI_API_KEY=...       # 可选
python3 monitor/monitor.py
```

按 `monitor/queries.json` 的固定query集逐一提问,结果写入 `monitor/results/YYYY-MM-DD.jsonl`,并输出当日引用率(核心指标:AI引用率)。未设置key的provider自动跳过。上线后把 `queries.json` 中的 `site_domains` 改为正式域名,配合cron每日运行。

## 当前样例内容

- 品牌页 ×10:Anker、Xiaomi、SwitchBot、Roborock、DJI、Insta360(中国)/ BALMUDA、CIO(日本)/ SharkNinja(美国)/ Dyson(英国)
- 问答页 ×18:以调研确认的日本高频问题模式「〇〇はどこの国の会社?」为主,加安全性、修理、法规、品牌对比类问题
- 设计遵循日本Web惯例:パンくずリスト、最終確認日、目次、「結論」先行、よくある質問折叠区、国别徽章、高信息密度表格、運営方針页

⚠️ **样例内容未经日语母语审校,标注【要確認】的事实(法人番号、技適型号、保修期限等)需在一次来源(国税庁/総務省/消費者庁)逐条核实后方可上线。** 按说明书§6.1,所有对外内容需日语母语审校通过。

## 尚未实现(按说明书为后续阶段)

- 联盟转链(M4之后启用)
- 技適/召回的headless批量抓取管线
- 法人番号国税庁API自动查询
