#target photoshop
app.displayDialogs = DialogModes.NO;

var ROOT = "C:/Users/Administrator/Desktop/涓骇缇庤";
var OUT = "D:/Documents/New project/probes/probe_psd_phonetic_metrics.json";
var PSD = ROOT + "/3-4 1.psd";

function esc(s) {
  if (s === undefined || s === null) return "";
  return String(s).replace(/\\/g, "\\\\").replace(/"/g, '\\"').replace(/\r/g, "\\r").replace(/\n/g, "\\n");
}

function boundsArray(layer) {
  try {
    var b = layer.bounds;
    return [b[0].as("px"), b[1].as("px"), b[2].as("px"), b[3].as("px")];
  } catch (e) {
    return null;
  }
}

function textLeading(layer) {
  try {
    return layer.textItem.leading.as("px");
  } catch (e) {
    return null;
  }
}

function textSize(layer) {
  try {
    return layer.textItem.size.as("px");
  } catch (e) {
    return null;
  }
}

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

function unlockLayer(layer) {
  try { layer.allLocked = false; } catch (e) {}
  try { layer.pixelsLocked = false; } catch (e) {}
  try { layer.positionLocked = false; } catch (e) {}
  try { layer.transparentPixelsLocked = false; } catch (e) {}
}

function measureDuplicate(doc, source, name, contents) {
  var layer = source.duplicate();
  layer.name = name;
  unlockLayer(layer);
  layer.visible = true;
  doc.activeLayer = layer;
  layer.textItem.contents = contents;
  var row = {
    name: name,
    text: contents,
    font: layer.textItem.font,
    size: textSize(layer),
    leading: textLeading(layer),
    bounds: boundsArray(layer)
  };
  layer.remove();
  return row;
}

var doc = app.open(new File(PSD));
var phoneticSource = findLayer(doc, "@PART1_READING_LEFT_TEXT_STYLE_SOURCE");
var bodySource = findLayer(doc, "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE");
var rows = [];
rows.push(measureDuplicate(doc, phoneticSource, "@MEASURE_PHONETIC_ONLY", "[ha瑟]"));
rows.push(measureDuplicate(doc, bodySource, "@MEASURE_BODY_ONLY", "M: Hi, Don! How are you doing in your English class."));
rows.push(measureDuplicate(doc, phoneticSource, "@MEASURE_PHONETIC_BODY_PAIR", "[ha瑟]\rM: Hi, Don! How are you doing in your English class."));
rows.push(measureDuplicate(doc, bodySource, "@MEASURE_BODY_PAIR", "[ha瑟]\rM: Hi, Don! How are you doing in your English class."));
doc.close(SaveOptions.DONOTSAVECHANGES);

var f = new File(OUT);
f.encoding = "UTF-8";
f.open("w");
f.write("[\n");
for (var i = 0; i < rows.length; i++) {
  var r = rows[i];
  f.write('  {"name":"' + esc(r.name) + '","text":"' + esc(r.text) + '","font":"' + esc(r.font) +
    '","size":' + (r.size === null ? "null" : r.size) + ',"leading":' + (r.leading === null ? "null" : r.leading) +
    ',"bounds":' + (r.bounds ? "[" + r.bounds.join(",") + "]" : "null") + "}");
  if (i < rows.length - 1) f.write(",");
  f.write("\n");
}
f.write("]\n");
f.close();

