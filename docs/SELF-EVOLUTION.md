# EAO Enterprise Self-Evolution v1

Status: DESIGN BASELINE / RUNTIME NOT ENABLED  
Scope: employee experience → organizational intelligence  
Runtime authority: unchanged until separately audited and accepted

## 1. Purpose

Enterprise AI Office should become more useful as employees use it, not merely
because more documents, models, or third-party tools are added, but because the
system gradually learns how the company actually works.

The most valuable operating knowledge in a company is often tacit:

- how experienced purchasing staff evaluate a supplier beyond unit price;
- how finance staff recognize reporting or payment risks;
- how sales staff qualify customers, handle exceptions, and avoid bad commitments;
- how operations staff recognize recurring failure patterns;
- how employees correct procedures after real incidents.

This knowledge is usually distributed across employees and is often absent from
formal manuals.

EAO Self-Evolution exists to convert useful experience that naturally appears
during normal work into reusable organizational intelligence.

The target loop is:

```text
normal employee work
        ↓
Hermes observes corrections / advice / exceptions / lessons
        ↓
experience extraction
        ↓
source-aware role experience
        ↓
later reuse in similar work
        ↓
real-world correction / reinforcement
        ↓
refinement
        ↓
mature organizational intelligence
```

This is not autonomous self-modification without governance.

## 2. Primary design constraint: humans do not serve the AI

EAO exists to reduce human work.

A Self-Evolution feature is unacceptable if it creates a parallel knowledge-
management job for ordinary employees or requires a company to appoint a new
"AI knowledge reviewer" merely to keep the Agent useful.

Hard rule:

```text
human workload added by the learning mechanism
must remain materially lower than
human work saved by the resulting intelligence
```

Therefore the normal employee must not be required to:

- complete a post-task experience form;
- manually classify lessons;
- add tags or metadata;
- write summaries for the AI;
- maintain an AI-specific knowledge base;
- process a routine review queue;
- learn EAO internals;
- act as a data-entry operator for Hermes.

Knowledge management should be a by-product of real work, not a second job.

### Work-embedded learning

The preferred interaction is:

```text
Employee: "No, for this supplier we also need to check MOQ and payment terms."

Hermes:
- corrects the current task;
- recognizes the statement as potentially reusable experience;
- extracts the general lesson and provenance in the background;
- reuses it later only within its appropriate confidence and scope.
```

If confirmation is genuinely needed, use the smallest possible interruption,
for example a single natural-language confirmation. Do not require a form.

## 3. No new universal expert or review role

EAO must not assume that a small or medium company can assign a person who
understands every department well enough to review finance, procurement,
sales, operations, engineering, and marketing experience.

The people doing the work are already the distributed subject-matter experts.

Use this principle:

```text
review at the source
```

The employee who supplied or corrected an experience is normally the best
available person to confirm whether Hermes understood that experience correctly.

This does not make every employee statement company policy. It establishes
provenance:

```text
"an experienced employee used this judgment in this work context"
≠
"this is an immutable company-wide rule"
```

EAO Admin remains responsible for system governance, permissions, architecture,
and exceptional/high-risk promotion. EAO Admin is not a daily reviewer of
department knowledge.

## 4. Capability Reuse Pass decision

Self-Evolution v1 must reuse the current EAO authorities before introducing any
new platform.

Existing components already cover most of the lifecycle:

| Need | Existing EAO authority |
| --- | --- |
| Employee work surface | Open WebUI |
| Agent reasoning and work execution | Hermes Agent |
| Durable work / organizational memory | Existing governed Vault / Wiki working-memory authority; ARMOR reference: ARMOR Vault |
| Approved enterprise factual/reference retrieval | WeKnora |
| Reusable procedures | Hermes Skills |
| Runtime role behavior | Hermes Profiles / SOUL |
| Knowledge intake rules | Knowledge Intake v1 |
| Skill admission and ownership | Skill Admission + repository governance |
| Administrative governance | EAO Admin / existing control plane |
| Scheduled/durable Agent work if later required | Hermes Cron / Kanban |

Decision:

```text
NO NEW DATABASE
NO NEW VECTOR STORE
NO NEW WORKFLOW ENGINE
NO NEW KNOWLEDGE PORTAL
NO NEW UNIVERSAL REVIEW ROLE
```

The remaining gap is the learning bridge:

```text
employee experience
→ detection
→ extraction
→ low-friction retention
→ scoped reuse
→ feedback
→ optional promotion
```

Prefer Hermes native self-improvement primitives when the deployed version is
proven to support them safely. Do not design a replacement learning engine
before the runtime audit.

## 5. Experience is not the same as knowledge, policy, or memory

EAO must keep four concepts separate.

### Experience

A source-aware observation, heuristic, exception, lesson, or judgment produced
through real work.

Example:

> For this class of supplier, low unit price is not enough; MOQ, payment terms,
> lead time, and inventory exposure also matter.

Experience may be useful before it is formally established as company truth.

### Approved enterprise knowledge

Stable factual/reference material whose authority is appropriate for WeKnora.

### Procedure / Skill

A reusable method describing how Hermes should perform a task.

### Company rule / policy

A formal behavioral or authorization rule that can affect company decisions,
risk, or external side effects.

Hermes Profile Memory remains optional continuity state. It is not the durable
authority for employee-derived organizational intelligence.

## 6. Experience signals

Hermes should treat the following as high-value learning signals during normal
work:

- **Correction** — "That is not how we do this; instead..."
- **Pitfall** — "We tried this before and it caused..."
- **Decision heuristic** — "When this happens, I normally check..."
- **Exception** — "Usually yes, but for this case..."
- **Procedure improvement** — "Do this step before that step..."
- **Escalation boundary** — "If this condition occurs, ask the responsible person."
- **Reasoned preference** — "We prefer A over B here because..."
- **Post-result feedback** — "That worked / did not work because..."

Ordinary instructions such as "make this shorter" or one-off personal
preferences should not automatically become organizational experience.

The system should prefer reusable, context-dependent lessons over arbitrary
conversation retention.

## 7. Minimal experience record

Do not turn employee experience into a heavy ontology.

A minimal retained experience needs only enough information to prevent context
loss and unsafe generalization:

```yaml
experience:
  lesson: "Do not evaluate this supplier class by unit price alone."
  context: "supplier quotation evaluation"
  role_domain: "procurement"
  source_type: "employee_work"
  source_context: "correction during a real task"
  applicability:
    - "check MOQ"
    - "check payment terms"
    - "check lead time"
    - "check inventory exposure"
  confidence: "emerging"
  status: "active_experience"
```

Where the runtime already provides trustworthy identity, timestamp, task/session
reference, or provenance metadata, capture it automatically. Do not ask the
employee to type it.

Do not retain secrets, passwords, tokens, unnecessary private employee data, or
customer-confidential content merely because it appeared in a learning moment.

## 8. Default retention target: existing Vault / Wiki working-memory authority

The default durable landing place for employee-derived experience is the
existing governed Vault / Wiki working-memory authority. In the ARMOR reference
deployment, this is ARMOR Vault Wiki. Use a bounded logical area such as:

```text
organizational-intelligence/
  role-experience/
    procurement/
    finance/
    sales/
    operations/
    marketing/
  lessons/
```

This is a logical information architecture, not a requirement to add a new
database or Wiki application.

The existing scoped Vault boundary remains mandatory. Self-Evolution must not be
implemented by granting ordinary employee Profiles a generic filesystem.

The exact runtime write/read interface is an implementation decision that must
reuse or minimally extend the existing scoped Vault capability.

## 9. Trust grows through work, not through a central review queue

EAO should use progressive trust rather than treating every experience as either
"unapproved" or "company truth."

A practical lifecycle is:

```text
emerging
→ reinforced
→ established
→ superseded / disputed when later evidence changes it
```

### Emerging

Observed in real work with clear provenance.

May be reused cautiously in similar contexts as experience, not stated as
formal company policy.

### Reinforced

The same principle is independently repeated, successfully reused, or explicitly
supported again in later work.

### Established

The experience has accumulated enough consistent real-world support to be
treated as a mature operating practice within its defined scope.

"Established" still does not automatically mean formal policy.

### Disputed / superseded

Later employee correction, changed business conditions, or authoritative
documentation contradicts the prior experience.

Hermes should refine or retire the experience rather than preserving it as an
eternal rule.

Do not use simplistic usage counts alone as truth. Repeated use is evidence, not
proof. Contradictions and applicability conditions matter.

## 10. Reuse must preserve provenance and uncertainty

When using employee-derived experience, Hermes should distinguish it from
authoritative company facts.

Appropriate behavior:

> Based on ARMOR's retained procurement experience, similar low-price quotations
> should also be checked for MOQ, payment terms, lead time, and inventory risk.

Inappropriate behavior:

> Company policy requires this.

unless an actual policy authority supports that statement.

When experience conflicts with authoritative documentation, the authoritative
source wins unless governance explicitly changes that authority.

## 11. Promotion ladder

Most experience should remain useful experience. It does not need to be
"promoted" merely to justify its existence.

Promotion is reserved for cases where the object has clearly matured into a
different authority type.

```text
Role Experience
   │
   ├─ remains experience → governed Vault / Wiki working memory
   │
   ├─ stable factual/reference knowledge → WeKnora
   │
   ├─ repeatable work method → Hermes Skill
   │
   └─ formal behavior / company policy → Profile/SOUL or controlled policy source
```

### Experience → WeKnora

Use the existing Knowledge Intake authority. Do not silently auto-ingest normal
Vault experience into WeKnora.

### Experience → Skill

Prefer a proposal/staged change rather than silent production mutation.
Company-owned Skills remain version-controlled where practical.

### Experience → Profile / policy

This is high impact and should be rare. Any change that alters authorization,
external commitments, company policy, or high-risk behavior requires explicit
existing human authority.

Self-Evolution must never grant itself new permissions.

## 12. Human-interruption policy

Human attention is a scarce business resource.

Use this order:

```text
no interruption
→ passive correction through normal conversation
→ one-step source confirmation only when ambiguity matters
→ explicit approval only for high-impact promotion or side effects
```

Do not ask for confirmation when the employee has already clearly stated the
experience and there is no meaningful ambiguity.

Do not repeatedly ask employees to approve minor wording refinements.

The system should learn primarily from work that is already happening.

## 13. Risk classes

### Low-risk learning

Examples:

- lessons learned;
- role heuristics;
- warnings;
- contextual preferences;
- procedure tips without external side effects.

Default: retain with provenance and appropriate confidence.

### Medium-risk learning

Examples:

- reusable procedures that materially influence business output;
- cross-role practices;
- changes to shared Skills.

Default: stage/propose using existing Skill and repository governance when the
change would affect shared runtime behavior.

### High-risk learning

Examples:

- authorization changes;
- payment or financial controls;
- legal/compliance rules;
- external customer commitments;
- autonomous sending/publishing;
- system permissions;
- secrets or credential handling.

Default: never become active through autonomous learning alone.

## 14. Privacy, trust, and employee relationship

Self-Evolution must not become employee surveillance.

Do not use the experience system to:

- rank employee competence;
- create hidden productivity scores;
- infer performance ratings;
- retain private employee conversations unrelated to reusable work;
- attribute mistakes publicly when attribution is unnecessary;
- build an HR evaluation database.

The purpose is to preserve organizational capability, not evaluate people.

Where identity is not needed for later use, prefer role/domain provenance over
unnecessary personal exposure while retaining enough audit provenance for
governed correction when required.

## 15. Hermes native Self-Improvement: audit before enablement

EAO should prefer upstream Hermes capability over custom infrastructure, but the
repository must not assume a feature exists merely because a newer upstream
release documents it.

Before runtime enablement, audit the exact deployed Hermes build for:

- background self-improvement/review behavior;
- Skill create/update/delete primitives;
- staged or approval-gated Skill writes;
- Memory write approval behavior;
- pending change persistence;
- reviewer/approval authority;
- Profile isolation;
- external/shared Skill-directory mutation behavior;
- whether ordinary employees can approve their own shared production changes;
- whether the feature can operate without generic shell/filesystem exposure.

Required security outcome:

```text
ordinary employee
≠ authority to approve shared high-impact production behavior
```

If the deployed version lacks a safe native primitive, prefer a thin adaptation
around existing Vault/Skill authorities. Do not introduce a new learning
platform unless a precise residual gap remains after the Capability Reuse Pass.
The repository-side Operations Skill mutation boundary is implemented in [infrastructure/hermes/plugins/skill-mutation-guard/](../infrastructure/hermes/plugins/skill-mutation-guard/) and remains disabled until the Phase 0 audit and isolated runtime acceptance are complete.

## 16. Implementation phases

### Phase 0 — Capability Audit

No production behavior change.

Determine what the actual deployed Hermes runtime can safely reuse.

Output:

- exact supported native Self-Improvement primitives;
- permission and isolation behavior;
- gap analysis;
- smallest implementation path;
- rollback and acceptance plan.

### Phase 1 — Shadow Experience Capture

Goal: prove that Hermes can recognize useful experience without disturbing
employees.

Rules:

- do not change production Skills or SOUL;
- do not publish to WeKnora automatically;
- avoid routine employee confirmation prompts;
- inspect precision: is the Agent extracting reusable lessons rather than noise?
- use only a bounded pilot role/domain.

Success means the system can "understand what the employee taught it" with
minimal human effort.

### Phase 2 — Scoped Experience Reuse

Allow accepted low-risk role experience to be retrieved in relevant work.

Validate:

- correct role/domain scoping;
- provenance-aware wording;
- contradiction handling;
- no generic filesystem exposure;
- employee can naturally correct outdated experience;
- no material increase in employee workload.

### Phase 3 — Governed Procedural Evolution

Use accumulated experience to propose improvements to reusable Skills or formal
knowledge.

Prefer native staged Skill changes when proven safe.

Production Skill/policy changes remain inside existing repository/governance
authority.

### Phase 4 — Closed Learning Loop

Target:

```text
work
→ experience
→ reuse
→ result
→ correction/reinforcement
→ refinement
→ better future work
```

Do not open this phase merely because capture works. It requires evidence that
the loop improves work without causing knowledge pollution or human-maintenance
burden.

## 17. Acceptance principles

A Self-Evolution implementation is not accepted merely because it can save text.

It must prove:

### Human workload

- no new mandatory employee form;
- no new universal knowledge-review position;
- no routine central review queue for low-risk experience;
- normal employees can teach through normal work;
- interruption is exceptional and proportionate.

### Learning quality

- reusable corrections are captured;
- one-off instructions are not routinely misclassified as company experience;
- applicability/context is preserved;
- later corrections can refine or supersede prior experience;
- authoritative knowledge is not silently overridden.

### Safety

- employee experience cannot grant new permissions;
- low-confidence experience is not presented as policy;
- sensitive material is not retained unnecessarily;
- generic employee filesystem/shell access remains prohibited;
- high-impact production changes require existing authority.

### Business value

The Agent should measurably become more useful in repeated real work.

If employees spend more time feeding, labeling, reviewing, or maintaining the
learning system than the system saves, the design has failed.

## 18. Anti-patterns

Do not implement Self-Evolution as:

- "turn on long-term Memory for everyone";
- automatic ingestion of all conversations into RAG;
- automatic conversion of every correction into a Skill;
- a central employee-experience review department;
- a large approval workflow for routine lessons;
- a second knowledge database;
- a new workflow engine;
- a generic filesystem granted to business Profiles;
- an employee scoring or surveillance system;
- an autonomous permission-escalation mechanism.

## 19. Relationship to existing EAO authorities

This document complements rather than replaces:

- `CAPABILITY-REUSE-PASS.md` — reuse before build;
- `KNOWLEDGE.md` — WeKnora / Vault authority boundary;
- `KNOWLEDGE-INTAKE.md` — durable approved knowledge ingestion;
- `PROFILE-STANDARD.md` — Profile, memory, Skill, and tool boundaries;
- `SKILL-ADMISSION.md` — external Skill admission;
- `REPOSITORY-GOVERNANCE.md` — company-owned runtime/configuration change authority;
- `EAO-ADMIN-CONSOLE-V1A.md` — administrator review/governance plane.

When conflicts appear, higher-order repository contracts and existing security
boundaries remain authoritative.

## 20. Current production statement

As of this design baseline:

```text
Enterprise Self-Evolution architecture: DEFINED
Employee experience capture runtime: NOT YET ENABLED
Employee Hermes long-term memory: remains OFF
Autonomous production Skill mutation: NOT AUTHORIZED
Automatic Vault → WeKnora promotion: PROHIBITED
New review job/role: NOT REQUIRED
```

The next action is Phase 0 runtime capability audit on the designated EAO host.
That audit must inspect the actual Hermes installation before any Self-Evolution
runtime feature is enabled.
