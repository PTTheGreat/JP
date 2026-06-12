from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(r"C:\Users\Administrator\Desktop\中级美语")
ANALYSIS_JSON = ROOT / "data" / "docx_analysis.json"
OUT_JSON = ROOT / "data" / "lessons.json"
OUT_PREVIEW = ROOT / "data" / "lessons_preview.txt"
OUT_REPORT = ROOT / "data" / "lessons_parse_report.md"

LESSON_RE = re.compile(r"^Lesson\s+(\d+)\s*[-–]\s*(\d+)$")
PART_RE = re.compile(r"^Part\s*([1-4])\s*[:：]\s*(.+?)\s*$", re.I)
SPEAKER_RE = re.compile(r"^([A-Z]):\s*(.+)")
VOCAB_RE = re.compile(
    r"^(?P<word>.+?)\s+KK:\s*(?P<kk>\[[^\]]+\])\s+IPA:\s*(?P<ipa>\[[^\]]+\])\s*(?P<meaning>.*)$"
)
PHONETIC_LINE_RE = re.compile(r"^\s*(/[^\n/]+/\s*)+$")
EXERCISE_SECTION_RE = re.compile(r"^(\d+)\.\s*(.+)$")
CIRCLED_NUMBERS = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩"]


def normalize_text(text: str) -> str:
    text = text.replace("\u3000", " ")
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def normalize_run(run: dict[str, Any]) -> dict[str, Any]:
    return {
        "text": run.get("text", ""),
        "color": run.get("color"),
        "highlight": None if run.get("highlight") == "none" else run.get("highlight"),
        "italic": bool(run.get("italic")),
        "bold": bool(run.get("bold")),
    }


def paragraph_items() -> list[dict[str, Any]]:
    raw = json.loads(ANALYSIS_JSON.read_text(encoding="utf-8"))
    items: list[dict[str, Any]] = []
    for item in raw:
        if item.get("type") != "paragraph":
            continue
        text = normalize_text(item.get("text", ""))
        if not text:
            continue
        runs = [normalize_run(run) for run in item.get("runs", []) if run.get("text")]
        items.append(
            {
                "text": text,
                "displayText": normalize_text(item.get("displayText", "")) if item.get("displayText") else text,
                "numberingLabel": item.get("numberingLabel"),
                "rawText": item.get("text", ""),
                "runs": runs,
                "style": item.get("style"),
                "numId": item.get("numId"),
                "ilvl": item.get("ilvl"),
            }
        )
    return items


def split_lessons(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lessons: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for item in items:
        match = LESSON_RE.match(item["text"])
        if match:
            if current:
                lessons.append(current)
            current = {
                "lessonNo": f"Lesson {match.group(1)}-{match.group(2)}",
                "lessonStart": int(match.group(1)),
                "lessonEnd": int(match.group(2)),
                "items": [],
            }
            continue
        if current:
            current["items"].append(item)
    if current:
        lessons.append(current)
    return lessons


def split_parts(items: list[dict[str, Any]]) -> tuple[str, str, dict[str, list[dict[str, Any]]]]:
    first_part_idx = next((i for i, item in enumerate(items) if PART_RE.match(item["text"])), len(items))
    title_items = items[:first_part_idx]
    lesson_title_phonetic = " ".join(convert_phonetic(item["text"]) for item in title_items if is_phonetic(item["text"]))
    title_candidates = [item["text"] for item in title_items if not is_phonetic(item["text"])]
    title = title_candidates[-1] if title_candidates else ""
    parts = {"1": [], "2": [], "3": [], "4": []}
    active: str | None = None
    for item in items[first_part_idx:]:
        match = PART_RE.match(item["text"])
        if match:
            active = match.group(1)
            parts[active].append({"partTitle": match.group(2), **item})
            continue
        if active:
            parts[active].append(item)
    return title, lesson_title_phonetic, parts


def is_phonetic(text: str) -> bool:
    return bool(PHONETIC_LINE_RE.match(text))


def convert_phonetic(text: str) -> str:
    return re.sub(r"/([^/]+?)/", lambda m: "[" + m.group(1).strip() + "]", text)


def parse_part1(items: list[dict[str, Any]]) -> dict[str, Any]:
    body = [item for item in items if "partTitle" not in item]
    first_speaker = next((i for i, item in enumerate(body) if SPEAKER_RE.match(item["text"])), len(body))

    intro_idx = None
    role_idx = None
    for i in range(first_speaker - 1, -1, -1):
        text = body[i]["text"]
        if re.match(r"^\(.+=.+\)$", text):
            role_idx = i
            continue
        if not is_phonetic(text):
            intro_idx = i
            break

    reading_end = intro_idx if intro_idx is not None else first_speaker
    reading: list[dict[str, str]] = []
    pending_phonetic: list[str] = []
    for item in body[:reading_end]:
        text = item["text"]
        if is_phonetic(text):
            pending_phonetic.append(convert_phonetic(text))
        else:
            reading.append(
                {
                    "phonetic": " ".join(pending_phonetic),
                    "text": text,
                }
            )
            pending_phonetic = []

    dialogue_start = intro_idx + 1 if intro_idx is not None else first_speaker
    dialogue: list[dict[str, Any]] = []
    pending_phonetic = []
    for item in body[dialogue_start:]:
        text = item["text"]
        if role_idx is not None and body.index(item) == role_idx:
            continue
        if is_phonetic(text):
            pending_phonetic.append(convert_phonetic(text))
            continue
        match = SPEAKER_RE.match(text)
        if match:
            dialogue.append(
                {
                    "speaker": match.group(1),
                    "text": match.group(2).strip(),
                    "phonetic": " ".join(pending_phonetic),
                }
            )
            pending_phonetic = []
        elif text:
            dialogue.append(
                {
                    "speaker": None,
                    "text": text,
                    "phonetic": " ".join(pending_phonetic),
                }
            )
            pending_phonetic = []

    return {
        "title": "Reading&Dialogue",
        "reading": reading,
        "dialogueIntro": body[intro_idx]["text"] if intro_idx is not None else "",
        "dialogueRoleNote": body[role_idx]["text"] if role_idx is not None else "",
        "dialogue": dialogue,
    }


def parse_part2(items: list[dict[str, Any]]) -> dict[str, Any]:
    body = [item for item in items if "partTitle" not in item]
    vocab_items = []
    for index, item in enumerate(body, start=1):
        text = item["text"]
        match = VOCAB_RE.match(text)
        if match:
            vocab_items.append(
                {
                    "no": str(index),
                    "word": match.group("word").strip(),
                    "kk": "KK: " + match.group("kk").strip(),
                    "ipa": "IPA: " + match.group("ipa").strip(),
                    "meaning": match.group("meaning").strip(),
                    "raw": text,
                }
            )
        else:
            vocab_items.append({"no": str(index), "word": text, "kk": "", "ipa": "", "meaning": "", "raw": text})
    return {"title": "Vocabulary&Idioms", "items": vocab_items}


def paragraph_has_orange(item: dict[str, Any]) -> bool:
    for run in item.get("runs", []):
        color = (run.get("color") or "").upper()
        if color and color not in {"000000", "AUTO"}:
            return True
    return False


def parse_part3(items: list[dict[str, Any]]) -> dict[str, Any]:
    body = [item for item in items if "partTitle" not in item]
    lead = body[0]["text"] if body else ""
    lead_is_orange = paragraph_has_orange(body[0]) if body else False
    blocks = []
    for item in body[1:]:
        text = item["text"]
        block_type = "paragraph"
        if re.match(r"^[①②③④⑤⑥⑦⑧⑨⑩]", text):
            block_type = "numberedExample"
        elif "→" in text or text.startswith("->"):
            block_type = "transformExample"
        elif re.match(r"^\d+\.\s*", text):
            block_type = "sectionTitle"
        blocks.append({"type": block_type, "text": text, "runs": item.get("runs", [])})
    return {
        "title": "Grammar points",
        "leadSentence": lead,
        "leadStyle": "orangeItalic" if lead_is_orange else "templateLead",
        "blocks": blocks,
    }


def parse_part4(items: list[dict[str, Any]]) -> dict[str, Any]:
    body = [item for item in items if "partTitle" not in item]
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    item_index = 0
    for item in body:
        match = EXERCISE_SECTION_RE.match(item["text"])
        if match:
            current = {"sectionNo": match.group(1) + ".", "title": match.group(2).strip(), "items": []}
            sections.append(current)
            item_index = 0
            continue
        if current is None:
            current = {"sectionNo": "", "title": "", "items": []}
            sections.append(current)
        item_index += 1
        item_no = item.get("numberingLabel") or (
            CIRCLED_NUMBERS[item_index - 1] if item_index <= len(CIRCLED_NUMBERS) else f"{item_index}."
        )
        text = item["text"]
        display_text = item.get("displayText") or text
        if display_text == text and text[:1] not in CIRCLED_NUMBERS:
            display_text = f"{item_no} {text}"
        current["items"].append(
            {
                "itemNo": item_no,
                "text": text,
                "displayText": display_text,
                "answerLines": 1 if current.get("title") == "翻译" else 0,
                "runs": item.get("runs", []),
            }
        )
    return {"title": "Exercise", "sections": sections}


def build_lessons() -> list[dict[str, Any]]:
    lessons = []
    for raw_lesson in split_lessons(paragraph_items()):
        lesson_title, lesson_title_phonetic, parts = split_parts(raw_lesson["items"])
        lessons.append(
            {
                "lessonNo": raw_lesson["lessonNo"],
                "lessonStart": raw_lesson["lessonStart"],
                "lessonEnd": raw_lesson["lessonEnd"],
                "lessonTitle": lesson_title,
                "lessonTitlePhonetic": lesson_title_phonetic,
                "part1": parse_part1(parts["1"]),
                "part2": parse_part2(parts["2"]),
                "part3": parse_part3(parts["3"]),
                "part4": parse_part4(parts["4"]),
            }
        )
    return lessons


def write_outputs(lessons: list[dict[str, Any]]) -> None:
    OUT_JSON.write_text(json.dumps({"lessons": lessons}, ensure_ascii=False, indent=2), encoding="utf-8")

    preview: list[str] = []
    for lesson in lessons:
        preview.append(f"{lesson['lessonNo']} | {lesson['lessonTitle']}")
        preview.append(
            "  counts: "
            f"reading={len(lesson['part1']['reading'])}, "
            f"dialogue={len(lesson['part1']['dialogue'])}, "
            f"vocab={len(lesson['part2']['items'])}, "
            f"grammarBlocks={len(lesson['part3']['blocks'])}, "
            f"exerciseSections={len(lesson['part4']['sections'])}"
        )
        preview.append("")
    OUT_PREVIEW.write_text("\n".join(preview), encoding="utf-8")

    issues: list[str] = []
    for lesson in lessons:
        if not lesson["lessonTitle"]:
            issues.append(f"- {lesson['lessonNo']} 缺少 Lesson 英文标题")
        for part_name in ("part1", "part2", "part3", "part4"):
            if not lesson.get(part_name):
                issues.append(f"- {lesson['lessonNo']} 缺少 {part_name}")
        if not lesson["part2"]["items"]:
            issues.append(f"- {lesson['lessonNo']} Part2 没有解析到词汇")
        if not lesson["part4"]["sections"]:
            issues.append(f"- {lesson['lessonNo']} Part4 没有解析到练习小节")

    report = [
        "# Word 结构化解析报告",
        "",
        f"- 输入：`{ANALYSIS_JSON}`",
        f"- 输出：`{OUT_JSON}`",
        f"- Lesson 数量：{len(lessons)}",
        f"- Part1 数量：{sum(1 for l in lessons if l.get('part1'))}",
        f"- Part2 数量：{sum(1 for l in lessons if l.get('part2'))}",
        f"- Part3 数量：{sum(1 for l in lessons if l.get('part3'))}",
        f"- Part4 数量：{sum(1 for l in lessons if l.get('part4'))}",
        "",
        "## 可能问题",
        "",
    ]
    report.extend(issues or ["- 未发现阻断性结构问题。"])
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    lessons = build_lessons()
    write_outputs(lessons)
    print(f"lessons={len(lessons)}")
    print(OUT_JSON)
    print(OUT_PREVIEW)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()
