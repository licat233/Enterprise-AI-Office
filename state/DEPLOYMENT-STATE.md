# Enterprise AI Office Deployment State

> Sanitized local-demo record. Secrets, tokens, passwords, and host identifiers are intentionally omitted.

Last updated: 2026-09-06
Deployment status: `local-demo-validated`
Demo readiness: `DEMO READY`
Company / environment: `MacBook local demo / first generic reference validation`

The versions and model choices recorded below describe this validation run; they are not permanent Enterprise AI Office requirements.

## Host

| Field | Value |
| --- | --- |
| Host type | Apple Silicon Mac with OrbStack |
| OS | macOS 14.8.7 |
| CPU / architecture | arm64 |
| RAM | 16 GB |
| Storage | Approximately 201 GB free at validation |
| Hostname | Omitted |
| LAN / private address strategy | Loopback-only published container ports; Hermes is trusted-local-only because its listener also serves the OrbStack bridge |

## Container Runtime

| Field | Value |
| --- | --- |
| Runtime | OrbStack |
| Version | OrbStack 2.2.3; Docker Engine 29.4.0; Docker Compose 5.1.2 |
| Startup behavior | WeKnora and Open WebUI use `restart: unless-stopped`; Hermes Gateway runs as the user LaunchAgent `ai.hermes.gateway` |
| OrbStack login startup | Actual `orb config get app.start_at_login` is `false`; the first post-login probe found OrbStack stopped, and automatic Mac/OrbStack recovery is not claimed |
| Host reboot rehearsal | Executed 2026-09-05; Hermes recovered at login, but OrbStack was stopped at the first post-login probe and the full stack is not an automatic-recovery PASS |

## WeKnora

| Field | Value |
| --- | --- |
| Version / tag | `v0.8.0` |
| Commit if applicable | `1edcd54b43606d9079bb36650efe3f68707a79ea` |
| Deployment method | Pinned upstream Compose core stack under `$EAIO_RUNTIME_DIR/WeKnora` |
| Database | Upstream PostgreSQL container, internal-only; `pg_isready` accepting connections |
| Cache | Upstream Redis container, internal-only; authenticated `PING` returned `PONG` |
| File storage | Upstream persistent Docker-managed storage under the external runtime directory |
| Embedding model | DashScope `qwen3.7-text-embedding` |
| Embedding dimension | `1024` |
| Rerank model | None configured for this demo |
| Chat model if used | DashScope `qwen-plus` |
| MCP/API bridge | Official WeKnora MCP server over the supported API; read-only retrieval tools |
| Knowledge Bases | `Company & Brand` (`33362e35-04e8-4ce2-b2c0-8e70169063c7`); `Products & Technical` (`aa32f6dd-96a2-414f-a781-00ce162a1545`) |

The corpus is synthetic and stored outside Git at `$EAIO_RUNTIME_DIR/demo-corpus`. Both demo documents were ingested and completed successfully. The WeKnora API is published at `http://127.0.0.1:18080`; its UI is at `http://127.0.0.1:8088`.

## Hermes Agent

| Field | Value |
| --- | --- |
| Version / release | `0.21.0` |
| Commit if applicable | `f1ccf436a27522c1bb5d36383a6f13b950676338` |
| Version note | Hermes reports a newer upstream update is available; no unreviewed upgrade was applied |
| Installation | Host-native under the existing Hermes installation |
| Gateway service | LaunchAgent `ai.hermes.gateway`, healthy |
| API listener | `0.0.0.0:8642` for the local OrbStack bridge; health endpoint `http://127.0.0.1:8642/health` |
| Multi-Profile/multiplex | Enabled |
| Served Profile allowlist | `general`, `sales`, `qc` |
| Default model/provider | `gpt-5.5` via `openai-codex` |
| Memory provider | Employee Profile memory and user profiles disabled; conversation history remains in Open WebUI |

### Profiles

#### default / admin

- Purpose: privileged Hermes administration and engineering control surface.
- Employee exposed: `false`.
- Model: `gpt-5.5` via `openai-codex`.
- Tools/toolsets: privileged local Hermes capabilities plus the read-only WeKnora bridge; not an employee toolset.
- MCP: root-level WeKnora server.
- Credentials boundary: separate privileged API key; never configured as an Open WebUI employee connection.

#### general

- Purpose: broad office assistant grounded in approved knowledge.
- Employee groups: `All-Employees`.
- Model: `gpt-5.5` via `openai-codex`.
- Tools/toolsets: seven read-only WeKnora retrieval tools only.
- MCP: profile-scoped `weknora_general` server.
- Memory policy: disabled (`memory: false`, `user_profile: false`).

#### sales

- Status: `enabled`.
- Employee groups: `Sales`.
- Model: `gpt-5.5` via `openai-codex`.
- Tools/toolsets: seven read-only WeKnora retrieval tools only.
- MCP: profile-scoped `weknora_sales` server.
- Memory policy: disabled (`memory: false`, `user_profile: false`).

#### qc

- Status: `enabled`.
- Employee groups: `QC`.
- Model: `gpt-5.5` via `openai-codex`.
- Tools/toolsets: seven read-only WeKnora retrieval tools only.
- MCP: profile-scoped `weknora_qc` server.
- Memory policy: disabled (`memory: false`, `user_profile: false`).

#### marketing

- Status: `not enabled in this demo`.
- Employee groups: none.

#### engineering

- Status: `not enabled in this demo`.
- Employee groups: none. Coding delegation and engineering tool expansion were not part of this local validation.

## Open WebUI

| Field | Value |
| --- | --- |
| Version | `v0.11.3` |
| Image commit | `2a960a59fe1dbbd35282f0556b3666d81102e781` |
| Deployment method | Pinned Compose manifest; persistent named volume `open-webui-data` |
| Employee URL / access method | `http://127.0.0.1:3000`, local login form |
| Authentication | Open WebUI local accounts; admin and demo-user credentials are in protected files outside Git |
| Signup | Disabled after provisioning; login form enabled |
| Groups | `All-Employees`, `Sales`, `QC` |
| Hermes Profile resources | General Assistant → `general`; Sales Assistant → `sales`; QC Assistant → `qc` |
| Default employee permissions | Native Open WebUI defaults: `Allow Chat System Prompt = off`, `Allow Chat Params = off`, `Allow File Upload = on`; normal chat and history remain enabled |
| Long-term memory header/scoping | Disabled deliberately; the deployed Open WebUI connection path does not provide a validated per-user Hermes session-header mapping |

Demo users `sales-test-a` and `sales-test-b` are in `All-Employees` and `Sales`. Demo user `qc-test` is in `All-Employees` and `QC`. Model visibility was verified through the employee `/api/v1/models` route: Sales users see `general` and `sales`; the QC user sees `general` and `qc`. No default/admin connection is present.

Employee-client validation observed on 2026-09-06: the real Open WebUI UI
allowed Sales and QC users to select only their permitted employee assistants,
completed grounded General/Sales/QC conversations, displayed readable source
titles, preserved a five-turn Sales conversation through refresh and
logout/login, and read a small temporary text attachment as attachment context
without treating it as durable company knowledge. The employee account menu
did not expose administration, providers, MCP, WeKnora, Profiles, or API keys.
The final cleanup used the native Default permissions editor to remove employee
System Prompt and Advanced Parameters editing while keeping file upload,
normal chat, and history available. The Products & Technical source was
reindexed after local infrastructure details were removed; the follow-up Sales
grounded answer still showed its source title without endpoint leakage.

## hermes-webui

| Field | Value |
| --- | --- |
| Repository | Not deployed in this demo |
| Version / commit | Not applicable |
| Deployment | Not applicable |
| Access boundary | `admin-only` when introduced; not an employee surface |

## Specialized Coding Agents

| Component | Version / status | Authentication / notes |
| --- | --- | --- |
| Codex | Available on host; not wired into employee Profiles | No employee delegation enabled |
| Claude Code | Available/recognized on host; not wired into employee Profiles | No employee delegation enabled |

## Messaging

| Field | Value |
| --- | --- |
| Platform | Disabled in this demo |
| Status | Not configured |
| Authorization method | Not applicable |
| Profile routing | Not applicable |

## Kanban

- Enabled: `not configured in this demo`
- Boards: none created
- Dispatcher mode: not applicable
- Business-critical workflows: none

## Cron

- Enabled: `not configured in this demo`
- Business-critical jobs: none
- Model/provider pinning policy: not applicable
- Delivery targets: none

## Backup

| Field | Value |
| --- | --- |
| Schedule | Not configured for this local demo |
| Retention | Not configured |
| Backup method | `scripts/backup.sh`: PostgreSQL logical dump, Docker volume archives, runtime configuration, Hermes state/Profiles, protected credentials, manifest, and checksums |
| Primary destination | Protected local generation under `$EAIO_RUNTIME_DIR/backups/<timestamp>`; the pre-change Hermes archive remains separately preserved |
| Off-primary-disk copy | No |
| Secrets recovery method | Protected local credential files; no secret values recorded here |
| Last successful backup | 2026-09-05, native demo backup generation `20260905T150125Z`; checksum and archive inspection passed |
| Last restore test | 2026-09-05, isolated temporary Compose/OrbStack restore; WeKnora, Open WebUI, Hermes, RBAC, key isolation, MCP, and terminal-denial checks passed |
| Restore helper | `scripts/restore.sh` requires a new target plus `--confirm-isolated`; it never overwrites or cleans live state |

## Network Exposure

```text
Open WebUI: 127.0.0.1:3000 only
WeKnora UI: 127.0.0.1:8088 only
hermes-webui: not deployed
Hermes API: process listens on 0.0.0.0:8642 so the OrbStack bridge can reach it; treat as trusted-local-only and do not expose externally
PostgreSQL: internal Docker network only
Redis: internal Docker network only
```

## Reboot Preparation

Pre-reboot baseline recorded on 2026-09-05:

- `orb status`: `Running`; OrbStack helper/app processes are present.
- `docker info`: reachable; the `weknora` and `open-webui` Compose projects are
  running.
- Actual live container policies: WeKnora app/docreader/frontend/PostgreSQL use
  `unless-stopped`, Redis uses `always`, and Open WebUI uses `unless-stopped`.
- `launchctl print gui/$(id -u)/ai.hermes.gateway`: LaunchAgent is loaded and
  `state = running`; the plist has `RunAtLoad=1` and `KeepAlive=1`. The recorded
  `last exit code = 78` is historical; the current Hermes process is running,
  listening, and its health endpoint returns HTTP 200.
- Explicit-endpoint health check: 6 PASS, 0 FAIL; backup freshness marker is
  the only WARN.
- General, Sales, and QC Profile model/chat checks returned HTTP 200 with
  source-backed answers.

Actual startup-boundary conclusion:

- OrbStack app startup is not currently automatic at macOS login. Its
  privileged helper LaunchDaemon is not equivalent to starting the OrbStack
  app/VM.
- Once OrbStack/Docker is available, the current Compose restart policies are
  the mechanism expected to recover WeKnora and Open WebUI containers.
- Hermes is independently managed by the loaded user LaunchAgent and should be
  launched at GUI login, subject to the post-reboot health check.

Pre-reboot status: `READY FOR REAL REBOOT TEST`.
This was preparation evidence only.

Post-reboot validation recorded on 2026-09-05:

- The Mac booted at `2026-09-05 23:13:22` local time; the first post-login
  probe therefore observed a real host reboot rather than a container restart.
- Hermes LaunchAgent `ai.hermes.gateway` recovered automatically at GUI login:
  `state = running`, `runs = 1`, `last exit code = (never exited)`, and the
  API health endpoint returned HTTP 200.
- OrbStack was `Stopped` at the first post-login probe. Docker then failed to
  connect because `$HOME/.orbstack/run/docker.sock` was absent, so WeKnora and
  Open WebUI could not yet have recovered. Read-only diagnosis confirmed
  `orb config get app.start_at_login` is `false`; macOS Background Task records
  show the OrbStack login item as disabled, while only the privileged helper
  LaunchDaemon is installed. The helper is not the OrbStack app/VM startup.
- During the read-only diagnostic window, without changing configuration or
  running `open -a OrbStack`, OrbStack processes appeared at `23:17:37` and
  the Docker socket became available. The existing Docker restart policies then
  recovered all five WeKnora containers and `eaio-open-webui`; all configured
  health checks became healthy. This conditional container recovery does not
  prove automatic Mac/OrbStack recovery.
- After services were available, the Open WebUI General, Sales, and QC
  grounded chats returned HTTP 200 with WeKnora source titles. The complete
  Profile key matrix, Sales/QC terminal-denial probes, and unauthorized model
  probes were repeated successfully. Employee Hermes `memory_enabled` and
  `user_profile_enabled` remained `false` for `general`, `sales`, and `qc`.
- Exact intervention boundary: OrbStack was unavailable at the first
  post-login check and became available during CLI diagnostics; no config write
  or explicit app launch was performed. Automatic reboot recovery is therefore
  not claimed.

Reboot recovery status: `NOT AUTOMATIC — OrbStack was stopped at the first
post-login probe; dependent Compose services recovered only after the runtime
became available`.

## Acceptance Status

Reference `docs/ACCEPTANCE-TESTS.md`.

- Functional: `PASS` — WeKnora app/document reader/PostgreSQL health checks, Redis authenticated `PING`, frontend/API liveness, Open WebUI health, both KB ingestions, direct Profile answers, grounded employee chats, and citations/source titles all passed.
- RBAC: `PASS` — group membership and employee model visibility verified; unauthorized direct chat attempts returned HTTP 400 `Model not found` for the other department's model.
- Profile key isolation: `PASS` — each employee Profile key returned HTTP 200 only for its own route and HTTP 401 for the other two routes.
- Memory isolation: `DISABLED` — employee Hermes long-term memory is deliberately off; no cross-user memory channel is enabled.
- Dangerous-tool isolation: `PASS` — Sales and QC terminal requests produced no terminal/system tool call; the employee toolsets remain WeKnora read-only retrieval only, and the backend boundary is fail-closed. A specific natural-language refusal marker is not required.
- Employee client: `PASS` — Sales/QC login, assistant visibility, native permission cleanup, grounded chat, source visibility, conversation persistence, temporary text attachment handling, direct unauthorized model rejection, file upload, and history passed. Source presentation remains plain inline text rather than a rich citation card.
- Backup restore: `PASS` — native backup artifacts passed checksums; an isolated restore recovered WeKnora PostgreSQL/Knowledge Bases, Open WebUI state, Hermes Profiles/configuration, and representative grounded access.
- Reboot recovery: `NOT AUTOMATIC` — the real reboot was observed, Hermes
  recovered at login, but OrbStack was stopped at the first post-login probe;
  after OrbStack became available, Docker restart policies recovered WeKnora
  and Open WebUI and all post-recovery functional/security checks passed.

## Known Issues / Limitations

- This is a local synthetic demonstration, not a production deployment.
- The initial OpenAI model configuration was quota-exhausted during ingestion, so the validated demo uses the protected DashScope Qwen model configuration. Replace it with an approved production provider before rollout.
- The scoped WeKnora viewer key supports retrieval from the two demo KBs. `list_shared_knowledge_bases` correctly returns 403 because that endpoint is outside the key's `retrieve` capability/scope.
- Hermes v0.21.0 multiplex registration is name-sensitive; the employee MCP servers intentionally use unique names (`weknora_general`, `weknora_sales`, `weknora_qc`) so each Profile receives its own read-only tool scope.
- Hermes emits an unsandboxed/network-access warning because the local process binds `0.0.0.0`; keep the host firewall and loopback-only UI bindings in place.
- Backup generations and secrets currently remain on the same Mac; no encrypted independent copy or retention schedule has been configured.
- Mac/OrbStack automatic reboot recovery was not proven: OrbStack's actual
  login startup setting is disabled, and the first post-login probe found no
  OrbStack runtime or Docker socket.
- A rich expandable citation-card presentation is not part of this demo; source
  titles remain readable inline in the employee UI.

## Pending Decisions

- Replace synthetic documents and demo credentials with approved company data and secret management.
- Move a successful backup generation to encrypted independent storage and configure retention/monitoring.
- Decide whether to enable OrbStack's existing login-start setting for a future
  automatic-recovery run, then repeat the reboot test without treating delayed
  CLI-triggered availability as proof of automatic recovery.
- Validate a supported per-user Hermes session-key/header mapping before enabling employee long-term memory.
- Review and pin current upstream releases before any production deployment; decide separately on messaging, Kanban/Cron, and restricted engineering delegation.

## 2026-09-09 — Phase 2 clean-room migration state

This section records the later Enterprise Hermes clean-room migration on the
actual Mac Studio target. It supersedes the earlier local synthetic-demo
assumptions for the Hermes runtime only; it does not retroactively change the
historical demo record above.

- Target host: authorized Mac Studio deployment target; private host and
  checkout details are intentionally omitted.
- Hermes runtime: `0.21.1`; active global source is the protected Hermes
  global SOUL source.

> Version-authority note: `0.21.1` is retained here as the phase-specific
> runtime observation recorded on 2026-09-09. It is not the current
> reconstruction baseline. As of 2026-09-11, `config/validated-stack.yaml`
> and `state/REAL-DEPLOYMENT-STATUS.md` identify Hermes `0.21.0` as the
> current validated/reference runtime. The public history does not establish
> the exact transition between these observations, so do not infer an
> upgrade/downgrade procedure from this historical line.
- Enterprise Global Rule v1.0 Frozen Baseline is active, with the approved
  communication baseline at the top of the editable target SOUL.
- Global and General long-term Memory are OFF. No legacy Memory was read or
  migrated.
- The served Profile remains `general`; the prepared Department Profile is not
  served because no official Department identifier/name was found.
- General is fail-closed to the target-native WeKnora read-only tool set. Web,
  browser, terminal, file, code execution, delegation, cron, Memory, session
  search, computer use, and media-generation tools are disabled for General.
- 40 deduplicated P0/P1 Department-shared Skills are staged under
  `skills/shared/department/` but are not served by a live Department Profile.
  P2/P3 assets and protected secret references were not activated.
- `ARMOR_VAULT_ROOT` is bound to the approved private Vault path on the target.
  Vault and WeKnora content were not modified.
- Enabled cron jobs: `0`. Relevant plugins migrated: `0`.
- Validation: Global Rule security tests `5/5 PASS`; General WeKnora smoke
  `PASS`; General regression `2/2 PASS`; path decontamination `PASS`; gateway
  restart `PASS` and remains launchd-supervised.
- A pre-existing stale LaunchAgent plist warning remains documented; the
  existing Hermes installation/service mechanism was not rewritten.
- Rollback backup: protected Phase 2 backup retained outside Git.
- Phase 2 decision: `ENTERPRISE HERMES CLEAN-ROOM PHASE 2 — PASS`.

## 2026-09-09 — Phase 3 Department Profile state

- Department identity confirmed from the existing protected ARMOR namespace:
  `operations` / `Operations Assistant`.
- Created the supported Hermes Operations Profile and added it to the explicit
  gateway served allowlist alongside `general`.
- Operations inherits the active Global Rule and uses a small Department SOUL;
  long-term Memory and user-profile Memory remain OFF.
- Bound Operations to the existing Company Knowledge WeKnora read-only MCP
  surface. Only the six approved read tools are enabled; no WeKnora write,
  management, deletion, or Vault write path is enabled.
- Activated 12 of the 40 staged P0/P1 Skills: 7 `SAFE_BASELINE` and 5
  `WORKFLOW`. 28 remain disabled; `PRIVILEGED_OR_EXTERNAL` enabled count is
  `0`. P2/P3 assets remain untouched.
- Operations built-in boundary: Skills plus read-only WeKnora only; Web,
  browser, terminal, file, code execution, delegation, Memory, session search,
  Cron, plugins, computer use, and external actions are disabled. Hermes
  `skill_manage` remains approval-guarded with no Department approval granted.
- Functional validation: `15/15 PASS`; enabled-Skill smoke tests `12/12 PASS`;
  security probes `6/6 DENIED`; General regression `3/3 PASS`; Operations
  health endpoint HTTP 200; Cron `0`.
- Company-private configuration declares `operations-employees` and the
  Operations Assistant mapping for the existing Open WebUI RBAC workflow.
- Recovered the existing Open WebUI runtime through the authoritative Compose
  project `eaio-openwebui`; the apparent absence was caused by querying the
  wrong project name `eaio-open-webui`, not by loss of the deployment. The
  existing `eaio-open-webui` container is healthy on `127.0.0.1:3000`, using
  the existing named volume `eaio-openwebui_open-webui-data` and the existing
  persistent `webui.db` state.
- Existing Open WebUI state was preserved: existing administrator and employee
  accounts/groups, and the existing `General Assistant` model/connection. No
  database or volume reset,
  replacement bootstrap, user deletion, or credential reset occurred.
- Added the required protected independent Operations Profile authentication
  binding; this was the minimum necessary runtime binding because Hermes
  multiplex routing requires a named Profile's own credential. Secret values
  and the protected environment remain outside Git.
- Provisioned the declared `Operations Employees` group, reused the existing
  authorized test identity, added the `Operations Assistant`
  model with group read access, and preserved General's existing mapping.
- Open WebUI employee visibility: `PASS` — exactly `General Assistant` and
  `Operations Assistant`; default/admin and unrelated upstream models were
  not visible.
- Open WebUI Operations acceptance: `5/5 PASS`; security acceptance:
  `5/5 DENIED`; General regression after provisioning: `3/3 PASS`.
- Phase 3 Hermes runtime decision: `PASS`; full employee-facing Department
  Assistant exposure: `PASS`.
- Rollback backup: protected Phase 3 backup retained outside Git.

## 2026-09-09 — Global Rule v1.1 Root-Cause Persistence

- Active Global Rule version: `v1.1 — Root-Cause Persistence`.
- The complete editable rule remains in the single protected Hermes global
  source; no competing full Global Rule source was created.
- General and Operations inherit the updated Global Rule. Neither Profile
  received a duplicated copy or a Profile-specific override.
- Global, General, and Operations long-term Memory remain OFF. No legacy Memory
  was imported.
- Persistent errors route to their authoritative owner: Knowledge, Skill,
  Department policy, Global Rule, implementation, protected runtime
  configuration, Project/Operating Plan, Scheduler, or Session as applicable.
  Memory is not used as a correction overlay.
- Host/runtime facts remain runtime discovery or protected deployment
  configuration concerns, not durable Memory.
- Behavioral validation: Operations “Remember This” and root-cause routing
  tests `5/5 PASS`; General and Operations inheritance checks `PASS`.
- Regression: General health `PASS`; Operations health `PASS`; Company
  Knowledge retrieval `PASS`; General/Operations Memory `OFF`; Cron `0`.
- Vault and WeKnora were not modified. Department Skills were not modified.
- Rollback backup: protected v1.1 pre-change Global Rule backup retained
  outside Git.

## 2026-09-11 — EAO Operations RBAC v1 closure

- Target: armor@MacStudio.local.
- Status: CLOSED / FROZEN / PASS.
- Open WebUI: v0.11.3; published as 0.0.0.0:13000 -> 8080.
- All Employees has READ access to General Assistant.
- Operations Employees has READ access to Operations Assistant.
- Employee defaults retain basic chat and approved productivity features;
  workspace management, sharing, access grants, API keys, native web search,
  image generation, code interpreter, memories, controls, and valves remain
  denied.
- Open WebUI Knowledge records = 0 is intentional.
- Company Knowledge access is retrieve-only through the Hermes Operations
  Profile and operations-weknora MCP namespace; WeKnora scope is the Company
  Knowledge tenant with full_access=false and capabilities=["retrieve"].
- The secondary Operations API-server binding is disabled so the Profile uses
  the shared Hermes multiplex gateway; no secondary port is created.
- The non-secret checked-in routing source is
  infrastructure/hermes/operations-routing.example.yaml.
- Sanitized before/after RBAC snapshots are retained under docs/rbac/snapshots.
- Production health, employee knowledge retrieval, admin/employee boundaries,
  LAN/Tailscale access, HTTP 401 unauthenticated denial, and restart
  persistence were verified.
- Future changes require a new explicit task and baseline version.
