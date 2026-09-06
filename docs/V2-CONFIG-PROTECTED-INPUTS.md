# Enterprise AI Office v2 — Configuration & Protected Input Contract

Status: ID-2 frozen / real deployment not authorized
Version: 1.0
Date: 2026-09-06

This document closes `ID-2 — Company configuration and protected-input contract` for Enterprise AI Office v2 Installation Design.

It defines how a future AI Engineering Agent separates reusable public blueprint configuration, company-private non-secret desired state, secret values, and observed runtime state.

It does **not** authorize use of real credentials, real employee identities, a real mailbox, or a real deployment target.

Use with:

- `state/PROJECT-PHASE.yaml`
- `docs/V2-INSTALLATION-ARCHITECTURE.md`
- `docs/V2-IMPLEMENTATION-PLAN.md`
- `config/company.example.yaml`
- `config/company.private.example.yaml`
- `config/capabilities.yaml`
- `config/.env.example`
- provider/component-specific `.env.example` and provisioning playbooks

---

## 1. Objective

A fresh installer must be able to determine, without guessing:

```text
what is reusable public blueprint data
what is company-private but non-secret desired state
what is a secret/credential
which enabled capability requires each input
which component consumes each secret
which native environment/file/credential binding receives it
what to do when an input is missing or contradictory
what may be recorded after deployment
```

The blueprint deliberately does not introduce a new secrets manager or configuration compiler.

---

## 2. Four information classes

### Class A — Public blueprint contract

Authority:

```text
public repository
```

Examples:

```text
architecture invariants
capability definitions
supported configuration shape
synthetic defaults/examples
validated stack versions
installation/acceptance paths
secret classes and expected native binding names
```

Representative files:

```text
config/company.example.yaml
config/capabilities.yaml
config/validated-stack.yaml
config/company.private.example.yaml   # shape only; values synthetic
component *.env.example files         # binding templates only
```

Public artifacts must not contain real credentials, real employee identifiers, or private customer/business data.

### Class B — Company-private non-secret desired state

Authority:

```text
active company-private configuration overlay
```

Reference location for a checkout-based deployment:

```text
private/company.yaml
```

`private/` is already excluded by the repository `.gitignore`. A company may instead use a private configuration repository or another protected path.

Examples:

```text
real company identifier/name where private
host/runtime path
real employee/group identifiers
selected Hermes Profiles
selected Knowledge Bases
selected mailbox logical IDs and addresses
mailbox business purpose
mailbox-scoped grants
allowed folders
selected provider endpoints/modes
controlled acceptance recipient addresses
non-secret model IDs
private network routes
backup destination identifiers/paths
retention policy selection
symbolic secret references
```

These values may be sensitive company configuration, but they are not credentials and should not be forced into a secret store merely because they are private.

### Class C — Protected secrets / external authority

Authority:

```text
selected protected secret storage / provider / operator authority
```

Examples:

```text
mailbox client password
SMTP/IMAP credential
Hermes Profile API key
Open WebUI administrator password
model-provider API key
WeKnora runtime/database password
OIDC client secret
messaging bot secret
```

Secret values must never be stored in:

```text
public repository
company YAML desired-state overlay
deployment-state record
normal logs
prompt/chat content
governance audit evidence
```

The private overlay may contain only a symbolic `secret_ref` identifying which protected secret must be resolved.

### Class D — Observed runtime/deployment state

Authority:

```text
actual runtime + deployment-specific state record
```

Examples:

```text
actual component versions/commits
actual stable resource IDs
actual enabled capability state
non-secret service endpoints
acceptance result
provider result references
secret storage class/location description, never value
backup/restore result
known limitations
```

Desired state and observed state are not the same thing. Do not rewrite desired configuration merely to make it match an accidental runtime drift.

---

## 3. Configuration precedence

The effective installation intent is resolved in this order:

```text
Frozen architecture / security contracts
        ↓
config/capabilities.yaml
        ↓
config/company.example.yaml reusable schema/default posture
        ↓
active company-private non-secret overlay
        ↓
protected secret resolution
        ↓
actual runtime reconciliation
```

Higher-precedence private values may select company-specific leaves, but they may not silently override frozen architecture/security invariants.

For example, the v2 private overlay may select:

```text
which mailbox
which employee group
which communication Profile ID
which runtime path
```

but it may not change:

```text
send_requires_human_approval: true
```

to disable the frozen v2 human-approval boundary.

Such a request requires an explicit System Design change, not a configuration override.

---

## 4. Merge/reconciliation rule

The blueprint does not require a universal YAML merge engine.

A capable installer may resolve desired state directly from the public schema plus private overlay, but must apply these semantics:

```text
scalar company-specific value
→ private value replaces public placeholder/default when permitted

map/object
→ reconcile by key

list of named resources
→ reconcile by stable logical `id`, not by array position

secret reference
→ resolve externally; never merge the secret value into desired-state YAML
```

Do not blindly concatenate lists such as Profiles, mailboxes, groups, or mailbox grants.

If two active sources define contradictory ownership/authorization for the same stable resource and the conflict cannot be resolved deterministically:

```text
BLOCKED — CONFIG CONFLICT: <resource / field>
```

---

## 5. Placeholder rule

Placeholders such as:

```text
<SELECT_PROVIDER>
<SELECT_MODEL>
<ASSIGN_OWNER>
<PILOT_MAILBOX>
<PROTECTED_CLIENT_PASSWORD>
```

are valid in public examples only.

An active deployment/validation configuration must not treat an unresolved placeholder as a real value.

If a field is required by the selected readiness/capability and still contains a placeholder/null/empty value:

```text
BLOCKED — REQUIRED INPUT: <exact field or decision>
```

Disabled capabilities do not require their conditional inputs.

---

## 6. Secret reference model

The blueprint uses symbolic references rather than inventing a universal secret URI/backend.

Example private desired state:

```yaml
client_credential_ref: email-sales-mailbox-client-password

secret_refs:
  email-sales-mailbox-client-password:
    class: email-mailbox-client-credential
    consumer: eao-email-governance
    native_binding: EAIO_EMAIL_CLIENT_PASSWORD
```

This means:

```text
which secret is needed       → symbolic ref
what kind of secret          → class
which process receives it    → consumer
where selected code expects it → native binding
actual value                 → protected storage / operator authority
```

It does **not** mean the secret value belongs in YAML.

The deployment implementation may use:

```text
protected process environment
upstream-supported credential store
OS keychain/secret mechanism
protected file readable only by the service
another approved enterprise secret store
```

Choose the smallest mechanism appropriate to the selected runtime. Do not add Vault/another secret platform merely because v2 has credentials.

---

## 7. v2 email private desired-state contract

When `capabilities.email.enabled: true`, the private configuration must resolve at least:

```text
provider
communication Profile ID
one or more explicitly selected mailbox definitions
stable mailbox logical ID
mailbox address
business purpose/owner context
allowed read folders
mailbox grants by human/group principal
controlled initial test recipient scope for acceptance
attachment policy
human-approval policy (must remain enabled in v2)
email-governance state location or accepted default
mailbox credential secret reference
```

Reference shape is provided by:

```text
config/company.private.example.yaml
```

### Mailbox grant shape

The baseline permission unit is:

```text
principal + mailbox_id + explicit permissions
```

Example:

```yaml
principal:
  type: group
  id: sales-team
mailbox_id: sales-mailbox
permissions:
  - email.read
  - email.draft
  - email.approve
  - email.send
```

No matching effective grant means deny.

Do not infer mailbox authorization from mailbox credentials, Profile tool availability, or Open WebUI Assistant visibility.

---

## 8. Communication Profile configuration

When email is enabled, the reference ID-1 topology expects a separate communication Profile/equivalent isolated Profile boundary.

The company-private desired state must identify that Profile and its intended employee groups.

It must not copy provider passwords into the Hermes Profile configuration.

Conceptually:

```text
communication Profile
→ receives only the private governance MCP/API binding and WeKnora retrieval needed for its role

eao-email-governance
→ owns provider credentials and deterministic email governance state
```

The exact Profile runtime template is closed under later Installation Design work; ID-2 only defines the required configuration input boundary.

---

## 9. Runtime environment templates are bindings, not desired-state authority

Files such as:

```text
config/.env.example
infrastructure/email/tencent-exmail/imap.env.example
Hermes *.env.example
```

show native runtime binding names.

They are not the canonical source of company desired state and must not become a second configuration database.

A future installer should:

```text
resolve desired non-secret value from private company config
resolve secret from protected secret authority
render/inject the minimum native environment expected by the selected component
```

For the current Tencent Stage 1 candidate, for example:

```text
mailbox address       → private company config
IMAP host/port        → private config or provider-safe default
allowed folders       → private company config
client password       → protected secret reference

runtime bindings:
EAIO_EMAIL_USERNAME
EAIO_EMAIL_IMAP_HOST
EAIO_EMAIL_IMAP_PORT
EAIO_EMAIL_ALLOWED_FOLDERS
EAIO_EMAIL_CLIENT_PASSWORD
```

Only the last item is the mailbox credential secret.

---

## 10. Required-input evaluation

Before mutating a target for an enabled capability, the installer must build a small closure table:

```text
Input
Class
Source/ref
Required now?
Resolved?
Consumer
```

Example for read-only email:

```text
mailbox logical ID        private non-secret   required   governance service
mailbox address           private non-secret   required   governance service
allowed folders           private non-secret   required   governance service
communication Profile     private non-secret   required   Open WebUI/Hermes
human/group grants        private non-secret   required   governance authorization
client password ref       private non-secret   required   secret resolver
client password value     secret               required   governance service only
SMTP credential/use       secret               not Stage 1   not injected
```

Do not inject credentials for a later stage merely because they are already available.

---

## 11. Fail-closed result classes

Use these baseline installation outcomes:

### Missing business/private desired-state input

```text
BLOCKED — REQUIRED INPUT: <specific field/decision>
```

Examples:

```text
BLOCKED — REQUIRED INPUT: capabilities.email.mailboxes[0].address
BLOCKED — REQUIRED INPUT: authorized human/group scope for sales-mailbox
```

### Missing protected secret

```text
BLOCKED — REQUIRED INPUT: secret <symbolic-ref>
```

Do not print the expected value or nearby environment contents.

### Contradictory configuration

```text
BLOCKED — CONFIG CONFLICT: <specific conflict>
```

### Frozen security invariant violated

```text
FAIL — SECURITY CONTRACT VIOLATION: <invariant>
```

Example:

```text
send_requires_human_approval=false
```

for the frozen v2 customer-facing email capability.

### Unknown provider/runtime mechanism

If the selected capability is valid but the repository lacks an implementation binding:

```text
FAIL — BLUEPRINT INCOMPLETE: <missing adapter/playbook/contract>
```

Do not silently substitute another provider.

---

## 12. Secret handling rules for AI installers

An AI Engineering Agent performing a later authorized deployment must:

```text
request only secrets required by the active stage
avoid echoing secret values
avoid placing secrets in command history where practical
avoid writing secrets into generated reports/logs
use exact upstream/native variable names or credential stores
scope each credential to the narrowest practical consumer
verify protected-file permissions when file-based injection is selected
record only secret class/reference/location description after installation
```

If a tool/API response reveals a secret unexpectedly, do not reproduce it in subsequent prose or state records.

---

## 13. Runtime/deployment-state recording

Deployment state may record:

```text
mailbox logical ID/address when company policy permits
provider
communication Profile ID
human/group authorization scope
allowed folders
selected non-secret endpoint mode
secret symbolic reference or storage class/location description
acceptance results
```

It must not record:

```text
mailbox password
client password
API token
Hermes Profile API key
Open WebUI bearer/admin token
model-provider API key
raw secret-bearing environment dump
```

---

## 14. Public/private boundary

The public repository may include only synthetic examples such as:

```text
sales@example.invalid
integration-test@example.invalid
sales-team
sales-mailbox
communication
```

Real employee lists, mailbox addresses, internal network topology, credential references that reveal sensitive naming, and other deployment-private values belong in the private layer when disclosure would create risk.

A real company may choose to make some non-secret values public; the blueprint does not require secrecy for information that the adopter has intentionally published.

---

## 15. ID-2 acceptance contract

ID-2 is complete when the repository makes all of the following unambiguous:

```text
[✓] public blueprint configuration is distinct from company-private desired state
[✓] company-private desired state is distinct from secret values
[✓] observed runtime state is not a desired-state source
[✓] a synthetic private-overlay shape exists
[✓] secret values are represented only by symbolic references/classes in configuration
[✓] each secret has an identified consumer/native binding before use
[✓] unresolved required inputs block rather than guess
[✓] unresolved placeholders cannot become runtime values
[✓] mailbox grants are explicit per principal + mailbox + operation
[✓] v2 human approval cannot be disabled by private configuration
[✓] environment templates are runtime bindings, not competing configuration authorities
[✓] disabled capabilities do not require unused secrets
[✓] real credentials remain independently gated by a real deployment/validation task
```

Result:

```text
ID-2: PASS
CONFIG / SECRET INPUT CONTRACT FROZEN
```
