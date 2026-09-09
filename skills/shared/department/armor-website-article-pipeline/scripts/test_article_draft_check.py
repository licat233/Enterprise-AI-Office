import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("article-draft-check.py")
SPEC = importlib.util.spec_from_file_location("article_draft_check", MODULE_PATH)
CHECKER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHECKER)
REGRESSION_DIR = Path("/tmp/armor-retail-rewrite")


def results(body):
    return {item["id"]: item["result"] for item in CHECKER.editorial_prose_checks(body)}


class EditorialGateTests(unittest.TestCase):
    def test_customer_value_title_matrix(self):
        rejected = [
            "LCD Shelf Label Displays and the Shelf-Edge Retail Media Wave",
            "The Future of LCD Shelf Labels",
            "Revolutionizing Retail with LCD Shelf Labels",
        ]
        accepted = [
            "Are LCD Shelf Labels Worth It for Retail Media in 2026?",
            "LCD vs E-Paper ESL: Which Display Should Retailers Choose?",
            "How to Choose an LCD Shelf Label for Retail Media",
            "LCD Shelf Label Buyer Guide for Supermarkets",
        ]
        for title in rejected:
            with self.subTest(title=title):
                self.assertNotEqual("ok", CHECKER.title_value_outcome(title))
        for title in accepted:
            with self.subTest(title=title):
                self.assertEqual("ok", CHECKER.title_value_outcome(title))

    def test_title_value_is_not_a_question_mark_gate(self):
        checks = CHECKER.title_value_checks(
            "How to Choose an LCD Shelf Label for Retail Media",
            "LCD Shelf Label Buyer Guide for Supermarkets",
        )
        self.assertEqual("TITLE-01", checks[0]["id"])
        self.assertEqual("passed", checks[0]["result"])

    def test_intro_overlap_and_close_negative(self):
        positive = """# Shelf Lighting

Ceiling beams miss packed middle shelves, leaving merchandise below poorly lit.

## Where the beam stops

Packed middle shelves block ceiling beams before the light reaches merchandise below.
"""
        negative = """# Shelf Lighting

Ceiling beams can miss packed middle shelves.

## Set the electrical boundary

Cold cabinets require moisture protection and a verified low-voltage connection.
"""
        self.assertEqual("failed", results(positive)["PROSE-03"])
        self.assertEqual("passed", results(negative)["PROSE-03"])

    def test_behavior_and_attributed_negative(self):
        self.assertEqual("failed", results("# X\n\nBuyers most commonly forget the IP rating.\n")["PROSE-04"])
        self.assertEqual("passed", results("# X\n\nAccording to the 2025 buyer survey, buyers most commonly ask about IP ratings.\n")["PROSE-04"])

    def test_roadmap_and_operational_negative(self):
        self.assertEqual("failed", results("# X\n\nThis article covers the four specs.\n")["PROSE-05"])
        self.assertEqual("passed", results("# X\n\nThe cold cabinet requires an IP65 fixture.\n")["PROSE-05"])

    def test_spec_tour_and_technical_reference_negative(self):
        tour = """# X

## Choose by zone

### CRI: Color accuracy
Text.

### R9: Saturated red
Text.

### CCT: Department tone
Text.

### IP: Moisture boundary
Text.
"""
        reference = tour.replace("## Choose by zone", "## API Reference")
        self.assertEqual("failed", results(tour)["PROSE-06"])
        self.assertEqual("passed", results(reference)["PROSE-06"])

    def test_protected_regions_do_not_trigger(self):
        body = """# X

<!--
This article covers the four specs.
Buyers most commonly forget IP ratings.
### CRI: Color accuracy
### R9: Saturated red
### CCT: Department tone
### IP: Moisture boundary
-->
"""
        gate_results = results(body)
        self.assertEqual("passed", gate_results["PROSE-04"])
        self.assertEqual("passed", gate_results["PROSE-05"])
        self.assertEqual("passed", gate_results["PROSE-06"])

    def test_real_rewrites_when_available(self):
        first = REGRESSION_DIR / "rewritten-index.md"
        final = REGRESSION_DIR / "rewritten-index-v3.md"
        if not first.is_file() or not final.is_file():
            self.skipTest("local regression articles are unavailable")
        _, first_body = CHECKER.parse_frontmatter(first.read_text(encoding="utf-8"))
        _, final_body = CHECKER.parse_frontmatter(final.read_text(encoding="utf-8"))
        first_results = results(first_body)
        final_results = results(final_body)
        self.assertTrue(any(first_results[key] == "failed" for key in ("PROSE-03", "PROSE-04", "PROSE-05", "PROSE-06")))
        self.assertTrue(all(final_results[key] == "passed" for key in ("PROSE-03", "PROSE-04", "PROSE-05", "PROSE-06")))


if __name__ == "__main__":
    unittest.main()
