from __future__ import annotations

import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(r"C:\Users\Administrator\Desktop\中级美语")
MANIFEST = ROOT / "PSD_layer_rename_SAFE_JSX_scripts_最终MD同步版" / "PSD_layer_rename_manifest.json"
DOCX = ROOT / "6.6排版用-中上综合语法辅导书.docx"


def docx_text(path: Path) -> str:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    lines: list[str] = []
    for p in root.findall(".//w:p", ns):
        text = "".join(t.text or "" for t in p.findall(".//w:t", ns)).strip()
        if text:
            lines.append(text)
    return "\n".join(lines)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    print("manifest_files", len(manifest))
    for psd_name, rows in manifest.items():
        names = [row["new"] for row in rows]
        dup = [name for name, count in Counter(names).items() if count > 1]
        print(psd_name, "layers", len(rows), "unique", len(set(names)), "duplicates", len(dup))
        if dup[:10]:
            print("  dup_sample", dup[:10])

    text = docx_text(DOCX)
    lessons = re.findall(r"(?m)^Lesson\s+\d+\s*[-–]\s*\d+\s*$", text)
    print("docx_lesson_count", len(lessons))
    print("docx_lesson_first_5", lessons[:5])
    print("docx_lesson_last_5", lessons[-5:])
    part_counts = {
        "Part 1": len(re.findall(r"(?m)^Part\s*1[:：]", text)),
        "Part 2": len(re.findall(r"(?m)^Part\s*2[:：]", text)),
        "Part 3": len(re.findall(r"(?m)^Part\s*3[:：]", text)),
        "Part 4": len(re.findall(r"(?m)^Part\s*4[:：]", text)),
    }
    print("docx_part_counts", part_counts)

    for psd in sorted(ROOT.glob("3-4 *.psd")):
        data = psd.read_bytes()
        marker_count = data.count(b"@SHELL") + data.count(b"@PART") + data.count(b"@PAGE") + data.count(b"@LESSON")
        print("psd_marker_bytes", psd.name, marker_count)


if __name__ == "__main__":
    main()
