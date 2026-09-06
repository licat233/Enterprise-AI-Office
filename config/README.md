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
