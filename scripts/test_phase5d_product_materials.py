#!/usr/bin/env python3
"""Offline tests for the Phase 5D Website Product Materials boundary."""

from __future__ import annotations

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
SKILL = ROOT / "skills/shared/department/armor-website-product-materials/SKILL.md"


def vault_standard_path() -> Path | None:
    raw_root = os.environ.get("ARMOR_VAULT_ROOT", "").strip()
    if not raw_root:
        return None
    return Path(raw_root) / "02-Projects/Workspaces/Website/Product-Materials/ARMOR-Website-Product-Materials-Standard-v1.0.md"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ROUTER_MODULE = load_module(ROUTER, "phase5d_armor_route")
MCP_MODULE = load_module(SCOPED_MCP, "phase5d_scoped_vault_mcp")


def product_files() -> dict[str, str]:
    return {
        "product-source-map.yaml": """product_id: armor-hm-sx64f010w24-2835
sources:
  - id: hm-sx64-datasheet
    kind: authoritative-original-datasheet
    authority: authoritative
    identity_relation: same_product
  - id: website-wp-365
    kind: current-website-evidence
    authority: evidence
    identity_relation: same_product
  - id: historical-mic
    kind: historical-mic-record
    authority: evidence
    identity_relation: historical_or_unknown
facts:
  model: {value: HM-SX64F010W24-2835, status: authority_readback_required}
unknowns:
  - exact_technical_values_until_original_document_is_read_back
conflicts:
  - code: PRODUCT_AUTHORITY_REVIEW_REQUIRED
    field: technical_values
    reason: original PDF is present but readback is required before publication
""",
        "product-page-content.md": """# Product Page Content

## Page brief

ARMOR high-efficient LED flexible strip light for retail display applications.

## Source-grounded content

The product-page proposal is limited to source-supported positioning. Confirm
the exact technical values from the original Datasheet before publication.

## Website Product schema mapping

- `system`: Retail Lighting
- `family`: LED Strip Lights
- `subfamily`: SMD / Standard LED Strips
- `sourceId`: 365
""",
        "product-seo.md": """# Product SEO

- Proposed title: High Efficient LED Flexible Strip Light | ARMOR Lighting
- Proposed permalink: `/product/high-efficient-led-flexible-strip-light-2835-64leds-m`
- Meta description: Source-grounded product-page proposal for ARMOR's slim
  flexible LED strip light for retail display; exact technical values remain
  under review.
- Keywords/entities: LED flexible strip light, SMD2835, retail display
  lighting.
""",
        "product-media-plan.md": """# Product Media Plan

- Existing evidence: current product-page hero, gallery images, and linked
  Datasheet path.
- Missing: readable original technical-document readback and verified current
  model-labelled image, if required by the website owner.
- Shot list: front profile, cut/connector detail, installed retail context,
  scale reference, and model-labelled packaging if available.
- Alt text must describe only visible form, mounting, finish, and context.
""",
        "product-audit.md": """# Product Audit

- Status: READY_FOR_REVIEW
- Blocker: PRODUCT_AUTHORITY_REVIEW_REQUIRED until the original Datasheet is
  readable and reconciled.
- Unknown numeric/technical values remain unknown and are not public claims.
- Historical MIC and website values are evidence only.
- Publication performed: false
- Website repository modified: false
- Agent Delegate/Multi-Agent Orchestration: OFF
""",
    }


class WebsiteProductMaterialsTests(unittest.TestCase):
    TECHNICAL_ORDER = {
        "authoritative_original": 0,
        "canonical_verified": 1,
        "weknora_retrieval": 2,
        "current_listing": 3,
        "historical_mic": 4,
    }

    def resolve_technical(self, claims):
        """Acceptance oracle for the Standard's source-authority ordering."""
        allowed = [claim for claim in claims if claim.get("source") in self.TECHNICAL_ORDER]
        if not allowed:
            return {"status": "UNKNOWN", "value": None}
        ranked = sorted(allowed, key=lambda claim: self.TECHNICAL_ORDER[claim["source"]])
        best_rank = self.TECHNICAL_ORDER[ranked[0]["source"]]
        best = [claim for claim in ranked if self.TECHNICAL_ORDER[claim["source"]] == best_rank]
        values = {claim["value"] for claim in best}
        if len(values) > 1:
            return {"status": "PRODUCT_AUTHORITY_REVIEW_REQUIRED", "value": None}
        return {"status": "SUPPORTED", "value": ranked[0]["value"]}

    def resolve_commercial(self, claims):
        """Acceptance oracle for current commercial confirmation precedence."""
        order = {"current_confirmation": 0, "approved_commercial": 1, "historical_mic": 2}
        if not claims:
            return {"status": "UNKNOWN", "value": None}
        winner = min(claims, key=lambda claim: order[claim["source"]])
        return {"status": "SUPPORTED", "value": winner["value"]}

    def test_authority_oracle_enforces_source_hierarchy(self):
        self.assertEqual(
            self.resolve_technical(
                [
                    {"source": "authoritative_original", "value": "12W"},
                    {"source": "weknora_retrieval", "value": "10W"},
                    {"source": "historical_mic", "value": "8W"},
                ]
            ),
            {"status": "SUPPORTED", "value": "12W"},
        )
        self.assertEqual(
            self.resolve_technical([{"source": "weknora_retrieval", "value": "10W"}]),
            {"status": "SUPPORTED", "value": "10W"},
        )
        self.assertEqual(
            self.resolve_technical(
                [
                    {"source": "authoritative_original", "value": "12W"},
                    {"source": "authoritative_original", "value": "10W"},
                ]
            )["status"],
            "PRODUCT_AUTHORITY_REVIEW_REQUIRED",
        )
        self.assertEqual(
            self.resolve_commercial(
                [
                    {"source": "historical_mic", "value": "MOQ 100"},
                    {"source": "current_confirmation", "value": "MOQ 50"},
                ]
            )["value"],
            "MOQ 50",
        )
        self.assertEqual(
            self.resolve_technical([{"source": "reasonable_inference", "value": "24V"}]),
            {"status": "UNKNOWN", "value": None},
        )
        self.assertEqual(self.resolve_technical([]), {"status": "UNKNOWN", "value": None})

    def test_router_has_one_semantically_correct_destination(self):
        result = ROUTER_MODULE.route_request(
            object_type="work-product", domain="website", artifact="product-materials"
        )
        self.assertEqual(result.path, "02-Projects/Workspaces/Website/Product-Materials/")
        env = dict(os.environ)
        env.pop("ARMOR_ARCH_ROOT", None)
        completed = subprocess.run(
            [str(WRAPPER), "--object", "work-product", "--domain", "website", "--artifact", "product-materials"],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.splitlines()[0], result.path)

    def test_closed_five_file_package_readback_and_sha(self):
        files = product_files()
        with tempfile.TemporaryDirectory() as temp:
            with unittest.mock.patch.dict(os.environ, {"ARMOR_VAULT_ROOT": temp}, clear=False):
                saved = MCP_MODULE._save_website_product_materials_package(
                    {"package_id": "ARMOR 10x10 Fixture", "files": files}
                )
            package_dir = Path(temp) / saved["relative_path"]
            self.assertEqual(saved["contract"], "Website_Product_Materials_v1.0_five_file_package")
            self.assertTrue(saved["read_back"])
            self.assertEqual({p.name for p in package_dir.iterdir()}, set(files))
            self.assertEqual(set(saved["sha256"]), set(files))
            for name, content in files.items():
                self.assertEqual((package_dir / name).read_text(encoding="utf-8"), content)

    def test_contract_identity_traversal_and_symlink_fail_closed(self):
        files = product_files()
        with tempfile.TemporaryDirectory() as temp:
            with unittest.mock.patch.dict(os.environ, {"ARMOR_VAULT_ROOT": temp}, clear=False):
                with self.assertRaises(MCP_MODULE.ScopedVaultError):
                    MCP_MODULE._save_website_product_materials_package(
                        {"package_id": "fixture", "files": {**files, "extra.md": "x"}}
                    )
                with self.assertRaises(MCP_MODULE.ScopedVaultError):
                    MCP_MODULE._save_website_product_materials_package(
                        {"package_id": "../escape", "files": files}
                    )
                root = Path(temp)
                destination = root / "02-Projects/Workspaces/Website/Product-Materials"
                destination.mkdir(parents=True)
                outside = Path(temp).parent / f"phase5d-outside-{Path(temp).name}"
                outside.mkdir()
                (destination / "symlink-fixture").symlink_to(outside, target_is_directory=True)
                with self.assertRaises(MCP_MODULE.ScopedVaultError):
                    MCP_MODULE._save_website_product_materials_package(
                        {"package_id": "symlink-fixture", "files": files}
                    )
                outside.rmdir()

    def test_mcp_exposes_new_tool_without_changing_old_closed_contracts(self):
        names = {tool["name"] for tool in MCP_MODULE.TOOLS}
        self.assertEqual(
            names,
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
            MCP_MODULE.MIC_REQUIRED_FILES,
            {"mic-product-data.yaml", "mic-bulkfill.txt", "mic-audit.md"},
        )

    def test_website_repo_is_read_only_and_publication_is_not_a_tool(self):
        skill = SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("website repository", skill)
        self.assertIn("read-only evidence", skill)
        names = {tool["name"] for tool in MCP_MODULE.TOOLS}
        self.assertFalse(any(name in names for name in {"publish", "deploy", "publish_product_page"}))
        self.assertIn("not a generic filesystem tool", MCP_MODULE.__doc__.lower())

    def test_single_entrypoint_and_no_personal_runtime_path(self):
        active = list((ROOT / "skills/shared/department").glob("*/SKILL.md"))
        matching = [path for path in active if "product-materials" in path.parent.name]
        self.assertEqual([path.parent.name for path in matching], ["armor-website-product-materials"])
        personal_home = str(Path.home())
        for path in (SKILL, ROUTER, SCOPED_MCP, ROOT / "config/mcp-registry.yaml"):
            self.assertNotIn(personal_home, path.read_text(encoding="utf-8"))

    def test_authority_unknown_and_non_publication_rules_are_present(self):
        skill = SKILL.read_text(encoding="utf-8")
        standard_path = vault_standard_path()
        if standard_path is None or not standard_path.is_file():
            self.skipTest("ARMOR_VAULT_ROOT is not bound to a readable Vault Standard")
        standard = standard_path.read_text(encoding="utf-8")
        for text in (skill, standard):
            self.assertIn("PRODUCT_AUTHORITY_REVIEW_REQUIRED", text)
            self.assertIn("WeKnora", text)
            self.assertIn("unknown", text.lower())
            self.assertIn("do not", text.lower())
        self.assertIn("1. authoritative original Datasheet", standard)
        self.assertIn("2. canonical or explicitly verified Product Knowledge", standard)
        self.assertIn("3. WeKnora retrieval", standard)
        self.assertIn("4. current MIC or website listing", standard)
        self.assertIn("no-publication", skill.lower())
        self.assertIn("Agent Delegate/Multi-Agent Orchestration", skill)


if __name__ == "__main__":
    unittest.main()
