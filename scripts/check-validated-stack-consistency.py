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
            "hermes_agent": field(hermes, "version"),
            "open_webui": field(open_webui, "version"),
        }
        commits = {
            "weknora": field(weknora, "commit"),
            "hermes_agent": field(hermes, "commit"),
            "open_webui": field(open_webui, "commit"),
        }
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
    require_equal(
        "Hermes source ref type",
        field(hermes, "source_ref_type"),
        "commit_only_no_version_tag",
        failures,
    )
    require_equal(
        "Hermes version source",
        field(hermes, "version_source"),
        "pyproject.toml_at_component_commit",
        failures,
    )
    require_equal(
        "Hermes acquisition method",
        field(hermes, "method"),
        "official_installer_from_component_commit",
        failures,
    )
    installer_template = field(hermes, "installer_url_template")
    if "{commit}" not in installer_template or "NousResearch/hermes-agent" not in installer_template:
        failures.append("Hermes installer template is not commit-addressed to the validated upstream")
    require_equal("Hermes installer commit flag", field(hermes, "commit_flag"), "--commit", failures)

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
            f"Derived schema pin: config/validated-stack.yaml -> Hermes Agent {versions['hermes_agent']}",
            failures,
        )

    require_contains("DEPLOY.md", "git clone https://github.com/Tencent/WeKnora.git", failures)
    require_contains("DEPLOY.md", commits["weknora"], failures)
    require_contains("DEPLOY.md", "NousResearch/hermes-agent", failures)
    require_contains("DEPLOY.md", commits["hermes_agent"], failures)
    require_contains("DEPLOY.md", open_webui_image, failures)
    require_contains("DEPLOY.md", commits["open_webui"], failures)

    print("Enterprise AI Office Validated Stack Consistency")
    print("-----------------------------------------------")
    print(f"WeKnora: {versions['weknora']} @ {commits['weknora'][:12]}")
    print(f"Hermes Agent: {versions['hermes_agent']} @ {commits['hermes_agent'][:12]}")
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
