#!/usr/bin/env python3
"""Validate capability acceptance document/section references.

This is a narrow, dependency-free structural check. It parses only the
acceptance blocks in config/capabilities.yaml and requires every declared
section/sections value to match a Markdown heading in the referenced document.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "capabilities.yaml"

CAPABILITY_RE = re.compile(r"^  ([A-Za-z0-9_.-]+):\s*$")
ACCEPTANCE_RE = re.compile(r"^    acceptance:\s*$")
FIELD_RE = re.compile(r"^      (document|section|sections):(?:\s*(.*))?$")
LIST_RE = re.compile(r"^        -\s+(.+?)\s*$")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def normalize_heading(value: str) -> str:
    value = unquote(value.strip())
    value = value.replace(chr(96), "")
    value = re.sub(r"[*_]", "", value)
    value = re.sub(r"^\d+(?:\.\d+)*[.)]?\s+", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip().casefold()


def parse_acceptance_blocks(text: str) -> list[tuple[str, str, list[str]]]:
    lines = text.splitlines()
    current = ""
    blocks: list[tuple[str, str, list[str]]] = []
    i = 0

    while i < len(lines):
        cap = CAPABILITY_RE.match(lines[i])
        if cap:
            current = cap.group(1)
            i += 1
            continue

        if not ACCEPTANCE_RE.match(lines[i]):
            i += 1
            continue

        document = ""
        sections: list[str] = []
        collecting_sections = False
        i += 1

        while i < len(lines):
            line = lines[i]
            if line and len(line) - len(line.lstrip(" ")) <= 4:
                break

            field = FIELD_RE.match(line)
            if field:
                key, raw = field.groups()
                collecting_sections = key == "sections"
                if key == "document" and raw:
                    document = unquote(raw)
                elif key == "section" and raw:
                    sections.append(unquote(raw))
                i += 1
                continue

            if collecting_sections:
                item = LIST_RE.match(line)
                if item:
                    sections.append(unquote(item.group(1)))

            i += 1

        blocks.append((current or "<unknown>", document, sections))

    return blocks


def markdown_headings(path: Path) -> set[str]:
    headings: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if match:
            headings.add(normalize_heading(match.group(1)))
    return headings


def main() -> int:
    if not REGISTRY.is_file():
        print("FAIL config/capabilities.yaml missing")
        return 2

    blocks = parse_acceptance_blocks(REGISTRY.read_text(encoding="utf-8"))
    failures: list[str] = []
    checked_sections = 0

    print("Enterprise AI Office Capability Acceptance Integrity")
    print("---------------------------------------------------")
    print(f"Acceptance blocks found: {len(blocks)}")

    for capability, document, sections in blocks:
        if not document:
            failures.append(f"{capability}: acceptance.document missing")
            continue

        target = (ROOT / document).resolve()
        try:
            target.relative_to(ROOT.resolve())
        except ValueError:
            failures.append(f"{capability}: acceptance document escapes repository: {document}")
            continue

        if not target.is_file():
            failures.append(f"{capability}: acceptance document missing: {document}")
            continue

        if not sections:
            failures.append(f"{capability}: acceptance section(s) missing for {document}")
            continue

        headings = markdown_headings(target)
        for section in sections:
            checked_sections += 1
            normalized = normalize_heading(section)
            if normalized not in headings:
                failures.append(
                    f"{capability}: heading not found in {document}: {section!r}"
                )

    print(f"Acceptance sections checked: {checked_sections}")

    if failures:
        print(f"Acceptance reference failures: {len(failures)}")
        for failure in failures:
            print(f"FAIL {failure}")
        return 2

    print("Acceptance reference failures: 0")
    print("CAPABILITY ACCEPTANCE INTEGRITY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
