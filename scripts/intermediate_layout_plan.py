from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.dynamic_layout_plan import build_lesson_layout_plan


DATA_DIR = PROJECT_ROOT / "data"
LESSONS_JSON = DATA_DIR / "intermediate_lessons.json"
DEFAULT_LESSON_NO = "Lesson 1-2"
DEFAULT_OUT_JSON = DATA_DIR / "lesson_1_2_layout_plan.json"


def load_lessons(path: Path = LESSONS_JSON) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))["lessons"]


def select_lesson(lessons: list[dict[str, Any]], lesson_no: str) -> dict[str, Any]:
    for lesson in lessons:
        if lesson["lessonNo"] == lesson_no:
            return lesson
    raise RuntimeError(f"{lesson_no} not found")


def write_report(plan: dict[str, Any], output_path: Path) -> Path:
    report_path = output_path.with_suffix(".md")
    lines = [
        f"# {plan['lessonNo']} 动态排版计划报告",
        "",
        f"- Lesson：{plan['lessonNo']} {plan['lessonTitle']}",
        f"- 状态：{plan['status']}",
        f"- 页面数：{len(plan['pages'])}",
        f"- 首页模板：{plan['rules']['firstPageTemplate']}",
        f"- 后续页模板：{plan['rules']['continuePageTemplate']}",
        "",
        "## 页面概览",
        "",
    ]
    for page in plan["pages"]:
        frame_summary = ", ".join(
            f"{frame['name']} {frame['usedLines']}/{frame['capacityLines']} lines"
            for frame in page["frames"]
        )
        lines.append(
            f"- Page {page['pageIndex']} / {page['template']} / "
            f"{page['pageNumbers'][0]}-{page['pageNumbers'][1]}：{frame_summary}"
        )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def build_and_write(lesson_no: str = DEFAULT_LESSON_NO, output_path: Path = DEFAULT_OUT_JSON) -> dict[str, Any]:
    lesson = select_lesson(load_lessons(), lesson_no)
    plan = build_lesson_layout_plan(lesson)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(plan, output_path)
    return plan


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    lesson_no = args[0] if args else DEFAULT_LESSON_NO
    output_path = Path(args[1]) if len(args) > 1 else DEFAULT_OUT_JSON
    plan = build_and_write(lesson_no, output_path)
    print(output_path)
    print(output_path.with_suffix(".md"))
    print(f"{plan['lessonNo']} pages={len(plan['pages'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
