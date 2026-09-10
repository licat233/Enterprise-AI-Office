#!/usr/bin/env python3
"""Regression tests for the Phase 5B.1 MIC authority correction."""

from __future__ import annotations

import os
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/shared/department/armor-mic-product-optimization/SKILL.md"
STANDARD_RELATIVE = Path(
    "02-Projects/Workspaces/Products/MIC-Products/"
    "ARMOR-MIC-Product-Optimization-Standard-v1.0.md"
)


def _documents() -> dict[str, str]:
    documents = {"Enterprise MIC Skill": SKILL.read_text(encoding="utf-8")}
    vault_root = os.environ.get("ARMOR_VAULT_ROOT")
    if vault_root:
        standard = Path(vault_root) / STANDARD_RELATIVE
        if not standard.is_file():
            raise AssertionError(f"canonical MIC standard is missing: {standard}")
        documents["Canonical MIC Vault standard"] = standard.read_text(encoding="utf-8")
    return documents


def _technical_section(text: str) -> str:
    start = text.index("### Exact product technical facts")
    end = text.index("### Mutable commercial/business fields", start)
    return text[start:end]


def _normalized(text: str) -> str:
    return " ".join(text.split())


class MICTechnicalAuthorityTests(unittest.TestCase):
    def test_authoritative_original_document_outranks_weknora_and_mic(self):
        for label, text in _documents().items():
            section = _technical_section(text)
            ranks = {
                "original": section.index("1. authoritative original Datasheet"),
                "knowledge": section.index("2. canonical or verified Product Knowledge"),
                "weknora": section.index("3. read-only WeKnora retrieval"),
                "mic": section.index("4. the current MIC listing or edit page"),
            }
            self.assertLess(ranks["original"], ranks["knowledge"], label)
            self.assertLess(ranks["knowledge"], ranks["weknora"], label)
            self.assertLess(ranks["weknora"], ranks["mic"], label)

            candidates = {
                "WeKnora-derived value": ("24V", ranks["weknora"]),
                "conflicting Datasheet value": ("12V", ranks["original"]),
                "historical MIC value": ("36V", ranks["mic"] + 1),
            }
            winner = min(candidates.values(), key=lambda item: item[1])
            self.assertEqual(winner[0], "12V", label)

    def test_weknora_is_retrieval_only_and_cannot_override_original(self):
        for label, text in _documents().items():
            normalized = _normalized(text)
            self.assertIn("used to locate or retrieve the Knowledge or", normalized, label)
            self.assertIn("never as final technical authority", normalized, label)
            self.assertIn("WeKnora must never silently override a conflicting", normalized, label)
            self.assertIn("Historical MIC output cannot override a current authoritative specification", normalized, label)

    def test_current_commercial_confirmation_can_supersede_historical_data(self):
        for label, text in _documents().items():
            normalized = _normalized(text)
            self.assertIn("current explicit company or user confirmation", normalized, label)
            self.assertIn("current approved commercial documentation", normalized, label)
            self.assertIn("may supersede historical MIC listing data", normalized, label)

    def test_observable_media_is_limited_to_visible_facts(self):
        for label, text in _documents().items():
            normalized = _normalized(text)
            self.assertIn("Observable media supports directly visible facts only", normalized, label)
            self.assertIn("cannot create exact", normalized, label)

    def test_inference_cannot_populate_unknown_numeric_specification(self):
        for label, text in _documents().items():
            normalized = _normalized(text)
            self.assertIn("REASONABLE_INFERENCE` may improve wording", normalized, label)
            self.assertIn("cannot create numeric facts", normalized, label)
            self.assertIn("technical specifications", normalized, label)
            lowered = normalized.lower()
            self.assertTrue(
                "unknown values remain explicit" in lowered or "unknown` stays explicit" in lowered,
                label,
            )


if __name__ == "__main__":
    unittest.main()
