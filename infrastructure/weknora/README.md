# WeKnora Deployment Adapter

WeKnora is the Enterprise AI Office knowledge platform and the source of truth for durable company facts.

For deployment execution, follow `DEPLOY.md` first.

## Validated reference release

The first validated local deployment used WeKnora `v0.8.0` at commit `1edcd54b43606d9079bb36650efe3f68707a79ea`.

This is a tested reproducibility baseline, not a permanent version requirement. Do not silently substitute a newer release during an ordinary deployment; treat an upgrade as a separate compatibility decision.

## Deployment posture

Use the supported upstream deployment plus the smallest validated Enterprise AI Office adapter.

Baseline requirements:

- persist the database and uploaded/original documents;
- keep PostgreSQL, Redis/cache, parser/DocReader, and other internal services off public interfaces;
- configure only the model roles required by the selected WeKnora version;
- create only the Knowledge Bases declared by company configuration;
- validate ingestion and retrieval with a small non-sensitive seed document before connecting Hermes.

The repository does not require optional vector databases, graph databases, tracing stacks, or other feature services unless a real requirement justifies them.

## Models

The validated reference deployment proved that the architecture can use a provider other than the initial attempted provider.

Exact provider/model IDs belong in protected deployment configuration and `state/DEPLOYMENT-STATE.md`, not in the generic architecture.

When selecting models:

- record the embedding model and dimension exactly;
- record any chat/reasoning model used by WeKnora;
- add reranking only when retrieval evaluation shows a need;
- treat embedding-model changes as high-risk because reindexing may be required.

## Knowledge Bases

Knowledge Base structure is company configuration.

The generic baseline may use one shared employee Knowledge Base such as:

```text
Company Knowledge
```

Additional Knowledge Bases are created only when distinct semantic, access, lifecycle, or operational boundaries justify them.

Do not copy runtime-generated Knowledge Base IDs from a reference deployment.

## Knowledge bridge

Hermes accesses WeKnora through supported MCP/API surfaces rather than direct database access.

For the baseline `general` Profile, provide the smallest read-only retrieval capability needed to:

- address/discover approved Knowledge Bases;
- retrieve relevant chunks/documents;
- expose human-readable source evidence.

Scope retrieval credentials to the Knowledge Bases and actions the Profile actually needs. Keep those credentials outside Git and out of the employee browser.

Exact MCP tool names may vary by upstream release; verify the installed release instead of hard-coding a historical tool inventory as a permanent contract.

## Persistent data and credentials

Production secrets and runtime `.env` files belong in protected storage outside this public repository.

Before backup or migration, identify the actual runtime directory, database/storage volumes, uploaded-file storage, configuration, and secret-recovery material.

Use `docs/BACKUP-RESTORE.md` for production recovery requirements.

## Validation

Core Ready requires:

- required WeKnora services healthy;
- seed document ingestion complete;
- known fact retrievable;
- source evidence visible;
- Hermes `general` can retrieve the same approved knowledge through supported MCP/API integration.

Specific demo Knowledge Bases, provider choices, runtime IDs, and specialist Profile results are recorded in `state/DEPLOYMENT-STATE.md` as evidence rather than generic provisioning defaults.
