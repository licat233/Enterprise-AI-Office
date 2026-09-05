# Enterprise AI Office Deployment State

> Sanitized local-demo record. Secrets, tokens, passwords, and host identifiers are intentionally omitted.

Last updated: 2026-09-05
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
| Host reboot rehearsal | Not executed; exact post-reboot continuation is documented in `docs/BACKUP-RESTORE.md` |

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

## Acceptance Status

Reference `docs/ACCEPTANCE-TESTS.md`.

- Functional: `PASS` — WeKnora app/document reader/PostgreSQL health checks, Redis authenticated `PING`, frontend/API liveness, Open WebUI health, both KB ingestions, direct Profile answers, grounded employee chats, and citations/source titles all passed.
- RBAC: `PASS` — group membership and employee model visibility verified; unauthorized direct chat attempts returned HTTP 400 `Model not found` for the other department's model.
- Profile key isolation: `PASS` — each employee Profile key returned HTTP 200 only for its own route and HTTP 401 for the other two routes.
- Memory isolation: `DISABLED` — employee Hermes long-term memory is deliberately off; no cross-user memory channel is enabled.
- Dangerous-tool isolation: `PASS` — Sales and QC terminal escape probes returned `NO_TERMINAL_TOOL`; employee toolsets are WeKnora read-only retrieval only.
- Backup restore: `PASS` — native backup artifacts passed checksums; an isolated restore recovered WeKnora PostgreSQL/Knowledge Bases, Open WebUI state, Hermes Profiles/configuration, and representative grounded access.
- Reboot recovery: `REBOOT RECOVERY NOT YET EXECUTED` — no host reboot was performed; startup configuration and exact continuation checks are documented only.

## Known Issues / Limitations

- This is a local synthetic demonstration, not a production deployment.
- The initial OpenAI model configuration was quota-exhausted during ingestion, so the validated demo uses the protected DashScope Qwen model configuration. Replace it with an approved production provider before rollout.
- The scoped WeKnora viewer key supports retrieval from the two demo KBs. `list_shared_knowledge_bases` correctly returns 403 because that endpoint is outside the key's `retrieve` capability/scope.
- Hermes v0.21.0 multiplex registration is name-sensitive; the employee MCP servers intentionally use unique names (`weknora_general`, `weknora_sales`, `weknora_qc`) so each Profile receives its own read-only tool scope.
- Hermes emits an unsandboxed/network-access warning because the local process binds `0.0.0.0`; keep the host firewall and loopback-only UI bindings in place.
- Backup generations and secrets currently remain on the same Mac; no encrypted independent copy or retention schedule has been configured.
- Mac/OrbStack reboot recovery is not yet evidenced by a post-reboot run.

## Pending Decisions

- Replace synthetic documents and demo credentials with approved company data and secret management.
- Move a successful backup generation to encrypted independent storage and configure retention/monitoring.
- Execute the documented Mac/OrbStack reboot recovery rehearsal and record the post-reboot checks.
- Validate a supported per-user Hermes session-key/header mapping before enabling employee long-term memory.
- Review and pin current upstream releases before any production deployment; decide separately on messaging, Kanban/Cron, and restricted engineering delegation.
