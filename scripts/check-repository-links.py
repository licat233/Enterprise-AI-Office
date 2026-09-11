#!/usr/bin/env python3
"""Validate repository-local Markdown links without network access.

The checker scans tracked Markdown files only. It validates local file/directory
targets and rejects links that escape the repository. External URLs, mailto
links, document-local anchors, and site-root routes are intentionally ignored.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
FENCE_RE = re.compile(r"^\\s*(\`\`\`|~~~)")
INLINE_LINK_RE = re.compile(r"!?\\[[^\\]]*\\]\\(([^)\\n]+)\\)")
REFERENCE_LINK_RE = re.compile(r"^\\s*\\[[^\\]]+\\]:\\s*(\\S+)", re.MULTILINE)

SKIP_SCHEMES = {
    "http",
    "https",
    "mailto",
    "tel",
    "data",
    "javascript",
}


def tracked_markdown_files() -> list[Path]:
    try:
        completed = subprocess.run(
            ["git", "ls-files", "*.md"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        paths = [ROOT / line for line in completed.stdout.splitlines() if line.strip()]
    except (OSError, subprocess.CalledProcessError):
        paths = list(ROOT.rglob("*.md"))
    return sorted(path for path in paths if path.is_file())


def remove_fenced_code(text: str) -> str:
    result: list[str] = []
    in_fence = False
    fence = ""
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if match:
            token = match.group(1)
            if not in_fence:
                in_fence = True
                fence = token
            elif token == fence:
                in_fence = False
                fence = ""
            result.append("")
            continue
        result.append("" if in_fence else line)
    return "\n".join(result)


def normalize_target(raw: str) -> str | None:
    target = raw.strip()

    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        match = re.match(r"^(.*?)(?:\\s+['\"][^'\"]*['\"])$", target)
        if match:
            target = match.group(1).strip()

    if not target or target.startswith("#"):
        return None

    parsed = urlsplit(target)
    if parsed.scheme.casefold() in SKIP_SCHEMES:
        return None
    if parsed.scheme or target.startswith("//"):
        return None

    if target.startswith("/"):
        return None

    path = unquote(parsed.path)
    if not path:
        return None

    if "<" in path or ">" in path:
        return None

    return path


def local_targets(path: Path) -> list[str]:
    text = remove_fenced_code(path.read_text(encoding="utf-8"))
    targets = [match.group(1) for match in INLINE_LINK_RE.finditer(text)]
    targets.extend(match.group(1) for match in REFERENCE_LINK_RE.finditer(text))
    return targets


def main() -> int:
    checked = 0
    failures: list[tuple[str, str, str]] = []
    root = ROOT.resolve()

    files = tracked_markdown_files()
    for markdown in files:
        rel_source = markdown.relative_to(ROOT).as_posix()
        for raw in local_targets(markdown):
            target = normalize_target(raw)
            if target is None:
                continue
            checked += 1
            resolved = (markdown.parent / target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                failures.append((rel_source, raw, "escapes repository"))
                continue
            if not resolved.exists():
                failures.append((rel_source, raw, "target missing"))

    print("Enterprise AI Office Repository Link Integrity")
    print("---------------------------------------------")
    print(f"Markdown files scanned: {len(files)}")
    print(f"Local links checked:    {checked}")

    if failures:
        print(f"Broken local links:     {len(failures)}")
        for source, target, reason in failures:
            print(f"FAIL {source}: {target!r} — {reason}")
        return 2

    print("Broken local links:     0")
    print("REPOSITORY LINK INTEGRITY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
