# MCP Control Plane

Status: current control-plane interpretation for the reusable registry plus the sanitized ARMOR reference snapshot.

The machine-readable authority is **config/mcp-registry.yaml**.

This document explains how to read that registry. It supersedes the earlier Phase 4A-only interpretation that all definitions were merely PREPARED and that Operations was WeKnora-only.

## 1. Two layers exist in one registry

config/mcp-registry.yaml contains two kinds of information:

~~~text
Reusable control-plane contract
→ transport shape
→ classification
→ required logical environment names
→ tool/exposure boundary
→ default exposure policy
→ security constraints

Sanitized ARMOR reference snapshot
→ runtime.status
→ installed/configured/enabled
→ version/install strategy
→ health status / live probe evidence
~~~

The reusable definition layer applies to a fresh deployment.

The runtime/health layer does **not**.

A fresh Agent must recompute runtime truth from the target host and active company configuration. It must not infer installed, configured, enabled, or HEALTHY merely because those values are present in the ARMOR reference snapshot.

The registry records this rule explicitly:

~~~yaml
scope:
  runtime_state_scope: sanitized_ARMOR_reference_snapshot
  fresh_deployment_rule: recompute_runtime_and_health_do_not_inherit_reference_flags
~~~

## 2. Current ARMOR reference snapshot

As of the registry review date, the public sanitized reference state is:

| Definition | Reference runtime state | Direct Operations exposure | Role |
| --- | --- | --- | --- |
| anysearch | registered / credential-blocked | no | future read-only candidate |
| firecrawl-mcp | package/runtime available; raw health not an employee requirement | **no** | upstream/internal inventory; employee surface is adapter-only |
| enterprise-web-research | enabled / healthy | yes, exactly web_search + web_fetch | bounded Operations Web Research |
| obscura | installed / direct lane disabled / healthy internal probe | no | internal Level-2 rendered-page backend |
| paddle_ocr | installed / disabled / healthy internal probe | no | reserved machine-specific OCR runtime |
| toolscout | enabled / healthy | yes | approved shared Agent infrastructure |
| armor-vault-scoped-router | enabled / healthy | yes | ARMOR-scoped closed-package writes |

WeKnora is part of the Operations MCP allowlist but is governed by the knowledge/runtime contracts rather than represented as one of the migration inventory entries above.

Current bounded Operations allowlist:

~~~text
weknora
toolscout
enterprise-web-research
armor-vault-scoped-router
~~~

This is ARMOR reference evidence, not a universal default for another company.

## 3. Raw Firecrawl is not an employee MCP

The current Web Research architecture is:

~~~text
Operations
→ enterprise-web-research
   → Firecrawl API
   → Obscura fallback
   → CloakBrowser fallback
~~~

It is **not**:

~~~text
Operations
→ firecrawl-mcp
~~~

Therefore the registry requires:

~~~yaml
firecrawl-mcp:
  exposure:
    allowed_profiles: []
    operations_exposure: false
  boundary:
    employee_surface: adapter_only
    raw_tools_exposed_to_operations: false
~~~

The upstream Firecrawl package may exist on the reference host without granting its raw MCP tools to an employee Profile. Runtime availability and employee exposure are separate dimensions.

The raw `firecrawl-mcp` entry may therefore report `BLOCKED_CREDENTIAL` for its own
direct health probe while `enterprise-web-research` is `HEALTHY`. That raw blocker
does **not** mean employee Web Research is broken: the approved adapter has its own
protected `FIRECRAWL_API_KEY` binding and separate acceptance evidence. The registry
records this distinction with `scope: raw_firecrawl_mcp_entry_only` and
`does_not_apply_to: [enterprise-web-research]`.

The deterministic Phase 6 checker verifies that the real Operations Profile does not bind firecrawl-mcp, Obscura, or CloakBrowser directly.

## 4. Internal browser backends

Obscura and CloakBrowser are implementation details of Enterprise Web Research.

They do not create a generic browser capability.

Allowed behavior remains bounded:

- public HTTP/HTTPS acquisition only;
- no authenticated browsing;
- no personal browser profile;
- no cookie/session import;
- no form submission;
- no generic click/type/fill surface;
- no arbitrary JavaScript;
- no binary download;
- no automatic persistence into Vault, WeKnora, or Hermes Memory.

Absolute /Users/armor/... paths in the frozen Web Research acceptance record are ARMOR deployment evidence only. The reusable adapter and config/.env.example now resolve target-host-specific paths.

### Upstream provenance

The ARMOR reference runtime records exact upstream identities for the external
local runtimes that participate in the current bounded Operations capability:

- Obscura `v0.2.2` → `h4ckf0r0day/obscura` (Apache-2.0 observed at the validated release).
- ToolScout `v1.0.0` → `licat233/toolscout` (MIT observed at the validated release).

Those identities are recorded in `config/mcp-registry.yaml`. A fresh
deployment must still resolve and accept its selected versions rather than
treating ARMOR runtime flags as universal defaults.

## 5. ToolScout boundary

ToolScout is approved shared Agent infrastructure in the ARMOR Operations reference profile.

Its separate Agent identity/memory home does not enable employee Hermes long-term Memory.

A fresh deployment must still decide whether the active company configuration enables ToolScout and must run its applicable acceptance before claiming Configured Ready.

## 6. ARMOR Vault Router boundary

armor-vault-scoped-router is an ARMOR-specific capability.

It is not a generic filesystem tool.

Its allowed tools are closed package operations such as article, social, MIC, website-product-material, and product-visual packages. Generic filesystem write, arbitrary destination, path traversal, symlink escape, and published-source mutation remain forbidden.

Another company does not inherit this ARMOR capability unless it intentionally adopts an equivalent company-specific contract.

## 7. Fresh deployment interpretation

A fresh Agent should read the registry in this order:

1. read scope;
2. inspect reusable classification/transport/boundary/exposure rules;
3. read config/capabilities.yaml and the active company configuration;
4. determine which definitions are actually required;
5. inspect the target host;
6. resolve host-specific runtime bindings and secrets;
7. install/reconcile only enabled capabilities;
8. test health and employee-visible exposure;
9. record the target deployment's own runtime truth outside the public blueprint.

Do not copy ARMOR runtime or health values into a fresh deployment state.

## 8. Phase 4A historical origin

The original Phase 4A work inventoried five legacy definitions:

- Anysearch;
- Firecrawl MCP;
- Obscura;
- Paddle OCR MCP;
- ToolScout.

At that time they were intentionally recorded as PREPARED / not employee-exposed while the Operations capability migration was still being designed.

That Phase 4A state remains valid historical evidence in:

- docs/PHASE4A-ARMOR-MIGRATION.md;
- Git history;
- later Phase 4B–6 closure records.

It is no longer the current control-plane state.

Subsequent approved work added and/or enabled the bounded Enterprise Web Research adapter, ToolScout, and the ARMOR scoped Vault Router for the ARMOR reference deployment.

## 9. Secret and authority policy

The registry may contain logical environment-variable names, but never secret values.

Runtime credentials do not grant human authority.

Profile exposure must remain explicit and least-privilege.

A definition appearing in the registry does not mean:

- it must be installed for every company;
- it is enabled for every Profile;
- it is healthy on a new target;
- its raw tools are employee-visible.

The active company configuration + capability registry + target runtime evidence determine the actual deployment.

## 10. Acceptance

Relevant public checks include:

~~~text
EAO_REPOSITORY_ONLY=1 sh scripts/repository-readiness-check.sh
sh scripts/run-public-offline-tests.sh
~~~

For the ARMOR reference Web Research runtime, the target-host Phase 6 acceptance additionally validates the actual Operations Profile and its exact MCP bindings.

Public repository checks do not replace target runtime acceptance.
