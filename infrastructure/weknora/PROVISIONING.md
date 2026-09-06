# WeKnora Machine Provisioning Contract

This playbook turns the Enterprise AI Office company configuration into a reconciled WeKnora runtime without requiring an operator to click through the WeKnora UI.

It is written against the first validated core baseline:

```text
Tencent/WeKnora v0.8.0
commit 1edcd54b43606d9079bb36650efe3f68707a79ea
```

Use the exact selected release. If a deployment deliberately upgrades WeKnora, verify the affected routes and payloads against that release before reusing this contract.

This file is an execution contract, not a second WeKnora implementation. Prefer WeKnora's supported REST API and official MCP server. Do not write directly to its database.

## 1. Completion contract

Provisioning is complete only when the deployment agent can prove this chain:

```text
protected WeKnora owner/admin identity
→ reconcile required model(s)
→ reconcile company-declared Knowledge Base(s)
→ ingest a non-sensitive seed document
→ wait for parsing/indexing to complete
→ retrieve the known seed fact with source evidence
→ create Profile-specific read-only retrieval credential(s)
→ connect Hermes through the supported WeKnora MCP server
→ retrieve the same fact from the intended Hermes Profile
→ prove the runtime retrieval credential cannot mutate WeKnora
→ record runtime IDs and acceptance evidence without recording secrets
```

Service health alone is not completion.

## 2. Inputs

Resolve these inputs before mutation.

From the active company configuration:

```text
company-defined Knowledge Bases
Profile → Knowledge Base mappings
selected WeKnora embedding provider/model/dimension
optional rerank configuration, only when enabled
```

From protected deployment input/secret storage:

```text
WeKnora API base URL
WeKnora owner/admin login needed for provisioning
selected model-provider credential(s)
provider-specific endpoint/config only when the selected provider requires it
protected destination for generated Hermes retrieval keys
```

The owner email/password and temporary JWT are provisioning credentials. They are not Hermes runtime credentials and must not be copied into a Profile `.env`.

`WEKNORA_BASE_URL` and `WEKNORA_API_KEY` are real environment variables consumed by the official WeKnora MCP server. Other shell variable names shown in this document are local orchestration conveniences only; WeKnora does not read them unless upstream documentation explicitly says so.

If a required provider, model, credential, or target Knowledge Base definition is unresolved, report:

```text
BLOCKED — REQUIRED INPUT: <specific item>
```

Do not silently choose another provider or invent a company knowledge boundary.

## 3. Pinned v0.8.0 API surface used by this contract

The validated v0.8.0 source exposes the following supported routes under `/api/v1`:

```text
Authentication
POST /auth/login
GET  /auth/me
GET  /tenants

Models
GET  /models/providers
GET  /models
POST /models
GET  /models/:id
PUT  /models/:id

Knowledge Bases
GET  /knowledge-bases
POST /knowledge-bases
GET  /knowledge-bases/:id
PUT  /knowledge-bases/:id
POST /knowledge-bases/:id/hybrid-search

Knowledge
POST /knowledge-bases/:id/knowledge/file
POST /knowledge-bases/:id/knowledge/url
POST /knowledge-bases/:id/knowledge/manual
GET  /knowledge-bases/:id/knowledge
GET  /knowledge/:id
POST /knowledge/:id/reparse

Tenant API keys
GET    /tenants/:id/api-keys
POST   /tenants/:id/api-keys
PUT    /tenants/:id/api-keys/:key_id
DELETE /tenants/:id/api-keys/:key_id
```

For new retrieval integrations use `POST /knowledge-bases/:id/hybrid-search`; the legacy GET-with-body compatibility path is not the Enterprise AI Office default.

## 4. Authenticate for provisioning

### 4.1 Check the deployed API

Confirm the WeKnora application and required internal services are healthy using the selected upstream deployment and `infrastructure/weknora/README.md`.

Set a local orchestration variable to the API-v1 root, for example:

```bash
BASE='http://127.0.0.1:18080/api/v1'
```

The exact host/port belongs to the deployment.

### 4.2 Obtain an Owner/admin bearer token

For a standard server deployment, use the protected WeKnora owner/admin account supplied for the company deployment:

```http
POST <BASE>/auth/login
Content-Type: application/json

{
  "email": "<OWNER_EMAIL_FROM_PROTECTED_INPUT>",
  "password": "<OWNER_PASSWORD_FROM_PROTECTED_INPUT>"
}
```

Capture the returned bearer `token` in process memory/protected temporary state and use:

```text
Authorization: Bearer <OWNER_TOKEN>
```

for provisioning calls that require human/Owner authority, especially API-key management.

Do not print the token, commit it, or persist it in Hermes.

The v0.8.0 `/auth/auto-setup` path is Lite-edition-specific. Do not use it as the generic server bootstrap path. If a fresh standard deployment has no authorized owner/admin identity yet, creation/authorization of that identity is a genuine bootstrap input and must follow the selected upstream deployment policy.

### 4.3 Resolve the target tenant/workspace

Use the tenant returned by login and/or:

```http
GET <BASE>/tenants
Authorization: Bearer <OWNER_TOKEN>
```

A dedicated company WeKnora deployment normally has one intended active workspace.

Do not guess when the owner belongs to multiple plausible workspaces. Resolve the intended tenant from protected deployment state/company-specific configuration or report:

```text
BLOCKED — REQUIRED INPUT: target WeKnora workspace is ambiguous
```

Record the resulting runtime tenant ID in deployment state. Do not put it into generic company templates as a permanent cross-deployment ID.

## 5. Reconcile model configuration

The public company example intentionally declares model intent rather than hard-coding a provider endpoint or runtime model UUID.

### 5.1 Resolve the selected provider against upstream

For each required WeKnora model role, query the installed release rather than maintaining a second provider catalog:

```http
GET <BASE>/models/providers?model_type=embedding
Authorization: Bearer <OWNER_TOKEN>
```

Use the selected provider from company configuration. If the provider exposes an upstream default URL, use it unless protected company configuration deliberately overrides it. A custom/generic provider may require an explicit approved base URL.

Never substitute another provider merely because the configured provider is unavailable.

### 5.2 Required baseline model

The baseline employee retrieval path requires the configured embedding model.

Create/update other roles only when the selected WeKnora features actually require them, for example:

```text
Rerank      only when models.weknora.rerank.enabled == true
KnowledgeQA only when a selected WeKnora feature needs a chat/summary model
VLLM/ASR    only for explicitly enabled multimodal/audio behavior
```

Do not install optional local models or extra model infrastructure for completeness.

### 5.3 Idempotent model reconciliation

For each required model:

1. `GET /models`;
2. prefer a previously recorded runtime model ID when it still resolves correctly;
3. otherwise match the intended model by model type + configured upstream model name + selected provider/source;
4. if exactly one matching model exists, adopt it;
5. if none exists, create it;
6. if multiple plausible matches exist, stop with `BLOCKED — AMBIGUOUS STATE` rather than binding a Knowledge Base arbitrarily;
7. update only company-managed drift and preserve unrelated approved models.

A remote embedding model uses the upstream-native shape, for example:

```json
{
  "name": "<CONFIGURED_MODEL_ID>",
  "type": "Embedding",
  "source": "remote",
  "description": "Enterprise AI Office managed embedding model",
  "parameters": {
    "base_url": "<SELECTED_PROVIDER_ENDPOINT>",
    "api_key": "<PROTECTED_PROVIDER_CREDENTIAL>",
    "provider": "<CONFIGURED_PROVIDER>",
    "embedding_parameters": {
      "dimension": 1024,
      "truncate_prompt_tokens": 0
    }
  }
}
```

`1024` above is only an API-shape example. The deployment must use the verified dimension from the selected model, never copy that example value blindly.

WeKnora masks stored provider secrets in read responses. Do not overwrite a valid stored secret with a masked/empty value during reconciliation. Update the secret only when the protected deployment input intentionally provides a replacement.

Record the resulting runtime model ID, provider, model name, source, and verified embedding dimension. Do not record the provider API key.

## 6. Reconcile Knowledge Bases

Company configuration uses logical Knowledge Base identifiers such as `company-general`. WeKnora generates its own runtime UUIDs. Maintain a deployment-state mapping instead of hard-coding runtime UUIDs into the generic repository.

For every company-declared Knowledge Base:

1. if deployment state contains a logical-ID → runtime-ID mapping, `GET /knowledge-bases/:id` and validate it;
2. if the mapping is absent/stale, `GET /knowledge-bases` and exact-match the intended company-defined name;
3. exactly one match: adopt it and record the mapping;
4. no match: create it;
5. multiple plausible matches: stop with `BLOCKED — AMBIGUOUS STATE`;
6. reconcile only fields controlled by active company configuration;
7. preserve unrelated Knowledge Bases and optional upstream settings not owned by this deployment contract.

A minimal document Knowledge Base can be created with the selected embedding model and upstream defaults, for example:

```json
{
  "name": "Company Knowledge",
  "description": "Shared company information approved for employee use.",
  "type": "document",
  "is_temporary": false,
  "embedding_model_id": "<RESOLVED_EMBEDDING_MODEL_RUNTIME_ID>"
}
```

Do not add a dedicated vector database, reranker, graph extractor, VLM, ASR, external object store, or custom parser unless active company configuration/requirements justify it.

### Embedding-model drift

Treat changing the embedding model of a populated Knowledge Base as a migration, not an ordinary idempotent update.

If an existing populated Knowledge Base is bound to a different embedding model/dimension than the requested target:

```text
BLOCKED — MIGRATION REQUIRED
```

until an explicit reindex/migration plan and recovery point are approved. Do not silently invalidate existing retrieval data.

## 7. Ingest and wait for a seed document

Before connecting Hermes, validate WeKnora itself with a small non-sensitive source containing a fact that cannot be guessed accidentally.

Prefer an approved company seed document when one is supplied. Otherwise generate a harmless synthetic validation file in protected temporary workspace, for example:

```text
Enterprise AI Office WeKnora provisioning validation.
Validation marker: EAO-WEKNORA-<UNIQUE_NON_SECRET_MARKER>
```

Upload through the supported file-ingestion API so the test exercises source-file storage and parsing:

```bash
curl -fsS \
  -H "Authorization: Bearer $OWNER_TOKEN" \
  -F 'file=@/protected/tmp/eao-weknora-seed.txt' \
  "$BASE/knowledge-bases/$KB_ID/knowledge/file"
```

Capture the returned knowledge ID.

The v0.8.0 parser status is asynchronous. Poll:

```http
GET <BASE>/knowledge/<KNOWLEDGE_ID>
Authorization: Bearer <OWNER_TOKEN>
```

until `parse_status` reaches a terminal state.

Successful terminal state:

```text
completed
```

Non-terminal states include:

```text
pending
processing
finalizing
```

Failure terminal states include:

```text
failed
cancelled
```

Use a bounded polling deadline. On failure, capture the non-secret error/status evidence and stop; do not loop forever or declare Core Ready.

For repeat runs, inspect existing knowledge first and avoid blindly creating duplicate validation documents. Reuse an existing deployment-owned seed only when its identity/content is known. Otherwise use a new unique harmless marker and clean it up with the provisioning identity after acceptance if company policy does not want validation material retained.

## 8. Validate hybrid retrieval and source evidence

After parsing completes, query the target Knowledge Base:

```http
POST <BASE>/knowledge-bases/<KB_ID>/hybrid-search
Authorization: Bearer <OWNER_TOKEN>
Content-Type: application/json

{
  "query_text": "What is the WeKnora provisioning validation marker?",
  "match_count": 10
}
```

PASS requires:

```text
known marker/fact is present in a relevant result
source fields identify the seed knowledge/file in human-readable form
result belongs to the intended Knowledge Base
```

Typical v0.8.0 result evidence includes `knowledge_title`, `knowledge_filename`, `knowledge_source`, and `knowledge_id`.

Do not proceed to Hermes merely because the document upload endpoint returned success.

## 9. Create least-privilege Hermes retrieval credentials

The v0.8.0 tenant API-key model supports capability and Knowledge Base scoping.

For each employee-facing Hermes Profile that needs company knowledge, create or reconcile a distinct runtime retrieval key whose scope equals that Profile's configured Knowledge Base set.

Baseline `general` payload:

```http
POST <BASE>/tenants/<TENANT_ID>/api-keys
Authorization: Bearer <OWNER_TOKEN>
Content-Type: application/json

{
  "name": "enterprise-ai-office-hermes-general",
  "full_access": false,
  "knowledge_base_ids": ["<COMPANY_GENERAL_RUNTIME_KB_ID>"],
  "capabilities": ["retrieve"]
}
```

Critical rules:

- `full_access` must be `false` for normal employee retrieval Profiles;
- `capabilities` should contain only `retrieve` for the baseline knowledge bridge;
- `knowledge_base_ids` must be the explicit non-empty runtime allow-list for that Profile;
- an empty Knowledge Base list is not the least-privilege baseline because it does not express the intended KB boundary;
- do not share one broad retrieval key across Profiles with different knowledge scopes;
- keep the returned plaintext token only in protected secret storage/Profile `.env`;
- record key ID/name/scope metadata, never the token value.

### Idempotent key reconciliation

Before creating a key, list existing keys for the tenant and reconcile by the deployment-managed key name plus expected scope.

If an existing key has the correct scope and its plaintext token is still available in protected secret storage, reuse it.

If metadata drift exists and the stored token is available, use the supported update route rather than creating duplicates.

If the key record exists but its plaintext token has been lost, do not try to recover a secret from masked/list responses. Rotate it: create a replacement key, update and validate the Hermes Profile, then revoke the old key. Avoid leaving orphaned broad credentials.

## 10. Prove the retrieval credential fails closed

Before placing the key into Hermes, test the runtime credential directly.

Allowed operation:

```text
POST /knowledge-bases/<ALLOWED_KB_ID>/hybrid-search → PASS
```

Denied operation:

```text
attempt a harmless write endpoint with the runtime key
→ authorization denied
→ no resource created/modified
```

For example, the retrieval-only key must not be able to create a Knowledge Base or ingest/update/delete company knowledge.

When another Knowledge Base exists outside the Profile's configured allow-list, also verify retrieval against that KB fails. If no second KB exists, record the cross-KB probe as N/A and preserve evidence that the key's `knowledge_base_ids` allow-list is explicit and non-empty.

A Hermes MCP tool whitelist is defense in depth; it does not replace this backend credential test.

## 11. Connect the official WeKnora MCP server to Hermes

The validated WeKnora release includes the official MCP server. It consumes:

```text
WEKNORA_BASE_URL
WEKNORA_API_KEY
```

The existing Enterprise AI Office Hermes Profile templates already wire these values and expose only approved read-only tools.

For reproducibility, the baseline may run the MCP server from the same pinned WeKnora v0.8.0 checkout used by the deployment. Do not silently point the Profile at a floating upstream checkout.

Populate each Profile's protected `.env`:

```text
WEKNORA_BASE_URL=<DEPLOYED_WEKNORA_API_V1_URL>
WEKNORA_API_KEY=<PROFILE_SPECIFIC_RETRIEVE_ONLY_KEY>
```

Use the Profile's existing config template, for example `infrastructure/hermes/general.config.example.yaml`, whose baseline allow-list contains read-only WeKnora tools such as:

```text
list_knowledge_bases
get_knowledge_base
hybrid_search
list_knowledge
get_knowledge
list_chunks
```

Do not expose the MCP server's write/model/admin tools to a normal employee Profile merely because upstream implements them.

Restart/reload Hermes using the supported selected Hermes procedure, then inspect the effective Profile toolset rather than assuming the template was applied.

## 12. End-to-end Hermes acceptance

From the intended employee-facing Profile, ask for the seed marker/fact.

PASS requires:

```text
Profile reaches the intended WeKnora Knowledge Base
same known fact/marker is returned
human-readable source/document context is available
no unauthorized Knowledge Base is exposed
no WeKnora write/admin tool appears in the effective normal Profile toolset
```

Then run the relevant Part A checks in `docs/ACCEPTANCE-TESTS.md` through the real Open WebUI employee client.

Direct API/MCP success does not replace employee-client acceptance.

## 13. Reconciliation rules

Every rerun follows these rules:

```text
read current state first
→ match/adopt existing intended resources
→ create only missing resources
→ update only owned drift
→ preserve unrelated resources
→ never delete merely because a resource is absent from an example
→ never write the database directly
→ never copy runtime IDs from a reference deployment
→ never replace protected secrets with masked values
```

Destructive cleanup, embedding-model migration, tenant deletion, or broad credential revocation is not part of ordinary idempotent provisioning.

If current runtime state conflicts with company intent in a way that cannot be resolved safely, stop with a specific blocker rather than forcing convergence.

## 14. Deployment-state record

Record at least:

```text
WeKnora version + commit
API/admin access boundary
runtime tenant/workspace ID
logical KB ID → runtime KB ID mapping
KB purpose/type/embedding-model binding
embedding provider/model/dimension
optional rerank state
seed-ingestion result
hybrid-retrieval/source-evidence result
for each Hermes Profile:
  retrieval key record ID/name (not token)
  capability set
  allowed runtime KB IDs
  MCP implementation/version/path
  credential-denial result
  Hermes retrieval result
```

Do not record:

```text
owner password
JWT/refresh token
model-provider API key
WeKnora API-key plaintext token
```

## 15. Acceptance gate

WeKnora provisioning passes only when all applicable checks below are true:

```text
[ ] exact selected WeKnora version/commit recorded
[ ] required services healthy and internal dependencies privately exposed
[ ] owner/admin provisioning authentication succeeds
[ ] target tenant/workspace unambiguous
[ ] required provider/model reconciled without duplicate creation
[ ] verified embedding dimension recorded
[ ] only configured Knowledge Bases reconciled
[ ] logical → runtime KB mapping recorded
[ ] seed document reaches parse_status=completed
[ ] hybrid retrieval returns the known fact
[ ] source evidence identifies the seed source
[ ] each knowledge-enabled Hermes Profile has a distinct retrieve-only key
[ ] each runtime key has an explicit non-empty KB allow-list
[ ] runtime key can retrieve allowed knowledge
[ ] runtime key cannot perform a WeKnora write/admin operation
[ ] cross-KB denial passes when another out-of-scope KB exists
[ ] Hermes MCP uses the supported pinned WeKnora server/path
[ ] Hermes effective normal Profile toolset is read-only as configured
[ ] Hermes retrieves the same seed fact/source
[ ] no provisioning/runtime secret is committed or exposed to employee browser
[ ] actual evidence recorded in deployment state
```

Only then continue to the remaining Core Ready employee-client acceptance.