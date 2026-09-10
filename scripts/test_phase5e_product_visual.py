#!/usr/bin/env python3
"""Offline acceptance tests for the Phase 5E Product Visual boundary."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "skills/shared/department/armor-memory/scripts/armor-route.py"
WRAPPER = ROOT / "skills/shared/department/armor-memory/scripts/route.sh"
SCOPED_MCP = ROOT / "skills/shared/department/armor-memory/scripts/armor-vault-mcp.py"
SKILL = ROOT / "skills/shared/department/armor-product-visual/SKILL.md"
STANDARD_RELATIVE = Path(
    "02-Projects/Workspaces/Products/Product-Visual/"
    "ARMOR-Product-Visual-Standard-v1.0.md"
)


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ROUTER_MODULE = load_module(ROUTER, "phase5e_armor_route")
MCP_MODULE = load_module(SCOPED_MCP, "phase5e_scoped_vault_mcp")


def standard_path() -> Path | None:
    raw = os.environ.get("ARMOR_VAULT_ROOT", "").strip()
    return Path(raw) / STANDARD_RELATIVE if raw else None


def visual_files() -> dict[str, str]:
    return {
        "visual-source-map.yaml": """product_id: SLIM-213BWRY
sources:
  - id: esl-v26-original-datasheet
    kind: authoritative-original-datasheet
    authority: authoritative_original
    identity_relation: same_product
  - id: esl-v27-product-knowledge
    kind: derived-product-knowledge
    authority: verified_product_knowledge
    identity_relation: same_product
  - id: esl-screen-reference
    kind: supplied-source-image
    authority: observable_source_image
    identity_relation: same_product
facts:
  model: {value: SLIM-213BWRY, class: AUTHORITATIVE_PRODUCT_FACT}
  dimensions: {value: 72.31x34.31x9.1 mm, class: AUTHORITATIVE_PRODUCT_FACT}
  display: {value: 250x128 Full Graphic E-Ink, class: AUTHORITATIVE_PRODUCT_FACT}
unknowns:
  - generated_screen_text
conflicts: []
asset_provenance:
  - id: slim-213bwry-source-image
    class: REAL_SOURCE_ASSET
    locator: supplied/SLIM-213BWRY.jpg
""",
        "visual-brief.md": """# Visual Brief

visual_objective: Prepare a close-up source-grounded ESL product visual handoff.
channel_or_use: internal product visual reference for website/social/MIC consumers.
subject: One SLIM-213BWRY electronic shelf label with the supplied source image as reference.
creative_direction: Clean controlled product presentation; do not change the product.
source_constraints: Preserve the verified screen, frame, proportions, and visible geometry.
approval: Simulated review complete for text-only handoff; generation requires separate approval.
""",
        "visual-prompt.md": """# Visual Prompt Handoff

immutable_product_facts:
- model: SLIM-213BWRY
- dimensions: 72.31x34.31x9.1 mm
- display: 250x128 Full Graphic E-Ink

observable_asset_constraints:
- Use the supplied source image only as a REAL_SOURCE_ASSET reference.
- Preserve the visible bezel, screen area, proportions, and product geometry.

scene_and_composition: Close-up of one product, product large in frame, controlled neutral background.
lighting_and_camera: Soft controlled commercial light with natural edge detail and controlled sharpness.
materials_and_environment: Preserve the verified ABS frame appearance; no invented materials.
target_use_and_channel: Internal handoff for later approved channel adaptation.
controlled_text_policy: Do not rely on generated text; add factual text manually after review.
negative_constraints: moire pattern, interference pattern, aliasing, wavy lines, noisy texture, distorted grid, rainbow artifacts.
anti_moire_constraints: Avoid distant dense shelf repetition and pixel-grid emphasis; inspect screen and edges at 100 percent.
unknowns_and_do_not_guess: Do not invent screen text, hidden technical values, certifications, logos, ports, or mounting details.
""",
        "visual-audit.md": """# Visual Audit

provenance: REAL_SOURCE_ASSET reference; no generated or composite asset was created.
qa_status: READY_FOR_GENERATION; image QA is a manual handoff because generation did not run.
identity_check: PASS — source map and original Datasheet identify SLIM-213BWRY.
product_truth_check: PASS — creative direction and inference do not override product facts.
anti_moire_check: PASS — screen/pixel-grid, repetitive structure, sharpness, and 100 percent checks are listed.
unsupported_claim_check: PASS — no fabricated feature, certification, logo, label, or numeric specification.
approval: Simulated approval for text/metadata package only; separate product-owner approval required before any generation or commercial use.
generation_performed: false
publication_performed: false
""",
    }


class ProductVisualTests(unittest.TestCase):
    TECHNICAL_ORDER = {
        "authoritative_original": 0,
        "verified_product_knowledge": 1,
        "weknora_retrieval": 2,
        "current_listing": 3,
    }

    def resolve_technical(self, claims):
        allowed = [claim for claim in claims if claim.get("source") in self.TECHNICAL_ORDER]
        if not allowed:
            return {"status": "UNKNOWN", "value": None}
        best_rank = min(self.TECHNICAL_ORDER[claim["source"]] for claim in allowed)
        best = [claim for claim in allowed if self.TECHNICAL_ORDER[claim["source"]] == best_rank]
        values = {claim["value"] for claim in best}
        if len(values) > 1:
            return {"status": "VISUAL_AUTHORITY_REVIEW_REQUIRED", "value": None}
        return {"status": "SUPPORTED", "value": best[0]["value"]}

    def test_product_facts_beat_creative_direction_and_retrieval(self):
        self.assertEqual(
            self.resolve_technical(
                [
                    {"source": "authoritative_original", "value": "72.31x34.31x9.1 mm"},
                    {"source": "weknora_retrieval", "value": "72x34x9 mm"},
                    {"source": "current_listing", "value": "compact label"},
                    {"source": "creative_direction", "value": "ultra-thin 60 mm"},
                ]
            ),
            {"status": "SUPPORTED", "value": "72.31x34.31x9.1 mm"},
        )
        self.assertEqual(
            self.resolve_technical(
                [
                    {"source": "authoritative_original", "value": "250x128"},
                    {"source": "authoritative_original", "value": "296x128"},
                ]
            )["status"],
            "VISUAL_AUTHORITY_REVIEW_REQUIRED",
        )

    def test_inference_cannot_populate_unknown_numeric_spec(self):
        self.assertEqual(
            self.resolve_technical(
                [{"source": "reasonable_inference", "value": "24V"}]
            ),
            {"status": "UNKNOWN", "value": None},
        )

    def test_router_has_one_cross_channel_product_visual_destination(self):
        result = ROUTER_MODULE.route_request(
            object_type="work-product", domain="products", artifact="product-visual"
        )
        self.assertEqual(result.path, "02-Projects/Workspaces/Products/Product-Visual/")
        self.assertNotIn("Published", result.path)
        completed = subprocess.run(
            [str(WRAPPER), "--object", "work-product", "--domain", "products", "--artifact", "product-visual"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.splitlines()[0], result.path)

    def test_closed_four_file_package_readback_sha_and_no_binary_upload(self):
        files = visual_files()
        with tempfile.TemporaryDirectory() as temp:
            with unittest.mock.patch.dict(os.environ, {"ARMOR_VAULT_ROOT": temp}, clear=False):
                saved = MCP_MODULE._save_product_visual_package(
                    {"package_id": "SLIM-213BWRY Visual Fixture", "files": files}
                )
            package_dir = Path(temp) / saved["relative_path"]
            self.assertEqual(saved["contract"], "ARMOR_Product_Visual_v1.0_four_file_package")
            self.assertTrue(saved["read_back"])
            self.assertEqual({p.name for p in package_dir.iterdir()}, set(files))
            for name, content in files.items():
                target = package_dir / name
                self.assertEqual(target.read_text(encoding="utf-8"), content)
                self.assertEqual(saved["sha256"][name], hashlib.sha256(target.read_bytes()).hexdigest())

    def test_contract_traversal_and_symlink_fail_closed(self):
        files = visual_files()
        with tempfile.TemporaryDirectory() as temp:
            with unittest.mock.patch.dict(os.environ, {"ARMOR_VAULT_ROOT": temp}, clear=False):
                with self.assertRaises(MCP_MODULE.ScopedVaultError):
                    MCP_MODULE._save_product_visual_package(
                        {"package_id": "fixture", "files": {**files, "asset.png": "binary"}}
                    )
                with self.assertRaises(MCP_MODULE.ScopedVaultError):
                    MCP_MODULE._save_product_visual_package(
                        {"package_id": "../escape", "files": files}
                    )
                root = Path(temp)
                destination = root / "02-Projects/Workspaces/Products/Product-Visual"
                destination.mkdir(parents=True)
                outside = Path(temp).parent / f"phase5e-outside-{Path(temp).name}"
                outside.mkdir()
                (destination / "symlink-fixture").symlink_to(outside, target_is_directory=True)
                with self.assertRaises(MCP_MODULE.ScopedVaultError):
                    MCP_MODULE._save_product_visual_package(
                        {"package_id": "symlink-fixture", "files": files}
                    )
                outside.rmdir()

    def test_single_entrypoint_standard_and_runtime_boundaries(self):
        matches = [
            path for path in (ROOT / "skills/shared/department").glob("*/SKILL.md")
            if path.parent.name == "armor-product-visual"
        ]
        self.assertEqual([path.parent.name for path in matches], ["armor-product-visual"])
        self.assertTrue(SKILL.is_file())
        standard = standard_path()
        self.assertIsNotNone(standard)
        self.assertTrue(standard.is_file())
        skill_text = SKILL.read_text(encoding="utf-8")
        standard_text = standard.read_text(encoding="utf-8") if standard else ""
        self.assertIn("save_product_visual_package", skill_text)
        self.assertIn("READY_FOR_GENERATION", skill_text)
        self.assertIn("anti-moiré", standard_text)
        self.assertIn("1. authoritative original Datasheet", standard_text)
        self.assertIn("2. canonical or explicitly verified Product Knowledge", standard_text)
        self.assertIn("3. read-only WeKnora retrieval", standard_text)
        self.assertIn("4. current website or MIC listing", standard_text)
        self.assertIn("REAL_SOURCE_ASSET", standard_text)
        self.assertIn("GENERATED_ASSET", standard_text)
        self.assertIn("may not populate a numeric", standard_text)
        self.assertIn("image generation is disabled", standard_text.lower())
        self.assertIn("Agent Delegate", standard_text)
        self.assertNotIn(str(Path.home()), skill_text)
        self.assertNotIn(str(Path.home()), standard_text)

    def test_mcp_exposes_product_visual_without_changing_existing_contracts(self):
        self.assertEqual(
            {tool["name"] for tool in MCP_MODULE.TOOLS},
            {
                "route_work_product",
                "save_article_package",
                "save_social_package",
                "save_mic_product_package",
                "save_website_product_materials_package",
                "save_product_visual_package",
            },
        )
        self.assertEqual(
            MCP_MODULE.ARTICLE_FILES,
            {"article-brief.json", "seo-blueprint.json", "article.md", "audit-report.md"},
        )
        self.assertEqual(
            MCP_MODULE.SOCIAL_REQUIRED_FILES,
            {"topic-brief.yaml", "core-draft.md", "social-copy.md", "audit-report.md"},
        )
        self.assertEqual(
            MCP_MODULE.MIC_REQUIRED_FILES,
            {"mic-product-data.yaml", "mic-bulkfill.txt", "mic-audit.md"},
        )
        self.assertEqual(
            MCP_MODULE.PRODUCT_MATERIALS_REQUIRED_FILES,
            {
                "product-source-map.yaml",
                "product-page-content.md",
                "product-seo.md",
                "product-media-plan.md",
                "product-audit.md",
            },
        )

    def test_no_publication_or_image_runtime_tool(self):
        names = {tool["name"] for tool in MCP_MODULE.TOOLS}
        self.assertFalse(any(name in names for name in {"publish", "deploy", "generate_image", "upload_asset"}))
        self.assertIn("not a generic filesystem tool", MCP_MODULE.__doc__.lower())
        config = ROOT / "private/department-profile/config.yaml"
        if config.is_file():
            text = config.read_text(encoding="utf-8")
            self.assertIn("image_gen", text)
            self.assertIn("delegation", text)


if __name__ == "__main__":
    unittest.main()
