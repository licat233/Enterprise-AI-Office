# Enterprise AI Office Knowledge Intake v1

Status: canonical administrator operating procedure
Lifecycle: CLOSED / FROZEN / PASS WITH GAPS
Knowledge Authority: WeKnora v0.8.0

This procedure is the canonical v1 answer to: “How do I safely add a PDF,
webpage, document, Markdown note, or research report to Enterprise AI Office?”
It records the accepted workflow only; it does not add an ingestion capability
or authorize a new runtime path.

## 1. Scope

Knowledge Intake v1 covers administrator-reviewed intake of:

- PDF
- DOC/DOCX
- Markdown
- TXT
- HTML
- EPUB
- CSV
- XLS/XLSX
- PPT/PPTX
- JSON
- supported images
- supported audio
- webpage URL
- remote document URL
- manually entered text or Markdown

Video is not claimed as supported durable knowledge. Temporary chat attachments
and Open WebUI native Knowledge are not durable enterprise knowledge
authorities.

## 2. Authority model

| Responsibility | Authority |
| --- | --- |
| Durable knowledge, parsing, chunking, embedding, retrieval, source traceability, and KB management | WeKnora |
| Source review, classification, duplicate/conflict decision, target-KB decision, and metadata recommendation | EAO Admin |
| Mutation boundary | Human administrator using the native WeKnora surface |
| Verification | Read-only WeKnora retrieval, with optional Hermes retrieval |

The accepted workflow is:

    Discover source
      ↓ EAO Admin Review
      ↓ Classify value, knowledge type, duplicate, conflict, authority, KB, metadata
      ↓ Human administrator confirms
      ↓ Native WeKnora ingestion
      ↓ Wait for parse_status = completed and enable_status = enabled
      ↓ KB-scoped hybrid retrieval verification
      ↓ Optional Hermes retrieval verification
      ↓ Accepted into operational knowledge

WeKnora remains the Knowledge Authority. Open WebUI Knowledge must not become a
parallel enterprise knowledge store.

Installed != Exposed != Authorized. An installed capability is not necessarily
exposed to a Profile, and an exposed capability is not necessarily authorized
for a particular actor, KB, or operation. Prompt is not a security boundary.
Actor identity, permissions, target KB, and mutation authority come from the
authenticated runtime and native access controls.

The accepted ARMOR boundary remains:

    EAO Admin Review Plane: ACTIVE / ACCEPTED
    EAO Admin Knowledge Mutation: BLOCKED / DISABLED
EAO Admin reviews and recommends. It does not upload, write, or publish
automatically. A human administrator performs the native WeKnora mutation.

## 3. Administrator review checklist

Before import, answer the following.

### Value

- Is the material useful to ARMOR or EAO?
- Is it durable enough for enterprise knowledge?
- Is it better stored as reference rather than authoritative guidance?

### Duplication and conflict

- Does equivalent knowledge already exist?
- Is this another copy, or has the source materially changed?
- Does it conflict with current authority?
- Does it supersede an older source?
- If sources conflict, which is authoritative?

### Target

- Which KB should contain it?
- Should it remain in Company Knowledge?
- Is another KB justified by a real semantic, access, confidentiality, or
  lifecycle boundary?

Do not create KBs for folders, topics, categories, people, or departments that
existing folders, tags, or metadata can represent.

### Security and provenance

- Is the material appropriate for enterprise ingestion?
- Does it contain secrets, passwords, API keys, private credentials, or
  unnecessary sensitive material?
- Does its confidentiality match the target retrieval scope?
- Is the original source known?
- Is source ownership and date/version clear?

Never ingest credentials, private keys, tokens, passwords, or secret configuration.

## 4. Authority classification

Use two v1 classifications, represented through existing WeKnora tags or
custom metadata.

### Authoritative

Authority=Authoritative means accepted current enterprise truth, for example
approved ARMOR documentation, current product specifications, approved SOPs,
policies, operating instructions, or accepted internal standards.

### External Reference

Authority=External Reference means useful material that does not override ARMOR
authority, for example industry research, vendor documentation, external
articles, platform guides, analyst reports, or regulatory/background material.

External Reference must not silently override Authoritative knowledge. Resolve
conflicts through governance before import or status change. This is a
documented convention, not a new database or enforcement service.

## 5. Metadata convention

Use existing WeKnora tags and custom metadata. The recommended v1 set is:

    Product
    Document Type
    Language
    Source Owner
    Effective Date
    Status
    Version
    Confidentiality
    Authority
    Source URL

No field is mandatory for every document.

For normal external material, recommend Authority, Document Type, Source Owner,
Effective Date or publication date when known, and Source URL when applicable.

For ARMOR authoritative documentation, recommend Authority=Authoritative,
Document Type, Source Owner, Effective Date, Status, Version when applicable,
and Confidentiality when applicable.

Use status values such as current, superseded, draft, reference, or legacy.

## 6. Target Knowledge Base

Current production baseline:

    Knowledge Base: Company Knowledge
    KB ID: 1d5cf386-77a2-4142-a59f-37e99f78da7f

Default to Company Knowledge. Use another KB only for a material access,
confidentiality, lifecycle, ownership, or semantic-isolation boundary.

## 7. Exact intake procedures

Every path begins with EAO Admin review and ends with parse/index and retrieval
acceptance. The human administrator uses native WeKnora UI or supported
native administrative API. Do not route intake through the disabled EAO Admin
Knowledge Action.

### A. PDF or file

    EAO Admin Review → Company Knowledge → native file upload
    → metadata/tags → completed/enabled → retrieval verification

Route: POST /api/v1/knowledge-bases/{kb_id}/knowledge/file

The observed production file-size limit is 50 MB. Normal file duplicate
checking is generally MD5/content-hash based within tenant and KB; the same
content under another filename can still be detected. Filename is not the
duplicate authority.

### B. Webpage URL

Route: POST /api/v1/knowledge-bases/{kb_id}/knowledge/url

Webpage URLs are supported and the source URL is retained. An identical raw URL
is normally protected by duplicate detection, but URL canonicalization is not
guaranteed. Basic direct URL ingestion has no automatic refresh. Multiple URLs
can be queued in the native UI but are submitted individually, not as one
atomic transaction.

Sitemap or web-crawler configuration is outside the current v1 baseline unless
separately required and authorized. Do not introduce a crawler workflow for v1.

### C. Remote document URL

Use the same native URL route when WeKnora can identify the document type from
the URL or supplied file hints. Confirm that the source is appropriate and
actually a document. Remote file_url duplicate behavior is weaker and less
aligned than normal uploaded-file duplicate detection; perform a human
duplicate check before import and do not assume repeat rejection.

### D. Manual text or Markdown

Route: POST /api/v1/knowledge-bases/{kb_id}/knowledge/manual

Provide title, content, and draft or publish status. Draft may remain
non-indexed; publish enters normal parse/index. Native manual content supports
substantially more content than the disabled EAO adapter. For large or
structured content, a .md upload is acceptable and often preferred.

Manual duplicate detection is weaker; search the target KB and review before
creating another record. Do not route manual content through the disabled EAO
Knowledge Action.

## 8. Parse and index acceptance

Upload success is not intake acceptance. The record must reach:

    parse_status = completed
    enable_status = enabled

If parsing fails, inspect native status/error, check source format/size/content,
retry or reparse using native administrative capability where appropriate, and
repeat retrieval verification. Do not invent another processing pipeline.
Reparse is reprocessing/re-indexing, not file replacement or version control.

## 9. Retrieval acceptance test

Use the existing read-only capabilities:

    list_knowledge_bases
    get_knowledge_base
    list_knowledge
    get_knowledge
    list_chunks
    hybrid_search

1. Confirm the correct KB.
2. Confirm the knowledge record exists.
3. Confirm parse_status=completed.
4. Confirm enable_status=enabled.
5. Inspect source, title, filename, and available metadata.
6. Select distinctive facts from the source.
7. Perform KB-scoped hybrid search.
8. Confirm returned chunks belong to the expected document.
9. Confirm source and knowledge ID.
10. Where useful, verify the same fact through normal Hermes retrieval.

Upload success is not acceptance. Retrieval verification is required.

## 10. Duplicate, update, conflict, and supersession rules

- Do not re-import an exact file duplicate without a justified reason.
- Treat changed file content as an intentional update decision.
- Decide whether an old source remains historical/reference, becomes
  superseded/legacy, or is removed/replaced through native administration.
- Manual duplicate detection is weaker; require human review and KB search.
- The same raw URL normally receives duplicate protection, but different URL
  forms may not.
- When sources conflict, do not ingest both and let RAG decide. EAO Admin must
  identify authority, determine whether the older source remains valid, and
  decide its status or removal. This is governance, not vector search.

Do not create a version-control service.

## 11. Non-goals for Knowledge Intake v1

V1 does not require an EAO automatic write path, active
eao_admin_knowledge_action, new administrator portal, approval ledger, durable
replay state, SQLite/PostgreSQL/Redis additions, filesystem ledger, new vector
database, Open WebUI Knowledge, crawler scheduling, automatic source refresh,
document-version-history service, new RBAC design, direct database mutation,
automatic web crawling, or automatic bulk URL transactions.

These are intentional boundaries, not unfinished v1 work.

## 12. Related contracts

- [Enterprise Knowledge Standard](KNOWLEDGE.md)
- [Capability Reuse Pass](CAPABILITY-REUSE-PASS.md)
- [WeKnora provisioning contract](../infrastructure/weknora/PROVISIONING.md)
- [EAO Admin Open WebUI provisioning](../infrastructure/open-webui/EAO-ADMIN-PROVISIONING.md)
- [Repository governance](REPOSITORY-GOVERNANCE.md)

This SOP is a v1 operating convention over the existing pinned WeKnora
capabilities, not a replacement implementation.
