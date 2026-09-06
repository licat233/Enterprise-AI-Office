# Open WebUI Provisioning Playbook

This playbook turns the Enterprise AI Office company configuration into Open WebUI users/groups, Hermes-backed model resources, and access grants without requiring a deployment operator to click through the UI manually.

It is pinned conceptually to the first validated Open WebUI core version (`v0.11.3`, commit recorded in `config/validated-stack.yaml`). Before using it with another release, verify the exact routes/forms against that selected upstream version.

Use this after the Open WebUI container is healthy and the Hermes employee Profile APIs are reachable from the Open WebUI container.

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

## 2. Required protected inputs

Resolve without printing or committing:

```text
OPEN_WEBUI_URL
OPEN_WEBUI_ADMIN_EMAIL
OPEN_WEBUI_ADMIN_PASSWORD

for each enabled employee Profile:
  Profile ID
  employee-facing display name
  Hermes OpenAI-compatible base URL
  Profile API key
  allowed Open WebUI group IDs/names
```

Baseline:

```text
Profile ID: general
Display name: General Assistant
Allowed group: All Employees
Hermes URL: http://host.docker.internal:8642/p/general/v1
```

Exact host/port may differ by deployment.

## 3. Use the native admin API

The validated Open WebUI release exposes supported application APIs that the admin UI itself uses. Prefer these over direct database writes.

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
POST /api/v1/models/model/update?id=<model_id>   # verify exact route before reuse on another version

GET  /api/models
GET  /api/v1/models
```

All modifying operations below require an authenticated administrator token.

Do not write directly to Open WebUI's SQLite/PostgreSQL tables for normal provisioning.

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

Do not blindly create duplicate groups.

For every group declared by company configuration:

1. `GET /api/v1/groups/`;
2. match by intended name or previously recorded group ID;
3. create only when absent;
4. record the resulting stable group ID in deployment state/protected provisioning state.

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

Baseline groups:

```text
All Employees
AI Administrators
```

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

For a Hermes employee Profile, use a narrow config such as:

```json
{
  "enable": true,
  "model_ids": ["general"]
}
```

where `general` is the exact model name advertised by the Hermes Profile API. For a specialist Profile use its own unique model ID.

Then submit the reconciled complete object:

```http
POST /openai/config/update
Authorization: Bearer <ADMIN_TOKEN>
Content-Type: application/json
```

Each Hermes Profile connection uses its own Profile API key. Do not connect the privileged Hermes default/admin Profile to the employee client.

After updating, verify the admin can see the expected upstream model IDs through `/openai/models` or `/api/models`.

## 8. Create the employee-visible Model/Assistant ACL record

For the validated Open WebUI version, a raw upstream model without a corresponding Models DB entry is admin-only when model access control is enforced.

For each enabled employee Profile, create a Model record **with the same model ID advertised by Hermes**. A Model record whose `id` matches a base model and has `base_model_id: null` acts as metadata/access-control override for that base model.

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

## 9. Idempotent update behavior

Before creating a Model record, query the existing resource:

```http
GET /api/v1/models/model?id=<MODEL_ID>
Authorization: Bearer <ADMIN_TOKEN>
```

If it exists, reconcile name/metadata/access grants through the exact update route supported by the selected pinned release rather than creating a duplicate.

For Open WebUI v0.11.3, inspect `backend/open_webui/routers/models.py` before scripting the update call; do not assume an update route from another release.

The deployment agent should preserve unrelated administrator-curated metadata unless company configuration intentionally owns it.

## 10. Why the ACL record matters

With `BYPASS_MODEL_ACCESS_CONTROL=false`, Open WebUI filters ordinary-user model visibility against its Models records and access grants.

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

API provisioning is not the final acceptance.

Use the actual browser employee UI and verify Part A / applicable Part B of `docs/ACCEPTANCE-TESTS.md`:

- login;
- Assistant visibility;
- grounded answer/source;
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

Record, without secrets:

```text
Open WebUI version
admin bootstrap method
group IDs/names
employee identity method
Hermes Profile connection URLs at non-secret level
employee-visible Model IDs/display names
group → Model grants
ordinary employee permission baseline
acceptance result
```

Do not record API keys, admin passwords, employee passwords, or bearer tokens.
