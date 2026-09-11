# MCP Control Plane — ARMOR Phase 4A

Status: inventory and acceptance contract; no new employee exposure.

This document records the Enterprise-side replacement boundary for the five
MCP definitions identified during the ARMOR capability migration. The registry
is not a credential store and does not assert that a server is installed or
healthy.

## Status vocabulary

- MIGRATED: the definition and an approved Enterprise runtime binding exist.
- PREPARED: the definition and safe logical binding are recorded; runtime
  installation or host rebinding remains open.
- PREPARED_REPLACEMENT_REQUIRED: the legacy definition is recorded, but the
  mixed-risk or machine-specific behavior must be replaced by an Enterprise
  adapter before activation.
- ENABLED: a named Profile is explicitly allowed to use the server.
- HEALTHY: the enabled runtime has passed its current health and acceptance
  checks.

## Registry state

| Definition | Classification | Runtime state | Employee exposure | Logical credentials |
|---|---|---|---|---|
| anysearch | OPERATIONS_READ | PREPARED | none | ANYSEARCH_API_KEY |
| firecrawl-mcp | OPERATIONS_EXTERNAL_WRITE | PREPARED_REPLACEMENT_REQUIRED | none | FIRECRAWL_API_KEY |
| obscura | MACHINE_SPECIFIC_REBIND | PREPARED | none | none recorded |
| paddle_ocr | MACHINE_SPECIFIC_REBIND | PREPARED | none | EAIO_PADDLE_OCR_PYTHON, EAIO_PADDLE_OCR_SERVER |
| toolscout | ADMIN_CONTROL_PLANE | PREPARED | admin/engineering reserved, not active | TOOLSCOUT_AGENT_NAME, TOOLSCOUT_MEMORY_HOME |

All five definitions are present in config/mcp-registry.yaml. All five have
health NOT_RUN because Phase 4A does not install, probe, or enable a runtime.

## Profile boundary

The Operations Profile remains WeKnora-only. The registry does not add any
server to its allowlist, and employee exposure remains disabled by default.
Any future exposure requires an explicit business purpose, tool allowlist,
protected credential reference, host/runtime binding, health result, and
acceptance evidence.

Anysearch is reserved for a future read-only research lane. Firecrawl must be
split into a read adapter and a separately approved privileged lane; the
legacy mixed server is not an Operations dependency. Obscura requires an
isolated Enterprise browser-session worker and may not consume personal Chrome
state. Paddle OCR must bind to an Enterprise media runtime or adapter, not a
personal virtual environment. Toolscout belongs to the admin/control-plane or
engineering boundary with a separate agent identity and memory home.

## Secret and health policy

Only logical environment-variable names are recorded. Secret values, cookies,
sessions, personal browser profiles, and personal runtime paths are not
copied. Live probes remain disabled until the corresponding Enterprise
runtime and approval boundary exist.
