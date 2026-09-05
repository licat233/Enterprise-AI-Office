# Enterprise Knowledge Standard

This document defines how Enterprise AI Office organizes and governs company knowledge.

## 1. Knowledge platform

WeKnora is the v1 enterprise knowledge platform.

It owns:

- document ingestion;
- parsing;
- chunking;
- embeddings;
- hybrid retrieval;
- reranking;
- citations;
- Knowledge Bases;
- document metadata;
- knowledge-management UI/workflows.

## 2. Knowledge vs memory

Do not use Hermes Profile memory as the primary store for durable company facts.

```text
WeKnora
= shared company knowledge

Hermes Profile memory
= role-specific operating experience / context
```

Examples that belong in WeKnora:

- product specifications;
- manuals;
- SOPs;
- policies;
- company profile;
- certifications;
- brand guidelines;
- training material;
- technical FAQs.

## 3. Knowledge Base design

Do not create one Knowledge Base per file, person, or small topic.

Split Knowledge Bases when either of these materially differs:

- semantic domain;
- permission boundary.

A generic starting point may be:

```text
Company & Brand
Products & Technical
Sales & Marketing
Operations & SOP
```

Sensitive finance, HR, supplier-cost, legal, or customer-confidential data should be separated only when there is a real permission/data-boundary requirement.

## 4. Folder, tag, metadata first

Before creating another Knowledge Base, consider whether folder/tag/metadata organization inside an existing KB is sufficient.

Typical metadata:

```text
Product
Document Type
Language
Source Department
Effective Date
Status
Version
Confidentiality
```

## 5. Document status

Recommended lifecycle tags:

```text
current
superseded
draft
reference
legacy
```

`current` means the document is the preferred current operational reference.

`superseded` means the document remains useful as history/evidence but should not be treated as the latest truth.

## 6. Preserve useful history

Do not delete old documents merely to make the knowledge base look clean.

When a new document replaces an old one:

```text
new version → current
old version → superseded
```

Preserve provenance when historical documents may matter for audits, customer communications, or understanding earlier decisions.

## 7. File naming

Use consistent descriptive names where practical.

Example:

```text
Product_Model_DocumentType_Language_Date_Version.pdf
```

Avoid ambiguous names such as:

```text
final.pdf
final2.pdf
new-final-final.pdf
use-this-one.pdf
```

## 8. Ingestion quality

Do not dump an entire shared drive into WeKnora on day one.

Start with:

```text
high value
+
current
+
frequently used
+
well understood
```

knowledge.

RAG quality cannot compensate for large amounts of duplicated, obsolete, or contradictory source material.

## 9. Pilot corpus

A good initial corpus includes representative examples of:

- product specifications;
- manuals;
- catalogs;
- certificates;
- company profile;
- key SOPs;
- training documents;
- sales/marketing FAQs.

## 10. Parsing validation

An upload success message is not enough.

Inspect representative parsed content and retrieval for:

- English PDF;
- Chinese PDF;
- tables;
- DOCX;
- XLSX;
- scanned/OCR document;
- image-heavy document if relevant.

Verify important numeric values, units, model names, and table structure survive parsing sufficiently for retrieval.

## 11. Retrieval strategy

Start with the upstream-recommended hybrid retrieval/rerank configuration.

Do not immediately hand-tune many thresholds, chunk sizes, top-k values, and external vector databases before measuring real failures.

When an answer fails, diagnose in order:

```text
source quality
→ parsing
→ chunking
→ metadata
→ embedding/retrieval
→ rerank
→ prompt/agent reasoning
```

## 12. Model benchmark

Before large-scale rollout, create a company-specific Golden Question Set.

Include:

- exact product/technical facts;
- SOP questions;
- cross-language questions;
- table/spreadsheet lookups;
- source-citation questions;
- conflicting-document questions;
- unknown/unanswerable questions.

Evaluate:

- retrieval recall;
- answer correctness;
- citation correctness;
- cross-language quality;
- hallucination behavior;
- latency;
- cost.

## 13. Embedding model changes

Treat an embedding-model change as high risk.

Before changing:

- record current model/dimension;
- back up;
- understand reindex requirements;
- create a migration/reindex plan;
- rerun Golden Questions;
- define rollback.

Do not silently switch embeddings in production.

## 14. Knowledge conflict behavior

When retrieved sources materially conflict, the agent should not silently pick one.

Expected response pattern:

```text
A conflict exists.
Source A says X.
Source B says Y.
The current authoritative value cannot be safely established from the available sources.
```

A responsible human/knowledge maintainer should then correct document status or source quality.

## 15. Unknown-answer behavior

If the knowledge base does not contain sufficient evidence, the agent should say so.

Do not let general model priors become invented company facts.

## 16. Language behavior

Company knowledge may be multilingual.

Benchmark at least:

- Chinese question → English source;
- English question → Chinese source;
- Chinese answer;
- English answer.

Do not assume strong monolingual benchmark performance implies strong cross-language enterprise retrieval.

## 17. Knowledge permissions

Normal employees primarily consume knowledge through authorized assistants.

Knowledge Maintainers/Contributors may receive WeKnora UI permissions to upload, organize, and update sources.

Do not grant every employee unrestricted KB administration.

## 18. Sensitive data

Do not ingest credentials, passwords, private keys, or secret configuration values into WeKnora.

Before ingesting Confidential/Restricted data, verify:

- WeKnora permission boundaries;
- external model data flow;
- regulatory/contractual requirements;
- backup/storage exposure.

## 19. Hermes integration

Hermes should access WeKnora through supported MCP/API interfaces.

Prefer read-oriented retrieval tools for normal knowledge work.

Avoid direct database coupling.

## 20. Nested agent reasoning

WeKnora may have its own Agent capabilities. They can be useful for specialized knowledge reasoning.

Do not automatically route every Hermes knowledge query through another Agent layer.

Use the simplest supported retrieval path that solves the task.

## 21. Knowledge ingestion ownership

Define at least one human role responsible for knowledge hygiene.

Typical responsibilities:

- upload current documents;
- mark superseded material;
- resolve conflicting versions;
- maintain metadata/tags;
- investigate bad retrieval sources;
- coordinate with domain owners.

## 22. Change traceability

When a critical company fact changes, preserve enough provenance to answer:

- what is current now?
- what was true before?
- when did it change?
- which source supports the current answer?

## 23. Knowledge acceptance checklist

```text
[ ] KB boundaries make semantic/permission sense
[ ] Pilot corpus is current and high quality
[ ] Representative formats parse correctly
[ ] Exact technical values survive retrieval
[ ] Chinese/English cross-language tests pass
[ ] Citations point to correct sources
[ ] Unknown questions do not hallucinate company facts
[ ] Conflicting sources are surfaced
[ ] Sensitive data boundary reviewed
[ ] Knowledge maintainer role defined
```
