# Hermes Agent Deployment Adapter

Hermes Agent is the primary Agent runtime for Enterprise AI Office.

This directory contains tested Enterprise AI Office configuration/compatibility guidance layered on top of a pinned Hermes release.

For deployment execution, follow `DEPLOY.md` first.

## Baseline configuration artifacts

For the validated Core Ready path, use these as the starting point rather than rebuilding the baseline from prose:

```text
infrastructure/hermes/
├── default.config.example.yaml
├── default.env.example
├── general.config.example.yaml
└── general.env.example
```

They encode the verified configuration shape for:

- default/admin as the multiplex control plane;
- an explicit served-Profile allowlist;
- `general` as the baseline employee Profile;
- Profile-scoped API credentials;
- employee long-term memory disabled;
- WeKnora MCP integration;
- an API-server toolset restricted to the read-only WeKnora MCP surface.

Replace placeholders with protected deployment values. Recheck the pinned Hermes/WeKnora upstream documentation if the validated versions change.

## Default posture

The validated macOS path keeps Hermes host-native.

The baseline Profile model is:

```text
default / admin   # privileged control plane
general           # baseline employee-facing assistant
```

The default/admin Profile must not be exposed as a normal employee assistant.

Specialist Profiles are optional and are created only when the adopting company's configuration requires a distinct role, knowledge boundary, tool/credential boundary, automation owner, model/memory policy, or risk boundary.

Templates under `profiles/` are a library, not a provisioning list.

## Core capabilities used by the baseline

- Profiles;
- SOUL;
- Skills/external Skill directories as needed;
- MCP;
- employee Profile API;
- explicit served Profile allowlisting where supported.

Kanban, Cron, Bot Mode, messaging Gateway, Codex, Claude Code, and stronger host tools are enabled only when required.

## Multi-Profile API

Use the currently supported Hermes Profile routing/multiplex mechanism.

For every employee-facing Profile:

- use a unique API credential;
- serve only explicitly approved Profiles where allowlisting is supported;
- keep privileged/default routes out of the employee client;
- keep the API on the smallest trusted network boundary that still allows the selected client runtime to reach it.

With the validated multiplex model, the default Profile owns the port-binding API server and named employee routes use `/p/<profile>/...`; the named Profile keeps its own `API_SERVER_KEY` secret scope.

If multiple employee Profiles are enabled, run the complete cross-Profile credential matrix from `docs/ACCEPTANCE-TESTS.md`.

## Knowledge bridge

Register WeKnora through supported MCP/API configuration.

The baseline `general` template launches the pinned WeKnora MCP server over stdio and uses a `tools.include` whitelist so the employee API surface receives only approved read-only retrieval operations.

Do not couple Hermes directly to WeKnora's database schema for normal retrieval.

## Skills

Use upstream bundled Skills where appropriate and company-owned Skills through supported external Skill directories.

Do not copy common company Skills into every Profile without a real reason.

Authoritative company facts belong in WeKnora rather than SOUL/Profile memory.

## Tools

Normal employee Profiles default to least privilege.

Do not grant arbitrary terminal, filesystem write, Docker, host administration, GitHub administration, raw credentials, or coding-agent delegation unless the role's actual work requires those capabilities and the workspace/credential boundary is explicit.

Profile state isolation is not the same as host sandboxing.

## Memory

Employee long-term memory is disabled by default until the deployed Open WebUI → Hermes user/session mapping passes the cross-user isolation test.

Open WebUI conversation history can remain enabled independently.

Shared Profile memory must not accumulate employee-private data.

## Optional technical workers

If a technical Profile is enabled, test Codex and/or Claude Code independently under the actual long-lived Hermes service account before enabling delegation.

Use a disposable repository first and verify repository-local instructions, PATH, authentication, working directory, and credential scope.

## Optional Kanban / Cron / messaging

Enable these only when company configuration requires them.

Run the corresponding conditional acceptance tests after enabling them.

## Validation

Baseline Core Ready requires:

- Hermes health;
- `general` Profile served;
- grounded WeKnora access with source evidence;
- employee Profile API credential boundary;
- default/admin non-exposure;
- least-privilege employee tools;
- deliberate employee-memory disablement or proven isolation.

See `DEPLOY.md` and `docs/ACCEPTANCE-TESTS.md`.
