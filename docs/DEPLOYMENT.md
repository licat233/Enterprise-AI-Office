# Deployment Reference

This document provides implementation detail for the execution contract in `DEPLOY.md`.

For deployment tasks, follow `DEPLOY.md` first. This document may explain how a phase is implemented, but it must not expand the baseline deployment by treating optional examples as required components.

## 1. Deployment objective

The baseline deployment is complete at `CORE READY` only when this path works from the real employee client:

```text
Employee
→ Open WebUI
→ General Assistant
→ Hermes `general` Profile
→ WeKnora MCP/API
→ grounded company answer + source
```

`PRODUCTION READY` is a separate, higher standard defined in `DEPLOY.md` and the operational/security documents.

## 2. First validated target

The first validated reference path is:

```text
Apple Silicon macOS
│
├── Host-native
│   └── Hermes Agent
│
└── OrbStack / Docker
    ├── WeKnora
    └── Open WebUI
```

Validated versions are recorded in `state/DEPLOYMENT-STATE.md`. The initial reproducibility baseline is:

- WeKnora `v0.8.0`;
- Hermes Agent `v0.21.0`;
- Open WebUI `v0.11.3`.

These are tested reference versions, not permanent requirements. Do not silently upgrade them during an ordinary deployment.

## 3. Pre-deployment inventory

Before installing or changing anything, record:

- OS/version and CPU architecture;
- RAM and free disk;
- container runtime/version;
- Git and required runtime tools;
- existing Hermes installation/state;
- existing Enterprise AI Office runtime directories;
- intended employee access method;
- protected secrets/configuration location.

Run `scripts/preflight.sh` as a read-only first step.

If an existing deployment is present, reconcile it with `state/DEPLOYMENT-STATE.md` before mutation.

## 4. Runtime layout

Suggested macOS reference layout:

```text
/Users/Shared/enterprise-ai-office/
├── ops/
├── runtime/
│   ├── WeKnora/
│   └── open-webui/
├── company-skills/
├── backup-work/
└── logs/
```

Hermes should use its supported upstream home convention unless a real deployment reason requires otherwise.

Company-private values and secrets must remain outside this public repository.

## 5. Company configuration

Resolve target state from the adopting company's configuration before creating runtime objects.

Baseline objects are:

```text
Hermes Profiles
├── default/admin     # control plane; not employee exposed
└── general           # baseline employee assistant

Open WebUI groups
├── All-Employees
└── AI-Admins

Knowledge
└── company-defined shared employee Knowledge Base(s)
```

Specialist Profiles, department groups, additional Knowledge Bases, Skills, tools, credentials, automation, and integrations are opt-in.

A template present in this repository is not sufficient reason to instantiate it.

## 6. WeKnora deployment

Use the pinned upstream release plus the smallest validated Enterprise AI Office adapter.

Requirements:

- persist the database and uploaded documents;
- keep PostgreSQL/Redis/internal parser services off public interfaces;
- configure the required model roles;
- create only Knowledge Bases declared by company configuration;
- use a small non-sensitive seed document to prove ingestion and retrieval before integrating Hermes.

Start with the upstream/default retrieval stack. Add reranking or alternate retrieval infrastructure only when measured retrieval quality justifies it.

Changing the embedding model later is a high-risk operation because reindexing may be required.

## 7. WeKnora → Hermes bridge

Use supported WeKnora MCP/API surfaces.

The baseline employee Profile needs read-only knowledge operations sufficient to:

- discover or address its allowed Knowledge Base(s);
- retrieve relevant chunks/documents;
- expose human-readable source evidence.

Do not give normal retrieval flows direct SQL access to WeKnora's database.

Scope credentials to the Knowledge Bases and retrieval actions the Profile actually needs.

## 8. Hermes deployment

Use the pinned/tested Hermes release and supported upstream installation method.

On the validated macOS path, Hermes is host-native.

Baseline configuration:

- privileged `default` / admin Profile retained as control plane;
- `general` employee Profile created from `profiles/general/SOUL.md`;
- WeKnora MCP/API registered for `general`;
- least-privilege retrieval tools for `general`;
- distinct employee Profile API credential;
- employee long-term memory disabled until isolation is proven;
- explicit served-Profile allowlist where supported.

Do not expose the default/admin Profile as an employee model.

For every specialist Profile requested by company configuration, define its purpose, SOUL, Knowledge Base access, tools, credentials, model policy, memory policy, and client group mapping, then run role-specific acceptance.

## 9. Skills

Load company-owned shared Skills through supported external Skill directories where practical.

A Profile should receive only the shared and role-specific Skills it needs.

Do not duplicate authoritative company facts into SOUL or Skill text when they belong in WeKnora.

## 10. Tool least privilege

Normal employee Profiles default to no unrestricted:

- terminal;
- filesystem writes;
- Docker control;
- host configuration;
- GitHub administration;
- Codex / Claude Code delegation;
- raw credential access.

Stronger tools are enabled only for roles whose work requires them and only with explicit workspace/credential boundaries.

## 11. Open WebUI deployment

Deploy Open WebUI independently with persistent state and a pinned/tested version.

Baseline configuration:

- provision the administrator;
- disable open self-signup after provisioning unless company policy requires it;
- create `All-Employees` and `AI-Admins`;
- create a server-side General Assistant connection to Hermes `general`;
- keep Profile API keys server-side;
- do not expose default/admin as an employee assistant;
- set ordinary employee permissions to minimal enterprise defaults.

Validated ordinary employee settings:

```text
Chat                     enabled
History                  enabled
File Upload              enabled unless company policy disables it
Chat System Prompt       disabled
Advanced Chat Parameters disabled
```

Build specialist groups and assistant resources only from company configuration.

## 12. Employee-client acceptance

Backend health alone is not sufficient.

Using a real ordinary employee account, verify:

- login succeeds;
- only permitted assistants are visible;
- General Assistant can chat normally;
- a company-knowledge question produces a grounded answer;
- source evidence is visible;
- follow-up context works;
- history survives refresh/re-login;
- file upload works when enabled;
- admin/default resources are absent;
- unapproved terminal/system tools are absent;
- unauthorized direct access fails closed.

Record the result in `state/DEPLOYMENT-STATE.md`.

## 13. Optional specialist Profiles

Create a specialist Profile only when the company configuration defines a real specialist role or boundary.

For each enabled specialist Profile, validate:

- group → Assistant → Profile mapping;
- distinct API credential;
- Knowledge Base scope;
- least-privilege tools;
- cross-Profile/direct unauthorized denial;
- role-specific behavior.

Do not infer organization structure from the optional templates under `profiles/`.

## 14. Optional capabilities

The following are extensions, not Core Ready requirements unless explicitly enabled by company configuration:

- hermes-webui;
- Codex / Claude Code delegation;
- Kanban;
- Cron;
- enterprise messaging;
- remote browser access;
- employee Hermes long-term memory;
- SSO/enterprise identity integration.

When enabled, use their dedicated documentation and acceptance tests.

## 15. Network posture

Baseline trust path:

```text
Employee → Open WebUI
Open WebUI → Hermes employee Profile API
Hermes → WeKnora MCP/API
AI Admin → protected administrative surfaces
```

Do not publicly expose PostgreSQL, Redis, parser/internal services, raw credentials, or privileged Hermes administrative routes.

Remote employee access requires a separately approved private/identity-aware access design.

## 16. Backup, restore, and reboot

These are production-readiness concerns unless the requested task explicitly includes them.

Before a real production rollout, implement and validate the controls required by:

- `docs/BACKUP-RESTORE.md`;
- `docs/SECURITY.md`;
- `docs/OPERATIONS.md`.

Do not claim `PRODUCTION READY` without the relevant recovery and operational controls.

A bounded functional/demo deployment may reach `CORE READY` without pretending those production controls were validated.

## 17. Deployment state

Every real deployment must record actual runtime truth, including:

- host/runtime;
- exact component versions;
- model/provider roles;
- enabled Knowledge Bases;
- enabled Profiles;
- employee groups/assistant mappings;
- memory state;
- network exposure;
- enabled optional capabilities;
- acceptance status;
- known limitations.

Use `state/DEPLOYMENT-STATE.md` as the runtime record, not as a source of universal defaults.

## 18. Dry-run planning

A dry-run deployability review should resolve:

```text
host
→ exact versions
→ runtime paths
→ company Knowledge Bases
→ Profiles/groups
→ credentials required
→ WeKnora deployment
→ Hermes integration
→ Open WebUI RBAC
→ employee acceptance
→ deployment-state output
```

It should identify only genuine missing human inputs and should not mutate the host.

## 19. Final statuses

Use the execution statuses defined in `DEPLOY.md`:

```text
CORE READY
BLOCKED — REQUIRED INPUT
FAIL — <specific failed boundary>
```

Use `PRODUCTION READY` only after the additional production controls relevant to that deployment are validated.
