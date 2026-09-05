# WeKnora Deployment Adapter

WeKnora is the Enterprise AI Office knowledge platform.

This directory is reserved for tested Enterprise AI Office configuration layered on top of a pinned upstream WeKnora release.

## Default deployment posture

Use WeKnora's standard production-oriented deployment, normally Docker Compose for the reference implementation.

Do not use a lightweight/demo mode as the default company production architecture when the deployment requires multi-user, long-lived knowledge ingestion and ongoing document growth.

## Required outcomes

A production WeKnora deployment must provide:

- persistent enterprise knowledge;
- reliable document parsing;
- hybrid retrieval/reranking as supported by the selected release;
- citations/source traceability;
- secure user/admin access as required;
- a supported MCP/API bridge for Hermes;
- recoverable database and document storage.

## Upstream-first implementation

At deployment time:

1. select the tested WeKnora release;
2. use that release's official Compose/install definitions;
3. generate strong secrets;
4. configure models;
5. configure persistent storage;
6. restrict internal service exposure;
7. add only minimal Enterprise AI Office overrides;
8. record versions and real volume/storage locations.

## Retrieval stack

Start with WeKnora's supported default PostgreSQL/vector/hybrid retrieval stack for the selected version.

Do not add an external vector database unless measured scale/performance/retrieval requirements justify it.

## Model roles

Record exact deployed values for:

- embedding model and dimension;
- reranker;
- chat/reasoning model if WeKnora Agent is used;
- parser/VLM models if enabled.

## Knowledge bridge

Hermes should use WeKnora's supported MCP/API surface.

Do not grant Hermes direct SQL coupling to WeKnora's internal database schema for ordinary knowledge access.

## Persistent data

The deployment agent must identify and document:

- PostgreSQL persistence;
- uploaded/original-file storage;
- any object-storage backend;
- important application config;
- backup/restore commands for the exact version.

## Validation

Run the WeKnora sections of `docs/ACCEPTANCE-TESTS.md` before employee rollout.
