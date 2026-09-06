# Hermes Agent Deployment Adapter

Hermes Agent is the primary Agent runtime for Enterprise AI Office.

For deployment execution, follow `DEPLOY.md`, the active company configuration, and `config/capabilities.yaml` first.

## Baseline configuration artifacts

For the validated core path:

```text
infrastructure/hermes/
├── default.config.example.yaml
├── default.env.example
├── general.config.example.yaml
├── general.env.example
├── specialist.config.example.yaml
├── specialist.env.example
└── features/
    └── README.md
```

The first four artifacts encode the baseline:

- default/admin as privileged control plane;
- explicit served-Profile allowlisting;
- `general` as baseline employee Profile;
- distinct Profile API credentials;
- employee long-term memory disabled;
- WeKnora MCP integration;
- API tool exposure restricted to the approved read-only WeKnora surface.

The specialist templates are generic starting points only when company configuration enables a real specialist Profile. They are not a list of Profiles to provision.

`features/README.md` covers the optional native Hermes Kanban, Cron, and messaging capabilities selected through the capability registry.

## Default posture

Validated macOS reference:

```text
default/admin  → privileged control plane
general        → baseline employee Assistant
```

The default/admin Profile is never an ordinary employee Assistant.

Specialist Profiles are opt-in. For each enabled specialist, define the purpose, SOUL, employee groups, Knowledge Base scope, tools, credentials, model policy, memory policy, and risk boundary before exposing it.

## Multi-Profile API

Use the supported Hermes Profile routing/multiplex mechanism for the selected version.

For every employee-facing Profile:

- use a unique API credential;
- serve only explicitly approved Profiles where allowlisting is supported;
- keep default/admin out of the employee client;
- keep the API on the smallest trusted network boundary that still supports the selected client.

In the validated Hermes reference, the default Profile owns the port-binding API server and named employee routes use `/p/<profile>/...`; each named Profile keeps its own API key secret scope.

When multiple employee Profiles are enabled, run the pairwise credential/access tests in `docs/ACCEPTANCE-TESTS.md`.

## Knowledge bridge

Register WeKnora through supported MCP/API configuration.

The baseline `general` template launches the selected WeKnora MCP server over stdio and uses a `tools.include` whitelist so the employee API surface receives only approved read-only retrieval operations.

Use distinct MCP server names/configuration where the selected Hermes multiplex implementation requires Profile-scoped registration.

Do not couple ordinary knowledge retrieval to WeKnora's internal database schema.

## Skills

Use upstream bundled Skills where appropriate and company-owned Skills through supported external Skill directories.

Authoritative company facts belong in WeKnora rather than SOUL or Skill prose.

Do not copy all shared Skills into every Profile merely because they exist.

## Tools and privileged technical roles

Normal employee Profiles default to least privilege.

Do not grant arbitrary terminal, filesystem write, Docker/system administration, GitHub administration, raw credentials, or coding-agent delegation unless the role's actual work requires them.

When coding delegation is enabled, follow `infrastructure/coding-agents/README.md` and define explicit repository/workspace plus credential boundaries.

Profile state isolation is not host sandboxing.

## Memory

Employee Hermes long-term memory remains disabled unless the configured Open WebUI → Hermes user/session-scoping path passes the cross-user isolation acceptance test.

Open WebUI conversation history is independent.

## Native optional features

When company configuration enables Kanban, Cron, or messaging, use `infrastructure/hermes/features/README.md` and the selected Hermes release's official implementation.

Do not add a separate workflow/scheduler/messaging framework when the built-in Hermes capability meets the configured requirement.

## Validation

Core Hermes acceptance includes:

- runtime/Gateway health;
- `general` served;
- grounded WeKnora access with source evidence;
- employee Profile API credential boundary;
- default/admin non-exposure;
- least-privilege employee tools;
- deliberate employee-memory disablement or proven isolation.

Every enabled specialist/native optional capability adds its corresponding conditional acceptance before `CONFIGURED READY` may be claimed.
