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
    typed MCP/control-plane bindings
    repository typed path status: BLOCKED — TYPED REPOSITORY CAPABILITY NOT RESOLVED
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
    Skill actual-source review
    ToolScout-first review
    MCP/backend review without automatic exposure
    bounded WeKnora contributor/retrieval operation
    operation-plan preview/approval binding

The repository read/search, CI/readiness, branch, and PR path is currently:

    BLOCKED — TYPED REPOSITORY CAPABILITY NOT RESOLVED

Do not expose or claim those repository operations at runtime. If a typed
binding is unavailable, leave that operation disabled/blocked. Do not
compensate with generic terminal, filesystem, Docker, browser, shell,
package-manager, or arbitrary HTTP access.

## 4. Deterministic approval Action

A server-side Open WebUI Action may use
infrastructure/open-webui/eao_operation_envelope.py for validation. The
Action/control-plane binding must:

1. receive the current authenticated Open WebUI user context;
2. derive HumanActor and current groups server-side. The Action receives server-side Open WebUI user context only from the authenticated request.
3. resolve the operation subject by server-owned operation context, not model text;
4. display exact operation fields, source fingerprint, target, impact, hash, and expiry;
5. on Approve, reload current state, recheck authorization, recompute the hash,
   reject expiry/staleness, and invoke only the typed operation;
6. on Cancel, create no approval/effect;
7. return only sanitized non-secret evidence.

The Action must never accept actor IDs, group IDs, operation IDs, plan hashes,
commands, paths, package names, or approval state as authority from assistant
text or user-supplied tool arguments. The envelope helper is side-effect free;
durable approval/effect evidence belongs to the existing control-plane/owning
authority. Do not add an approval database or generic admin endpoint.

## 5. v1A typed operations

Resolved typed operations:

    classify_resource
    review_capability_reuse
    review_skill_source
    review_tool_with_toolscout
    review_mcp_backend
    ingest_approved_knowledge_source

Repository operations are not in the v1A runtime set:

    BLOCKED — TYPED REPOSITORY CAPABILITY NOT RESOLVED

The WeKnora operation must use the pinned official v0.8.0 bounded contributor
path: X-API-Key with the ingest capability and a non-empty
knowledge_base_ids allow-list. The only v1A write routes are:

    POST /api/v1/knowledge-bases/{id}/knowledge/file
    POST /api/v1/knowledge-bases/{id}/knowledge/url
    POST /api/v1/knowledge-bases/{id}/knowledge/manual

Status is read through GET /api/v1/knowledge/{id}. The credential must not
have full_access, manage_kbs, manage_agents, platform, or runtime-management
capabilities. It must not expose tenant deletion, Knowledge Base deletion,
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
