from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


DOCX_PATH = Path(r"D:\Documents\New project\intermediate_source.docx")
OUT_JSON = Path(r"C:\Users\Administrator\Desktop\中级美语\data\docx_analysis.json")
OUT_TXT = Path(r"C:\Users\Administrator\Desktop\中级美语\data\docx_text.txt")

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}

CIRCLED = [
    "①",
    "②",
    "③",
    "④",
    "⑤",
    "⑥",
    "⑦",
    "⑧",
    "⑨",
    "⑩",
    "⑪",
    "⑫",
    "⑬",
    "⑭",
    "⑮",
    "⑯",
    "⑰",
    "⑱",
    "⑲",
    "⑳",
]


def val(node: ET.Element | None, name: str = "val") -> str | None:
    if node is None:
        return None
    return node.attrib.get(f"{{{NS['w']}}}{name}")


def text_of(node: ET.Element) -> str:
    parts: list[str] = []
    for child in node.iter():
        if child.tag == f"{{{NS['w']}}}t":
            parts.append(child.text or "")
        elif child.tag == f"{{{NS['w']}}}tab":
            parts.append("\t")
        elif child.tag == f"{{{NS['w']}}}br":
            parts.append("\n")
    return "".join(parts)


def normalize_text(s: str) -> str:
    s = s.replace("\u3000", " ")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


def load_numbering(zf: zipfile.ZipFile) -> dict[str, dict[str, dict[str, str | None]]]:
    try:
        xml = zf.read("word/numbering.xml")
    except KeyError:
        return {}
    root = ET.fromstring(xml)
    abstract_levels: dict[str, dict[str, dict[str, str | None]]] = {}
    for abstract in root.findall("w:abstractNum", NS):
        abstract_id = val(abstract, "abstractNumId")
        if abstract_id is None:
            continue
        levels: dict[str, dict[str, str | None]] = {}
        for lvl in abstract.findall("w:lvl", NS):
            ilvl = val(lvl, "ilvl") or "0"
            levels[ilvl] = {
                "format": val(lvl.find("w:numFmt", NS)),
                "text": val(lvl.find("w:lvlText", NS)),
                "start": val(lvl.find("w:start", NS)) or "1",
            }
        abstract_levels[abstract_id] = levels

    num_to_levels: dict[str, dict[str, dict[str, str | None]]] = {}
    for num in root.findall("w:num", NS):
        num_id = val(num, "numId")
        abstract_id = val(num.find("w:abstractNumId", NS))
        if num_id and abstract_id:
            num_to_levels[num_id] = abstract_levels.get(abstract_id, {})
    return num_to_levels


def render_number(fmt: str | None, lvl_text: str | None, number: int) -> str:
    if fmt == "decimalEnclosedCircleChinese":
        rendered = CIRCLED[number - 1] if 1 <= number <= len(CIRCLED) else str(number)
    else:
        rendered = str(number)
    if lvl_text:
        return lvl_text.replace("%1", rendered).strip()
    return rendered


def paragraph_info(p: ET.Element, num_to_levels: dict[str, dict[str, dict[str, str | None]]], counters: dict[tuple[str, str], int]) -> dict:
    ppr = p.find("w:pPr", NS)
    style = None
    num_id = None
    ilvl = None
    jc = None
    numbering_label = None
    if ppr is not None:
        style = val(ppr.find("w:pStyle", NS))
        num_pr = ppr.find("w:numPr", NS)
        if num_pr is not None:
            num_id = val(num_pr.find("w:numId", NS))
            ilvl = val(num_pr.find("w:ilvl", NS)) or "0"
        jc = val(ppr.find("w:jc", NS))

    if num_id is not None:
        level = num_to_levels.get(num_id, {}).get(ilvl or "0", {})
        key = (num_id, ilvl or "0")
        if key not in counters:
            try:
                counters[key] = int(level.get("start") or "1")
            except ValueError:
                counters[key] = 1
        else:
            counters[key] += 1
        numbering_label = render_number(level.get("format"), level.get("text"), counters[key])

    run_styles: list[dict] = []
    for r in p.findall("w:r", NS):
        rpr = r.find("w:rPr", NS)
        font = None
        size = None
        bold = False
        italic = False
        color = None
        highlight = None
        if rpr is not None:
            rfonts = rpr.find("w:rFonts", NS)
            if rfonts is not None:
                font = (
                    rfonts.attrib.get(f"{{{NS['w']}}}ascii")
                    or rfonts.attrib.get(f"{{{NS['w']}}}eastAsia")
                    or rfonts.attrib.get(f"{{{NS['w']}}}hAnsi")
                )
            size = val(rpr.find("w:sz", NS))
            bold = rpr.find("w:b", NS) is not None
            italic = rpr.find("w:i", NS) is not None
            color = val(rpr.find("w:color", NS))
            highlight = val(rpr.find("w:highlight", NS))
        rt = text_of(r)
        if rt:
            run_styles.append(
                {
                    "text": rt,
                    "font": font,
                    "sizeHalfPoints": size,
                    "bold": bold,
                    "italic": italic,
                    "color": color,
                    "highlight": highlight,
                }
            )

    text = text_of(p)
    display_text = f"{numbering_label} {text}" if numbering_label else text
    return {
        "type": "paragraph",
        "text": text,
        "displayText": display_text,
        "numberingLabel": numbering_label,
        "style": style,
        "numId": num_id,
        "ilvl": ilvl,
        "justification": jc,
        "runs": run_styles,
    }


def table_info(tbl: ET.Element, num_to_levels: dict[str, dict[str, dict[str, str | None]]], counters: dict[tuple[str, str], int]) -> dict:
    rows = []
    for tr in tbl.findall("w:tr", NS):
        row = []
        for tc in tr.findall("w:tc", NS):
            cell_paras = [paragraph_info(p, num_to_levels, counters)["displayText"] for p in tc.findall("w:p", NS)]
            row.append("\n".join([p for p in cell_paras if p]))
        rows.append(row)
    return {"type": "table", "rows": rows}


def iter_body_items(root: ET.Element, num_to_levels: dict[str, dict[str, dict[str, str | None]]]) -> list[dict]:
    body = root.find("w:body", NS)
    if body is None:
        return []
    items = []
    counters: dict[tuple[str, str], int] = {}
    for child in body:
        if child.tag == f"{{{NS['w']}}}p":
            info = paragraph_info(child, num_to_levels, counters)
            if info["text"].strip():
                items.append(info)
        elif child.tag == f"{{{NS['w']}}}tbl":
            items.append(table_info(child, num_to_levels, counters))
    return items


def analyze_docx(docx_path: Path, out_json: Path, out_txt: Path) -> None:
    with zipfile.ZipFile(docx_path) as zf:
        num_to_levels = load_numbering(zf)
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    items = iter_body_items(root, num_to_levels)

    plain_lines: list[str] = []
    for idx, item in enumerate(items, start=1):
        if item["type"] == "paragraph":
            plain_lines.append(f"{idx:04d}\t{normalize_text(item.get('displayText') or item['text'])}")
        else:
            plain_lines.append(f"{idx:04d}\t[TABLE]")
            for row in item["rows"]:
                plain_lines.append("\t" + " | ".join(normalize_text(c) for c in row))

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    out_txt.write_text("\n".join(plain_lines), encoding="utf-8")
    print(f"items={len(items)}")
    print(f"json={out_json}")
    print(f"text={out_txt}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze DOCX paragraphs/runs into JSON with Word numbering labels.")
    parser.add_argument("--docx", type=Path, default=DOCX_PATH)
    parser.add_argument("--out-json", type=Path, default=OUT_JSON)
    parser.add_argument("--out-text", type=Path, default=OUT_TXT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    analyze_docx(args.docx, args.out_json, args.out_text)


if __name__ == "__main__":
    main()
