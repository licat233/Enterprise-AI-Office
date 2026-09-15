#!/usr/bin/env python3
"""Verify validated Core provenance, acquisition metadata, and derived pins."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STACK = ROOT / "config" / "validated-stack.yaml"


def component_block(text: str, component: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line == f"  {component}:":
            start = index + 1
            break
    if start is None:
        raise ValueError(f"missing component block: {component}")

    body: list[str] = []
    for line in lines[start:]:
        if line and not line.startswith(" "):
            break
        if re.match(r"^  [A-Za-z0-9_.-]+:\s*$", line):
            break
        body.append(line)
    return "\n".join(body)


def field(block: str, key: str) -> str:
    match = re.search(rf"^\s+{re.escape(key)}:\s*(.+?)\s*$", block, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"missing field in component block: {key}")
    return match.group(1).strip().strip("'\"")


def require_contains(path: str, needle: str, failures: list[str]) -> None:
    target = ROOT / path
    if not target.is_file():
        failures.append(f"missing file: {path}")
        return
    text = target.read_text(encoding="utf-8")
    if needle not in text:
        failures.append(f"{path}: expected text not found: {needle}")


def require_equal(label: str, actual: str, expected: str, failures: list[str]) -> None:
    if actual != expected:
        failures.append(f"{label}: expected {expected!r}, got {actual!r}")


def main() -> int:
    if not STACK.is_file():
        print("FAIL config/validated-stack.yaml missing")
        return 2

    text = STACK.read_text(encoding="utf-8")
    failures: list[str] = []

    try:
        weknora = component_block(text, "weknora")
        hermes = component_block(text, "hermes_agent")
        open_webui = component_block(text, "open_webui")

        versions = {
            "weknora": field(weknora, "version"),
            "open_webui": field(open_webui, "version"),
        }
        commits = {
            "weknora": field(weknora, "commit"),
            "open_webui": field(open_webui, "commit"),
        }
        hermes_policy = field(hermes, "version_policy")
        hermes_reference_version = field(hermes, "reference_version")
        hermes_reference_commit = field(hermes, "reference_commit")
    except ValueError as exc:
        print(f"FAIL {exc}")
        return 2

    require_equal(
        "WeKnora upstream repository",
        field(weknora, "upstream_repository"),
        "https://github.com/Tencent/WeKnora.git",
        failures,
    )
    require_equal(
        "WeKnora source ref",
        field(weknora, "source_ref"),
        versions["weknora"],
        failures,
    )
    require_equal(
        "WeKnora source ref type",
        field(weknora, "source_ref_type"),
        "tag",
        failures,
    )
    require_equal(
        "WeKnora tag/commit verification marker",
        field(weknora, "source_ref_matches_commit"),
        "true",
        failures,
    )
    require_equal(
        "WeKnora acquisition method",
        field(weknora, "method"),
        "git_clone_then_checkout_component_commit",
        failures,
    )
    require_equal(
        "WeKnora runtime image version",
        field(weknora, "value"),
        versions["weknora"].removeprefix("v"),
        failures,
    )

    require_equal(
        "Hermes upstream repository",
        field(hermes, "upstream_repository"),
        "https://github.com/NousResearch/hermes-agent.git",
        failures,
    )
    require_equal("Hermes version policy", hermes_policy, "rolling-validated", failures)
    require_equal("Hermes tracking ref", field(hermes, "tracking_ref"), "main", failures)
    require_equal("Hermes permanent version pin", field(hermes, "permanent_version_pin"), "false", failures)
    require_equal(
        "Hermes resolve candidate once",
        field(hermes, "resolve_candidate_once_per_change"),
        "true",
        failures,
    )
    require_equal(
        "Hermes unattended auto-update",
        field(hermes, "automatic_unattended_update"),
        "false",
        failures,
    )
    require_equal(
        "Hermes candidate acceptance required",
        field(hermes, "candidate_acceptance_required"),
        "true",
        failures,
    )
    require_equal(
        "Hermes rollback commit required",
        field(hermes, "rollback_commit_required"),
        "true",
        failures,
    )
    if not hermes_reference_version:
        failures.append("Hermes reference version is empty")
    if not re.fullmatch(r"[0-9a-f]{40}", hermes_reference_commit):
        failures.append("Hermes reference commit is not a 40-character lowercase Git SHA")
    require_equal(
        "Hermes version source",
        field(hermes, "version_source"),
        "hermes_version_plus_git_identity",
        failures,
    )
    require_equal(
        "Hermes acquisition method",
        field(hermes, "method"),
        "official_installer_from_resolved_candidate_commit",
        failures,
    )
    require_equal(
        "Hermes candidate resolution",
        field(hermes, "candidate_resolution"),
        "upstream_tracking_ref_at_transaction_start",
        failures,
    )
    installer_template = field(hermes, "installer_url_template")
    if "{candidate_commit}" not in installer_template or "NousResearch/hermes-agent" not in installer_template:
        failures.append("Hermes installer template is not candidate-commit-addressed to upstream")
    require_equal("Hermes installer commit flag", field(hermes, "commit_flag"), "--commit", failures)
    require_equal(
        "Hermes source path provenance",
        field(hermes, "provenance"),
        "scripts/install.sh_at_candidate_commit",
        failures,
    )
    require_equal(
        "Hermes explicit install-dir env override",
        field(hermes, "explicit_env_override"),
        "HERMES_INSTALL_DIR",
        failures,
    )
    require_equal(
        "Hermes explicit install-dir flag override",
        field(hermes, "explicit_flag_override"),
        "--dir",
        failures,
    )
    require_equal(
        "Hermes non-root source default",
        field(hermes, "non_root_default"),
        "${HERMES_HOME:-$HOME/.hermes}/hermes-agent",
        failures,
    )
    require_equal(
        "Hermes root Linux source default",
        field(hermes, "root_linux_default"),
        "/usr/local/lib/hermes-agent",
        failures,
    )

    require_equal(
        "Open WebUI upstream repository",
        field(open_webui, "upstream_repository"),
        "https://github.com/open-webui/open-webui.git",
        failures,
    )
    require_equal(
        "Open WebUI source ref",
        field(open_webui, "source_ref"),
        versions["open_webui"],
        failures,
    )
    require_equal(
        "Open WebUI source ref type",
        field(open_webui, "source_ref_type"),
        "tag",
        failures,
    )
    require_equal(
        "Open WebUI tag/commit verification marker",
        field(open_webui, "source_ref_matches_commit"),
        "true",
        failures,
    )
    require_equal(
        "Open WebUI acquisition method",
        field(open_webui, "method"),
        "official_container_image_via_eao_compose",
        failures,
    )
    open_webui_image = field(open_webui, "image")
    require_equal(
        "Open WebUI image",
        open_webui_image,
        f"ghcr.io/open-webui/open-webui:{versions['open_webui']}",
        failures,
    )

    require_equal(
        "WeKnora runtime identity container",
        field(weknora, "container_name"),
        "WeKnora-app",
        failures,
    )
    require_equal(
        "WeKnora runtime identity image",
        field(weknora, "container_image"),
        f"wechatopenai/weknora-app:{versions['weknora'].removeprefix('v')}",
        failures,
    )
    require_equal(
        "Hermes runtime version command",
        field(hermes, "version_command"),
        "hermes --version",
        failures,
    )
    require_equal(
        "Hermes exact version recording",
        field(hermes, "exact_version_recording_required"),
        "true",
        failures,
    )
    require_equal(
        "Hermes source commit required",
        field(hermes, "source_commit_required"),
        "true",
        failures,
    )
    require_equal(
        "Hermes reference match required",
        field(hermes, "reference_match_required"),
        "false",
        failures,
    )
    require_equal(
        "Open WebUI runtime identity container",
        field(open_webui, "container_name"),
        "eaio-open-webui",
        failures,
    )
    require_equal(
        "Open WebUI runtime identity image",
        field(open_webui, "container_image"),
        open_webui_image,
        failures,
    )

    require_contains(
        "infrastructure/open-webui/docker-compose.yml",
        f"image: {open_webui_image}",
        failures,
    )
    require_contains(
        "infrastructure/open-webui/docker-compose.yml",
        f"Derived pin: config/validated-stack.yaml -> Open WebUI {versions['open_webui']}",
        failures,
    )
    require_contains(
        "infrastructure/weknora/docker-compose.demo.override.yml",
        f"Derived pin: config/validated-stack.yaml -> WeKnora {versions['weknora']}",
        failures,
    )
    for path in (
        "infrastructure/hermes/default.config.example.yaml",
        "infrastructure/hermes/general.config.example.yaml",
    ):
        require_contains(
            path,
            "Derived schema contract: config/validated-stack.yaml -> Hermes Agent rolling-validated candidate.",
            failures,
        )

    require_contains("DEPLOY.md", "git clone https://github.com/Tencent/WeKnora.git", failures)
    require_contains("DEPLOY.md", commits["weknora"], failures)
    require_contains("DEPLOY.md", "NousResearch/hermes-agent", failures)
    require_contains("DEPLOY.md", "HERMES_CANDIDATE_COMMIT", failures)
    require_contains("DEPLOY.md", "git ls-remote https://github.com/NousResearch/hermes-agent.git refs/heads/main", failures)
    require_contains("DEPLOY.md", open_webui_image, failures)
    require_contains("DEPLOY.md", commits["open_webui"], failures)
    require_contains("DEPLOY.md", "RUNTIME_ROOT = deployment.runtime_root", failures)
    require_contains("DEPLOY.md", "HERMES_INSTALL_DIR", failures)
    require_contains("DEPLOY.md", "${HERMES_HOME:-$HOME/.hermes}/hermes-agent", failures)
    require_contains("DEPLOY.md", "/usr/local/lib/hermes-agent", failures)
    require_contains("DEPLOY.md", "### 4.2 Post-acquisition Core identity assertions", failures)
    require_contains("DEPLOY.md", f"wechatopenai/weknora-app:{versions['weknora'].removeprefix('v')}", failures)
    require_contains("DEPLOY.md", "hermes --version", failures)
    require_contains("DEPLOY.md", "docker inspect -f '{{.Config.Image}}' eaio-open-webui", failures)

    print("Enterprise AI Office Validated Stack Consistency")
    print("-----------------------------------------------")
    print(f"WeKnora: {versions['weknora']} @ {commits['weknora'][:12]}")
    print(f"Hermes Agent policy: {hermes_policy}")
    print(f"Hermes accepted reference: {hermes_reference_version} @ {hermes_reference_commit[:12]}")
    print(f"Open WebUI: {versions['open_webui']} @ {commits['open_webui'][:12]}")

    if failures:
        print(f"Consistency failures: {len(failures)}")
        for failure in failures:
            print(f"FAIL {failure}")
        return 2

    print("Consistency failures: 0")
    print("VALIDATED STACK CONSISTENCY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
