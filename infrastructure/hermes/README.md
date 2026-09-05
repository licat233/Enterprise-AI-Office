# Hermes Agent Deployment Adapter

Hermes Agent is the primary Agent runtime for Enterprise AI Office.

This directory is reserved for tested Enterprise AI Office configuration/compatibility notes layered on top of a pinned Hermes release.

## Default posture

Reference deployment keeps Hermes host-native initially so restricted engineering Profiles can use controlled access to:

- local repositories;
- Git / GitHub CLI;
- Codex;
- Claude Code;
- approved host tools.

Do not containerize Hermes merely to make all components look uniform if that complicates real work execution.

## Core capabilities used by Enterprise AI Office

- Profiles;
- SOUL;
- Skills and external Skill directories;
- MCP;
- API server;
- multi-Profile/multiplex Gateway when appropriate;
- Kanban;
- Cron;
- Bot Mode / role management;
- messaging Gateway;
- Codex / Claude Code integration.

## Production Profile model

Create only Profiles justified by real roles.

A reference company may use:

```text
default / admin
general
sales
qc
marketing
engineering
```

The default/admin Profile is privileged and must not be exposed as a normal employee assistant.

## Multi-Profile API

Use the currently supported Hermes Profile routing/multiplex mechanism.

Configure:

- explicit served Profile allowlist where available;
- unique API key per employee-facing Profile;
- internal-only API listener exposure;
- correct Profile routing.

Run cross-Profile credential tests before production.

## Skills

Use upstream bundled Skills where appropriate and company-owned Skills from `skills/` via supported external Skill directory configuration.

Do not copy common company Skills into every Profile unless there is a real reason.

## Tools

Business Profiles should default to least privilege.

Engineering may receive stronger tools only under explicit workspace/repository and credential policies.

Remember that Profile state isolation is not the same as host sandboxing.

## Knowledge bridge

Register WeKnora through supported MCP/API configuration.

Prefer direct knowledge retrieval tools for straightforward queries.

## Memory

Do not enable employee user-scoped long-term memory until the deployed client/Session-Key/memory-provider path passes isolation testing.

Shared Profile memory must not accumulate employee-private data.

## Kanban and Cron

Use Kanban for durable multi-agent work and Cron for scheduled automation.

Do not treat either as a per-user employee permission system unless separately validated/designed.

## Coding workers

Test Codex and Claude Code independently under the host service account, then test Hermes delegation in a disposable repository.

Check PATH/auth behavior under the actual long-lived Gateway/service environment, not only an interactive terminal.

## Validation

Run the Hermes, Profile isolation, tool restriction, Codex/Claude Code, Kanban, Cron, messaging, and reboot sections in `docs/ACCEPTANCE-TESTS.md`.
