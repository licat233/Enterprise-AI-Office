#!/usr/bin/env python3
"""Regression tests for the Phase 5B.2 MIC authority de-duplication."""

from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/shared/department/armor-mic-product-optimization/SKILL.md"
STANDARD_RELATIVE = Path(
    "02-Projects/Workspaces/Products/MIC-Products/"
    "ARMOR-MIC-Product-Optimization-Standard-v1.0.md"
)
CHECKER_PATH = ROOT / "scripts/phase5b_mic_runtime_check.py"


def _load_checker():
    spec = importlib.util.spec_from_file_location("phase5b2_runtime_checker", CHECKER_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CHECKER = _load_checker()


def _normalized(text: str) -> str:
    return " ".join(text.split())


def _standard() -> tuple[Path, str]:
    vault_root = os.environ.get("ARMOR_VAULT_ROOT")
    if not vault_root:
        raise AssertionError("ARMOR_VAULT_ROOT is required for MIC de-duplication tests")
    path = Path(vault_root) / STANDARD_RELATIVE
    if not path.is_file():
        raise AssertionError(f"canonical MIC standard is missing: {path}")
    return path, path.read_text(encoding="utf-8")


class MICAuthorityDedupTests(unittest.TestCase):
    def test_vault_standard_exists_and_is_canonical(self):
        path, text = _standard()
        self.assertIn("authority: canonical", text)
        self.assertTrue(path.is_file())

    def test_skill_references_exact_standard_and_not_embedded_sop(self):
        skill = _normalized(SKILL.read_text(encoding="utf-8"))
        self.assertIn("$ARMOR_VAULT_ROOT/02-Projects/Workspaces/Products/MIC-Products/ ARMOR-MIC-Product-Optimization-Standard-v1.0.md", skill)
        self.assertIn("sole detailed MIC workflow authority", skill)
        self.assertIn("Never silently fall back to an embedded duplicate rule set", skill)
        self.assertNotIn("### Exact product technical facts", skill)
        self.assertNotIn("### Mutable commercial/business fields", skill)

    def test_skill_and_standard_are_not_identical_and_skill_is_smaller(self):
        standard_path, standard_text = _standard()
        skill_text = SKILL.read_text(encoding="utf-8")
        self.assertNotEqual(skill_text.encode("utf-8"), standard_text.encode("utf-8"))
        self.assertLess(len(skill_text), len(standard_text), f"Skill must be thinner than {standard_path}")

    def test_corrected_technical_hierarchy_remains_in_vault_standard(self):
        _, text = _standard()
        normalized = _normalized(text)
        markers = (
            "1. authoritative original Datasheet",
            "2. canonical or verified Product Knowledge",
            "3. read-only WeKnora retrieval",
            "4. the current MIC listing or edit page",
        )
        positions = [normalized.index(marker) for marker in markers]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("never as final technical authority", normalized)
        self.assertIn("may supersede historical MIC listing data", normalized)

    def test_skill_keeps_concise_fail_closed_invariants(self):
        normalized = _normalized(SKILL.read_text(encoding="utf-8"))
        self.assertIn("Do not fabricate technical, commercial, certification, packaging, or performance facts", normalized)
        self.assertIn("Exact technical values must ultimately resolve to an authoritative original source", normalized)
        self.assertIn("`UNKNOWN` remains unknown", normalized)
        self.assertIn("save_mic_product_package", normalized)
        self.assertIn("Do not perform live MIC editing", normalized)
        self.assertIn("upload, publication", normalized)
        self.assertNotIn("Source priority is:", normalized)

    def test_runtime_standard_resolution_fails_closed_when_missing(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(FileNotFoundError):
                CHECKER.resolve_canonical_mic_standard(Path(temp))

    def test_operations_canonical_skill_symlink_still_resolves(self):
        operations_root = os.environ.get("ARMOR_OPERATIONS_ROOT")
        if not operations_root:
            self.skipTest("ARMOR_OPERATIONS_ROOT is required for deployed symlink verification")
        link = Path(operations_root) / "skills/armor-mic-product-optimization"
        self.assertTrue(link.is_symlink())
        self.assertEqual(link.resolve(), SKILL.parent.resolve())


if __name__ == "__main__":
    unittest.main()
