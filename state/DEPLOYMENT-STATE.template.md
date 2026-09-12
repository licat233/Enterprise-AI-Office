# Enterprise AI Office Deployment State

> Fresh-deployment template. Copy this file to the deployment's protected/operational storage and replace placeholders with observed runtime truth. Do **not** overwrite the repository's historical `state/DEPLOYMENT-STATE.md`. Do not copy role/capability values from another reference instance, and never commit a real operational copy when it contains company-private runtime identifiers or state.

Last updated: `<ISO_DATE>`
Company / environment: `<COMPANY> / <ENVIRONMENT>`
Requested readiness: `<core-ready | configured-ready | production-ready>`
Achieved readiness: `<CORE READY | CONFIGURED READY | PRODUCTION READY | BLOCKED | FAIL>`
Operational state path: `<protected path; recommended ${EAIO_RUNTIME_DIR}/state/deployment-state.md>`
Backup state source: `<default path or EAIO_DEPLOYMENT_STATE_FILE override>`
EAO repository origin: `<repository URL / approved local mirror>`
EAO blueprint commit: `<40-character git commit SHA>`
EAO tracked working tree at start: `clean`
EAO revision changes during this deployment: `none | <explicitly authorized restart/rebaseline>`

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
| Hermes source checkout | `<resolved installer path>` |

## Core network

Record the resolved non-secret network desired state and the observed runtime
truth. Do not copy private addresses into public status documents.

| Boundary | Desired state | Observed runtime | Acceptance |
| --- | --- | --- | --- |
| WeKnora API for Hermes/MCP | `<core_network.weknora.api_base_url_for_hermes>` | `<...>` | `<PASS/FAIL>` |
| WeKnora direct employee exposure | `false or explicitly authorized value` | `<...>` | `<PASS/FAIL>` |
| Hermes shared listener bind | `<host:port>` | `<...>` | `<PASS/FAIL>` |
| Hermes URL used by Open WebUI backend | `<core_network.hermes.open_webui_backend_base_url>` | `<...>` | `<PASS/FAIL>` |
| Hermes direct employee exposure | `false or explicitly authorized value` | `<...>` | `<PASS/FAIL>` |
| Open WebUI employee URL | `<core_network.open_webui.employee_url>` | `<...>` | `<PASS/FAIL>` |
| Open WebUI access layer | `<lan-only/private-network/approved ingress>` | `<...>` | `<PASS/FAIL>` |

## Core components

| Component | Version / commit | Deployment | Health |
| --- | --- | --- | --- |
| WeKnora | `<...>` | `<...>` | `<PASS/FAIL>` |
| Hermes Agent | `<...>` | `<...>` | `<PASS/FAIL>` |
| Open WebUI | `<...>` | `<...>` | `<PASS/FAIL>` |

Add rows only for optional components actually enabled.

## Models / providers

| Role | Source / auth path | Provider | Model | Credential ref / native binding | Notes |
| --- | --- | --- | --- | --- | --- |
| Hermes default/general | `<api-key / OAuth / keyless / ...>` | `<...>` | `<...>` | `<symbolic ref + native binding, or none>` | `<...>` |
| WeKnora embedding | `<local / remote>` | `<... or n/a>` | `<...>` | `<symbolic ref + native binding, or none>` | dimension `<...>` |
| WeKnora rerank | `<disabled / local / remote>` | `<...>` | `<...>` | `<symbolic ref + native binding, or none>` | `<...>` |

Do not record API keys/secrets here. Record only the selected non-secret auth
mechanism and symbolic credential-ref/native-binding metadata needed to rebind
the same model role after recovery.

## Knowledge

| Company logical KB ID | Runtime WeKnora KB ID | Purpose | Allowed Profiles | State |
| --- | --- | --- | --- | --- |
| `<company-general>` | `<runtime UUID>` | `<...>` | `<general>` | `<...>` |

Record the logical-ID → runtime-ID mapping generated/adopted by
`infrastructure/weknora/PROVISIONING.md`. Runtime UUIDs belong here (or in the
protected operational copy), not in generic company configuration.

Also record:

```text
WeKnora auth registration mode/bootstrap method:
WeKnora tenant/workspace runtime ID:
Embedding runtime model ID:
Embedding dimension:
Profile → retrieval-key record ID/name/scope:
Profile → retrieval-key naming source: recorded-existing | enterprise-ai-office-hermes-<profile-id>
Profile → protected retrieval-token reference name:
Official MCP server source/path/version:
```

The retrieval-token **value** remains only in protected secret storage/Profile
`.env`; the state record stores only its non-secret reference/record identity.

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
- Employee groups: `<company logical group IDs>`.
- Knowledge scope: `<company logical KB IDs + resolved runtime KB IDs>`.
- Effective tool scope: `<...>`.
- API route: `<shared gateway base>/p/general/v1`.
- Advertised model ID: `general`.
- API credential record/reference: `<non-secret identifier>`; value omitted.
- WeKnora retrieval credential record/reference: `<non-secret identifier>`; value omitted.
- Memory policy: `<disabled or validated mechanism>`.

### Hermes served-set / route handoff

```text
Shared gateway owner Profile: default
Shared listener host/port:
Effective multiplex allowlist:
Profile → API route:
Profile → advertised model ID:
Profile → API credential non-secret reference:
Profile → logical KB scope:
Profile → WeKnora runtime KB IDs:
```

This is the handoff consumed by Open WebUI provisioning. Do not copy plaintext
Profile API keys into this record.

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
| System Prompt editing | `<enabled/disabled>` |
| Advanced Parameters | `<enabled/disabled>` |
| File Upload | `<enabled/disabled>` |
| Conversation history | `<enabled/disabled>` |

### Group runtime mappings

| Company logical group ID | Display name | Open WebUI runtime UUID |
| --- | --- | --- |
| `all-employees` | `All Employees` | `<runtime UUID>` |
| `ai-admins` | `AI Administrators` | `<runtime UUID>` |

Add only groups selected by active company configuration.

### Assistant / connection runtime mappings

| Hermes Profile | Hermes API route | Advertised model ID | Open WebUI Model ID | Allowed logical groups | Runtime group UUID grants |
| --- | --- | --- | --- | --- | --- |
| `general` | `<...>/p/general/v1` | `general` | `general` | `all-employees` | `<runtime UUID>` |

Also record, without secrets:

```text
Profile → Open WebUI exact connection URL:
Profile → observed Open WebUI connection index/runtime handle:
Profile → advertised model ID → resolved Open WebUI connection URL/index:
Profile → protected Profile-API-key reference name:
EAO-managed native Open WebUI company Knowledge attachment: absent
```

The Open WebUI mapping consumes the Hermes route/model identity and company group
mapping; it must not invent a second Profile or Knowledge authority. The exact
Profile connection URL is the reconciliation identity. The Open WebUI array
index is only an observed runtime handle and must be rediscovered when the
connection list changes; never bind a Profile from a historical index alone.

## Capability closure

Copy the enabled capability set derived from the active company config and `config/capabilities.yaml`.

| Capability | Requested | Version/implementation | Acceptance | Final state |
| --- | --- | --- | --- | --- |
| Core employee path | yes | core adapters | `<PASS/FAIL>` | enabled |
| `<enabled capability>` | yes | `<playbook/version>` | `<PASS/FAIL/BLOCKED>` | `<...>` |

Disabled capabilities may be recorded compactly when useful, but do not create runtime objects for them.

## Enabled conditional capability evidence

For every company-enabled conditional capability in `config/capabilities.yaml`,
record **every** item listed by that capability's `records` block. This section
is the common evidence index for Configured Ready.

Use one block per enabled capability:

```text
Capability registry key:
Selected implementation/version/commit:
Enabled Profile(s)/group(s):
Acceptance document + section(s):
Acceptance result:
Records checklist:
  <one line/value for every item declared by config/capabilities.yaml -> records>
Dedicated protected-state section/reference:
Known limitations/blockers:
```

Rules:

- do not omit a registry `records` item because it seems repetitive;
- when a dedicated section exists (for example v2 Email Governance), keep the
  detailed evidence there and reference it from this common block;
- record non-secret credential IDs/reference names/classes only, never values;
- runtime UUIDs/IDs belong in the protected operational copy, not generic public
  company configuration;
- disabled capabilities do not need an evidence block and must not gain runtime
  objects merely to make this template look complete.

Configured Ready requires all enabled conditional capability blocks to be
complete and their acceptance results to pass.

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
Latest backup generation/timestamp:
Protected operational deployment-state artifact included: <yes/no>
Whole-generation confidentiality/encryption result:
Off-primary encrypted destination/boundary:
Latest successful off-primary copy generation/timestamp:
Checksum/integrity result:
Independent-copy freshness/retention result:
Last isolated restore source/generation (must identify off-primary copy for Production Ready):
Last isolated restore result/date:
Restored Core handoff-mapping verification:
Restored Core employee-path acceptance result:
Governance SQLite snapshot method/result when Email enabled:
Unresolved-send preservation after restore when applicable:
Secrets recovery method (non-secret description):
Known backup exclusions/limitations:
```

### Startup / recovery

```text
Startup/supervisor policy:
Service dependency/start order:
Supported startup/recovery procedure:
Last restart/reboot validation:
Hermes Profile/Gateway recovery result:
WeKnora/Open WebUI employee-path recovery result:
Enabled-capability recovery result:
Governance restart/reconciliation result when Email enabled:
Known manual recovery boundary:
```

### Security / access review

```text
Review date/owner:
Protected-secret storage/recovery boundary:
Employee versus admin access review:
Network exposure review:
Company-knowledge scope review:
Effective employee tool boundary review:
Approved exceptions/known limitations:
```

### Operations / health

```text
Operational owner:
Health-check method/cadence:
Last health result:
Backup/restore monitoring method:
Enabled-capability health ownership:
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
