# Dynamic PS Layout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the fixed five-page sample plan with a content-driven lesson layout plan that can be verified without Photoshop.

**Architecture:** Add a small Python layout planner that converts parsed lesson JSON into pages, frames, and keep-together blocks. Keep Photoshop-specific rendering in JSX, but make the Python plan responsible for dynamic page count, module order, and overflow boundaries.

**Tech Stack:** Python standard library, `unittest`, existing JSON inputs in `data/`.

---

### Task 1: Add Regression Tests For Dynamic Planning

**Files:**
- Create: `tests/test_dynamic_layout_plan.py`
- Modify: none

- [ ] **Step 1: Write the failing tests**

```python
import json
import unittest
from pathlib import Path

from scripts.dynamic_layout_plan import build_lesson_layout_plan


ROOT = Path(__file__).resolve().parents[1]
LESSONS = json.loads((ROOT / "data" / "intermediate_lessons.json").read_text(encoding="utf-8"))["lessons"]


class DynamicLayoutPlanTests(unittest.TestCase):
    def lesson(self, lesson_no):
        return next(item for item in LESSONS if item["lessonNo"] == lesson_no)

    def test_lesson_3_4_uses_content_driven_page_count(self):
        plan = build_lesson_layout_plan(self.lesson("Lesson 3-4"))
        self.assertEqual(plan["status"], "dynamicPlan")
        self.assertGreater(len(plan["pages"]), 5)
        self.assertEqual(plan["pages"][0]["template"], "3-4 1.psd")
        self.assertTrue(all(page["template"] == "3-4 2.psd" for page in plan["pages"][1:]))

    def test_grammar_blocks_are_not_truncated_to_fixed_slots(self):
        lesson = self.lesson("Lesson 3-4")
        plan = build_lesson_layout_plan(lesson)
        grammar_blocks = [
            block
            for page in plan["pages"]
            for frame in page["frames"]
            for block in frame["blocks"]
            if block["part"] == "part3"
        ]
        self.assertEqual(len(grammar_blocks), 1 + len(lesson["part3"]["blocks"]))
        self.assertEqual(grammar_blocks[0]["kind"], "lead")
        self.assertTrue(any(block["kind"] == "sectionTitle" and block["text"].startswith("5.") for block in grammar_blocks))

    def test_exercise_items_keep_answer_lines_together(self):
        plan = build_lesson_layout_plan(self.lesson("Lesson 3-4"))
        answer_items = [
            block
            for page in plan["pages"]
            for frame in page["frames"]
            for block in frame["blocks"]
            if block["part"] == "part4" and block.get("answerLines")
        ]
        self.assertGreaterEqual(len(answer_items), 10)
        self.assertTrue(all(block["keepTogether"] for block in answer_items))
        self.assertTrue(all(block["estimatedLines"] >= 2 for block in answer_items))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m unittest tests.test_dynamic_layout_plan -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.dynamic_layout_plan'`.

### Task 2: Implement Dynamic Layout Planner

**Files:**
- Create: `scripts/dynamic_layout_plan.py`
- Modify: `scripts/intermediate_layout_plan.py`
- Test: `tests/test_dynamic_layout_plan.py`

- [ ] **Step 1: Create planner module**

Implement `build_lesson_layout_plan(lesson)` with these behaviors:
- first page uses `3-4 1.psd`;
- all continuation pages use `3-4 2.psd`;
- frames are left then right on every page;
- blocks flow in Part 1, Part 2, Part 3, Part 4 order;
- vocab and exercise items are keep-together blocks;
- grammar includes the lead plus every source grammar block without truncation.

- [ ] **Step 2: Run tests to verify planner passes**

Run: `python3 -m unittest tests.test_dynamic_layout_plan -v`
Expected: PASS.

### Task 3: Wire Existing Plan Generator To Dynamic Planner

**Files:**
- Modify: `scripts/intermediate_layout_plan.py`
- Test: `tests/test_dynamic_layout_plan.py`

- [ ] **Step 1: Replace fixed five-page construction**

Make `scripts/intermediate_layout_plan.py` delegate to `scripts.dynamic_layout_plan.build_lesson_layout_plan`, support a lesson number parameter, and continue writing `data/lesson_1_2_layout_plan.json` by default for compatibility.

- [ ] **Step 2: Run generator and tests**

Run: `python3 scripts/intermediate_layout_plan.py "Lesson 3-4" /tmp/lesson_3_4_layout_plan.json`
Expected: JSON status is `dynamicPlan` and page count is greater than 5.

### Task 4: Verify And Commit

**Files:**
- All modified files

- [ ] **Step 1: Run verification**

Run:
```bash
python3 -m unittest tests.test_dynamic_layout_plan -v
python3 -m py_compile scripts/*.py tests/*.py
```

- [ ] **Step 2: Commit**

Run:
```bash
git add docs/superpowers/plans/2026-06-12-dynamic-ps-layout.md tests/test_dynamic_layout_plan.py scripts/dynamic_layout_plan.py scripts/intermediate_layout_plan.py
git commit -m "fix(layout): generate content-driven lesson plans"
```
