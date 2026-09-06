# Deployment Reference

This document provides implementation detail for `DEPLOY.md`.

For deployment, the binding execution model is:

```text
AGENTS.md
→ DEPLOY.md
→ docs/COMPLETENESS.md
→ active company configuration
→ config/capabilities.yaml
→ implementation adapters/playbooks
→ docs/ACCEPTANCE-TESTS.md
→ deployment state
```

Do not expand the system from examples, and do not stop at the core path when the configured readiness level requires more.

## 1. Readiness model

A deployment declares one target:

```text
core-ready
configured-ready
production-ready
```

### Core Ready

The baseline employee path works:

```text
Employee
→ Open WebUI
→ General Assistant
→ Hermes `general`
→ WeKnora MCP/API
→ grounded company answer + source
```

### Configured Ready

Core Ready remains PASS and every optional capability enabled by company configuration is deployed, secured, accepted, and recorded.

### Production Ready

Configured Ready remains PASS and applicable production recovery/security/access/operations controls are implemented and accepted.

See `docs/COMPLETENESS.md` for the full contract.

## 2. First validated core target

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

The reproducibility baseline is machine-readable in `config/validated-stack.yaml`:

- WeKnora `v0.8.0`;
- Hermes Agent `v0.21.0`;
- Open WebUI `v0.11.3`.

These are tested core reference versions, not permanent requirements. Do not silently upgrade them during an ordinary deployment.

Optional components not present in the first reference demo require version-specific upstream verification when enabled.

## 3. Pre-deployment inventory

Before mutation record/inspect:

- OS/version and CPU architecture;
- RAM and free disk;
- container runtime/version;
- Git and required runtime tools;
- existing Hermes state;
- existing Enterprise AI Office runtime directories;
- protected config/secrets location;
- intended employee/admin access method.

Run `scripts/preflight.sh` first.

For an existing deployment, reconcile runtime reality with `state/DEPLOYMENT-STATE.md` before changing it.

## 4. Runtime layout

Suggested macOS reference layout:

```text
/Users/Shared/enterprise-ai-office/
├── ops/
├── runtime/
│   ├── WeKnora/
│   ├── open-webui/
│   └── optional-component-checkouts/
├── company-skills/
├── backup-work/
└── logs/
```

Hermes should use its supported upstream home convention unless the deployment has a justified alternative.

Secrets and private company values remain outside the public repository.

## 5. Resolve company target before installation

Read the active company config and `config/capabilities.yaml`.

Baseline objects:

```text
Hermes Profiles
├── default/admin
└── general

Open WebUI groups
├── All-Employees
└── AI-Admins

Knowledge
└── company-defined shared employee Knowledge Base(s)
```

Then build a capability closure table for every enabled optional capability.

Typical conditional capabilities are:

- specialist Profiles;
- hermes-webui;
- Codex/Claude Code delegation;
- Kanban;
- Cron;
- messaging;
- remote/private access;
- SSO/enterprise identity;
- employee Hermes long-term memory.

A template/playbook existing in the repository is not sufficient reason to enable it.

An enabled capability cannot be silently skipped.

## 6. WeKnora

Use the selected pinned upstream release plus `infrastructure/weknora/`.

Requirements:

- persistent database and uploaded documents;
- internal database/cache/parser services not publicly exposed;
- required model roles configured;
- only configured Knowledge Bases created;
- non-sensitive seed document ingested and retrieved before Hermes integration.

Start with upstream/default retrieval capabilities. Add reranking or alternate retrieval infrastructure only when the configured requirement or measured retrieval quality justifies it.

Embedding changes are high risk because reindexing may be required.

## 7. WeKnora → Hermes knowledge bridge

Use supported WeKnora MCP/API surfaces.

Normal business Profiles should receive only the retrieval operations needed for their allowed Knowledge Bases.

The repository's baseline Hermes templates use a read-only WeKnora MCP whitelist.

Do not give normal knowledge flows direct SQL/database coupling.

## 8. Hermes baseline

Use `infrastructure/hermes/` and the selected pinned Hermes release.

Baseline:

- default/admin retained as privileged control plane;
- `general` created from `profiles/general/SOUL.md` plus baseline config template;
- WeKnora MCP registered;
- distinct employee Profile API credential;
- least-privilege API toolset;
- employee long-term memory disabled until proven isolated;
- explicit served-Profile allowlist where supported;
- default/admin not exposed to employee client.

## 9. Specialist Profiles

When active company configuration declares an employee-facing specialist Profile:

1. start from `infrastructure/hermes/specialist.config.example.yaml` and `.env.example`;
2. select the appropriate SOUL/template or define the role cleanly;
3. define employee group mapping;
4. define Knowledge Base scope;
5. define effective tools/credentials;
6. define model/memory policy;
7. create a distinct API credential;
8. add it to the served allowlist as appropriate;
9. expose only its intended employee Assistant resource;
10. run specialist RBAC/credential/behavior acceptance.

Do not infer specialist roles from the optional templates directory.

## 10. Skills

Use company-owned shared Skills through supported external directories where practical.

A Profile receives only Skills relevant to its actual work.

Authoritative company facts belong in WeKnora rather than being duplicated into SOUL/Skill prose.

## 11. Tool least privilege

Normal employee Profiles default to no unrestricted:

- terminal;
- filesystem writes;
- Docker/system control;
- GitHub administration;
- Codex/Claude Code delegation;
- raw credentials.

Privileged technical capabilities require an explicit role, workspace, and credential boundary.

## 12. Open WebUI

Use `infrastructure/open-webui/` and a pinned/tested release.

Baseline:

- persistent data;
- deterministic initial admin provisioning;
- open signup disabled unless explicitly required;
- `All-Employees` and `AI-Admins` groups;
- server-side General Assistant connection to Hermes `general`;
- Profile API keys kept server-side;
- default/admin not exposed;
- minimal employee permissions.

Validated employee baseline:

```text
Chat                     enabled
History                  enabled
File Upload              enabled unless company policy disables it
Chat System Prompt       disabled
Advanced Chat Parameters disabled
```

Specialist groups/resources are created only from company configuration.

## 13. Core employee acceptance

Use a real ordinary employee account and Part A of `docs/ACCEPTANCE-TESTS.md`.

Backend health is not enough. Validate actual login, Assistant visibility, grounded answer/source, follow-up, history, file upload when enabled, admin non-exposure, and dangerous-tool denial.

When Part A passes, `CORE READY` may be recorded.

If target readiness is higher, continue.

## 14. Capability closure for Configured Ready

For every enabled conditional capability, follow the implementation path in `config/capabilities.yaml`.

### hermes-webui

Use `infrastructure/hermes-webui/README.md`.

Pin a compatible upstream commit/version, keep the surface administrative and narrowly exposed, and run its conditional acceptance.

### Coding delegation

Use `infrastructure/coding-agents/README.md`.

Enable only authorized technical Profiles and explicit workspaces. Validate Codex/Claude Code in disposable/harmless repositories before real work.

### Kanban / Cron / messaging

Use `infrastructure/hermes/features/README.md` and the selected Hermes release's native features.

Do not add another workflow/scheduler/messaging framework when Hermes' native capability satisfies the requirement.

### Remote/private access and SSO

Use `infrastructure/access/README.md`.

The company must select/authorize the external access method or identity provider. Do not invent enterprise credentials or public exposure policy.

### Employee long-term memory

Use `docs/CLIENT-RBAC.md` / `docs/PROFILE-STANDARD.md`. Enable only after exact deployed user scoping passes isolation tests.

When all enabled Part B capabilities pass and state is recorded, `CONFIGURED READY` may be declared.

## 15. External input/blocker behavior

Some complete deployments necessarily depend on external authority:

- IdP/OIDC application registration;
- enterprise messaging application/bot credentials;
- private-access account/tunnel approval;
- model-provider credentials;
- approved repository/workspace paths;
- OS permissions requiring human approval.

When such input is required and unavailable, report exactly:

```text
BLOCKED — REQUIRED INPUT: <specific item>
```

Do not silently disable the requested capability and do not replace it with an unrelated provider.

## 16. Network posture

Conceptual trust path:

```text
Employee → Open WebUI
Open WebUI → authorized Hermes employee Profile API
Hermes → WeKnora MCP/API
AI Admin → protected admin surfaces
```

Keep PostgreSQL, Redis, parser workers, secret stores, and privileged raw routes private.

Remote access must use the configured approved boundary rather than public exposure by convenience.

## 17. Production Ready closure

When `deployment.target_readiness: production-ready`, continue after Configured Ready.

Implement/verify applicable production controls using:

- `docs/BACKUP-RESTORE.md`;
- `docs/SECURITY.md`;
- `docs/OPERATIONS.md`;
- `scripts/backup.sh`;
- `scripts/restore.sh`;
- `scripts/health-check.sh`;
- Part C of `docs/ACCEPTANCE-TESTS.md`.

Production closure includes the configured backup/restore strategy, isolated restore evidence, startup/recovery policy, secrets/access review, representative company knowledge/security testing, and operational ownership.

Do not equate container/service startup with Production Ready.

## 18. Deployment state

For a fresh deployment, start from `state/DEPLOYMENT-STATE.template.md` when available rather than copying the MacBook reference instance.

Record actual runtime truth:

- requested/achieved readiness;
- host/runtime;
- exact component versions;
- model/provider roles;
- Knowledge Bases;
- Profiles;
- groups/Assistant mappings;
- capability closure table;
- memory state;
- network/access boundary;
- production recovery controls where applicable;
- acceptance results;
- known limitations.

For an existing deployment, update its existing deployment state rather than replacing history with a template.

## 19. Dry-run planning

A dry run should resolve without host mutation:

```text
host
→ requested readiness
→ core versions/runtime
→ company Knowledge Bases
→ Profiles/groups
→ enabled capability closure
→ required protected inputs
→ implementation playbooks
→ acceptance evidence required
→ final state/report format
```

If the plan still contains routine questions such as “should I configure the enabled messaging capability?” the repository/configuration has not been followed correctly.

## 20. Final statuses

```text
CORE READY
CONFIGURED READY
PRODUCTION READY
BLOCKED — REQUIRED INPUT: <specific input>
FAIL — <specific failed boundary>
```

Use the highest status actually supported by evidence and never silently downgrade a configured target.
