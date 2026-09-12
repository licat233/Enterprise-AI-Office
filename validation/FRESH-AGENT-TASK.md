# Fresh-Agent Validation Task

You are a capable AI engineering agent with no previous Enterprise AI Office conversation history.

Your task is to determine whether this repository is sufficient to understand and reproduce Enterprise AI Office safely.

## Rules

1. Treat repository evidence as authoritative over assumptions.
2. Read `AGENTS.md` before making material recommendations.
3. Do not infer a real deployment authorization.
4. Do not use or request real credentials during the comprehension or dry-run stages.
5. Do not invent a replacement architecture.
6. Perform the Capability Reuse Pass before proposing new infrastructure.
7. Distinguish normative contracts, reference deployment evidence, and historical migration evidence.
8. When information is genuinely missing, classify the gap instead of guessing.

## Stage A — Comprehension exam

Before writing an installation plan, answer all of these from repository evidence.

1. What is Enterprise AI Office trying to provide?
2. Which component owns:
   - employee Web access and human-facing Assistant ACLs;
   - Agent runtime and Profiles;
   - shared company knowledge;
   - scheduled Agent work;
   - durable Agent work;
   - governed Email send evidence?
3. What is the validated core stack and which versions are pinned?
4. Explain why:
   - Profile is not a user;
   - Knowledge is not Memory;
   - provider credential is not human authority;
   - installation blueprint is not a live installation.
5. What does `real_deployment_task.active: false` mean?
6. Does a real ARMOR reference deployment exist? Where is its sanitized status recorded?
7. What is the baseline employee workflow?
8. What is the current Operations employee workflow?
9. Why can Open WebUI native Knowledge records legitimately be zero?
10. What is the current employee/Profile long-term Memory policy?
11. What is the WeKnora access scope used by the Operations reference path?
12. Before adding n8n, another vector database, another browser stack, or another scheduler, what must you do?
13. Which capabilities are frozen/validated versus merely present as repository assets?
14. What security boundaries must an ordinary employee Profile preserve?
15. What must happen if an external email send outcome is unknown?
16. Which information belongs in Git, and which classes must remain private?
17. What is the difference between:
    - blueprint lifecycle;
    - deployment target readiness;
    - reference implementation status?
18. Which documents are the primary execution and acceptance contracts?
19. Which evidence is historical and should not silently override the current contracts?
20. What would make you stop with a repository defect rather than improvise?
21. Is backup/restore enabled by any readiness label automatically? If backup is enabled and company policy requires off-primary independence, what evidence is required? Explain why the primary runtime/data disk is not itself a backup.
22. Why do LaunchAgent/Compose restart settings not prove startup/recovery PASS, and what post-recovery evidence is required before claiming automatic or unattended recovery?
23. How must a Fresh Agent determine:
    - WeKnora model `source` (`local` / `remote`);
    - Hermes model-provider credential native binding;
    - WeKnora remote-model credential binding;
    - when an API-key credential ref may legitimately be empty for local/keyless/OAuth/account paths?
    Explain why none of these may be guessed from the ARMOR reference runtime or a provider name alone.

Do not proceed until you can answer these with repository paths.

## Stage B — Reconstruction dry run

Assume a hypothetical clean macOS arm64 validation host compatible with the validated reference stack.

No real credentials are supplied yet.

Produce:

1. required reading order;
2. component installation order;
3. exact public configuration inputs;
4. private input classes that would be required before an authorized deployment;
5. model-role source/auth plan, including symbolic provider-credential refs and exact pinned native bindings without secret values;
6. capability closure table;
7. minimum Core target state;
8. General Assistant/Profile/knowledge route;
9. Operations Assistant/Profile/knowledge route if enabled;
10. network and administrative exposure principles;
11. least-privilege tool plan;
12. acceptance sequence;
13. restart sequence and backup/restore sequence only if backup is explicitly enabled;
14. backup evidence boundary when enabled, including the distinction between primary runtime/data storage and any separately selected backup target;
15. rollback principles;
16. all blockers, classified as one of:

```text
REPOSITORY_DEFECT
MISSING_PRIVATE_INPUT
TARGET_ENVIRONMENT_BLOCKER
RUNTIME_FAILURE
POLICY_OR_AUTHORITY_BLOCKER
```

Do not ask the human to choose routine implementation details already frozen by the repository.

## Stage C — New capability challenge

The business asks:

> "We want a daily AI process that reviews work and performs a scheduled task. Add a workflow platform."

Do not implement anything.

Perform the Capability Reuse Pass and explain whether a new workflow platform is justified.

Then answer a second challenge:

> "We need a new enterprise knowledge feature. Add a second vector database."

Again, perform the Capability Reuse Pass before proposing architecture.

## Stage D — Runtime reproduction

Do not perform this stage unless the human explicitly authorizes Blueprint Validation and provides a specific validation target.

If authorized, follow `VALIDATE.md`, `DEPLOY.md`, and `docs/ACCEPTANCE-TESTS.md`.

Your final evidence must use `validation/REPORT.template.md`.
