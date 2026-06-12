#target photoshop
app.displayDialogs = DialogModes.NO;

var ROOT = "C:/Users/Administrator/Desktop/涓骇缇庤";
var OUT = "D:/Documents/New project/probes/probe_psd_reading_paragraph_style.json";
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

function unitValue(desc, key) {
  try { return desc.getUnitDoubleValue(id(key)); } catch (e) {}
  try { return desc.getDouble(id(key)); } catch (e2) {}
  return null;
}

function paragraphStyleRanges(layer) {
  var rows = [];
  var ref = new ActionReference();
  ref.putIdentifier(charIDToTypeID("Lyr "), layer.id);
  var layerDesc = executeActionGet(ref);
  var textDesc = layerDesc.getObjectValue(id("textKey"));
  var text = textDesc.getString(id("textKey"));
  var ranges = textDesc.getList(id("paragraphStyleRange"));
  for (var i = 0; i < ranges.count; i++) {
    var r = ranges.getObjectValue(i);
    var style = r.getObjectValue(id("paragraphStyle"));
    rows.push({
      from: r.getInteger(id("from")),
      to: r.getInteger(id("to")),
      text: text.substring(r.getInteger(id("from")), r.getInteger(id("to"))),
      firstLineIndent: unitValue(style, "firstLineIndent"),
      startIndent: unitValue(style, "startIndent"),
      endIndent: unitValue(style, "endIndent"),
      spaceBefore: unitValue(style, "spaceBefore"),
      spaceAfter: unitValue(style, "spaceAfter")
    });
  }
  return rows;
}

var doc = app.open(new File(PSD));
var names = ["@PART1_READING_LEFT_TEXT_STYLE_SOURCE", "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE"];
var result = [];
for (var i = 0; i < names.length; i++) {
  var layer = findLayer(doc, names[i]);
  if (!layer) {
    result.push({ name: names[i], missing: true });
  } else {
    try {
      result.push({ name: names[i], missing: false, ranges: paragraphStyleRanges(layer) });
    } catch (e) {
      result.push({ name: names[i], missing: false, error: e.message });
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
  if (item.ranges) {
    f.write(',"ranges":[');
    for (var k = 0; k < item.ranges.length; k++) {
      var r = item.ranges[k];
      f.write('{"from":' + r.from + ',"to":' + r.to + ',"text":"' + esc(r.text) + '"' +
        ',"firstLineIndent":' + (r.firstLineIndent === null ? "null" : r.firstLineIndent) +
        ',"startIndent":' + (r.startIndent === null ? "null" : r.startIndent) +
        ',"endIndent":' + (r.endIndent === null ? "null" : r.endIndent) +
        ',"spaceBefore":' + (r.spaceBefore === null ? "null" : r.spaceBefore) +
        ',"spaceAfter":' + (r.spaceAfter === null ? "null" : r.spaceAfter) + '}');
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

