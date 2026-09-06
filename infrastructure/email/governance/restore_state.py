#!/usr/bin/env python3
"""Restore EAO Email Governance SQLite state into a new isolated target.

Installation Design helper only. This script never starts the Governance service
and never performs provider/network operations.
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

SUPPORTED_SCHEMA_VERSION = 2


def fail(message: str, code: int = 1) -> "NoReturn":
    print(f"FAIL — GOVERNANCE BACKUP INTEGRITY: {message}", file=sys.stderr)
    raise SystemExit(code)


def blocked(message: str) -> "NoReturn":
    print(f"BLOCKED — SCHEMA VERSION NEWER THAN RUNTIME: {message}", file=sys.stderr)
    raise SystemExit(3)


def integrity_check(conn: sqlite3.Connection, label: str) -> None:
    row = conn.execute("PRAGMA integrity_check").fetchone()
    if not row or row[0] != "ok":
        fail(f"{label} integrity_check failed: {row[0] if row else 'no result'}")

    violations = conn.execute("PRAGMA foreign_key_check").fetchall()
    if violations:
        fail(f"{label} foreign_key_check reported {len(violations)} violation(s)")


def schema_version(conn: sqlite3.Connection) -> int:
    try:
        row = conn.execute(
            "SELECT schema_version FROM schema_meta WHERE schema_name='email_governance'"
        ).fetchone()
    except sqlite3.DatabaseError as exc:
        fail(f"schema metadata unavailable: {exc}")
    if not row:
        fail("email_governance schema metadata missing")
    return int(row[0])


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return (
        conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
            (name,),
        ).fetchone()
        is not None
    )


def unresolved_attempt_count(conn: sqlite3.Connection) -> int:
    if not table_exists(conn, "send_attempts") or not table_exists(conn, "send_attempt_results"):
        return 0
    row = conn.execute(
        """
        SELECT COUNT(*)
        FROM send_attempts AS a
        LEFT JOIN send_attempt_results AS r ON r.attempt_id = a.attempt_id
        WHERE r.attempt_id IS NULL
        """
    ).fetchone()
    return int(row[0]) if row else 0


def unknown_result_count(conn: sqlite3.Connection) -> int:
    if not table_exists(conn, "send_attempt_results"):
        return 0
    row = conn.execute(
        "SELECT COUNT(*) FROM send_attempt_results WHERE outcome='OUTCOME_UNKNOWN'"
    ).fetchone()
    return int(row[0]) if row else 0


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: restore_state.py BACKUP_STATE.sqlite3 NEW_TARGET_STATE.sqlite3", file=sys.stderr)
        raise SystemExit(2)

    backup = Path(sys.argv[1]).expanduser().resolve()
    target = Path(sys.argv[2]).expanduser().resolve()

    if not backup.is_file():
        fail(f"backup database not found: {backup}")
    if target.exists() or target.is_symlink():
        fail(f"target already exists: {target}")
    if not target.parent.is_dir():
        fail(f"target parent does not exist: {target.parent}")
    if backup == target:
        fail("backup and target must differ")

    try:
        src = sqlite3.connect(f"file:{backup}?mode=ro", uri=True)
        src.execute("PRAGMA foreign_keys = ON")
        integrity_check(src, "backup")
        version = schema_version(src)
        if version > SUPPORTED_SCHEMA_VERSION:
            src.close()
            blocked(f"backup={version} supported<={SUPPORTED_SCHEMA_VERSION}")

        dst = sqlite3.connect(str(target))
        try:
            src.backup(dst)
            dst.execute("PRAGMA foreign_keys = ON")
            integrity_check(dst, "restored target")
            restored_version = schema_version(dst)
            if restored_version != version:
                fail(
                    f"schema version changed during restore: backup={version} target={restored_version}"
                )
            unresolved = unresolved_attempt_count(dst)
            unknown = unknown_result_count(dst)
            dst.commit()
        finally:
            dst.close()
            src.close()
    except sqlite3.Error as exc:
        if target.exists():
            try:
                target.unlink()
            except OSError:
                pass
        fail(f"sqlite restore failed: {exc}")

    os.chmod(target, 0o600)
    print(
        "PASS — GOVERNANCE SQLITE RESTORE "
        f"schema_version={version} unresolved_attempts={unresolved} "
        f"unknown_results={unknown} target={target}"
    )
    if unresolved or unknown:
        print(
            "RECONCILIATION_REQUIRED — restored send evidence contains unresolved/unknown outcomes; no retry was executed"
        )


if __name__ == "__main__":
    main()
