# Real Deployment Status — Sanitized Public Summary

> This file is a **sanitized public progress summary** for the explicitly authorized real company deployment. It is not the protected runtime state record and must never contain credentials, real employee identifiers, private network details, mailbox data, or secret values.

Last updated: 2026-09-12

## Deployment authorization

```text
Reference real deployment: ACTIVE / DEPLOYED / IN USE (separately authorized; runtime details private)
Target: designated company Mac Studio (publicly sanitized)
Requested readiness: configured-ready
Fresh-clone/new-target deployment authorization default: inactive
Blueprint lifecycle: installation_design (unchanged)
Blueprint Validation: not opened
```

The ARMOR real deployment is already independently authorized, deployed, active, and in use. This file exposes only a sanitized public summary; protected runtime details remain outside Git. The `real_deployment_task.active: false` value in `state/PROJECT-PHASE.yaml` is only the default authorization state for a fresh clone or a new target, so cloning the repository never implies permission to perform another real deployment. It is **not** the ARMOR deployment status. The existing ARMOR deployment authorization also does **not** advance the repository blueprint lifecycle.

## 2026-09-12 operational baseline conclusion

The ARMOR reference EAO baseline is no longer merely an installation or validation
exercise. It is deployed on the designated company Mac Studio and is available
for normal employee AI-office use through the approved private access boundary.

Observed operational facts already validated in the reference deployment include:

- employees can authenticate to Open WebUI;
- General Assistant is usable through the employee-facing client;
- the Operations employee path is deployed with its own RBAC boundary;
- conversation history persists across refresh/re-login;
- file upload is accepted under the validated employee boundary;
- Hermes → WeKnora knowledge retrieval returns grounded answers with source evidence;
- ordinary employee access remains least-privilege and unauthenticated access is denied;
- LAN and the already-approved Tailscale private path can reach the employee surface;
- restart/reboot acceptance has passed;
- historical backup/isolated-restore mechanics were validated during deployment work, but backup is not currently enabled as an operating capability.

Therefore the **EAO baseline construction phase is operationally complete for
normal use at `CONFIGURED READY — PASS`**. Ongoing work should be treated as
feedback-driven maintenance, defect correction, or bounded capability extension
rather than as evidence that the Core office platform is still unfinished.

The ARMOR owner has explicitly selected `CONFIGURED READY` as the current
delivery target. The Mac Studio internal disk is the current EAO runtime and
primary data storage. Backup/restore is an independent optional capability and
is currently disabled. It may be enabled later if business requirements and
storage conditions justify it.

Governed AI email marketing is a separate follow-on business capability. Existing
email/governance/Hermes/Cron assets should be reused through the Capability Reuse
Pass rather than reopening Core EAO architecture.

## 2026-09-11 synchronization update

The reference Mac Studio deployment has advanced beyond the 2026-09-08 core/media baseline. The following additional production capabilities and boundaries are now frozen and documented in this repository:

- **Hermes Skills Migration v1.0 — CLOSED**, frozen at commit `6ee5034811681d40ac1ce61cef315aac8551fdb5`.
- **Enterprise Web Research v1.0 — CLOSED / FROZEN / PASS**, frozen at commit `8d232285b68ed85aca146b81f3ca946f2502c357`.
- **Operations employee RBAC v1 — CLOSED / FROZEN / PASS**, frozen at commit `6848d89877db08c57d3b8c128efe7410f9c49ccb`.
- Open WebUI remains on **v0.11.3** and the employee surface is published on the approved private network boundary at host TCP **13000 → container 8080**. Authentication remains required.
- The same employee surface has also been successfully reached through the host's already-installed **Tailscale** private address. This is an additional approved private access path, not a replacement architecture or a public exposure.
- `All Employees` has explicit **READ** access to **General Assistant**.
- `Operations Employees` has explicit **READ** access to **Operations Assistant**.
- Employee groups do not receive Open WebUI Workspace administration grants.
- The production Operations path is:

```text
Operations Employee
→ Open WebUI Operations Assistant
→ Hermes /p/operations
→ Operations Profile
→ operations-weknora
→ Company Knowledge
```

- The Operations profile uses the existing shared Hermes gateway. Its profile-local API server binding is disabled to avoid a second listener conflict.
- The Operations WeKnora MCP registration is profile-locally named `operations-weknora` so it can coexist with the General profile registration in the same Hermes process.
- Company Knowledge access remains least privilege: `full_access=false`, `capabilities=["retrieve"]`.
- **Open WebUI native Knowledge records = 0 is intentional** for this architecture; company knowledge is reached through Hermes → WeKnora rather than duplicated into Open WebUI Knowledge.
- Employee long-term Hermes/Profile Memory remains **OFF**.
- The approved Operations capability set includes the migrated/frozen department Skills and Enterprise Web Research under their documented boundaries.
- Governed Email Operations assets exist in the repository, but unrestricted/autonomous customer-facing send is not implied by the presence of those assets. Human authority and the governed send boundary remain mandatory.

These updates supersede any earlier demo-only role list or network description when interpreting the current sanitized ARMOR reference deployment. The older `state/DEPLOYMENT-STATE.md` remains historical reference evidence.

## Current achieved readiness

```text
CORE READY — PASS
CONFIGURED READY — PASS
REBOOT ACCEPTANCE — PASS
PRODUCTION READY — NOT CURRENTLY REQUESTED
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

The active protected company configuration now enables the Core employee path, the frozen ARMOR Operations specialist lane, Enterprise Web Research through the approved Operations boundary, and the validated `media_transcription` optional capability. All currently enabled capabilities have passed their applicable acceptance boundary, so `CONFIGURED READY — PASS` remains valid.

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

The current table above is the later 2026-09-11 sanitized runtime truth. The
historical 2026-09-09 Phase 2 section in `state/DEPLOYMENT-STATE.md` records a
phase-local Hermes `0.21.1` observation. That older observation is preserved
for audit history but does not override `config/validated-stack.yaml` or this
current status. The public repository does not contain a complete
0.21.1→0.21.0 transition record; future reference-runtime version changes must
be accompanied by explicit changelog/upgrade evidence.
| Signup | ✅ Disabled |
| Employee groups / baseline ACL | ✅ Reconciled |
| General Assistant | ✅ Configured |
| Operations Profile / Assistant | ✅ Deployed / frozen reference |
| Operations employee ACL | ✅ `Operations Employees` READ → Operations Assistant |
| Enterprise Web Research v1.0 | ✅ Deployed / CLOSED / FROZEN / PASS |
| Raw Firecrawl / Obscura / CloakBrowser employee exposure | ✅ Not exposed directly |
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
| Primary EAO runtime/data storage | ✅ Mac Studio internal disk |
| Backup/restore capability | ➖ Optional / currently disabled |
| Historical backup/restore mechanics validation | ✅ Completed during deployment work |
| Retrieved prompt-injection source test | ✅ PASS |
| Real Mac Studio reboot acceptance | ✅ PASS |
| Post-reboot employee path | ✅ Grounded answer + source |
| Post-reboot ACL / history / upload / retrieve-only boundary | ✅ PASS |
| Independent encrypted backup target | ➖ Optional / not currently requested |
| Off-primary backup / retention / final external restore evidence | ➖ Optional future hardening |
| Production Ready | ➖ Not the current delivery target |

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

## Operational hardening and recovery evidence

The current ARMOR deployment uses the Mac Studio internal disk as its normal EAO
runtime and primary data storage. No backup schedule, backup destination, or
backup retention policy is currently enabled.

Earlier deployment work validated the repository's backup and isolated-restore
mechanics on the primary host. That evidence is retained because it proves the
optional capability can be activated later without redesigning EAO. It does not
mean a backup service is currently running or required for the deployed baseline.

Other completed operational evidence remains in force:

- application surfaces are loopback-only where applicable and database/cache/parser internals are not published as host ports;
- a real Mac Studio reboot was completed and the required employee path recovered successfully;
- after reboot, OrbStack/Docker, WeKnora, Open WebUI, Hermes, and Ollama were healthy;
- after reboot, the ordinary employee path again returned grounded company knowledge with source evidence;
- ordinary-employee visibility, history, file upload, retrieve-only knowledge boundaries, and disabled employee memory remained correct.

Backup/restore may be enabled later as a separate optional capability. If enabled,
its selected storage, retention, encryption, and restore-test policy must then
pass the dedicated backup acceptance contract.

## Reboot recovery boundary

`REBOOT ACCEPTANCE — PASS` confirms that the deployed system can recover through a real Mac Studio restart and re-establish the validated employee path.

The current operational recovery sequence still includes a human/operator boundary after host reboot:

- macOS GUI login is required;
- the existing operator recovery mechanism is used to bring the required user-session-dependent runtime into service;
- no macOS privilege boundary was bypassed;
- the deployment has **not** been validated as fully unattended boot-to-service recovery.

This is an accepted current operational limitation, not a reason to invalidate the completed reboot acceptance. If future requirements demand unattended recovery after power loss without operator login, that should be treated as a separate operational improvement rather than silently assumed from the current result.

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
- ARMOR Operations specialist lane, including the frozen migrated department Skills;
- Enterprise Web Research v1.0 through the approved bounded Operations path;
- Media Transcription / audio-video transcription, with manual knowledge-publication review.

Other optional capabilities remain disabled unless explicitly selected later, including:

- Backup / Restore;
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

The protected deployment state and public reusable implementation are aligned for the current sanitized reference capability set: Core, the frozen ARMOR Operations lane, Enterprise Web Research v1.0, and Media Transcription. Their reusable contracts, acceptance evidence, RBAC/tool boundaries, and recovery implications are represented in the current `main` branch. Runtime-specific private configuration and evidence remain protected outside Git.

## Reference demo vs current deployment

[`DEPLOYMENT-STATE.md`](./DEPLOYMENT-STATE.md) records the earlier sanitized local reference/demo validation. It is useful reproducibility evidence, but it is **not** the current Mac Studio runtime state.

Fresh deployments should start from [`DEPLOYMENT-STATE.template.md`](./DEPLOYMENT-STATE.template.md) and keep the real operational copy in protected deployment storage when it contains company-private information.

## Next deployment direction

The EAO baseline is deployed and in normal use at `CONFIGURED READY — PASS`.
Core-platform construction is closed. Future work should be driven by real usage
feedback, defect correction, or explicitly selected business capabilities.

The next planned business capability is governed AI email marketing. Backup/restore
remains optional and should be revisited only when ARMOR decides the business need
or storage conditions justify enabling it.
