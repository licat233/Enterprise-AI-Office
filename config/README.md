# Company Configuration

This directory defines the reusable declarative boundary for an Enterprise AI Office deployment.

## Configuration files

```text
config/
├── company.example.yaml   # what the adopting company wants built
├── capabilities.yaml      # how enabled capabilities close implementation + acceptance
├── validated-stack.yaml   # first validated core reproducibility baseline
└── .env.example           # non-secret deployment environment placeholders
```

## `company.example.yaml`

Schema v2 describes deployment intent, including:

- company identity/language/timezone;
- target readiness (`core-ready`, `configured-ready`, or `production-ready`);
- Knowledge Base structure;
- Hermes Profiles;
- employee groups/permissions;
- model roles;
- enabled/disabled optional capabilities;
- production control intent;
- secret references/placeholders.

It contains no production secrets.

### Baseline

The reusable baseline is deliberately small:

```text
Hermes control plane
└── default/admin

Employee plane
├── general
├── all-employees
└── ai-admins

Knowledge
└── company-defined shared Knowledge Base(s)
```

Specialist Profiles, department groups, extra Knowledge Bases, hermes-webui, coding delegation, Kanban, Cron, messaging, remote access, SSO, and employee long-term memory are opt-in.

Templates/playbooks are a capability library, not a deployment checklist.

## `config/capabilities.yaml`

This is the machine-readable capability closure registry.

For each optional capability it points a deployment agent to the relevant:

```text
implementation playbook/adapter
required company/external inputs
acceptance test
state fields to record
```

The deployment agent combines:

```text
active company configuration
+
capability registry
        ↓
exact target state
```

An enabled capability must be implemented and accepted before `CONFIGURED READY` can be claimed. A disabled capability must not be instantiated merely because its playbook exists.

## `config/validated-stack.yaml`

This records the first validated core stack and baseline feature flags in machine-readable form.

It is a reproducibility baseline, not a permanent version policy. Use `docs/UPGRADE.md` when qualifying newer versions.

Optional components not present in the first validated core demo must resolve and record their own exact compatible version/commit when enabled.

## Schema vs installer

The company YAML is declarative intent for humans and capable AI engineering agents. It is not a claim that a single universal installer/compiler exists.

The repository's deployment mechanism is the agent execution contract:

```text
AGENTS.md
→ DEPLOY.md
→ company config + capabilities registry
→ upstream-native adapters/playbooks
→ acceptance
→ deployment state
```

Do not pretend a parser/compiler exists when it does not. A capable deployment agent is expected to read the declarative target and execute the referenced implementation paths.

## Protected company overlay

A real adopter should keep company-private deployment values in a private repository or protected deployment location.

Do not commit publicly:

- real employee lists;
- private network details that create risk;
- API/model keys;
- bot/OAuth secrets;
- database passwords;
- private documents/customer data;
- production `.env` values.

## `config/.env.example`

This contains non-secret placeholders used by local adapters/scripts. Copy/adapt it only to a protected untracked location.

Conditional secrets should exist only when their capability is enabled.

## Configuration precedence

Conceptually:

```text
Generic architecture / standards / capability registry
        ↓
Company configuration
        ↓
Environment-specific protected configuration
        ↓
Protected secrets / external authority
        ↓
Actual runtime state
```

Desired state comes from active company configuration. Actual state is recorded in `state/DEPLOYMENT-STATE.md` and must match runtime reality.

## Architecture boundary

Company differences belong primarily in configuration rather than generic architecture forks.

Change the reusable architecture only when the underlying reusable system model or security boundary genuinely changes.
