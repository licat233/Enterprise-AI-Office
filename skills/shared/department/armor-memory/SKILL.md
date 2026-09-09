---
name: armor-memory
description: >
  Retrieve or route documents using ARMOR Minimal Stable. Use when an
  Agent reads, searches, creates, stores, records, researches, or updates
  content in the ARMOR Vault.
---

# ARMOR Memory

## Use this Skill when

Use this Skill when a task reads, searches, creates, stores, modifies, records, researches, or classifies content in the ARMOR Vault.

Do not use it for:

- ordinary source-code edits
- temporary chat answers
- terminal output
- calculations
- disposable scratch files
- files outside the ARMOR Vault

## Retrieval workflow

1. If an exact file or domain `index.md` is known, read it directly.
2. Otherwise choose one relevant top-level area: current business facts and rules -> `01-Knowledge/`; active work -> `02-Projects/`; event or publication evidence -> `03-Records/`; external sources or analysis -> `04-Research/`.
3. Search only that area first.
4. Exclude Records, Inbox, and Archive unless the task requires evidence, unresolved material, audit, or history.
5. Expand to the full ARMOR Vault only after the scoped search fails, and state why; this does not mean switching to Web search.
6. Treat search results as candidates; determine authority from `00-System/AUTHORITY-RULES.md` and the underlying files.
7. When multiple files discuss the same mature topic, prefer an explicit canonical Knowledge entry as the default current-truth entry point. Supporting project, record, or research documents are not peer current-truth authorities merely because they mention the same topic.

## Retrieval authority rules

When a task depends on whether a claim is current or authoritative, read
`references/AUTHORITY-GUIDE.md`.

- Use only an explicit `authority` field to assign an authority level.
- `status` is optional lifecycle metadata. It does not mean `verified` or `canonical` and must not become a recurring human-maintenance obligation.
- `revision`, `source_quality`, `write_policy`, document type, and location in
  `01-Knowledge/` do not promote a file to `verified` or `canonical`.
- If a knowledge file has no explicit authority, treat it as `working` and
  qualify claims from it accordingly.
- Prefer explicit `canonical` over explicit `verified`, and explicit
  `verified` over `working`.
- If sources of equal or unclear authority conflict, report the conflict and
  request a decision. Do not silently choose one.
- Never say "all facts verified" unless each relied-on claim comes from an
  explicitly verified or canonical source, or was verified in the current
  task.

## Human-cost minimization

Human attention is reserved for material business judgment, unresolved authority, or ambiguity that the Agent cannot safely resolve.

Do not make the human act as a file administrator.

The Agent should perform deterministic or already-authorized maintenance itself, including:

- choosing the Router destination;
- updating routine status metadata when useful;
- applying a conflict resolution after the human has already decided it;
- completing scoped knowledge convergence after approval;
- re-routing and moving a previously unresolved item once the user supplies the missing classification information;
- other mechanical cleanup that follows directly from the current approved task.

Do not ask for a second confirmation when the user's current instruction already explicitly approves the exact change, resolves the conflict, or says which conclusion should be the current reference.

Do not require humans to move files merely because a lifecycle state changed. Directory location represents operational purpose, not lifecycle status.

## Write workflow

1. Classify the task using `references/CLASSIFICATION-PROTOCOL.md`.
2. Select only supported router values.
3. Call `scripts/route.sh`.
4. Use exactly the path returned by the router.
5. Write or update the document.
6. If this task resolves the classification of a previously unresolved Vault item, re-route and move that item to the returned destination in the same task. Do not leave a manual Inbox cleanup step for the human.
7. Stop.

ARMOR website articles use `work-product + website + article` and always route to the lifecycle-neutral content home `02-Projects/Workspaces/Website/Articles/`, whether or not `--project` is supplied.

Official social content uses `work-product + marketing + social-copy` and always routes to `02-Projects/Workspaces/Marketing/Social-Media/`, whether or not `--project` is supplied. Article and social-copy files do not move merely because their lifecycle state changes.

`03-Records/Published/` is for evidence of an actual publication event or an explicitly requested published snapshot. Do not place newly drafted channel content there merely because it is intended for publication.

Named project work that uses project-scoped routing lives under `02-Projects/Projects/<project>/`. Project completion does not require moving the project tree.

## Explicit knowledge quality workflow

Knowledge-quality maintenance is opt-in. Run it only when the user explicitly asks to audit, check, review, diagnose, or maintain ARMOR knowledge quality, or when an architecture/development task is specifically validating the knowledge system.

Do not run a Vault-wide quality check after an ordinary read or write.

Standard entry point:

```bash
bash scripts/knowledge.sh check
```

`check` is read-only and scans only `01-Knowledge/`. It reports:

- missing or invalid explicit authority;
- `evidence` authority placed in Knowledge as an advisory classification check;
- verified/canonical pages without an explicit provenance marker;
- possible duplicate titles, including possible canonical title collisions.

Duplicate and provenance findings are advisory. The tool does not merge, delete, rewrite, promote, or demote knowledge.

For a material canonical change, present the proposed change when human judgment is still required. When both current and candidate files exist, the standard helper is:

```bash
bash scripts/knowledge.sh diff <current.md> <candidate.md>
```

The diff helper is read-only. It does not create authority by itself. If the current user instruction already explicitly approves the exact change, do not request duplicate approval merely because a diff was shown.

## Explicit knowledge compilation workflow

Knowledge compilation is an explicit Agent workflow, not a background process or standalone service.

Use it when the user explicitly asks to turn source material into reusable ARMOR knowledge, consolidate a mature topic, resolve conflicting knowledge, make a conclusion the current reference, or otherwise converge multiple materials into current Knowledge.

Do not trigger it merely because an ordinary project, record, article, social post, research note, or conversation was created.

### Compilation steps

1. Scope the source material named by the user. Treat Records and Research as evidence, not current truth.
2. Extract only reusable claims or conclusions that merit long-term Knowledge. Do not create Knowledge merely to summarize every source document.
3. Classify the candidate using the current supported `knowledge-type` vocabulary.
4. If the candidate cannot be represented accurately by the current Router vocabulary, report `Router vocabulary gap` and stop before inventing a new enum or forcing the material into the nearest category.
5. Search the relevant `01-Knowledge/` scope for an existing current target before proposing a new page.
6. Compare the candidate material with the best current target and return one of these semantic outcomes:
   - `NOOP` — current Knowledge already expresses the same material conclusion.
   - `CREATE` — reusable Knowledge is warranted and no suitable current target exists.
   - `UPDATE` — the source adds or changes material Knowledge without unresolved contradiction.
   - `CONFLICT` — current Knowledge and new evidence materially disagree.
   - `AMBIGUOUS` — identity, target, meaning, scope, or authority cannot be resolved reliably.
7. Preserve provenance using stable source references and human-readable locators when available.
8. For `CREATE` or `UPDATE`, prepare the smallest useful candidate change. New Knowledge defaults to `working` unless it is explicitly verified or approved under the authority rules.
9. For a material canonical change, determine whether authority is already sufficient from the user's current instruction or an explicitly designated authoritative source. Ask the human only when material judgment remains unresolved.
10. For `CONFLICT` or `AMBIGUOUS`, do not improvise a resolution. Surface the exact competing claims, their authority/provenance, and the decision required.

### Conflict closure

A human answer that resolves a knowledge conflict is not merely a chat answer. It is authority input for closing that conflict in current Knowledge.

After the human explicitly resolves a conflict:

1. Apply the approved resolution to the intended current Knowledge target without asking for duplicate confirmation.
2. Preserve relevant provenance and add the required short changelog for material verified/canonical changes.
3. Search the same relevant `01-Knowledge/` scope for other current Knowledge that still presents the rejected claim as current truth.
4. Converge those competing current claims so the same resolved conflict does not remain active for the next Agent. Do not silently discard distinct valid knowledge while doing so.
5. Do not rewrite `03-Records/`, `04-Research/`, historical published records, or other evidence merely to make history match the new current conclusion.
6. If competing current Knowledge cannot be safely reconciled because identity or scope remains uncertain, report that closure is incomplete instead of pretending the conflict is solved.

A resolved conflict should not be escalated to a human again unless materially new evidence reopens the question.

### Topic convergence

Multiple documents may legitimately discuss the same topic, but mature reusable knowledge should provide one default current-knowledge entry point when that materially reduces ambiguity and repeated reading cost.

When explicitly asked to consolidate a mature topic:

1. Treat project documents, model-generated discussion documents, Records, and Research as supporting material unless they independently have explicit Knowledge authority.
2. Find an existing canonical or best current Knowledge entry before creating another page.
3. Compile the current ARMOR conclusion, not a transcript-style summary of what every source said.
4. Preserve unresolved questions as unresolved; do not fabricate consensus.
5. Prefer one canonical current entry when the topic has a settled ARMOR position. Supporting documents remain evidence/history and should not compete as default current truth.
6. Do not create a canonical topic page for every casual discussion. Convergence is warranted when the topic is reusable, repeatedly queried, supported by multiple materials, operationally important, or has produced recurring ambiguity/conflict.

The purpose of topic convergence is to reduce how many documents a human or Agent must read to know ARMOR's current position. It is not a license to generate more summaries, indexes, or lifecycle layers.

### Compilation boundaries

- Knowledge compilation does not authorize a new database, vector store, graph store, queue, background daemon, MCP server, or separate Knowledge Compiler service.
- The LLM performs semantic extraction, comparison, ambiguity detection, and proposal drafting; deterministic routing and authority rules still control persistence boundaries.
- Do not introduce Proposal folders, Review Queues, Draft Wiki roots, or other lifecycle directories for this workflow.
- Retirement/archive mechanics for redundant current Knowledge are a separate lifecycle-maintenance concern; do not invent an ad hoc storage path during compilation.
- Knowledge compilation is an explicit exception to ordinary route -> write -> stop only for the scoped convergence task the user requested. Do not turn it into hidden Vault-wide maintenance.

## Mandatory rules

- Full-Vault search is a fallback, not the first retrieval action.
- Do not treat Records, Research, Inbox, or Archive as current truth without qualification.
- Never construct a destination path manually.
- Never add a new router value during ordinary work.
- Never route unverified content to Inbox merely because it is unverified.
- Inbox is allowed only through explicit `object=unresolved`.
- Draft is a status, not a destination.
- Do not create human-maintained lifecycle queues or require manual file moves for routine state changes.
- Do not run extra memory-maintenance operations after an ordinary write unless the current task explicitly resolved a prior unresolved item or requested scoped knowledge convergence.
- Knowledge-quality tools are diagnostic and read-only; never treat a warning as permission to modify canonical knowledge.
- Do not leave a human-resolved contradiction active in current Knowledge when the explicit task is conflict resolution or knowledge convergence.
- Do not rewrite evidence/history merely to make it agree with current Knowledge.

## Canonical knowledge

Load `references/AUTHORITY-GUIDE.md` when changing canonical knowledge or when
retrieval requires an authority judgment.
