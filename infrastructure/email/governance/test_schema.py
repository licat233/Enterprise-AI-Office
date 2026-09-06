#!/usr/bin/env python3
"""Offline deterministic checks for the v2 Email Governance SQLite contract.

This test uses only Python stdlib + in-memory SQLite. It does not access any
real mailbox, employee identity, provider credential, or network service.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "schema.sql"


def draft_hash(*, draft_id: str, revision: int, source_message_id: str,
               sender_mailbox_id: str, to_addresses: list[str],
               cc_addresses: list[str], subject: str, body: str) -> str:
    payload = {
        "schema": "eao.draft-reply.v1",
        "draft_id": draft_id,
        "revision": revision,
        "source_message_id": source_message_id,
        "sender_mailbox_id": sender_mailbox_id,
        "to_addresses": to_addresses,
        "cc_addresses": cc_addresses,
        "subject": subject,
        "body": body,
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def main() -> None:
    db = sqlite3.connect(":memory:")
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(SCHEMA.read_text(encoding="utf-8"))

    draft_id = "draft-001"
    source_message_id = "message-001"
    mailbox_id = "mailbox-001"
    actor_id = "open-webui:user-001"

    hash_v1 = draft_hash(
        draft_id=draft_id,
        revision=1,
        source_message_id=source_message_id,
        sender_mailbox_id=mailbox_id,
        to_addresses=["customer@example.invalid"],
        cc_addresses=[],
        subject="Re: Test",
        body="Version one",
    )
    assert hash_v1 == draft_hash(
        draft_id=draft_id,
        revision=1,
        source_message_id=source_message_id,
        sender_mailbox_id=mailbox_id,
        to_addresses=["customer@example.invalid"],
        cc_addresses=[],
        subject="Re: Test",
        body="Version one",
    )

    db.execute(
        """
        INSERT INTO draft_replies(
            draft_id, revision, source_message_id, sender_mailbox_id,
            to_addresses_json, cc_addresses_json, subject, body,
            content_hash, created_by_actor_id, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            draft_id,
            1,
            source_message_id,
            mailbox_id,
            json.dumps(["customer@example.invalid"]),
            "[]",
            "Re: Test",
            "Version one",
            hash_v1,
            actor_id,
            "2026-09-06T00:00:00Z",
        ),
    )

    hash_v2 = draft_hash(
        draft_id=draft_id,
        revision=2,
        source_message_id=source_message_id,
        sender_mailbox_id=mailbox_id,
        to_addresses=["customer@example.invalid"],
        cc_addresses=[],
        subject="Re: Test",
        body="Version two",
    )
    db.execute(
        """
        INSERT INTO draft_replies(
            draft_id, revision, source_message_id, sender_mailbox_id,
            to_addresses_json, cc_addresses_json, subject, body,
            content_hash, created_by_actor_id, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            draft_id,
            2,
            source_message_id,
            mailbox_id,
            json.dumps(["customer@example.invalid"]),
            "[]",
            "Re: Test",
            "Version two",
            hash_v2,
            actor_id,
            "2026-09-06T00:01:00Z",
        ),
    )

    revisions = db.execute(
        "SELECT revision, body FROM draft_replies WHERE draft_id=? ORDER BY revision",
        (draft_id,),
    ).fetchall()
    assert revisions == [(1, "Version one"), (2, "Version two")]

    approval_id = "approval-001"
    db.execute(
        """
        INSERT INTO send_approvals(
            approval_id, draft_id, draft_revision, draft_content_hash,
            approved_by_actor_id, approved_at
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            approval_id,
            draft_id,
            2,
            hash_v2,
            actor_id,
            "2026-09-06T00:02:00Z",
        ),
    )

    # Exact same human + exact same Draft approval is replay-safe: schema rejects
    # a second independently reusable approval row.
    try:
        db.execute(
            """
            INSERT INTO send_approvals(
                approval_id, draft_id, draft_revision, draft_content_hash,
                approved_by_actor_id, approved_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                "approval-duplicate",
                draft_id,
                2,
                hash_v2,
                actor_id,
                "2026-09-06T00:02:01Z",
            ),
        )
        raise AssertionError("duplicate approval unexpectedly accepted")
    except sqlite3.IntegrityError:
        pass

    db.execute(
        """
        INSERT INTO approval_claims(
            approval_id, logical_send_id, claimed_by_actor_id, claimed_at
        ) VALUES (?, ?, ?, ?)
        """,
        (approval_id, "send-001", actor_id, "2026-09-06T00:03:00Z"),
    )

    # One Approval cannot authorize a second logical send.
    try:
        db.execute(
            """
            INSERT INTO approval_claims(
                approval_id, logical_send_id, claimed_by_actor_id, claimed_at
            ) VALUES (?, ?, ?, ?)
            """,
            (approval_id, "send-002", actor_id, "2026-09-06T00:03:01Z"),
        )
        raise AssertionError("same approval unexpectedly claimed twice")
    except sqlite3.IntegrityError:
        pass

    db.execute(
        """
        INSERT INTO governance_audit_events(
            audit_event_id, occurred_at, human_actor_id,
            human_group_ids_json, operation, target_type, target_id,
            mailbox_id, decision, reason_code, correlation_id,
            contract_version, policy_version, metadata_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "audit-001",
            "2026-09-06T00:03:00Z",
            actor_id,
            "[]",
            "claim_approval_for_send",
            "SendApproval",
            approval_id,
            mailbox_id,
            "ALLOW",
            "APPROVAL_CLAIMED",
            "corr-001",
            "v2-id5-1.0",
            "baseline",
            "{}",
        ),
    )

    assert db.execute("SELECT COUNT(*) FROM governance_audit_events").fetchone()[0] == 1
    assert db.execute("PRAGMA foreign_keys").fetchone()[0] == 1

    print("PASS — v2 governance SQLite/hash contract")


if __name__ == "__main__":
    main()
