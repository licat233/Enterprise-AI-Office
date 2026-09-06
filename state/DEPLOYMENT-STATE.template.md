# Enterprise AI Office Deployment State

> Fresh-deployment template. Copy to the deployment's protected/operational state record and replace placeholders with observed runtime truth. Do not copy role/capability values from another reference instance.

Last updated: `<ISO_DATE>`
Company / environment: `<COMPANY> / <ENVIRONMENT>`
Requested readiness: `<core-ready | configured-ready | production-ready>`
Achieved readiness: `<CORE READY | CONFIGURED READY | PRODUCTION READY | BLOCKED | FAIL>`

## Host

| Field | Value |
| --- | --- |
| Host type | `<...>` |
| OS/version | `<...>` |
| Architecture | `<...>` |
| RAM | `<...>` |
| Storage/free space | `<...>` |
| Container runtime/version | `<...>` |
| Runtime root | `<...>` |

## Core components

| Component | Version / commit | Deployment | Health |
| --- | --- | --- | --- |
| WeKnora | `<...>` | `<...>` | `<PASS/FAIL>` |
| Hermes Agent | `<...>` | `<...>` | `<PASS/FAIL>` |
| Open WebUI | `<...>` | `<...>` | `<PASS/FAIL>` |

Add rows only for optional components actually enabled.

## Models / providers

| Role | Provider | Model | Notes |
| --- | --- | --- | --- |
| Hermes default/general | `<...>` | `<...>` | `<...>` |
| WeKnora embedding | `<...>` | `<...>` | dimension `<...>` |
| WeKnora rerank | `<disabled or ...>` | `<...>` | `<...>` |

Do not record API keys/secrets here.

## Knowledge

| Knowledge Base | Purpose | Allowed groups/Profiles | State |
| --- | --- | --- | --- |
| `<configured KB>` | `<...>` | `<...>` | `<...>` |

Document source/corpus location at a non-secret level where operationally useful.

## Hermes Profiles

### default / admin

- Purpose: privileged control plane.
- Employee exposed: `false`.
- Model/provider: `<...>`.
- Served/API state: `<...>`.
- Privileged capability boundary: `<...>`.

### general

- Purpose: baseline employee Assistant.
- Employee groups: `<...>`.
- Knowledge scope: `<...>`.
- Effective tool scope: `<...>`.
- API credential: distinct/protected; value omitted.
- Memory policy: `<disabled or validated mechanism>`.

### Enabled specialist Profiles

For each configured specialist Profile record:

```text
Profile:
Purpose:
Employee groups:
Knowledge scope:
Tools/capabilities:
Model/provider:
API credential boundary:
Memory policy:
Acceptance result:
```

Do not add template Profiles that were not enabled.

## Open WebUI

| Field | Value |
| --- | --- |
| Employee URL/access method | `<...>` |
| Authentication | `<local / SSO / ...>` |
| Signup policy | `<...>` |
| Baseline groups | `<...>` |
| Assistant mappings | `<...>` |
| System Prompt editing | `<enabled/disabled>` |
| Advanced Parameters | `<enabled/disabled>` |
| File Upload | `<enabled/disabled>` |
| Conversation history | `<enabled/disabled>` |

## Capability closure

Copy the enabled capability set derived from the active company config and `config/capabilities.yaml`.

| Capability | Requested | Version/implementation | Acceptance | Final state |
| --- | --- | --- | --- | --- |
| Core employee path | yes | core adapters | `<PASS/FAIL>` | enabled |
| `<enabled capability>` | yes | `<playbook/version>` | `<PASS/FAIL/BLOCKED>` | `<...>` |

Disabled capabilities may be recorded compactly when useful, but do not create runtime objects for them.

## v2 Email Governance

Complete only when the Email capability is enabled.

```text
Provider:
Governance service version/contract:
Governance state path:
Governance schema version:
Communication Assistant ID:
Email Governance tool connection ID:
Logical group → Open WebUI runtime group mappings:
Mailbox grant summary:
Provider endpoint mode:
Provider/forwarder secret reference classes (names only, never values):
Stage 0 result:
Stage 1 result:
Stage 2 result:
Stage 3 result:
Stage 4 result:
Current unresolved reconciliation count/status:
Latest Governance backup generation:
Governance snapshot included in backup: <yes/no>
Last isolated Governance restore result:
Installer second-run convergence result:
v2 rollback/degrade + v1 preservation result:
Known Email limitations:
```

Do not record Draft bodies, mailbox passwords, forwarder tokens, provider credentials, or full provider logs here.

## Administrative surfaces

Record only those actually enabled:

```text
hermes-webui: <disabled or URL/access/version>
WeKnora admin: <access boundary>
Open WebUI admin: <access boundary>
Host/Docker/Hermes CLI: <operator boundary>
```

## Coding delegation

If enabled:

```text
Allowed Profiles:
Enabled backends:
Codex version/auth boundary:
Claude Code version/auth boundary:
Allowed workspaces/repositories:
Acceptance result:
```

Otherwise: `disabled`.

## Kanban

If enabled:

```text
Boards:
Orchestrator/worker Profiles:
Workspace policy:
Dispatcher state:
Acceptance result:
```

Otherwise: `disabled`.

## Cron

If enabled:

```text
Owner Profiles:
Model/provider policy:
Business-critical jobs:
Delivery targets:
Acceptance result:
```

Otherwise: `disabled`.

## Messaging

If enabled:

```text
Platform:
Authorization method:
Profile routing:
Delivery targets:
Acceptance result:
```

Otherwise: `disabled`.

## Remote access / SSO

If enabled:

```text
Remote access method:
Employee surfaces:
Admin surfaces:
Identity provider:
Group/claim mapping policy:
Acceptance result:
```

Otherwise record each as `disabled` independently.

## Memory

```text
Employee Hermes long-term memory: <disabled/enabled>
User-scoping mechanism: <N/A or verified mechanism>
Cross-user isolation: <N/A/PASS/FAIL>
Cross-Profile isolation: <N/A/PASS/FAIL>
Open WebUI conversation history: <enabled/disabled>
```

## Network exposure

```text
Open WebUI: <...>
Hermes employee API: <...>
WeKnora UI/API: <...>
Email Governance: <disabled/private loopback-or-private-network/...>
hermes-webui: <disabled/...>
PostgreSQL: <internal only/...>
Redis: <internal only/...>
Other enabled surfaces: <...>
```

## Production controls

Complete when `production-ready` is requested.

### Backup / restore

```text
Schedule:
Retention:
Off-primary-disk destination/boundary:
Last successful backup:
Last isolated restore test:
Governance SQLite snapshot method/result when Email enabled:
Unresolved-send preservation after restore when applicable:
Secrets recovery method (non-secret description):
```

### Startup / recovery

```text
Policy:
Supported startup/recovery procedure:
Last validation:
Governance restart/reconciliation result when Email enabled:
Known manual boundary:
```

### Operations / health

```text
Operational owner:
Health-check method:
Review cadence:
Known alerts/limitations:
```

## Acceptance summary

```text
Core Ready: <PASS/FAIL>
Configured capability closure: <PASS/FAIL/BLOCKED/N/A>
Production controls: <PASS/FAIL/BLOCKED/N/A>
```

## Known issues / limitations

- `<only real current limitations>`

## Final status

```text
<CORE READY | CONFIGURED READY | PRODUCTION READY | BLOCKED — REQUIRED INPUT: ... | FAIL — ...>
```

Never record a readiness level higher than the evidence supports.
