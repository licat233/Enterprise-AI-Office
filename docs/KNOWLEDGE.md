# Enterprise Knowledge Standard

This document defines how Enterprise AI Office organizes and governs company knowledge.

## 1. Knowledge platform

WeKnora is the enterprise knowledge platform.

It owns document ingestion, parsing, chunking, embedding, retrieval, source traceability, metadata, and Knowledge Base management.

## 2. Knowledge vs memory

Do not use Hermes Profile memory as the primary store for durable company facts.

```text
WeKnora
= authoritative shared company knowledge

Hermes Profile memory
= optional operating continuity/context subject to its memory policy
```

Company facts such as specifications, manuals, SOPs, policies, company profile, certifications, brand guidance, training material, and technical FAQs belong in WeKnora.

## 3. Knowledge Base baseline

A generic deployment may begin with one shared employee Knowledge Base, for example:

```text
Company Knowledge
```

Create another Knowledge Base only when at least one material boundary justifies it:

- semantic domain;
- permission/access;
- lifecycle/retention;
- operational ownership;
- confidentiality/data handling.

Do not create one Knowledge Base per file, person, department name, or small topic merely because such categories exist.

## 4. Prefer organization inside a Knowledge Base first

Before creating another top-level Knowledge Base, consider whether folders, tags, metadata, document status, or filters inside the existing Knowledge Base are sufficient.

Useful metadata may include:

```text
Product
Document Type
Language
Source Owner
Effective Date
Status
Version
Confidentiality
```

Add metadata that helps real retrieval/governance; do not create fields only for schema completeness.

## 5. Document status and provenance

Use clear lifecycle/status metadata so the system can distinguish current truth from useful history.

Possible statuses include:

```text
current
superseded
draft
reference
legacy
```

When a new document replaces an old one, preserve the prior version when history/provenance matters and mark the preferred current source accordingly.

## 6. File naming

Use descriptive names where practical.

Example pattern:

```text
Subject_DocumentType_Language_Date_Version.ext
```

Avoid ambiguous names that make source identification difficult.

## 7. Ingestion quality

Do not dump an entire shared drive into WeKnora by default.

Start with high-value, current, frequently used, well-understood knowledge.

RAG quality cannot compensate for duplicated, obsolete, contradictory, or poorly governed source material.

## 8. Seed corpus for Core Ready

A deployment needs only a small non-sensitive seed corpus to prove the technical knowledge path.

The seed should contain at least one known fact that can be retrieved and cited through:

```text
WeKnora
→ Hermes `general`
→ Open WebUI General Assistant
```

The seed corpus is a functional validation fixture, not a substitute for production company knowledge.

## 9. Production corpus

Production knowledge should be selected from the company's real work and access requirements.

Prioritize documents that employees actually need, then expand based on retrieval failures and user feedback rather than attempting exhaustive ingestion before launch.

## 10. Parsing validation

For Core Ready, verify the seed document parses and its known fact is retrievable.

For Production Ready, test the representative file formats the company will actually use, such as PDFs, DOCX, XLSX/tables, scanned/OCR material, or image-heavy documents where relevant.

Verify important numeric values, units, model names, tables, and other critical structure survive parsing sufficiently for retrieval.

Do not require file-format tests for formats the company does not use.

## 11. Retrieval strategy

Start with the selected WeKnora release's supported/default retrieval approach.

Do not immediately tune many thresholds, chunk sizes, top-k values, rerankers, or external vector stores before measuring real retrieval failures.

When an answer fails, diagnose in this order:

```text
source quality
→ parsing
→ chunking
→ metadata
→ embedding/retrieval
→ rerank
→ agent reasoning
```

## 12. Golden Questions

Before or during real production rollout, build a company-specific Golden Question Set from actual employee work.

Evaluate:

- source retrieval;
- answer correctness;
- source/citation correctness;
- cross-language behavior where relevant;
- unknown-answer behavior;
- conflicting-source behavior;
- latency/cost where operationally important.

Do not invent a generic question set that forces the company to model work it does not have.

## 13. Embedding deployment choices

Embedding does not have to come from a cloud model API.

For WeKnora deployments, treat the embedding runtime as an independent deployment choice from the reasoning/chat model used by Hermes.

Two supported patterns are useful:

```text
Remote embedding API
WeKnora → provider API → embedding vectors

Local embedding
WeKnora → local Ollama → embedding vectors
```

WeKnora v0.8.0 has a native local Ollama embedding path (`source=local`), so a deployment does not need a second inference framework merely to run embeddings locally.

### Remote embedding API

Use a remote embedding provider when:

- the host has limited local compute or memory headroom;
- operational simplicity is more important than per-call cost;
- external model/API use is acceptable for the selected knowledge boundary;
- provider availability and network dependency are acceptable.

Advantages:

- minimal local resource usage;
- no local model lifecycle to manage;
- easy to change capacity on the provider side.

Costs/trade-offs:

- recurring API cost;
- external network/provider dependency;
- provider credentials are required;
- knowledge text is sent to the selected provider according to that provider's data-handling terms.

The first synthetic reference deployment used DashScope `qwen3.7-text-embedding` at dimension `1024`. That is reference evidence, not a permanent requirement. The `3.7` in that cloud model name must not be interpreted as a `3.7B` local parameter count.

### Local embedding with Ollama

Use local embedding when:

- the deployment host has sufficient spare resources;
- reducing recurring API cost matters;
- keeping embedding traffic on the local host is desirable;
- the team prefers fewer external provider credentials/dependencies.

Advantages:

- no per-call embedding API fee;
- no external embedding-provider outage dependency;
- embedding text can remain on the local deployment host;
- no cloud embedding API key is required.

Costs/trade-offs:

- local RAM/CPU/GPU resources are consumed during model load, ingestion, and query embedding;
- the model/runtime must be kept operational;
- actual retrieval quality must be checked on the company's languages and document types.

A local embedding model does **not** imply that the main reasoning model must also run locally. A valid architecture is:

```text
Open WebUI
→ Hermes `general`
→ remote reasoning model (for example the selected GPT model)
→ WeKnora retrieval
   → local Ollama embedding model
```

### Recommended local starting candidates

For multilingual enterprise knowledge, especially Chinese + English, use a small mature embedding model first and increase model size only when measured retrieval failures justify it.

Current recommended starting candidates:

| Candidate | Typical role | Why consider it |
| --- | --- | --- |
| `bge-m3` | preferred first local candidate | mature multilingual retrieval, strong Chinese/English support, 1024-dimensional embeddings, no model-specific query instruction required for normal dense retrieval |
| `qwen3-embedding:0.6b` | lighter alternative | compact local footprint, strong Chinese/multilingual capability, 1024-dimensional output available |

Do **not** default to 4B/8B-class embedding models merely because the host can run them. For a shared enterprise host, the smallest model that gives acceptable retrieval quality is usually the better operational choice.

`bge-m3` is currently the preferred local candidate for the first real Mac Studio deployment, but it should be promoted to a validated deployment baseline only after the deployment's small retrieval/resource smoke test passes. Until then, treat it as a recommendation, not frozen architecture.

### Minimal qualification instead of a benchmark project

Do not turn embedding selection into a research project by default.

For a new deployment, a practical qualification is enough:

1. load the candidate model locally;
2. create a temporary/small non-sensitive Knowledge Base;
3. ingest roughly 5–10 representative documents;
4. ask roughly 5–10 representative queries, including required cross-language retrieval;
5. confirm the expected source is retrieved;
6. observe macOS Memory Pressure / obvious host slowdown during ingestion and normal queries;
7. accept the model if retrieval is adequate and host impact is acceptable.

Only compare another model when the first candidate shows a real quality or resource problem.

### WeKnora v0.8.0 local-Ollama note

In WeKnora v0.8.0's local Ollama embedding implementation, `truncate_prompt_tokens = 0` falls back to approximately `511` tokens rather than meaning unlimited input.

Therefore:

- do not assume UI value `0` means unlimited;
- keep normal RAG chunks within a safe size or set/validate an explicit truncation value where needed;
- re-check this behavior when upgrading WeKnora because it is version-specific implementation behavior.

## 14. Embedding model changes

Treat an embedding-model change as high risk.

Before changing:

- record current model/dimension;
- understand reindex requirements;
- protect/backup the current state as appropriate;
- create a migration/reindex plan;
- rerun representative retrieval tests;
- define rollback.

Do not silently switch embeddings in an established deployment.

Select and validate the embedding model before large-scale production ingestion whenever possible. Changing embedding model or vector dimension after indexing normally implies re-embedding/reindexing the affected corpus.

## 15. Knowledge conflict behavior

When authoritative-looking sources materially conflict, the assistant should surface the conflict rather than silently choose or invent a reconciliation.

The knowledge maintainer/domain owner should then resolve document status or source quality.

## 16. Unknown-answer behavior

If approved company knowledge does not provide sufficient evidence, the assistant should say so.

Do not allow general model priors to become invented company facts.

## 17. Language behavior

Company knowledge may be multilingual.

Test cross-language retrieval only for language combinations the company actually needs.

Do not assume monolingual retrieval performance guarantees multilingual performance.

## 18. Knowledge permissions

Normal employees primarily consume knowledge through authorized Assistants.

Knowledge maintainers may receive WeKnora administration/contributor permissions required to ingest, organize, and update sources.

Do not give every employee unrestricted knowledge administration.

Split or protect Knowledge Bases when real permission/data boundaries require it.

## 19. Sensitive data

Do not ingest credentials, passwords, private keys, tokens, or secret configuration values into WeKnora.

Before ingesting confidential/restricted information, review:

- access boundaries;
- model/provider data flow;
- contractual/regulatory obligations;
- storage/backup exposure.

## 20. Hermes integration

Hermes accesses WeKnora through supported MCP/API interfaces.

Normal employee Profiles should receive a least-privilege read-oriented retrieval surface.

Avoid direct database coupling.

## 21. Nested reasoning

If WeKnora provides its own agent/reasoning features, use them only when they add concrete value to a knowledge workflow.

Do not route every Hermes retrieval through another agent layer automatically.

## 22. Knowledge ownership

A production deployment should identify at least one human role responsible for knowledge hygiene.

Responsibilities may include:

- adding/updating approved sources;
- marking superseded material;
- resolving conflicting versions;
- maintaining useful metadata;
- investigating retrieval failures;
- coordinating with domain owners.

This is an operational responsibility, not a requirement to create a dedicated AI Profile or organizational department.

## 23. Change traceability

For critical company facts, preserve enough provenance to determine:

- what is current now;
- what was true before when relevant;
- when it changed;
- which source supports the current answer.

## 24. Knowledge acceptance checklist

### Core Ready

```text
[ ] Company-configured Knowledge Base exists
[ ] Seed document ingestion completes
[ ] Known fact is retrievable
[ ] Source evidence is visible
[ ] Hermes `general` retrieves through supported MCP/API
[ ] Unknown company fact is not invented
```

### Production Ready

```text
[ ] Knowledge Base boundaries match real semantic/permission needs
[ ] Production corpus is current and useful
[ ] Representative company file formats parse correctly
[ ] Critical values survive retrieval
[ ] Required language/cross-language behavior is tested
[ ] Source evidence is correct
[ ] Conflicting sources are surfaced
[ ] Sensitive-data boundary is reviewed
[ ] Knowledge ownership is defined
```
