#!/usr/bin/env python3
"""Create a consistent backup of the EAO Email Governance SQLite database.

Installation Design helper only. This script performs no provider/network action
and never starts the Governance service.
"""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path


def fail(message: str, code: int = 1) -> "NoReturn":
    print(f"FAIL — GOVERNANCE BACKUP: {message}", file=sys.stderr)
    raise SystemExit(code)


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


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: backup_state.py SOURCE_STATE.sqlite3 DEST_BACKUP.sqlite3", file=sys.stderr)
        raise SystemExit(2)

    source = Path(sys.argv[1]).expanduser().resolve()
    destination = Path(sys.argv[2]).expanduser().resolve()

    if not source.is_file():
        fail(f"source database not found: {source}")
    if destination.exists() or destination.is_symlink():
        fail(f"destination already exists: {destination}")
    if not destination.parent.is_dir():
        fail(f"destination parent does not exist: {destination.parent}")
    if source == destination:
        fail("source and destination must differ")

    try:
        src = sqlite3.connect(f"file:{source}?mode=ro", uri=True)
        src.execute("PRAGMA foreign_keys = ON")
        integrity_check(src, "source")
        version = schema_version(src)

        dst = sqlite3.connect(str(destination))
        try:
            src.backup(dst)
            dst.execute("PRAGMA foreign_keys = ON")
            integrity_check(dst, "backup")
            copied_version = schema_version(dst)
            if copied_version != version:
                fail(
                    f"schema version changed during backup: source={version} backup={copied_version}"
                )
            dst.commit()
        finally:
            dst.close()
            src.close()
    except sqlite3.Error as exc:
        if destination.exists():
            try:
                destination.unlink()
            except OSError:
                pass
        fail(f"sqlite backup failed: {exc}")

    os.chmod(destination, 0o600)
    print(
        "PASS — GOVERNANCE SQLITE BACKUP "
        f"schema_version={version} source={source} destination={destination}"
    )


if __name__ == "__main__":
    main()
