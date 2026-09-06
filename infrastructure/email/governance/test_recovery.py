#!/usr/bin/env python3
"""Offline deterministic recovery checks for v2 Email Governance state.

Uses only Python stdlib, temporary files, and SQLite. No network/provider access.
"""

from __future__ import annotations

import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "schema.sql"
MIGRATION_002 = ROOT / "migrations" / "002_send_reconciliation.sql"
BACKUP_HELPER = ROOT / "backup_state.py"
RESTORE_HELPER = ROOT / "restore_state.py"


def run(*args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != expect:
        raise AssertionError(
            f"unexpected exit {result.returncode}, expected {expect}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def build_source(path: Path) -> None:
    db = sqlite3.connect(path)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(SCHEMA.read_text(encoding="utf-8"))
    db.executescript(MIGRATION_002.read_text(encoding="utf-8"))

    draft_hash = "sha256:" + "a" * 64
    transport_hash = "sha256:" + "b" * 64
    actor = "open-webui:user-001"

    db.execute(
        """
        INSERT INTO draft_replies(
            draft_id, revision, source_message_id, sender_mailbox_id,
            to_addresses_json, cc_addresses_json, subject, body,
            content_hash, created_by_actor_id, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "draft-001", 1, "message-001", "mailbox-001",
            '["customer@example.invalid"]', '[]',
            "Re: Recovery Test", "Synthetic body", draft_hash,
            actor, "2026-09-07T00:00:00Z",
        ),
    )
    db.execute(
        """
        INSERT INTO send_approvals(
            approval_id, draft_id, draft_revision, draft_content_hash,
            approved_by_actor_id, approved_at
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        ("approval-001", "draft-001", 1, draft_hash, actor, "2026-09-07T00:01:00Z"),
    )
    db.execute(
        """
        INSERT INTO approval_claims(
            approval_id, logical_send_id, claimed_by_actor_id, claimed_at
        ) VALUES (?, ?, ?, ?)
        """,
        ("approval-001", "send-001", actor, "2026-09-07T00:02:00Z"),
    )
    db.execute(
        """
        INSERT INTO logical_sends(
            logical_send_id, approval_id,
            draft_id, draft_revision, draft_content_hash,
            sender_mailbox_id, envelope_from, envelope_recipients_json,
            rfc_message_id, date_header, transport_payload_hash,
            initialized_by_actor_id, initialized_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "send-001", "approval-001", "draft-001", 1, draft_hash,
            "mailbox-001", "sales@example.invalid",
            '["customer@example.invalid"]',
            "<eao.send-001@example.invalid>",
            "Mon, 07 Sep 2026 00:02:00 +0000",
            transport_hash, actor, "2026-09-07T00:02:00Z",
        ),
    )
    db.execute(
        """
        INSERT INTO send_attempts(
            attempt_id, logical_send_id, attempt_no,
            provider, endpoint, transport_payload_hash, started_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "attempt-001", "send-001", 1,
            "tencent-exmail", "smtp.example.invalid:465",
            transport_hash, "2026-09-07T00:03:00Z",
        ),
    )
    db.commit()
    db.close()


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="eaio-recovery-") as tmp:
        root = Path(tmp)
        source = root / "state.sqlite3"
        backup = root / "backup.sqlite3"
        restored = root / "restored.sqlite3"
        build_source(source)

        backup_result = run(str(BACKUP_HELPER), str(source), str(backup))
        assert "PASS — GOVERNANCE SQLITE BACKUP" in backup_result.stdout

        restore_result = run(str(RESTORE_HELPER), str(backup), str(restored))
        assert "PASS — GOVERNANCE SQLITE RESTORE" in restore_result.stdout
        assert "unresolved_attempts=1" in restore_result.stdout
        assert "RECONCILIATION_REQUIRED" in restore_result.stdout

        db = sqlite3.connect(restored)
        assert db.execute(
            "SELECT COUNT(*) FROM draft_replies WHERE draft_id='draft-001'"
        ).fetchone()[0] == 1
        assert db.execute(
            "SELECT COUNT(*) FROM send_approvals WHERE approval_id='approval-001'"
        ).fetchone()[0] == 1
        assert db.execute(
            "SELECT COUNT(*) FROM send_attempts WHERE attempt_id='attempt-001'"
        ).fetchone()[0] == 1
        assert db.execute(
            "SELECT COUNT(*) FROM send_attempt_results WHERE attempt_id='attempt-001'"
        ).fetchone()[0] == 0
        db.close()

        # Corrupt material must be rejected, not materialized as a usable target.
        corrupt = root / "corrupt.sqlite3"
        corrupt.write_bytes(b"not-a-sqlite-database")
        corrupt_target = root / "corrupt-target.sqlite3"
        corrupt_result = run(
            str(RESTORE_HELPER), str(corrupt), str(corrupt_target), expect=1
        )
        assert "FAIL — GOVERNANCE BACKUP INTEGRITY" in corrupt_result.stderr
        assert not corrupt_target.exists()

        # A backup from a newer schema must fail closed rather than be downgraded.
        newer = root / "newer.sqlite3"
        shutil.copy2(backup, newer)
        db = sqlite3.connect(newer)
        db.execute(
            "UPDATE schema_meta SET schema_version=999 WHERE schema_name='email_governance'"
        )
        db.commit()
        db.close()
        newer_target = root / "newer-target.sqlite3"
        newer_result = run(
            str(RESTORE_HELPER), str(newer), str(newer_target), expect=3
        )
        assert "BLOCKED — SCHEMA VERSION NEWER THAN RUNTIME" in newer_result.stderr
        assert not newer_target.exists()

    print("PASS — v2 governance backup/restore/recovery contract")


if __name__ == "__main__":
    main()
