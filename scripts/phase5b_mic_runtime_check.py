#!/usr/bin/env python3
"""Repository and deployed-runtime acceptance checks for Phase 5B MIC."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment diagnostic
    print(f"FAIL: PyYAML is required: {exc}")
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
MIC_SKILL = ROOT / "skills/shared/department/armor-mic-product-optimization/SKILL.md"
OLD_MIC_SKILL = ROOT / "skills/shared/department/mic-product-fill"
MCP = ROOT / "skills/shared/department/armor-memory/scripts/armor-vault-mcp.py"
ROUTER = ROOT / "skills/shared/department/armor-memory/scripts/armor-route.py"
ROUTE = ROOT / "skills/shared/department/armor-memory/scripts/route.sh"
REGISTRY = ROOT / "config/mcp-registry.yaml"
CONFIG = ROOT / "private/department-profile/config.yaml"
ENABLED_SKILLS = ROOT / "private/department-profile/enabled-skills.csv"
DISABLED_SKILLS = ROOT / "private/department-profile/disabled-skills.csv"
ENABLED_TOOLS = ROOT / "private/department-profile/enabled-tools.csv"
MANIFEST = ROOT / "private/department-profile/.symlink_manifest"
PHASE_DOC = ROOT / "docs/PHASE5B-ARMOR-MIC-PRODUCT-OPTIMIZATION-MIGRATION.md"
DEDUP_DOC = ROOT / "docs/PHASE5B.2-MIC-SKILL-VAULT-AUTHORITY-DEDUPLICATION.md"
TESTS = ROOT / "scripts/test_phase5b_mic.py"
AUTHORITY_TESTS = ROOT / "scripts/test_phase5b1_mic_authority.py"
AUTHORITY_DEDUP_TESTS = ROOT / "scripts/test_phase5b2_mic_authority_dedup.py"
MIC_STANDARD_RELATIVE = Path(
    "02-Projects/Workspaces/Products/MIC-Products/"
    "ARMOR-MIC-Product-Optimization-Standard-v1.0.md"
)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a mapping")
    return value


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def check(condition: bool, label: str, failures: list[str]) -> None:
    print(f"{'PASS' if condition else 'FAIL'}: {label}")
    if not condition:
        failures.append(label)


def resolve_canonical_mic_standard(vault_root: Path) -> Path:
    standard = vault_root / MIC_STANDARD_RELATIVE
    if not standard.is_file():
        raise FileNotFoundError(f"canonical MIC standard unavailable: {standard}")
    return standard


def check_repository() -> list[str]:
    failures: list[str] = []
    registry = load_yaml(REGISTRY)
    servers = registry.get("servers", {})
    skill_text = MIC_SKILL.read_text(encoding="utf-8") if MIC_SKILL.is_file() else ""
    normalized_skill_text = " ".join(skill_text.split())
    check(MIC_SKILL.is_file(), "canonical MIC Skill exists", failures)
    check(not OLD_MIC_SKILL.exists(), "legacy shared mic-product-fill entrypoint is removed", failures)
    check("save_mic_product_package" in skill_text, "MIC Skill declares the scoped save operation", failures)
    check("mic-product-edit-context/v1" in skill_text, "MIC Skill honors current edit-page extraction", failures)
    check("BLOCKED_SOURCE" in skill_text, "MIC Skill fails closed when the canonical Standard is unavailable", failures)
    check("MIC_AUTHORITY_REVIEW_REQUIRED" in skill_text, "MIC Skill has explicit authority-conflict state", failures)
    check("UNKNOWN" in skill_text and "Exact technical values must ultimately resolve" in normalized_skill_text, "MIC Skill keeps concise fact safety invariants", failures)
    check("$ARMOR_VAULT_ROOT" in skill_text and "ARMOR-MIC-Product-Optimization-Standard-v1.0.md" in skill_text, "MIC Skill resolves the canonical Vault Standard", failures)
    check("BLOCKED_SOURCE" in skill_text and "Never silently fall back" in skill_text, "MIC Standard lookup fails closed", failures)
    check("## Type-aware authority rules" not in skill_text and "### Exact product technical facts" not in skill_text, "MIC Skill does not embed the detailed SOP", failures)
    check("03-Records/Published" not in skill_text, "MIC Skill does not use Published as editable source", failures)
    check("/Users/licat" not in skill_text, "canonical MIC Skill has no personal machine paths", failures)
    check(not (ROOT / "skills/shared/department/mic-product-audit").exists(), "no duplicate shared MIC audit workflow is active", failures)
    check(not (ROOT / "skills/shared/department/mic-product-detail-page").exists(), "no duplicate shared MIC detail workflow is active", failures)
    check(PHASE_DOC.is_file(), "Phase 5B migration record exists", failures)
    check(DEDUP_DOC.is_file(), "Phase 5B.2 de-duplication record exists", failures)
    check(TESTS.is_file(), "Phase 5B MIC tests exist", failures)
    check(AUTHORITY_TESTS.is_file(), "Phase 5B.1 authority regression tests exist", failures)
    check(AUTHORITY_DEDUP_TESTS.is_file(), "Phase 5B.2 authority de-duplication tests exist", failures)
    check(MCP.is_file() and "MIC_REQUIRED_FILES" in MCP.read_text(encoding="utf-8"), "scoped MIC package contract is present", failures)
    check("save_mic_product_package" in MCP.read_text(encoding="utf-8"), "scoped MIC save tool is implemented", failures)
    check("mic-product" in ROUTER.read_text(encoding="utf-8"), "Router has the closed mic-product artifact", failures)
    check(REGISTRY.is_file() and set(servers) == {"anysearch", "firecrawl-mcp", "obscura", "paddle_ocr", "toolscout", "armor-vault-scoped-router"}, "MCP registry remains complete", failures)
    boundary = servers.get("armor-vault-scoped-router", {}).get("boundary", {})
    check(boundary.get("mic_product_write_scope") == "MIC_v1.0_required_data_bulkfill_audit_optional_detail_package", "MIC write boundary is registered", failures)
    check("save_mic_product_package" in boundary.get("allowed_tools", []), "registry exposes the named MIC save tool", failures)
    check("ARMOR-MIC-Product-Optimization-Standard-v1.0.md" in skill_text, "MIC Skill references the canonical detailed standard", failures)
    check("automatic" in skill_text.lower() and "live MIC listing" in skill_text, "MIC Skill documents the no-automatic-edit boundary", failures)
    profile_files = (ENABLED_SKILLS, DISABLED_SKILLS, ENABLED_TOOLS, MANIFEST, CONFIG)
    check(all(path.is_file() for path in profile_files), "private Operations profile manifests are available", failures)
    if all(path.is_file() for path in profile_files):
        enabled_skills = ENABLED_SKILLS.read_text(encoding="utf-8")
        disabled_skills = DISABLED_SKILLS.read_text(encoding="utf-8")
        enabled_tools = ENABLED_TOOLS.read_text(encoding="utf-8")
        manifest = MANIFEST.read_text(encoding="utf-8")
        config = load_yaml(CONFIG)
        check("armor-mic-product-optimization,PRIVILEGED_OR_EXTERNAL" in enabled_skills, "Operations enables canonical MIC Skill", failures)
        check("mic-product-fill," not in disabled_skills, "Operations has no disabled duplicate MIC workflow", failures)
        check("save_mic_product_package" in enabled_tools and "armor-mic-product-optimization ->" in manifest, "Operations records scoped MIC save", failures)
        check(config.get("memory", {}).get("memory_enabled") is False and config.get("memory", {}).get("user_profile_enabled") is False, "Operations Hermes Memory remains OFF", failures)
    return failures


def check_runtime(runtime_root: Path, hermes_home: Path, vault_root: Path) -> list[str]:
    failures = check_repository()
    config = load_yaml(runtime_root / "config.yaml")
    mcp = config.get("mcp_servers", {})
    check({"weknora", "toolscout", "firecrawl-mcp", "armor-vault-scoped-router"} <= set(mcp), "Operations exposes WeKnora, ToolScout, Firecrawl, and scoped Router", failures)
    check(not ({"anysearch", "obscura", "paddle_ocr"} & set(mcp)), "Operations does not expose Anysearch, Obscura, or PaddleOCR", failures)
    check(config.get("memory", {}).get("memory_enabled") is False and config.get("memory", {}).get("user_profile_enabled") is False, "deployed Operations Hermes Memory remains OFF", failures)
    disabled = set(config.get("agent", {}).get("disabled_toolsets", []))
    check({"terminal", "file", "browser", "code_execution", "delegation", "memory"} <= disabled, "generic execution boundaries remain disabled", failures)
    include = mcp.get("armor-vault-scoped-router", {}).get("tools", {}).get("include", [])
    check(set(include) == {"route_work_product", "save_article_package", "save_social_package", "save_mic_product_package", "save_website_product_materials_package"}, "Operations receives the exact five-tool scoped Router allowlist", failures)
    profile_skills = hermes_home / "profiles/operations/skills"
    mic_link = profile_skills / "armor-mic-product-optimization"
    check(mic_link.is_symlink() and mic_link.resolve() == MIC_SKILL.parent.resolve(), "Operations exposes canonical MIC Skill by symlink", failures)
    check(not (profile_skills / "mic-product-fill").exists(), "Operations has no Legacy MIC fill symlink", failures)
    check(vault_root.is_dir(), "Enterprise Vault root is readable", failures)
    standard = vault_root / MIC_STANDARD_RELATIVE
    try:
        standard = resolve_canonical_mic_standard(vault_root)
    except FileNotFoundError:
        check(False, "deployed canonical MIC standard is readable", failures)
        standard_text = ""
    else:
        standard_text = standard.read_text(encoding="utf-8")
    normalized_standard_text = " ".join(standard_text.split())
    check("### Exact product technical facts" in standard_text and "1. authoritative original Datasheet" in normalized_standard_text, "deployed MIC standard has the corrected technical hierarchy", failures)
    check("3. read-only WeKnora retrieval" in normalized_standard_text and "never as final technical authority" in normalized_standard_text, "deployed MIC standard keeps WeKnora retrieval-only", failures)
    check("current explicit company or user confirmation" in normalized_standard_text and "may supersede historical MIC listing data" in normalized_standard_text, "deployed MIC standard has the current commercial rule", failures)
    check("REASONABLE_INFERENCE` may improve wording" in normalized_standard_text and "cannot create numeric facts" in normalized_standard_text, "deployed MIC standard blocks numeric inference", failures)
    env = dict(__import__("os").environ)
    env["ARMOR_VAULT_ROOT"] = str(vault_root)
    env["ARMOR_OPERATIONS_ROOT"] = str(hermes_home / "profiles/operations")
    route_result = subprocess.run([str(ROUTE), "--object", "work-product", "--domain", "products", "--artifact", "mic-product"], text=True, capture_output=True, env=env, check=False)
    check(route_result.returncode == 0 and route_result.stdout.splitlines()[0] == "02-Projects/Workspaces/Products/MIC-Products/", "deployed MIC Router resolves the canonical workspace", failures)
    completed = subprocess.run([sys.executable, str(TESTS)], text=True, capture_output=True, check=False)
    check(completed.returncode == 0, "deployed scoped MIC MCP passes the real-product acceptance fixture", failures)
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
    authority = subprocess.run([sys.executable, str(AUTHORITY_TESTS)], text=True, capture_output=True, env=env, check=False)
    check(authority.returncode == 0, "deployed MIC authority regression tests pass", failures)
    if authority.returncode != 0:
        print(authority.stdout)
        print(authority.stderr)
    dedup = subprocess.run([sys.executable, str(AUTHORITY_DEDUP_TESTS)], text=True, capture_output=True, env=env, check=False)
    check(dedup.returncode == 0, "deployed MIC authority de-duplication tests pass", failures)
    if dedup.returncode != 0:
        print(dedup.stdout)
        print(dedup.stderr)
    return failures


def build_parser():
    import argparse

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
        print(f"Phase 5B MIC runtime check: {len(failures)} failure(s)")
        return 2
    print("Phase 5B MIC runtime check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
