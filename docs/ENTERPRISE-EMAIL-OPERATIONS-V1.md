# Enterprise AI Email Operations v1.0

Status: Phase 1 implementation complete on the requested branch. This
document records the bounded runtime contract; it does not authorize a
production schedule, live mailbox login, SMTP send, or automatic sending.

## Reused

- The frozen Email Ontology and DraftReply immutable-revision contract.
- The existing governance SQLite schema, with additive idempotency and actor
  evidence fields.
- The existing read-only Tencent Enterprise Mail IMAP adapter for the
  provider boundary.
- The existing send, approval, reconciliation, backup, and recovery contract
  documents and their offline tests.
- The validated Operations profile boundary: Memory OFF, Agent Delegate OFF,
  terminal/shell/filesystem/browser/code tools OFF, and no
  email-inbox-triage skill.
- The existing sales-discovery-coach, sales-coach, product-marketing, and
  governed WeKnora knowledge path as reusable context layers.

## New in Phase 1

- A standard-library-only thin GovernanceService in
  infrastructure/email/governance/runtime.py.
- ServiceActor identity service:hermes-cron:operations with a dedicated
  credential boundary. The runtime accepts only email.read and email.draft for
  this actor and denies email.approve and email.send.
- Explicit actor_type and actor_id audit evidence, while preserving the
  existing human_actor_id compatibility field.
- A governed scheduled-draft idempotency mapping keyed by workflow version,
  mailbox logical ID, and source Message-ID.
- Three scheduled-runtime operations only:
  search_email, get_email, and prepare_reply_draft over a fixed MCP stdio
  surface.
- A safe synthetic operator dry run and offline Phase 1 tests.
- A thin department skill at
  skills/shared/department/armor-email-operations/SKILL.md.

The runtime preserves the source Message-ID as the draft source identity.
Provider-specific reply headers remain the responsibility of the existing
adapter contract; this phase does not create a shadow thread database or
bulk-ingest WeKnora email data.

## Deferred

- No production Hermes Cron job is created in Phase 1.
- No live IMAP authentication or customer mailbox access is performed.
- No SMTP connection, provider send, Open WebUI action binding, or customer
  communication is performed.
- No AUTO_SEND path exists. Human approval and send remain separate governed
  control-plane actions.
- No new database, mail cache, generic mail tool, raw IMAP/SMTP surface,
  Himalaya surface, or high-risk toolset is enabled.
- Credential provisioning, mailbox policy activation, and deployment
  readiness remain operator-governed follow-up work.

## Safe acceptance

Use the synthetic dry run and offline tests with the managed Hermes Python
environment. They prove schema, authorization, idempotency, immutability, and
surface-boundary behavior only. They do not prove live provider acceptance,
delivery, reboot recovery, or company deployment.
