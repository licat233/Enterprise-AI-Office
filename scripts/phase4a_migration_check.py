#!/usr/bin/env python3
"""Offline acceptance checks for the Phase 4A Article/MCP migration."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment diagnostic
    print(f"FAIL: PyYAML is required: {exc}")
    raise SystemExit(2)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config/mcp-registry.yaml"
ARTICLE_SKILL = ROOT / "skills/shared/department/armor-website-article-pipeline/SKILL.md"
OPERATIONS_CONFIG = ROOT / "private/department-profile/config.yaml"
ENABLED_SKILLS = ROOT / "private/department-profile/enabled-skills.csv"
DISABLED_SKILLS = ROOT / "private/department-profile/disabled-skills.csv"
RUNTIME_COPY = ROOT / "skills/shared/department/armor/armor-article-pipeline-runtime"

EXPECTED = {
    "anysearch": "OPERATIONS_READ",
    "firecrawl-mcp": "OPERATIONS_EXTERNAL_WRITE",
    "obscura": "MACHINE_SPECIFIC_REBIND",
    "paddle_ocr": "MACHINE_SPECIFIC_REBIND",
    "toolscout": "SHARED_AGENT_INFRASTRUCTURE",
}
ALLOWED_SCOPED = {"armor-vault-scoped-router"}
OPERATIONS_MCP = {"weknora", "toolscout", "firecrawl-mcp", "armor-vault-scoped-router"}

PROHIBITED_ACTIVE = re.compile(
    r"/Users/" + r"licat|mcp_Obsidian_|personal[ _-]+chrome[ _-]+profile|"
    r"personal[ _-]+cookie|personal[ _-]+session|storage[ _-]+state",
    re.IGNORECASE,
)
SECRET_LITERAL = re.compile(
    r"(?i)(api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*"
    r"(?!\$\{)[A-Za-z0-9_./+=-]{20,}"
)


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if not isinstance(value, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} is not a mapping")
    return value


def check(condition: bool, label: str, failures: list[str]) -> None:
    if condition:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label}")
        failures.append(label)


def main() -> int:
    failures: list[str] = []
    registry = load(REGISTRY)
    policy = registry.get("policy", {})
    servers = registry.get("servers", {})

    check(set(EXPECTED) <= set(servers), "all five MCP definitions are registered", failures)
    check(set(servers) <= set(EXPECTED) | ALLOWED_SCOPED, "registry additions stay within the scoped Phase 4C boundary", failures)
    check(policy.get("secret_values_allowed") is False, "registry forbids secret values", failures)
    check(policy.get("employee_exposure_default") == "disabled", "employee exposure defaults disabled", failures)
    check(set(policy.get("operations_allowlist", [])) == OPERATIONS_MCP, "Operations allowlist contains only approved scoped capabilities", failures)

    for name, classification in EXPECTED.items():
        server = servers.get(name, {})
        check(server.get("classification") == classification, f"{name} classification", failures)
        runtime_status = server.get("runtime", {}).get("status")
        check(
            runtime_status in {"PREPARED", "PREPARED_REPLACEMENT_REQUIRED", "REGISTERED", "INSTALLED"},
            f"{name} records an explicit runtime state",
            failures,
        )
        exposure = server.get("exposure", {})
        check(exposure.get("default_enabled") is False, f"{name} default disabled", failures)
        check(exposure.get("default_enabled") is False, f"{name} default remains disabled", failures)
        check(server.get("health", {}).get("status") in {"NOT_RUN", "BLOCKED_CREDENTIAL", "HEALTHY"}, f"{name} health state is explicit", failures)

    article = ARTICLE_SKILL.read_text(encoding="utf-8")
    check("02-Projects/Workspaces/Website/Articles/" in article, "Article Router target is the Website Articles workspace", failures)
    check("03-Records/Published/" in article, "Published records are evidence-only", failures)
    for artifact in ("article-brief.json", "seo-blueprint.json", "article.md", "audit-report.md"):
        check(artifact in article, f"four-file contract includes {artifact}", failures)
    check("ai-writing-audit" in article and "v0.3.1" in article, "Article requires ai-writing-audit v0.3.1", failures)
    check("ARMOR_VAULT_ROOT" in article, "Article Skill uses runtime Vault root", failures)
    check("one Codex final editorial pass" in article, "Article flow has one Codex final editorial pass", failures)
    check("03-Records/Published/Articles/" not in article, "obsolete Published/Articles source route is absent", failures)
    check('pipeline_version: "1.3"' in article, "Article Skill declares pipeline v1.3", failures)
    check(not any(path.is_file() for path in RUNTIME_COPY.rglob("*")), "nested article runtime copy is absent", failures)

    operations = load(OPERATIONS_CONFIG)
    mcp_servers = operations.get("mcp_servers", {})
    check(set(mcp_servers) <= OPERATIONS_MCP and "weknora" in mcp_servers, "Operations runtime config contains only approved MCPs", failures)
    check(operations.get("memory", {}).get("memory_enabled") is False, "Operations Memory remains disabled", failures)

    for path in (ARTICLE_SKILL, OPERATIONS_CONFIG, ENABLED_SKILLS, DISABLED_SKILLS):
        text = path.read_text(encoding="utf-8")
        check(not PROHIBITED_ACTIVE.search(text), f"active path scan: {path.relative_to(ROOT)}", failures)
        check(not SECRET_LITERAL.search(text), f"active secret scan: {path.relative_to(ROOT)}", failures)

    if failures:
        print(f"Phase 4A migration check: {len(failures)} failure(s)")
        return 2
    print("Phase 4A migration check: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
