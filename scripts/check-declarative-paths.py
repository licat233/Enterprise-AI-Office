#!/usr/bin/env python3
"""Validate repository paths declared by machine-readable EAO contracts.

This intentionally avoids a YAML dependency. It only inspects scalar values
that clearly look like repository paths under known repository prefixes, plus
the small set of root-level contract files.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECLARATIVE_FILES = (
    ROOT / "config" / "eao-manifest.yaml",
    ROOT / "config" / "capabilities.yaml",
)

PATH_PREFIXES = (
    "config/",
    "docs/",
    "infrastructure/",
    "ontology/",
    "profiles/",
    "reference/",
    "scripts/",
    "skills/",
    "state/",
    "validation/",
)

ROOT_CONTRACTS = {
    "AGENTS.md",
    "CONTRIBUTING.md",
    "DEPLOY.md",
    "README.md",
    "README.zh-CN.md",
    "REPRODUCE.md",
    "VALIDATE.md",
}


def scalar_value(line: str) -> str | None:
    body = line.split("#", 1)[0].strip()
    if not body:
        return None

    if body.startswith("- "):
        value = body[2:].strip()
    elif ":" in body:
        value = body.split(":", 1)[1].strip()
    else:
        return None

    if not value or value in {"|", "|-", ">", ">-"}:
        return None

    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()

    return value or None


def looks_like_repository_path(value: str) -> bool:
    return value in ROOT_CONTRACTS or value.startswith(PATH_PREFIXES)


def main() -> int:
    failures: list[tuple[str, int, str]] = []
    checked: set[str] = set()

    print("Enterprise AI Office Declarative Path Integrity")
    print("----------------------------------------------")

    for source in DECLARATIVE_FILES:
        if not source.is_file():
            failures.append((source.relative_to(ROOT).as_posix(), 0, "source file missing"))
            continue

        for lineno, line in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
            value = scalar_value(line)
            if value is None or not looks_like_repository_path(value):
                continue

            checked.add(value)
            target = (ROOT / value).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                failures.append((source.relative_to(ROOT).as_posix(), lineno, f"{value} escapes repository"))
                continue

            if not target.exists():
                failures.append((source.relative_to(ROOT).as_posix(), lineno, f"{value} missing"))

    print(f"Declarative files scanned: {len(DECLARATIVE_FILES)}")
    print(f"Repository paths checked:  {len(checked)}")

    if failures:
        print(f"Broken declared paths:      {len(failures)}")
        for source, lineno, reason in failures:
            location = f"{source}:{lineno}" if lineno else source
            print(f"FAIL {location} — {reason}")
        return 2

    print("Broken declared paths:      0")
    print("DECLARATIVE PATH INTEGRITY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
