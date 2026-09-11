# Authority Guide

- `working`: the default state for project documents, research notes, and new knowledge pages
- `verified`: checked against a relevant source or reviewer
- `canonical`: explicitly approved or designated as the authoritative version
- `evidence`: record material documenting what happened or what was received

Rules:

- project documents default to `working`
- research notes default to `working`
- records may use `evidence`
- knowledge defaults to `working` unless verified
- `canonical` requires explicit user approval or an explicitly designated authoritative source
- canonical content must not be silently overwritten
- do not ask for a second approval when the user's current instruction already explicitly approves the exact change, resolves the conflict, or designates the conclusion as the current reference
- an explicitly designated authoritative source may satisfy the authority basis when the requested update is unambiguous; do not add a redundant human confirmation solely because the target is canonical
- ask the human only when a material judgment remains unresolved, competing authoritative claims remain, identity/scope is ambiguous, or the requested action would exceed the authority already granted

## Authority during retrieval

- Read the file's explicit `authority` field. Do not infer authority from other
  metadata.
- `status` is optional lifecycle metadata. It does not create authority and must
  not become a recurring human-maintenance obligation.
- `revision`, `source_quality`, `write_policy`, `type`, and folder location are
  supporting metadata, not substitutes for `authority`.
- A knowledge file without explicit `authority` remains `working`.
- Rank claims only as explicit `canonical` > explicit `verified` > `working`.
- When equal or unclear authority sources conflict, expose the conflict and
  ask for a decision.
- Do not describe a set of claims as verified unless every material claim has
  explicit verified/canonical authority or was checked in the current task.

Before changing canonical content:

1. Read current content.
2. Identify the exact change and its source/reviewer basis.
3. Determine whether approval is already present in the user's current instruction or through an explicitly designated authoritative source.
4. Ask for human approval only if the material judgment is still unresolved.
5. Update the file once the authority basis is sufficient.
6. Add a short changelog entry for a material change.
7. If the change resolves a conflict, complete the scoped conflict-closure workflow in the same task instead of leaving cleanup to the human.

Do not add Proposal files or Review Queues to the default workflow.
