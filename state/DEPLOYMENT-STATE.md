# Enterprise AI Office Deployment State

> Template. Fill this file in a private/company deployment or sanitized reference implementation. Do not commit production secrets.

Last updated: Not deployed
Deployment status: `not-deployed`
Company / environment: `<COMPANY_OR_ENVIRONMENT>`

## Host

| Field | Value |
| --- | --- |
| Host type | `<HOST_TYPE>` |
| OS | `<OS_AND_VERSION>` |
| CPU / architecture | `<CPU>` |
| RAM | `<RAM>` |
| Storage | `<STORAGE>` |
| Hostname | `<HOSTNAME>` |
| LAN / private address strategy | `<NETWORK_STRATEGY>` |

## Container Runtime

| Field | Value |
| --- | --- |
| Runtime | `<DOCKER_OR_OTHER>` |
| Version | `<VERSION>` |
| Startup behavior | `<STARTUP_BEHAVIOR>` |

## WeKnora

| Field | Value |
| --- | --- |
| Version / tag | `<VERSION>` |
| Commit if applicable | `<COMMIT>` |
| Deployment method | `<COMPOSE_OR_OTHER>` |
| Database | `<POSTGRES_VERSION_OR_STACK>` |
| File storage | `<LOCAL_MINIO_S3_OTHER>` |
| Embedding model | `<MODEL>` |
| Embedding dimension | `<DIMENSION>` |
| Rerank model | `<MODEL>` |
| Chat model if used | `<MODEL>` |
| MCP/API bridge | `<METHOD>` |
| Knowledge Bases | `<LIST_OR_LINK>` |

## Hermes Agent

| Field | Value |
| --- | --- |
| Version / release | `<VERSION>` |
| Commit if applicable | `<COMMIT>` |
| Installation | `<HOST_NATIVE_OR_OTHER>` |
| Gateway service | `<STATUS>` |
| API listener | `<INTERNAL_ADDRESS_OR_DESCRIPTION>` |
| Multi-Profile/multiplex | `<ENABLED_DISABLED>` |
| Served Profile allowlist | `<PROFILES>` |
| Default model/provider | `<MODEL_PROVIDER>` |
| Memory provider | `<MEMORY_POLICY_PROVIDER>` |

### Profiles

#### default / admin

- Purpose: `<PURPOSE>`
- Employee exposed: `false`
- Model: `<MODEL>`
- Tools/toolsets: `<SUMMARY>`
- MCP: `<SUMMARY>`
- Credentials boundary: `<SUMMARY>`

#### general

- Purpose: `<PURPOSE>`
- Employee groups: `<GROUPS>`
- Model: `<MODEL>`
- Tools/toolsets: `<SUMMARY>`
- MCP: `<SUMMARY>`
- Memory policy: `<POLICY>`

#### sales

- Status: `<ENABLED_DISABLED_NOT_APPLICABLE>`
- Employee groups: `<GROUPS>`
- Model: `<MODEL>`
- Tools/toolsets: `<SUMMARY>`
- MCP: `<SUMMARY>`
- Memory policy: `<POLICY>`

#### qc

- Status: `<ENABLED_DISABLED_NOT_APPLICABLE>`
- Employee groups: `<GROUPS>`
- Model: `<MODEL>`
- Tools/toolsets: `<SUMMARY>`
- MCP: `<SUMMARY>`
- Memory policy: `<POLICY>`

#### marketing

- Status: `<ENABLED_DISABLED_NOT_APPLICABLE>`
- Employee groups: `<GROUPS>`
- Model: `<MODEL>`
- Tools/toolsets: `<SUMMARY>`
- MCP: `<SUMMARY>`
- Memory policy: `<POLICY>`

#### engineering

- Status: `<ENABLED_DISABLED_NOT_APPLICABLE>`
- Employee groups: `<GROUPS>`
- Model: `<MODEL>`
- Terminal/backend policy: `<SUMMARY>`
- Working directory/repositories: `<SUMMARY>`
- Codex: `<ENABLED_DISABLED>`
- Claude Code: `<ENABLED_DISABLED>`

## Open WebUI

| Field | Value |
| --- | --- |
| Version | `<VERSION>` |
| Deployment method | `<METHOD>` |
| Employee URL / access method | `<PRIVATE_ACCESS_DESCRIPTION>` |
| Authentication | `<METHOD>` |
| Groups | `<GROUPS>` |
| Hermes Profile resources | `<MAPPING>` |
| Long-term memory header/scoping | `<METHOD_OR_DISABLED>` |

## hermes-webui

| Field | Value |
| --- | --- |
| Repository | `<REPOSITORY>` |
| Version / commit | `<VERSION>` |
| Deployment | `<METHOD>` |
| Access boundary | `admin-only` |

## Specialized Coding Agents

| Component | Version / status | Authentication / notes |
| --- | --- | --- |
| Codex | `<VERSION_STATUS>` | `<NON_SECRET_SUMMARY>` |
| Claude Code | `<VERSION_STATUS>` | `<NON_SECRET_SUMMARY>` |

## Messaging

| Field | Value |
| --- | --- |
| Platform | `<FEISHU_WECOM_WEIXIN_OTHER_DISABLED>` |
| Status | `<STATUS>` |
| Authorization method | `<ALLOWLIST_PAIRING_ENTERPRISE_IDENTITY>` |
| Profile routing | `<SUMMARY>` |

## Kanban

- Enabled: `<true_false>`
- Boards: `<LIST>`
- Dispatcher mode: `<MODE>`
- Business-critical workflows: `<SUMMARY>`

## Cron

- Enabled: `<true_false>`
- Business-critical jobs: `<SUMMARY>`
- Model/provider pinning policy: `<SUMMARY>`
- Delivery targets: `<SUMMARY>`

## Backup

| Field | Value |
| --- | --- |
| Schedule | `<SCHEDULE>` |
| Retention | `<RETENTION>` |
| Primary destination | `<DESTINATION_DESCRIPTION>` |
| Off-primary-disk copy | `<YES_NO_DESTINATION>` |
| Secrets recovery method | `<METHOD_WITHOUT_SECRET>` |
| Last successful backup | `<DATE>` |
| Last restore test | `<DATE>` |

## Network Exposure

Document which services are reachable from which networks. Do not record secrets.

```text
Open WebUI: <EXPOSURE>
WeKnora UI: <EXPOSURE>
hermes-webui: <EXPOSURE>
Hermes API: <EXPOSURE>
PostgreSQL: <EXPOSURE>
Redis: <EXPOSURE>
```

## Acceptance Status

Reference `docs/ACCEPTANCE-TESTS.md`.

- Functional: `<PASS_FAIL_NOT_RUN>`
- RBAC: `<PASS_FAIL_NOT_RUN>`
- Profile key isolation: `<PASS_FAIL_NOT_RUN>`
- Memory isolation: `<PASS_FAIL_DISABLED_NOT_RUN>`
- Dangerous-tool isolation: `<PASS_FAIL_NOT_RUN>`
- Backup restore: `<PASS_FAIL_NOT_RUN>`
- Reboot recovery: `<PASS_FAIL_NOT_RUN>`

## Known Issues / Limitations

- `<ISSUE_OR_NONE>`

## Pending Decisions

- `<DECISION_OR_NONE>`
