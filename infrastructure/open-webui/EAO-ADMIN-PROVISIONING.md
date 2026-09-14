# EAO Admin Open WebUI Provisioning

Status: repository capability artifact; requires an explicitly authorized target
and private configuration before use.

## 1. Preconditions

Read DEPLOY.md, AGENTS.md, state/PROJECT-PHASE.yaml,
config/capabilities.yaml, the active private company configuration, and
docs/ACCEPTANCE-TESTS.md. Provision only when
capabilities.eao_administrator_console.enabled is true.

The administrator surface is a normal Open WebUI resource backed by the
Hermes maintainer Profile. It is not a second portal and it is not a
connection to Hermes default/admin.

Required protected inputs:

    Open WebUI administrator bootstrap/session
    EAO Administrators logical/runtime group identity
    Hermes maintainer Profile API URL and unique API key
    configured WeKnora target Knowledge Base
    read-only maintainer WeKnora retrieval binding
    bounded Enterprise Web Research binding (web_search + web_fetch only)
    bounded ToolScout maintainer review binding
    MCP/control-plane registry authority for review-only inspection
    repository typed path status: BLOCKED — TYPED REPOSITORY CAPABILITY NOT RESOLVED
    protected operation-envelope HMAC signing-key reference
    scoped WeKnora contributor credential for the Action only
    operation-envelope approval TTL (default and maximum 30 minutes)

Never print, store, or commit the API key, bootstrap password, bearer token, or
forwarder credential.

## 2. Native Open WebUI resource

Use the selected Open WebUI release's native admin API/UI. Do not edit its
database directly and do not rely on CSS/UI hiding.

Create or reconcile exactly:

    Group: EAO Administrators
    Assistant/model id: maintainer
    Display name: EAO Admin
    Hermes URL: http://<trusted-hermes-host>:<port>/p/maintainer/v1

The exact URL/port must match the selected pinned release and private target.
The Profile API key is server-side only.

The native ACL record must grant read only to the resolved EAO Administrators
group:

    {
      "id": "maintainer",
      "base_model_id": null,
      "name": "EAO Admin",
      "access_grants": [
        {
          "principal_type": "group",
          "principal_id": "<EAO_ADMINISTRATORS_GROUP_ID>",
          "permission": "read"
        }
      ],
      "is_active": true
    }

Preserve unrelated Open WebUI resources. Do not grant anyone, wildcard,
All-Employees, Operations, Sales, Procurement, or other ordinary groups.

## 3. Hermes connection

Register one server-side OpenAI-compatible connection for the named
maintainer Profile. Use its unique Profile key and an explicit served-profile
allowlist. Keep the privileged default/admin Profile absent from all employee
Assistant connections.

The Profile's effective tools must be the currently resolved typed EAO
intake/review capability set only:

    resource classification
    Capability Reuse Pass
    read-only Company Knowledge retrieval
    bounded external source inspection through enterprise-web-research
    Skill actual-source review
    ToolScout-first review through the maintainer review subset
    MCP/backend review without automatic exposure
    operation-plan preview/approval binding

The Hermes maintainer Profile MUST NOT receive the WeKnora contributor write
credential or contributor write routes. Knowledge mutation is held by the
server-side Open WebUI Action only.

The repository read/search, CI/readiness, branch, and PR path is currently:

    BLOCKED — TYPED REPOSITORY CAPABILITY NOT RESOLVED

Do not expose or claim those repository operations at runtime. If a typed
binding is unavailable, leave that operation disabled/blocked. Do not
compensate with generic terminal, filesystem, Docker, browser, shell,
package-manager, or arbitrary HTTP access.

## 4. Deterministic approval Action

Reference implementation:

    infrastructure/open-webui/eao_admin_knowledge_action.py

Shared deterministic envelope primitive:

    infrastructure/open-webui/eao_operation_envelope.py

The Action reuses Open WebUI v0.11.3's server-side authenticated Action
runtime. It does not add a governance service or approval database.

The Action/control-plane binding must:

1. receive the current authenticated Open WebUI user context;
2. derive HumanActor and current groups server-side. The Action receives server-side Open WebUI user context only from the authenticated request.
3. resolve the source from the current owned chat branch and the exact parent user
   message; uploaded files must resolve through Open WebUI's own file record and
   storage provider and must be owned by the current HumanActor;
4. derive the source fingerprint, operation_id, target Knowledge Base and expected
   current state server-side. Do not accept these as authority from model text;
5. build/sign the immutable operation envelope with the protected HMAC key;
6. display exact operation fields, source fingerprint, target, impact and plan hash;
7. on Approve, reload current group membership and re-resolve the source from the
   current chat. Changed source/current state must invalidate approval;
8. before the external write, persist a sanitized OUTCOME_UNKNOWN operation marker
   in the existing Open WebUI assistant-message metadata so a crash cannot cause a
   blind retry. This is replay evidence, not a new approval database;
9. invoke only the three bounded WeKnora contributor write routes and the one
   bounded knowledge-detail read route;
10. on Cancel, create no approval/effect;
11. return only sanitized non-secret evidence.

The Action must never accept actor IDs, group IDs, operation IDs, plan hashes,
commands, filesystem paths, package names, Knowledge Base IDs, or approval state
as authority from assistant text or user-supplied tool arguments. A URL/manual
body/file attachment is source material, not approval authority.

The envelope helper is side-effect free. The Action may keep only sanitized
operation result/replay evidence in the already-existing Open WebUI chat message
metadata. It must never store the HMAC key, WeKnora contributor key or trusted
plan signature there. Do not add an approval database or generic admin endpoint.

The Open WebUI Action receives server-side-only configuration equivalent to:

    EAIO_EAO_ADMIN_GROUP_ID
    EAIO_EAO_ADMIN_ASSISTANT_ID=maintainer
    EAIO_EAO_ADMIN_WEKNORA_BASE_URL
    EAIO_EAO_ADMIN_WEKNORA_API_KEY
    EAIO_EAO_ADMIN_KB_ID
    EAIO_EAO_ADMIN_KB_DISPLAY_NAME
    EAIO_EAO_ADMIN_APPROVAL_SIGNING_KEY
    EAIO_EAO_ADMIN_APPROVAL_TTL_MINUTES
    EAIO_EAO_ADMIN_OPERATION_ENVELOPE_PATH (or approved module directory)

Only symbolic secret references belong in company/deployment state. The real
contributor key and HMAC key must never be committed or returned to the model.

## 5. v1A typed operations

Resolved typed operations:

    classify_resource
    review_capability_reuse
    inspect_public_source_with_web_search_or_fetch
    review_skill_source
    review_tool_with_toolscout
    review_mcp_backend
    ingest_approved_knowledge_source

The source-inspection binding exposes only enterprise-web-research web_search
and web_fetch. Raw Firecrawl, Obscura, CloakBrowser, authenticated browsing,
binary download and generic browser access remain unavailable.

The maintainer ToolScout binding exposes only advise_tool_use, query_registry,
detect_candidates, check_conflicts and doctor. ToolScout record_memory,
recall_memory and install/execute primitives are not exposed to maintainer.

The MCP/backend review operation is review-only. It may inspect the current MCP
control-plane authority but has no registration, exposure, install, or mutation
operation in v1A and therefore does not require a mutation-capable MCP binding.

Repository operations are not in the v1A runtime set:

    BLOCKED — TYPED REPOSITORY CAPABILITY NOT RESOLVED

The WeKnora operation must use the pinned official v0.8.0 bounded contributor
path: X-API-Key with exactly the ingest and retrieve capabilities,
full_access=false, and a non-empty knowledge_base_ids allow-list. The only v1A
write routes are:

    POST /api/v1/knowledge-bases/{id}/knowledge/file
    POST /api/v1/knowledge-bases/{id}/knowledge/url
    POST /api/v1/knowledge-bases/{id}/knowledge/manual

Status is read through GET /api/v1/knowledge/{id}. The credential must keep
full_access=false and must not carry manage_kbs, manage_agents, manage_models,
MCP admin, tenant/system admin, platform, or runtime-management capabilities.
It must not expose tenant deletion, Knowledge Base deletion,
embedding/reranker administration, bulk deletion, or direct database writes.

Not exposed in v1A:

    run_shell
    execute
    write_file
    delete_file
    docker
    install_package
    install_skill
    install_tool
    reconcile_profile
    reconcile_mcp
    switch_profile

## 6. Direct acceptance probes

For the enabled target, test through the actual Open WebUI resource and backend:

    authorized EAO administrator → maintainer visible/use → PASS
    ordinary employee → /api/v1/models excludes maintainer → PASS
    Operations employee → direct maintainer request denied → PASS
    wrong group → model/resource request denied → PASS
    maintainer credential → default/admin route denied → PASS
    maintainer effective tools → no generic shell/filesystem/Docker/browser → PASS
    missing/forged actor context → approval denied → PASS
    expired/changed envelope → approval denied → PASS

A successful provisioning API response or hidden UI item is not acceptance. Record
the actual identifiers and results in deployment state without secrets.

## 7. Target gate

This file does not authorize provisioning on armor@MacStudio.local or any
other real host. Re-read state/PROJECT-PHASE.yaml and obtain the separate
explicit real-deployment request before mutating the target.
