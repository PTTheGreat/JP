from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(r"C:\Users\Administrator\Desktop\中级美语")
SCRIPT_DIR = ROOT / "PSD_layer_rename_SAFE_JSX_scripts_最终MD同步版"
MANIFEST = SCRIPT_DIR / "PSD_layer_rename_manifest.json"
SYNC_MD = SCRIPT_DIR / "Word内容自动排版到PSD_最终规则说明_图层名已同步.md"

OUT_JSX = Path(r"D:\Documents\New project\validate_intermediate_psd_layers_batch.jsx")
OUT_PS1 = Path(r"D:\Documents\New project\run_validate_intermediate_psd_layers_batch.ps1")
OUT_MERGED_LOCAL = Path(r"D:\Documents\New project\Word到PSD自动排版_执行版_图层验证后.md")

REPORT_JSON = ROOT / "PS内部图层验证报告.json"
REPORT_MD = ROOT / "PS内部图层验证报告.md"
MERGED_MD = ROOT / "Word到PSD自动排版_执行版_图层验证后.md"

PSD_MAP = {
    "3-4_1_FIRST_PAGE_template_renamed.psd": ROOT / "3-4 1.psd",
    "3-4_2_CONT_PAGE_template_renamed.psd": ROOT / "3-4 2.psd",
    "3-4_3_GRAMMAR_CONT_ref_renamed.psd": ROOT / "3-4 3.psd",
    "3-4_4_GRAMMAR_EXERCISE_ref_renamed.psd": ROOT / "3-4 4.psd",
    "3-4_5_EXERCISE_END_ref_renamed.psd": ROOT / "3-4 5.psd",
}


def js(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def build_jsx() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    jobs = []
    for manifest_name, psd_path in PSD_MAP.items():
        rows = manifest[manifest_name]
        expected = [row["new"] for row in rows]
        jobs.append(
            {
                "manifestName": manifest_name,
                "psdPath": str(psd_path).replace("\\", "/"),
                "expected": expected,
            }
        )

    jsx = f"""#target photoshop
app.displayDialogs = DialogModes.NO;
app.preferences.rulerUnits = Units.PIXELS;

var JOBS = {js(jobs)};
var REPORT_JSON = {js(str(REPORT_JSON).replace("\\", "/"))};
var REPORT_MD = {js(str(REPORT_MD).replace("\\", "/"))};

function collectLayerNames(container, out, duplicates, paths, prefix) {{
  for (var i = 0; i < container.layers.length; i++) {{
    var layer = container.layers[i];
    var path = prefix ? prefix + " > " + layer.name : layer.name;
    if (out[layer.name]) {{
      duplicates[layer.name] = (duplicates[layer.name] || 1) + 1;
    }} else {{
      out[layer.name] = true;
    }}
    paths[layer.name] = path;
    if (layer.typename == "LayerSet") {{
      collectLayerNames(layer, out, duplicates, paths, path);
    }}
  }}
}}

function quoteJsonString(value) {{
  var s = String(value);
  var out = "";
  for (var i = 0; i < s.length; i++) {{
    var code = s.charCodeAt(i);
    if (code == 92) out += String.fromCharCode(92, 92);
    else if (code == 34) out += String.fromCharCode(92, 34);
    else if (code == 13) out += String.fromCharCode(92) + "r";
    else if (code == 10) out += String.fromCharCode(92) + "n";
    else if (code == 9) out += String.fromCharCode(92) + "t";
    else out += s.charAt(i);
  }}
  return String.fromCharCode(34) + out + String.fromCharCode(34);
}}

function jsonStringify(value, indent) {{
  if (indent === undefined) indent = "";
  var nextIndent = indent + "  ";
  if (value === null) return "null";
  if (typeof value == "number" || typeof value == "boolean") return String(value);
  if (typeof value == "string") return quoteJsonString(value);
  if (value instanceof Array) {{
    if (value.length === 0) return "[]";
    var parts = [];
    for (var i = 0; i < value.length; i++) parts.push(nextIndent + jsonStringify(value[i], nextIndent));
    return "[\\n" + parts.join(",\\n") + "\\n" + indent + "]";
  }}
  var fields = [];
  for (var key in value) {{
    if (value.hasOwnProperty(key)) {{
      fields.push(nextIndent + quoteJsonString(key) + ": " + jsonStringify(value[key], nextIndent));
    }}
  }}
  if (fields.length === 0) return "{{}}";
  return "{{\\n" + fields.join(",\\n") + "\\n" + indent + "}}";
}}

function writeText(path, text) {{
  var f = new File(path);
  f.encoding = "UTF-8";
  f.open("w");
  f.write(text);
  f.close();
}}

function validateJob(job) {{
  var result = {{
    manifestName: job.manifestName,
    psdPath: job.psdPath,
    opened: false,
    expectedCount: job.expected.length,
    foundCount: 0,
    missingCount: 0,
    duplicateLayerNames: [],
    missing: [],
    error: null
  }};

  var doc = null;
  try {{
    doc = app.open(new File(job.psdPath));
    result.opened = true;
    result.documentName = doc.name;
    result.width = Number(doc.width.as("px"));
    result.height = Number(doc.height.as("px"));
    result.resolution = Number(doc.resolution);

    var names = {{}};
    var duplicates = {{}};
    var paths = {{}};
    collectLayerNames(doc, names, duplicates, paths, "");

    for (var d in duplicates) {{
      result.duplicateLayerNames.push({{ name: d, count: duplicates[d] }});
    }}

    for (var i = 0; i < job.expected.length; i++) {{
      var name = job.expected[i];
      if (names[name]) {{
        result.foundCount++;
      }} else {{
        result.missing.push(name);
      }}
    }}
    result.missingCount = result.missing.length;
  }} catch (e) {{
    result.error = String(e);
  }} finally {{
    if (doc) {{
      try {{ doc.close(SaveOptions.DONOTSAVECHANGES); }} catch (closeErr) {{}}
    }}
  }}
  return result;
}}

var report = {{
  generatedAt: new Date().toString(),
  root: {js(str(ROOT).replace("\\", "/"))},
  jobs: [],
  summary: {{
    totalExpected: 0,
    totalFound: 0,
    totalMissing: 0,
    filesOpened: 0,
    filesFailed: 0
  }}
}};

for (var j = 0; j < JOBS.length; j++) {{
  var r = validateJob(JOBS[j]);
  report.jobs.push(r);
  report.summary.totalExpected += r.expectedCount;
  report.summary.totalFound += r.foundCount;
  report.summary.totalMissing += r.missingCount;
  if (r.opened && !r.error) report.summary.filesOpened++;
  if (r.error) report.summary.filesFailed++;
}}

writeText(REPORT_JSON, jsonStringify(report, ""));

var md = [];
md.push("# PS 内部图层验证报告");
md.push("");
md.push("- 生成时间：" + report.generatedAt);
md.push("- 模板目录：" + report.root);
md.push("- 成功打开 PSD：" + report.summary.filesOpened + " / " + JOBS.length);
md.push("- 预期图层总数：" + report.summary.totalExpected);
md.push("- 找到图层总数：" + report.summary.totalFound);
md.push("- 缺失图层总数：" + report.summary.totalMissing);
md.push("");
for (var k = 0; k < report.jobs.length; k++) {{
  var item = report.jobs[k];
  md.push("## " + item.psdPath);
  md.push("");
  md.push("- manifest: `" + item.manifestName + "`");
  md.push("- 打开状态：" + (item.opened ? "成功" : "失败"));
  if (item.error) md.push("- 错误：" + item.error);
  md.push("- 预期 / 找到 / 缺失：" + item.expectedCount + " / " + item.foundCount + " / " + item.missingCount);
  md.push("- Photoshop 内重复图层名数量：" + item.duplicateLayerNames.length);
  if (item.missing.length > 0) {{
    md.push("");
    md.push("缺失图层：");
    for (var m = 0; m < item.missing.length; m++) md.push("- `" + item.missing[m] + "`");
  }}
  if (item.duplicateLayerNames.length > 0) {{
    md.push("");
    md.push("重复图层名：");
    for (var q = 0; q < item.duplicateLayerNames.length; q++) {{
      md.push("- `" + item.duplicateLayerNames[q].name + "` x " + item.duplicateLayerNames[q].count);
    }}
  }}
  md.push("");
}}
writeText(REPORT_MD, md.join("\\r\\n"));
"""
    OUT_JSX.write_text(jsx, encoding="utf-8")


def build_ps1() -> None:
    ps1 = f"""$ErrorActionPreference = 'Stop'

$photoshopCandidates = @(
  "D:\\software\\photoshop2024\\Adobe Photoshop 2024\\Photoshop.exe",
  "D:\\software\\photoshop2023\\Adobe Photoshop 2023\\Photoshop.exe"
)

$photoshopExe = $null
foreach ($candidate in $photoshopCandidates) {{
  if (Test-Path -LiteralPath $candidate) {{
    $photoshopExe = $candidate
    break
  }}
}}

if (-not $photoshopExe) {{
  throw "Photoshop not found in known paths."
}}

$jsxPath = "{str(OUT_JSX)}"

$existing = Get-Process | Where-Object {{ $_.ProcessName -like '*Photoshop*' }}
if ($existing) {{
  $existing | Stop-Process -Force
}}

Start-Process -FilePath $photoshopExe -WindowStyle Hidden
Start-Sleep -Seconds 20

$app = New-Object -ComObject Photoshop.Application
$app.DisplayDialogs = 3
$app.DoJavaScriptFile($jsxPath)

Get-Process | Where-Object {{ $_.ProcessName -like '*Photoshop*' }} | Stop-Process -Force
Write-Output "PS internal layer validation finished"
"""
    OUT_PS1.write_text(ps1, encoding="utf-8")


def build_merged_md() -> None:
    text = SYNC_MD.read_text(encoding="utf-8")
    text = text.replace("@HEADER_LESSON_NO", "@SHELL_TOP_LESSON_NO_TEXT")
    text = text.replace("@HEADER_LESSON_TITLE", "@SHELL_TOP_LESSON_TITLE_TEXT")
    text = text.replace("@HEADER_GREEN_BAR_BREAK", "@SHELL_TOP_BAR_BREAK_SHAPE")
    text = text.replace("@HEADER_GREEN_BAR", "@SHELL_TOP_BAR_MAIN_SHAPE")
    text = text.replace("@STYLE_GRAMMAR_LEAD_ORANGE_ITALIC", "@PART3_LEAD_ORANGE_ITALIC_TEXT")
    text = text.replace("@STYLE_DIALOGUE_M_RED", "@PART1_DIALOGUE_SAMPLE_LINE_TEXT")
    text = text.replace("@STYLE_ANSWER_LINE", "@PART4_EXERCISE_CONT_BODY_TEXT")
    text = text.replace(
        "语法内容按 Word 段落顺序排入。\n- 行距固定为 `24 px`。",
        "语法内容按 Word 段落顺序排入。\n- 行距必须复制 PSD 对应文本层的实测行距；MD 中出现的 `24 px` 只能作为早期估算，不得覆盖 PSD 实测样式。",
    )
    text = text.replace(
        "后续普通语法说明恢复为黑色正文，行距仍为 `24 px`。",
        "后续普通语法说明恢复为黑色正文，行距仍以 PSD 对应文本层实测值为准。",
    )
    appendix = f"""

---

## 20. 本次合并修正说明（2026-06-11）

本文件为执行版规则，合并依据如下：

- 以 `PSD_layer_rename_SAFE_JSX_scripts_最终MD同步版/Word内容自动排版到PSD_最终规则说明_图层名已同步.md` 为主规则。
- 桌面 `Word到PSD自动排版_Codex直接执行极简版_37Lesson批量版.md` 作为执行摘要，不作为最终图层名依据。
- 所有 Photoshop 自动排版脚本必须以第 6 节中的 `@SHELL_*`、`@PART*_*`、`@PAGE_*`、`@LESSON_*` 新图层名为准。
- 旧图层名或旧伪代码名不得再使用，包括 `@HEADER_LESSON_NO`、`@HEADER_LESSON_TITLE`、`@HEADER_GREEN_BAR`、`@STYLE_ROOT`。
- 所有字体、字号、颜色、行距、段落格式以 PSD 内部实测图层为准；MD 中的数字如果与 PSD 实测冲突，以 PSD 为准。

## 21. PS 内部验证要求

正式排版前必须先运行 Photoshop 内部图层验证：

```text
输入 PSD：
C:\\Users\\Administrator\\Desktop\\中级美语\\3-4 1.psd
C:\\Users\\Administrator\\Desktop\\中级美语\\3-4 2.psd
C:\\Users\\Administrator\\Desktop\\中级美语\\3-4 3.psd
C:\\Users\\Administrator\\Desktop\\中级美语\\3-4 4.psd
C:\\Users\\Administrator\\Desktop\\中级美语\\3-4 5.psd

输出报告：
C:\\Users\\Administrator\\Desktop\\中级美语\\PS内部图层验证报告.json
C:\\Users\\Administrator\\Desktop\\中级美语\\PS内部图层验证报告.md
```

验收标准：

- 5 个 PSD 都能由 Photoshop 打开。
- manifest 中 367 个模板图层名都能在对应 PSD 内找到。
- 缺失图层数必须为 0。
- 若 Photoshop 内存在重复图层名，应在正式排版脚本中使用父组路径或 manifest 类型辅助定位，避免误取同名层。

## 22. 当前文件核对结果

已通过静态核对：

- manifest 文件数：5
- manifest 图层映射总数：367
- 每个模板 manifest 内部无重复新图层名
- Word 可识别 Lesson 数量：37
- Word 可识别 Part 1 / Part 2 / Part 3 / Part 4 数量：均为 37

最终是否可执行，以 Photoshop 内部验证报告为准。
"""
    OUT_MERGED_LOCAL.write_text(text + appendix, encoding="utf-8")


def main() -> None:
    build_jsx()
    build_ps1()
    build_merged_md()
    print(OUT_JSX)
    print(OUT_PS1)
    print(OUT_MERGED_LOCAL)
    print(MERGED_MD)


if __name__ == "__main__":
    main()
