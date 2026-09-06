# Open WebUI v2 Communication Provisioning

Status: installation-design execution path / no real deployment authorized

This playbook implements the Open WebUI side of:

- `docs/V2-IDENTITY-AUTHORIZATION-INSTALLATION.md`
- `docs/V2-INSTALLATION-ARCHITECTURE.md`
- `docs/V2-STAGE-CONTRACTS.md`

It is version-bound to the first validated Open WebUI reference release:

```text
Open WebUI v0.11.3
```

Re-verify native routes/fields against another selected release before deployment.

---

## 1. Goal

Provision one restricted Communication Assistant backed by the isolated Hermes communication Profile and bind the EAO Email Governance server as an admin-managed server-side tool connection.

The employee browser must never call governance directly.

Reference path:

```text
Employee
→ Open WebUI Communication Assistant
→ Hermes communication Profile for reasoning
→ Open WebUI server-side tool loop
→ eao-email-governance
```

---

## 2. Required inputs

Resolve from active company/private configuration and protected storage:

```text
Open WebUI admin bootstrap/auth
Communication Profile ID/display name/base URL/Profile key
intended Open WebUI logical group(s)
resolved Open WebUI runtime group IDs
Governance private URL
Open WebUI → Governance forwarder token
current accepted Stage
stage-enabled Email tool set
```

Missing protected forwarder token on an authorized target:

```text
BLOCKED — REQUIRED INPUT: Open WebUI → Governance forwarder credential
```

---

## 3. Reconcile Communication groups

Use the existing `infrastructure/open-webui/PROVISIONING.md` group logic.

For every logical group referenced by the Communication Profile or mailbox grants:

```text
inspect existing Open WebUI groups
→ reuse intended match when unambiguous
→ create only when absent and configuration owns it
→ record logical group ID → Open WebUI runtime group ID
```

Do not authorize downstream mailbox operations by mutable display name.

If a logical group maps ambiguously:

```text
BLOCKED — CONFIG CONFLICT: unresolved or ambiguous Open WebUI group mapping
```

---

## 4. Reconcile Hermes communication model connection

Use the same supported OpenAI-compatible connection mechanism as the baseline provisioning playbook, but with the communication Profile's own URL/key.

Conceptually:

```text
Communication Assistant
→ Hermes communication Profile API
→ distinct Profile API credential
```

Do not connect Hermes default/admin.

Do not reuse the `general` Profile key.

---

## 5. Reconcile the Email Governance external-tool connection

Prefer Open WebUI's native admin-managed HTTP MCP connection when the governance service exposes Streamable HTTP MCP. An OpenAPI connection is acceptable if the final governance service exposes OpenAPI instead; do not add MCPO merely to bridge an already-HTTP service.

Reference connection properties:

```text
ID: eao-email-governance
URL: <private governance tool endpoint>
Access: only intended Communication groups/users
Authentication: protected service-to-service bearer credential
```

Configure server-side custom headers conceptually as:

```json
{
  "Authorization": "Bearer <PROTECTED_FORWARDER_TOKEN>",
  "X-EAO-Human-Actor-Id": "{{USER_ID}}",
  "X-EAO-Human-Group-Ids": "{{USER_GROUP_IDS}}",
  "X-EAO-Chat-Id": "{{CHAT_ID}}",
  "X-EAO-Message-Id": "{{MESSAGE_ID}}"
}
```

The actual protected token must be injected through the selected protected provisioning mechanism; never commit it in this JSON.

For the pinned Open WebUI line, custom header templates are expanded server-side using the authenticated user and current Open WebUI group membership.

Do not expose actor/group headers as tool input parameters.

---

## 6. Tool access control

The external Email Governance connection is admin-managed.

Grant read/use access only to the users/groups configured for the Communication capability.

Ordinary employees must not receive permission to register or replace MCP servers for this capability.

Open WebUI Access Control is a first gate only. Governance still performs mailbox-scoped authorization per operation.

---

## 7. Bind stage-enabled tools to Communication Assistant

The Communication Assistant is a restricted Workspace Model/Assistant backed by the Hermes communication Profile.

Attach only the tools allowed by the accepted Stage:

```text
Stage 1
  search_email
  get_email

Stage 2
  + prepare_reply_draft

Stage 3
  no approval LLM tool

Stage 4
  send_approved_reply remains governed and may be invoked only through the deterministic approval/send path
```

The `general` Model/Assistant must not have the Email Governance tool server attached.

Do not make the external tool public/wildcard merely because it is attached to a restricted model.

---

## 8. Current user identity contract

For normal tool calls, Open WebUI is the trusted forwarder.

The Governance service receives:

```text
HumanActor ID     from {{USER_ID}}
current group IDs from {{USER_GROUP_IDS}}
chat/message IDs  for correlation only
```

Canonical HumanActor:

```text
open-webui:<USER_ID>
```

Email/display name may be used for user-facing display but not as the authorization identifier.

If group placeholder resolution fails and the authorization decision depends on group grants, governance must deny rather than assume membership.

---

## 9. Formal approval Action preparation

Stage 3 adds a trusted server-side Action/Function attached only to the Communication Assistant.

The exact implementation is completed under ID-5, but its identity contract is fixed here:

```text
Action receives current __user__.id from Open WebUI
Action resolves current group membership server-side
Action calls governance using the protected forwarder channel
browser/model cannot override actor/group identity
```

The pinned Open WebUI v0.11.3 backend exposes group lookup by member ID through its group model; a version-bound Action may use that supported-in-release server-side capability.

Do not treat free-form chat text as approval evidence.

---

## 10. OIDC deployments

OIDC changes how the HumanActor enters Open WebUI, not the downstream governance identity contract.

Use `infrastructure/access/OPEN-WEBUI-OIDC.md`.

When Open WebUI synchronizes groups from OIDC claims, test the actual login/session refresh behavior after membership changes.

The governance service still consumes:

```text
open-webui:<current user id>
+
current Open WebUI runtime group IDs
```

Do not reimplement OIDC validation inside `eao-email-governance` for the baseline.

---

## 11. Optional signed-user JWT

Open WebUI v0.11.3 can globally forward a signed user JWT when its forwarding settings are enabled.

The reference v2 installation does not require that global mode because the dedicated Email tool connection already has a protected service credential and per-connection identity templates, and the signed token does not include group IDs in the pinned implementation.

A deployment may enable signed-user forwarding as an additional hardening decision after reviewing where Open WebUI forwards that identity metadata.

Do not invent a new JWT issuer solely for this capability.

---

## 12. Reconciliation

On rerun:

```text
inspect current groups
inspect logical → runtime group mapping
inspect communication model/Profile connection
inspect Email Governance tool connection
inspect tool access grants
inspect Communication Assistant attached tool set
compare with current accepted Stage
update only owned differences
preserve unrelated Open WebUI resources/settings
```

Do not create duplicate Assistants/tool connections/groups.

If Stage is rolled back, remove higher-stage tools before removing lower-stage dependencies.

---

## 13. Acceptance

Run with synthetic/authorized identities on an explicitly approved target.

Required matrix:

```text
Authorized Communication user
→ sees Communication Assistant
→ has intended Email tools
→ authorized mailbox read/draft operation succeeds

User outside Communication groups
→ cannot use Communication Assistant/tool resource
→ direct governance request without trusted forwarder auth fails

Authorized user without mailbox grant
→ Open WebUI may expose Communication Assistant
→ governance denies mailbox operation

General Assistant
→ no Email Governance tools attached by default
```

Also test:

```text
missing forwarder token → deny
forged browser/tool actor field → ignored/deny
removed group membership → subsequent governed request loses group grant
Profile key A does not authenticate as another Hermes Profile
no forwarder/mailbox/Profile secret appears in browser, prompt, logs, or Git
```

Record non-secret runtime group IDs/mappings, resource IDs, tool connection ID, and acceptance result in deployment state.

---

## 14. Result

When applicable target tests pass:

```text
PASS — TRUSTED HUMAN IDENTITY / MAILBOX AUTHORIZATION PROPAGATION
```

For Installation Design closure, the existence and consistency of this playbook contributes to:

```text
IDENTITY / AUTHORIZATION INSTALLATION CONTRACT FROZEN
```
