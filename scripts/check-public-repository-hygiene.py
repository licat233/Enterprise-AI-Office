#!/usr/bin/env python3
"""High-confidence public repository hygiene checks.

This is intentionally narrower than a full secret-scanning product. It uses Git
as the source of truth, rejects protected/local path classes that must never be
tracked, and detects a small set of high-confidence credential signatures and
sensitive environment assignments with real-looking values.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PREFIXES = (
    "private/",
    "credentials/",
    "secrets/",
    "runtime/",
)

FORBIDDEN_EXACT_PATHS = (
    "state/deployment-state.md",
)

FORBIDDEN_SUFFIXES = (
    ".pem",
    ".key",
    ".p12",
    ".pfx",
    ".secret",
    ".credentials",
)

HIGH_CONFIDENCE_PATTERNS = (
    ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")),
    ("OpenAI-style secret", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
)

SENSITIVE_KEY_SUFFIXES = (
    "API_KEY",
    "ACCESS_KEY",
    "SECRET",
    "TOKEN",
    "PASSWORD",
    "PRIVATE_KEY",
    "CLIENT_SECRET",
)

SAFE_VALUE_MARKERS = (
    "<",
    "${",
    "$(",
    "example",
    "test",
    "dummy",
    "fake",
    "redacted",
    "placeholder",
    "generate_",
    "optional_",
    "set_",
    "change_",
    "replace_",
)


def tracked_files() -> list[Path]:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    result = []
    for raw in completed.stdout.split(b"\0"):
        if not raw:
            continue
        path = ROOT / raw.decode("utf-8")
        if path.is_file():
            result.append(path)
    return sorted(result)


def forbidden_tracked_path(rel: str) -> str | None:
    if rel in FORBIDDEN_EXACT_PATHS:
        return "protected operational deployment state is tracked"

    if rel.startswith(FORBIDDEN_PREFIXES):
        return "protected/local directory is tracked"

    name = Path(rel).name
    lower = name.casefold()

    if lower == ".env":
        return "runtime .env is tracked"
    if lower.startswith(".env.") and lower != ".env.example":
        return "runtime .env variant is tracked"
    if lower.endswith(".env") and not lower.endswith(".env.example"):
        return "runtime env file is tracked"

    if lower.endswith(FORBIDDEN_SUFFIXES):
        return "credential/private-key file type is tracked"

    return None


def read_text(path: Path) -> str | None:
    data = path.read_bytes()
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def obvious_fixture(value: str) -> bool:
    normalized = value.strip().strip("'\"").casefold()
    if not normalized:
        return True
    if normalized in {"none", "null", "false", "true"}:
        return True
    return any(marker in normalized for marker in SAFE_VALUE_MARKERS)


def sensitive_assignment(line: str) -> tuple[str, str] | None:
    body = line.strip()
    if not body or body.startswith("#"):
        return None
    if body.startswith("export "):
        body = body[7:].strip()

    separator = "=" if "=" in body else ":" if ":" in body else None
    if separator is None:
        return None

    key, value = body.split(separator, 1)
    key = key.strip()
    value = value.split("#", 1)[0].strip()

    if not key or not key.replace("_", "").isalnum() or key.upper() != key:
        return None
    if not key.endswith(SENSITIVE_KEY_SUFFIXES):
        return None
    if obvious_fixture(value):
        return None
    return key, value


def main() -> int:
    failures: list[str] = []
    files = tracked_files()
    text_files = 0
    assignment_checks = 0

    for path in files:
        rel = path.relative_to(ROOT).as_posix()

        reason = forbidden_tracked_path(rel)
        if reason:
            failures.append(f"{rel}: {reason}")
            continue

        text = read_text(path)
        if text is None:
            continue
        text_files += 1

        for label, pattern in HIGH_CONFIDENCE_PATTERNS:
            for match in pattern.finditer(text):
                token = match.group(0)
                if obvious_fixture(token):
                    continue
                failures.append(f"{rel}: {label} signature detected")
                break

        for lineno, line in enumerate(text.splitlines(), start=1):
            found = sensitive_assignment(line)
            if found is None:
                continue
            assignment_checks += 1
            key, _value = found
            failures.append(f"{rel}:{lineno}: {key} has a non-placeholder tracked value")

    print("Enterprise AI Office Public Repository Hygiene")
    print("---------------------------------------------")
    print(f"Tracked files scanned:       {len(files)}")
    print(f"Tracked text files scanned:  {text_files}")
    print(f"Sensitive assignments found: {assignment_checks}")

    if failures:
        print(f"Hygiene failures:            {len(failures)}")
        for failure in failures:
            print(f"FAIL {failure}")
        return 2

    print("Hygiene failures:            0")
    print("PUBLIC REPOSITORY HYGIENE: PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as exc:
        print(f"FAIL unable to enumerate tracked files: {exc}")
        sys.exit(2)
