# Company Configuration

This directory defines the reusable declarative boundary for an Enterprise AI Office deployment.

For v2 Installation Design, the normative protected-input contract is:

```text
docs/V2-CONFIG-PROTECTED-INPUTS.md
```

## Configuration files

```text
config/
├── company.example.yaml           # public reusable desired-state schema/default posture
├── company.private.example.yaml   # synthetic shape for company-private non-secret overlay
├── capabilities.yaml              # capability implementation/input/acceptance closure
├── mcp-registry.yaml              # Enterprise MCP control-plane definitions and boundaries
├── validated-stack.yaml           # validated core reproducibility baseline
└── .env.example                   # runtime binding placeholder template, not desired-state authority
```

A real checkout-based adopter may use:

```text
private/company.yaml
```

for deployment-private, non-secret desired state. The repository already ignores `private/`.

Actual secret values remain outside both YAML files.

---

## 1. Three-layer desired-input model

Keep these classes separate:

```text
A. Public blueprint
   → config/company.example.yaml
   → config/capabilities.yaml
   → reusable templates/contracts

B. Company-private non-secret desired state
   → private/company.yaml or equivalent protected private config

C. Protected secrets
   → external protected storage / native credential mechanism
   → referenced symbolically from private configuration
```

Observed runtime state is a fourth, output-side class:

```text
D. Runtime truth
   → actual runtime + deployment-specific state record
```

Do not collapse B and C into one `.env`, and do not treat D as desired-state authority.

---

## 2. `company.example.yaml`

Schema v2 describes reusable deployment intent, including:

- company identity/language/timezone;
- target readiness (`core-ready`, `configured-ready`, or `production-ready`);
- Core network desired state for the existing WeKnora → Hermes → Open WebUI paths;
- Core provisioning bootstrap identities and symbolic secret-reference slots;
- Knowledge Base structure;
- Hermes Profiles;
- employee groups/permissions;
- model roles;
- enabled/disabled optional capabilities;
- v2 Email mailbox/grant shape;
- production control intent;
- secret classes/references, never values.

It is intentionally synthetic and contains no production secrets.

### Baseline

The reusable baseline remains deliberately small:

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

Specialist Profiles, department groups, extra Knowledge Bases, Email, hermes-webui, coding delegation, Kanban, Cron, messaging, remote access, SSO, and employee long-term memory are opt-in.

Templates/playbooks are a capability library, not a deployment checklist.

---

## 3. `company.private.example.yaml`

This file is a **public synthetic shape example** for the private overlay. It may safely contain `example.invalid` addresses and fictional group/mailbox IDs.

A real private overlay may contain non-secret but private values such as:

```text
real employee/group identifiers
selected mailbox addresses/logical IDs
mailbox business purpose
mailbox grants
allowed folders
selected communication Profile
private host/runtime paths
provider endpoint mode
controlled test recipients
backup destinations
symbolic secret references
```

Do not place actual secret values in the private overlay.

For Core, private non-secret network routes belong under `core_network` rather
than ad-hoc fields. The public schema defines the shape; the private overlay
resolves the real WeKnora API route used by Hermes, Hermes listener/backend
route, and Open WebUI employee URL/access layer.

The reusable exposure default is: Open WebUI is employee-facing; WeKnora and
Hermes are not directly employee-exposed. A different exposure pattern is an
explicit deployment/security decision, not a value to infer from the ARMOR
reference instance.

For Core, the private overlay also resolves the non-secret bootstrap identity
and stable symbolic secret refs under `core_provisioning`. The current
validated bindings include WeKnora `DB_PASSWORD`, `REDIS_PASSWORD`, and
`JWT_SECRET`; Hermes Profile-local `API_SERVER_KEY`; and the Open WebUI
bootstrap admin password provisioning input.

`config/.env.example` is only a runtime binding shape. It is not a competing
secret authority: values must be resolved from the active symbolic refs /
protected storage.

### Runtime binding taxonomy

Do not assume every variable shown in `config/.env.example` is read directly
by an upstream component.

The template intentionally contains four classes:

| Class | Examples | Consumer / meaning |
| --- | --- | --- |
| EAO/operator metadata | `EAIO_ENVIRONMENT`, `EAIO_COMPANY_ID`, `EAIO_TIMEZONE` | Selected EAO/operator tooling only; not universal upstream env |
| EAO helper inputs | `OPEN_WEBUI_HEALTH_URL`, `EAIO_BACKUP_SUCCESS_MARKER` | Repository scripts such as `scripts/health-check.sh` |
| Provisioning convenience aliases | `OPEN_WEBUI_ADMIN_PASSWORD`, `HERMES_DEFAULT_API_KEY`, `HERMES_GENERAL_API_KEY` | Inputs to the EAO provisioning/operator flow; must be translated to the component's real API/request/Profile binding |
| Upstream/adapter-native env | WeKnora `DB_PASSWORD` / `REDIS_PASSWORD` / `JWT_SECRET`, Open WebUI OIDC vars, enabled capability-specific vars | Exact names consumed by the selected pinned upstream/runtime or EAO adapter |

For Hermes specifically, the upstream runtime consumes Profile-local
`API_SERVER_KEY`; `HERMES_DEFAULT_API_KEY` and
`HERMES_GENERAL_API_KEY` are not Hermes-native variable names.

The generic Open WebUI health URL uses the checked-in loopback Compose default
(`127.0.0.1:3000`). A reference deployment may deliberately publish another
approved private host port. Health tooling must use observed target runtime
state, not inherit a reference deployment's port.

The private overlay is reconciled by stable logical IDs for named resources such as Profiles, groups, mailboxes, and grants; do not blindly concatenate arrays.

---

## 4. `config/capabilities.yaml`

This is the machine-readable capability closure registry.

For each optional capability it points a deployment agent to relevant:

```text
implementation playbook/adapter
required company-private inputs
required secret classes
protected-input contract where applicable
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

### `config/mcp-registry.yaml`

This is the Enterprise control-plane inventory for MCP definitions. It records
transport, runtime rebinding requirements, logical environment names, risk
classification, profile scope, default exposure, and health-check strategy.

Its **definition/boundary layer is reusable**, while the current `runtime` and
`health` fields are a sanitized snapshot of the ARMOR reference implementation
at the recorded review date. A fresh deployment must recompute `installed`,
`configured`, `enabled`, and health from the target host; it must not inherit
those reference flags merely because they are present in Git.

Definitions may exist in the inventory while their runtime and employee
exposure remain disabled. Runtime availability and Profile exposure are separate
dimensions; for example, an upstream package may be installed while raw employee
exposure remains forbidden.

The registry is not a secret store and is not a request to start a server.
Actual Profile exposure remains controlled by the Profile configuration and
must be explicitly allowlisted.

Company desired state uses `mcp_control_plane.profile_allowlists`, keyed by an
actually declared Profile ID. The reusable baseline therefore contains only
`general: [weknora]`; a private communication example contains
`communication: [weknora]`. Do not predeclare an `operations` allowlist when
no Operations Profile exists in the active company configuration.

The reusable baseline does not require an `operations` Profile at all. In the
sanitized ARMOR reference implementation, Operations has later approved/frozen
capabilities beyond WeKnora retrieval: the bounded Enterprise Web Research
adapter, ToolScout, and the scoped ARMOR Vault Router. That reference allowlist
is recorded in `config/mcp-registry.yaml` and
`docs/ENTERPRISE-OPERATIONS-V1.0-ACCEPTANCE.md`.

A fresh deployment must derive its own Operations/specialist exposure from the
active company configuration and enabled capability contracts. It must not copy
the ARMOR reference allowlist merely because those runtime flags exist in Git.

Capability selection should be machine-resolvable whenever the reusable company
schema has a typed field. For example, Enterprise Web Research is selected by
`capabilities.enterprise_web_research.enabled == true`.

ARMOR-specific workflow entries may instead declare
`selection.scope: ARMOR_reference_specific` and point to the sanitized ARMOR
reference index. Their presence in the capability library does not create a
generic company-schema field or enable them for another company.

An enabled capability must be implemented and accepted before `CONFIGURED READY` can be claimed. A disabled capability must not be instantiated merely because its playbook exists and does not require unused conditional secrets.

### Operational integrations

When an enabled integration exposes governed reads/writes, its closure must resolve:

```text
business purpose
selected provider/upstream
System-of-Record / Authority boundary
trusted human/service identity path
Profile/tool/credential scope
Object visibility/read authorization
Named Actions and preconditions
approval semantics
write/idempotency/reconciliation behavior
required private inputs
required secret classes
acceptance tests
state/audit evidence
```

Do not predeclare or enable generic CRM/ERP/workflow integration merely for theoretical completeness.

---

## 5. `config/validated-stack.yaml`

### Single machine-readable Core version authority

`config/validated-stack.yaml` is the only machine-readable authority for the
validated Core host baseline, component versions, upstream commits, and
deployment mode. Other machine-readable files may point to it, but must not
copy those version/host/runtime values.

Human-facing documentation may summarize the current baseline when useful, but
must identify `config/validated-stack.yaml` as the authoritative source and
must not be treated as a second version policy.

The stack file separates two dates:

- `first_validated_on` — when the baseline first completed reference
  qualification;
- `reference_runtime_last_confirmed_on` — when the same versions were last
  observed in the current sanitized reference runtime.

The second date is **not** a substitute for a new clean-host qualification.
Upgrade/requalification remains governed by `docs/UPGRADE.md`.

Each Core component also records its validated upstream repository and
acquisition method. These fields answer a separate reproducibility question:
"where does a fresh Agent obtain this exact runtime?" They are part of the
validated-stack authority, not convenience links.

The current baseline deliberately distinguishes:

- tag-backed components (WeKnora and Open WebUI), whose tag→commit mapping was
  verified;
- Hermes Agent, whose `0.21.0` package version is verified in
  `pyproject.toml` at the pinned commit and is installed through the official
  installer fetched from that same commit.

See `DEPLOY.md §4.1` for the deterministic acquisition procedure.


This records the first validated core stack and baseline feature flags in machine-readable form.

It is a reproducibility baseline, not a permanent version policy. Use `docs/UPGRADE.md` when qualifying newer versions.

Optional components not present in the first validated core demo must resolve and record their own compatible version/commit when enabled.

---

## 6. Runtime `.env.example` files

`config/.env.example` and component-specific `.env.example` files are **binding templates**, not competing desired-state stores.

A future installer should conceptually do:

```text
private desired non-secret value
+
protected secret value
        ↓
render/inject the minimum native runtime variables expected by that component
```

Example for Tencent read-only Email:

```text
mailbox address / allowed folders / host / port
→ private desired state

mailbox client password
→ protected secret

adapter runtime
→ EAIO_EMAIL_USERNAME / EAIO_EMAIL_ALLOWED_FOLDERS / ...
```

Do not maintain independent hand-edited copies of the same authorization policy across YAML and `.env` files.

---

## 7. Secret references

A private overlay may define symbolic references such as:

```yaml
secret_refs:
  email-sales-mailbox-client-password:
    class: email-mailbox-client-credential
    consumer: eao-email-governance
    native_binding: EAIO_EMAIL_CLIENT_PASSWORD
```

This records what must be resolved and where it will be injected. It never contains the actual password/token/key.

The blueprint does not mandate a new secret platform. Use the smallest approved native/protected mechanism appropriate to the selected deployment.

---

## 8. Missing/conflicting input behavior

For an enabled capability:

```text
missing private/business input
→ BLOCKED — REQUIRED INPUT: <specific input>

missing secret
→ BLOCKED — REQUIRED INPUT: secret <symbolic-ref>

contradictory desired state
→ BLOCKED — CONFIG CONFLICT: <specific conflict>

frozen security invariant violated
→ FAIL — SECURITY CONTRACT VIOLATION: <invariant>
```

Do not guess, invent a provider, broaden a credential, or silently disable the configured capability.

Unresolved `<PLACEHOLDER>` values in an active required field count as missing input.

---

## 9. Schema vs installer

The YAML files are declarative intent for humans and capable AI Engineering Agents. They are not a claim that a universal compiler exists.

The execution contract remains:

```text
AGENTS.md
→ DEPLOY.md
→ public schema + active private company config
→ config/capabilities.yaml
→ protected secret resolution
→ upstream-native adapters/playbooks
→ acceptance
→ deployment state
```

Do not pretend a parser/compiler exists when it does not.

---

## 10. Public/private data boundary

Do not commit publicly:

- real credentials/tokens/passwords;
- real employee lists/identifiers unless intentionally public;
- private customer data;
- sensitive mailbox/address mappings;
- private network details that create risk;
- production `.env` files;
- secret-bearing deployment-state records.

Synthetic examples use domains such as `example.invalid` and fictional IDs.

---

## 11. Configuration precedence

Conceptually:

```text
Frozen architecture / security contracts
        ↓
Capability registry
        ↓
Public reusable company schema/default posture
        ↓
Company-private non-secret desired state
        ↓
Protected secret resolution
        ↓
Actual runtime reconciliation
```

Private configuration may select company-specific values but may not silently override a frozen architecture/security invariant such as v2 customer-facing human approval.

Company differences belong primarily in configuration rather than generic architecture forks.
