from __future__ import annotations

import json
import re
from pathlib import Path


ANALYSIS_JSON = Path(r"D:\Documents\New project\docx_analysis.json")
OUT_JSON = Path(r"D:\Documents\New project\docx_page_data.json")
OUT_TXT = Path(r"D:\Documents\New project\docx_page_data_preview.txt")

LESSON_RE = re.compile(r"^Lesson\s+(\d+)[–-](\d+)$")
SECTION_RE = re.compile(r"^[123]\.$")
CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩"


def clean(s: str) -> str:
    s = s.replace("\u3000", " ")
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    return re.sub(r"[ \t]+", " ", s).strip()


def clean_runs(runs: list[dict]) -> list[dict]:
    cleaned = []
    for run in runs:
        text = run.get("text", "")
        text = text.replace("\u3000", " ")
        text = text.replace("’", "'").replace("‘", "'")
        text = text.replace("“", '"').replace("”", '"')
        if not text:
            continue
        highlight = run.get("highlight")
        if highlight == "none":
            highlight = None
        cleaned.append(
            {
                "text": text,
                "highlight": highlight,
                "color": run.get("color"),
            }
        )
    return cleaned


def plain_runs(text: str) -> list[dict]:
    return [{"text": text, "highlight": None, "color": None}] if text else []


def concat_runs(prefix: str, runs: list[dict]) -> list[dict]:
    out = plain_runs(prefix)
    out.extend(runs)
    return out


def runs_text(runs: list[dict]) -> str:
    return "".join(run.get("text", "") for run in runs)


def spaced_circled(s: str) -> str:
    chars = [ch for ch in s if ch.strip()]
    if all(ch in CIRCLED for ch in chars):
        return "  ".join(chars)
    return s


def numbered_lines(lines: list[str], start: int = 1) -> list[str]:
    out = []
    for i, line in enumerate(lines, start=start):
        prefix = CIRCLED[i - 1] if i <= len(CIRCLED) else f"{i}."
        out.append(f"{prefix} {line}")
    return out


def split_lessons(lines: list[str]) -> list[dict]:
    lessons: list[dict] = []
    current: dict | None = None

    for line in lines:
        match = LESSON_RE.match(line)
        if match:
            if current:
                lessons.append(current)
            current = {
                "lesson": f"Lesson {match.group(1)}-{match.group(2)}",
                "start": int(match.group(1)),
                "end": int(match.group(2)),
                "lines": [],
            }
            continue
        if current:
            current["lines"].append(line)

    if current:
        lessons.append(current)
    return lessons


def split_lesson_items(items: list[dict]) -> list[dict]:
    lessons: list[dict] = []
    current: dict | None = None
    for item in items:
        if item.get("type") != "paragraph":
            continue
        text = clean(item.get("text", ""))
        if not text:
            continue
        match = LESSON_RE.match(text)
        if match:
            if current:
                lessons.append(current)
            current = {
                "lesson": f"Lesson {match.group(1)}-{match.group(2)}",
                "start": int(match.group(1)),
                "end": int(match.group(2)),
                "items": [],
            }
            continue
        if current:
            current["items"].append(
                {
                    "text": text,
                    "runs": clean_runs(item.get("runs", [])) or plain_runs(text),
                }
            )
    if current:
        lessons.append(current)
    return lessons


def parse_sections(lines: list[str]) -> dict[str, list[str]]:
    sections = {"1": [], "2": [], "3": []}
    active: str | None = None
    for line in lines:
        if SECTION_RE.match(line):
            active = line[0]
            continue
        if active is None and not sections["1"]:
            sections["1"].append(line)
            if all(ch in CIRCLED for ch in line if ch.strip()):
                active = "2"
            continue
        if active:
            sections[active].append(line)
    return sections


def parse_rich_sections(items: list[dict]) -> dict[str, list[dict]]:
    sections: dict[str, list[dict]] = {"1": [], "2": [], "3": []}
    active: str | None = None
    for item in items:
        line = item["text"]
        if SECTION_RE.match(line):
            active = line[0]
            continue
        if active is None and not sections["1"]:
            sections["1"].append(item)
            if all(ch in CIRCLED for ch in line if ch.strip()):
                active = "2"
            continue
        if active:
            sections[active].append(item)
    return sections


def format_block(lesson: dict) -> dict:
    sections = parse_sections(lesson["lines"])
    answer_1 = ""
    if sections["1"]:
        answer_1 = "1. " + spaced_circled(sections["1"][0])

    answer_2_lines = numbered_lines(sections["2"])
    answer_2 = ""
    if answer_2_lines:
        answer_2 = "2. " + answer_2_lines[0]
        if len(answer_2_lines) > 1:
            answer_2 += "\r" + "\r".join("     " + line for line in answer_2_lines[1:])

    answer_3 = ""
    if sections["3"]:
        answer_3 = "3. " + sections["3"][0]
        if len(sections["3"]) > 1:
            answer_3 += "\r" + "\r".join("     " + line for line in sections["3"][1:])

    return {
        "lesson": lesson["lesson"],
        "part": "Part 4",
        "answer_1": answer_1,
        "answer_2": answer_2,
        "answer_3": answer_3,
        "raw_sections": sections,
    }


def format_rich_block(lesson: dict) -> dict:
    sections = parse_rich_sections(lesson["items"])
    rich_lines: list[dict] = []

    if sections["1"]:
        answer = spaced_circled(sections["1"][0]["text"])
        rich_lines.append({"runs": plain_runs("1. " + answer), "gapBefore": 0})

    if sections["2"]:
        for i, item in enumerate(sections["2"], start=1):
            prefix = ("2. " if i == 1 else "     ") + (CIRCLED[i - 1] + " " if i <= len(CIRCLED) else f"{i}. ")
            rich_lines.append(
                {
                    "runs": concat_runs(prefix, item["runs"]),
                    "gapBefore": 28 if rich_lines and i == 1 else 0,
                }
            )

    if sections["3"]:
        for i, item in enumerate(sections["3"]):
            prefix = "3. " if i == 0 else "     "
            rich_lines.append(
                {
                    "runs": concat_runs(prefix, item["runs"]),
                    "gapBefore": 28 if rich_lines and i == 0 else 0,
                }
            )

    return {
        "lesson": lesson["lesson"],
        "part": "Part 4",
        "rich_lines": rich_lines,
    }


def main() -> None:
    items = json.loads(ANALYSIS_JSON.read_text(encoding="utf-8"))
    lines = [clean(item["text"]) for item in items if item.get("type") == "paragraph" and clean(item.get("text", ""))]
    lessons = [format_block(block) for block in split_lessons(lines)]
    rich_lessons = [format_rich_block(block) for block in split_lesson_items(items)]

    for lesson, rich in zip(lessons, rich_lessons):
        lesson["rich_lines"] = rich["rich_lines"]

    pages = []
    for i in range(0, len(lessons), 2):
        page_number = f"{i // 2 + 1:03d}"
        pages.append(
            {
                "page_number": page_number,
                "top": lessons[i],
                "bottom": lessons[i + 1] if i + 1 < len(lessons) else None,
            }
        )

    OUT_JSON.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")

    preview = []
    for page in pages:
        preview.append(f"PAGE {page['page_number']}")
        for slot in ("top", "bottom"):
            block = page.get(slot)
            if not block:
                continue
            preview.append(f"[{slot}] {block['lesson']} {block['part']}")
            for key in ("answer_1", "answer_2", "answer_3"):
                if block[key]:
                    preview.append(block[key].replace("\r", "\n"))
            preview.append("")
    OUT_TXT.write_text("\n".join(preview), encoding="utf-8")
    print(f"lessons={len(lessons)} pages={len(pages)}")
    print(f"json={OUT_JSON}")
    print(f"preview={OUT_TXT}")


if __name__ == "__main__":
    main()
