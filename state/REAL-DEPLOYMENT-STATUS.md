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

The active protected company configuration now enables the Core employee path plus the validated `media_transcription` optional capability. All currently enabled capabilities have passed their applicable acceptance boundary, so `CONFIGURED READY — PASS` remains valid.

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
| Media transcription capability | ✅ Enabled in protected config / 18 of 18 acceptance checks PASS |
| English transcription route | ✅ Whisper preferred |
| Chinese / Cantonese transcription route | ✅ SenseVoice preferred |
| Transcript Markdown + timestamps | ✅ PASS |
| Automatic knowledge publication | ✅ Disabled; human review required |
| Retrieval-only transcript → WeKnora compatibility | ✅ HTTP 201 KB create / HTTP 200 ingest + retrieval |
| WeKnora Summary/Chat model for transcript test | ✅ Not required / not configured |
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
KnowledgeQA/Chat not required for Core or retrieval-only transcript compatibility
Rerank           disabled
VLLM             disabled
ASR              disabled in WeKnora Core
```

DashScope and `qwen-plus` are not required for the selected Core or media-transcription retrieval path.

Media transcription remains a separate host-native capability rather than a WeKnora ASR model role:

```text
English audio/video
→ Whisper preferred

Chinese / Cantonese audio/video
→ SenseVoice preferred

media
→ ffmpeg-compatible audio extraction when needed
→ local ASR
→ timestamped Markdown transcript
→ human review
→ optional later knowledge publication
```

Whisper and SenseVoice are treated as complementary engines. The deployment does not run both engines by default or introduce an ensemble/benchmark pipeline merely because both are installed.

## Media transcription acceptance

The first real Mac Studio deployment completed the media-transcription acceptance with `18/18 PASS`.

Validated boundaries include:

- existing local Whisper and SenseVoice installations were reused rather than replaced by a new ASR platform;
- English routing prefers Whisper;
- Chinese and Cantonese routing prefer SenseVoice;
- transcript output is UTF-8 Markdown with timestamps and source metadata;
- original media remains unchanged;
- temporary extraction/work files are cleaned up;
- transcription does not automatically publish content into `Company Knowledge`;
- the capability does not require a new background queue, daemon, database, Web UI, or cloud transcription provider;
- Core services remained healthy after enablement.

WeKnora transcript compatibility was validated through a temporary retrieval-only Knowledge Base:

```text
Temporary KB creation          HTTP 201
Embedding                      existing bge-m3 / 1024 only
summary_model_id               unset
Transcript ingestion           HTTP 200
Retrieval                      HTTP 200
Unique marker                  returned
Source filename                returned
Temporary document / KB        deleted after test
Formal Company Knowledge       unchanged
```

This evidence confirms an important deployment rule: a WeKnora UI workflow that offers or requests a Conversation/Summary model does not imply that document ingestion and retrieval require one. For retrieval-only Knowledge Bases, the deployed WeKnora v0.8.0 path can operate with Embedding bound and `summary_model_id` unset.

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
- latest health state is 6 PASS, 0 FAIL, and 1 WARN, where the only WARN is the expected missing backup-freshness marker while no approved off-primary backup destination exists.

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

## Capability state

Currently enabled employee/business capabilities:

- Core employee knowledge path;
- Media Transcription / audio-video transcription, with manual knowledge-publication review.

Other optional capabilities remain disabled unless explicitly selected later, including:

- governed Email / external send;
- Messaging;
- Hermes Cron;
- Hermes Kanban;
- employee coding delegation;
- hermes-webui employee exposure;
- Remote access;
- SSO expansion;
- Employee Hermes long-term memory.

Optional capabilities should be added only when explicitly selected and accepted under their own capability contracts.

## Public repository synchronization note

The protected deployment state confirms the capability is enabled and accepted on the real Mac Studio. Public reusable implementation/configuration changes must still be synchronized separately from the target-host working copy; runtime success alone must not be confused with a complete GitHub implementation artifact.

## Reference demo vs current deployment

[`DEPLOYMENT-STATE.md`](./DEPLOYMENT-STATE.md) records the earlier sanitized local reference/demo validation. It is useful reproducibility evidence, but it is **not** the current Mac Studio runtime state.

Fresh deployments should start from [`DEPLOYMENT-STATE.template.md`](./DEPLOYMENT-STATE.template.md) and keep the real operational copy in protected deployment storage when it contains company-private information.

## Next deployment direction

The system is usable at `CONFIGURED READY — PASS`, including the currently enabled media-transcription capability, and all Production Ready acceptance work that does not depend on external backup hardware has passed.

After an approved independent encrypted backup destination and policy are provided, complete the off-primary backup copy, retention/freshness evidence, and final external restore acceptance. If those pass, the deployment may advance to:

```text
PRODUCTION READY — PASS
```
