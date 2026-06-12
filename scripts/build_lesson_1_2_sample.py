import json
import re
from pathlib import Path


ROOT = Path(r"C:\Users\Administrator\Desktop\中级美语")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROBES_DIR = PROJECT_ROOT / "probes"
PHOTOSHOP_DIR = PROJECT_ROOT / "photoshop"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
LESSONS_JSON = DATA_DIR / "intermediate_lessons.json"
PLAN_JSON = DATA_DIR / "lesson_1_2_layout_plan.json"
OUT_JSX = PHOTOSHOP_DIR / "render_lesson_1_2_sample.jsx"
OUT_PS1 = SCRIPTS_DIR / "run_render_lesson_1_2_sample.ps1"
DIALOGUE_METRICS_JSON = PROBES_DIR / "probe_psd_dialogue_metrics.json"
PHONETIC_METRICS_JSON = PROBES_DIR / "probe_psd_phonetic_metrics.json"
READING_LAYERS_JSON = PROBES_DIR / "probe_psd_reading_layers.json"
READING_PARAGRAPH_STYLE_JSON = PROBES_DIR / "probe_psd_reading_paragraph_style.json"


def js_string(value):
    text = "" if value is None else str(value)
    return json.dumps(text, ensure_ascii=False)


def chunk_lines(lines, count):
    return "\r".join(lines[:count]), lines[count:]


def grammar_lines(blocks):
    lines = []
    for block in blocks:
        text = block.get("text", "").strip()
        if text:
            lines.append(text)
    return lines


def exercise_lines(sections):
    lines = []
    for section in sections:
        title = section.get("title", "")
        section_no = section.get("sectionNo", "")
        if title:
            lines.append(f"{section_no} {title}".strip())
        for item in section.get("items", []):
            text = item.get("displayText") or item.get("text", "")
            text = text.strip()
            if not text:
                continue
            lines.append(text)
            if item.get("answerLines", 0):
                lines.append("____________________________________________")
    return lines


def vocab_payload(item):
    phonetic = "\r".join(part for part in [item.get("kk", ""), item.get("ipa", "")] if part)
    return {
        "no": item.get("no", ""),
        "word": item.get("word", ""),
        "phonetic": phonetic,
        "meaning": item.get("meaning", ""),
    }


def normalize_lookup(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def phonetic_chunks(text):
    return [m.group(0).strip() for m in re.finditer(r"\[[^\]]+\]", text or "")]


def phonetic_key(text):
    return re.sub(r"[\s\[\]ː:']", "", (text or "").replace("KK", "").replace("IPA", "").lower())


def loose_phonetic_key(text):
    return phonetic_key(text).replace("z", "")


def candidate_surfaces(word):
    base = (word or "").replace("+动词原形", "").strip()
    surfaces = [base]
    if base.endswith("y"):
        surfaces.append(base[:-1] + "ies")
    surfaces.append(base + "s")
    surfaces.append(base + "ed")
    if base == "depend on":
        surfaces.append("depends on")
    if base == "tip":
        surfaces.append("tips")
    return [s for s in surfaces if s]


def find_surface_in_text(word, text):
    haystack = text or ""
    for surface in candidate_surfaces(word):
        pattern = r"(?<![A-Za-z])" + re.escape(surface).replace(r"\ ", r"\s+") + r"(?![A-Za-z])"
        m = re.search(pattern, haystack, flags=re.IGNORECASE)
        if m:
            return haystack[m.start():m.end()]
    return ""


def reading_blocks_with_targets(reading_items, vocab_items):
    blocks = []
    for item in reading_items:
        body = item.get("text", "").strip()
        segments = []
        for chunk in phonetic_chunks(item.get("phonetic", "")):
            key = phonetic_key(chunk)
            target = ""
            vocab_word = ""
            for vocab_item in vocab_items:
                kk_key = phonetic_key(vocab_item.get("kk", ""))
                ipa_key = phonetic_key(vocab_item.get("ipa", ""))
                loose_key = loose_phonetic_key(chunk)
                loose_kk = loose_phonetic_key(vocab_item.get("kk", ""))
                loose_ipa = loose_phonetic_key(vocab_item.get("ipa", ""))
                if key and (key in kk_key or key in ipa_key or kk_key in key or ipa_key in key or
                            loose_key in loose_kk or loose_key in loose_ipa or loose_kk in loose_key or loose_ipa in loose_key):
                    surface = find_surface_in_text(vocab_item.get("word", ""), body)
                    if surface:
                        target = surface
                        vocab_word = vocab_item.get("word", "")
                        break
            segments.append({
                "text": chunk,
                "target": target,
                "vocabWord": vocab_word,
            })
        blocks.append({
            "phonetic": item.get("phonetic", "").strip(),
            "text": body,
            "segments": segments,
        })
    return blocks


def load_metric_rows(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing PSD metric probe output: {path}")
    return {row["name"]: row for row in json.loads(path.read_text(encoding="utf-8-sig"))}


def load_json(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing PSD probe output: {path}")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def bounds_width(row):
    b = row["bounds"]
    return b[2] - b[0]


def bounds_height(row):
    b = row["bounds"]
    return b[3] - b[1]


dialogue_metric_rows = load_metric_rows(DIALOGUE_METRICS_JSON)
phonetic_metric_rows = load_metric_rows(PHONETIC_METRICS_JSON)
reading_layer_rows = load_metric_rows(READING_LAYERS_JSON)
reading_paragraph_rows = load_json(READING_PARAGRAPH_STYLE_JSON)
sample_line = dialogue_metric_rows["@PART1_DIALOGUE_SAMPLE_LINE_TEXT"]
dialogue_text_source = reading_layer_rows["@PART1_READING_RIGHT_TEXT_STYLE_SOURCE"]
role_m = dialogue_metric_rows["@MEASURE_DIALOGUE_ROLE_M"]
role_d = dialogue_metric_rows["@MEASURE_DIALOGUE_ROLE_D"]
m_no_space_a = dialogue_metric_rows["@MEASURE_DIALOGUE_M_NO_SPACE_A"]
m_space_a = dialogue_metric_rows["@MEASURE_DIALOGUE_M_SPACE_A"]
phonetic_body_pair = phonetic_metric_rows["@MEASURE_PHONETIC_BODY_PAIR"]
body_only = phonetic_metric_rows["@MEASURE_BODY_ONLY"]
dialogue_metrics = {
    "source": {
        "dialogue": str(DIALOGUE_METRICS_JSON),
        "phonetic": str(PHONETIC_METRICS_JSON),
        "dialogueTextSource": "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE",
    },
    "roleX": dialogue_text_source["bounds"][0],
    "lineTop": dialogue_text_source["bounds"][1] + dialogue_text_source["leading"],
    "lineGap": dialogue_text_source["leading"],
    "roleWidths": {
        "M:": bounds_width(role_m),
        "D:": bounds_width(role_d),
    },
    "roleSpaceWidth": bounds_width(m_space_a) - bounds_width(m_no_space_a),
    "textMaxRight": dialogue_text_source["bounds"][2],
    "continuationIndentX": dialogue_text_source["bounds"][0] + bounds_width(role_m) + (bounds_width(m_space_a) - bounds_width(m_no_space_a)),
    "lineBgBottom": dialogue_text_source["bounds"][3],
    "phoneticOffset": bounds_height(phonetic_body_pair) - bounds_height(body_only),
}
reading_left_source = reading_layer_rows["@PART1_READING_LEFT_TEXT_STYLE_SOURCE"]
reading_paragraph_style = next(row for row in reading_paragraph_rows if row["name"] == "@PART1_READING_LEFT_TEXT_STYLE_SOURCE")
reading_first_line_indent = next(
    (
        float(r["firstLineIndent"])
        for r in reading_paragraph_style.get("ranges", [])
        if r.get("firstLineIndent") and re.search(r"[A-Za-z]", r.get("text", "")) and "[" not in r.get("text", "")
    ),
    0.0,
)
reading_metrics = {
    "source": {
        "readingLayers": str(READING_LAYERS_JSON),
        "textStyleRanges": str(PROBES_DIR / "probe_psd_text_style_ranges.json"),
        "paragraphStyle": str(READING_PARAGRAPH_STYLE_JSON),
    },
    "textX": reading_left_source["bounds"][0],
    "textTop": reading_left_source["bounds"][1],
    "maxRight": reading_left_source["bounds"][2],
    "lineGap": reading_left_source["leading"],
    "bodyFirstLineIndent": reading_first_line_indent,
    "bodyContinuationIndent": 0,
    "blockLineCount": 3,
    "phoneticStyleSource": "@PART1_READING_LEFT_TEXT_STYLE_SOURCE",
    "bodyStyleSource": "@PART1_DIALOGUE_INTRO_TEXT",
}


lesson = json.loads(LESSONS_JSON.read_text(encoding="utf-8"))["lessons"][0]
layout_plan = json.loads(PLAN_JSON.read_text(encoding="utf-8"))
START_LESSON_INDEX = 0
END_LESSON_INDEX = 0
MAX_PAGES_PER_LESSON = 20
RENDER_FIRST_PAGE_ONLY = True
reading_lines = []
for item in lesson["part1"]["reading"]:
    phonetic = item.get("phonetic", "").strip()
    text = item.get("text", "").strip()
    if phonetic:
        reading_lines.append({"kind": "phonetic", "text": phonetic})
    reading_lines.append({"kind": "body", "text": text})
reading_blocks = reading_blocks_with_targets(lesson["part1"]["reading"], lesson["part2"]["items"])

dialogue_lines = []
for item in lesson["part1"]["dialogue"]:
    phonetic = item.get("phonetic", "").strip()
    speaker = item.get("speaker", "").strip()
    text = item.get("text", "").strip()
    if phonetic:
        dialogue_lines.append({"kind": "phonetic", "text": phonetic})
    dialogue_lines.append({"kind": "dialogue", "speaker": speaker, "text": f"{speaker}: {text}" if speaker else text})

vocab = [vocab_payload(item) for item in lesson["part2"]["items"]]
grammar = grammar_lines(lesson["part3"]["blocks"])
part4 = exercise_lines(lesson["part4"]["sections"])

grammar_slots = (grammar + [""] * 8)[:8]
grammar_overflow = grammar[8:]

exercise_p4_a = "\r".join(part4[:8])
exercise_p4_b = "\r".join(part4[8:])
exercise_sections = lesson["part4"]["sections"]

data = {
    "lessonNo": lesson["lessonNo"],
    "lessonTitle": lesson["lessonTitle"],
    "part1Title": "PART 1    Reading&Dialogue",
    "part2Title": "PART 2    Vocabulary&Idioms",
    "part3Title": "PART 3    Grammar points",
    "part4Title": "PART 4    Exercise",
    "readingLines": reading_lines,
    "readingBlocks": reading_blocks,
    "readingLeft": "\r".join(line["text"] for line in reading_lines[:8]),
    "readingRight": "\r".join(line["text"] for line in reading_lines[8:]),
    "readingMetrics": reading_metrics,
    "dialogueIntro": lesson["part1"]["dialogueIntro"],
    "dialogueRole": lesson["part1"]["dialogueRoleNote"],
    "dialogueLines": dialogue_lines,
    "dialogue": "\r".join(line["text"] for line in dialogue_lines),
    "dialogueMetrics": dialogue_metrics,
    "vocab": vocab,
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
    "exerciseP4A": exercise_p4_a,
    "exerciseP4B": exercise_p4_b,
}

jsx = f"""#target photoshop
app.displayDialogs = DialogModes.NO;

var ROOT = "C:/Users/Administrator/Desktop/中级美语";
var OUT = ROOT + "/output/lesson_1_2_sample";
var START_LESSON_INDEX = {START_LESSON_INDEX};
var END_LESSON_INDEX = {END_LESSON_INDEX};
var MAX_PAGES_PER_LESSON = {MAX_PAGES_PER_LESSON};
var RENDER_FIRST_PAGE_ONLY = {str(RENDER_FIRST_PAGE_ONLY).lower()};
var DATA = {json.dumps(data, ensure_ascii=False, indent=2)};
var PLAN = {json.dumps(layout_plan, ensure_ascii=False, indent=2)};
var layerMap = {{}};
var logFile = null;

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

var TRACE = [];

function openLog() {{
  logFile = new File(OUT + "/layout_log.txt");
  logFile.encoding = "UTF-8";
  logFile.open("w");
  log("START lessonIndex=" + START_LESSON_INDEX + "-" + END_LESSON_INDEX + " lesson=" + DATA.lessonNo);
}}

function log(message) {{
  if (logFile) logFile.writeln(new Date().toISOString ? new Date().toISOString() + "\\t" + message : message);
}}

function closeLog() {{
  if (logFile) {{
    log("END");
    logFile.close();
    logFile = null;
  }}
}}

function unlockLayer(layer) {{
  try {{ layer.allLocked = false; }} catch (e) {{}}
  try {{ layer.pixelsLocked = false; }} catch (e) {{}}
  try {{ layer.positionLocked = false; }} catch (e) {{}}
  try {{ layer.transparentPixelsLocked = false; }} catch (e) {{}}
}}

function unlockAll(doc) {{
  walkLayers(doc, function(layer) {{
    unlockLayer(layer);
  }});
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

function setText(doc, name, value) {{
  var layer = findLayer(doc, name);
  if (!layer) {{
    TRACE.push("MISSING " + name);
    log("MISSING_LAYER " + name);
    return false;
  }}
  layer.visible = true;
  unlockLayer(layer);
  if (layer.kind === LayerKind.TEXT) {{
    try {{
      doc.activeLayer = layer;
      layer.textItem.contents = value || "";
      log("SET_TEXT " + name);
    }} catch (e) {{
      TRACE.push("SET_TEXT_FAILED " + name + " :: " + e.message);
      log("SET_TEXT_FAILED " + name + " :: " + e.message);
      return false;
    }}
  }}
  return true;
}}

function moveLayerTopLeft(layer, targetLeft, targetTop) {{
  if (!layer) return;
  try {{
    var b = layer.bounds;
    var left = b[0].as("px");
    var top = b[1].as("px");
    layer.translate(UnitValue(targetLeft - left, "px"), UnitValue(targetTop - top, "px"));
  }} catch (e) {{
    TRACE.push("MOVE_FAILED " + layer.name + " :: " + e.message);
  }}
}}

function bringLayerToDocumentTop(doc, layer) {{
  if (!layer || doc.layers.length < 1) return;
  try {{
    layer.move(doc.layers[0], ElementPlacement.PLACEBEFORE);
  }} catch (e) {{
    TRACE.push("BRING_TO_TOP_FAILED " + layer.name + " :: " + e.message);
  }}
}}

function requireStyleSource(doc, sourceName) {{
  var source = findLayer(doc, sourceName);
  if (!source) {{
    TRACE.push("MISSING_STYLE_SOURCE " + sourceName);
    log("MISSING_STYLE_SOURCE " + sourceName);
    throw new Error("Missing PSD style source: " + sourceName);
  }}
  if (source.kind !== LayerKind.TEXT) {{
    TRACE.push("INVALID_STYLE_SOURCE " + sourceName);
    log("INVALID_STYLE_SOURCE " + sourceName);
    throw new Error("PSD style source is not a text layer: " + sourceName);
  }}
  return source;
}}

function duplicateTextLayer(doc, sourceName, newName, text, targetLeft, targetTop) {{
  var source = requireStyleSource(doc, sourceName);
  var layer = source.duplicate();
  layer.name = newName;
  unlockLayer(layer);
  layer.visible = true;
  if (layer.kind === LayerKind.TEXT) {{
    doc.activeLayer = layer;
    layer.textItem.contents = text || "";
  }}
  moveLayerTopLeft(layer, targetLeft, targetTop);
  bringLayerToDocumentTop(doc, layer);
  layerMap[newName] = layer;
  log("CREATE_TEXT " + newName + " styleSource=" + sourceName);
  return layer;
}}

function measureTextRight(doc, sourceName, text, targetLeft, targetTop) {{
  var layer = duplicateTextLayer(doc, sourceName, "@RUN_MEASURE_TEXT_TMP", text, targetLeft, targetTop);
  if (!layer) return targetLeft;
  var right = targetLeft;
  try {{
    var b = layer.bounds;
    right = b[2].as("px");
  }} catch (e) {{
    TRACE.push("MEASURE_TEXT_RIGHT_FAILED :: " + e.message);
  }}
  try {{ layer.remove(); }} catch (e2) {{}}
  layerMap["@RUN_MEASURE_TEXT_TMP"] = null;
  return right;
}}

function splitTextByMeasuredRight(doc, sourceName, text, targetLeft, targetTop, maxRight) {{
  var words = (text || "").split(/\\s+/);
  var lines = [];
  var current = "";
  for (var i = 0; i < words.length; i++) {{
    if (!words[i]) continue;
    var candidate = current ? current + " " + words[i] : words[i];
    if (current && measureTextRight(doc, sourceName, candidate, targetLeft, targetTop) > maxRight) {{
      lines.push(current);
      current = words[i];
    }} else {{
      current = candidate;
    }}
  }}
  if (current) lines.push(current);
  return lines;
}}

function applyFontFromStyleSource(doc, targetName, sourceName) {{
  var target = findLayer(doc, targetName);
  var source = requireStyleSource(doc, sourceName);
  if (!target || target.kind !== LayerKind.TEXT) {{
    TRACE.push("MISSING_TEXT_FOR_STYLE " + targetName);
    log("MISSING_TEXT_FOR_STYLE " + targetName);
    return false;
  }}
  try {{
    target.textItem.font = source.textItem.font;
    log("APPLY_FONT_SOURCE target=" + targetName + " source=" + sourceName);
    return true;
  }} catch (e) {{
    TRACE.push("APPLY_FONT_SOURCE_FAILED " + targetName + " :: " + e.message);
    log("APPLY_FONT_SOURCE_FAILED " + targetName + " :: " + e.message);
    return false;
  }}
}}

function setOptionalText(doc, name, value) {{
  var layer = findLayer(doc, name);
  if (!layer) return false;
  return setText(doc, name, value);
}}

function hideLayer(doc, name) {{
  var layer = findLayer(doc, name);
  if (layer) {{
    layer.visible = false;
    log("HIDE_LAYER " + name);
  }}
}}

function setHeader(doc) {{
  setText(doc, "@SHELL_TOP_LESSON_NO_TEXT", DATA.lessonNo);
  setText(doc, "@SHELL_TOP_LESSON_TITLE_TEXT", DATA.lessonTitle);
  setOptionalText(doc, "@LESSON_NO_COVER_TEXT", DATA.lessonNo);
  setOptionalText(doc, "@LESSON_TITLE_COVER_TEXT", DATA.lessonTitle);
}}

function setPageNo(doc, left, right) {{
  setText(doc, "@PAGE_NO_LEFT_TEXT", left);
  setText(doc, "@PAGE_NO_RIGHT_TEXT", right);
}}

function applyHiddenLayers(doc, pageSpec) {{
  var names = pageSpec.hiddenLayers || [];
  for (var i = 0; i < names.length; i++) {{
    hideLayer(doc, names[i]);
  }}
}}

function hidePart3Subtitle(doc, no) {{
  var id = no < 10 ? "0" + no : "" + no;
  hideLayer(doc, "@PART3_SUBTITLE_" + id + "_GROUP");
}}

function hideAllPart3Subtitles(doc) {{
  for (var i = 1; i <= 12; i++) {{
    hidePart3Subtitle(doc, i);
  }}
}}

function applyPart3SubtitlePolicy(doc, pageSpec) {{
  var modules = pageSpec.modules || [];
  for (var i = 0; i < modules.length; i++) {{
    if ((modules[i].type === "grammarFlow" || modules[i].type === "grammarFlowContinuation") &&
        (modules[i].subtitlePolicy === "hideSubtitleGroupsWhenWordHasNoSectionTitle" || PLAN.rules.part3NoFakeSubtitles)) {{
      hideAllPart3Subtitles(doc);
      return;
    }}
  }}
  if (PLAN.rules.part3NoFakeSubtitles) hideAllPart3Subtitles(doc);
}}

function findModule(pageSpec, moduleId) {{
  var modules = pageSpec.modules || [];
  for (var i = 0; i < modules.length; i++) {{
    if (modules[i].id === moduleId) return modules[i];
  }}
  throw new Error("Missing module " + moduleId + " on page " + pageSpec.pageIndex);
}}

function fixedRowTextMayOverflow(text, limit) {{
  return (text || "").length > limit;
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
  applyFontFromStyleSource(doc, prefix + "_PHONETIC_TEXT", "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE");
  setText(doc, prefix + "_MEANING_TEXT", item.meaning);
  if (rowSpec.fixedHeight && (fixedRowTextMayOverflow(item.word, 32) || fixedRowTextMayOverflow(item.meaning, 42))) {{
    TRACE.push("REVIEW_VOCAB_FIXED_BOX row=" + rowNo + " word=" + item.word);
  }}
}}

function applyVocabModule(doc, pageSpec, moduleId) {{
  var module = findModule(pageSpec, moduleId);
  var rows = module.rows || [];
  var items = module.items || [];
  for (var i = 0; i < rows.length; i++) {{
    setVocabRowFromPlan(doc, rows[i], items[i]);
  }}
}}

function applyPart1Module(doc, pageSpec) {{
  var module = findModule(pageSpec, "part1");
  hideLayer(doc, "@PART1_READING_LEFT_TEXT_STYLE_SOURCE");
  hideLayer(doc, "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE");
  layoutReadingLines(doc);
  setText(doc, "@PART1_DIALOGUE_INTRO_TEXT", DATA.dialogueIntro);
  setText(doc, "@PART1_DIALOGUE_ROLE_MAP_TEXT", DATA.dialogueRole);
  hideLayer(doc, "@PART1_DIALOGUE_SAMPLE_LINE_TEXT");
  layoutDialogueLines(doc);
  TRACE.push("MEASURE_REQUIRED part1 reading line wraps using PSD font metrics");
  TRACE.push("MEASURE_REQUIRED part1 reading green border bottom resize");
  TRACE.push("MEASURE_REQUIRED part1 dialogue yellow box bottom resize");
  TRACE.push("MEASURE_REQUIRED part1 dialogue green vertical line resize");
  TRACE.push("MEASURE_REQUIRED part1 dialogue overflow right frame to next left frame");
  if (module.dynamic !== true) TRACE.push("REVIEW part1 module is not marked dynamic");
}}

function layoutReadingLines(doc) {{
  var metrics = DATA.readingMetrics;
  var x = metrics.textX;
  var y = metrics.textTop;
  var maxRight = metrics.maxRight;
  var lineGap = metrics.lineGap;
  var firstLineX = x + (metrics.bodyFirstLineIndent || 0);
  var continuationX = x + (metrics.bodyContinuationIndent || 0);
  var blockLineCount = metrics.blockLineCount;
  var phoneticStyleSource = metrics.phoneticStyleSource;
  var bodyStyleSource = metrics.bodyStyleSource;
  requireStyleSource(doc, phoneticStyleSource);
  requireStyleSource(doc, bodyStyleSource);

  function lowerText(value) {{
    return (value || "").toLowerCase();
  }}

  function findTargetInLine(lineText, target) {{
    if (!target) return -1;
    return lowerText(lineText).indexOf(lowerText(target));
  }}

  function splitReadingBody(text, bodyTop) {{
    var firstCandidates = splitTextByMeasuredRight(doc, bodyStyleSource, text, firstLineX, bodyTop, maxRight);
    var firstText = firstCandidates.length ? firstCandidates[0] : "";
    var remaining = "";
    if (firstText && text.length > firstText.length) {{
      remaining = text.substring(firstText.length).replace(/^\\s+/, "");
    }}
    var lines = [];
    if (firstText) lines.push({{ text: firstText, x: firstLineX, y: bodyTop }});
    if (remaining) {{
      var continuationLines = splitTextByMeasuredRight(doc, bodyStyleSource, remaining, continuationX, bodyTop + lineGap, maxRight);
      for (var c = 0; c < continuationLines.length; c++) {{
        lines.push({{ text: continuationLines[c], x: continuationX, y: bodyTop + lineGap * (c + 1) }});
      }}
    }}
    return lines;
  }}

  function placeReadingPhoneticSegments(block, bodyLines, phoneticTop, blockIndex) {{
    var placed = 0;
    var segments = block.segments || [];
    for (var s = 0; s < segments.length; s++) {{
      var segment = segments[s];
      var placedSegment = false;
      for (var l = 0; l < bodyLines.length; l++) {{
        var line = bodyLines[l];
        var targetAt = findTargetInLine(line.text, segment.target);
        if (targetAt >= 0) {{
          var prefix = line.text.substring(0, targetAt);
          var targetX = line.x;
          if (prefix) targetX = measureTextRight(doc, bodyStyleSource, prefix, line.x, line.y);
          duplicateTextLayer(doc, phoneticStyleSource, "@RUN_READING_PHONETIC_" + blockIndex + "_" + s, segment.text, targetX, line.y - lineGap);
          placed++;
          placedSegment = true;
          break;
        }}
      }}
      if (!placedSegment) {{
        duplicateTextLayer(doc, phoneticStyleSource, "@RUN_READING_PHONETIC_" + blockIndex + "_" + s, segment.text, firstLineX, phoneticTop);
        TRACE.push("READING_PHONETIC_TARGET_MISSING block=" + blockIndex + " text=" + segment.text);
        placed++;
      }}
    }}
    if (!placed && block.phonetic) {{
      duplicateTextLayer(doc, phoneticStyleSource, "@RUN_READING_PHONETIC_" + blockIndex, block.phonetic, firstLineX, phoneticTop);
    }}
  }}

  var placedBodyLines = 0;
  for (var i = 0; i < DATA.readingBlocks.length; i++) {{
    var block = DATA.readingBlocks[i];
    var bodyTop = y + lineGap;
    var bodyLines = splitReadingBody(block.text || "", bodyTop);
    placeReadingPhoneticSegments(block, bodyLines, y, i);
    for (var w = 0; w < bodyLines.length; w++) {{
      duplicateTextLayer(doc, bodyStyleSource, "@RUN_READING_BODY_" + i + "_" + w, bodyLines[w].text, bodyLines[w].x, bodyLines[w].y);
      placedBodyLines++;
    }}
    y = bodyTop + lineGap * Math.max(bodyLines.length, 1);
    y += lineGap * Math.max(blockLineCount - 2, 0);
  }}
  TRACE.push("READING_PLACED_BODY_LINES=" + placedBodyLines + " bottom=" + y + " firstLineX=" + firstLineX + " continuationX=" + continuationX);
}}

function layoutDialogueLines(doc) {{
  var metrics = DATA.dialogueMetrics;
  var roleX = metrics.roleX;
  var y = metrics.lineTop;
  var phoneticOffset = metrics.phoneticOffset;
  var dialogueGap = metrics.lineGap;
  var roleSpaceWidth = metrics.roleSpaceWidth;
  var maxRight = metrics.textMaxRight;
  var continuationX = metrics.continuationIndentX;
  var phoneticStyleSource = "@PART1_READING_LEFT_TEXT_STYLE_SOURCE";
  var roleStyleSource = "@PART1_DIALOGUE_SAMPLE_LINE_TEXT";
  var bodyStyleSource = "@PART1_DIALOGUE_INTRO_TEXT";
  requireStyleSource(doc, phoneticStyleSource);
  requireStyleSource(doc, roleStyleSource);
  requireStyleSource(doc, bodyStyleSource);
  var pendingPhonetic = "";
  var placedLines = 0;
  for (var i = 0; i < DATA.dialogueLines.length; i++) {{
    var line = DATA.dialogueLines[i];
    if (line.kind === "phonetic") {{
      pendingPhonetic = line.text;
      continue;
    }}
    if (pendingPhonetic) {{
      duplicateTextLayer(doc, phoneticStyleSource, "@RUN_DIALOGUE_PHONETIC_" + i, pendingPhonetic, roleX, y - phoneticOffset);
      pendingPhonetic = "";
    }}
    var role = line.speaker ? line.speaker + ":" : "";
    var body = line.text || "";
    if (role && body.indexOf(role) === 0) body = body.substring(role.length).replace(/^\\s+/, "");
    var roleWidth = metrics.roleWidths[role] || metrics.roleWidths["M:"];
    var bodyX = roleX + roleWidth + roleSpaceWidth;
    var firstLines = splitTextByMeasuredRight(doc, bodyStyleSource, body, bodyX, y, maxRight);
    var firstText = firstLines.length ? firstLines[0] : "";
    duplicateTextLayer(doc, roleStyleSource, "@RUN_DIALOGUE_ROLE_" + i, role, roleX, y);
    duplicateTextLayer(doc, bodyStyleSource, "@RUN_DIALOGUE_BODY_" + i + "_0", firstText, bodyX, y);
    placedLines++;
    var remaining = "";
    if (firstText && body.length > firstText.length) {{
      remaining = body.substring(firstText.length).replace(/^\\s+/, "");
    }}
    var continuationLines = remaining ? splitTextByMeasuredRight(doc, bodyStyleSource, remaining, continuationX, y + dialogueGap, maxRight) : [];
    for (var c = 0; c < continuationLines.length; c++) {{
      y += dialogueGap;
      duplicateTextLayer(doc, bodyStyleSource, "@RUN_DIALOGUE_BODY_" + i + "_" + (c + 1), continuationLines[c], continuationX, y);
      placedLines++;
    }}
    y += dialogueGap;
  }}
  TRACE.push("DIALOGUE_PLACED_LINES=" + placedLines + " bottom=" + y + " maxRight=" + maxRight + " continuationX=" + continuationX);
}}

function savePsd(doc, path) {{
  var opts = new PhotoshopSaveOptions();
  opts.layers = true;
  doc.saveAs(new File(path), opts, true, Extension.LOWERCASE);
}}

function exportJpg(doc, path) {{
  var opts = new ExportOptionsSaveForWeb();
  opts.format = SaveDocumentType.JPEG;
  opts.quality = 80;
  doc.exportDocument(new File(path), ExportType.SAVEFORWEB, opts);
}}

function pageSpec(pageNo) {{
  for (var i = 0; i < PLAN.pages.length; i++) {{
    if (PLAN.pages[i].pageIndex === pageNo) return PLAN.pages[i];
  }}
  throw new Error("Missing page spec " + pageNo);
}}

function renderPage(pageNo, fillFn) {{
  if (pageNo > MAX_PAGES_PER_LESSON) throw new Error("MAX_PAGES_PER_LESSON exceeded: " + pageNo);
  var spec = pageSpec(pageNo);
  log("OPEN_PAGE page=" + pageNo + " template=" + spec.template);
  var doc = app.open(new File(ROOT + "/" + spec.template));
  buildLayerMap(doc);
  unlockAll(doc);
  applyHiddenLayers(doc, spec);
  applyPart3SubtitlePolicy(doc, spec);
  setHeader(doc);
  setPageNo(doc, spec.pageNumbers[0], spec.pageNumbers[1]);
  fillFn(doc);
  var base = OUT + "/lesson_1_2_page_" + (pageNo < 10 ? "0" + pageNo : pageNo);
  log("SAVE_PAGE page=" + pageNo + " psd=" + base + ".psd");
  savePsd(doc, base + ".psd");
  log("EXPORT_JPG page=" + pageNo + " jpg=" + base + ".jpg");
  exportJpg(doc, base + ".jpg");
  doc.close(SaveOptions.DONOTSAVECHANGES);
  log("CLOSE_PAGE page=" + pageNo);
}}

ensureFolder(ROOT + "/output");
ensureFolder(OUT);
if (PLAN.pages.length > MAX_PAGES_PER_LESSON) throw new Error("Plan pages exceed MAX_PAGES_PER_LESSON: " + PLAN.pages.length);
openLog();

renderPage(1, function(doc) {{
  var spec = pageSpec(1);
  applyPart1Module(doc, spec);
  applyVocabModule(doc, spec, "part2_rows_01_08");
}});

if (!RENDER_FIRST_PAGE_ONLY) {{

renderPage(2, function(doc) {{
  var spec = pageSpec(2);
  applyVocabModule(doc, spec, "part2_rows_09_21");
  setText(doc, "@PART3_LEAD_ORANGE_ITALIC_TEXT", DATA.grammarLead);
  setText(doc, "@PART3_BODY_TEXT_BLOCK_02", DATA.grammarP2A);
  setText(doc, "@PART3_BODY_TEXT_BLOCK_03", DATA.grammarP2B);
}});

renderPage(3, function(doc) {{
  setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT_01", DATA.grammarP3A);
  setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT_02", DATA.grammarP3B);
  setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT_03", DATA.grammarP3C);
  setText(doc, "@PART3_CONT_TEXT_BLOCK_RIGHT_01", DATA.grammarP3D);
  setText(doc, "@PART3_CONT_TEXT_BLOCK_RIGHT_02", "");
}});

renderPage(4, function(doc) {{
  setText(doc, "@PART3_CONT_TEXT_BLOCK_LEFT", DATA.grammarP4A);
  setText(doc, "@PART3_CONT_TEXT_BLOCK_RIGHT_TOP", DATA.grammarP4B);
  if (DATA.grammarOverflow && DATA.grammarOverflow.length) TRACE.push("REVIEW_GRAMMAR_OVERFLOW paragraphs=" + DATA.grammarOverflow.length);
  setText(doc, "@PART4_EXERCISE_Q1_NO_TEXT", DATA.exerciseSection1No);
  setText(doc, "@PART4_EXERCISE_Q1_BODY_TEXT", DATA.exerciseP4A);
  setText(doc, "@PART4_EXERCISE_Q2_NO_TEXT", DATA.exerciseSection2No);
  setText(doc, "@PART4_EXERCISE_Q2_BODY_TEXT", "");
}});

renderPage(5, function(doc) {{
  setText(doc, "@PART4_EXERCISE_CONT_BODY_TEXT", DATA.exerciseP4B);
}});

}}

var traceFile = new File(OUT + "/render_trace.txt");
traceFile.encoding = "UTF-8";
traceFile.open("w");
traceFile.write(TRACE.join("\\n"));
traceFile.close();
closeLog();
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

$projectRoot = Split-Path $PSScriptRoot -Parent
$jsxPath = Join-Path $projectRoot "photoshop\render_lesson_1_2_sample.jsx"

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
Write-Output "Lesson 1-2 sample render finished"
"""

OUT_JSX.write_text(jsx, encoding="utf-8-sig")
OUT_PS1.write_text(ps1, encoding="utf-8")
print(OUT_JSX)
print(OUT_PS1)
