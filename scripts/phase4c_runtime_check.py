#!/usr/bin/env python3
"""Repository and optional live checks for the Phase 4C runtime closure."""

from __future__ import annotations

import argparse
import json
import os
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
ROUTER = ROOT / "skills/shared/department/armor-memory/scripts/armor-route.py"
WRAPPER = ROOT / "skills/shared/department/armor-memory/scripts/route.sh"
SCOPED_MCP = ROOT / "skills/shared/department/armor-memory/scripts/armor-vault-mcp.py"
REGISTRY = ROOT / "config/mcp-registry.yaml"


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


def scoped_probe() -> list[str]:
    failures: list[str] = []
    fixture = {
        "article-brief.json": json.dumps({"title": "Phase 4C fixture"}),
        "seo-blueprint.json": json.dumps({"primary_keyword": "fixture"}),
        "article.md": "# Phase 4C fixture\n",
        "audit-report.md": "# Audit\n\nPASS\n",
    }
    with tempfile.TemporaryDirectory() as temp:
        env = dict(os.environ)
        env["ARMOR_VAULT_ROOT"] = temp
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "route_work_product", "arguments": {"domain": "website", "artifact": "article"}},
            },
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "save_article_package", "arguments": {"package_id": "phase4c-fixture", "files": fixture}},
            },
        ]
        completed = subprocess.run(
            [sys.executable, str(SCOPED_MCP)],
            input="\n".join(json.dumps(item) for item in requests) + "\n",
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )
        check(completed.returncode == 0, "scoped MCP process exits cleanly", failures)
        try:
            replies = [json.loads(line) for line in completed.stdout.splitlines()]
            names = {tool["name"] for tool in replies[1]["result"]["tools"]}
            route = json.loads(replies[2]["result"]["content"][0]["text"])
            saved = json.loads(replies[3]["result"]["content"][0]["text"])
        except (IndexError, KeyError, TypeError, json.JSONDecodeError) as exc:
            failures.append(f"scoped MCP response shape: {exc}")
            print(f"FAIL: scoped MCP response shape: {exc}")
            return failures
        check(replies[0]["result"]["serverInfo"]["version"] == "1.0.0", "scoped MCP initialize", failures)
        check(
            names == {"route_work_product", "save_article_package", "save_social_package", "save_mic_product_package", "save_website_product_materials_package", "save_product_visual_package"},
            "scoped MCP exposes Article, Social, MIC, Website Product Materials, and Product Visual tools",
            failures,
        )
        check(route["relative_path"] == "02-Projects/Workspaces/Website/Articles/", "scoped route is Article workspace", failures)
        check(saved["read_back"] is True, "scoped Article save read-back", failures)
        package_dir = Path(temp) / "02-Projects/Workspaces/Website/Articles/phase4c-fixture"
        check(package_dir.is_dir(), "scoped Article package exists under Vault root", failures)
        check({path.name for path in package_dir.iterdir()} == set(fixture), "scoped save contains only four files", failures)
    return failures


def check_repository() -> list[str]:
    failures: list[str] = []
    registry = load_yaml(REGISTRY)
    servers = registry.get("servers", {})
    check(ROUTER.is_file(), "Enterprise-owned deterministic Router exists", failures)
    check("ARMOR_ARCH_ROOT" not in WRAPPER.read_text(encoding="utf-8"), "route wrapper has no ARMOR_ARCH_ROOT dependency", failures)
    check(SCOPED_MCP.is_file(), "scoped Vault MCP exists", failures)
    check(set(servers) == {"anysearch", "firecrawl-mcp", "obscura", "paddle_ocr", "toolscout", "armor-vault-scoped-router"}, "registry contains five MCP runtimes plus scoped Router", failures)
    check(servers["toolscout"]["classification"] == "SHARED_AGENT_INFRASTRUCTURE", "ToolScout is shared agent infrastructure", failures)
    check(servers["firecrawl-mcp"]["boundary"]["adapter_required"] is False, "Firecrawl uses native Hermes filtering", failures)
    router_boundary = servers["armor-vault-scoped-router"]["boundary"]
    check(
        router_boundary["article_write_scope"] == "Article_v1.3_four_file_package_only",
        "Article write boundary remains the four-file package",
        failures,
    )
    check(servers["anysearch"]["health"]["status"] == "BLOCKED_CREDENTIAL", "Anysearch credential state is explicit", failures)
    check("Published evidence cannot be" in SCOPED_MCP.read_text(encoding="utf-8"), "scoped MCP rejects Published as source", failures)
    failures.extend(scoped_probe())
    return failures


def check_runtime(runtime_root: Path, hermes_home: Path, vault_root: Path) -> list[str]:
    failures = check_repository()
    config_path = runtime_root / "config.yaml"
    config = load_yaml(config_path)
    mcp = config.get("mcp_servers", {})
    check({"weknora", "toolscout", "firecrawl-mcp", "armor-vault-scoped-router"} <= set(mcp), "Operations exposes WeKnora, ToolScout, Firecrawl, and scoped Router", failures)
    check("obscura" not in mcp and "paddle_ocr" not in mcp, "Operations does not receive browser or raw OCR file access", failures)
    check(config.get("memory", {}).get("memory_enabled") is False, "Operations Hermes Memory is OFF", failures)
    check(config.get("memory", {}).get("user_profile_enabled") is False, "Operations user Profile Memory is OFF", failures)
    disabled = set(config.get("agent", {}).get("disabled_toolsets", []))
    check({"terminal", "file", "browser", "code_execution", "delegation", "memory"} <= disabled, "Operations generic execution boundaries remain disabled", failures)
    global_config = hermes_home / "config.yaml"
    check(global_config.is_file(), "Enterprise Hermes global config exists", failures)
    if global_config.is_file():
        global_text = global_config.read_text(encoding="utf-8", errors="replace")
        check("ARMOR_ARCH_ROOT" not in global_text, "Enterprise Hermes global config has no ARMOR_ARCH_ROOT", failures)
    check(vault_root.is_dir(), "Enterprise Vault root is readable", failures)
    return failures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", type=Path)
    parser.add_argument("--hermes-home", type=Path)
    parser.add_argument("--vault-root", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = check_repository()
    supplied = (args.runtime_root, args.hermes_home, args.vault_root)
    if any(value is not None for value in supplied):
        if not all(value is not None for value in supplied):
            print("FAIL: runtime-root, hermes-home, and vault-root must be supplied together")
            return 2
        failures = check_runtime(args.runtime_root, args.hermes_home, args.vault_root)
    if failures:
        print(f"Phase 4C runtime check: {len(failures)} failure(s)")
        return 2
    print("Phase 4C runtime check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
