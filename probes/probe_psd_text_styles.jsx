#target photoshop
app.displayDialogs = DialogModes.NO;

var ROOT = "C:/Users/Administrator/Desktop/涓骇缇庤";
var OUT = "D:/Documents/New project/probes/probe_psd_text_styles.json";
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

function textColorHex(layer) {
  try {
    var c = layer.textItem.color.rgb;
    function h(v) {
      var s = Math.round(v).toString(16).toUpperCase();
      return s.length < 2 ? "0" + s : s;
    }
    return h(c.red) + h(c.green) + h(c.blue);
  } catch (e) {
    return "";
  }
}

function textSize(layer) {
  try {
    return layer.textItem.size.as("px");
  } catch (e) {
    return null;
  }
}

function walk(container, rows) {
  for (var i = 0; i < container.layers.length; i++) {
    var layer = container.layers[i];
    if (layer.typename === "LayerSet") {
      walk(layer, rows);
    } else if (layer.kind === LayerKind.TEXT) {
      rows.push({
        name: layer.name,
        visible: layer.visible,
        text: layer.textItem.contents,
        font: layer.textItem.font,
        size: textSize(layer),
        color: textColorHex(layer),
        bounds: boundsArray(layer)
      });
    }
  }
}

var doc = app.open(new File(PSD));
var rows = [];
walk(doc, rows);
doc.close(SaveOptions.DONOTSAVECHANGES);

var f = new File(OUT);
f.encoding = "UTF-8";
f.open("w");
f.write("[\n");
for (var i = 0; i < rows.length; i++) {
  var r = rows[i];
  f.write('  {"name":"' + esc(r.name) + '","visible":' + (r.visible ? "true" : "false") +
    ',"text":"' + esc(r.text) + '","font":"' + esc(r.font) + '","size":' + (r.size === null ? "null" : r.size) +
    ',"color":"' + esc(r.color) + '","bounds":' + (r.bounds ? "[" + r.bounds.join(",") + "]" : "null") + "}");
  if (i < rows.length - 1) f.write(",");
  f.write("\n");
}
f.write("]\n");
f.close();

