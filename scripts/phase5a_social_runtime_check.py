#!/usr/bin/env python3
"""Repository and deployed-runtime acceptance checks for Phase 5A Social."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment diagnostic
    print(f"FAIL: PyYAML is required: {exc}")
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
SOCIAL_SKILL = ROOT / "skills/shared/department/armor-social-media-pipeline/SKILL.md"
VIDEO_SKILL = ROOT / "skills/shared/department/armor-video-content-rules/SKILL.md"
SOCIAL_CONFIG = ROOT / "private/department-profile/config.yaml"
ENABLED_SKILLS = ROOT / "private/department-profile/enabled-skills.csv"
DISABLED_SKILLS = ROOT / "private/department-profile/disabled-skills.csv"
ENABLED_TOOLS = ROOT / "private/department-profile/enabled-tools.csv"
MANIFEST = ROOT / "private/department-profile/.symlink_manifest"
MCP = ROOT / "skills/shared/department/armor-memory/scripts/armor-vault-mcp.py"
ROUTE = ROOT / "skills/shared/department/armor-memory/scripts/route.sh"
REGISTRY = ROOT / "config/mcp-registry.yaml"
PHASE_DOC = ROOT / "docs/PHASE5A-ARMOR-SOCIAL-MEDIA-MIGRATION.md"

SOCIAL_HEADINGS = {
    "## LinkedIn — ARMOR Company",
    "## LinkedIn — Lisa",
    "## Facebook — ARMOR Company",
    "## Facebook — Lisa",
    "## Instagram",
    "## TikTok",
    "## YouTube",
}
SOCIAL_REQUIRED_KEYS = {
    "topic",
    "product",
    "buyer_role",
    "buyer_problem",
    "pillar",
    "funnel",
    "campaign",
    "content_goal",
    "unique_angle",
    "core_claim",
    "proof_points",
    "source_material",
    "source_links",
    "risk_notes",
    "unknowns",
    "hooks",
    "cta",
    "platforms",
    "visual_direction",
    "approval_required",
}


TOPIC_BRIEF = """topic: "How to check magnetic shelf light compatibility before a retail fixture reset"
product: "ARMOR 10x10mm Slim Magnetic LED Shelf Light"
buyer_role: "Retail Fixture Manufacturer"
buyer_problem: "Lighting needs to move when a compatible steel shelf layout changes."
pillar: "Problem-Solution"
funnel: "Consideration"
campaign: "Retail fixture planning"
content_goal: "Help fixture teams check mounting compatibility before choosing a shelf light."
unique_angle: "Treat surface compatibility as the first design check, not an installation detail."
market_signal: "Retail layouts are reset as merchandising plans change."
core_claim: "On ferromagnetic shelf surfaces, a built-in magnetic shelf light can make repositioning easier, provided the surface and electrical requirements are checked first."
proof_points:
  - "The product source describes built-in magnets for tool-free placement."
  - "The mounting source limits magnetic installation to ferromagnetic shelf surfaces."
  - "The practical decision is compatibility before copy or purchase commitment."
source_material:
  - "01-Knowledge/Products/entities/armor-10x10mm-slim-magnetic-led-shelf-light.md"
  - "01-Knowledge/Products/entities/magnetic-mounting-system.md"
source_links: []
risk_notes:
  - "Do not claim that ARMOR manufactures the shelf or that every shelf surface is compatible."
  - "Do not promise labor savings, ROI, or a result without project evidence."
unknowns: []
hooks:
  - "Before choosing a magnetic shelf light, check the shelf surface."
cta: "Learn more about ARMOR retail display lighting at https://www.armorlighting.com"
platforms: [LinkedIn, Facebook, Instagram, TikTok, YouTube]
visual_direction: "Text-overlay product planning card; no unverified footage or visual claim."
approval_required: true
"""


CORE_DRAFT = """Retail fixture teams often focus on the light before checking the shelf. That order can create avoidable rework when a merchandising plan changes.

For a compatible steel fixture, the first question is simple: can the light be repositioned without drilling, adhesive, or a new mounting plan? ARMOR’s 10x10mm Slim Magnetic LED Shelf Light is described with built-in magnets for tool-free placement. The related mounting guidance makes the condition clear: the shelf surface must be ferromagnetic. A magnetic mount is therefore a compatibility decision, not a universal installation promise.

That distinction matters during fixture planning. A team can check the shelf material, confirm the electrical connection, and then decide whether a magnetic bar fits the reset strategy. If the surface is not ferromagnetic, the project needs another mounting approach; the magnetic option should not be presented as a fit.

The useful buyer takeaway is a short pre-purchase check: identify the shelf material, confirm the light dimensions and connection requirements for the project, and keep the intended reset process in view. This keeps a product feature connected to a real installation decision instead of turning it into a generic claim about convenience.

For more information about ARMOR retail display lighting, visit https://www.armorlighting.com.
"""


SOCIAL_COPY = """---
pipeline_version: "2.0"
topic: "Magnetic shelf light compatibility before a retail fixture reset"
product: "ARMOR 10x10mm Slim Magnetic LED Shelf Light"
buyer_role: "Retail Fixture Manufacturer"
pillar: "Problem-Solution"
funnel: "Consideration"
campaign: "Retail fixture planning"
quality_status: DRAFT
---

# ARMOR Social Copy

## Topic Brief

Check the shelf surface before choosing a magnetic shelf light. The fixture must be ferromagnetic for the magnetic mounting method to apply.

## Core Draft

The core draft is stored separately as `core-draft.md` in this controlled package.

## LinkedIn — ARMOR Company

### Post Content

The shelf material is part of the lighting specification.

When a retail fixture layout changes, a magnetic shelf light can make repositioning easier on compatible ferromagnetic surfaces. ARMOR’s 10x10mm Slim Magnetic LED Shelf Light is described with built-in magnets for tool-free placement. The practical check comes first: confirm the shelf material and the project’s electrical requirements before treating the mounting method as a fit.

That small check keeps a product feature tied to a real fixture decision. Learn more about ARMOR retail display lighting: https://www.armorlighting.com #RetailLighting #ShelfLighting #RetailFixtures

## LinkedIn — Lisa

### Post Content

I like to start shelf-lighting conversations with the surface, not the sales claim. If the shelf is ferromagnetic, built-in magnets may make a reset easier to plan. If it is not, the magnetic option is not the right assumption.

For me, the useful buyer question is whether the mounting method matches the fixture and the next layout change. Check the material, confirm the connection requirements, and then compare the light. Explore ARMOR retail display lighting at https://www.armorlighting.com #RetailLighting #StoreDesign #ShelfLighting

## Facebook — ARMOR Company

### Reels Title

Magnetic Shelf Light for Retail Resets

### Post Content

Before choosing a magnetic shelf light, check the shelf surface. On compatible ferromagnetic fixtures, built-in magnets can support a simpler repositioning conversation when layouts change. Learn more at https://www.armorlighting.com #ShelfLighting #RetailDisplay #StoreDesign

### Tags

magnetic shelf light, retail display lighting, store fixture design

## Facebook — Lisa

### Post Content

One practical question I ask early: will the shelf surface work with the mounting method? A magnetic light may be useful on a ferromagnetic fixture, but it is not a universal answer. I share more ARMOR retail lighting guidance at https://www.armorlighting.com #ShelfLighting #RetailLighting

## Instagram

### Post Content

Start with the shelf surface. A magnetic shelf light is a fit only when the fixture is ferromagnetic. Check compatibility before planning the next retail reset. Learn more: https://www.armorlighting.com #MagneticShelfLight #RetailLighting #VisualMerchandising #StoreDesign

## TikTok

### Post Content

The detail to check before a magnetic shelf-light plan: the shelf surface. Ferromagnetic fixture? The mounting method may fit. Not ferromagnetic? Choose another approach. More retail lighting guidance: https://www.armorlighting.com #ShelfLighting #RetailFixtures #StoreDesign

## YouTube

### Title

Magnetic Shelf Light Setup for Steel Retail Shelves | ARMOR

### Description

How should a fixture team check a magnetic shelf light before a retail reset? Start with the shelf surface. This controlled example explains why ferromagnetic compatibility comes before a mounting decision, then connects the check to ARMOR’s retail display lighting. Confirm project-specific dimensions and electrical requirements before purchase. Learn more at https://www.armorlighting.com #MagneticShelfLight #RetailLighting #ShelfLighting

### Tags

magnetic shelf light, steel retail shelf, retail display lighting, shelf lighting

## Audit Handoff

The independent Social audit is recorded in `audit-report.md`; the final Codex editorial pass used `ai-writing-audit v0.3.1` with the `armor` profile.
"""


VIDEO_PACKAGE = """# Video Package

mode: Text Overlay Only
source: Controlled product/topic fixture; no footage claim is made.
rule: Do not infer footage. Confirm the actual shelf surface before showing a magnetic installation.
cards:
  - Hook: Check the shelf surface first.
  - Proof: Magnetic mounting needs ferromagnetic metal.
  - Close: Match the mount to the fixture.
"""


AUDIT_REPORT = """# Social Audit Report

pipeline_version: "2.0"
status: PASS
audit_tool: ai-writing-audit v0.3.1
audit_profile: armor
independent_checks: factual grounding, buyer value, platform adaptation, CTA, limits, approval boundary
approval_simulated: true
approval_note: No real user approval occurred; this isolated fixture simulates the already-approved gate only for save-path testing.
publication_performed: false
"""


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a mapping")
    return value


def check(condition: bool, label: str, failures: list[str]) -> None:
    print(f"{'PASS' if condition else 'FAIL'}: {label}")
    if not condition:
        failures.append(label)


def section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^{re.escape(heading)}\n(.*?)(?=^## |\Z)", text)
    return match.group(1) if match else ""


def quality_check(files: dict[str, str], audit_ok: bool, failures: list[str]) -> None:
    brief = yaml.safe_load(files["topic-brief.yaml"])
    check(isinstance(brief, dict) and SOCIAL_REQUIRED_KEYS <= set(brief), "Social Topic Brief has the full required contract", failures)
    check(brief.get("approval_required") is True, "Social approval remains an explicit gate", failures)
    core_words = re.findall(r"\b[\w'-]+\b", files["core-draft.md"])
    check(180 <= len(core_words) <= 350, "controlled Core Draft is within the 180–350 word guidance", failures)
    copy = files["social-copy.md"]
    for heading in SOCIAL_HEADINGS:
        check(heading in copy, f"Social output contains {heading}", failures)
    platform_sections = {heading: section(copy, heading) for heading in SOCIAL_HEADINGS}
    check(all("https://www.armorlighting.com" in body for body in platform_sections.values()), "every platform variant contains the official website URL", failures)
    check(len({body.strip() for body in platform_sections.values()}) == len(platform_sections), "platform variants are independently adapted", failures)
    lisa_sections = platform_sections["## LinkedIn — Lisa"] + platform_sections["## Facebook — Lisa"]
    check(bool(re.search(r"\b(I|we|our|I've|I'm)\b", lisa_sections, re.IGNORECASE)), "Lisa variants use first-person voice", failures)
    facebook_company = platform_sections["## Facebook — ARMOR Company"]
    reels_title = re.search(r"(?ms)^### Reels Title\n\n(.*?)(?=^### )", facebook_company)
    tags = re.search(r"(?ms)^### Tags\n\n(.*?)(?=^## |\Z)", facebook_company)
    check(reels_title is not None and len(reels_title.group(1).strip()) <= 60, "Facebook Company Reels Title is present and within 60 characters", failures)
    check(tags is not None and "#" not in tags.group(1), "Facebook Company Reels Tags are plain keywords", failures)
    youtube = platform_sections["## YouTube"]
    title = re.search(r"(?ms)^### Title\n\n(.*?)(?=^### )", youtube)
    check(title is not None and len(title.group(1).strip()) <= 100, "YouTube Title is within 100 characters", failures)
    check("[" not in youtube and "]" not in youtube, "YouTube output has no square-bracket placeholders", failures)
    banned = ("game-changing", "revolutionary", "seamlessly", "link in bio", "#B2B", "#OEM", "#ODM", "From chip to shelf")
    check(not any(term.lower() in copy.lower() for term in banned), "Social copy avoids known generic or unsafe claims", failures)
    check("03-Records/Published" not in copy, "Social copy does not use Published as editable source", failures)
    check(audit_ok, "ai-writing-audit v0.3.1 detect completed successfully", failures)
    check("status: PASS" in files["audit-report.md"] and "ai-writing-audit v0.3.1" in files["audit-report.md"], "independent Social audit report is PASS and cites the required audit", failures)
    check("approval_simulated: true" in files["audit-report.md"], "approval boundary is simulated, not falsely claimed", failures)
    check("publication_performed: false" in files["audit-report.md"], "controlled fixture performed no publication", failures)


def run_ai_audit(core_path: Path, social_path: Path, audit_script: Path | None) -> bool:
    if audit_script is None or not audit_script.is_file():
        return False
    for path in (core_path, social_path):
        result = subprocess.run(
            [sys.executable, str(audit_script), str(path), "--mode", "detect", "--language", "auto", "--profile", "armor", "--format", "json"],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            return False
    return True


def social_probe(audit_script: Path | None) -> list[str]:
    failures: list[str] = []
    files = {
        "topic-brief.yaml": TOPIC_BRIEF,
        "core-draft.md": CORE_DRAFT,
        "social-copy.md": SOCIAL_COPY,
        "audit-report.md": AUDIT_REPORT,
        "video-package.md": VIDEO_PACKAGE,
    }
    with tempfile.TemporaryDirectory(prefix="phase5a-social-vault-") as vault_temp, tempfile.TemporaryDirectory(prefix="phase5a-social-input-") as input_temp:
        input_root = Path(input_temp)
        core_path = input_root / "core-draft.md"
        social_path = input_root / "social-copy.md"
        core_path.write_text(CORE_DRAFT, encoding="utf-8")
        social_path.write_text(SOCIAL_COPY, encoding="utf-8")
        audit_ok = run_ai_audit(core_path, social_path, audit_script)
        quality_check(files, audit_ok, failures)
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "route_work_product", "arguments": {"domain": "marketing", "artifact": "social-copy"}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "save_social_package", "arguments": {"package_id": "phase5a-social-fixture", "files": files}}},
        ]
        env = dict(os.environ)
        env["ARMOR_VAULT_ROOT"] = vault_temp
        completed = subprocess.run(
            [sys.executable, str(MCP)],
            input="\n".join(json.dumps(request) for request in requests) + "\n",
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        check(completed.returncode == 0, "Social scoped MCP process exits cleanly", failures)
        try:
            replies = [json.loads(line) for line in completed.stdout.splitlines()]
            names = {tool["name"] for tool in replies[1]["result"]["tools"]}
            route = json.loads(replies[2]["result"]["content"][0]["text"])
            saved = json.loads(replies[3]["result"]["content"][0]["text"])
        except (IndexError, KeyError, TypeError, json.JSONDecodeError) as exc:
            failures.append(f"Social scoped MCP response shape: {exc}")
            print(f"FAIL: Social scoped MCP response shape: {exc}")
            return failures
        check(names == {"route_work_product", "save_article_package", "save_social_package", "save_mic_product_package", "save_website_product_materials_package", "save_product_visual_package"}, "Social MCP exposes the closed Router, Article, Social, MIC, Website Product Materials, and Product Visual tools", failures)
        check(route["relative_path"] == "02-Projects/Workspaces/Marketing/Social-Media/", "Social Router destination is lifecycle-neutral", failures)
        check(saved["read_back"] is True, "Social package read-back verification passes", failures)
        package_dir = Path(vault_temp) / "02-Projects/Workspaces/Marketing/Social-Media/phase5a-social-fixture"
        check(package_dir.is_dir(), "Social package exists under the isolated Vault root", failures)
        check({path.name for path in package_dir.iterdir()} == set(files), "Social package contains only the required and submitted optional files", failures)
        check(not (Path(vault_temp) / "03-Records/Published").exists(), "isolated Social test does not touch Published", failures)
    return failures


def check_repository() -> list[str]:
    failures: list[str] = []
    registry = load_yaml(REGISTRY)
    servers = registry.get("servers", {})
    check(SOCIAL_SKILL.is_file(), "canonical Social Skill exists", failures)
    check(VIDEO_SKILL.is_file(), "canonical video rules Skill exists", failures)
    check(not (ROOT / "skills/shared/department/armor-social-media-workflow").exists(), "duplicate Social workflow Skill is not active", failures)
    social_text = SOCIAL_SKILL.read_text(encoding="utf-8") if SOCIAL_SKILL.is_file() else ""
    check("${ARMOR_VAULT_ROOT}" in social_text, "Social Skill uses the runtime Vault root", failures)
    check("save_social_package" in social_text, "Social Skill declares the scoped Social save operation", failures)
    check("02-Projects/Workspaces/Marketing/Social-Media/" in social_text, "Social Skill uses the lifecycle-neutral Social workspace", failures)
    check("03-Records/Published/Social-Media/" not in social_text, "obsolete Published Social source route is absent", failures)
    check("/Users/licat" not in social_text and "/Users/licat" not in VIDEO_SKILL.read_text(encoding="utf-8"), "active Social Skills have no personal machine paths", failures)
    check("ARMOR_ARCH_ROOT" not in ROUTE.read_text(encoding="utf-8"), "Social uses the closed local Router without ARMOR_ARCH_ROOT", failures)
    check(REGISTRY.is_file() and set(servers) == {"anysearch", "firecrawl-mcp", "obscura", "paddle_ocr", "toolscout", "armor-vault-scoped-router"}, "Phase 4C MCP registry remains complete", failures)
    boundary = servers.get("armor-vault-scoped-router", {}).get("boundary", {})
    check(boundary.get("article_write_scope") == "Article_v1.3_four_file_package_only", "Article scoped write contract is unchanged", failures)
    check(boundary.get("social_write_scope") == "Social_v2.0_required_four_files_plus_optional_video_artifacts", "Social scoped write contract is registered", failures)
    check("save_social_package" in boundary.get("allowed_tools", []), "registry exposes only the named Social save tool", failures)
    check(PHASE_DOC.is_file(), "Phase 5A migration record exists", failures)
    return failures


def check_runtime(runtime_root: Path, hermes_home: Path, vault_root: Path) -> list[str]:
    failures = check_repository()
    config = load_yaml(runtime_root / "config.yaml")
    mcp = config.get("mcp_servers", {})
    check({"weknora", "toolscout", "firecrawl-mcp", "armor-vault-scoped-router"} <= set(mcp), "Operations exposes the approved MCP set", failures)
    check(not ({"anysearch", "obscura", "paddle_ocr"} & set(mcp)), "Operations does not expose Anysearch, Obscura, or PaddleOCR", failures)
    check(config.get("memory", {}).get("memory_enabled") is False and config.get("memory", {}).get("user_profile_enabled") is False, "Operations Hermes Memory remains OFF", failures)
    disabled = set(config.get("agent", {}).get("disabled_toolsets", []))
    check({"terminal", "file", "browser", "code_execution", "delegation", "memory"} <= disabled, "generic execution boundaries remain disabled", failures)
    router_include = mcp.get("armor-vault-scoped-router", {}).get("tools", {}).get("include", [])
    check(set(router_include) == {"route_work_product", "save_article_package", "save_social_package", "save_mic_product_package", "save_website_product_materials_package", "save_product_visual_package"}, "Operations receives the exact scoped Router tool allowlist", failures)
    profile_skills = hermes_home / "profiles/operations/skills"
    social_link = profile_skills / "armor-social-media-pipeline"
    video_link = profile_skills / "armor-video-content-rules"
    check(social_link.is_symlink() and social_link.resolve() == SOCIAL_SKILL.parent.resolve(), "Operations exposes the canonical Social Skill by symlink", failures)
    check(video_link.is_symlink() and video_link.resolve() == VIDEO_SKILL.parent.resolve(), "Operations exposes canonical video rules by symlink", failures)
    check(not (profile_skills / "armor-social-media-workflow").exists(), "Operations has no competing compatibility workflow Skill", failures)
    enabled_text = ENABLED_SKILLS.read_text(encoding="utf-8")
    disabled_text = DISABLED_SKILLS.read_text(encoding="utf-8")
    check("armor-social-media-pipeline,PRIVILEGED_OR_EXTERNAL" in enabled_text, "Social Skill is enabled in the curated Operations manifest", failures)
    check("armor-social-media-pipeline," not in disabled_text, "Social Skill is removed from the disabled manifest", failures)
    check("armor-social-media-pipeline ->" in MANIFEST.read_text(encoding="utf-8"), "Social Skill symlink is recorded in the profile manifest", failures)
    check("save_social_package" in ENABLED_TOOLS.read_text(encoding="utf-8"), "Social scoped save is recorded in the enabled tool manifest", failures)
    check(vault_root.is_dir(), "Enterprise Vault root is readable", failures)
    env = dict(os.environ)
    env.pop("ARMOR_ARCH_ROOT", None)
    env["ARMOR_VAULT_ROOT"] = str(vault_root)
    route_result = subprocess.run([str(ROUTE), "--object", "work-product", "--domain", "marketing", "--artifact", "social-copy"], text=True, capture_output=True, env=env, check=False)
    check(route_result.returncode == 0 and route_result.stdout.splitlines()[0] == "02-Projects/Workspaces/Marketing/Social-Media/", "deployed Social Router resolves the canonical destination", failures)
    audit_script = profile_skills / "ai-writing-audit/scripts/audit.py"
    failures.extend(social_probe(audit_script))
    return failures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", type=Path)
    parser.add_argument("--hermes-home", type=Path)
    parser.add_argument("--vault-root", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    supplied = (args.runtime_root, args.hermes_home, args.vault_root)
    if any(value is not None for value in supplied) and not all(value is not None for value in supplied):
        print("FAIL: runtime-root, hermes-home, and vault-root must be supplied together")
        return 2
    failures = check_runtime(*supplied) if all(value is not None for value in supplied) else check_repository()
    if failures:
        print(f"Phase 5A Social runtime check: {len(failures)} failure(s)")
        return 2
    print("Phase 5A Social runtime check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
