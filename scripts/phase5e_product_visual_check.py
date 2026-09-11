#!/usr/bin/env python3
"""Repository and deployed-runtime checks for Phase 5E Product Visual."""

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
SKILL = ROOT / "skills/shared/department/armor-product-visual/SKILL.md"
TESTS = ROOT / "scripts/test_phase5e_product_visual.py"
TOOLS = {
    "route_work_product",
    "save_article_package",
    "save_social_package",
    "save_mic_product_package",
    "save_website_product_materials_package",
    "save_product_visual_package",
}
STANDARD_RELATIVE = Path(
    "02-Projects/Workspaces/Products/Product-Visual/"
    "ARMOR-Product-Visual-Standard-v1.0.md"
)


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
    standard = Path(vault_root_raw) / STANDARD_RELATIVE if vault_root_raw else None
    check(ROUTER.is_file(), "Product Visual Router exists", failures)
    check(SCOPED_MCP.is_file(), "scoped Vault MCP exists", failures)
    check(SKILL.is_file(), "canonical Product Visual Skill exists", failures)
    check(TESTS.is_file(), "Product Visual acceptance tests exist", failures)
    check(standard is not None and standard.is_file(), "canonical Product Visual Standard exists", failures)

    if ROUTER.is_file():
        route = subprocess.run(
            [sys.executable, str(ROUTER), "--object", "work-product", "--domain", "products", "--artifact", "product-visual"],
            text=True,
            capture_output=True,
            check=False,
        )
        check(
            route.returncode == 0
            and route.stdout.splitlines()[0] == "02-Projects/Workspaces/Products/Product-Visual/",
            "Router resolves the cross-channel Product Visual workspace",
            failures,
        )
        wrong_domain = subprocess.run(
            [sys.executable, str(ROUTER), "--object", "work-product", "--domain", "website", "--artifact", "product-visual"],
            text=True,
            capture_output=True,
            check=False,
        )
        check(wrong_domain.returncode != 0, "Product Visual is not attached to the Website route", failures)

    if SCOPED_MCP.is_file():
        text = SCOPED_MCP.read_text(encoding="utf-8")
        check("PRODUCT_VISUAL_REQUIRED_FILES" in text, "Product Visual closed four-file contract is present", failures)
        check("save_product_visual_package" in text, "scoped Product Visual save is implemented", failures)
        check("Published evidence cannot be" in text, "scoped MCP rejects Published source writes", failures)
        check("binary" in text.lower() and "upload" in text.lower(), "scoped MCP documents no binary upload", failures)

    if SKILL.is_file():
        text = SKILL.read_text(encoding="utf-8")
        check("ARMOR-Product-Visual-Standard-v1.0.md" in text, "Skill references the canonical Standard", failures)
        check("READY_FOR_GENERATION" in text, "Skill ends at a generation handoff", failures)
        check("save_product_visual_package" in text, "Skill binds the scoped Product Visual save", failures)
        check("agent delegate" in " ".join(text.lower().split()), "Skill excludes Agent Delegate runtime", failures)
        check("generation" in text.lower() and "does not" in text.lower(), "Skill keeps generation outside the workflow", failures)
        check(str(Path.home()) not in text, "Skill has no personal runtime path", failures)

    if standard is not None and standard.is_file():
        text = standard.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        check("authority: canonical" in text, "Product Visual Standard is canonical", failures)
        check("1. authoritative original Datasheet" in text, "original product documents are first authority", failures)
        check("2. canonical or explicitly verified Product Knowledge" in text, "verified Product Knowledge is second authority", failures)
        check("3. read-only WeKnora retrieval" in text and "not final technical authority" in normalized, "WeKnora remains retrieval-only", failures)
        check("4. current website or MIC listing" in text and "existing-state evidence only" in normalized, "current listings remain evidence", failures)
        check("anti-moiré" in text and "moire pattern" in text, "ARMOR anti-moiré rules are canonical", failures)
        check("REAL_SOURCE_ASSET" in text and "GENERATED_ASSET" in text, "asset provenance model is canonical", failures)
        check("may not populate a numeric" in normalized, "inference cannot populate numeric facts", failures)
        check("save_product_visual_package" in text and "exactly these four" in normalized, "closed save package is documented", failures)
        normalized_lower = normalized.lower()
        check("operations image generation is disabled" in normalized_lower and "installed or bound by this capability" in normalized_lower, "image runtime is explicitly outside the capability", failures)
        check(str(Path.home()) not in text, "Standard has no personal runtime path", failures)

    registry = ROOT / "config/mcp-registry.yaml"
    if registry.is_file():
        data = load_yaml(registry)
        boundary = data.get("servers", {}).get("armor-vault-scoped-router", {}).get("boundary", {})
        check(boundary.get("product_visual_write_scope") == "Product_Visual_v1.0_required_four_text_files_no_binary_upload", "registry declares Product Visual write scope", failures)
        check(set(boundary.get("allowed_tools", [])) == TOOLS, "registry declares the exact scoped Router tools", failures)
        check("Product_Visual_v1.0" in boundary.get("write_scope", ""), "registry includes Product Visual in the closed write scope", failures)

    completed = subprocess.run([sys.executable, str(TESTS)], text=True, capture_output=True, check=False)
    check(completed.returncode == 0, "Phase 5E offline acceptance tests pass", failures)
    if completed.returncode != 0:
        print(completed.stdout)
        print(completed.stderr)
    return failures


def check_runtime(runtime_root: Path, hermes_home: Path, vault_root: Path) -> list[str]:
    failures = check_repository()
    config = load_yaml(runtime_root / "config.yaml")
    disabled = set(config.get("agent", {}).get("disabled_toolsets", []))
    check(config.get("memory", {}).get("memory_enabled") is False, "Operations Hermes Memory remains OFF", failures)
    check({"terminal", "file", "browser", "code_execution", "delegation", "memory", "image_gen"} <= disabled, "generic execution, delegation, and image generation remain disabled", failures)
    check(config.get("skills", {}).get("external_dirs") == [], "Operations external Skill dirs remain empty", failures)
    check(config.get("skills", {}).get("project_discovery") is False, "Operations project discovery remains disabled", failures)
    include = set(config.get("mcp_servers", {}).get("armor-vault-scoped-router", {}).get("tools", {}).get("include", []))
    check(include == TOOLS, "Operations receives the exact scoped Router tool allowlist", failures)
    product_link = hermes_home / "profiles/operations/skills/armor-product-visual"
    check(product_link.is_symlink() and product_link.resolve() == (ROOT / "skills/shared/department/armor-product-visual").resolve(), "Operations exposes canonical Product Visual Skill by symlink", failures)
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
    print(f"Phase 5E Product Visual check: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
