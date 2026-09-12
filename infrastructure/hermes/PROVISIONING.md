# Hermes Core Provisioning Contract

This playbook turns the active Enterprise AI Office company configuration into
the baseline Hermes control plane plus employee-facing `general` Profile.

It is written against the validated Hermes Agent baseline in
`config/validated-stack.yaml`. Acquire and verify the exact runtime through
`DEPLOY.md §4.1–4.2` before applying this contract.

This is a reconciliation contract around upstream Hermes capabilities. It does
not replace Hermes Profile management, Gateway management, or configuration
semantics.

## 1. Completion contract

Hermes Core provisioning is complete only when the deployment agent can prove:

```text
validated Hermes source/version
→ default/admin control plane retained
→ general Profile exists
→ general Profile opted out of bundled Skill seeding
→ default gateway multiplexes only explicitly allowed employee Profiles
→ default owns the shared API listener
→ general has its own API credential
→ general has no independent API listener
→ general exposes only the approved WeKnora MCP tool surface
→ employee long-term memory remains disabled
→ /p/general/v1/models advertises general
→ general credential works only on general
→ default/admin credential does not grant general
→ gateway restart preserves the same boundary
```

Service health alone is not completion.

## 2. Required inputs

Resolve before mutation.

From the active company configuration:

```text
agent_runtime.multi_profile_gateway
profiles[]
mcp_control_plane.profile_allowlists
models.hermes.provider
models.hermes.default_model
models.hermes.credential_refs
core_network.hermes.shared_listener.bind_host
core_network.hermes.shared_listener.port
core_network.hermes.open_webui_backend_base_url
core_network.hermes.employee_exposed_directly
core_network.weknora.api_base_url_for_hermes
core_provisioning.hermes.default_api_key_ref
core_provisioning.hermes.profile_api_key_refs
```

For the reusable baseline, the required employee Profile is:

```text
general
```

Resolve the symbolic Profile API-key refs through `secret_refs` and protected
storage. Both the default/admin and named Profile bindings use Hermes' native
`API_SERVER_KEY`, but they must resolve to distinct values.

Resolve model-provider authentication separately from Profile API
authentication. For the selected Hermes provider, inspect the pinned 0.21.0
`PROVIDER_REGISTRY` / provider catalog. When that provider uses an API key,
each declared `models.hermes.credential_refs[]` entry must exist in
`secret_refs`, use `class: model-provider-credentials`, and name a
`native_binding` accepted by that pinned provider (for example,
`openai-api` accepts `OPENAI_API_KEY`). If the selected provider is
keyless or uses a supported OAuth/account flow, an empty API-key ref list is
valid and the upstream native auth flow remains authoritative.

From protected deployment input:

```text
secret value referenced by core_provisioning.hermes.default_api_key_ref
secret value referenced by core_provisioning.hermes.profile_api_key_refs.general
secret values referenced by models.hermes.credential_refs when the selected provider requires them
selected provider-native OAuth/account authorization when applicable
general WeKnora retrieve-only API key
absolute path to the selected WeKnora MCP server runtime
```

Do not place secret values in company YAML, repository templates, deployment
state, shell history, or logs.

The shared bind address/port, Open WebUI-backend route to Hermes, and WeKnora
API base URL are non-secret desired state from `core_network`. Do not silently
fall back to `8642`, `0.0.0.0`, `host.docker.internal`, or a reference
WeKnora URL when those fields are unresolved.

The reusable baseline keeps `core_network.hermes.employee_exposed_directly:
false`; Open WebUI is the employee surface.

If any required protected input is unresolved, stop with:

```text
BLOCKED — REQUIRED INPUT: <specific item>
```

## 3. Inspect before mutation

Confirm the installed runtime first:

Resolve the Hermes source checkout using `config/validated-stack.yaml` and the
pinned installer's path rules. Record the resolved non-secret path in protected
operational state; do not infer it from the ARMOR host.

```sh
hermes --version
hermes profile list
```

The version must match `config/validated-stack.yaml`.

Inspect the default Profile and any existing `general` Profile:

```sh
hermes profile show default
hermes profile show general
```

A missing `general` Profile is expected on a fresh deployment. On an existing
deployment, inspect and reconcile it in place.

Never delete/recreate an existing Profile merely to obtain a clean state. That
can destroy sessions, state, cron jobs, Skills, memory, and local configuration.

### 3.1 Pinned Hermes behavior provenance

The provisioning behaviors below were verified against the validated Hermes
Agent source commit recorded in `config/validated-stack.yaml`:

```text
NousResearch/hermes-agent
commit: f1ccf436a27522c1bb5d36383a6f13b950676338
package version at commit: 0.21.0
```

Source files used for behavior verification:

```text
hermes_cli/subcommands/profile.py
hermes_cli/profiles.py
gateway/config.py
gateway/platforms/api_server.py
```

At that commit:

- `hermes profile create --no-skills` is a supported upstream CLI option;
- `profiles.py` writes `.no-bundled-skills` and future bundled-Skill sync
  honors the opt-out marker;
- `gateway.multiplex_profiles` and
  `gateway.multiplex_profile_allowlist` are supported config keys;
- the API server mirrors native routes under `/p/<profile>/...` when
  multiplexing is enabled;
- named Profile requests resolve that Profile's own `API_SERVER_KEY` and fail
  closed rather than inheriting the default/owner key;
- `GET /p/<profile>/v1/models` advertises the active Profile name as the
  primary model ID unless an explicit override is configured.

These behaviors are version-specific implementation contracts. On a Hermes
upgrade, re-read the selected commit's Profile/config/API-server implementation
and rerun Profile creation, multiplex routing, credential-isolation, model-ID,
tool-boundary, and restart acceptance before inheriting this playbook.

## 4. Create the baseline employee Profile only when absent

Hermes Profiles are native upstream state directories. Use the upstream command;
do not create `~/.hermes/profiles/general` manually.

For a fresh `general` Profile:

```sh
hermes profile create general --no-skills --no-alias
```

Why `--no-skills` is required for the reusable baseline:

- Hermes normally seeds bundled Skills into a new Profile.
- EAO `general` is a least-privilege employee knowledge Profile.
- Its baseline API tool surface is the approved WeKnora MCP surface, not the
  full bundled Skill catalog.
- The upstream `.no-bundled-skills` marker also prevents a later
  `hermes update` from silently re-seeding bundled Skills into this Profile.

Verify:

```sh
test -d "${HOME}/.hermes/profiles/general"
test -f "${HOME}/.hermes/profiles/general/.no-bundled-skills"
hermes profile show general
```

If the adopting company explicitly enables additional General Assistant
capabilities later, add only the approved Skill/tool boundary from the
capability contract. Do not remove the opt-out marker merely for completeness.

## 5. Reconcile the default/admin control plane

The default Profile is privileged control-plane state. It is not an ordinary
employee Assistant.

Use `infrastructure/hermes/default.config.example.yaml` as the EAO-owned
configuration fragment.

Required baseline:

```yaml
gateway:
  multiplex_profiles: true
  multiplex_profile_allowlist:
    - general
```

When specialist Profiles are explicitly enabled, add only those Profile IDs to
the allowlist.

### Existing default config

Do not overwrite an existing `~/.hermes/config.yaml` with the example file.
Read the existing config and reconcile only the EAO-owned gateway keys while
preserving unrelated approved settings.

The upstream CLI supports the boolean switch:

```sh
hermes config set gateway.multiplex_profiles true
```

For the allowlist, reconcile the selected Profile IDs against the current
`config.yaml` using the installed Hermes schema. The final effective value,
not the editing method, is authoritative.

### Default secret scope

Use `infrastructure/hermes/default.env.example` as the secret-shape reference.

The protected default `.env` must provide:

```text
API_SERVER_ENABLED=true
API_SERVER_KEY=<distinct privileged control-plane key>
API_SERVER_PORT=<selected shared listener port>
API_SERVER_HOST=<selected trusted bind address>
```

The validated reusable example uses port `8642`, but the active deployment
configuration is authoritative.

Keep file permissions restrictive. Do not copy the default key into any named
Profile.

## 6. Reconcile the `general` Profile config

Render/adapt `infrastructure/hermes/general.config.example.yaml` into:

```text
~/.hermes/profiles/general/config.yaml
```

Resolve the placeholders from the active company/protected configuration:

```text
<SELECT_PROVIDER>
<SELECT_MODEL>
<ABSOLUTE_WEKNORA_MCP_SERVER_DIRECTORY>
```

Required baseline semantics:

### Model

```yaml
model:
  provider: <company-selected provider>
  default: <company-selected model>
```

Do not silently choose a provider/model because one happens to be available.
Do not guess provider credential variable names. For API-key providers, bind
only the declared symbolic refs whose `native_binding` is accepted by the
pinned Hermes provider registry.

### Memory

```yaml
memory:
  memory_enabled: false
  user_profile_enabled: false
```

Do not enable employee long-term memory until the exact deployed
Open WebUI → Hermes user/session isolation path passes the documented cross-user
acceptance test.

### Employee API tool surface

The EAO baseline must expose only the approved dynamic MCP toolset:

```yaml
platform_toolsets:
  api_server:
    - mcp-weknora
```

Do not add terminal, unrestricted filesystem, Docker, coding-agent, or generic
browser toolsets to `general`.

### WeKnora MCP

Use the configured read-only WeKnora MCP server and keep the include list
limited to the approved retrieval operations in
`general.config.example.yaml`.

The runtime credential behind that MCP server must independently be
retrieve-only and Knowledge-Base-scoped. Hermes tool whitelisting and WeKnora
credential scoping are both required.

## 7. Reconcile the `general` secret scope

Use `infrastructure/hermes/general.env.example` as the shape reference.

The protected Profile `.env` must contain:

```text
API_SERVER_KEY=<distinct general Profile key>
WEKNORA_API_KEY=<retrieve-only KB-scoped key>
WEKNORA_BASE_URL=<deployed WeKnora API-v1 root>
<resolved models.hermes.credential_refs at their exact pinned-provider native bindings, when required>
```

Do **not** set `API_SERVER_ENABLED=true` on `general` in the multiplex
baseline. The default Profile owns the shared listener.

Do not copy the default/admin API key into `general`.

The model-provider secret value is available only to Profiles whose rendered
model configuration actually uses that provider. A symbolic ref name or generic
`model-provider-credentials` class is not enough: the exact native binding
must be compatible with the selected pinned provider.

## 8. Reconcile the General Assistant SOUL

Render:

```text
profiles/general/SOUL.md
```

into:

```text
~/.hermes/profiles/general/SOUL.md
```

Replace `<COMPANY_NAME>` with the active company display name.

Do not put changing product/company facts into SOUL. Those belong in WeKnora.

If the SOUL already exists on an established deployment, review differences
before replacement. Preserve approved company-specific behavior that does not
violate the current Profile/security contract.

## 9. Start or restart only the shared gateway

In multiplex mode, the default Profile owns the gateway process.

After reconciliation, use the supported upstream gateway lifecycle for the
target host, for example:

```sh
hermes gateway restart
hermes status
```

On a new host with no running gateway, start/install it through the supported
Hermes gateway lifecycle appropriate to the requested readiness level.

Do **not** start a second gateway for `general` while the default multiplexer
serves it.

For Production Ready, persistent startup/recovery behavior remains governed by
`docs/ACCEPTANCE-TESTS.md` and `docs/OPERATIONS.md`.

## 10. Verify Profile inventory and served set

Run:

```sh
hermes profile list
hermes profile show general
hermes status
```

Require:

```text
default exists
general exists
general is in the multiplex served set
no undeclared employee Profile is served
```

If the active company configuration enables specialists, compare the complete
served set with the explicit desired-state Profile list.

Repository file presence does not authorize serving a Profile.

## 11. Verify the shared API route

For Hermes Agent 0.21.0, the default shared API listener exposes a named Profile
under:

```text
/p/<profile>/...
```

The `general` OpenAI-compatible root is therefore:

```text
http://<trusted-host>:<shared-port>/p/general/v1
```

The upstream 0.21.0 API server resolves the primary `/v1/models` ID from the
active named Profile under a `/p/<profile>/` request. Therefore:

```text
GET /p/general/v1/models
→ primary model id = general
```

No separate `API_SERVER_MODEL_NAME=general` override is required for this
validated baseline.

## 12. Verify credential isolation

Use protected shell variables or an equivalent secret-safe test harness. Do not
print key values.

Positive test:

```sh
curl -fsS \
  -H "Authorization: Bearer ${GENERAL_API_KEY}" \
  "http://<trusted-host>:<shared-port>/p/general/v1/models"
```

Require HTTP success and a primary model ID of `general`.

Negative tests:

```text
general key → unprefixed/default privileged API     DENY
default/admin key → /p/general/...                  DENY
invalid key → /p/general/...                        DENY
```

When multiple employee Profiles are enabled, run the complete pairwise
credential matrix:

```text
for each Profile A:
  A key → A route                 PASS
  A key → every other route      DENY
```

Any unintended cross-Profile acceptance is a blocker.

## 13. Verify effective tool boundary

From the employee-facing `general` route, verify the effective API toolset.

Required baseline:

```text
approved WeKnora retrieval MCP tools     present
terminal                                 absent
unrestricted filesystem                  absent
Docker/system administration             absent
coding-agent delegation                   absent
generic browser                           absent
```

Then request a harmless disallowed action and prove no unapproved tool call is
made.

This is an effective-runtime test. Merely inspecting YAML is not sufficient.

## 14. Verify company knowledge through Hermes

After WeKnora provisioning has passed, query the same non-sensitive seed fact
through `general`.

Require:

```text
general
→ approved WeKnora MCP
→ intended Knowledge Base
→ expected fact
→ human-readable source evidence
```

A direct WeKnora success with a broken Hermes bridge does not satisfy Core.

## 15. Existing deployments

For an existing Hermes installation:

- inspect before mutation;
- do not recreate `general`;
- do not replace the whole default config;
- preserve unrelated approved provider/gateway settings;
- preserve sessions and state;
- reconcile only EAO-owned fields and secret bindings;
- restart only after the proposed effective configuration is understood;
- rerun Profile/API/tool/knowledge acceptance after every material Profile,
  MCP, model, Skill, SOUL, Gateway, or credential change.

If an existing Profile has bundled Skills that conflict with the intended
least-privilege boundary, do not blindly delete files. Inventory them, determine
ownership, disable/remove only the unapproved surface through supported Hermes
mechanisms, then re-run effective tool acceptance.

## 16. Completion evidence

Consume the WeKnora logical/runtime KB mapping and retrieval credential record
metadata from the protected operational state created from
`state/DEPLOYMENT-STATE.template.md`. Resolve secret **values** only from the
protected secret store/Profile `.env`.

After reconciliation, write the Hermes route/model/served-set handoff back to
that same protected operational record for Open WebUI provisioning.

Record without secrets:

```text
Hermes package version
Hermes source commit
Hermes source checkout path
default Profile path
general Profile path
general no-bundled-skills marker present
effective multiplex setting
effective multiplex allowlist
shared API bind host/port at non-secret level
employee Profile IDs
Profile → API route mapping
Profile → advertised model ID
Profile → non-secret credential reference name/identifier
Profile → MCP server names
Profile → Knowledge Base logical scopes
Profile → resolved WeKnora runtime KB IDs
effective employee tool boundary
memory policy
credential isolation result
seed retrieval result
gateway restart/persistence result
```

Never record plaintext API keys, provider tokens, WeKnora keys, or private
employee data.

## 17. Final rule

A Hermes Core deployment is not complete because:

- `hermes` is installed;
- a Profile directory exists;
- the gateway process is running;
- the config file looks correct.

It is complete only when the actual shared gateway serves exactly the intended
Profile set, each Profile authenticates with its own credential, `general`
exposes only its approved tool boundary, and the employee knowledge path works
with source evidence.
