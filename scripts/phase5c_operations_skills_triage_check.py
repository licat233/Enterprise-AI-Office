#!/usr/bin/env python3
"""Deterministic acceptance checks for the Phase 5C legacy operations triage."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


EXPECTED_PROFILE_EXPOSURES = {
    "web-ops": 110,
    "social-ops": 92,
    "mic-ops": 153,
    "design-ops": 97,
    "armor-fallback-content-worker": 4,
    "armor-independent-auditor": 4,
}
VALID_CLASSIFICATIONS = {
    "MIGRATED",
    "ABSORBED",
    "KEEP_MIGRATE",
    "REFERENCE_ONLY",
    "EXPERIMENTAL_HOLD",
    "DO_NOT_MIGRATE",
    "DUPLICATE",
}
DELEGATE_SKILLS = {
    "agents-orchestrator",
    "coding-agent-delegation",
    "kanban-codex-lane",
    "kanban-orchestrator",
    "kanban-worker",
    "kanban-system",
    "codex",
    "claude-code",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv",
        default="docs/inventory/legacy-operations-skills-triage.csv",
        type=Path,
    )
    parser.add_argument(
        "--report",
        default="docs/PHASE5C-REMAINING-OPERATIONS-SKILLS-TRIAGE.md",
        type=Path,
    )
    parser.add_argument("--runtime-config", type=Path)
    parser.add_argument("--operations-skills-root", type=Path)
    args = parser.parse_args()

    failures: list[str] = []
    passes: list[str] = []

    def check(condition: bool, label: str, detail: str = "") -> None:
        if condition:
            passes.append(label)
        else:
            failures.append(f"{label}: {detail}" if detail else label)

    try:
        with args.csv.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except OSError as exc:
        failures.append(f"inventory readable: {exc}")
        rows = []

    required = {
        "legacy_profile",
        "skill_name",
        "resolved_source",
        "source_kind",
        "content_identity",
        "business_capability",
        "classification",
        "duplicate_of",
        "enterprise_equivalent",
        "priority",
        "machine_specific",
        "external_action_risk",
        "exposure_count",
        "identity_relation",
        "skill_md_sha256",
        "notes",
    }
    actual = set(rows[0]) if rows else set()
    check(not rows or required <= actual, "inventory schema")
    check(len(rows) == 433, "deduplicated inventory row count", f"got {len(rows)}")

    classifications = {row.get("classification", "") for row in rows}
    check(
        classifications <= VALID_CLASSIFICATIONS,
        "classification vocabulary",
        f"unknown={sorted(classifications - VALID_CLASSIFICATIONS)}",
    )
    check(
        "KEEP_MIGRATE" not in classifications,
        "v1.0 ledger has no unresolved KEEP_MIGRATE rows",
        "mature Phase 5C candidates must be finalized or moved to Post-v1.0 Backlog",
    )
    final_classifications = VALID_CLASSIFICATIONS - {"KEEP_MIGRATE"}
    check(
        final_classifications <= classifications,
        "final classification vocabulary represented",
        f"missing={sorted(final_classifications - classifications)}",
    )

    profile_rows = [row for row in rows if row.get("legacy_profile") != "global-only"]
    exposure_sum = sum(int(row.get("exposure_count", "0")) for row in profile_rows)
    check(exposure_sum == 460, "active Profile exposure accounting", f"got {exposure_sum}")
    for profile, expected in EXPECTED_PROFILE_EXPOSURES.items():
        # A deduplicated row may represent one exposure in several Profiles;
        # exposure_count is the cross-Profile total, so per-Profile accounting
        # counts membership once for each listed Profile.
        observed = sum(1 for row in profile_rows if profile in row["legacy_profile"].split(","))
        check(observed == expected, f"{profile} exposure count", f"got {observed}")

    for row in rows:
        if row.get("classification") == "KEEP_MIGRATE":
            check(
                row.get("priority") in {"P0", "P1", "P2", "P3"},
                f"KEEP_MIGRATE priority: {row.get('skill_name')}",
            )
        if row.get("classification") == "DUPLICATE":
            check(bool(row.get("duplicate_of")), f"duplicate target: {row.get('skill_name')}")

    for skill in DELEGATE_SKILLS:
        matching = [row for row in rows if row.get("skill_name") == skill]
        check(bool(matching), f"Delegate inventory entry: {skill}")
        check(
            bool(matching) and all(row.get("classification") == "EXPERIMENTAL_HOLD" for row in matching),
            f"Delegate hold: {skill}",
        )

    if args.report.exists():
        report_text = args.report.read_text(encoding="utf-8")
        for phrase in (
            "Multi-Agent Orchestration: EXPERIMENTAL_HOLD",
            "Agent Delegate migrated: NO",
            "Operations delegation: OFF",
            "Legacy Memory accessed: NO",
        ):
            check(phrase in report_text, f"report decision: {phrase}")

    if args.runtime_config:
        try:
            runtime_text = args.runtime_config.read_text(encoding="utf-8")
        except OSError as exc:
            failures.append(f"Operations runtime config readable: {exc}")
            runtime_text = ""
        check("memory_enabled: false" in runtime_text, "Operations Hermes memory disabled")
        check("- delegation" in runtime_text, "Operations delegation disabled")
        check("external_dirs: []" in runtime_text, "Operations external Skill dirs empty")
        check("project_discovery: false" in runtime_text, "Operations project discovery disabled")

    if args.operations_skills_root:
        try:
            exposed = {entry.name for entry in args.operations_skills_root.iterdir()}
        except OSError as exc:
            failures.append(f"Operations Skill root readable: {exc}")
            exposed = set()
        prohibited = {
            "armor-fallback-content-worker",
            "armor-independent-auditor",
            "coding-agent-delegation",
            "codex",
            "claude-code",
            "kanban-system",
            "kanban-orchestrator",
            "kanban-worker",
        }
        check(not (exposed & prohibited), "Operations Delegate runtime not exposed", f"found={sorted(exposed & prohibited)}")

    for label in passes:
        print(f"PASS: {label}")
    for failure in failures:
        print(f"FAIL: {failure}")
    print(f"Phase 5C triage check: {len(passes)} PASS / {len(failures)} FAIL")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
