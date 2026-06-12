#target photoshop
app.displayDialogs = DialogModes.NO;

var ROOT = "C:/Users/Administrator/Desktop/涓骇缇庤";
var OUT = "D:/Documents/New project/probes/probe_psd_reading_layers.json";
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
  try { return layer.textItem.size.as("px"); } catch (e) { return null; }
}

function textLeading(layer) {
  try { return layer.textItem.leading.as("px"); } catch (e) { return null; }
}

function kindName(layer) {
  try {
    if (layer.typename === "LayerSet") return "LayerSet";
    if (layer.kind === LayerKind.TEXT) return "TEXT";
    if (layer.kind === LayerKind.SOLIDFILL) return "SOLIDFILL";
    return String(layer.kind);
  } catch (e) {
    return "";
  }
}

function walk(container, rows, path) {
  for (var i = 0; i < container.layers.length; i++) {
    var layer = container.layers[i];
    var itemPath = path ? path + "/" + layer.name : layer.name;
    if (layer.name.indexOf("@PART1_READING") >= 0 || itemPath.indexOf("@PART1_READING") >= 0) {
      var row = {
        name: layer.name,
        path: itemPath,
        typename: layer.typename,
        kind: kindName(layer),
        visible: layer.visible,
        bounds: boundsArray(layer)
      };
      if (layer.typename !== "LayerSet" && layer.kind === LayerKind.TEXT) {
        row.text = layer.textItem.contents;
        row.font = layer.textItem.font;
        row.size = textSize(layer);
        row.leading = textLeading(layer);
        row.color = textColorHex(layer);
      }
      rows.push(row);
    }
    if (layer.typename === "LayerSet") walk(layer, rows, itemPath);
  }
}

var doc = app.open(new File(PSD));
var rows = [];
walk(doc, rows, "");
doc.close(SaveOptions.DONOTSAVECHANGES);

var f = new File(OUT);
f.encoding = "UTF-8";
f.open("w");
f.write("[\n");
for (var i = 0; i < rows.length; i++) {
  var r = rows[i];
  f.write("  {");
  var first = true;
  for (var k in r) {
    if (!first) f.write(",");
    first = false;
    if (k === "bounds") {
      f.write('"' + k + '":' + (r[k] ? "[" + r[k].join(",") + "]" : "null"));
    } else if (typeof r[k] === "number") {
      f.write('"' + k + '":' + r[k]);
    } else if (typeof r[k] === "boolean") {
      f.write('"' + k + '":' + (r[k] ? "true" : "false"));
    } else {
      f.write('"' + k + '":"' + esc(r[k]) + '"');
    }
  }
  f.write("}");
  if (i < rows.length - 1) f.write(",");
  f.write("\n");
}
f.write("]\n");
f.close();

