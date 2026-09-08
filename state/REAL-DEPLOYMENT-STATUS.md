# Real Deployment Status — Sanitized Public Summary

> This file is a **sanitized public progress summary** for the explicitly authorized real company deployment. It is not the protected runtime state record and must never contain credentials, real employee identifiers, private network details, mailbox data, or secret values.

Last updated: 2026-09-08

## Deployment authorization

```text
Real deployment task: ACTIVE
Target: designated company Mac Studio (publicly sanitized)
Requested readiness: production-ready
Blueprint lifecycle: installation_design (unchanged)
Blueprint Validation: not opened
```

The real deployment is an independently authorized consumer activity. Its activation does **not** advance the repository blueprint lifecycle.

## Operator topology

```text
Operator Mac
  ↓
Codex macOS App
  ↓ SSH
Designated company Mac Studio
  ↓
Enterprise AI Office runtime
```

Deployment commands execute on the remote Mac Studio unless a task explicitly says otherwise. A local Codex/ChatGPT login on the Mac Studio is not required for the deployment path.

## Current deployment stage

Current achieved readiness:

```text
CORE READY — PASS
CONFIGURED READY — PASS
PRODUCTION READY — BLOCKED BY EXTERNAL BACKUP / RESTORE INPUT
```

Validated employee path:

```text
Employee
→ Open WebUI
→ General Assistant
→ Hermes `general`
→ WeKnora `Company Knowledge`
→ grounded company answer + source
```

The active company configuration currently enables only the Core employee path. No optional capability is enabled, so Configured Ready is satisfied once Core Ready passes and the configured capability closure remains empty.

Current public status:

| Area | Status |
| --- | --- |
| Remote host preflight | ✅ Complete |
| OrbStack / Docker | ✅ Running |
| WeKnora v0.8.0 | ✅ Running |
| Hermes v0.21.0 | ✅ Running |
| Hermes `general` | ✅ Configured |
| Hermes reasoning model | ✅ `gpt-5.6-luna` |
| Hermes employee long-term memory | ✅ Disabled |
| Hermes network bind | ✅ Loopback-only baseline |
| Open WebUI v0.11.3 | ✅ Running |
| Open WebUI admin bootstrap | ✅ Complete |
| Signup | ✅ Disabled |
| Employee groups / baseline ACL | ✅ Reconciled |
| General Assistant | ✅ Configured |
| Employee model isolation | ✅ Baseline checks passed |
| System Prompt editing | ✅ Disabled for ordinary employee |
| Advanced Parameters editing | ✅ Disabled for ordinary employee |
| Conversation history | ✅ Persists across refresh and re-login |
| File upload | ✅ Accepted and source reference visible |
| Unknown-company-fact behavior | ✅ Unavailable / no fabrication observed |
| WeKnora Owner/Admin bootstrap | ✅ Complete |
| Local Embedding | ✅ `bge-m3` / 1024 dimensions |
| Formal `Company Knowledge` | ✅ Created and bound to `bge-m3` |
| Seed ingestion / retrieval | ✅ Marker and source filename returned |
| `general` WeKnora credential | ✅ Retrieve-only / `full_access=false` |
| Knowledge write-denial check | ✅ HTTP 403 |
| Hermes → WeKnora MCP | ✅ Grounded marker/source returned |
| Core service health | ✅ WeKnora / Open WebUI / Hermes / Ollama healthy |
| Core Ready | ✅ PASS |
| Configured Ready | ✅ PASS |
| Independent encrypted backup target | ⏳ Not yet provided |
| Off-primary backup generation/copy | ⏳ Pending backup target |
| Isolated restore evidence | ⏳ Pending backup target |
| Production Ready | ⛔ BLOCKED — backup / restore closure |

Readiness remains evidence-based under [`docs/COMPLETENESS.md`](../docs/COMPLETENESS.md).

## Current model configuration

Reasoning / answer generation:

```text
Hermes
→ gpt-5.6-luna
```

Knowledge retrieval / embedding:

```text
WeKnora v0.8.0
→ local Ollama
→ bge-m3
→ 1024 dimensions
```

The current Core deployment does **not** require a separate WeKnora Chat/KnowledgeQA model.

Current WeKnora model-role posture:

```text
Embedding        enabled: bge-m3 / 1024
KnowledgeQA/Chat not required for Core
Rerank           disabled
VLLM             disabled
ASR              disabled in WeKnora Core
```

DashScope is not required for the selected local embedding path.

## Local embedding qualification evidence

Before formal binding, the current Mac Studio deployment qualified `bge-m3` with a small representative test:

- 6 sanitized representative documents parsed successfully;
- 8 mixed Chinese / English / cross-language retrieval questions returned relevant source evidence;
- observed Ollama RSS was approximately 1.75 GB;
- available-memory ratio remained approximately 68–71% on the deployment host;
- WeKnora and Open WebUI remained healthy;
- no obvious system slowdown was observed;
- `qwen3-embedding:0.6b` was not tested because `bge-m3` already passed the intended minimal qualification.

The temporary test Knowledge Base was removed after formal provisioning; the `bge-m3` model remains installed for production use.

## Core access and knowledge boundary

The employee-facing Hermes `general` path uses a dedicated WeKnora retrieve-only credential:

```text
Knowledge scope: Company Knowledge only
full_access: false
write attempt: denied (HTTP 403)
```

The ordinary employee surface does not expose Hermes `default/admin`.

The Core path is intentionally fail-closed for company facts that are not supported by approved knowledge.

## Production Ready blocker

The active target remains `production-ready`, but Production Ready is intentionally not declared yet.

The unresolved production boundary is backup / restore resilience, not the AI employee path itself.

Current external-input blocker:

```text
No approved physically independent encrypted backup destination has been provided yet.
```

Consequences:

- a complete backup generation cannot yet be copied off the Mac Studio primary disk;
- isolated restore evidence cannot yet be completed against the approved production backup target;
- backup retention and recovery evidence cannot yet be closed.

A dedicated external backup disk may be HDD or SSD. Enterprise AI Office does not require SSD for this purpose. The important properties are physical independence from the Mac Studio internal disk, adequate capacity/reliability, and approved encryption/retention policy.

Until that operator input exists, deployment work should continue on Production Ready checks that do **not** depend on the external backup target. The deployment must not falsely declare Production Ready merely to remove the blocker.

## Protected deployment state

Detailed non-public runtime state is maintained outside the public repository in protected deployment storage.

The public repository must not contain:

- passwords;
- API keys;
- OAuth tokens;
- bearer tokens;
- employee credentials;
- real employee identifiers;
- private host/network identifiers beyond intentionally sanitized descriptions;
- protected company configuration.

Actual deployment truth is:

```text
active private company configuration
+
protected deployment/runtime state
+
observed runtime behavior
```

This public file is only a sanitized progress summary.

## Capabilities intentionally outside the active deployment

No optional Enterprise AI Office capability is currently enabled in the active company configuration.

Examples currently outside the active deployment include:

- governed Email / external send;
- Messaging;
- Hermes Cron;
- Hermes Kanban;
- employee coding delegation;
- hermes-webui employee exposure;
- Remote access;
- SSO expansion;
- Employee Hermes long-term memory;
- Media Transcription / audio-video knowledge ingestion.

Optional capabilities should be added only when explicitly selected and accepted under their own capability contracts.

## Reference demo vs current deployment

[`DEPLOYMENT-STATE.md`](./DEPLOYMENT-STATE.md) records the earlier **sanitized local reference/demo validation** performed before this company deployment. It is useful reproducibility evidence, but it is **not** the current Mac Studio runtime state.

That reference record contains historical choices such as:

- MacBook demo host characteristics;
- `gpt-5.5`;
- DashScope embedding/chat models;
- `sales` / `qc` demo Profiles.

Do not copy those values into the current deployment unless the active company configuration explicitly selects them.

Fresh deployments should start from [`DEPLOYMENT-STATE.template.md`](./DEPLOYMENT-STATE.template.md) and keep the real operational copy in protected deployment storage when it contains company-private information.

## Next deployment direction

The system is usable at `CONFIGURED READY — PASS` while the production backup/restore boundary remains open.

Continue all Production Ready work that is independent of the missing external backup target. After an approved independent encrypted backup disk and policy are provided, complete backup generation, off-primary copy, isolated restore, and the remaining Production Ready acceptance evidence.
