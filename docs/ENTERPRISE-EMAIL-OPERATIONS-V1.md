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

## Threat model — Indirect Prompt Injection

Email is attacker-controlled external content. Security does not depend on
the LLM reliably refusing jailbreak instructions.

The primary protection layers are:

1. deterministic authorization;
2. least privilege;
3. explicit separation of provider metadata from
   UNTRUSTED_EMAIL_CONTENT;
4. source-bound envelope integrity;
5. no email-driven active retrieval or execution;
6. human approval before customer-facing send; and
7. append-oriented audit evidence.

The deterministic pattern screen is supplemental defense in depth. It can have
false positives and false negatives and does not make prompt injection
impossible. A flagged source email produces ESCALATE and no automated
customer reply DraftReply.

Provider results carry trust_class=UNTRUSTED_EMAIL_CONTENT and
instruction_authority=NONE. Instructions appearing in email have zero
authority over system, security, Skill, tool, approval, or authorization
policy. HTML scripts, styles, and comments are excluded from visible text;
links are recorded as untrusted data and never followed by this workflow.
Requests for credentials, system prompts, private employee/authentication data,
internal-only instructions, arbitrary Vault contents, or unshareable internal
commercial information are escalated rather than answered by retrieval.

For Hermes Agent v0.21.1, the native Cron scheduler supports per-job
enabled_toolsets and layers the global disabled-toolset denylist on top. A
future operator-created job may therefore bind only the governed Email MCP
surface. No production job or live binding is created in Phase 1.1.
