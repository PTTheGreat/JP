#target photoshop
app.displayDialogs = DialogModes.NO;

var ROOT = "C:/Users/Administrator/Desktop/涓骇缇庤";
var OUT = "D:/Documents/New project/probes/probe_psd_text_style_ranges.json";
var PSD = ROOT + "/3-4 1.psd";

function esc(s) {
  if (s === undefined || s === null) return "";
  return String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "\\r").replace(/\n/g, "\\n");
}

function id(s) { return stringIDToTypeID(s); }

function walk(container, callback) {
  for (var i = 0; i < container.layers.length; i++) {
    var layer = container.layers[i];
    callback(layer);
    if (layer.typename === "LayerSet") walk(layer, callback);
  }
}

function findLayer(doc, name) {
  var found = null;
  walk(doc, function(layer) {
    if (!found && layer.name === name) found = layer;
  });
  return found;
}

function colorFromStyle(styleDesc) {
  try {
    var c = styleDesc.getObjectValue(id("color"));
    function component(stringKey, charKey) {
      try { return c.getDouble(id(stringKey)); } catch (e1) {}
      try { return c.getDouble(charIDToTypeID(charKey)); } catch (e2) {}
      return null;
    }
    var red = component("red", "Rd  ");
    var green = component("green", "Grn ");
    var blue = component("blue", "Bl  ");
    if (red === null || green === null || blue === null) return "";
    function h(v) {
      var s = Math.round(v).toString(16).toUpperCase();
      return s.length < 2 ? "0" + s : s;
    }
    return h(red) + h(green) + h(blue);
  } catch (e) {
    return "";
  }
}

function numFromStyle(styleDesc, key) {
  try {
    var v = styleDesc.getUnitDoubleValue(id(key));
    return v;
  } catch (e) {
    return null;
  }
}

function strFromStyle(styleDesc, key) {
  try {
    return styleDesc.getString(id(key));
  } catch (e) {
    return "";
  }
}

function getTextStyleRanges(layer) {
  var rows = [];
  var ref = new ActionReference();
  ref.putIdentifier(charIDToTypeID("Lyr "), layer.id);
  var layerDesc = executeActionGet(ref);
  var textDesc = layerDesc.getObjectValue(id("textKey"));
  var text = textDesc.getString(id("textKey"));
  var ranges = textDesc.getList(id("textStyleRange"));
  for (var i = 0; i < ranges.count; i++) {
    var r = ranges.getObjectValue(i);
    var from = r.getInteger(id("from"));
    var to = r.getInteger(id("to"));
    var st = r.getObjectValue(id("textStyle"));
    rows.push({
      from: from,
      to: to,
      text: text.substring(from, to),
      fontPostScriptName: strFromStyle(st, "fontPostScriptName"),
      fontName: strFromStyle(st, "fontName"),
      fontStyleName: strFromStyle(st, "fontStyleName"),
      size: numFromStyle(st, "size"),
      leading: numFromStyle(st, "leading"),
      color: colorFromStyle(st)
    });
  }
  return { text: text, ranges: rows };
}

var targetNames = [
  "@PART1_DIALOGUE_ROLE_MAP_TEXT",
  "@PART1_DIALOGUE_SAMPLE_LINE_TEXT",
  "@PART1_DIALOGUE_INTRO_TEXT",
  "@PART1_READING_LEFT_TEXT_STYLE_SOURCE",
  "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE"
];

var doc = app.open(new File(PSD));
var result = [];
for (var i = 0; i < targetNames.length; i++) {
  var layer = findLayer(doc, targetNames[i]);
  if (!layer) {
    result.push({ name: targetNames[i], missing: true });
  } else {
    try {
      var info = getTextStyleRanges(layer);
      result.push({ name: targetNames[i], missing: false, text: info.text, ranges: info.ranges });
    } catch (e) {
      result.push({ name: targetNames[i], missing: false, error: e.message });
    }
  }
}
doc.close(SaveOptions.DONOTSAVECHANGES);

var f = new File(OUT);
f.encoding = "UTF-8";
f.open("w");
f.write("[\n");
for (var j = 0; j < result.length; j++) {
  var item = result[j];
  f.write('  {"name":"' + esc(item.name) + '","missing":' + (item.missing ? "true" : "false"));
  if (item.error) f.write(',"error":"' + esc(item.error) + '"');
  if (item.text !== undefined) f.write(',"text":"' + esc(item.text) + '"');
  if (item.ranges) {
    f.write(',"ranges":[');
    for (var k = 0; k < item.ranges.length; k++) {
      var r = item.ranges[k];
      f.write('{"from":' + r.from + ',"to":' + r.to + ',"text":"' + esc(r.text) +
        '","fontPostScriptName":"' + esc(r.fontPostScriptName) +
        '","fontName":"' + esc(r.fontName) +
        '","fontStyleName":"' + esc(r.fontStyleName) +
        '","size":' + (r.size === null ? "null" : r.size) +
        ',"leading":' + (r.leading === null ? "null" : r.leading) +
        ',"color":"' + esc(r.color) + '"}');
      if (k < item.ranges.length - 1) f.write(",");
    }
    f.write(']');
  }
  f.write("}");
  if (j < result.length - 1) f.write(",");
  f.write("\n");
}
f.write("]\n");
f.close();

