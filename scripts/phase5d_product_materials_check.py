#!/usr/bin/env python3
"""Repository and optional Operations checks for Phase 5D."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment diagnostic
    print(f"FAIL: PyYAML is required for runtime checks: {exc}")
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "skills/shared/department/armor-memory/scripts/armor-route.py"
SCOPED_MCP = ROOT / "skills/shared/department/armor-memory/scripts/armor-vault-mcp.py"
SKILL = ROOT / "skills/shared/department/armor-website-product-materials/SKILL.md"
TOOLS = {
    "route_work_product",
    "save_article_package",
    "save_social_package",
    "save_mic_product_package",
    "save_website_product_materials_package",
}


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


def check_repository() -> list[str]:
    failures: list[str] = []
    vault_root_raw = os.environ.get("ARMOR_VAULT_ROOT", "").strip()
    standard = (
        Path(vault_root_raw)
        / "02-Projects/Workspaces/Website/Product-Materials/ARMOR-Website-Product-Materials-Standard-v1.0.md"
        if vault_root_raw
        else None
    )
    check(ROUTER.is_file(), "Enterprise Product Materials Router exists", failures)
    check(SCOPED_MCP.is_file(), "scoped Vault MCP exists", failures)
    check(SKILL.is_file(), "canonical Product Materials Skill exists", failures)
    check(standard is not None and standard.is_file(), "canonical Product Materials Standard exists", failures)
    if ROUTER.is_file():
        route = subprocess.run(
            [sys.executable, str(ROUTER), "--object", "work-product", "--domain", "website", "--artifact", "product-materials"],
            text=True,
            capture_output=True,
            check=False,
        )
        check(
            route.returncode == 0
            and route.stdout.splitlines()[0]
            == "02-Projects/Workspaces/Website/Product-Materials/",
            "Router resolves the Website Product Materials workspace",
            failures,
        )
    if SCOPED_MCP.is_file():
        text = SCOPED_MCP.read_text(encoding="utf-8")
        check("save_website_product_materials_package" in text, "scoped Product Materials save tool is present", failures)
        check("PRODUCT_MATERIALS_REQUIRED_FILES" in text, "Product Materials closed contract is present", failures)
        check("Published evidence cannot be" in text, "scoped MCP rejects Published source writes", failures)
    if SKILL.is_file():
        text = SKILL.read_text(encoding="utf-8")
        check("ARMOR-Website-Product-Materials-Standard-v1.0.md" in text, "Skill references the canonical Vault Standard", failures)
        check("save_website_product_materials_package" in text, "Skill binds the scoped save boundary", failures)
        check("PRODUCT_AUTHORITY_REVIEW_REQUIRED" in text, "Skill has the product authority blocker", failures)
        check("WeKnora retrieval" in text and "not final technical authority" in text, "Skill keeps WeKnora retrieval-only", failures)
        check("Agent Delegate/Multi-Agent Orchestration" in text, "Skill keeps Delegate runtime out of scope", failures)
        check(str(Path.home()) not in text, "Skill has no personal runtime path", failures)
    if standard is not None and standard.is_file():
        text = standard.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        check("authority: canonical" in text, "Product Materials Standard is canonical", failures)
        check("1. authoritative original Datasheet" in normalized, "original documents are first technical authority", failures)
        check("2. canonical or explicitly verified Product Knowledge" in normalized, "verified Product Knowledge is second authority", failures)
        check("3. WeKnora retrieval" in normalized and "never a final technical authority" in normalized, "WeKnora is retrieval-only", failures)
        check("4. current MIC or website listing" in normalized and "evidence only" in normalized, "current listings remain evidence", failures)
        check("current company/user confirmation" in normalized and "supersede historical" in normalized, "current commercial confirmation rule exists", failures)
        check("REASONABLE_INFERENCE" in text and "may not create numeric facts" in normalized, "inference cannot create technical values", failures)
        check("save_website_product_materials_package" in text and "exactly these five" in normalized, "closed package is documented", failures)
        check(str(Path.home()) not in text, "Standard has no personal runtime path", failures)
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts/test_phase5d_product_materials.py")],
        text=True,
        capture_output=True,
        check=False,
    )
    check(completed.returncode == 0, "Phase 5D offline acceptance tests pass", failures)
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
    return failures


def check_runtime(runtime_root: Path, hermes_home: Path, vault_root: Path) -> list[str]:
    failures = check_repository()
    config = load_yaml(runtime_root / "config.yaml")
    disabled = set(config.get("agent", {}).get("disabled_toolsets", []))
    check(config.get("memory", {}).get("memory_enabled") is False, "Operations Hermes Memory remains OFF", failures)
    check({"terminal", "file", "browser", "code_execution", "delegation", "memory"} <= disabled, "generic execution and delegation remain disabled", failures)
    check(config.get("skills", {}).get("external_dirs") == [], "Operations external Skill dirs remain empty", failures)
    check(config.get("skills", {}).get("project_discovery") is False, "Operations project discovery remains disabled", failures)
    router_include = set(config.get("mcp_servers", {}).get("armor-vault-scoped-router", {}).get("tools", {}).get("include", []))
    check(router_include == TOOLS, "Operations receives the exact five-tool scoped Router allowlist", failures)
    product_link = hermes_home / "profiles/operations/skills/armor-website-product-materials"
    check(product_link.is_symlink() and product_link.resolve() == (ROOT / "skills/shared/department/armor-website-product-materials").resolve(), "Operations exposes canonical Product Materials Skill by symlink", failures)
    check(not (hermes_home / "profiles/operations/skills/armor-fallback-content-worker").exists(), "Operations does not expose Delegate worker Profile", failures)
    check(not (hermes_home / "profiles/operations/skills/armor-independent-auditor").exists(), "Operations does not expose Delegate auditor Profile", failures)
    check(vault_root.is_dir(), "Enterprise Vault root is readable", failures)
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", type=Path)
    parser.add_argument("--hermes-home", type=Path)
    parser.add_argument("--vault-root", type=Path)
    args = parser.parse_args(argv)
    supplied = (args.runtime_root, args.hermes_home, args.vault_root)
    if any(value is not None for value in supplied) and not all(value is not None for value in supplied):
        print("FAIL: runtime-root, hermes-home, and vault-root must be supplied together")
        return 2
    failures = check_runtime(*supplied) if all(value is not None for value in supplied) else check_repository()
    print(f"Phase 5D Product Materials check: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
