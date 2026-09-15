# WeKnora Deployment Adapter

WeKnora is the Enterprise AI Office knowledge platform and the source of truth for durable company facts.

For deployment execution, follow `DEPLOY.md` first. For non-interactive model/Knowledge Base/credential reconciliation, use [`PROVISIONING.md`](PROVISIONING.md).

## Validated reference release

The first validated local deployment used WeKnora `v0.8.0` at commit `1edcd54b43606d9079bb36650efe3f68707a79ea`.

Validated upstream: `https://github.com/Tencent/WeKnora.git`. The authoritative
repo/ref/commit/acquisition metadata lives in `config/validated-stack.yaml`;
follow `DEPLOY.md §4.1` before using this adapter.

This is a tested reproducibility baseline, not a permanent version requirement. Do not silently substitute a newer release during an ordinary deployment; treat an upgrade as a separate compatibility decision.

## Deployment posture

Use the supported upstream deployment plus the smallest validated Enterprise AI Office adapter.

Baseline requirements:

- persist the database and uploaded/original documents;
- keep PostgreSQL, Redis/cache, parser/DocReader, and other internal services off public interfaces;
- configure only the model roles required by the selected WeKnora version;
- create only the Knowledge Bases declared by company configuration;
- validate ingestion and retrieval with a small non-sensitive seed document before connecting Hermes;
- provision through supported upstream APIs rather than direct database writes;
- give each knowledge-enabled employee Profile a backend-enforced least-privilege retrieval credential matching its configured Knowledge Base scope.

The repository does not require optional vector databases, graph databases, tracing stacks, or other feature services unless a real requirement justifies them.

## Container service discovery hardening

Docker/Compose container IP addresses are ephemeral implementation details. EAO must never rely on a specific container IP remaining stable across recreate, upgrade, or recovery.

The pinned WeKnora v0.8.0 frontend proxies to the backend service name `app`, but its Nginx configuration resolves that name when Nginx starts. If `app` is recreated later while the frontend keeps running, Nginx can continue using the stale IP and return `502 Bad Gateway` for every `/api/v1/*` request. The UI can then misleadingly appear to have lost models or Knowledge Bases even though PostgreSQL data is intact.

The canonical deployment checkout is `${RUNTIME_ROOT}/runtime/WeKnora`.
Materialize the two EAO adapter files into that checkout, then start Compose
there:

```sh
mkdir -p "${RUNTIME_ROOT}/runtime/WeKnora/eao-adapter"
cp infrastructure/weknora/frontend-entrypoint.sh \
  "${RUNTIME_ROOT}/runtime/WeKnora/eao-adapter/frontend-entrypoint.sh"
cp infrastructure/weknora/docker-compose.eaio.override.yml \
  "${RUNTIME_ROOT}/runtime/WeKnora/docker-compose.eaio-override.yml"

cd "${RUNTIME_ROOT}/runtime/WeKnora"
docker compose -f docker-compose.yml -f docker-compose.eaio-override.yml up -d
```

This keeps the production runtime independent of the location of the EAO Git
checkout.

The adapter:

- freezes the existing Compose project identity as `weknora`, protecting the project-qualified persistent-volume identity from working-directory drift;
- preserves the official WeKnora frontend image and official `/docker-entrypoint.sh`;
- patches only the runtime Nginx template before the official entrypoint renders it;
- uses Docker embedded DNS (`127.0.0.11`) to re-resolve `app`;
- keeps routing based on the stable Compose service name rather than a container IP;
- fails closed when the expected pinned upstream template shape changes, forcing compatibility review on upgrade.

Do **not** assign static container IPs merely to work around stale DNS. Stable identity is the Compose service name; container IPs remain disposable.

The protected runtime must also preserve the same `SYSTEM_AES_KEY` across
recreate, upgrade, restore, and migration. A changed/missing key can make stored
encrypted provider/model/MCP/datasource credentials unreadable even when the
database rows still exist.

For host-native services consumed from WeKnora containers, such as Ollama or an OpenAI-compatible local gateway, use `host.docker.internal` on the validated macOS Docker path rather than `localhost`. If WeKnora SSRF validation protects that endpoint, add the exact trusted hostname to the WeKnora container's `SSRF_WHITELIST_EXTRA`; setting a host OS environment variable alone does not inject it into an already-created container.

## Models

The validated reference deployment proved that the architecture can use a provider other than the initial attempted provider.

Exact provider/model IDs belong in protected deployment configuration and `state/DEPLOYMENT-STATE.md`, not in the generic architecture.

When selecting models:

- record the embedding model and dimension exactly;
- record any chat/reasoning model used by WeKnora;
- add reranking only when retrieval evaluation shows a need;
- treat embedding-model changes as high-risk because reindexing may be required.

`PROVISIONING.md` defines how to reconcile these models against the installed upstream API without duplicating unrelated model records.

## Knowledge Bases

Knowledge Base structure is company configuration.

The generic baseline may use one shared employee Knowledge Base such as:

```text
Company Knowledge
```

Additional Knowledge Bases are created only when distinct semantic, access, lifecycle, or operational boundaries justify them.

Do not copy runtime-generated Knowledge Base IDs from a reference deployment. Maintain the logical company-config ID → actual WeKnora runtime ID mapping in deployment state.

## Knowledge bridge

Hermes accesses WeKnora through supported MCP/API surfaces rather than direct database access.

For the baseline `general` Profile, provide the smallest read-only retrieval capability needed to:

- address/discover approved Knowledge Bases;
- retrieve relevant chunks/documents;
- expose human-readable source evidence.

Use both layers of least privilege:

```text
Hermes MCP tool allow-list
+
WeKnora retrieve-only API key with explicit Knowledge Base allow-list
```

Scope retrieval credentials to the Knowledge Bases and actions the Profile actually needs. Keep those credentials outside Git and out of the employee browser.

Exact MCP tool names may vary by upstream release; verify the installed release instead of hard-coding a historical tool inventory as a permanent contract. The validated baseline templates are release-specific examples and `PROVISIONING.md` defines the required backend credential checks.

## Persistent data and credentials

Production secrets and runtime `.env` files belong in protected storage outside this public repository.

Keep the WeKnora owner/admin provisioning identity separate from Profile runtime retrieval keys. Do not put an Owner JWT or broad provisioning credential into Hermes.

Before backup or migration, identify the actual runtime directory, database/storage volumes, uploaded-file storage, configuration, and secret-recovery material.

Use `docs/BACKUP-RESTORE.md` for production recovery requirements.

## Validation

Core Ready requires:

- required WeKnora services healthy;
- provisioning reconciliation completed through the supported API path;
- seed document ingestion complete;
- known fact retrievable;
- source evidence visible;
- normal Profile runtime key limited to `retrieve` plus its explicit Knowledge Base allow-list;
- a harmless write attempt with that runtime key fails closed;
- Hermes `general` can retrieve the same approved knowledge through supported MCP/API integration.

Then continue with the real employee-client checks in `docs/ACCEPTANCE-TESTS.md`.

Specific demo Knowledge Bases, provider choices, runtime IDs, key IDs/scope metadata, and specialist Profile results are recorded in `state/DEPLOYMENT-STATE.md` as evidence rather than generic provisioning defaults. Never record plaintext secrets there.