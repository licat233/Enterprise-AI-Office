#!/usr/bin/env python3
"""Deterministic Phase 4B checks for the Article runtime boundary.

Repository-only mode validates the committed contract. Runtime mode accepts
explicit target paths and inspects only the Operations Profile, the bound
Vault, and the Hermes source needed to verify MCP tool filtering. It reports
known blocked boundaries without converting them into a false HEALTHY state.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - target runtime diagnostic
    print(f"FAIL: PyYAML is required: {exc}")
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
ARTICLE_SKILL = ROOT / "skills/shared/department/armor-website-article-pipeline/SKILL.md"
AUDIT_ROOT = ROOT / "skills/shared/department/ai-writing-audit"
AUDIT_SKILL = AUDIT_ROOT / "SKILL.md"
AUDIT_CLI = AUDIT_ROOT / "scripts/audit.py"
ARMOR_MEMORY_ROOT = ROOT / "skills/shared/department/armor-memory"
REGISTRY = ROOT / "config/mcp-registry.yaml"
PROFILE_CONFIG = ROOT / "private/department-profile/config.yaml"
PROFILE_MANIFEST = ROOT / "private/department-profile/.symlink_manifest"
PROFILE_ENABLED = ROOT / "private/department-profile/enabled-skills.csv"
PROFILE_DISABLED = ROOT / "private/department-profile/disabled-skills.csv"

RETIRED_SKILLS = {
    "armor-content-pipeline",
    "armor-topic-radar",
    "armor-topic-recommendation",
    "agent-seo-research",
    "agent-content-writer",
    "agent-content-auditor",
    "agent-knowledge-growth",
}
FORBIDDEN_ACTIVE = re.compile(
    r"/Users/licat|/Volumes/MacData|mcp_Obsidian_|personal[ _-]+(?:chrome|cookie|session)|storage[ _-]+state",
    re.IGNORECASE,
)
REQUIRED_DISABLED_TOOLSETS = {"browser", "terminal", "file", "code_execution", "delegation", "memory"}
REQUIRED_STAGE_FILES = (
    "armor-article-pipeline.md",
    "article-pipeline-config.yaml",
    "article-brief-standard.md",
    "seo-geo-blueprint-standard.md",
    "blueprint-gate-standard.md",
    "article-writing-standard.md",
    "article-audit-standard.md",
    "article-frontmatter-standard.md",
    "executor-fallback-standard.md",
    "audit-report.template.md",
)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a mapping")
    return value


def named_binding(text: str, name: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(name)}\s*:\s*(.*?)\s*$", text)
    if not match:
        return None
    return match.group(1).strip().strip("\"'") or None


def file_has_binding(path: Path, name: str) -> bool:
    if not path.is_file():
        return False
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if re.match(rf"^\s*(?:export\s+)?{re.escape(name)}\s*=", line):
            return bool(line.split("=", 1)[1].strip().strip("\"'"))
    return False


def has_forbidden_active_reference(text: str) -> bool:
    return bool(FORBIDDEN_ACTIVE.search(text))


def router_state(repo_root: Path, architecture_root: Path | None = None) -> tuple[str, str]:
    local_candidates = (
        repo_root / "skills/shared/department/armor-memory/scripts/armor-route.py",
        repo_root / "minimal-stable/scripts/armor-route.py",
    )
    for local in local_candidates:
        if local.is_file():
            return "READY", str(local)
    if architecture_root is not None:
        external = architecture_root / "minimal-stable/scripts/armor-route.py"
        if external.is_file():
            return "READY", str(external)
    return (
        "BLOCKED",
        "SCOPED_ROUTER_WRITE_BLOCKED: Operations has no scoped Vault-write executor, "
        "and armor-memory/scripts/route.sh cannot resolve its local armor-route.py "
        "without an available ARMOR_ARCH_ROOT or local implementation",
    )


def check(condition: bool, label: str, failures: list[str]) -> None:
    if condition:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label}")
        failures.append(label)


def check_repository() -> list[str]:
    failures: list[str] = []
    check(ARTICLE_SKILL.is_file(), "canonical Article Skill exists", failures)
    check(AUDIT_SKILL.is_file(), "canonical ai-writing-audit Skill exists", failures)
    check(AUDIT_CLI.is_file(), "audit CLI exists", failures)
    audit_text = AUDIT_SKILL.read_text(encoding="utf-8") if AUDIT_SKILL.is_file() else ""
    cli_text = AUDIT_CLI.read_text(encoding="utf-8") if AUDIT_CLI.is_file() else ""
    check("version: 0.3.1" in audit_text, "audit Skill declares v0.3.1", failures)
    check('TOOL_VERSION = "0.3.1"' in cli_text, "audit CLI declares v0.3.1", failures)
    check(not has_forbidden_active_reference(audit_text + cli_text), "audit active files contain no personal runtime paths", failures)
    check(ARMOR_MEMORY_ROOT.joinpath("scripts/route.sh").is_file(), "canonical armor-memory Router wrapper exists", failures)

    manifest = PROFILE_MANIFEST.read_text(encoding="utf-8") if PROFILE_MANIFEST.is_file() else ""
    enabled = PROFILE_ENABLED.read_text(encoding="utf-8") if PROFILE_ENABLED.is_file() else ""
    disabled = PROFILE_DISABLED.read_text(encoding="utf-8") if PROFILE_DISABLED.is_file() else ""
    check("ai-writing-audit -> /Users/armor/Enterprise-AI-Office/skills/shared/department/ai-writing-audit" in manifest, "Profile manifest exposes audit canonically", failures)
    check("armor-website-article-pipeline -> /Users/armor/Enterprise-AI-Office/skills/shared/department/armor-website-article-pipeline" in manifest, "Profile manifest exposes Article canonically", failures)
    check("ai-writing-audit,SAFE_BASELINE" in enabled, "Profile enables audit dependency", failures)
    check("armor-website-article-pipeline,PRIVILEGED_OR_EXTERNAL" in enabled, "Profile enables Article entrypoint", failures)
    check("armor-website-article-pipeline," not in disabled, "Article is not listed as disabled", failures)
    check(not any(name in enabled or name in manifest for name in RETIRED_SKILLS), "retired Article/SEO Writer Skills stay inactive", failures)

    profile = load_yaml(PROFILE_CONFIG)
    check(profile.get("memory", {}).get("memory_enabled") is False, "repository Operations Memory is OFF", failures)
    allowed_mcp = {"weknora", "toolscout", "enterprise-web-research", "armor-vault-scoped-router"}
    check(set(profile.get("mcp_servers", {})) <= allowed_mcp and "weknora" in profile.get("mcp_servers", {}), "repository Operations MCP config stays within approved capabilities", failures)
    check(set(profile.get("platform_toolsets", {}).get("cli", [])) == {"weknora", "skills", "toolscout", "enterprise-web-research", "armor-vault-scoped-router"}, "repository Operations toolsets stay within the Phase 4C allowlist", failures)
    check(REQUIRED_DISABLED_TOOLSETS <= set(profile.get("agent", {}).get("disabled_toolsets", [])), "generic shell/file/browser paths remain disabled", failures)

    for path in (ARTICLE_SKILL, PROFILE_CONFIG, PROFILE_MANIFEST, PROFILE_ENABLED, PROFILE_DISABLED):
        if path.is_file():
            check(not has_forbidden_active_reference(path.read_text(encoding="utf-8")), f"active path scan: {path.relative_to(ROOT)}", failures)
    return failures


def check_runtime(
    runtime_root: Path,
    hermes_home: Path,
    vault_root: Path,
    hermes_source: Path | None,
    architecture_root: Path | None,
    expect_blocked_router: bool,
) -> list[str]:
    failures = check_repository()
    runtime_config_path = runtime_root / "config.yaml"
    runtime_config = load_yaml(runtime_config_path)
    runtime_text = runtime_config_path.read_text(encoding="utf-8")
    check(runtime_config.get("memory", {}).get("memory_enabled") is False, "deployed Operations Memory is OFF", failures)
    runtime_mcp = set(runtime_config.get("mcp_servers", {}))
    check(runtime_mcp <= {"weknora", "toolscout", "enterprise-web-research", "armor-vault-scoped-router"} and "weknora" in runtime_mcp, "deployed Operations MCP config stays within approved capabilities", failures)
    cli_tools = set(runtime_config.get("platform_toolsets", {}).get("cli", []))
    check(cli_tools == {"weknora", "skills", "toolscout", "enterprise-web-research", "armor-vault-scoped-router"}, "deployed Operations toolsets stay within the Phase 4C allowlist", failures)
    disabled = set(runtime_config.get("agent", {}).get("disabled_toolsets", []))
    check(REQUIRED_DISABLED_TOOLSETS <= disabled, "deployed generic shell/file/browser paths remain disabled", failures)
    check(not has_forbidden_active_reference(runtime_text), "deployed Operations config has no prohibited active references", failures)

    expected_links = {
        "armor-website-article-pipeline": ROOT / "skills/shared/department/armor-website-article-pipeline",
        "ai-writing-audit": AUDIT_ROOT,
    }
    for name, target in expected_links.items():
        link = runtime_root / "skills" / name
        check(link.is_symlink(), f"deployed Profile exposes {name} as a symlink", failures)
        if link.is_symlink():
            check(link.resolve() == target.resolve(), f"deployed {name} points to canonical repository source", failures)

    global_config = hermes_home / "config.yaml"
    global_text = global_config.read_text(encoding="utf-8") if global_config.is_file() else ""
    bound_vault = named_binding(global_text, "ARMOR_VAULT_ROOT")
    check(bound_vault == str(vault_root), "ARMOR_VAULT_ROOT binding matches supplied Enterprise Vault", failures)
    article_folder = vault_root / "02-Projects/Workspaces/Content/ARMOR-Content-Operations/ARMOR-Article-Production-Pipeline-v1.3"
    check(article_folder.is_dir(), "Article canonical Vault folder is readable", failures)
    for name in REQUIRED_STAGE_FILES:
        check((article_folder / name).is_file(), f"Vault Article standard readable: {name}", failures)
        stage_file = article_folder / name
        if stage_file.is_file() and name.endswith((".md", ".yaml", ".json")):
            check(not has_forbidden_active_reference(stage_file.read_text(encoding="utf-8", errors="replace")), f"Vault active path scan: {name}", failures)
    if (article_folder / "article-pipeline-config.yaml").is_file():
        pipeline_config = load_yaml(article_folder / "article-pipeline-config.yaml")
        check(pipeline_config.get("pipeline_version") == "1.3", "Vault Article config declares pipeline v1.3", failures)
        detection = pipeline_config.get("ai_detection", {})
        check(detection.get("required_tool_version") == "0.3.1", "Vault Article config requires audit v0.3.1", failures)
        check(detection.get("final_run_owner") == "codex_final_editor", "Vault Article config assigns final audit to Codex", failures)
    article_target = vault_root / "02-Projects/Workspaces/Website/Articles"
    published_target = vault_root / "03-Records/Published"
    check(article_target.is_dir(), "Router Article target is resolvable", failures)
    check(published_target.is_dir(), "Published evidence directory exists separately", failures)
    check("03-Records/Published/Articles/" not in ARTICLE_SKILL.read_text(encoding="utf-8"), "Article Skill does not use Published as source", failures)

    route_status, route_detail = router_state(ROOT, architecture_root)
    if route_status == "READY":
        print(f"PASS: Router implementation resolvable at {route_detail}")
    elif expect_blocked_router:
        print(f"BLOCKED: {route_detail}")
    else:
        print(f"FAIL: {route_detail}")
        failures.append("scoped Router executor is unavailable")

    credential_present = file_has_binding(runtime_root / ".env", "ANYSEARCH_API_KEY") or file_has_binding(hermes_home / ".env", "ANYSEARCH_API_KEY")
    print(f"Anysearch credential binding: {'PRESENT' if credential_present else 'MISSING'}")
    if "anysearch" in runtime_config.get("mcp_servers", {}):
        failures.append("Anysearch must remain disabled while credential/runtime boundary is unresolved")
    else:
        print("PASS: Anysearch is not exposed to Operations")

    if hermes_source is not None:
        registration = hermes_source / "tools/mcp_tool_registration.py"
        source = registration.read_text(encoding="utf-8", errors="replace") if registration.is_file() else ""
        check('tools_filter.get("include")' in source, "Hermes supports MCP tool-level include allowlisting", failures)
    else:
        print("INFO: Hermes source not supplied; tool-level allowlist evidence not checked")
    return failures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check the Phase 4B Article runtime boundary.")
    parser.add_argument("--runtime-root", type=Path, help="Operations Profile directory")
    parser.add_argument("--hermes-home", type=Path, help="Enterprise Hermes root")
    parser.add_argument("--vault-root", type=Path, help="Resolved Enterprise Vault root")
    parser.add_argument("--hermes-source", type=Path, help="Hermes source checkout for MCP filter verification")
    parser.add_argument("--architecture-root", type=Path, help="Optional ARMOR memory architecture root")
    parser.add_argument("--expect-blocked-router", action="store_true", help="Accept the documented fail-closed Router blocker")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = check_repository()
    if args.runtime_root or args.hermes_home or args.vault_root:
        if not (args.runtime_root and args.hermes_home and args.vault_root):
            print("FAIL: --runtime-root, --hermes-home, and --vault-root are required together")
            return 2
        failures = check_runtime(
            args.runtime_root,
            args.hermes_home,
            args.vault_root,
            args.hermes_source,
            args.architecture_root,
            args.expect_blocked_router,
        )
    if failures:
        print(f"Phase 4B runtime check: {len(failures)} failure(s)")
        return 2
    print("Phase 4B runtime check: PASS (known blocked boundaries are fail-closed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
