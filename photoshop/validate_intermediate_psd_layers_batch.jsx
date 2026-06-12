#target photoshop
app.displayDialogs = DialogModes.NO;
app.preferences.rulerUnits = Units.PIXELS;

var JOBS = [{"manifestName": "3-4_1_FIRST_PAGE_template_renamed.psd", "psdPath": "C:/Users/Administrator/Desktop/中级美语/3-4 1.psd", "expected": ["@SHELL_FIRST_BG_TEXTURE_FULL", "@SHELL_FIRST_STICKER_LEFT", "@SHELL_FIRST_STICKER_RIGHT", "@SHELL_FIRST_TOP_BAR_OR_PANEL_SHAPE_01", "@SHELL_FIRST_TOP_DECOR_TEXTURE_RIGHT", "@SHELL_FIRST_TOP_BAR_MAIN_SHAPE_01", "@SHELL_FIRST_TOP_BAR_BREAK_SHAPE_01", "@SHELL_FIRST_TOP_BAR_MAIN_SHAPE_02", "@SHELL_FIRST_TOP_DECOR_TEXTURE_LEFT", "@SHELL_FIRST_TITLE_BAR_DECOR_01", "@SHELL_FIRST_TITLE_BAR_DECOR_02", "@SHELL_TOP_LESSON_NO_TEXT", "@SHELL_TOP_LESSON_TITLE_TEXT", "@SHELL_FIRST_COVER_LESSON_NO_BG_SHAPE", "@SHELL_FIRST_COVER_LESSON_TITLE_BG_SHAPE", "@SHELL_FIRST_COVER_BAR_MAIN_SHAPE", "@SHELL_FIRST_COVER_BAR_BREAK_SHAPE", "@LESSON_NO_COVER_TEXT", "@LESSON_TITLE_COVER_TEXT", "@LESSON_COVER_TITLE_GROUP", "@SHELL_FIRST_TOP_HEADER_GROUP", "@PART1_DIALOGUE_LINE_BG_SHAPE", "@PART1_DIALOGUE_SAMPLE_LINE_TEXT", "@PART1_DIALOGUE_YELLOW_BG_SHAPE", "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE", "@PART1_READING_BORDER_SHAPE_A", "@PART1_READING_BORDER_SHAPE_B", "@PART1_DIALOGUE_BORDER_TOP_SHAPE", "@PART1_DIALOGUE_BORDER_BOTTOM_SHAPE", "@PART1_DIALOGUE_BORDER_LEFT_SHAPE", "@PART1_READING_LEFT_TEXT_STYLE_SOURCE", "@PART1_DIALOGUE_INTRO_TEXT", "@PART1_DIALOGUE_ROLE_MAP_TEXT", "@PART1_TITLE_BG_SHAPE_A", "@PART1_TITLE_BG_SHAPE_B", "@PART1_TITLE_GROUP", "@PART1_TITLE_TEXT", "@PART1_CONTENT_GROUP", "@PART1_READING_DIALOGUE_GROUP", "@PAGE_NO_LEFT_BG_SHAPE", "@PAGE_NO_LEFT_DECOR_SHAPE", "@PAGE_NO_LEFT_TEXT", "@PAGE_NO_RIGHT_BG_SHAPE", "@PAGE_NO_RIGHT_DECOR_SHAPE", "@PAGE_NO_RIGHT_TEXT", "@PAGE_NUMBER_GROUP", "@PART2_VOCAB_ROW_01_BG_SHAPE", "@PART2_VOCAB_ROW_01_WORD_TEXT", "@PART2_VOCAB_ROW_01_PHONETIC_TEXT", "@PART2_VOCAB_ROW_01_NO_TEXT", "@PART2_VOCAB_ROW_01_MEANING_TEXT", "@PART2_VOCAB_ROW_01_GROUP", "@PART2_VOCAB_ROW_02_BG_SHAPE", "@PART2_VOCAB_ROW_02_WORD_TEXT", "@PART2_VOCAB_ROW_02_PHONETIC_TEXT", "@PART2_VOCAB_ROW_02_NO_TEXT", "@PART2_VOCAB_ROW_02_MEANING_TEXT", "@PART2_VOCAB_ROW_02_GROUP", "@PART2_VOCAB_ROW_03_BG_SHAPE", "@PART2_VOCAB_ROW_03_WORD_TEXT", "@PART2_VOCAB_ROW_03_PHONETIC_TEXT", "@PART2_VOCAB_ROW_03_NO_TEXT", "@PART2_VOCAB_ROW_03_MEANING_TEXT", "@PART2_VOCAB_ROW_03_GROUP", "@PART2_VOCAB_ROW_04_BG_SHAPE", "@PART2_VOCAB_ROW_04_WORD_TEXT", "@PART2_VOCAB_ROW_04_PHONETIC_TEXT", "@PART2_VOCAB_ROW_04_NO_TEXT", "@PART2_VOCAB_ROW_04_MEANING_TEXT", "@PART2_VOCAB_ROW_04_GROUP", "@PART2_VOCAB_ROW_05_BG_SHAPE", "@PART2_VOCAB_ROW_05_WORD_TEXT", "@PART2_VOCAB_ROW_05_PHONETIC_TEXT", "@PART2_VOCAB_ROW_05_NO_TEXT", "@PART2_VOCAB_ROW_05_MEANING_TEXT", "@PART2_VOCAB_ROW_05_GROUP", "@PART2_VOCAB_ROW_06_BG_SHAPE", "@PART2_VOCAB_ROW_06_WORD_TEXT", "@PART2_VOCAB_ROW_06_PHONETIC_TEXT", "@PART2_VOCAB_ROW_06_NO_TEXT", "@PART2_VOCAB_ROW_06_MEANING_TEXT", "@PART2_VOCAB_ROW_06_GROUP", "@PART2_VOCAB_ROW_07_BG_SHAPE", "@PART2_VOCAB_ROW_07_WORD_TEXT", "@PART2_VOCAB_ROW_07_PHONETIC_TEXT", "@PART2_VOCAB_ROW_07_NO_TEXT", "@PART2_VOCAB_ROW_07_MEANING_TEXT", "@PART2_VOCAB_ROW_07_GROUP", "@PART2_VOCAB_ROW_08_BG_SHAPE", "@PART2_VOCAB_ROW_08_WORD_TEXT", "@PART2_VOCAB_ROW_08_PHONETIC_TEXT", "@PART2_VOCAB_ROW_08_NO_TEXT", "@PART2_VOCAB_ROW_08_MEANING_TEXT", "@PART2_VOCAB_ROW_08_GROUP", "@PART2_TITLE_BG_SHAPE_A", "@PART2_TITLE_BG_SHAPE_B", "@PART2_TITLE_GROUP", "@PART2_TITLE_TEXT", "@PART2_CONTENT_GROUP", "@SHELL_FIRST_CONTENT_PANEL_GROUP", "@SHELL_PANEL_CORNER_DECOR_LEFT", "@SHELL_PANEL_CORNER_DECOR_RIGHT", "@SHELL_CONTENT_PANEL_LEFT", "@SHELL_CONTENT_PANEL_RIGHT", "@SHELL_CONTENT_PANEL_DECOR_SHAPE"]}, {"manifestName": "3-4_2_CONT_PAGE_template_renamed.psd", "psdPath": "C:/Users/Administrator/Desktop/中级美语/3-4 2.psd", "expected": ["@SHELL_BG_TEXTURE_FULL", "@SHELL_STICKER_LEFT", "@SHELL_STICKER_RIGHT", "@SHELL_TOP_BAR_OR_PANEL_SHAPE_01", "@SHELL_TOP_DECOR_TEXTURE_RIGHT", "@SHELL_TOP_BAR_OR_PANEL_SHAPE_02", "@SHELL_TOP_DECOR_TEXTURE_LEFT", "@SHELL_TOP_BAR_MAIN_SHAPE", "@SHELL_TOP_BAR_BREAK_SHAPE", "@SHELL_TITLE_BAR_DECOR_01", "@SHELL_TITLE_BAR_DECOR_02", "@SHELL_TITLE_BAR_DECOR_03", "@SHELL_TITLE_BAR_DECOR_04", "@SHELL_TOP_LESSON_NO_TEXT", "@SHELL_TOP_LESSON_TITLE_TEXT", "@SHELL_BOOK_TITLE_BG_SHAPE", "@SHELL_BOOK_TITLE_TEXT", "@SHELL_TOP_HEADER_GROUP", "@PART2_VOCAB_ROW_09_BG_SHAPE", "@PART2_VOCAB_ROW_09_WORD_TEXT", "@PART2_VOCAB_ROW_09_PHONETIC_TEXT", "@PART2_VOCAB_ROW_09_NO_TEXT", "@PART2_VOCAB_ROW_09_MEANING_TEXT", "@PART2_VOCAB_ROW_09_GROUP", "@PART2_VOCAB_ROW_10_BG_SHAPE", "@PART2_VOCAB_ROW_10_WORD_TEXT", "@PART2_VOCAB_ROW_10_PHONETIC_TEXT", "@PART2_VOCAB_ROW_10_NO_TEXT", "@PART2_VOCAB_ROW_10_MEANING_TEXT", "@PART2_VOCAB_ROW_10_GROUP", "@PART2_VOCAB_ROW_11_BG_SHAPE", "@PART2_VOCAB_ROW_11_WORD_TEXT", "@PART2_VOCAB_ROW_11_PHONETIC_TEXT", "@PART2_VOCAB_ROW_11_NO_TEXT", "@PART2_VOCAB_ROW_11_MEANING_TEXT", "@PART2_VOCAB_ROW_11_GROUP", "@PART2_VOCAB_ROW_12_BG_SHAPE", "@PART2_VOCAB_ROW_12_WORD_TEXT", "@PART2_VOCAB_ROW_12_PHONETIC_TEXT", "@PART2_VOCAB_ROW_12_NO_TEXT", "@PART2_VOCAB_ROW_12_MEANING_TEXT", "@PART2_VOCAB_ROW_12_GROUP", "@PART2_VOCAB_ROW_13_BG_SHAPE", "@PART2_VOCAB_ROW_13_WORD_TEXT", "@PART2_VOCAB_ROW_13_PHONETIC_TEXT", "@PART2_VOCAB_ROW_13_NO_TEXT", "@PART2_VOCAB_ROW_13_MEANING_TEXT", "@PART2_VOCAB_ROW_13_GROUP", "@PART2_VOCAB_ROW_14_BG_SHAPE", "@PART2_VOCAB_ROW_14_WORD_TEXT", "@PART2_VOCAB_ROW_14_PHONETIC_TEXT", "@PART2_VOCAB_ROW_14_NO_TEXT", "@PART2_VOCAB_ROW_14_MEANING_TEXT", "@PART2_VOCAB_ROW_14_GROUP", "@PART2_VOCAB_ROW_15_BG_SHAPE", "@PART2_VOCAB_ROW_15_WORD_TEXT", "@PART2_VOCAB_ROW_15_PHONETIC_TEXT", "@PART2_VOCAB_ROW_15_NO_TEXT", "@PART2_VOCAB_ROW_15_MEANING_TEXT", "@PART2_VOCAB_ROW_15_GROUP", "@PART2_VOCAB_ROW_16_BG_SHAPE", "@PART2_VOCAB_ROW_16_WORD_TEXT", "@PART2_VOCAB_ROW_16_PHONETIC_TEXT", "@PART2_VOCAB_ROW_16_NO_TEXT", "@PART2_VOCAB_ROW_16_MEANING_TEXT", "@PART2_VOCAB_ROW_16_GROUP", "@PART2_VOCAB_ROW_17_BG_SHAPE", "@PART2_VOCAB_ROW_17_WORD_TEXT", "@PART2_VOCAB_ROW_17_PHONETIC_TEXT", "@PART2_VOCAB_ROW_17_NO_TEXT", "@PART2_VOCAB_ROW_17_MEANING_TEXT", "@PART2_VOCAB_ROW_17_GROUP", "@PART2_VOCAB_ROW_18_BG_SHAPE", "@PART2_VOCAB_ROW_18_WORD_TEXT", "@PART2_VOCAB_ROW_18_PHONETIC_TEXT", "@PART2_VOCAB_ROW_18_NO_TEXT", "@PART2_VOCAB_ROW_18_MEANING_TEXT", "@PART2_VOCAB_ROW_18_GROUP", "@PART2_VOCAB_ROW_19_BG_SHAPE", "@PART2_VOCAB_ROW_19_WORD_TEXT", "@PART2_VOCAB_ROW_19_PHONETIC_TEXT", "@PART2_VOCAB_ROW_19_NO_TEXT", "@PART2_VOCAB_ROW_19_MEANING_TEXT", "@PART2_VOCAB_ROW_19_GROUP", "@PART2_VOCAB_ROW_20_BG_SHAPE", "@PART2_VOCAB_ROW_20_WORD_TEXT", "@PART2_VOCAB_ROW_20_PHONETIC_TEXT", "@PART2_VOCAB_ROW_20_NO_TEXT", "@PART2_VOCAB_ROW_20_MEANING_TEXT", "@PART2_VOCAB_ROW_20_GROUP", "@PART2_VOCAB_ROW_21_BG_SHAPE", "@PART2_VOCAB_ROW_21_WORD_TEXT", "@PART2_VOCAB_ROW_21_PHONETIC_TEXT", "@PART2_VOCAB_ROW_21_NO_TEXT", "@PART2_VOCAB_ROW_21_MEANING_TEXT", "@PART2_VOCAB_ROW_21_GROUP", "@PART2_VOCAB_CONT_GROUP", "@PART3_BODY_TEXT_BLOCK_02", "@PART3_BODY_TEXT_BLOCK_03", "@PART3_LEAD_ORANGE_ITALIC_TEXT", "@PART3_SUBTITLE_01_BG_SHAPE_A", "@PART3_SUBTITLE_01_BG_SHAPE_B", "@PART3_SUBTITLE_01_BG_SHAPE_C", "@PART3_SUBTITLE_01_TEXT", "@PART3_SUBTITLE_01_NO_TEXT", "@PART3_SUBTITLE_01_GROUP", "@PART3_SUBTITLE_02_BG_SHAPE_A", "@PART3_SUBTITLE_02_BG_SHAPE_B", "@PART3_SUBTITLE_02_BG_SHAPE_C", "@PART3_SUBTITLE_02_TEXT", "@PART3_SUBTITLE_02_NO_TEXT", "@PART3_SUBTITLE_02_GROUP", "@PART3_TITLE_BG_SHAPE_A", "@PART3_TITLE_BG_SHAPE_B", "@PART3_TITLE_GROUP", "@PART3_TITLE_TEXT", "@PART3_CONTENT_GROUP", "@PART3_SECTION_GROUP", "@PART3_LEAD_GROUP", "@PAGE_NO_LEFT_BG_SHAPE", "@PAGE_NO_LEFT_DECOR_SHAPE", "@PAGE_NO_LEFT_TEXT", "@PAGE_NO_RIGHT_BG_SHAPE", "@PAGE_NO_RIGHT_DECOR_SHAPE", "@PAGE_NO_RIGHT_TEXT", "@PAGE_NUMBER_GROUP", "@SHELL_PANEL_CORNER_DECOR_LEFT", "@SHELL_PANEL_CORNER_DECOR_RIGHT", "@SHELL_CONTENT_PANEL_LEFT", "@SHELL_CONTENT_PANEL_RIGHT", "@SHELL_CONTENT_PANEL_DECOR_SHAPE_LEFT", "@SHELL_CONTENT_PANEL_DECOR_SHAPE_RIGHT"]}, {"manifestName": "3-4_3_GRAMMAR_CONT_ref_renamed.psd", "psdPath": "C:/Users/Administrator/Desktop/中级美语/3-4 3.psd", "expected": ["@SHELL_BG_TEXTURE_FULL", "@SHELL_STICKER_LEFT", "@SHELL_STICKER_RIGHT", "@SHELL_TOP_BAR_OR_PANEL_SHAPE_01", "@SHELL_TOP_DECOR_TEXTURE_RIGHT", "@SHELL_TOP_BAR_OR_PANEL_SHAPE_02", "@SHELL_TOP_DECOR_TEXTURE_LEFT", "@SHELL_TOP_BAR_MAIN_SHAPE", "@SHELL_TOP_BAR_BREAK_SHAPE", "@SHELL_TITLE_BAR_DECOR_01", "@SHELL_TITLE_BAR_DECOR_02", "@SHELL_TITLE_BAR_DECOR_03", "@SHELL_TITLE_BAR_DECOR_04", "@SHELL_TOP_LESSON_NO_TEXT", "@SHELL_TOP_LESSON_TITLE_TEXT", "@SHELL_BOOK_TITLE_BG_SHAPE", "@SHELL_BOOK_TITLE_TEXT", "@SHELL_TOP_HEADER_GROUP", "@PAGE_NO_LEFT_BG_SHAPE", "@PAGE_NO_LEFT_DECOR_SHAPE", "@PAGE_NO_LEFT_TEXT", "@PAGE_NO_RIGHT_BG_SHAPE", "@PAGE_NO_RIGHT_DECOR_SHAPE", "@PAGE_NO_RIGHT_TEXT", "@PAGE_NUMBER_GROUP", "@PART3_CONT_TEXT_BLOCK_RIGHT_02", "@PART3_CONT_TEXT_BLOCK_LEFT_02", "@PART3_CONT_TEXT_BLOCK_LEFT_01", "@PART3_CONT_TEXT_BLOCK_LEFT_03", "@PART3_CONT_TEXT_BLOCK_RIGHT_01", "@PART3_SUBTITLE_03_BG_SHAPE_A", "@PART3_SUBTITLE_03_BG_SHAPE_B", "@PART3_SUBTITLE_03_BG_SHAPE_C", "@PART3_SUBTITLE_03_TEXT", "@PART3_SUBTITLE_03_NO_TEXT", "@PART3_SUBTITLE_03_GROUP", "@PART3_SUBTITLE_04_BG_SHAPE_A", "@PART3_SUBTITLE_04_BG_SHAPE_B", "@PART3_SUBTITLE_04_BG_SHAPE_C", "@PART3_SUBTITLE_04_TEXT", "@PART3_SUBTITLE_04_NO_TEXT", "@PART3_SUBTITLE_04_GROUP", "@PART3_CONT_GROUP", "@SHELL_CONTENT_PANEL_LEFT", "@SHELL_CONTENT_PANEL_RIGHT", "@SHELL_PANEL_CORNER_DECOR_LEFT", "@SHELL_PANEL_CORNER_DECOR_RIGHT"]}, {"manifestName": "3-4_4_GRAMMAR_EXERCISE_ref_renamed.psd", "psdPath": "C:/Users/Administrator/Desktop/中级美语/3-4 4.psd", "expected": ["@SHELL_BG_TEXTURE_FULL", "@SHELL_STICKER_LEFT", "@SHELL_STICKER_RIGHT", "@SHELL_TOP_BAR_OR_PANEL_SHAPE_01", "@SHELL_TOP_DECOR_TEXTURE_RIGHT", "@SHELL_TOP_BAR_OR_PANEL_SHAPE_02", "@SHELL_TOP_DECOR_TEXTURE_LEFT", "@SHELL_TOP_BAR_MAIN_SHAPE", "@SHELL_TOP_BAR_BREAK_SHAPE", "@SHELL_TITLE_BAR_DECOR_01", "@SHELL_TITLE_BAR_DECOR_02", "@SHELL_TITLE_BAR_DECOR_03", "@SHELL_TITLE_BAR_DECOR_04", "@SHELL_TOP_LESSON_NO_TEXT", "@SHELL_TOP_LESSON_TITLE_TEXT", "@SHELL_BOOK_TITLE_BG_SHAPE", "@SHELL_BOOK_TITLE_TEXT", "@SHELL_TOP_HEADER_GROUP", "@PAGE_NO_LEFT_BG_SHAPE", "@PAGE_NO_LEFT_DECOR_SHAPE", "@PAGE_NO_LEFT_TEXT", "@PAGE_NO_RIGHT_BG_SHAPE", "@PAGE_NO_RIGHT_DECOR_SHAPE", "@PAGE_NO_RIGHT_TEXT", "@PAGE_NUMBER_GROUP", "@PART4_EXERCISE_Q1_BODY_TEXT", "@PART4_EXERCISE_Q2_BODY_TEXT", "@PART4_EXERCISE_Q2_NO_TEXT", "@PART4_EXERCISE_Q1_NO_TEXT", "@PART4_TITLE_BG_SHAPE_A", "@PART4_TITLE_BG_SHAPE_B", "@PART4_TITLE_GROUP", "@PART4_TITLE_TEXT", "@PART4_CONTENT_GROUP", "@PART4_EXERCISE_GROUP", "@PART3_CONT_TEXT_BLOCK_LEFT", "@PART3_CONT_TEXT_BLOCK_RIGHT_TOP", "@PART3_SUBTITLE_05_BG_SHAPE_A", "@PART3_SUBTITLE_05_BG_SHAPE_B", "@PART3_SUBTITLE_05_BG_SHAPE_C", "@PART3_SUBTITLE_05_TEXT", "@PART3_SUBTITLE_05_NO_TEXT", "@PART3_SUBTITLE_05_GROUP", "@PART3_CONT_GROUP", "@SHELL_PANEL_CORNER_DECOR_LEFT", "@SHELL_PANEL_CORNER_DECOR_RIGHT", "@SHELL_CONTENT_PANEL_LEFT", "@SHELL_CONTENT_PANEL_RIGHT"]}, {"manifestName": "3-4_5_EXERCISE_END_ref_renamed.psd", "psdPath": "C:/Users/Administrator/Desktop/中级美语/3-4 5.psd", "expected": ["@SHELL_BG_TEXTURE_FULL", "@SHELL_STICKER_LEFT", "@SHELL_STICKER_RIGHT", "@SHELL_TOP_BAR_OR_PANEL_SHAPE_01", "@SHELL_TOP_DECOR_TEXTURE_RIGHT", "@SHELL_TOP_BAR_OR_PANEL_SHAPE_02", "@SHELL_TOP_DECOR_TEXTURE_LEFT", "@SHELL_TOP_BAR_MAIN_SHAPE", "@SHELL_TOP_BAR_BREAK_SHAPE", "@SHELL_TITLE_BAR_DECOR_01", "@SHELL_TITLE_BAR_DECOR_02", "@SHELL_TITLE_BAR_DECOR_03", "@SHELL_TITLE_BAR_DECOR_04", "@SHELL_TOP_LESSON_NO_TEXT", "@SHELL_TOP_LESSON_TITLE_TEXT", "@SHELL_BOOK_TITLE_BG_SHAPE", "@SHELL_BOOK_TITLE_TEXT", "@SHELL_TOP_HEADER_GROUP", "@PAGE_NO_LEFT_BG_SHAPE", "@PAGE_NO_LEFT_DECOR_SHAPE", "@PAGE_NO_LEFT_TEXT", "@PAGE_NO_RIGHT_BG_SHAPE", "@PAGE_NO_RIGHT_DECOR_SHAPE", "@PAGE_NO_RIGHT_TEXT", "@PAGE_NUMBER_GROUP", "@PART4_EXERCISE_CONT_BODY_TEXT", "@PART4_TITLE_GROUP_REF", "@PART4_CONTENT_GROUP_REF", "@PART4_EXERCISE_CONT_GROUP_REF", "@PART3_OR_PART4_SUBTITLE_05_GROUP_REF", "@SHELL_CONTENT_PANEL_GROUP", "@SHELL_PANEL_CORNER_DECOR_LEFT", "@SHELL_PANEL_CORNER_DECOR_RIGHT", "@SHELL_CONTENT_PANEL_LEFT", "@SHELL_CONTENT_PANEL_RIGHT"]}];
var REPORT_JSON = "C:/Users/Administrator/Desktop/中级美语/PS内部图层验证报告.json";
var REPORT_MD = "C:/Users/Administrator/Desktop/中级美语/PS内部图层验证报告.md";

function collectLayerNames(container, out, duplicates, paths, prefix) {
  for (var i = 0; i < container.layers.length; i++) {
    var layer = container.layers[i];
    var path = prefix ? prefix + " > " + layer.name : layer.name;
    if (out[layer.name]) {
      duplicates[layer.name] = (duplicates[layer.name] || 1) + 1;
    } else {
      out[layer.name] = true;
    }
    paths[layer.name] = path;
    if (layer.typename == "LayerSet") {
      collectLayerNames(layer, out, duplicates, paths, path);
    }
  }
}

function quoteJsonString(value) {
  var s = String(value);
  var out = "";
  for (var i = 0; i < s.length; i++) {
    var code = s.charCodeAt(i);
    if (code == 92) out += String.fromCharCode(92, 92);
    else if (code == 34) out += String.fromCharCode(92, 34);
    else if (code == 13) out += String.fromCharCode(92) + "r";
    else if (code == 10) out += String.fromCharCode(92) + "n";
    else if (code == 9) out += String.fromCharCode(92) + "t";
    else out += s.charAt(i);
  }
  return String.fromCharCode(34) + out + String.fromCharCode(34);
}

function jsonStringify(value, indent) {
  if (indent === undefined) indent = "";
  var nextIndent = indent + "  ";
  if (value === null) return "null";
  if (typeof value == "number" || typeof value == "boolean") return String(value);
  if (typeof value == "string") return quoteJsonString(value);
  if (value instanceof Array) {
    if (value.length === 0) return "[]";
    var parts = [];
    for (var i = 0; i < value.length; i++) parts.push(nextIndent + jsonStringify(value[i], nextIndent));
    return "[\n" + parts.join(",\n") + "\n" + indent + "]";
  }
  var fields = [];
  for (var key in value) {
    if (value.hasOwnProperty(key)) {
      fields.push(nextIndent + quoteJsonString(key) + ": " + jsonStringify(value[key], nextIndent));
    }
  }
  if (fields.length === 0) return "{}";
  return "{\n" + fields.join(",\n") + "\n" + indent + "}";
}

function writeText(path, text) {
  var f = new File(path);
  f.encoding = "UTF-8";
  f.open("w");
  f.write(text);
  f.close();
}

function validateJob(job) {
  var result = {
    manifestName: job.manifestName,
    psdPath: job.psdPath,
    opened: false,
    expectedCount: job.expected.length,
    foundCount: 0,
    missingCount: 0,
    duplicateLayerNames: [],
    missing: [],
    error: null
  };

  var doc = null;
  try {
    doc = app.open(new File(job.psdPath));
    result.opened = true;
    result.documentName = doc.name;
    result.width = Number(doc.width.as("px"));
    result.height = Number(doc.height.as("px"));
    result.resolution = Number(doc.resolution);

    var names = {};
    var duplicates = {};
    var paths = {};
    collectLayerNames(doc, names, duplicates, paths, "");

    for (var d in duplicates) {
      result.duplicateLayerNames.push({ name: d, count: duplicates[d] });
    }

    for (var i = 0; i < job.expected.length; i++) {
      var name = job.expected[i];
      if (names[name]) {
        result.foundCount++;
      } else {
        result.missing.push(name);
      }
    }
    result.missingCount = result.missing.length;
  } catch (e) {
    result.error = String(e);
  } finally {
    if (doc) {
      try { doc.close(SaveOptions.DONOTSAVECHANGES); } catch (closeErr) {}
    }
  }
  return result;
}

var report = {
  generatedAt: new Date().toString(),
  root: "C:/Users/Administrator/Desktop/中级美语",
  jobs: [],
  summary: {
    totalExpected: 0,
    totalFound: 0,
    totalMissing: 0,
    filesOpened: 0,
    filesFailed: 0
  }
};

for (var j = 0; j < JOBS.length; j++) {
  var r = validateJob(JOBS[j]);
  report.jobs.push(r);
  report.summary.totalExpected += r.expectedCount;
  report.summary.totalFound += r.foundCount;
  report.summary.totalMissing += r.missingCount;
  if (r.opened && !r.error) report.summary.filesOpened++;
  if (r.error) report.summary.filesFailed++;
}

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
for (var k = 0; k < report.jobs.length; k++) {
  var item = report.jobs[k];
  md.push("## " + item.psdPath);
  md.push("");
  md.push("- manifest: `" + item.manifestName + "`");
  md.push("- 打开状态：" + (item.opened ? "成功" : "失败"));
  if (item.error) md.push("- 错误：" + item.error);
  md.push("- 预期 / 找到 / 缺失：" + item.expectedCount + " / " + item.foundCount + " / " + item.missingCount);
  md.push("- Photoshop 内重复图层名数量：" + item.duplicateLayerNames.length);
  if (item.missing.length > 0) {
    md.push("");
    md.push("缺失图层：");
    for (var m = 0; m < item.missing.length; m++) md.push("- `" + item.missing[m] + "`");
  }
  if (item.duplicateLayerNames.length > 0) {
    md.push("");
    md.push("重复图层名：");
    for (var q = 0; q < item.duplicateLayerNames.length; q++) {
      md.push("- `" + item.duplicateLayerNames[q].name + "` x " + item.duplicateLayerNames[q].count);
    }
  }
  md.push("");
}
writeText(REPORT_MD, md.join("\r\n"));
