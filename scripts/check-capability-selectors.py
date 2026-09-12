#!/usr/bin/env python3
"""Validate capability selectors and required deployment-record metadata.

This is intentionally dependency-free and checks stable selector paths against
the company schema plus the rule that every conditional capability and every
Production Ready control declares what non-secret operational evidence must be
recorded after deployment.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAPS = ROOT / "config" / "capabilities.yaml"
COMPANY = ROOT / "config" / "company.example.yaml"

CAP_RE = re.compile(r"^  ([A-Za-z0-9_.-]+):\s*$")
KEY_RE = re.compile(r"^(\s*)([A-Za-z0-9_.-]+):(?:\s|$)")


def company_paths(text: str) -> set[str]:
    paths: set[str] = set()
    stack: list[tuple[int, str]] = []

    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        normalized = line
        stripped = normalized.lstrip()
        if stripped.startswith("- "):
            indent = len(normalized) - len(stripped)
            normalized = " " * indent + stripped[2:]
        match = KEY_RE.match(normalized)
        if not match:
            continue

        indent = len(match.group(1))
        key = match.group(2)
        while stack and stack[-1][0] >= indent:
            stack.pop()
        stack.append((indent, key))
        paths.add(".".join(item[1] for item in stack))

    return paths


def selector_blocks(text: str) -> list[tuple[str, str, list[str], str]]:
    lines = text.splitlines()
    current = ""
    result: list[tuple[str, str, list[str], str]] = []
    i = 0

    while i < len(lines):
        cap = CAP_RE.match(lines[i])
        if cap:
            current = cap.group(1)

        if lines[i] != "    selection:":
            i += 1
            continue

        source = ""
        scope = ""
        paths: list[str] = []
        i += 1
        while i < len(lines):
            line = lines[i]
            if line and len(line) - len(line.lstrip(" ")) <= 4:
                break
            stripped = line.strip()
            if stripped.startswith("source:"):
                source = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("scope:"):
                scope = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("path:"):
                paths.append(stripped.split(":", 1)[1].strip())
            elif stripped.startswith("- path:"):
                paths.append(stripped.split(":", 1)[1].strip())
            i += 1

        result.append((current or "<unknown>", source, paths, scope))

    return result


def conditional_capabilities(text: str) -> set[str]:
    lines = text.splitlines()
    current = ""
    result: set[str] = set()
    for line in lines:
        cap = CAP_RE.match(line)
        if cap:
            current = cap.group(1)
            continue
        if current and line.strip() == "kind: conditional":
            result.add(current)
    return result


def recorded_capabilities(text: str) -> set[str]:
    lines = text.splitlines()
    current = ""
    result: set[str] = set()
    for line in lines:
        cap = CAP_RE.match(line)
        if cap:
            current = cap.group(1)
            continue
        if current and line == "    records:":
            result.add(current)
    return result


def production_controls(text: str) -> set[str]:
    result: set[str] = set()
    in_production = False
    for line in text.splitlines():
        if line == "production_controls:":
            in_production = True
            continue
        if not in_production:
            continue
        if line and not line.startswith(" "):
            break
        control = CAP_RE.match(line)
        if control:
            result.add(control.group(1))
    return result


def main() -> int:
    if not CAPS.is_file() or not COMPANY.is_file():
        print("FAIL required config file missing")
        return 2

    caps_text = CAPS.read_text(encoding="utf-8")
    company_text = COMPANY.read_text(encoding="utf-8")

    schema_paths = company_paths(company_text)
    selectors = selector_blocks(caps_text)
    conditional = conditional_capabilities(caps_text)
    production = production_controls(caps_text)
    recorded = recorded_capabilities(caps_text)
    failures: list[str] = []
    selected_names = {name for name, _, _, _ in selectors}

    for capability in sorted(conditional):
        if capability not in selected_names:
            failures.append(f"{capability}: conditional capability has no selection metadata")
        if capability not in recorded:
            failures.append(f"{capability}: conditional capability has no records metadata")

    for control in sorted(production):
        if control not in recorded:
            failures.append(f"{control}: production control has no records metadata")

    checked_paths = 0
    for capability, source, paths, scope in selectors:
        if scope == "ARMOR_reference_specific":
            if source == "company_configuration":
                failures.append(
                    f"{capability}: ARMOR-specific selector must not masquerade as generic company schema"
                )
            continue

        if source != "company_configuration":
            failures.append(
                f"{capability}: generic selector must declare source: company_configuration"
            )
            continue

        if not paths:
            failures.append(f"{capability}: company selector declares no path")
            continue

        for path in paths:
            checked_paths += 1
            if path not in schema_paths:
                failures.append(
                    f"{capability}: selector path missing from config/company.example.yaml: {path}"
                )

    print("Enterprise AI Office Capability Selector Integrity")
    print("------------------------------------------------")
    print(f"Conditional capabilities: {len(conditional)}")
    print(f"Selector blocks: {len(selectors)}")
    print(f"Conditional record blocks: {len(conditional & recorded)}")
    print(f"Production controls: {len(production)}")
    print(f"Production control record blocks: {len(production & recorded)}")
    print(f"Company selector paths checked: {checked_paths}")

    if failures:
        print(f"Selector failures: {len(failures)}")
        for failure in failures:
            print(f"FAIL {failure}")
        return 2

    print("Selector/record failures: 0")
    print("CAPABILITY SELECTOR / RECORD INTEGRITY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
