-- Enterprise AI Office v2 Email Governance schema migration 002
-- Adds governed logical-send / provider-attempt / reconciliation evidence.
-- Installation Design artifact only; does not authorize real SMTP use.
--
-- The application migration runner MUST verify current schema_version == 1
-- before applying this file. Unknown/newer versions fail closed.

BEGIN IMMEDIATE;

CREATE UNIQUE INDEX IF NOT EXISTS idx_approval_claim_pair
ON approval_claims(approval_id, logical_send_id);

CREATE TABLE IF NOT EXISTS logical_sends (
    logical_send_id TEXT PRIMARY KEY,
    approval_id TEXT NOT NULL UNIQUE,
    draft_id TEXT NOT NULL,
    draft_revision INTEGER NOT NULL,
    draft_content_hash TEXT NOT NULL,
    sender_mailbox_id TEXT NOT NULL,
    envelope_from TEXT NOT NULL,
    envelope_recipients_json TEXT NOT NULL,
    rfc_message_id TEXT NOT NULL UNIQUE,
    date_header TEXT NOT NULL,
    transport_payload_hash TEXT NOT NULL,
    initialized_by_actor_id TEXT NOT NULL,
    initialized_at TEXT NOT NULL,
    FOREIGN KEY (approval_id)
        REFERENCES send_approvals(approval_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    FOREIGN KEY (draft_id, draft_revision, draft_content_hash)
        REFERENCES draft_replies(draft_id, revision, content_hash)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_logical_sends_draft
ON logical_sends(draft_id, draft_revision);

CREATE INDEX IF NOT EXISTS idx_logical_sends_mailbox
ON logical_sends(sender_mailbox_id, initialized_at);

CREATE TRIGGER IF NOT EXISTS trg_logical_send_requires_matching_claim
BEFORE INSERT ON logical_sends
FOR EACH ROW
WHEN NOT EXISTS (
    SELECT 1
    FROM approval_claims AS c
    WHERE c.approval_id = NEW.approval_id
      AND c.logical_send_id = NEW.logical_send_id
)
BEGIN
    SELECT RAISE(ABORT, 'logical_send does not match committed approval claim');
END;

CREATE TABLE IF NOT EXISTS send_attempts (
    attempt_id TEXT PRIMARY KEY,
    logical_send_id TEXT NOT NULL,
    attempt_no INTEGER NOT NULL CHECK (attempt_no > 0),
    provider TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    transport_payload_hash TEXT NOT NULL,
    started_at TEXT NOT NULL,
    FOREIGN KEY (logical_send_id)
        REFERENCES logical_sends(logical_send_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    UNIQUE (logical_send_id, attempt_no)
);

CREATE INDEX IF NOT EXISTS idx_send_attempts_logical_send
ON send_attempts(logical_send_id, attempt_no);

CREATE TABLE IF NOT EXISTS send_attempt_results (
    attempt_id TEXT PRIMARY KEY,
    observed_at TEXT NOT NULL,
    outcome TEXT NOT NULL CHECK (
        outcome IN ('SENT', 'CONFIRMED_NOT_SENT', 'OUTCOME_UNKNOWN')
    ),
    smtp_stage TEXT NOT NULL,
    smtp_code INTEGER,
    provider_reference TEXT,
    diagnostic_code TEXT,
    diagnostic_summary TEXT,
    FOREIGN KEY (attempt_id)
        REFERENCES send_attempts(attempt_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS send_reconciliations (
    reconciliation_id TEXT PRIMARY KEY,
    logical_send_id TEXT NOT NULL,
    attempt_id TEXT,
    performed_by_actor_id TEXT,
    performed_at TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    evidence_reference TEXT NOT NULL,
    conclusion TEXT NOT NULL CHECK (
        conclusion IN ('SENT', 'CONFIRMED_NOT_SENT', 'REMAINS_UNKNOWN')
    ),
    sanitized_note TEXT,
    FOREIGN KEY (logical_send_id)
        REFERENCES logical_sends(logical_send_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,
    FOREIGN KEY (attempt_id)
        REFERENCES send_attempts(attempt_id)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_send_reconciliations_logical_send
ON send_reconciliations(logical_send_id, performed_at);

UPDATE schema_meta
SET schema_version = 2,
    applied_at = strftime('%Y-%m-%dT%H:%M:%fZ','now')
WHERE schema_name = 'email_governance'
  AND schema_version = 1;

COMMIT;
