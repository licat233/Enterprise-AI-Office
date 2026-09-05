# WeKnora Deployment Adapter

WeKnora is the Enterprise AI Office knowledge platform and the source of truth for durable company facts. The validated local demo uses the pinned upstream release `v0.8.0` at commit `1edcd54b43606d9079bb36650efe3f68707a79ea`.

## Local demo deployment

The runtime checkout is outside Git at `$EAIO_RUNTIME_DIR/WeKnora`. The demo uses WeKnora's upstream core Compose stack only; PostgreSQL, Redis, the application, frontend, and document reader run in Docker, with database and document storage kept in persistent Docker-managed storage. Optional Qdrant, Neo4j, Milvus, Weaviate, Langfuse, and other feature stacks are not enabled.

The small [docker-compose.demo.override.yml](docker-compose.demo.override.yml) mounts the tested built-in model configuration read-only. The runtime is started with the upstream Compose file plus this override. Published ports are loopback-only:

```text
WeKnora API: http://127.0.0.1:18080
WeKnora UI:  http://127.0.0.1:8088
```

Do not use this local demo posture as a production default. Production requires reviewed secrets, backup/restore, network policy, model-provider approval, and a tested upgrade path.

## Models and knowledge bases

The OpenAI built-in configuration was retained but was quota-exhausted during the first ingestion attempt. The validated demo therefore uses protected DashScope credentials with the following demo-only configuration; these are not permanent project model requirements:

- embedding: `qwen3.7-text-embedding`, dimension `1024`;
- chat/KnowledgeQA: `qwen-plus`;
- reranker: none configured. Reranking remains optional and should be added only if real retrieval evaluation shows that ranking quality requires it.

Two synthetic knowledge bases were created and populated:

```text
Company & Brand
Products & Technical
```

Runtime-generated knowledge-base IDs are intentionally not part of this reusable adapter. Deployment-specific identifiers may be recorded in sanitized deployment state when operationally useful, but adopters must create and discover their own IDs rather than copy a reference instance.

The corpus is outside Git at `$EAIO_RUNTIME_DIR/demo-corpus`. Both documents completed ingestion, and hybrid retrieval returned source-backed chunks. Replace the synthetic content with approved company documents before real use.

## Knowledge bridge

Hermes uses the supported WeKnora MCP server over the API; it does not connect directly to WeKnora PostgreSQL. Each employee Profile receives the seven read-only retrieval tools:

```text
list_knowledge_bases
list_shared_knowledge_bases
get_knowledge_base
hybrid_search
list_knowledge
get_knowledge
list_chunks
```

The WeKnora viewer key is scoped to the two demo KBs with the `retrieve` capability. As expected for that scope, `list_shared_knowledge_bases` returns 403; direct KB listing and `hybrid_search` succeed. Never put the key in Git or in a user-visible client.

## Persistent data and credentials

The runtime `.env`, admin credentials, viewer key, and model-provider credentials are protected outside this repository. The credential file is `$EAIO_RUNTIME_DIR/credentials/weknora-admin.env`; do not print or commit its values. The deployment state records locations and non-secret identifiers only.

Identify the exact Docker volumes and external runtime directory before backup or migration. A production deployment must back up PostgreSQL, uploaded/original files, application configuration, and secret-recovery material, then perform a restore test.

## Validation

The local demo passed service health, model-provider connectivity, document ingestion, KB listing, hybrid retrieval, source-title/file traceability, and Hermes MCP grounding through General, Sales, and QC Profiles. Run the WeKnora sections of `docs/ACCEPTANCE-TESTS.md` before employee rollout.
