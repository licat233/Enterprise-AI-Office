# Deployment Blueprint

This document defines the generic deployment sequence for Enterprise AI Office. It is an execution blueprint, not a claim that every adopting company has identical hardware or credentials.

## 1. Deployment objective

A deployment is complete only when the full path works:

```text
Employee
→ approved client
→ authorized Hermes Profile
→ company knowledge / tools
→ response or task execution
```

and the system is recoverable after failure/reboot.

## 2. Reference host model

Initial reference deployment:

```text
Company-owned host
│
├── Host-native
│   ├── Hermes Agent
│   ├── Codex
│   └── Claude Code
│
└── Containers
    ├── WeKnora
    └── Open WebUI
```

The first ARMOR deployment targets a Mac Studio. Other companies may use another supported host. Preserve component responsibilities even when the host changes.

## 3. Pre-deployment inventory

Before installing anything, record:

- OS and version;
- CPU architecture;
- RAM;
- total/free disk;
- hostname;
- LAN address strategy;
- Docker/container runtime and version;
- Git;
- Python;
- Node.js if needed;
- existing Hermes installation;
- existing Codex installation/authentication;
- existing Claude Code installation/authentication;
- backup destination;
- intended employee access method;
- intended enterprise messaging platform, if any.

Do not create duplicate runtimes or accounts before inspecting what already exists.

## 4. Operations repository checkout

Clone this repository to a stable administrative location.

Recommended pattern:

```text
/Users/Shared/enterprise-ai-office/ops/Enterprise-AI-Office
```

on macOS, or an equivalent administrative path on Linux.

Company-specific runtime data should not be committed to this public repository.

## 5. Runtime directory pattern

Suggested macOS reference layout:

```text
/Users/Shared/enterprise-ai-office/
├── ops/
├── runtime/
│   ├── WeKnora/
│   ├── open-webui/
│   └── hermes-webui/
├── company-skills/
├── backup-work/
└── logs/
```

Hermes should continue to use its upstream home convention (`~/.hermes`) unless a real deployment reason requires otherwise.

## 6. Version selection

For WeKnora, Hermes Agent, Open WebUI, and hermes-webui:

1. identify the current stable upstream release;
2. read release notes;
3. inspect breaking changes/security notes;
4. choose a tested exact version/tag/commit;
5. record it in `state/DEPLOYMENT-STATE.md`.

Do not build production around an unreviewed floating `main` or `latest` reference.

## 7. WeKnora deployment

Use the upstream standard production-oriented deployment, normally Docker Compose for the reference implementation.

Expected core responsibilities include:

- WeKnora application/frontend;
- document parser/DocReader;
- PostgreSQL-based storage/retrieval stack;
- Redis/task infrastructure where required by the selected upstream release;
- persistent uploaded-file storage.

### WeKnora rules

- Use strong generated secrets.
- Do not publish PostgreSQL or Redis to the public network.
- Persist database and uploaded files.
- Use the official/default retrieval stack first.
- Do not add Qdrant/Milvus/Weaviate merely because they are available.
- Start with a small high-quality pilot corpus.

### Initial Knowledge Bases

A generic starting point may be:

```text
Company & Brand
Products & Technical
Sales & Marketing
Operations & SOP
```

Adopting companies should change these to match their real semantic and permission boundaries.

## 8. WeKnora model configuration

Configure the required model roles for the selected upstream release, typically:

- embedding;
- reranking;
- chat/reasoning if used inside WeKnora;
- VLM/parser model only when needed.

Record exact model IDs and embedding dimensions in deployment state.

Changing the embedding model later is a high-risk operation because it may require reindexing.

## 9. WeKnora MCP/API bridge

Prefer supported WeKnora MCP/API surfaces for Hermes integration.

Validate the currently supported MCP tool inventory. At minimum verify the tools needed for:

- listing visible Knowledge Bases;
- searching chunks/documents;
- viewing source documents/chunks.

Do not give Hermes direct SQL access to the WeKnora database for normal retrieval.

## 10. Hermes installation

Install or update Hermes Agent using the currently supported upstream method.

Reference posture: host-native.

Configure:

- model/provider;
- API server;
- Gateway;
- Profiles;
- MCP;
- Skills;
- toolsets;
- credentials;
- Cron/Kanban only as required.

## 11. Hermes Profile creation

Do not create a large Profile fleet before real roles exist.

A reference company may start with:

```text
default / admin-orchestrator
general
sales
qc
marketing
engineering
```

Company-specific deployments may use a different role set.

For each Profile, define:

- purpose;
- SOUL;
- allowed Skills;
- allowed tools/toolsets;
- WeKnora access;
- model/provider;
- credentials;
- terminal/workspace policy;
- memory policy;
- Cron policy.

## 12. Hermes multi-Profile Gateway

If the selected Hermes release supports and the deployment benefits from it, enable the supported multi-Profile/multiplex Gateway mechanism.

Use an explicit Profile allowlist where available. Do not automatically serve every experimental Profile installed on the host.

Each employee-facing Profile must have a distinct API credential.

Validation requirement:

```text
general key → general PASS
general key → sales FAIL
sales key   → sales PASS
sales key   → qc FAIL
```

The privileged administrative/default Profile must not be exposed as a normal employee assistant.

## 13. Skills layout

Use Hermes upstream Skills plus company-owned Skills.

Prefer shared external Skill directories instead of copying the same Skill into every Profile.

Example:

```text
company-skills/
├── shared/
├── sales/
├── qc/
├── marketing/
└── engineering/
```

Each Profile loads only the shared and role-specific directories it needs.

## 14. Tool least privilege

Before employee access is enabled, explicitly review each Profile's tools.

Default business Profiles should not have unrestricted:

- terminal;
- filesystem write;
- Docker;
- system settings;
- GitHub administration;
- coding-agent delegation.

An Engineering Profile may have stronger tools only with deliberate workspace and credential boundaries.

## 15. Open WebUI deployment

Deploy Open WebUI independently from WeKnora so the two upstream projects can be upgraded and rolled back separately.

Use a tested pinned release.

Configure:

- first admin account;
- authentication policy;
- default user permissions;
- employee groups;
- Hermes Profile connections/resources;
- resource ACLs.

## 16. Open WebUI group model

A typical starting set:

```text
All-Employees
Sales
QC
Marketing
Engineering
Management
AI-Admins
```

Global defaults should be minimal. Permissions are granted through groups.

## 17. Hermes connections in Open WebUI

Create one server-side OpenAI-compatible connection/resource per employee-facing Hermes Profile using the currently supported Profile API route.

Do not expose Profile API keys to browsers or users.

For multi-user memory scoping, configure the supported Hermes session-key header using Open WebUI dynamic user variables where compatible.

Example conceptual mapping:

```text
sales:webui:<USER_ID>
qc:webui:<USER_ID>
marketing:webui:<USER_ID>
```

Exact header syntax must be validated against the currently installed upstream versions.

## 18. Memory isolation gate

Before enabling employee long-term memory, execute the cross-user test in `ACCEPTANCE-TESTS.md`.

If User B can recover private memory entered by User A through the same department Profile, long-term employee memory must be disabled until the isolation mechanism is corrected.

Do not solve a memory-isolation failure with prompt instructions alone.

## 19. hermes-webui deployment

Deploy hermes-webui only as an administrative control surface.

It may expose Profile configuration, Skills, MCP, memory, Cron, Kanban, providers, and other machine-level settings.

Restrict access to AI administrators/authorized maintainers.

## 20. Codex and Claude Code integration

Verify host-native Codex and Claude Code independently first.

Then verify Hermes can delegate coding work through the currently supported mechanisms.

Test only in a disposable/test repository before granting access to a production repository.

When entering a real repository, the coding worker must read repository-local instructions such as `AGENTS.md`, `CLAUDE.md`, and project documentation.

## 21. Kanban initialization

Initialize Kanban only when durable multi-agent work is needed.

Test:

- create task;
- assign Profile;
- dispatcher pickup;
- worker execution;
- comment/review;
- completion;
- persistence after Gateway restart.

Do not treat Kanban as an employee-wide project management system unless its access model has been separately designed.

## 22. Cron initialization

Create a harmless temporary scheduled job.

Verify:

- schedule;
- execution;
- history;
- pause/resume;
- delivery;
- persistence across Gateway restart.

Remove the test job afterward.

## 23. Messaging integration

Enable only the enterprise messaging platform the company actually uses.

Configure:

- platform app/bot credentials;
- allowlist/pairing/enterprise identity;
- approved chats/users;
- Profile routing;
- file/media behavior if needed;
- Cron delivery if needed.

If no platform is selected yet, leave messaging disabled. It is not a blocker for Web v1.

## 24. Network posture

Default:

```text
Employee → Open WebUI
Knowledge Maintainer → WeKnora UI
AI Admin → hermes-webui / admin tools
Open WebUI → internal Hermes API
Hermes → internal WeKnora MCP/API
```

Do not expose PostgreSQL, Redis, DocReader, or raw Hermes administrative endpoints publicly.

## 25. Backup before production

Implement backup according to `BACKUP-RESTORE.md` before production access.

At minimum back up:

- WeKnora database;
- WeKnora uploaded files;
- Open WebUI persistent state;
- Hermes home/Profiles;
- company Skills/configuration;
- encrypted secrets separately;
- this operations repository.

Perform one real restore test before declaring production ready.

## 26. Reboot test

Restart the host.

Verify required services recover automatically or according to documented startup procedures:

- Docker runtime;
- WeKnora;
- Open WebUI;
- Hermes Gateway;
- Profiles;
- MCP bridge;
- Cron/Kanban state.

A system that only works until the next reboot is not deployed.

## 27. Final acceptance

Run all checks in `docs/ACCEPTANCE-TESTS.md`.

Only then mark the deployment Production Ready in `state/DEPLOYMENT-STATE.md`.

## 28. Company-specific overlay

Do not edit generic architecture merely to encode one company's private details.

Store private deployment values in the adopting company's private configuration/ops layer and use `reference/` in this public project only for sanitized examples.
