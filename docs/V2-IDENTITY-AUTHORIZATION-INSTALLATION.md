# Enterprise AI Office v2 — Trusted Identity & Mailbox Authorization Installation Contract

Status: identity / authorization installation contract frozen / real deployment not authorized
Version: 1.0
Date: 2026-09-06

This document closes `ID-4 — Trusted identity and mailbox authorization propagation` for the Enterprise AI Office v2 `installation_design` phase.

It defines how a future authorized installation carries a trusted Open WebUI HumanActor identity and current group membership into the narrow EAO Email Governance boundary without confusing human identity with Hermes Profile identity or provider credentials.

It does **not** authorize a real company installation, real employee binding, mailbox credentials, or provider access.

Use with:

- `docs/V2-EMAIL-DESIGN.md`
- `docs/V2-INSTALLATION-ARCHITECTURE.md`
- `docs/V2-CONFIG-PROTECTED-INPUTS.md`
- `docs/V2-STAGE-CONTRACTS.md`
- `docs/CLIENT-RBAC.md`
- `infrastructure/open-webui/PROVISIONING.md`
- `config/company.example.yaml`
- `config/company.private.example.yaml`
- `config/capabilities.yaml`

---

## 1. Frozen identity roles

Keep these identities separate:

```text
HumanActor
= the authenticated human who requested/reviewed/approved an operation

Hermes Profile
= AI role / capability boundary

Open WebUI service
= trusted employee Web surface / server-side tool forwarder

Mailbox provider credential
= technical provider access only
```

None of these may be substituted for another.

A mailbox credential never proves human authority. A Hermes Profile key never identifies the employee. Human identity never comes from LLM text/tool arguments.

---

## 2. Reference runtime identity path

The reference v2 installation uses Open WebUI as both the authenticated human surface and the server-side executor of the narrow Email Governance tool connection.

```text
Employee browser
   ↓ authenticated session
Open WebUI
   ├─ Communication Assistant → Hermes communication Profile (reasoning)
   │
   └─ server-side Email Governance MCP/OpenAPI tool connection
         ↓ trusted forwarder identity headers
      eao-email-governance
         ↓ mailbox authorization evaluation
      Email Provider
```

Open WebUI supplies the Email Governance tool definitions to the Communication Assistant/model, executes approved tool calls server-side, and returns tool results to the model.

This intentionally avoids requiring Hermes to forward inbound HTTP identity into downstream MCP calls.

The Hermes communication Profile remains the AI role/capability boundary and must still be isolated from the v1 `general` Profile. It does not become the HumanActor identity authority.

---

## 3. Why the Open WebUI server-side tool path is the reference path

The pinned Open WebUI v0.11.3 line supports server-side external tool connections and server-side custom Header substitution using authenticated user context, including:

```text
{{USER_ID}}
{{USER_GROUP_IDS}}
{{CHAT_ID}}
{{MESSAGE_ID}}
```

The same release resolves group placeholders from Open WebUI's group membership store.

This gives the blueprint a supported upstream path for trusted per-request human context without:

```text
forking Hermes
putting identity in prompts
asking the model to echo employee IDs
building a new identity service
letting the browser call governance directly
```

The reference installation therefore prefers Open WebUI's native external-tool mechanism over a custom transitive identity relay inside Hermes.

---

## 4. Canonical HumanActor identifier

For the baseline installation, the canonical downstream HumanActor identifier is:

```text
open-webui:<Open WebUI user id>
```

Example using synthetic data:

```text
open-webui:00000000-0000-4000-8000-000000000001
```

The Open WebUI user ID is used for authorization/audit identity.

These are metadata only and must not be security identifiers:

```text
email address
display name
```

When OIDC/enterprise identity is enabled, the IdP authenticates the employee into Open WebUI and Open WebUI resolves the local user. The governance service still consumes the trusted Open WebUI HumanActor identifier rather than attempting to parse or reimplement the IdP login flow.

Do not enable account merging by email merely to simplify HumanActor mapping.

---

## 5. Reference trusted-forwarder envelope

The Email Governance external-tool connection is server-managed and uses a dedicated protected service-to-service secret plus Open WebUI server-side identity templates.

Conceptual request headers:

```text
Authorization: Bearer <protected Open WebUI → Governance forwarder token>
X-EAO-Human-Actor-Id: {{USER_ID}}
X-EAO-Human-Group-Ids: {{USER_GROUP_IDS}}
X-EAO-Chat-Id: {{CHAT_ID}}
X-EAO-Message-Id: {{MESSAGE_ID}}
```

Optional display/audit-only headers may include:

```text
X-EAO-Human-Name: {{USER_NAME}}
X-EAO-Human-Email: {{USER_EMAIL}}
```

The governance service canonicalizes:

```text
X-EAO-Human-Actor-Id: <id>
→ actor_id = open-webui:<id>
```

The group ID header is parsed only after the trusted-forwarder channel is authenticated.

The browser and LLM never supply these values as normal tool arguments.

---

## 6. Trusted-forwarder authentication

The governance service accepts Open WebUI human identity only when all required transport checks pass:

```text
request reaches the private governance endpoint
+
dedicated Open WebUI → Governance service credential is valid
+
HumanActor header is present and syntactically valid
+
group header is server-originated on the same authenticated request
```

If any required identity/trust input is missing or invalid:

```text
ACTOR_UNRESOLVED / TRUSTED_FORWARDER_INVALID
→ FAIL CLOSED
```

Do not fall back to:

```text
email address from request body
employee name from prompt
actor_id supplied as a tool parameter
Hermes Profile name
mailbox username
```

The service-to-service credential is a protected Secret and never appears in Git, model context, employee browser state, governance audit, or normal logs.

---

## 7. Optional Open WebUI signed-JWT mode

Open WebUI v0.11.3 also supports signed forwarded user JWTs when `ENABLE_FORWARD_USER_INFO_HEADERS` and `FORWARD_USER_INFO_HEADER_JWT_SECRET` are configured.

That token provides signed user identity claims (`sub`, `email`, `name`, `role`, issuer and timestamps), but group IDs are not part of the signed token in the pinned implementation.

The blueprint therefore does **not** require global signed-user-header forwarding as the baseline merely to obtain group authorization. A deployment may adopt it as additional identity hardening after reviewing its broader identity-forwarding/privacy behavior, while still resolving group membership through an authenticated server-side path.

Do not create a custom JWT/IdP service solely for v2 Email.

---

## 8. Open WebUI group IDs are runtime authorization facts

Company configuration may use stable logical group IDs such as:

```text
sales-team
support-team
```

Open WebUI assigns runtime group IDs.

Provisioning must record the mapping:

```text
company logical group id
→ Open WebUI runtime group id
```

in deployment/provisioning state without secrets.

Example:

```text
sales-team
→ owui-group-uuid-123
```

The governance authorization loader compiles mailbox grants against those resolved runtime group IDs.

At request time Open WebUI forwards the **current runtime group IDs** for the signed-in user. This prevents authorization from depending on mutable display names.

If a configured logical group cannot be resolved to exactly one intended Open WebUI group:

```text
BLOCKED — CONFIG CONFLICT: unresolved or ambiguous Open WebUI group mapping
```

---

## 9. Direct HumanActor grants

Group grants are the reference baseline because they are simpler to operate for shared mailboxes.

Direct grants remain supported when a company has a real need.

A direct grant must reference the canonical HumanActor identity:

```text
principal.type: human
principal.id: open-webui:<stable-user-id>
```

Do not use a display name as a direct-grant identifier.

If an OIDC/local-auth user has not yet been resolved to a stable Open WebUI user ID and a direct grant is required:

```text
BLOCKED — REQUIRED INPUT: resolved Open WebUI HumanActor id for <private logical principal>
```

Do not create a second employee directory merely to avoid this binding step.

---

## 10. Effective mailbox authorization

For each governed operation the governance service evaluates current request identity against the active mailbox grant policy.

Baseline operations:

```text
email.read
email.draft
email.approve
email.send
```

Effective human permission for one mailbox is the additive union of matching direct + current group grants:

```text
direct grants for actor_id
+
group grants for current Open WebUI group IDs
→ effective mailbox operations
```

No matching grant:

```text
DENY
```

Permissions remain operation-specific.

```text
read does not imply draft
read does not imply approve
approve does not imply send
```

The governance service additionally applies object visibility, action preconditions, and valid approval where required.

---

## 11. Profile/tool capability enforcement

Human mailbox permission and AI capability remain separate controls.

The reference installation enforces the Profile/tool boundary primarily in Open WebUI/Hermes provisioning:

```text
General Assistant
→ Hermes `general`
→ no Email Governance tools attached

Communication Assistant
→ Hermes communication Profile
→ only the stage-enabled Email Governance tools attached
```

The Email Governance external-tool resource itself is restricted to the intended Communication employee groups/users through Open WebUI Access Control.

Attaching a tool to the Communication Assistant does not replace the governance service's mailbox authorization check.

Acceptance must prove both:

```text
General Assistant does not receive Email tools by default
+
unauthorized HumanActor cannot execute mailbox operations even if an API/tool path is attempted directly
```

The governance service may record the configured Communication Assistant/Profile identifier as operation context, but it must never treat a model-supplied Profile string as human authorization.

---

## 12. Tool exposure by Stage

The Open WebUI Communication Assistant binds only the tools enabled by the current accepted Stage.

```text
Stage 1
  search_email
  get_email

Stage 2
  + prepare_reply_draft

Stage 3
  approval is NOT an LLM tool

Stage 4
  send_approved_reply may remain behind the deterministic approval action rather than being a free-choice model tool
```

The governance tool server connection is admin-managed. Ordinary employees cannot register arbitrary replacement MCP servers or change trusted identity headers.

---

## 13. Deterministic approval identity path

Formal approval remains a trusted-human interaction, not a model tool call.

Reference path:

```text
Employee clicks trusted approval Action
→ Open WebUI server-side Action executes
→ Action obtains current `__user__.id`
→ Action resolves current Open WebUI group membership server-side
→ Action calls governance through the same protected trusted-forwarder channel
→ governance re-evaluates email.approve for the exact mailbox/draft
→ SendApproval is created only if all checks pass
```

For the pinned Open WebUI v0.11.3 line, the server-side group model exposes group lookup by member ID. The version-bound Action implementation may use that upstream capability.

The Action must not accept `actor_id`, group IDs, or approval authority from browser-supplied form fields or model-generated message text.

Exact Action code and Draft/SendApproval persistence are completed under ID-5.

---

## 14. Identity changes and permission freshness

Mailbox authorization is evaluated on every governed request using the HumanActor and group membership presented by the current trusted Open WebUI server-side request.

Therefore:

```text
user removed from Open WebUI group
→ subsequent governed request no longer includes that group
→ grant no longer applies
```

For OIDC-managed groups, Open WebUI group membership freshness follows the configured OIDC synchronization behavior; where the selected release updates membership at login, the deployment acceptance must include the required logout/login or session-refresh behavior after a group change.

An existing DraftReply or SendApproval does not freeze future human permission.

At send time:

```text
current HumanActor / mailbox permission
must be checked again
```

An approval is not a permanent capability token.

---

## 15. Service/network boundary

Reference inbound governance policy:

```text
browser-direct access        DENY / unreachable
public Internet inbound      DENY / unreachable
unknown service caller       DENY
Open WebUI trusted forwarder ALLOW to employee-facing governed endpoints after authentication
local operator/admin path    separate protected control path only if explicitly required
```

Provider credentials are available only inside the governance/provider adapter boundary.

Hermes receives neither mailbox credential nor Open WebUI → Governance forwarder secret.

---

## 16. Audit identity fields

Governance evidence uses stable IDs:

```text
human_actor_id
human_group_ids_at_decision (or normalized grant references)
profile/assistant context when available
mailbox_id
operation
decision/reason
```

Display name/email may be recorded only when company policy requires them and they are not treated as identity authority.

Do not persist the service-to-service forwarder token, Open WebUI bearer/session token, OIDC token, or mailbox credential.

---

## 17. Failure semantics

Reference fail-closed results:

```text
missing/invalid trusted-forwarder credential
→ FAIL — TRUSTED FORWARDER AUTHENTICATION

missing/empty HumanActor ID
→ DENY — ACTOR_UNRESOLVED

malformed group identity context
→ DENY — GROUP_CONTEXT_INVALID

mailbox not configured
→ DENY — MAILBOX_SCOPE_NOT_FOUND

no matching read/draft/approve/send grant
→ DENY — MAILBOX_OPERATION_NOT_AUTHORIZED

configured group has no resolved Open WebUI runtime mapping
→ BLOCKED — CONFIG CONFLICT
```

Do not infer permission from prior successful requests.

---

## 18. Provisioning / reconciliation sequence

For an authorized future target:

```text
1. verify Stage 0 / v1 baseline
2. provision/reconcile Communication Open WebUI group(s)
3. provision/reconcile Hermes communication Profile and unique Profile key
4. provision/reconcile restricted Communication Assistant
5. start governance service on private endpoint
6. resolve logical group → Open WebUI runtime group mappings
7. compile mailbox grants into governance authorization config/state
8. create/reconcile Open WebUI admin-managed external Email Governance tool connection
9. configure protected forwarder credential + server-side identity templates
10. attach only stage-enabled Email tools to Communication Assistant
11. grant tool/Assistant access only to intended groups/users
12. run positive and negative identity/mailbox authorization acceptance
13. record non-secret mappings/evidence in deployment state
```

Provisioning is convergent; do not create duplicate groups, tool servers, Assistants, or Profile connections on rerun.

---

## 19. Acceptance contract

ID-4 installation contract is closed when the blueprint specifies and future target acceptance can prove:

```text
[ ] Open WebUI is the trusted HumanActor source
[ ] canonical actor ID is independent of email/display name
[ ] browser/model cannot supply trusted actor/group context as normal arguments
[ ] Open WebUI → Governance channel has protected service authentication
[ ] current Open WebUI group IDs reach governance on the trusted server-side path
[ ] logical company group → runtime Open WebUI group mapping is deterministic
[ ] direct and group mailbox grants resolve additively
[ ] no grant means deny
[ ] read/draft/approve/send remain independent
[ ] General Assistant has no Email tools by default
[ ] Communication Assistant exposes only stage-enabled Email tools
[ ] formal approval uses a deterministic current-human path
[ ] permission is re-evaluated on governed actions including send
[ ] provider credential remains separate from HumanActor authority
[ ] identity/authorization failure is fail-closed
[ ] no new IAM/auth proxy/directory is required
```

Result:

```text
ID-4: PASS
IDENTITY / AUTHORIZATION INSTALLATION CONTRACT FROZEN
```
