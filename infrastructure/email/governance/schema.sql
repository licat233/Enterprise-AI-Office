-- Enterprise AI Office v2 Email Governance reference SQLite schema
-- Installation Design artifact only. This file does not authorize real deployment.
--
-- Runtime contract: docs/V2-GOVERNANCE-RUNTIME.md

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_meta (
    schema_name TEXT PRIMARY KEY,
    schema_version INTEGER NOT NULL,
    applied_at TEXT NOT NULL
);

INSERT OR IGNORE INTO schema_meta(schema_name, schema_version, applied_at)
VALUES ('email_governance', 1, strftime('%Y-%m-%dT%H:%M:%fZ','now'));

CREATE TABLE IF NOT EXISTS draft_replies (
    draft_id TEXT NOT NULL,
    revision INTEGER NOT NULL CHECK (revision > 0),
    source_message_id TEXT NOT NULL,
    sender_mailbox_id TEXT NOT NULL,
    to_addresses_json TEXT NOT NULL,
    cc_addresses_json TEXT NOT NULL DEFAULT '[]',
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    created_by_actor_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (draft_id, revision),
    UNIQUE (draft_id, revision, content_hash)
);

CREATE INDEX IF NOT EXISTS idx_draft_replies_source_message
ON draft_replies(source_message_id);

CREATE INDEX IF NOT EXISTS idx_draft_replies_mailbox
ON draft_replies(sender_mailbox_id);

CREATE TABLE IF NOT EXISTS send_approvals (
    approval_id TEXT PRIMARY KEY,
    draft_id TEXT NOT NULL,
    draft_revision INTEGER NOT NULL,
    draft_content_hash TEXT NOT NULL,
    approved_by_actor_id TEXT NOT NULL,
    approved_at TEXT NOT NULL,
    valid_until TEXT,
    revoked_at TEXT,
    revoked_by_actor_id TEXT,
    revoke_reason_code TEXT,
    FOREIGN KEY (draft_id, draft_revision)
        REFERENCES draft_replies(draft_id, revision)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    UNIQUE (
        draft_id,
        draft_revision,
        draft_content_hash,
        approved_by_actor_id
    )
);

CREATE INDEX IF NOT EXISTS idx_send_approvals_draft
ON send_approvals(draft_id, draft_revision);

CREATE TABLE IF NOT EXISTS approval_claims (
    approval_id TEXT PRIMARY KEY,
    logical_send_id TEXT NOT NULL UNIQUE,
    claimed_by_actor_id TEXT NOT NULL,
    claimed_at TEXT NOT NULL,
    FOREIGN KEY (approval_id)
        REFERENCES send_approvals(approval_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS governance_audit_events (
    audit_event_id TEXT PRIMARY KEY,
    occurred_at TEXT NOT NULL,
    human_actor_id TEXT,
    human_group_ids_json TEXT NOT NULL DEFAULT '[]',
    assistant_id TEXT,
    profile_context TEXT,
    operation TEXT NOT NULL,
    target_type TEXT,
    target_id TEXT,
    mailbox_id TEXT,
    decision TEXT NOT NULL,
    reason_code TEXT,
    correlation_id TEXT,
    contract_version TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_governance_audit_occurred_at
ON governance_audit_events(occurred_at);

CREATE INDEX IF NOT EXISTS idx_governance_audit_actor
ON governance_audit_events(human_actor_id, occurred_at);

CREATE INDEX IF NOT EXISTS idx_governance_audit_target
ON governance_audit_events(target_type, target_id, occurred_at);

CREATE INDEX IF NOT EXISTS idx_governance_audit_correlation
ON governance_audit_events(correlation_id);

-- Notes:
-- 1. DraftReply revisions are immutable. Application code must never UPDATE
--    material fields on draft_replies after INSERT.
-- 2. SendApproval evidence is immutable except disposition facts used for
--    revocation. Application code must never rewrite draft binding fields.
-- 3. STALE is derived by comparing an approval's bound revision/hash with the
--    current (max) draft revision/hash; it is not persisted as a status.
-- 4. CONSUMED is derived from the existence of approval_claims.
-- 5. One UNIQUE approval_id claim enforces one Approval -> one logical send.
-- 6. Provider send attempt/result/reconciliation state is intentionally added
--    by ID-6, not this ID-5 schema contract.
-- 7. governance_audit_events is append-oriented. Do not UPDATE/DELETE normal
--    historical events as part of ordinary runtime operation.
