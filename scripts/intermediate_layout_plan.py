from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(r"C:\Users\Administrator\Desktop\中级美语")
WORK = Path(r"D:\Documents\New project")
LESSONS_JSON = WORK / "intermediate_lessons.json"
MANIFEST_JSON = WORK / "intermediate_manifest.json"
OUT_JSON = ROOT / "data" / "lesson_1_2_layout_plan.json"
OUT_REPORT = ROOT / "data" / "lesson_1_2_layout_plan_report.md"


FIRST_TEMPLATE = "3-4 1.psd"
CONT_TEMPLATE = "3-4 2.psd"
GRAMMAR_CONT_TEMPLATE = "3-4 3.psd"
GRAMMAR_EXERCISE_TEMPLATE = "3-4 4.psd"
EXERCISE_CONT_TEMPLATE = "3-4 5.psd"

HIDDEN_REFERENCE_LAYERS = [
    "@SHELL_CONTENT_PANEL_DECOR_SHAPE",
    "@SHELL_CONTENT_PANEL_LEFT",
    "@SHELL_CONTENT_PANEL_RIGHT",
    "@SHELL_PANEL_CORNER_DECOR_RIGHT",
    "@SHELL_PANEL_CORNER_DECOR_LEFT",
]


@dataclass(frozen=True)
class Rect:
    top: int
    left: int
    bottom: int
    right: int

    @classmethod
    def from_list(cls, raw: list[int]) -> "Rect":
        return cls(top=raw[0], left=raw[1], bottom=raw[2], right=raw[3])

    def to_json(self) -> dict[str, int]:
        return {"top": self.top, "left": self.left, "bottom": self.bottom, "right": self.right}


def load_lesson() -> dict[str, Any]:
    lessons = json.loads(LESSONS_JSON.read_text(encoding="utf-8"))["lessons"]
    for lesson in lessons:
        if lesson["lessonNo"] == "Lesson 1-2":
            return lesson
    raise RuntimeError("Lesson 1-2 not found")


def load_manifest() -> dict[str, dict[str, dict[str, Any]]]:
    raw = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    by_template: dict[str, dict[str, dict[str, Any]]] = {}
    for template, items in raw.items():
        by_template[template] = {item["new"]: item for item in items}
    return by_template


def manifest_key(template_name: str) -> str:
    mapping = {
        FIRST_TEMPLATE: "3-4_1_FIRST_PAGE_template_renamed.psd",
        CONT_TEMPLATE: "3-4_2_CONT_PAGE_template_renamed.psd",
        GRAMMAR_CONT_TEMPLATE: "3-4_3_GRAMMAR_CONT_ref_renamed.psd",
        GRAMMAR_EXERCISE_TEMPLATE: "3-4_4_GRAMMAR_EXERCISE_ref_renamed.psd",
        EXERCISE_CONT_TEMPLATE: "3-4_5_EXERCISE_END_ref_renamed.psd",
    }
    return mapping[template_name]


def layer_rect(manifest: dict[str, dict[str, dict[str, Any]]], template_name: str, layer_name: str) -> Rect | None:
    item = manifest[manifest_key(template_name)].get(layer_name)
    if not item:
        return None
    raw = item.get("rect") or [0, 0, 0, 0]
    if raw == [0, 0, 0, 0]:
        return None
    return Rect.from_list(raw)


def page_frames(manifest: dict[str, dict[str, dict[str, Any]]], template_name: str) -> dict[str, Any]:
    return {
        "left": (layer_rect(manifest, template_name, "@SHELL_CONTENT_PANEL_LEFT") or Rect(0, 0, 0, 0)).to_json(),
        "right": (layer_rect(manifest, template_name, "@SHELL_CONTENT_PANEL_RIGHT") or Rect(0, 0, 0, 0)).to_json(),
        "source": "hidden PSD reference layers; keep hidden in output",
    }


def page_number_pair(page_index: int) -> tuple[str, str]:
    left = page_index * 2 - 1
    return f"{left:03d}", f"{left + 1:03d}"


def reading_lines(lesson: dict[str, Any]) -> list[dict[str, str]]:
    lines: list[dict[str, str]] = []
    for item in lesson["part1"]["reading"]:
        if item.get("phonetic"):
            lines.append({"kind": "phonetic", "text": item["phonetic"]})
        lines.append({"kind": "body", "text": item["text"]})
    return lines


def dialogue_lines(lesson: dict[str, Any]) -> list[dict[str, str]]:
    lines: list[dict[str, str]] = []
    for item in lesson["part1"]["dialogue"]:
        if item.get("phonetic"):
            lines.append({"kind": "phonetic", "text": item["phonetic"]})
        speaker = item.get("speaker") or ""
        text = f"{speaker}: {item['text']}" if speaker else item["text"]
        lines.append({"kind": "dialogue", "speaker": speaker, "text": text})
    return lines


def vocab_rows(manifest: dict[str, dict[str, dict[str, Any]]], template_name: str, start: int, end: int) -> list[dict[str, Any]]:
    rows = []
    for row_no in range(start, end + 1):
        prefix = f"@PART2_VOCAB_ROW_{row_no:02d}"
        rows.append(
            {
                "rowNo": row_no,
                "fixedHeight": True,
                "group": prefix + "_GROUP",
                "slots": {
                    "no": layer_rect(manifest, template_name, prefix + "_NO_TEXT").to_json(),
                    "word": layer_rect(manifest, template_name, prefix + "_WORD_TEXT").to_json(),
                    "phonetic": layer_rect(manifest, template_name, prefix + "_PHONETIC_TEXT").to_json(),
                    "meaning": layer_rect(manifest, template_name, prefix + "_MEANING_TEXT").to_json(),
                },
            }
        )
    return rows


def part3_sections(lesson: dict[str, Any]) -> list[dict[str, Any]]:
    sections = []
    current: dict[str, Any] | None = None
    for block in lesson["part3"]["blocks"]:
        if block["type"] == "sectionTitle":
            current = {"title": block["text"], "blocks": []}
            sections.append(current)
            continue
        if current is None:
            current = {"title": None, "blocks": []}
            sections.append(current)
        current["blocks"].append(block)
    return sections


def exercise_blocks(lesson: dict[str, Any]) -> list[dict[str, Any]]:
    blocks = []
    for section in lesson["part4"]["sections"]:
        blocks.append({"kind": "sectionTitle", "sectionNo": section["sectionNo"], "text": section["title"]})
        for item in section["items"]:
            blocks.append(
                {
                    "kind": "exerciseItem",
                    "itemNo": item.get("itemNo"),
                    "text": item.get("displayText") or item["text"],
                    "answerLines": item.get("answerLines", 0),
                    "keepTogether": True,
                }
            )
    return blocks


def build_plan() -> dict[str, Any]:
    lesson = load_lesson()
    manifest = load_manifest()
    part3 = part3_sections(lesson)
    pages: list[dict[str, Any]] = []

    pages.append(
        {
            "pageIndex": 1,
            "template": FIRST_TEMPLATE,
            "pageNumbers": page_number_pair(1),
            "frames": page_frames(manifest, FIRST_TEMPLATE),
            "hiddenLayers": HIDDEN_REFERENCE_LAYERS,
            "modules": [
                {
                    "id": "part1",
                    "type": "readingDialogue",
                    "dynamic": True,
                    "titleLayerPolicy": "preserveTemplateTitleLayer",
                    "reading": {
                        "styleSources": [
                            "@PART1_READING_LEFT_TEXT_STYLE_SOURCE",
                            "@PART1_READING_RIGHT_TEXT_STYLE_SOURCE",
                        ],
                        "lines": reading_lines(lesson),
                        "requiresPsMeasurement": [
                            "line wraps",
                            "phonetic y offset",
                            "green border bottom",
                        ],
                    },
                    "dialogue": {
                        "intro": lesson["part1"]["dialogueIntro"],
                        "roleNote": lesson["part1"]["dialogueRoleNote"],
                        "lines": dialogue_lines(lesson),
                        "requiresPsMeasurement": [
                            "right frame overflow to next left frame",
                            "yellow box bottom",
                            "green vertical line height",
                        ],
                    },
                },
                {
                    "id": "part2_rows_01_08",
                    "type": "vocabularyFixedRows",
                    "titleLayerPolicy": "preserveTemplateTitleLayer",
                    "rowHeightPolicy": "fixedFromTemplate",
                    "overflowPolicy": "wrapInsideFixedTextBoxOrFlagReview",
                    "rows": vocab_rows(manifest, FIRST_TEMPLATE, 1, 8),
                    "items": lesson["part2"]["items"][:8],
                },
            ],
        }
    )

    pages.append(
        {
            "pageIndex": 2,
            "template": CONT_TEMPLATE,
            "pageNumbers": page_number_pair(2),
            "frames": page_frames(manifest, CONT_TEMPLATE),
            "hiddenLayers": HIDDEN_REFERENCE_LAYERS,
            "modules": [
                {
                    "id": "part2_rows_09_21",
                    "type": "vocabularyFixedRows",
                    "rowHeightPolicy": "fixedFromTemplate",
                    "overflowPolicy": "wrapInsideFixedTextBoxOrFlagReview",
                    "rows": vocab_rows(manifest, CONT_TEMPLATE, 9, 21),
                    "items": lesson["part2"]["items"][8:21],
                    "emptyRowsPolicy": "hideUnusedRows",
                },
                {
                    "id": "part3_start",
                    "type": "grammarFlow",
                    "titleLayerPolicy": "preserveTemplateTitleLayer",
                    "lead": lesson["part3"]["leadSentence"],
                    "sections": part3,
                    "subtitlePolicy": "hideSubtitleGroupsWhenWordHasNoSectionTitle",
                },
            ],
        }
    )

    pages.append(
        {
            "pageIndex": 3,
            "template": GRAMMAR_CONT_TEMPLATE,
            "pageNumbers": page_number_pair(3),
            "frames": page_frames(manifest, GRAMMAR_CONT_TEMPLATE),
            "hiddenLayers": HIDDEN_REFERENCE_LAYERS,
            "modules": [{"id": "part3_cont", "type": "grammarFlowContinuation", "source": "part3_start"}],
        }
    )

    pages.append(
        {
            "pageIndex": 4,
            "template": GRAMMAR_EXERCISE_TEMPLATE,
            "pageNumbers": page_number_pair(4),
            "frames": page_frames(manifest, GRAMMAR_EXERCISE_TEMPLATE),
            "hiddenLayers": HIDDEN_REFERENCE_LAYERS,
            "modules": [
                {"id": "part3_end", "type": "grammarFlowContinuation", "source": "part3_start"},
                {
                    "id": "part4_start",
                    "type": "exerciseFlow",
                    "titleLayerPolicy": "showOnceAtExerciseStart",
                    "blocks": exercise_blocks(lesson),
                    "keepTogetherPolicy": "exerciseItemAndAnswerLines",
                },
            ],
        }
    )

    pages.append(
        {
            "pageIndex": 5,
            "template": EXERCISE_CONT_TEMPLATE,
            "pageNumbers": page_number_pair(5),
            "frames": page_frames(manifest, EXERCISE_CONT_TEMPLATE),
            "hiddenLayers": HIDDEN_REFERENCE_LAYERS,
            "modules": [{"id": "part4_cont", "type": "exerciseFlowContinuation", "source": "part4_start"}],
        }
    )

    return {
        "lessonNo": lesson["lessonNo"],
        "lessonTitle": lesson["lessonTitle"],
        "status": "planOnlyNotRendered",
        "rules": {
            "preserveHiddenTemplateLayers": True,
            "partTitlesPreserveTemplateStyle": True,
            "vocabRowHeight": "fixed",
            "vocabLongText": "wrapInsideFixedTextBoxOrFlagReview",
            "part3NoFakeSubtitles": True,
            "exerciseKeepOriginalNumbering": True,
            "pageNumberFormat": "000",
        },
        "pages": pages,
        "unresolvedRequiresPhotoshopMeasurement": [
            "exact text wrap using PSD font metrics",
            "Part1 reading green border dynamic resize",
            "Dialogue yellow box and green line dynamic resize",
            "flow break positions after actual Photoshop text composition",
        ],
    }


def write_report(plan: dict[str, Any]) -> None:
    lines = [
        "# Lesson 1-2 动态排版计划报告",
        "",
        f"- Lesson：{plan['lessonNo']} {plan['lessonTitle']}",
        f"- 页面数计划：{len(plan['pages'])}",
        "- 状态：只生成排版计划，未启动 Photoshop 渲染",
        "",
        "## 已固化规则",
        "",
    ]
    for key, value in plan["rules"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 页面模块", ""])
    for page in plan["pages"]:
        lines.append(f"### Page {page['pageIndex']} / {page['template']}")
        lines.append(f"- 页码：{page['pageNumbers'][0]} / {page['pageNumbers'][1]}")
        lines.append(f"- 隐藏参考层：{', '.join(page['hiddenLayers'])}")
        for module in page["modules"]:
            lines.append(f"- 模块：{module['id']} ({module['type']})")
    lines.extend(["", "## 仍需 Photoshop 实测", ""])
    for item in plan["unresolvedRequiresPhotoshopMeasurement"]:
        lines.append(f"- {item}")
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    plan = build_plan()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(plan)
    print(OUT_JSON)
    print(OUT_REPORT)


if __name__ == "__main__":
    main()
