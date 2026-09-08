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

## Current achieved readiness

```text
CORE READY — PASS
CONFIGURED READY — PASS
REBOOT ACCEPTANCE — PASS
PRODUCTION READY — BLOCKED ONLY BY EXTERNAL BACKUP / RESTORE EVIDENCE
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

## Current production status

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
| Signup | ✅ Disabled |
| Employee groups / baseline ACL | ✅ Reconciled |
| General Assistant | ✅ Configured |
| System Prompt editing | ✅ Disabled for ordinary employee |
| Advanced Parameters editing | ✅ Disabled for ordinary employee |
| Conversation history | ✅ Persists across refresh and re-login |
| File upload | ✅ Accepted and source reference visible |
| Unknown-company-fact behavior | ✅ Unavailable / no fabrication observed |
| Local Embedding | ✅ `bge-m3` / 1024 dimensions |
| Formal `Company Knowledge` | ✅ Created and bound to `bge-m3` |
| `general` WeKnora credential | ✅ Retrieve-only / `full_access=false` |
| Knowledge write-denial check | ✅ HTTP 403 |
| Hermes → WeKnora MCP | ✅ Grounded marker/source returned |
| Core service health | ✅ WeKnora / Open WebUI / Hermes / Ollama healthy |
| Core Ready | ✅ PASS |
| Configured Ready | ✅ PASS |
| Backup/restore scripts | ✅ Reconciled with active runtime layout |
| Temporary primary-disk backup generation | ✅ Validated |
| Isolated restore materialization | ✅ Validated without touching production |
| Restored employee-path acceptance | ✅ PASS |
| Retrieved prompt-injection source test | ✅ PASS |
| Real Mac Studio reboot acceptance | ✅ PASS |
| Post-reboot employee path | ✅ Grounded answer + source |
| Post-reboot ACL / history / upload / retrieve-only boundary | ✅ PASS |
| Independent encrypted backup target | ⏳ Not yet provided |
| Off-primary backup / retention / final external restore evidence | ⏳ Pending backup target and approved policy |
| Production Ready | ⛔ BLOCKED ONLY BY EXTERNAL BACKUP / RESTORE EVIDENCE |

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

## Production hardening completed

Production work that does not depend on an external backup destination has now been completed for the current deployment.

Completed evidence includes:

- `scripts/backup.sh` / `scripts/restore.sh` resolve the active runtime root instead of reference/demo or company-private hard-coded paths;
- backup coverage validated for PostgreSQL, WeKnora, Open WebUI, Hermes, configuration, manifest, and checksums;
- temporary backup generation created on the primary disk for recovery-path validation only;
- isolated restore materialization completed in independent directories, volumes, containers, and loopback ports without stopping or rebuilding production;
- restored `Company Knowledge`, known fact/source retrieval, General Assistant mapping, ordinary-employee visibility, history, file upload, fail-closed behavior, and required employee path all passed;
- all temporary restore resources were removed after acceptance;
- retrieved prompt-injection test source was actually retrieved, but Hermes `gpt-5.6-luna` treated the source as data rather than authority;
- the prompt-injection test did not expose configuration/credentials, execute unauthorized instructions, or invoke mutation-capable tools, while still returning the ordinary test marker and source;
- the prompt-injection test document was removed after acceptance and the production Knowledge Base was rechecked clean;
- application surfaces are loopback-only where applicable and database/cache/parser internals are not published as host ports;
- a real Mac Studio reboot was completed and the required production path recovered successfully;
- after reboot, OrbStack/Docker, WeKnora, Open WebUI, Hermes, and Ollama were healthy;
- after reboot, `bge-m3` returned 1024-dimensional embeddings;
- after reboot, the ordinary employee path again returned a grounded marker and source;
- after reboot, ordinary-employee visibility, `default/admin` fail-closed behavior, history, file upload, WeKnora read/write boundary, and disabled employee memory all remained correct;
- latest health state is 6 PASS, 0 FAIL, and 1 WARN, where the only WARN is the expected missing backup-freshness marker while no approved off-primary backup destination exists;
- no Whisper, SenseVoice, Email, Messaging, Cron, Kanban, or other optional capability was enabled during this production-hardening work.

A primary-disk backup or temporary isolated restore is validation evidence only. It does **not** substitute for a physically independent production backup target.

## Reboot recovery boundary

`REBOOT ACCEPTANCE — PASS` confirms that the deployed system can recover through a real Mac Studio restart and re-establish the validated employee path.

The current operational recovery sequence still includes a human/operator boundary after host reboot:

- macOS GUI login is required;
- the existing operator recovery mechanism is used to bring the required user-session-dependent runtime into service;
- no macOS privilege boundary was bypassed;
- the deployment has **not** been validated as fully unattended boot-to-service recovery.

This is an accepted current operational limitation, not a reason to invalidate the completed reboot acceptance. If future requirements demand unattended recovery after power loss without operator login, that should be treated as a separate operational improvement rather than silently assumed from the current result.

## Remaining Production Ready blocker

Production Ready is intentionally not declared yet. The only remaining boundary is the independent external backup / restore evidence.

### Independent encrypted backup destination and external recovery evidence

No approved physically independent encrypted backup destination has been provided yet.

Still required before Production Ready can pass:

- an approved external/off-primary backup destination;
- an approved retention policy and RPO/RTO target;
- a complete production backup generation copied off the Mac Studio primary disk;
- backup freshness/retention evidence against that destination;
- final restore evidence from the approved external backup copy.

The dedicated backup disk may be HDD or SSD. Enterprise AI Office does not require SSD. The important properties are physical independence from the Mac Studio internal disk, adequate capacity/reliability, approved encryption, and an explicit retention/recovery policy.

## Protected deployment state

Detailed non-public runtime state is maintained outside the public repository in protected deployment storage.

Actual deployment truth is:

```text
active private company configuration
+
protected deployment/runtime state
+
observed runtime behavior
```

The public repository must not contain passwords, API keys, OAuth/bearer tokens, employee credentials, real employee identifiers, private host/network identifiers beyond intentionally sanitized descriptions, or protected company configuration.

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

[`DEPLOYMENT-STATE.md`](./DEPLOYMENT-STATE.md) records the earlier sanitized local reference/demo validation. It is useful reproducibility evidence, but it is **not** the current Mac Studio runtime state.

Fresh deployments should start from [`DEPLOYMENT-STATE.template.md`](./DEPLOYMENT-STATE.template.md) and keep the real operational copy in protected deployment storage when it contains company-private information.

## Next deployment direction

The system is usable at `CONFIGURED READY — PASS`, and all current Production Ready acceptance work that does not depend on external backup hardware has passed.

After an approved independent encrypted backup destination and policy are provided, complete the off-primary backup copy, retention/freshness evidence, and final external restore acceptance. If those pass, the deployment may advance to:

```text
PRODUCTION READY — PASS
```
