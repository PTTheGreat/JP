import json
from pathlib import Path


ROOT = Path(r"C:\Users\Administrator\Desktop\中级美语")
WORK = Path(r"D:\Documents\New project")
LESSONS_JSON = WORK / "intermediate_lessons.json"
PLAN_JSON = ROOT / "data" / "lesson_1_2_layout_plan.json"
OUT_JSX = WORK / "measure_lesson_1_2.jsx"
OUT_PS1 = WORK / "run_measure_lesson_1_2.ps1"


def grammar_lines(blocks):
    return [block.get("text", "").strip() for block in blocks if block.get("text", "").strip()]


def chunk_lines(lines, count):
    return "\r".join(lines[:count]), lines[count:]


def exercise_lines(sections):
    lines = []
    for section in sections:
        title = section.get("title", "")
        section_no = section.get("sectionNo", "")
        if title:
            lines.append(f"{section_no} {title}".strip())
        for item in section.get("items", []):
            text = (item.get("displayText") or item.get("text", "")).strip()
            if text:
                lines.append(text)
            if item.get("answerLines", 0):
                lines.append("____________________________________________")
    return lines


lesson = json.loads(LESSONS_JSON.read_text(encoding="utf-8"))["lessons"][0]
plan = json.loads(PLAN_JSON.read_text(encoding="utf-8"))
START_LESSON_INDEX = 0
END_LESSON_INDEX = 0
MAX_PAGES_PER_LESSON = 20

reading_lines = []
for item in lesson["part1"]["reading"]:
    if item.get("phonetic"):
        reading_lines.append({"kind": "phonetic", "text": item["phonetic"]})
    reading_lines.append({"kind": "body", "text": item["text"]})

dialogue_lines = []
for item in lesson["part1"]["dialogue"]:
    if item.get("phonetic"):
        dialogue_lines.append({"kind": "phonetic", "text": item["phonetic"]})
    speaker = item.get("speaker") or ""
    dialogue_lines.append({"kind": "dialogue", "speaker": speaker, "text": f"{speaker}: {item['text']}" if speaker else item["text"]})

grammar = grammar_lines(lesson["part3"]["blocks"])
grammar_slots = (grammar + [""] * 8)[:8]
grammar_overflow = grammar[8:]

part4 = exercise_lines(lesson["part4"]["sections"])
exercise_sections = lesson["part4"]["sections"]

data = {
    "lessonNo": lesson["lessonNo"],
    "lessonTitle": lesson["lessonTitle"],
    "readingLines": reading_lines,
    "readingLeft": "\r".join(line["text"] for line in reading_lines[:8]),
    "readingRight": "\r".join(line["text"] for line in reading_lines[8:]),
    "dialogueIntro": lesson["part1"]["dialogueIntro"],
    "dialogueRole": lesson["part1"]["dialogueRoleNote"],
    "dialogueLines": dialogue_lines,
    "dialogue": "\r".join(line["text"] for line in dialogue_lines),
    "grammarLead": lesson["part3"]["leadSentence"],
    "grammarP2A": grammar_slots[0],
    "grammarP2B": grammar_slots[1],
    "grammarP3A": grammar_slots[2],
    "grammarP3B": grammar_slots[3],
    "grammarP3C": grammar_slots[4],
    "grammarP3D": grammar_slots[5],
    "grammarP4A": grammar_slots[6],
    "grammarP4B": grammar_slots[7],
    "grammarOverflow": grammar_overflow,
    "exerciseSection1No": exercise_sections[0].get("sectionNo", "") if len(exercise_sections) > 0 else "",
    "exerciseSection2No": exercise_sections[1].get("sectionNo", "") if len(exercise_sections) > 1 else "",
    "exerciseP4A": "\r".join(part4[:8]),
    "exerciseP4B": "\r".join(part4[8:]),
}

jsx = f"""#target photoshop
app.displayDialogs = DialogModes.NO;

var ROOT = "C:/Users/Administrator/Desktop/中级美语";
var OUT = ROOT + "/output/lesson_1_2_measurement";
var START_LESSON_INDEX = {START_LESSON_INDEX};
var END_LESSON_INDEX = {END_LESSON_INDEX};
var MAX_PAGES_PER_LESSON = {MAX_PAGES_PER_LESSON};
var DATA = {json.dumps(data, ensure_ascii=False, indent=2)};
var PLAN = {json.dumps(plan, ensure_ascii=False, indent=2)};
var layerMap = {{}};

function ensureFolder(path) {{
  var folder = new Folder(path);
  if (!folder.exists) folder.create();
}}

function walkLayers(container, callback) {{
  for (var i = 0; i < container.layers.length; i++) {{
    var layer = container.layers[i];
    callback(layer);
    if (layer.typename === "LayerSet") walkLayers(layer, callback);
  }}
}}

function unlockLayer(layer) {{
  try {{ layer.allLocked = false; }} catch (e) {{}}
  try {{ layer.pixelsLocked = false; }} catch (e) {{}}
  try {{ layer.positionLocked = false; }} catch (e) {{}}
  try {{ layer.transparentPixelsLocked = false; }} catch (e) {{}}
}}

function unlockAll(doc) {{
  walkLayers(doc, function(layer) {{ unlockLayer(layer); }});
}}

function buildLayerMap(doc) {{
  layerMap = {{}};
  walkLayers(doc, function(layer) {{
    if (!layerMap[layer.name]) layerMap[layer.name] = layer;
  }});
}}

function findLayer(doc, name) {{
  return layerMap[name] || null;
}}

function px(v) {{
  try {{ return Math.round(v.as("px")); }} catch (e) {{ return null; }}
}}

function boundsOf(layer) {{
  if (!layer) return null;
  try {{
    return {{
      "left": px(layer.bounds[0]),
      "top": px(layer.bounds[1]),
      "right": px(layer.bounds[2]),
      "bottom": px(layer.bounds[3])
    }};
  }} catch (e) {{
    return null;
  }}
}}

function layerInfo(doc, name) {{
  var layer = findLayer(doc, name);
  if (!layer) return {{"name": name, "exists": false}};
  var text = null;
  try {{ if (layer.kind === LayerKind.TEXT) text = layer.textItem.contents; }} catch (e) {{}}
  return {{
    "name": name,
    "exists": true,
    "visible": layer.visible,
    "kind": layer.typename,
    "text": text,
    "bounds": boundsOf(layer)
  }};
}}

function setText(doc, name, value) {{
  var layer = findLayer(doc, name);
  if (!layer) return false;
  unlockLayer(layer);
  layer.visible = true;
  if (layer.kind === LayerKind.TEXT) {{
    doc.activeLayer = layer;
    layer.textItem.contents = value || "";
  }}
  return true;
}}

function setOptionalText(doc, name, value) {{
  if (!findLayer(doc, name)) return false;
  return setText(doc, name, value);
}}

function hideLayer(doc, name) {{
  var layer = findLayer(doc, name);
  if (layer) layer.visible = false;
}}

function pageSpec(pageNo) {{
  for (var i = 0; i < PLAN.pages.length; i++) {{
    if (PLAN.pages[i].pageIndex === pageNo) return PLAN.pages[i];
  }}
  throw new Error("Missing page spec " + pageNo);
}}

function findModule(pageSpec, moduleId) {{
  var modules = pageSpec.modules || [];
  for (var i = 0; i < modules.length; i++) {{
    if (modules[i].id === moduleId) return modules[i];
  }}
  return null;
}}

function applyHiddenLayers(doc, spec) {{
  var names = spec.hiddenLayers || [];
  for (var i = 0; i < names.length; i++) hideLayer(doc, names[i]);
}}

function setHeader(doc) {{
  setText(doc, "@SHELL_TOP_LESSON_NO_TEXT", DATA.lessonNo);
  setText(doc, "@SHELL_TOP_LESSON_TITLE_TEXT", DATA.lessonTitle);
  setOptionalText(doc, "@LESSON_NO_COVER_TEXT", DATA.lessonNo);
  setOptionalText(doc, "@LESSON_TITLE_COVER_TEXT", DATA.lessonTitle);
}}

function setPageNo(doc, spec) {{
  setText(doc, "@PAGE_NO_LEFT_TEXT", spec.pageNumbers[0]);
  setText(doc, "@PAGE_NO_RIGHT_TEXT", spec.pageNumbers[1]);
}}

function hidePart3Subtitle(doc, no) {{
  var id = no < 10 ? "0" + no : "" + no;
  hideLayer(doc, "@PART3_SUBTITLE_" + id + "_GROUP");
}}

function hideAllPart3Subtitles(doc) {{
  for (var i = 1; i <= 12; i++) hidePart3Subtitle(doc, i);
}}

function applyPart3SubtitlePolicy(doc, spec) {{
  if (PLAN.rules.part3NoFakeSubtitles) hideAllPart3Subtitles(doc);
}}

function setVocabRowFromPlan(doc, rowSpec, item) {{
  var rowNo = rowSpec.rowNo;
  var prefix = "@PART2_VOCAB_ROW_" + (rowNo < 10 ? "0" + rowNo : rowNo);
  if (!item) {{
    hideLayer(doc, prefix + "_GROUP");
    setText(doc, prefix + "_NO_TEXT", "");
    setText(doc, prefix + "_WORD_TEXT", "");
    setText(doc, prefix + "_PHONETIC_TEXT", "");
    setText(doc, prefix + "_MEANING_TEXT", "");
    return;
  }}
  setText(doc, prefix + "_NO_TEXT", item.no);
  setText(doc, prefix + "_WORD_TEXT", item.word);
  setText(doc, prefix + "_PHONETIC_TEXT", (item.kk || "") + (item.kk && item.ipa ? "\\r" : "") + (item.ipa || ""));
  setText(doc, prefix + "_MEANING_TEXT", item.meaning);
}}

function applyVocabModule(doc, spec, moduleId) {{
  var module = findModule(spec, moduleId);
  if (!module) return;
  var rows = module.rows || [];
  var items = module.items || [];
  for (var i = 0; i < rows.length; i++) setVocabRowFromPlan(doc, rows[i], items[i]);
}}

function applyPart1Module(doc) {{
  setText(doc, "@PART1_READING_LEFT_TEXT_STYLE_SOURCE", DATA.readingLeft);
  setText(doc, "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE", DATA.readingRight);
  setText(doc, "@PART1_DIALOGUE_INTRO_TEXT", DATA.dialogueIntro);
  setText(doc, "@PART1_DIALOGUE_ROLE_MAP_TEXT", DATA.dialogueRole);
  setText(doc, "@PART1_DIALOGUE_SAMPLE_LINE_TEXT", DATA.dialogue);
}}

function writePageContent(doc, spec) {{
  if (spec.pageIndex === 1) {{
    applyPart1Module(doc);
    applyVocabModule(doc, spec, "part2_rows_01_08");
  }} else if (spec.pageIndex === 2) {{
    applyVocabModule(doc, spec, "part2_rows_09_21");
    setText(doc, "@PART3_LEAD_ORANGE_ITALIC_TEXT", DATA.grammarLead);
    setText(doc, "@PART3_BODY_TEXT_BLOCK_02", DATA.grammarP2A);
    setText(doc, "@PART3_BODY_TEXT_BLOCK_03", DATA.grammarP2B);
  }} else if (spec.pageIndex === 3) {{
    setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT_01", DATA.grammarP3A);
    setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT_02", DATA.grammarP3B);
    setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT_03", DATA.grammarP3C);
    setText(doc, "@PART3_CONT_TEXT_BLOCK_RIGHT_01", DATA.grammarP3D);
    setText(doc, "@PART3_CONT_TEXT_BLOCK_RIGHT_02", "");
  }} else if (spec.pageIndex === 4) {{
    setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT", DATA.grammarP4A);
    setText(doc, "@PART3_CONT_TEXT_BLOCK_RIGHT_TOP", DATA.grammarP4B);
    setText(doc, "@PART4_EXERCISE_Q1_NO_TEXT", DATA.exerciseSection1No);
    setText(doc, "@PART4_EXERCISE_Q1_BODY_TEXT", DATA.exerciseP4A);
    setText(doc, "@PART4_EXERCISE_Q2_NO_TEXT", DATA.exerciseSection2No);
    setText(doc, "@PART4_EXERCISE_Q2_BODY_TEXT", "");
  }} else if (spec.pageIndex === 5) {{
    setText(doc, "@PART4_EXERCISE_CONT_BODY_TEXT", DATA.exerciseP4B);
  }}
}}

function measureVocab(doc, spec) {{
  var result = [];
  for (var m = 0; m < (spec.modules || []).length; m++) {{
    var module = spec.modules[m];
    if (module.type !== "vocabularyFixedRows") continue;
    var rows = module.rows || [];
    var items = module.items || [];
    for (var i = 0; i < rows.length; i++) {{
      var rowNo = rows[i].rowNo;
      var prefix = "@PART2_VOCAB_ROW_" + (rowNo < 10 ? "0" + rowNo : rowNo);
      result.push({{
        "rowNo": rowNo,
        "hasItem": !!items[i],
        "group": layerInfo(doc, prefix + "_GROUP"),
        "no": layerInfo(doc, prefix + "_NO_TEXT"),
        "word": layerInfo(doc, prefix + "_WORD_TEXT"),
        "phonetic": layerInfo(doc, prefix + "_PHONETIC_TEXT"),
        "meaning": layerInfo(doc, prefix + "_MEANING_TEXT"),
        "policy": {{
          "fixedHeight": rows[i].fixedHeight,
          "overflow": module.overflowPolicy
        }}
      }});
    }}
  }}
  return result;
}}

function measureHiddenReferenceLayers(doc, spec) {{
  var result = [];
  var names = spec.hiddenLayers || [];
  for (var i = 0; i < names.length; i++) {{
    result.push(layerInfo(doc, names[i]));
  }}
  return result;
}}

function measurePage(doc, spec) {{
  return {{
    "pageIndex": spec.pageIndex,
    "template": spec.template,
    "pageNumbers": {{
      "left": layerInfo(doc, "@PAGE_NO_LEFT_TEXT"),
      "right": layerInfo(doc, "@PAGE_NO_RIGHT_TEXT")
    }},
    "hiddenReferenceLayers": measureHiddenReferenceLayers(doc, spec),
    "part1": spec.pageIndex === 1 ? {{
      "readingLeft": layerInfo(doc, "@PART1_READING_LEFT_TEXT_STYLE_SOURCE"),
      "readingRight": layerInfo(doc, "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE"),
      "dialogueIntro": layerInfo(doc, "@PART1_DIALOGUE_INTRO_TEXT"),
      "dialogueRole": layerInfo(doc, "@PART1_DIALOGUE_ROLE_MAP_TEXT"),
      "dialogue": layerInfo(doc, "@PART1_DIALOGUE_SAMPLE_LINE_TEXT"),
      "measurementNeeded": [
        "reading green border bottom resize",
        "dialogue yellow box bottom resize",
        "dialogue green vertical line resize",
        "dialogue right-to-left-page overflow"
      ]
    }} : null,
    "part2": measureVocab(doc, spec),
    "part3SubtitleGroups": [
      layerInfo(doc, "@PART3_SUBTITLE_01_GROUP"),
      layerInfo(doc, "@PART3_SUBTITLE_02_GROUP"),
      layerInfo(doc, "@PART3_SUBTITLE_03_GROUP"),
      layerInfo(doc, "@PART3_SUBTITLE_04_GROUP"),
      layerInfo(doc, "@PART3_SUBTITLE_05_GROUP")
    ]
  }};
}}

function cleanText(value) {{
  if (value === null || value === undefined) return "";
  var s = String(value);
  s = s.replace(/\\r/g, "\\\\r").replace(/\\n/g, "\\\\n").replace(/\\t/g, " ");
  if (s.length > 120) s = s.substring(0, 120) + "...";
  return s;
}}

function boundsText(bounds) {{
  if (!bounds) return "";
  return [bounds.left, bounds.top, bounds.right, bounds.bottom].join(",");
}}

function writeLayerLine(file, pageIndex, category, info) {{
  file.writeln([
    pageIndex,
    category,
    info.name || "",
    info.exists ? "exists" : "missing",
    info.visible ? "visible" : "hidden",
    boundsText(info.bounds),
    cleanText(info.text)
  ].join("\\t"));
}}

function writePageTrace(file, doc, spec) {{
  file.writeln("PAGE\\t" + spec.pageIndex + "\\t" + spec.template + "\\t" + spec.pageNumbers[0] + "/" + spec.pageNumbers[1]);
  writeLayerLine(file, spec.pageIndex, "pageNoLeft", layerInfo(doc, "@PAGE_NO_LEFT_TEXT"));
  writeLayerLine(file, spec.pageIndex, "pageNoRight", layerInfo(doc, "@PAGE_NO_RIGHT_TEXT"));
  var hidden = measureHiddenReferenceLayers(doc, spec);
  for (var i = 0; i < hidden.length; i++) writeLayerLine(file, spec.pageIndex, "hiddenReference", hidden[i]);
  for (var s = 1; s <= 5; s++) {{
    var id = s < 10 ? "0" + s : "" + s;
    writeLayerLine(file, spec.pageIndex, "part3Subtitle", layerInfo(doc, "@PART3_SUBTITLE_" + id + "_GROUP"));
  }}
  if (spec.pageIndex === 1) {{
    writeLayerLine(file, spec.pageIndex, "part1ReadingLeft", layerInfo(doc, "@PART1_READING_LEFT_TEXT_STYLE_SOURCE"));
    writeLayerLine(file, spec.pageIndex, "part1ReadingRight", layerInfo(doc, "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE"));
    writeLayerLine(file, spec.pageIndex, "part1DialogueIntro", layerInfo(doc, "@PART1_DIALOGUE_INTRO_TEXT"));
    writeLayerLine(file, spec.pageIndex, "part1DialogueRole", layerInfo(doc, "@PART1_DIALOGUE_ROLE_MAP_TEXT"));
    writeLayerLine(file, spec.pageIndex, "part1Dialogue", layerInfo(doc, "@PART1_DIALOGUE_SAMPLE_LINE_TEXT"));
    file.writeln("MEASURE_REQUIRED\\t1\\tpart1\\treading green border bottom resize");
    file.writeln("MEASURE_REQUIRED\\t1\\tpart1\\tdialogue yellow box bottom resize");
    file.writeln("MEASURE_REQUIRED\\t1\\tpart1\\tdialogue green vertical line resize");
    file.writeln("MEASURE_REQUIRED\\t1\\tpart1\\tdialogue right-to-left-page overflow");
  }}
  var vocab = measureVocab(doc, spec);
  for (var v = 0; v < vocab.length; v++) {{
    file.writeln("VOCAB_ROW\\t" + spec.pageIndex + "\\t" + vocab[v].rowNo + "\\t" + (vocab[v].hasItem ? "item" : "empty") + "\\t" + vocab[v].policy.fixedHeight + "\\t" + vocab[v].policy.overflow);
    writeLayerLine(file, spec.pageIndex, "vocabGroup", vocab[v].group);
    writeLayerLine(file, spec.pageIndex, "vocabNo", vocab[v].no);
    writeLayerLine(file, spec.pageIndex, "vocabWord", vocab[v].word);
    writeLayerLine(file, spec.pageIndex, "vocabPhonetic", vocab[v].phonetic);
    writeLayerLine(file, spec.pageIndex, "vocabMeaning", vocab[v].meaning);
  }}
}}

function main() {{
  ensureFolder(ROOT + "/output");
  ensureFolder(OUT);
  if (PLAN.pages.length > MAX_PAGES_PER_LESSON) throw new Error("Plan pages exceed MAX_PAGES_PER_LESSON: " + PLAN.pages.length);
  var traceFile = new File(OUT + "/ps_measure_trace.tsv");
  traceFile.encoding = "UTF-8";
  traceFile.open("w");
  traceFile.writeln("STATUS\\tmeasurementOnlyNoPSDOutput");
  traceFile.writeln("LESSON\\t" + DATA.lessonNo + "\\t" + DATA.lessonTitle);
  traceFile.writeln("LESSON_RANGE\\t" + START_LESSON_INDEX + "\\t" + END_LESSON_INDEX);
  traceFile.writeln("RULE\\tpreserveHiddenTemplateLayers\\t" + PLAN.rules.preserveHiddenTemplateLayers);
  traceFile.writeln("RULE\\tvocabRowHeight\\t" + PLAN.rules.vocabRowHeight);
  traceFile.writeln("RULE\\tpart3NoFakeSubtitles\\t" + PLAN.rules.part3NoFakeSubtitles);
  for (var i = 0; i < PLAN.pages.length; i++) {{
    var spec = PLAN.pages[i];
    if (spec.pageIndex > MAX_PAGES_PER_LESSON) throw new Error("MAX_PAGES_PER_LESSON exceeded: " + spec.pageIndex);
    var doc = app.open(new File(ROOT + "/" + spec.template));
    buildLayerMap(doc);
    unlockAll(doc);
    applyHiddenLayers(doc, spec);
    applyPart3SubtitlePolicy(doc, spec);
    setHeader(doc);
    setPageNo(doc, spec);
    writePageContent(doc, spec);
    writePageTrace(traceFile, doc, spec);
    doc.close(SaveOptions.DONOTSAVECHANGES);
  }}
  traceFile.close();
}}

main();
"""

ps1 = r"""$ErrorActionPreference = 'Stop'

$photoshopCandidates = @(
  "D:\software\photoshop2024\Adobe Photoshop 2024\Photoshop.exe",
  "D:\software\photoshop2023\Adobe Photoshop 2023\Photoshop.exe"
)

$photoshopExe = $null
foreach ($candidate in $photoshopCandidates) {
  if (Test-Path -LiteralPath $candidate) {
    $photoshopExe = $candidate
    break
  }
}

if (-not $photoshopExe) {
  throw "Photoshop not found in known paths."
}

$jsxPath = Join-Path $PSScriptRoot "measure_lesson_1_2.jsx"

$existing = Get-Process | Where-Object { $_.ProcessName -like '*Photoshop*' }
if ($existing) {
  $existing | Stop-Process -Force
}

Start-Process -FilePath $photoshopExe -WindowStyle Hidden
Start-Sleep -Seconds 20

$app = New-Object -ComObject Photoshop.Application
$app.DisplayDialogs = 3
$app.DoJavaScriptFile($jsxPath)

Get-Process | Where-Object { $_.ProcessName -like '*Photoshop*' } | Stop-Process -Force
Write-Output "Lesson 1-2 measurement finished"
"""

OUT_JSX.write_text(jsx, encoding="utf-8-sig")
OUT_PS1.write_text(ps1, encoding="utf-8")
print(OUT_JSX)
print(OUT_PS1)
