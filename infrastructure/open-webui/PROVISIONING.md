# Open WebUI Provisioning Playbook

This playbook turns the Enterprise AI Office company configuration into Open WebUI users/groups, Hermes-backed model resources, and access grants without requiring a deployment operator to click through the UI manually.

The authoritative Open WebUI version, upstream provenance, acquisition method,
and runtime identity live in `config/validated-stack.yaml`. Use this contract
only after `DEPLOY.md §4.1–4.2` has acquired and verified that selected
runtime. If an upgrade is intentionally selected, re-qualify the version-specific
routes/forms before reusing this contract.

Use this after the Open WebUI container is healthy and the Hermes employee
Profile APIs are reachable from the Open WebUI container.

## 1. Security model

The employee authorization path is:

```text
Open WebUI user
→ group membership
→ Model/Assistant read grant
→ matching Hermes Profile connection
→ Profile-scoped API credential
```

For the validated Open WebUI version, ordinary users do not automatically receive raw upstream models when model access control is enabled. Employee-visible models require a corresponding Open WebUI Model record and read access grant.

This means the deployment should not rely on UI hiding or connection naming as authorization.

### Company knowledge authority

Open WebUI owns employee identity, chat UX, conversation history, and
Assistant/resource ACLs. It does **not** own authoritative EAO company
knowledge.

For the Core architecture:

```text
Open WebUI
→ Hermes employee Profile
→ approved WeKnora MCP/API
→ authoritative company Knowledge Base
```

This provisioning contract must not create a second EAO-managed copy of
company documents in Open WebUI native Knowledge or attach such a copy to the
General Assistant merely because Open WebUI supports that feature.

Conversation file upload may still be enabled as temporary chat context when
company policy allows it. Temporary employee attachments are not durable
company Knowledge and must not silently become the authoritative source for
policies, product specifications, SOPs, or other governed company facts.

On an existing Open WebUI deployment:

- preserve unrelated legitimate native Knowledge resources;
- do not delete them merely to make the record count zero;
- if an EAO employee Assistant is already coupled to a duplicate native company
  Knowledge resource, classify it as authority drift and review the dependency
  before changing it;
- remove/reconcile only the EAO-owned duplicate path after impact and acceptance
  are understood.

The sanitized ARMOR reference runtime currently has zero Open WebUI native
Knowledge records. That is valid evidence for the reference deployment, not a
requirement to destroy unrelated resources on another existing deployment.

## 2. Required inputs

From the active company configuration:

```text
employee_access.web.groups:
  company logical group ID
  intended display_name

core_provisioning.open_webui.admin_identity:
  email
  display_name
  password_ref

for each enabled employee Profile:
  Profile ID
  employee-facing display name
  allowed company logical group IDs
```

The administrator email/display name are private non-secret desired state.
Resolve `admin_identity.password_ref` through `secret_refs` and protected
storage; the provisioning binding is `OPEN_WEBUI_ADMIN_PASSWORD`.

From protected deployment input:

```text
OPEN_WEBUI_URL
secret value referenced by core_provisioning.open_webui.admin_identity.password_ref

for each enabled employee Profile:
  Hermes OpenAI-compatible base URL
  Profile API key resolved from the Profile's symbolic credential ref
```

Baseline mapping:

```text
Profile ID: general
Display name: General Assistant
Allowed company group: all-employees
Open WebUI group display name: All Employees
Hermes URL: http://host.docker.internal:8642/p/general/v1
```

Exact host/port may differ by deployment.

Do not print or commit protected values. If a required protected credential,
target Profile route, or company group mapping is unresolved, stop with:

```text
BLOCKED — REQUIRED INPUT: <specific item>
```

## 3. Use the native admin API

The validated Open WebUI release exposes application APIs used by its own administrative UI. Prefer these over direct database writes.

Relevant v0.11.3 routes:

```text
POST /api/v1/auths/signin
POST /api/v1/auths/add

GET  /api/v1/groups/
POST /api/v1/groups/create
POST /api/v1/groups/id/<group_id>/users/add

GET  /openai/config
POST /openai/config/update

POST /api/v1/models/create
GET  /api/v1/models/model?id=<model_id>
POST /api/v1/models/model/update

GET  /api/models
GET  /api/v1/models
```

`/api/v1/models/model/update` identifies the Model from the `id` inside the submitted `ModelForm` body; it does not require an `id` query parameter in v0.11.3.

All modifying operations below require an authenticated administrator token.

Do not write directly to Open WebUI's SQLite/PostgreSQL tables for normal provisioning.

### 3.1 Pinned API-route provenance

The provisioning routes in this playbook were verified against the validated
Open WebUI source commit recorded in `config/validated-stack.yaml`:

```text
open-webui/open-webui
commit: 2a960a59fe1dbbd35282f0556b3666d81102e781
tag: v0.11.3
```

Source files used for route verification:

```text
backend/open_webui/main.py
backend/open_webui/routers/auths.py
backend/open_webui/routers/groups.py
backend/open_webui/routers/openai.py
backend/open_webui/routers/models.py
```

At that commit, `main.py` mounts the relevant routers at:

```text
auths   → /api/v1/auths
groups  → /api/v1/groups
models  → /api/v1/models
openai  → /openai
```

The endpoint list above is a version-specific provisioning contract, not a
timeless Open WebUI API promise.

When Open WebUI is upgraded, re-read those router files at the selected commit,
verify the exact request bodies/response semantics used by this playbook, and
update this contract only after focused provisioning/RBAC acceptance passes.

## 4. Authenticate the administrator

Sign in with the protected bootstrap administrator:

```http
POST /api/v1/auths/signin
Content-Type: application/json

{
  "email": "<ADMIN_EMAIL>",
  "password": "<ADMIN_PASSWORD>"
}
```

The response contains a bearer token. Keep it in process memory/protected temporary state only. Do not echo it into logs or write it to Git.

Use:

```text
Authorization: Bearer <ADMIN_TOKEN>
```

for subsequent admin API calls.

## 5. Reconcile groups idempotently

Open WebUI owns a runtime UUID and a display name; the EAO company configuration
owns the stable logical group ID. Keep these identities distinct:

```text
company logical ID
→ intended Open WebUI display name
→ deployment-generated Open WebUI group UUID
```

Generic baseline:

| Company logical ID | Open WebUI display name |
| --- | --- |
| `all-employees` | `All Employees` |
| `ai-admins` | `AI Administrators` |

Do not blindly create duplicate groups.

For every group declared by company configuration:

1. read the company logical ID + intended `display_name` from active configuration;
2. `GET /api/v1/groups/`;
3. prefer the previously recorded logical-ID → runtime-UUID mapping when it still resolves to the intended resource;
4. otherwise match the intended Open WebUI display name;
5. if exactly one match exists, adopt it and record the mapping;
6. if none exists, create it;
7. if multiple plausible matches exist, stop with `BLOCKED — AMBIGUOUS STATE` rather than guessing;
8. record logical ID → display name → runtime UUID in deployment/protected provisioning state.

Create body:

```json
{
  "name": "All Employees",
  "description": "Baseline Enterprise AI Office employee group.",
  "permissions": {},
  "data": {}
}
```

Group permissions are additive. Keep group permissions minimal and rely on explicit Model resource grants for Assistant visibility.

The two baseline display names above are derived from the generic company
configuration. Do not create a second group whose name is a transformed logical
ID such as `All-Employees` or `AI-Admins`.

Specialist groups are created only from active company configuration.

## 6. Provision local employee users only when local auth is selected

If SSO/enterprise identity is enabled, follow `infrastructure/access/README.md` instead of pre-creating every employee as a local-password account.

For local-auth deployments, an administrator may create a known user through:

```http
POST /api/v1/auths/add
Authorization: Bearer <ADMIN_TOKEN>
Content-Type: application/json

{
  "name": "<EMPLOYEE_NAME>",
  "email": "<EMPLOYEE_EMAIL>",
  "password": "<PROTECTED_INITIAL_PASSWORD>",
  "role": "user"
}
```

Then add the returned user ID to each required group:

```http
POST /api/v1/groups/id/<GROUP_ID>/users/add
Authorization: Bearer <ADMIN_TOKEN>
Content-Type: application/json

{
  "user_ids": ["<USER_ID>"]
}
```

Do not place real employee lists/passwords in this public repository.

## 7. Reconcile Hermes OpenAI-compatible connections

Open WebUI stores OpenAI-compatible server connections in its native OpenAI configuration.

First read current state:

```http
GET /openai/config
Authorization: Bearer <ADMIN_TOKEN>
```

The validated update form contains:

```json
{
  "ENABLE_OPENAI_API": true,
  "OPENAI_API_BASE_URLS": [],
  "OPENAI_API_KEYS": [],
  "OPENAI_API_CONFIGS": {}
}
```

Never replace the whole configuration from a static example without reading it first. Reconcile by Hermes Profile base URL:

- preserve unrelated approved existing connections;
- update the existing matching URL if already present;
- otherwise append one connection;
- keep key and URL array indices aligned;
- add/update the corresponding index entry in `OPENAI_API_CONFIGS`.

For a Hermes employee Profile, use a narrow connection config such as:

```json
{
  "enable": true,
  "model_ids": ["general"]
}
```

where `general` is the exact model name advertised by that Hermes Profile API. A specialist connection uses its own unique Profile/model ID.

Then submit the reconciled complete object:

```http
POST /openai/config/update
Authorization: Bearer <ADMIN_TOKEN>
Content-Type: application/json
```

Each Hermes Profile connection uses its own Profile API key. Do not connect the privileged Hermes default/admin Profile to the employee client.

After updating, verify the administrator can see the expected upstream model IDs through `/openai/models` or `/api/models`.

This is also the required **container → host Hermes bridge acceptance** for the
selected container runtime. The request is resolved by the Open WebUI backend
using the configured Hermes connection URL (for the reference path,
`host.docker.internal`), so a successful host-side `curl` to Hermes is not a
substitute.

Require at least:

```text
Open WebUI backend
→ configured Hermes Profile URL
→ /p/general/v1
→ advertised model ID general
```

If Open WebUI is healthy but this enumeration fails, treat the container-runtime
bridge as incompatible/unresolved. Do not create the employee Model ACL record
until the backend connection succeeds.

## 8. Create the employee-visible Model/Assistant ACL record

For Open WebUI v0.11.3, a raw upstream model without a corresponding Models DB entry is admin-only when model access control is enforced.

For each enabled employee Profile, create a Model record **with the same model ID advertised by Hermes**. A record whose `id` matches a base model and has `base_model_id: null` acts as metadata/access-control override for that base model.

Baseline General payload:

```json
{
  "id": "general",
  "base_model_id": null,
  "name": "General Assistant",
  "meta": {
    "description": "Company-wide Enterprise AI Office assistant."
  },
  "params": {},
  "access_grants": [
    {
      "principal_type": "group",
      "principal_id": "<ALL_EMPLOYEES_GROUP_ID>",
      "permission": "read"
    }
  ],
  "is_active": true
}
```

Create through:

```http
POST /api/v1/models/create
Authorization: Bearer <ADMIN_TOKEN>
Content-Type: application/json
```

For an enabled specialist Profile, use that Profile's exact upstream model ID and grant `read` only to its configured employee group(s).

Do not give `anyone`/wildcard read access unless company policy explicitly requires a public resource.

## 9. Idempotent Model update behavior

Before creating a Model record, query the existing resource:

```http
GET /api/v1/models/model?id=<MODEL_ID>
Authorization: Bearer <ADMIN_TOKEN>
```

If it exists, submit the reconciled full `ModelForm` through:

```http
POST /api/v1/models/model/update
Authorization: Bearer <ADMIN_TOKEN>
Content-Type: application/json
```

The body includes the same `id`, intended display name, metadata, params, access grants, active flag, and desired `base_model_id` state.

Preserve unrelated administrator-curated metadata unless company configuration intentionally owns it. Do not create a duplicate Model ID.

## 10. Why the ACL record matters

With `BYPASS_MODEL_ACCESS_CONTROL=false`, Open WebUI filters ordinary-user model visibility against Models records and read grants. Direct model use checks the same access model and chained base-model access.

Conceptually:

```text
Hermes connection advertises `general`
        ↓
Open WebUI Model record `general`
        ↓
read grant → All Employees group
        ↓
ordinary employee sees General Assistant
```

A specialist model without a read grant to an employee's groups remains unavailable to that employee.

This authorization must also be tested through direct API requests; UI visibility alone is not sufficient.

## 11. Verify employee visibility

Sign in as an ordinary test employee and call:

```text
GET /api/v1/models
```

Expected baseline:

```text
General employee
→ sees `general`
→ does not see privileged/default admin
→ does not see ungranted specialist models
```

For each specialist group, verify the positive and negative model matrix derived from company configuration.

Attempt a direct chat/resource request to an unauthorized model and require fail-closed behavior.

## 12. Verify employee UI

API provisioning is not final acceptance.

Use the actual browser employee UI and verify Part A / applicable Part B of `docs/ACCEPTANCE-TESTS.md`:

- login;
- Assistant visibility;
- grounded answer/source through Hermes → WeKnora;
- follow-up/history;
- file upload when enabled;
- no System Prompt/Advanced Params editing under baseline permissions;
- no admin/provider/API-key controls;
- unauthorized Assistant inaccessible.

## 13. Existing deployments

For an existing Open WebUI database:

- inspect before mutation;
- preserve unrelated legitimate users/groups/connections/models;
- reconcile only resources owned by the Enterprise AI Office company configuration;
- do not reset the data volume merely to obtain a clean provisioning state.

## 14. SSO deployments

When SSO is enabled:

1. configure the selected native Open WebUI OIDC/OAuth mechanism from `infrastructure/access/README.md`;
2. allow the enterprise identity flow to create/resolve the human user according to company policy;
3. map/assign the user to the intended Open WebUI groups;
4. keep Model/Assistant ACL provisioning exactly as described above;
5. test both an authorized and unauthorized enterprise identity.

SSO changes how a human identity enters Open WebUI; it does not remove Assistant/Profile authorization.

## 15. Completion evidence

Consume Hermes Profile → API route/model identity and company group logical IDs
from the protected operational state created from
`state/DEPLOYMENT-STATE.template.md`. Resolve Profile API-key **values** only
from protected secret storage.

After reconciliation, write the logical-group/runtime-UUID and
Profile/model/ACL mappings back to that same protected operational record.

Record, without secrets:

```text
Open WebUI version
admin bootstrap method
group IDs/names
employee identity method
Hermes Profile connection URLs at non-secret level
employee-visible Model IDs/display names
group → Model grants
EAO-managed Open WebUI native company Knowledge attachments: none
ordinary employee permission baseline
acceptance result
```

Do not record API keys, admin passwords, employee passwords, or bearer tokens.
