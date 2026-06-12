import json
import unittest
from pathlib import Path

from scripts.dynamic_layout_plan import build_lesson_layout_plan


ROOT = Path(__file__).resolve().parents[1]
LESSONS = json.loads((ROOT / "data" / "intermediate_lessons.json").read_text(encoding="utf-8"))["lessons"]


class DynamicLayoutPlanTests(unittest.TestCase):
    def lesson(self, lesson_no):
        return next(item for item in LESSONS if item["lessonNo"] == lesson_no)

    def test_page_count_is_content_driven_and_uses_two_shell_templates(self):
        short_plan = build_lesson_layout_plan(self.lesson("Lesson 1-2"))
        long_plan = build_lesson_layout_plan(self.lesson("Lesson 3-4"))

        self.assertEqual(long_plan["status"], "dynamicPlan")
        self.assertGreater(len(long_plan["pages"]), len(short_plan["pages"]))
        self.assertLess(len(short_plan["pages"]), 5)
        self.assertEqual(long_plan["pages"][0]["template"], "3-4 1.psd")
        self.assertTrue(all(page["template"] == "3-4 2.psd" for page in long_plan["pages"][1:]))

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
        self.assertTrue(
            any(block["kind"] == "sectionTitle" and block["text"].startswith("5.") for block in grammar_blocks)
        )

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
