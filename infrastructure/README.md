# Infrastructure

This directory contains reusable deployment adapters and capability playbooks for Enterprise AI Office.

The repository intentionally does **not** vendor entire upstream projects. It pins/inspects upstream software and keeps only the smallest reusable Enterprise AI Office integration layer needed to reach the configured deployment state.

## Directory map

```text
infrastructure/
├── weknora/          # enterprise knowledge platform adapter
├── hermes/           # core Hermes Profile/MCP config + native feature playbook
│   └── features/     # Kanban, Cron, messaging Gateway
├── open-webui/       # employee Web client adapter
├── hermes-webui/     # optional Hermes administrative Web UI playbook
├── coding-agents/    # optional Codex / Claude Code delegation playbook
└── access/           # optional remote/private access and SSO playbook
```

Which directories are executed is determined by the active company configuration and `config/capabilities.yaml`.

A playbook existing here does not mean its capability should be deployed.

## Capability closure

For deployment, use:

```text
company configuration
+
config/capabilities.yaml
        ↓
selected infrastructure playbooks/adapters
        ↓
acceptance tests
        ↓
deployment state
```

Every enabled capability must have a referenced implementation path and matching acceptance test before `CONFIGURED READY` can be claimed.

## Upstream-version rule

Infrastructure files must target a known upstream version/commit rather than silently assume today's `main`/`latest`.

Before activating or changing an adapter/playbook:

1. identify the selected upstream version;
2. read that version's official deployment/configuration documentation or source;
3. prefer its native feature/integration mechanism;
4. apply the smallest Enterprise AI Office configuration layer;
5. validate the capability;
6. record the actual version and runtime boundary in `state/DEPLOYMENT-STATE.md`.

The validated core stack is recorded in `config/validated-stack.yaml`.

Optional components that were not part of that first core validation must resolve and pin their own compatible upstream version when enabled.

## Why not vendor upstream projects?

Vendoring full upstream Compose/config trees creates a stale fork and makes future agents unsure which project is authoritative.

Preferred pattern:

```text
pinned upstream release/commit
+
thin Enterprise AI Office adapter/playbook
+
company-specific protected configuration
+
recorded runtime state
```

## Secrets

Infrastructure examples contain placeholders only.

Never commit production `.env` values, API keys, database passwords, OAuth secrets, messaging tokens, or private credentials.

## Port/network rules

Do not publish internal databases, queues, parser services, privileged Hermes APIs, or admin surfaces merely because an upstream development example exposes them.

Exposure follows the company configuration, `docs/SECURITY.md`, and `infrastructure/access/README.md` when remote access is enabled.

## Promotion rule

A generic adapter should be based on official supported behavior and reusable configuration, not a one-off workaround.

When an optional capability has not yet been validated in the first reference deployment, label that fact honestly and validate the exact selected upstream behavior during the real deployment. A documented playbook is an execution path, not fabricated validation evidence.
