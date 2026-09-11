#!/usr/bin/env python3
"""Verify derived runtime pins stay aligned with config/validated-stack.yaml."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STACK = ROOT / "config" / "validated-stack.yaml"


def component_version(text: str, component: str) -> str:
    pattern = (
        rf"^  {re.escape(component)}:\n"
        rf"(?:    .*\n)*?"
        rf"    version:\s*([^\n#]+)"
    )
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        raise ValueError(f"missing version for component: {component}")
    return match.group(1).strip().strip("'\"")


def require_contains(path: str, needle: str, failures: list[str]) -> None:
    target = ROOT / path
    if not target.is_file():
        failures.append(f"missing derived file: {path}")
        return
    text = target.read_text(encoding="utf-8")
    if needle not in text:
        failures.append(f"{path}: expected derived pin not found: {needle}")


def main() -> int:
    if not STACK.is_file():
        print("FAIL config/validated-stack.yaml missing")
        return 2

    text = STACK.read_text(encoding="utf-8")
    try:
        versions = {
            "weknora": component_version(text, "weknora"),
            "hermes_agent": component_version(text, "hermes_agent"),
            "open_webui": component_version(text, "open_webui"),
        }
    except ValueError as exc:
        print(f"FAIL {exc}")
        return 2

    failures: list[str] = []

    require_contains(
        "infrastructure/open-webui/docker-compose.yml",
        f"image: ghcr.io/open-webui/open-webui:{versions['open_webui']}",
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

    print("Enterprise AI Office Validated Stack Consistency")
    print("-----------------------------------------------")
    print(f"WeKnora: {versions['weknora']}")
    print(f"Hermes Agent: {versions['hermes_agent']}")
    print(f"Open WebUI: {versions['open_webui']}")

    if failures:
        print(f"Derived-pin failures: {len(failures)}")
        for failure in failures:
            print(f"FAIL {failure}")
        return 2

    print("Derived-pin failures: 0")
    print("VALIDATED STACK CONSISTENCY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
