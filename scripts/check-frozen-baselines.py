#!/usr/bin/env python3
"""Verify frozen EAO baseline commits remain reachable from the checked HEAD.

The project manifest records local repository commits whose evidence must remain
inspectable. This check uses Git history only; it does not access the network or
validate upstream component commits.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "config" / "eao-manifest.yaml"
FROZEN_RE = re.compile(r"^\s*frozen_commit:\s*([0-9a-f]{40})\s*$", re.MULTILINE)


def git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    if not MANIFEST.is_file():
        print("FAIL config/eao-manifest.yaml is missing")
        return 2

    shas = list(dict.fromkeys(FROZEN_RE.findall(MANIFEST.read_text(encoding="utf-8"))))
    if not shas:
        print("FAIL no frozen_commit entries found in config/eao-manifest.yaml")
        return 2

    failures: list[str] = []

    print("Enterprise AI Office Frozen Baseline History")
    print("-------------------------------------------")
    print(f"Frozen commits declared: {len(shas)}")

    for sha in shas:
        exists = git("cat-file", "-e", f"{sha}^{{commit}}")
        if exists.returncode != 0:
            failures.append(f"{sha}: commit object unavailable in checkout")
            print(f"FAIL {sha} — commit object unavailable")
            continue

        ancestor = git("merge-base", "--is-ancestor", sha, "HEAD")
        if ancestor.returncode != 0:
            failures.append(f"{sha}: not an ancestor of HEAD")
            print(f"FAIL {sha} — not reachable from HEAD")
            continue

        print(f"PASS {sha} — reachable ancestor of HEAD")

    if failures:
        print(f"Failures: {len(failures)}")
        return 2

    print("Failures: 0")
    print("FROZEN BASELINE HISTORY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
