from __future__ import annotations

import math
import re
from copy import deepcopy
from typing import Any


FIRST_TEMPLATE = "3-4 1.psd"
CONT_TEMPLATE = "3-4 2.psd"

LINE_HEIGHT_PX = 83
MODULE_GAP_LINES = 1

FIRST_PAGE_FRAMES = [
    {"name": "left", "rect": {"top": 649, "left": 200, "bottom": 3311, "right": 2149}},
    {"name": "right", "rect": {"top": 421, "left": 2773, "bottom": 3311, "right": 4840}},
]
CONT_PAGE_FRAMES = [
    {"name": "left", "rect": {"top": 421, "left": 200, "bottom": 3311, "right": 2149}},
    {"name": "right", "rect": {"top": 421, "left": 2773, "bottom": 3311, "right": 4840}},
]

CHARS_PER_LINE = {
    "part1": 50,
    "part2": 24,
    "part3": 31,
    "part4": 30,
    "title": 28,
}


def page_number_pair(page_index: int) -> list[str]:
    left = page_index * 2 - 1
    return [f"{left:03d}", f"{left + 1:03d}"]


def frame_capacity(rect: dict[str, int]) -> int:
    height = rect["bottom"] - rect["top"]
    return max(1, int(height // LINE_HEIGHT_PX))


def normalize_text(text: Any) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def estimate_lines(text: str, part: str, minimum: int = 1, extra: int = 0) -> int:
    text = normalize_text(text)
    width = CHARS_PER_LINE.get(part, 30)
    ascii_count = sum(1 for char in text if ord(char) < 128)
    cjk_weight = len(text) - ascii_count
    weighted_length = ascii_count * 0.55 + cjk_weight
    return max(minimum, int(math.ceil(weighted_length / width)) + extra)


def make_block(
    part: str,
    kind: str,
    text: str,
    *,
    estimated_lines: int | None = None,
    keep_together: bool = False,
    answer_lines: int = 0,
    source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    block = {
        "part": part,
        "kind": kind,
        "text": text,
        "estimatedLines": estimated_lines if estimated_lines is not None else estimate_lines(text, part),
        "keepTogether": keep_together,
    }
    if answer_lines:
        block["answerLines"] = answer_lines
    if source:
        block["source"] = deepcopy(source)
    return block


def part_title_block(part_no: int, title: str) -> dict[str, Any]:
    return make_block(
        "title",
        "partTitle",
        f"PART {part_no}    {title}",
        estimated_lines=2,
        keep_together=True,
        source={"partNo": part_no},
    )


def reading_blocks(lesson: dict[str, Any]) -> list[dict[str, Any]]:
    blocks = [part_title_block(1, lesson["part1"].get("title", "Reading&Dialogue"))]
    for index, item in enumerate(lesson["part1"].get("reading", []), start=1):
        phonetic = normalize_text(item.get("phonetic"))
        text = normalize_text(item.get("text"))
        lines = estimate_lines(text, "part1", minimum=1)
        if phonetic:
            lines += 1
        blocks.append(
            make_block(
                "part1",
                "reading",
                text,
                estimated_lines=lines,
                keep_together=True,
                source={"index": index, "phonetic": phonetic},
            )
        )

    intro = normalize_text(lesson["part1"].get("dialogueIntro"))
    if intro:
        blocks.append(make_block("part1", "dialogueIntro", intro, estimated_lines=2, keep_together=True))

    role_note = normalize_text(lesson["part1"].get("dialogueRoleNote"))
    if role_note:
        blocks.append(make_block("part1", "dialogueRole", role_note, estimated_lines=1, keep_together=True))

    for index, item in enumerate(lesson["part1"].get("dialogue", []), start=1):
        speaker = normalize_text(item.get("speaker"))
        text = normalize_text(item.get("text"))
        phonetic = normalize_text(item.get("phonetic"))
        display = f"{speaker}: {text}" if speaker else text
        lines = estimate_lines(display, "part1", minimum=1)
        if phonetic:
            lines += 1
        blocks.append(
            make_block(
                "part1",
                "dialogue",
                display,
                estimated_lines=lines,
                keep_together=True,
                source={"index": index, "speaker": speaker, "phonetic": phonetic},
            )
        )
    return blocks


def vocab_blocks(lesson: dict[str, Any]) -> list[dict[str, Any]]:
    blocks = [part_title_block(2, lesson["part2"].get("title", "Vocabulary&Idioms"))]
    for item in lesson["part2"].get("items", []):
        text = " ".join(
            part
            for part in [
                item.get("no", ""),
                item.get("word", ""),
                item.get("kk", ""),
                item.get("ipa", ""),
                item.get("meaning", ""),
            ]
            if part
        )
        meaning_lines = estimate_lines(item.get("meaning", ""), "part2", minimum=1)
        word_lines = estimate_lines(item.get("word", ""), "part2", minimum=1)
        lines = max(2, meaning_lines, word_lines)
        blocks.append(
            make_block(
                "part2",
                "vocabItem",
                text,
                estimated_lines=lines,
                keep_together=True,
                source={
                    "no": item.get("no", ""),
                    "word": item.get("word", ""),
                    "kk": item.get("kk", ""),
                    "ipa": item.get("ipa", ""),
                    "meaning": item.get("meaning", ""),
                },
            )
        )
    return blocks


def grammar_blocks(lesson: dict[str, Any]) -> list[dict[str, Any]]:
    blocks = [part_title_block(3, lesson["part3"].get("title", "Grammar points"))]
    lead = normalize_text(lesson["part3"].get("leadSentence"))
    if lead:
        blocks.append(make_block("part3", "lead", lead, estimated_lines=2, keep_together=True))
    for index, item in enumerate(lesson["part3"].get("blocks", []), start=1):
        kind = item.get("type", "paragraph")
        text = normalize_text(item.get("text"))
        minimum = 2 if kind == "sectionTitle" else 1
        extra = 1 if kind == "transformExample" else 0
        blocks.append(
            make_block(
                "part3",
                kind,
                text,
                estimated_lines=estimate_lines(text, "part3", minimum=minimum, extra=extra),
                keep_together=(kind == "sectionTitle"),
                source={"index": index, "runs": item.get("runs", [])},
            )
        )
    return blocks


def exercise_blocks(lesson: dict[str, Any]) -> list[dict[str, Any]]:
    blocks = [part_title_block(4, lesson["part4"].get("title", "Exercise"))]
    for section in lesson["part4"].get("sections", []):
        section_no = normalize_text(section.get("sectionNo"))
        title = normalize_text(section.get("title"))
        heading = f"{section_no} {title}".strip()
        if heading:
            blocks.append(make_block("part4", "sectionTitle", heading, estimated_lines=2, keep_together=True))
        for item in section.get("items", []):
            text = normalize_text(item.get("displayText") or item.get("text"))
            answer_lines = int(item.get("answerLines", 0) or 0)
            estimated = estimate_lines(text, "part4", minimum=1) + answer_lines
            blocks.append(
                make_block(
                    "part4",
                    "exerciseItem",
                    text,
                    estimated_lines=estimated,
                    keep_together=True,
                    answer_lines=answer_lines,
                    source={"itemNo": item.get("itemNo"), "numberingLabel": item.get("numberingLabel")},
                )
            )
    return blocks


def lesson_blocks(lesson: dict[str, Any]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for group in [reading_blocks(lesson), vocab_blocks(lesson), grammar_blocks(lesson), exercise_blocks(lesson)]:
        if blocks:
            blocks.append(make_block("title", "moduleGap", "", estimated_lines=MODULE_GAP_LINES))
        blocks.extend(group)
    return blocks


class PageBuilder:
    def __init__(self) -> None:
        self.pages: list[dict[str, Any]] = []
        self.page_index = 0
        self.frame_index = 0
        self._add_page()

    @property
    def current_page(self) -> dict[str, Any]:
        return self.pages[-1]

    @property
    def current_frame(self) -> dict[str, Any]:
        return self.current_page["frames"][self.frame_index]

    def _frame_specs(self, page_index: int) -> list[dict[str, Any]]:
        return FIRST_PAGE_FRAMES if page_index == 1 else CONT_PAGE_FRAMES

    def _add_page(self) -> None:
        self.page_index += 1
        frame_specs = self._frame_specs(self.page_index)
        self.pages.append(
            {
                "pageIndex": self.page_index,
                "template": FIRST_TEMPLATE if self.page_index == 1 else CONT_TEMPLATE,
                "pageNumbers": page_number_pair(self.page_index),
                "frames": [
                    {
                        "name": spec["name"],
                        "rect": dict(spec["rect"]),
                        "capacityLines": frame_capacity(spec["rect"]),
                        "usedLines": 0,
                        "blocks": [],
                    }
                    for spec in frame_specs
                ],
            }
        )
        self.frame_index = 0

    def _advance_frame(self) -> None:
        if self.frame_index + 1 < len(self.current_page["frames"]):
            self.frame_index += 1
        else:
            self._add_page()

    def place(self, block: dict[str, Any]) -> None:
        needed = max(1, int(block.get("estimatedLines", 1)))
        while self.current_frame["usedLines"] and self.current_frame["usedLines"] + needed > self.current_frame["capacityLines"]:
            self._advance_frame()
        if needed > self.current_frame["capacityLines"]:
            block = dict(block)
            block["review"] = "estimated block exceeds frame capacity"
        self.current_frame["blocks"].append(block)
        self.current_frame["usedLines"] += min(needed, self.current_frame["capacityLines"])


def build_lesson_layout_plan(lesson: dict[str, Any]) -> dict[str, Any]:
    builder = PageBuilder()
    blocks = lesson_blocks(lesson)
    for index, block in enumerate(blocks):
        if block["kind"] == "partTitle" and index + 1 < len(blocks):
            needed = block["estimatedLines"] + blocks[index + 1].get("estimatedLines", 1)
            frame = builder.current_frame
            if frame["usedLines"] and frame["usedLines"] + needed > frame["capacityLines"]:
                builder._advance_frame()
        builder.place(block)

    return {
        "lessonNo": lesson.get("lessonNo", ""),
        "lessonTitle": lesson.get("lessonTitle", ""),
        "status": "dynamicPlan",
        "rules": {
            "firstPageTemplate": FIRST_TEMPLATE,
            "continuePageTemplate": CONT_TEMPLATE,
            "contentOrder": ["part1", "part2", "part3", "part4"],
            "keepTogetherKinds": ["vocabItem", "exerciseItem", "sectionTitle"],
            "lineHeightPx": LINE_HEIGHT_PX,
            "estimation": "static preflight; Photoshop render must remeasure final text bounds",
        },
        "pages": builder.pages,
    }
