#!/usr/bin/env python3
"""Validate the Stage 1 Web Research capability and optional live bindings."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print(f"FAIL: PyYAML is required: {exc}")
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config/mcp-registry.yaml"
CAPABILITIES = ROOT / "config/capabilities.yaml"
ADAPTER = ROOT / "infrastructure/web-research/adapter.py"
TESTS = ROOT / "infrastructure/web-research/test_adapter.py"
DOC = ROOT / "docs/ENTERPRISE-WEB-RESEARCH-V1.md"
EXPECTED_RUNTIME_MCPS = {"weknora", "toolscout", "enterprise-web-research", "armor-vault-scoped-router"}
FORBIDDEN_RAW = {
    "firecrawl_scrape",
    "firecrawl_crawl",
    "firecrawl_agent",
    "firecrawl_interact",
    "firecrawl_monitor_create",
    "firecrawl_monitor_update",
    "firecrawl_monitor_delete",
    "firecrawl_monitor_run",
}
FORBIDDEN_TOOLSETS = {"web", "browser", "terminal", "file", "code_execution", "computer_use", "image_gen", "delegation"}


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a mapping")
    return value


def check(condition: bool, label: str, failures: list[str], details: str = "") -> None:
    if condition:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label}{(' - ' + details) if details else ''}")
        failures.append(label)


def check_repository(failures: list[str]) -> None:
    for path in (ADAPTER, TESTS, DOC):
        check(path.is_file(), f"required Web Research file: {path.relative_to(ROOT)}", failures)
    registry = load(REGISTRY)
    servers = registry.get("servers", {})
    policy = registry.get("policy", {})
    firecrawl = servers.get("firecrawl-mcp", {})
    firecrawl_boundary = firecrawl.get("boundary", {})
    adapter = servers.get("enterprise-web-research", {})
    adapter_boundary = adapter.get("boundary", {})
    check("enterprise_web_research:" in CAPABILITIES.read_text(encoding="utf-8"), "capability registry contains enterprise_web_research", failures)
    check(adapter.get("classification") == "OPERATIONS_READ", "adapter is classified as Operations read-only", failures)
    check(adapter_boundary.get("allowed_tools") == ["web_search", "web_fetch"], "adapter allowlist is exactly web_search/web_fetch", failures)
    check(adapter_boundary.get("automatic_persistence") is False, "adapter automatic persistence is disabled", failures)
    check(adapter_boundary.get("trust_class") == "UNTRUSTED_WEB_CONTENT", "adapter trust class is explicit", failures)
    check(firecrawl.get("runtime", {}).get("version") == "3.24.0", "Firecrawl version remains 3.24.0", failures)
    check(firecrawl_boundary.get("adapter_required") is True, "Firecrawl direct exposure requires the adapter", failures)
    check(firecrawl_boundary.get("raw_tools_exposed_to_operations") is False, "raw Firecrawl tools are not Operations-exposed", failures)
    denied = set(firecrawl_boundary.get("excluded_action_capable_tools", [])) | set(adapter_boundary.get("denied_tools", []))
    check(FORBIDDEN_RAW <= denied, "dangerous Firecrawl lanes remain denied", failures, f"missing={sorted(FORBIDDEN_RAW - denied)}")
    check(set(policy.get("operations_allowlist", [])) == EXPECTED_RUNTIME_MCPS, "registry Operations allowlist is bounded", failures)
    adapter_text = ADAPTER.read_text(encoding="utf-8")
    check("UNTRUSTED_WEB_CONTENT" in adapter_text, "adapter enforces the trust marker", failures)
    check("ARMOR_VAULT_ROOT" not in adapter_text and "WeKnora" not in adapter_text, "adapter has no Vault/WeKnora persistence dependency", failures)


def check_runtime(runtime_root: Path, failures: list[str]) -> None:
    config_path = runtime_root / "config.yaml"
    config = load(config_path)
    servers = config.get("mcp_servers", {})
    check(set(servers) == EXPECTED_RUNTIME_MCPS, "Operations exposes only the bounded Web Research adapter and existing approved MCPs", failures, f"found={sorted(servers)}")
    adapter = servers.get("enterprise-web-research", {})
    include = set((adapter.get("tools") or {}).get("include", []))
    check(include == {"web_search", "web_fetch"}, "Operations receives exactly web_search/web_fetch", failures, f"found={sorted(include)}")
    check("firecrawl-mcp" not in servers, "Operations does not bind raw Firecrawl MCP", failures)
    disabled = set((config.get("agent") or {}).get("disabled_toolsets", []))
    check(FORBIDDEN_TOOLSETS <= disabled, "generic and delegation toolsets remain disabled", failures, f"missing={sorted(FORBIDDEN_TOOLSETS - disabled)}")
    memory = config.get("memory") or {}
    check(memory.get("memory_enabled") is False and memory.get("user_profile_enabled") is False, "Operations Memory remains disabled", failures)
    skills = config.get("skills") or {}
    check(skills.get("external_dirs") == [] and skills.get("project_discovery") is False, "Operations external Skill/project discovery boundaries remain closed", failures)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", type=Path)
    args = parser.parse_args()
    failures: list[str] = []
    check_repository(failures)
    if args.runtime_root:
        check_runtime(args.runtime_root, failures)
    for failure in failures:
        print(f"FAILURE: {failure}")
    print(f"Phase 6 Web Research check: {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
