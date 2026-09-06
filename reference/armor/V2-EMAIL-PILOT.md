# ARMOR v2 Email Pilot

Status: design-stage reference / provider selected / runtime not authorized
Date: 2026-09-06

This file records the sanitized ARMOR-specific design decision for the first Enterprise AI Office v2 communication pilot.

It is reference material, not a credential store, not an active deployment record, and not a universal deployment default.

## Selected provider

```text
Tencent Enterprise Mail (腾讯企业邮箱)
```

Generic provider design/playbook material:

```text
infrastructure/email/tencent-exmail/
```

## Candidate pilot mailbox

The concrete pilot mailbox identifier is intentionally **not stored in this public repository**.

The actual mailbox address belongs only in ARMOR's private deployment configuration or another approved private secret/configuration store when implementation is explicitly authorized.

Public repository rule:

```text
real employee/personal mailbox identifiers → private configuration only
public examples/tests                    → synthetic addresses only
```

Do not add a real ARMOR mailbox address to public documentation, examples, tests, fixtures, issues, or commit messages.

## Stage 1 design scope

The frozen future read-only stage is:

```text
allowed folder: INBOX initially
operations: search_email, get_email
attachments: filenames only; no attachment download
mailbox mutation: none
SMTP/send: absent from Stage 1
bulk mailbox ingestion into WeKnora: not allowed by default
```

The repository contains a candidate read-only adapter and deterministic tests to validate that this design is implementable. They are design-support prototypes, not active runtime configuration.

## Current design-support artifacts

```text
provider research/playbook
read-only MCP prototype
environment template
Hermes MCP registration example
deterministic read-only tests
provider-specific acceptance contract
email Ontology design fixture
capability-registry closure
```

These artifacts reduce future implementation uncertainty. They do **not** create a current requirement for mailbox authorization.

## Deferred implementation inputs

Only when ARMOR explicitly opens the future implementation/deployment gate will the runtime need to resolve privately:

```text
pilot mailbox identifier
mailbox-specific client credential / client-specific password
selected IMAP endpoint for the real deployment network
authorized human user/group scope
authorized Hermes Profile
protected secret location
actual runtime host access
harmless known acceptance-test message(s)
```

Until then, these are deferred inputs rather than blockers.

Do not place credentials, personal mailbox identifiers, or other private employee contact data in this repository, a Profile SOUL/Skill, shell history, logs, issue comments, or public chat transcripts.

## Future implementation sequence

When implementation is explicitly authorized later:

```text
Stage 0  preserve/verify v1 baseline
Stage 1  bounded read-only email
Stage 2  DraftReply preparation
Stage 3  trusted human approval
Stage 4  send_approved_reply
```

Customer-facing send remains human-governed and later than the read-only stage.

No autonomous customer-facing send is authorized by this design record.
