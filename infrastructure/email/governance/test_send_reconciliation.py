#!/usr/bin/env python3
"""Offline deterministic checks for ID-6 send/reconciliation SQLite evidence.

Uses only Python stdlib + in-memory SQLite. No real SMTP/IMAP/network access.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "schema.sql"
MIGRATION_002 = ROOT / "migrations" / "002_send_reconciliation.sql"


def main() -> None:
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(SCHEMA.read_text(encoding="utf-8"))
    db.executescript(MIGRATION_002.read_text(encoding="utf-8"))

    version = db.execute(
        "SELECT schema_version FROM schema_meta WHERE schema_name='email_governance'"
    ).fetchone()[0]
    assert version == 2

    draft_hash = "sha256:" + "a" * 64
    actor_id = "open-webui:user-001"

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
            "Re: Test", "Hello", draft_hash, actor_id,
            "2026-09-07T00:00:00Z",
        ),
    )

    db.execute(
        """
        INSERT INTO send_approvals(
            approval_id, draft_id, draft_revision, draft_content_hash,
            approved_by_actor_id, approved_at
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "approval-001", "draft-001", 1, draft_hash,
            actor_id, "2026-09-07T00:01:00Z",
        ),
    )

    db.execute(
        """
        INSERT INTO approval_claims(
            approval_id, logical_send_id, claimed_by_actor_id, claimed_at
        ) VALUES (?, ?, ?, ?)
        """,
        (
            "approval-001", "send-001", actor_id,
            "2026-09-07T00:02:00Z",
        ),
    )

    # Logical send must match the committed ApprovalClaim pair.
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
            "send-001", "approval-001",
            "draft-001", 1, draft_hash,
            "mailbox-001", "sales@example.invalid",
            '["customer@example.invalid"]',
            "<eao.send-001@example.invalid>",
            "Mon, 07 Sep 2026 00:02:00 +0000",
            "sha256:" + "b" * 64,
            actor_id,
            "2026-09-07T00:02:00Z",
        ),
    )

    try:
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
                "send-mismatch", "approval-001",
                "draft-001", 1, draft_hash,
                "mailbox-001", "sales@example.invalid",
                '["customer@example.invalid"]',
                "<eao.send-mismatch@example.invalid>",
                "Mon, 07 Sep 2026 00:02:00 +0000",
                "sha256:" + "b" * 64,
                actor_id,
                "2026-09-07T00:02:00Z",
            ),
        )
        raise AssertionError("logical send without matching claim unexpectedly accepted")
    except sqlite3.IntegrityError:
        pass

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
            "sha256:" + "b" * 64,
            "2026-09-07T00:03:00Z",
        ),
    )

    # Durable attempt without terminal result must be detectable and therefore
    # treated by runtime as reconciliation-required after restart.
    unresolved = db.execute(
        """
        SELECT a.attempt_id
        FROM send_attempts AS a
        LEFT JOIN send_attempt_results AS r ON r.attempt_id = a.attempt_id
        WHERE a.logical_send_id=? AND r.attempt_id IS NULL
        """,
        ("send-001",),
    ).fetchall()
    assert unresolved == [("attempt-001",)]

    db.execute(
        """
        INSERT INTO send_attempt_results(
            attempt_id, observed_at, outcome, smtp_stage,
            smtp_code, provider_reference, diagnostic_code, diagnostic_summary
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "attempt-001", "2026-09-07T00:03:05Z",
            "OUTCOME_UNKNOWN", "DATA", None, None,
            "DATA_TRANSPORT_OUTCOME_UNKNOWN", "synthetic timeout",
        ),
    )

    # Attempt numbers are unique within one logical send.
    try:
        db.execute(
            """
            INSERT INTO send_attempts(
                attempt_id, logical_send_id, attempt_no,
                provider, endpoint, transport_payload_hash, started_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "attempt-duplicate-number", "send-001", 1,
                "tencent-exmail", "smtp.example.invalid:465",
                "sha256:" + "b" * 64,
                "2026-09-07T00:04:00Z",
            ),
        )
        raise AssertionError("duplicate attempt number unexpectedly accepted")
    except sqlite3.IntegrityError:
        pass

    db.execute(
        """
        INSERT INTO send_reconciliations(
            reconciliation_id, logical_send_id, attempt_id,
            performed_by_actor_id, performed_at,
            evidence_type, evidence_reference, conclusion, sanitized_note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "recon-001", "send-001", "attempt-001",
            "operator:synthetic", "2026-09-07T00:05:00Z",
            "provider-log", "synthetic-provider-reference",
            "REMAINS_UNKNOWN", "no trustworthy acceptance evidence",
        ),
    )

    # Reconciliation is append-only evidence: original attempt observation remains.
    original = db.execute(
        "SELECT outcome FROM send_attempt_results WHERE attempt_id='attempt-001'"
    ).fetchone()[0]
    conclusion = db.execute(
        "SELECT conclusion FROM send_reconciliations WHERE reconciliation_id='recon-001'"
    ).fetchone()[0]
    assert original == "OUTCOME_UNKNOWN"
    assert conclusion == "REMAINS_UNKNOWN"

    print("PASS — v2 send/reconciliation SQLite contract")


if __name__ == "__main__":
    main()
