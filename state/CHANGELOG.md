# Enterprise AI Office Deployment Changelog

This file is a template for material deployment changes.

Do not record secrets. Do not turn it into a transcript of every terminal command.

## Entry format

```markdown
## YYYY-MM-DD — Short change title

Component:
Environment:

### Before

<previous state>

### After

<new state>

### Reason

<why this change was needed>

### Validation

<tests / checks performed>

### Rollback

<how to return to previous state, if applicable>

### Notes

<known limitations / follow-up>
```

---

## 2026-09-06 — Final employee client permission and corpus cleanup

Component: Open WebUI employee client, WeKnora synthetic demo corpus
Environment: Local Apple Silicon Mac with OrbStack; synthetic demo data

### Before

- Ordinary employee Settings exposed System Prompt and Advanced Parameters.
- The Products & Technical synthetic document contained local demo
  infrastructure details.
- Earlier terminal probes used `NO_TERMINAL_TOOL` as an observation, although
  the actual security evidence was the absence of a tool call and the
  read-only employee Profile toolsets.

### After

- Used Open WebUI `v0.11.3` native Default permissions to set `Allow Chat
  System Prompt = off` and `Allow Chat Params = off` for ordinary users.
- Kept File Upload enabled; normal chat, assistant visibility, and history
  remained enabled in the Sales and QC UI.
- Rewrote and reindexed the Products & Technical synthetic document so it
  contains only simulated enterprise product and quality-workflow knowledge.
- Removed the temporary local attachment fixture and deleted the temporary
  Sales smoke-test chat after verifying the upload and refresh behavior.
- Kept employee Hermes long-term memory and user profiles disabled.

### Reason

Finish the bounded synthetic employee-client demo without adding components or
changing the architecture.

### Validation

- Sales and QC Settings pages no longer exposed System Prompt or Advanced
  Parameters after the native permission change.
- Sales grounded chat returned source `Demo Products & Technical.md` after
  reindexing and contained no local endpoint/runtime detail.
- Sales and QC model visibility remained `general,sales` and `general,qc`.
- Profile key isolation remained same-Profile HTTP 200 and cross-Profile HTTP
  401. Cross-department and default/admin Open WebUI requests returned HTTP 400
  `Model not found`.
- Sales/QC terminal requests returned HTTP 200 with no terminal/system tool
  call; the employee Profile toolsets remained read-only WeKnora retrieval
  only. No specific refusal marker was required.
- File upload, normal chat, source visibility, history, and employee
  long-term-memory-disabled checks passed.

### Rollback

Re-enable the two native Default permissions in Open WebUI if the previous demo
behavior is specifically needed. Restore the prior synthetic document only for
an isolated test; do not reintroduce infrastructure details into employee
knowledge.

### Notes

This entry records only the final employee-client cleanup. Rich citation cards,
OrbStack reboot recovery, employee Hermes long-term memory, branding, and
production corpus work remain outside this demo stage.

## 2026-09-05 — First end-to-end Enterprise AI Office demo validated

Component: WeKnora, Hermes Agent, Open WebUI, deployment adapters
Environment: Local Apple Silicon Mac with OrbStack; synthetic demo data

### Before

- Repository contained architecture and deployment templates, but no validated local runtime record.
- The local host had an existing Hermes installation that required inspection before reuse.

### After

- Pinned and started WeKnora `v0.8.0` and Open WebUI `v0.11.3` with loopback-only container ports.
- Kept Hermes `0.21.0` host-native and enabled the `general`, `sales`, and `qc` Profile gateway routes with distinct API keys.
- Added read-only WeKnora MCP access, synthetic Company & Brand and Products & Technical KBs, and completed document ingestion using the protected Qwen/DashScope fallback after the initial OpenAI quota failure.
- Configured Open WebUI groups, employee model ACLs, and three server-side Hermes connections. The privileged default/admin Profile is not employee-exposed.
- Validated the end-to-end path: Open WebUI → authorized Hermes Profile → WeKnora MCP → grounded knowledge answer with source title.
- Disabled employee long-term Profile memory because a validated per-user Hermes session-header mapping is not available in this connection path.
- Added the tested Open WebUI Compose manifest and minimal WeKnora demo override. Marked the operational helper scripts executable.
- Created a protected pre-change Hermes default Profile archive before modifying the existing installation.
- Captured the reusable demo findings in commit `cabbef0f226b45e497c71e4003aed38c20f07c0f` and pushed them to `origin/main`.

### Reason

Build the requested macOS/OrbStack Enterprise AI Office demonstration while preserving the repository's source-of-truth, RBAC, least-privilege, and production-boundary requirements.

### Validation

- Container health, Open WebUI sign-in, group/model visibility, direct Profile key isolation, and grounded Open WebUI chats passed.
- General, Sales, and QC grounded Profile answers returned source titles from WeKnora.
- Sales and QC terminal escape probes returned `NO_TERMINAL_TOOL`.
- Employee memory remained deliberately disabled; backup restore and host reboot recovery were not run.

### Rollback

- Stop the demo Compose services from the configured EAIO runtime directory and remove the three demo Profile configs if reverting the local setup.
- Restore the protected pre-change Hermes default Profile archive only after confirming the exact target and preserving current user changes.
- Repository documentation/adapters can be rolled back with normal Git history; prefer `git revert` of the relevant committed change instead of rewriting published `main` history.

### Notes

- This is a local synthetic demo, not a production deployment. Hermes binds `0.0.0.0:8642` so OrbStack can reach the host process; keep it trusted-local-only.
- Employee MCP server names are intentionally unique per Profile because Hermes v0.21.0 multiplex registration is name-sensitive.

## 2026-09-06 — Validate employee-facing Open WebUI workflow

Component: Open WebUI employee client, Hermes Profiles, WeKnora retrieval
Environment: Local Apple Silicon Mac with OrbStack; synthetic demo data

### Before

- Backend health, RBAC, Profile-key isolation, backup/restore, and reboot
  recovery boundaries were already recorded. The employee UI had not yet been
  audited as a complete login-to-grounded-chat workflow.

### After

- Completed real UI sign-in tests for Sales and QC demo employees.
- Verified employee-visible assistant lists, grounded conversations, readable
  source names, follow-up context, refresh/logout-login conversation history,
  temporary text attachment handling, and closed-fail unauthorized model
  requests.
- Kept employee Hermes long-term memory and user profiles disabled.

### Reason

Validate whether native Open WebUI is a usable employee client without adding a
custom frontend, changing the architecture, or enabling new infrastructure.

### Validation

- Sales users exposed `general,sales`; QC exposed `general,qc` in the employee
  model route. Cross-department and default/admin Open WebUI model requests
  returned HTTP 400 `Model not found`.
- General, Sales, and QC UI workflows completed grounded WeKnora chats. Sales
  handled unsupported product and delivery claims conservatively; QC did not
  invent technical tolerances and produced a Hold-pending-evidence checklist.
- A five-turn Sales conversation survived refresh and logout/login. A small
  temporary text attachment was read and identified as attachment context, not
  durable company knowledge.
- Sales/QC terminal requests made no tool call and returned human-readable
  unavailable-capability responses, but the exact `NO_TERMINAL_TOOL` marker was
  not observed in this run.

### Rollback

No deployment or configuration change was made. This entry is observational;
revert only the documentation commit if the record itself must be corrected.

### Notes

- Source evidence is readable inline text rather than a rich expandable
  citation card.
- Open WebUI employee Settings exposes user-level System Prompt and Advanced
  Parameters controls.
- One grounded Sales answer surfaced local demo endpoint details present in the
  synthetic Products & Technical document. Sanitize or replace that corpus
  before production use.

## 2026-09-05 — Validate local backup and isolated restore

Component: WeKnora, Hermes Agent, Open WebUI, backup/restore helpers
Environment: Local Apple Silicon Mac with OrbStack; synthetic demo data

### Before

- The end-to-end demo was healthy, but no complete backup/restore rehearsal had
  been recorded.
- The host reboot recovery test had not been executed.

### After

- Added `scripts/backup.sh` for the inspected runtime: WeKnora PostgreSQL
  logical backup, WeKnora file storage, Open WebUI data, runtime configuration,
  Hermes Profiles/state/Skills/MCP, repository templates, protected credentials,
  a non-secret manifest, and checksums.
- Added guarded `scripts/restore.sh`, requiring a new target and
  `--confirm-isolated`; it restores into new temporary Docker resources and
  never stops or overwrites the live demo.
- Updated the backup/restore, operations, acceptance, and deployment-state
  documentation with the tested procedure and reboot continuation checklist.

### Reason

Verify that the current MacBook/OrbStack demo has a recoverable state without
adding components or changing the approved architecture.

### Validation

- Backup generation completed with PostgreSQL `pg_restore --list`, volume
  archive, manifest, and SHA-256 checks passing; secret values were not printed
  or committed.
- An isolated temporary Compose restore recovered both Knowledge Bases and
  document records; a restored Hermes Sales query returned the expected
  workflow and source title through the restored MCP configuration.
- Restored Open WebUI users signed in with Sales/QC model ACLs; unauthorized
  direct model probes returned HTTP 400 `Model not found`.
- Restored Hermes Profile key matrix returned only same-Profile HTTP 200s and
  cross-Profile HTTP 401s. Sales/QC terminal probes returned
  `NO_TERMINAL_TOOL`; employee memory remained disabled.
- `scripts/restore.sh` self-test also materialized a fresh temporary PostgreSQL
  container and both data volumes successfully.
- Host reboot recovery was intentionally not run because the active Codex
  session cannot safely resume and prove post-reboot state.

### Rollback

- The new helpers are ordinary repository files and can be reverted through
  Git. The live demo was not modified by the isolated restore.
- Remove only the exact temporary containers/volumes/targets listed by the
  restore helper after inspection; retain the successful backup generation.

### Notes

- The backup is still on the primary Mac and has no configured retention or
  encrypted off-device copy; this is not production disaster-recovery sign-off.
- Current final status is `PARTIAL — reboot recovery not yet executed`.

## 2026-09-05 — Prepare real Mac/OrbStack reboot recovery validation

Component: OrbStack, Docker Compose, Hermes LaunchAgent, operational state
Environment: Local Apple Silicon Mac with OrbStack; synthetic demo data

### Before

- The demo was healthy and isolated backup/restore had passed, but the actual
  host-reboot recovery test was still pending.

### After

- Recorded the live pre-reboot baseline and actual startup mechanisms in
  `state/DEPLOYMENT-STATE.md` and `docs/OPERATIONS.md`.
- Confirmed OrbStack is currently running but `app.start_at_login=false`; the
  post-login test therefore requires manually launching OrbStack.
- Confirmed live Compose project/container restart policies and the loaded
  Hermes LaunchAgent's `RunAtLoad`/`KeepAlive` behavior.
- Prepared the exact 14-step post-reboot checklist.

### Reason

Prepare a real reboot test without changing architecture, adding a startup
manager, or treating configuration evidence as recovery evidence.

### Validation

- Explicit-endpoint health check: 6 PASS, 0 FAIL; only backup freshness marker
  was WARN.
- General, Sales, and QC Profile checks returned HTTP 200 with source-backed
  answers.
- `orb status` was `Running`; both Compose projects and all live containers were
  present; Hermes LaunchAgent was loaded and running.
- Real reboot recovery remains `REBOOT RECOVERY NOT YET EXECUTED`.

### Rollback

- This is documentation/state only; revert the preparation commit if needed.

### Notes

- Stop here and reboot the Mac manually. After login and OrbStack startup,
  reopen Codex and continue the documented checklist.

## 2026-09-05 — Validate real Mac/OrbStack reboot recovery boundary

Component: OrbStack, Docker Compose, Hermes LaunchAgent, Open WebUI, WeKnora
Environment: Local Apple Silicon Mac with OrbStack; synthetic demo data

### Before

- The real reboot test had been prepared and the pre-reboot demo baseline was
  healthy.
- OrbStack's actual `app.start_at_login` setting was already known to be
  `false`; no startup configuration change was made for this validation.

### After

- A real macOS reboot was observed at `2026-09-05 23:13:22` local time.
- Hermes LaunchAgent `ai.hermes.gateway` recovered automatically at GUI login;
  it was running with `runs = 1` and its API returned HTTP 200.
- The first post-login probe found OrbStack `Stopped`, no Docker socket, and no
  reachable Docker/Compose services. Read-only diagnosis confirmed the
  OrbStack login item was disabled and only the privileged helper LaunchDaemon
  was present.
- During the read-only diagnostic window, without a configuration write or
  explicit `open -a OrbStack`, OrbStack became `Running` at approximately
  `23:17:37`. Docker restart policies then recovered all five WeKnora
  containers and `eaio-open-webui`; all configured service health checks became
  healthy.
- General, Sales, and QC Open WebUI grounded chats returned HTTP 200 with
  WeKnora source titles. Same-Profile key requests returned HTTP 200 and all
  cross-Profile requests returned HTTP 401. Sales/QC terminal probes returned
  `NO_TERMINAL_TOOL`. Unauthorized Sales/QC/default/admin model probes returned
  HTTP 400 `Model not found`. Employee Hermes memory and user profiles remained
  disabled.

### Reason

Run the requested real reboot validation without changing the architecture,
adding components, or changing startup configuration.

### Validation

- OrbStack/Docker availability, both Compose projects, all six containers,
  Hermes LaunchAgent/API, WeKnora API/UI, and Open WebUI were checked after the
  runtime became available.
- The end-to-end Open WebUI → Hermes → WeKnora grounded path was repeated for
  General, Sales, and QC, including source-title evidence.
- Profile API-key isolation, Sales/QC terminal denial, employee model ACLs,
  default/admin non-exposure, and disabled employee long-term memory were
  repeated successfully.

### Rollback

- No configuration, service definition, or runtime data was changed by this
  validation. There is no operational rollback action.

### Notes

- Exact intervention boundary: OrbStack was unavailable at the first post-login
  check and became available during CLI diagnostics; no explicit app launch or
  configuration write was performed.
- This run is `NOT AUTOMATIC`. `REBOOT RECOVERY PASS` and `RESILIENCE DEMO PASS`
  were intentionally not recorded because the first post-login probe failed to
  find the OrbStack runtime.

## Repository bootstrap history

### 2026-09-05 — Enterprise AI Office executable repository baseline created

Component: Project architecture / governance / implementation bootstrap
Environment: Public reference repository

#### After

- Selected v1 architecture documented.
- WeKnora established as enterprise knowledge layer.
- Hermes Agent established as primary Agent runtime.
- Open WebUI established as employee Web client.
- hermes-webui established as administrative Hermes surface.
- Codex and Claude Code established as specialist coding workers.
- Apache-2.0 project license added.
- Third-party license boundaries documented.
- `AGENTS.md` added as the highest-priority AI agent operating contract.
- Generic architecture, deployment, security, Profile, RBAC, knowledge, operations, backup, upgrade, and acceptance standards added.
- Generic `config/company.example.yaml` and non-secret environment template added.
- Reusable General, Sales, QC, Marketing, and Engineering SOUL templates added.
- Initial shared `company-knowledge` and `enterprise-security` Hermes Skill templates added.
- Infrastructure adapter guidance added for WeKnora, Open WebUI, and Hermes.
- Read-only `preflight.sh` and `health-check.sh` operational helpers added.
- Deployment-state template added.
- ARMOR separated as the first reference implementation rather than the universal project identity.
- Contribution guidance and runtime/secret `.gitignore` rules added.

#### Reason

Turn the initial ARMOR-specific design into a reusable, AI-agent-readable and increasingly executable Enterprise AI Office project that another company or AI engineering agent can understand without reconstructing the architecture from conversation history.

#### Validation

- Repository root and target directories were re-read after creation.
- README documentation map and repository tree were synchronized to actual files.
- Generic documents preserve the same component/source-of-truth boundaries.
- Public templates contain placeholders rather than production secrets.
- The repository explicitly distinguishes tested architecture/standards from runtime-specific deployment manifests that still require validation on the first real ARMOR deployment.

#### Rollback

Git history can restore earlier repository content. No production infrastructure is affected by this repository bootstrap.

#### Next validation milestone

The next major milestone is the first ARMOR Mac Studio deployment. That deployment should validate exact upstream versions, real service/volume names, Open WebUI ↔ Hermes Profile/RBAC/memory behavior, Codex/Claude Code delegation under the long-running service account, backup/restore commands, Kanban, Cron, and the selected enterprise messaging platform. Reusable validated runtime artifacts can then be promoted into `infrastructure/` and `scripts/`.
