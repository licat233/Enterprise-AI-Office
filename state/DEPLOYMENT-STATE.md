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
| Long-term memory header/scoping | Disabled deliberately; the deployed Open WebUI connection path does not provide a validated per-user Hermes session-header mapping |

Demo users `sales-test-a` and `sales-test-b` are in `All-Employees` and `Sales`. Demo user `qc-test` is in `All-Employees` and `QC`. Model visibility was verified through the employee `/api/v1/models` route: Sales users see `general` and `sales`; the QC user sees `general` and `qc`. No default/admin connection is present.

Employee-client validation observed on 2026-09-06: the real Open WebUI UI
allowed Sales and QC users to select only their permitted employee assistants,
completed grounded General/Sales/QC conversations, displayed readable source
titles, preserved a five-turn Sales conversation through refresh and
logout/login, and read a small temporary text attachment as attachment context
without treating it as durable company knowledge. The employee account menu
did not expose administration, providers, MCP, WeKnora, Profiles, or API keys.
The employee Settings page did expose user-level System Prompt and Advanced
Parameters controls. The synthetic Products & Technical source also caused one
Sales answer to surface local demo endpoint details.

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
- Dangerous-tool isolation: `PARTIAL` for this client run — Sales and QC terminal requests produced no tool call and a human-readable unavailable-capability response, but the exact `NO_TERMINAL_TOOL` marker was not observed. The deployed employee toolsets remain WeKnora read-only retrieval only.
- Employee client: `PASS WITH LIMITATIONS` — login, assistant visibility, grounded chat, source visibility, follow-up context, conversation persistence, temporary text attachment handling, and direct unauthorized model rejection passed. Source presentation is plain inline text, employee settings expose technical user-level controls, and the synthetic corpus contains local endpoint details that should not be used as production employee knowledge.
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
- The current employee UI did not emit the historical exact `NO_TERMINAL_TOOL`
  marker for Sales/QC terminal probes, although no terminal tool call occurred
  and the Profiles remain configured with read-only WeKnora tools.
- The synthetic Products & Technical document contains local demo endpoint
  details; one grounded Sales response surfaced them. Replace or sanitize the
  demo corpus before production use.
- Open WebUI employee Settings exposes user-level System Prompt and Advanced
  Parameters controls. This is a usability/least-confusion concern, not an
  employee provider or admin credential surface.

## Pending Decisions

- Replace synthetic documents and demo credentials with approved company data and secret management.
- Move a successful backup generation to encrypted independent storage and configure retention/monitoring.
- Decide whether to enable OrbStack's existing login-start setting for a future
  automatic-recovery run, then repeat the reboot test without treating delayed
  CLI-triggered availability as proof of automatic recovery.
- Validate a supported per-user Hermes session-key/header mapping before enabling employee long-term memory.
- Review and pin current upstream releases before any production deployment; decide separately on messaging, Kanban/Cron, and restricted engineering delegation.
