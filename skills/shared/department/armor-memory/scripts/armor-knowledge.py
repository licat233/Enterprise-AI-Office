#!/usr/bin/env python3
"""Read-only knowledge quality checks for ARMOR Minimal Stable."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


AUTHORITY_VALUES = {"working", "verified", "canonical", "evidence"}
PROVENANCE_FIELDS = {"source_ref", "source", "sources", "approved_by"}
KEY_PATTERN = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
H1_PATTERN = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
SOURCE_HEADING_PATTERN = re.compile(r"^#{1,6}\s+sources?\s*$", re.IGNORECASE | re.MULTILINE)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str


@dataclass(frozen=True)
class KnowledgeDocument:
    path: Path
    relative_path: str
    metadata: dict[str, object]
    body: str
    title: str | None
    normalized_title: str | None
    authority: str | None


def strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """Extract the simple top-level metadata ARMOR quality checks need.

    This is intentionally not a full YAML parser. It recognizes top-level scalar
    values and simple dash lists without adding an external dependency.
    """

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    closing_index: int | None = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        return {}, text

    metadata: dict[str, object] = {}
    current_list_key: str | None = None

    for raw_line in lines[1:closing_index]:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        if raw_line[:1].isspace():
            stripped = raw_line.strip()
            if current_list_key and stripped.startswith("-"):
                item = strip_scalar(stripped[1:].strip())
                existing = metadata.setdefault(current_list_key, [])
                if isinstance(existing, list) and item:
                    existing.append(item)
            continue

        match = KEY_PATTERN.match(raw_line)
        if not match:
            current_list_key = None
            continue

        key, raw_value = match.groups()
        value = raw_value.strip()
        if value:
            metadata[key] = strip_scalar(value)
            current_list_key = None
        else:
            metadata[key] = []
            current_list_key = key

    body = "\n".join(lines[closing_index + 1 :])
    if text.endswith("\n"):
        body += "\n"
    return metadata, body


def normalize_title(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold().strip()
    normalized = re.sub(r"[`*_~]", "", normalized)
    normalized = re.sub(r"[^\w]+", " ", normalized, flags=re.UNICODE)
    return " ".join(normalized.split())


def extract_title(body: str) -> str | None:
    match = H1_PATTERN.search(body)
    if not match:
        return None
    title = match.group(1).strip().strip("#").strip()
    return title or None


def has_provenance(metadata: dict[str, object], body: str) -> bool:
    for field in PROVENANCE_FIELDS:
        value = metadata.get(field)
        if isinstance(value, list) and value:
            return True
        if isinstance(value, str) and value.strip() and value.strip() not in {"[]", "null", "None"}:
            return True
    return SOURCE_HEADING_PATTERN.search(body) is not None


def load_document(path: Path, vault_root: Path) -> KnowledgeDocument:
    text = path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(text)
    raw_authority = metadata.get("authority")
    authority = raw_authority.strip().casefold() if isinstance(raw_authority, str) else None
    title = extract_title(body)
    normalized_title = normalize_title(title) if title else None
    return KnowledgeDocument(
        path=path,
        relative_path=path.relative_to(vault_root).as_posix(),
        metadata=metadata,
        body=body,
        title=title,
        normalized_title=normalized_title,
        authority=authority,
    )


def resolve_vault_root(explicit: str | None) -> Path:
    raw_root = explicit or os.environ.get("ARMOR_VAULT_ROOT")
    if not raw_root:
        raise ValueError("ARMOR_VAULT_ROOT is required unless --vault is provided")
    root = Path(raw_root).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"vault root does not exist or is not a directory: {root}")
    knowledge_root = root / "01-Knowledge"
    if not knowledge_root.is_dir():
        raise ValueError(f"knowledge directory not found: {knowledge_root}")
    return root


def audit_knowledge(vault_root: Path) -> tuple[dict[str, object], list[Finding]]:
    knowledge_root = vault_root / "01-Knowledge"
    paths = sorted(path for path in knowledge_root.rglob("*.md") if path.is_file())
    findings: list[Finding] = []
    documents: list[KnowledgeDocument] = []
    authority_counts: Counter[str] = Counter()

    for path in paths:
        relative_path = path.relative_to(vault_root).as_posix()
        try:
            document = load_document(path, vault_root)
        except (OSError, UnicodeError) as exc:
            findings.append(Finding("error", "read_failure", relative_path, str(exc)))
            continue

        documents.append(document)
        authority = document.authority
        authority_counts[authority or "missing"] += 1

        if authority is None:
            findings.append(
                Finding(
                    "warning",
                    "missing_authority",
                    relative_path,
                    "Knowledge has no explicit authority; Minimal Stable treats it as working.",
                )
            )
        elif authority not in AUTHORITY_VALUES:
            findings.append(
                Finding(
                    "error",
                    "invalid_authority",
                    relative_path,
                    f"Unsupported authority value: {authority!r}.",
                )
            )
        elif authority == "evidence":
            findings.append(
                Finding(
                    "warning",
                    "evidence_in_knowledge",
                    relative_path,
                    "Evidence normally belongs in 03-Records; confirm this file is correctly classified.",
                )
            )

        if authority in {"verified", "canonical"} and not has_provenance(document.metadata, document.body):
            findings.append(
                Finding(
                    "warning",
                    "provenance_not_declared",
                    relative_path,
                    f"{authority.capitalize()} knowledge has no explicit source/provenance marker.",
                )
            )

    title_groups: dict[str, list[KnowledgeDocument]] = defaultdict(list)
    for document in documents:
        if document.normalized_title:
            title_groups[document.normalized_title].append(document)

    for normalized_title, group in sorted(title_groups.items()):
        if len(group) < 2:
            continue
        canonical_group = [document for document in group if document.authority == "canonical"]
        paths_text = ", ".join(document.relative_path for document in group)
        code = "possible_canonical_title_collision" if len(canonical_group) > 1 else "duplicate_title"
        for document in group:
            findings.append(
                Finding(
                    "warning",
                    code,
                    document.relative_path,
                    f"Possible duplicate knowledge title {normalized_title!r}: {paths_text}",
                )
            )

    severity_counts = Counter(finding.severity for finding in findings)
    summary: dict[str, object] = {
        "knowledge_files": len(paths),
        "authority": dict(sorted(authority_counts.items())),
        "errors": severity_counts.get("error", 0),
        "warnings": severity_counts.get("warning", 0),
    }
    return summary, findings


def print_human_report(vault_root: Path, summary: dict[str, object], findings: list[Finding]) -> None:
    print("ARMOR Knowledge Quality")
    print(f"Vault: {vault_root}")
    print(f"Knowledge files: {summary['knowledge_files']}")
    print(f"Authority: {json.dumps(summary['authority'], ensure_ascii=False, sort_keys=True)}")
    print(f"Errors: {summary['errors']}")
    print(f"Warnings: {summary['warnings']}")

    if not findings:
        print("Findings: none")
        return

    print("Findings:")
    for finding in findings:
        print(f"- {finding.severity.upper()} [{finding.code}] {finding.path}: {finding.message}")


def run_check(args: argparse.Namespace) -> int:
    try:
        vault_root = resolve_vault_root(args.vault)
        summary, findings = audit_knowledge(vault_root)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        payload = {
            "vault": str(vault_root),
            "scope": "01-Knowledge",
            "summary": summary,
            "findings": [asdict(finding) for finding in findings],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print_human_report(vault_root, summary, findings)

    return 1 if any(finding.severity == "error" for finding in findings) else 0


def run_diff(args: argparse.Namespace) -> int:
    current = Path(args.current).expanduser()
    candidate = Path(args.candidate).expanduser()

    for label, path in (("current", current), ("candidate", candidate)):
        if not path.is_file():
            print(f"ERROR: {label} file not found: {path}", file=sys.stderr)
            return 2

    try:
        current_lines = current.read_text(encoding="utf-8").splitlines(keepends=True)
        candidate_lines = candidate.read_text(encoding="utf-8").splitlines(keepends=True)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    diff = list(
        difflib.unified_diff(
            current_lines,
            candidate_lines,
            fromfile=str(current),
            tofile=str(candidate),
        )
    )
    if not diff:
        print("No changes.")
        return 0

    sys.stdout.writelines(diff)
    if diff and not diff[-1].endswith("\n"):
        print()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only knowledge quality tools for ARMOR Minimal Stable."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser(
        "check",
        help="Audit 01-Knowledge without modifying the Vault.",
    )
    check_parser.add_argument(
        "--vault",
        help="Vault root. Defaults to ARMOR_VAULT_ROOT.",
    )
    check_parser.add_argument("--json", action="store_true", help="Output JSON.")
    check_parser.set_defaults(handler=run_check)

    diff_parser = subparsers.add_parser(
        "diff",
        help="Preview a candidate Markdown change without writing it.",
    )
    diff_parser.add_argument("current", help="Current Markdown file.")
    diff_parser.add_argument("candidate", help="Candidate Markdown file.")
    diff_parser.set_defaults(handler=run_diff)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
