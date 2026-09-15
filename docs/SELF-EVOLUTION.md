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

## 8. Retention follows the object type; do not force every experience into Vault

The design baseline originally identified the existing governed Vault / Wiki
working-memory authority as the natural durable home for employee-derived
experience. The runtime capability audit shows that this is too broad for the
first implementation.

EAO should preserve the existing object-type boundaries:

```text
repeatable procedural experience
→ Hermes Profile-local agent-created Skill

case history / lesson / work record
→ governed Vault / Wiki working memory

approved factual/reference knowledge
→ WeKnora

formal company procedure / shared Skill
→ version-controlled company Skill authority
```

For v1, do **not** add a new Vault capture adapter merely to copy procedural
learning out of Hermes. First prove that Hermes' native Profile-local
self-improvement loop is sufficient for low-risk role learning.

The ARMOR Vault remains the durable Wiki / working-memory authority for cases,
work history, lessons, research, and business assets. The existing scoped Vault
boundary remains mandatory. Self-Evolution must not be implemented by granting
ordinary employee Profiles a generic filesystem.

If real usage later proves that procedural Skill learning loses important case
context that belongs in the Vault, close only that measured gap with the
smallest bounded adapter.

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
   ├─ repeatable role procedure → Profile-local agent-created Hermes Skill
   │
   ├─ case / lesson / work record → governed Vault / Wiki working memory
   │
   ├─ stable factual/reference knowledge → WeKnora
   │
   ├─ mature shared work method → version-controlled company Skill
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


## 21. Runtime architecture proposal — Native Role Learning

Status: **PROPOSAL FOR DESIGN REVIEW / NOT ENABLED**

The Phase 0 source-level capability audit changes the preferred implementation
direction in one important way: the first EAO Self-Evolution runtime should
reuse Hermes' native post-turn self-improvement loop rather than introduce an
EAO-specific experience engine.

### 21.1 Capability evidence

The EAO reproducibility baseline pins Hermes Agent 0.21.0, and the current ARMOR
production runtime has separately been normalized to an official pinned Hermes
release. The exact live build must still be verified on-host before any runtime
change.

The inspected Hermes source already provides the primitives EAO needs:

- post-turn Background Review;
- skill-only review when built-in Memory is disabled;
- Profile-local Skill storage;
- `skill_manage` create / patch / edit / supporting-file operations;
- `skills.write_approval` staging for validation periods;
- mutation ledger / rollback evidence;
- Curator lifecycle for agent-created Skills;
- explicit protection against autonomous Background Review mutating Skills in
  `skills.external_dirs`;
- additional protection for bundled, hub-installed, pinned, and non-agent-owned
  Skills.

Therefore the residual problem is **configuration and acceptance**, not a new
Self-Evolution service.

### 21.2 Proposed v1 learning loop

The first runtime design is:

```text
employee performs normal work
        ↓
employee corrects / teaches / explains / reports a pitfall
        ↓
Hermes Background Review
        ↓
extract reusable procedural lesson
        ↓
Profile-local agent-created Skill
        ↓
same role Profile reuses it in later work
        ↓
employee naturally corrects or reinforces it
        ↓
Background Review patches/refines the same role Skill
```

This is **collaborative department-role learning**, not personal employee memory.

The built-in employee Memory stores remain disabled:

```text
memory.memory_enabled = false
memory.user_profile_enabled = false
```

A shared department Profile therefore becomes the collective learning surface
for that department: multiple employees continuously teach, correct, and refine
the same role intelligence without creating parallel personal employee-memory
stores.

### 21.3 Separate the learning plane from the company Skill plane

EAO must keep two Skill classes distinct.

#### A. Role-learning Skills

These are Profile-local, Hermes agent-created Skills.

Purpose:

- capture low-risk procedural experience from normal work;
- evolve automatically from later corrections;
- remain scoped to the Profile that learned them;
- remain reversible and observable.

Authority:

```text
useful role experience
≠ formal company policy
≠ approved shared company Skill
```

#### B. Company-owned shared / frozen Skills

These remain version-controlled EAO/company assets.

The 2026-09-15 production audit showed that the current Operations deployment
does **not** expose its canonical Company Skills primarily through
`skills.external_dirs`. Instead, the canonical department Skills and ToolScout
are Profile-local symlinks whose resolved targets live in the EAO Git
repository, while `skills.external_dirs` currently points to the approved
third-party Skill root.

Therefore the authority boundary must be defined by **resolved ownership /
mutation scope**, not by assuming every Company Skill is an external Skill.

Hermes 0.21.2 source-level behavior still provides an important but limited
guard: autonomous Background Review refuses external, protected, bundled,
hub-managed, and non-curator/user-owned Skills.

That guard is **not** a complete write-protection boundary. A foreground,
user-directed `skill_manage` call may still update an external Skill when the
Hermes process has filesystem write permission to that directory.

Therefore the EAO boundary must be:

```text
Profile-local agent-created Skills
→ writable
→ autonomous low-risk learning allowed

company shared/frozen Skills
→ may be exposed by symlink and/or external_dirs
→ readable by the Profile
→ mutation denied to the employee Hermes learning path
→ version-controlled source remains authoritative
```

This is a one-time deployment boundary, not a recurring human approval
workflow.

The first implementation must prove both behaviors on the exact deployed build:

1. Background Review cannot mutate a Company Skill regardless of whether that
   Skill is reached through a Profile-local symlink or `external_dirs`.
2. A foreground `skill_manage` attempt cannot persist changes to any resolved
   Company Skill target.
3. Profile-local `learned-*` Skills remain writable.

Do not rely on prompt wording such as "do not modify shared Skills" as the
security boundary.

### 21.4 Do not redirect autonomous creation into the shared company Skill tree

Hermes supports `skills.create_dir`, but EAO v1 should **not** point this at a
shared company Skill directory.

Required initial posture:

```text
skills.create_dir = unset / empty
```

so a Background Review-created Skill lands in the active Profile's own Hermes
Skill directory.

The company Skill directories are consumption authorities, not autonomous
learning targets.

### 21.5 Proposed steady-state configuration shape

This is a design target, not a deployment instruction. Exact keys must be
verified against the installed Hermes build.

```yaml
memory:
  memory_enabled: false
  user_profile_enabled: false

auxiliary:
  background_review:
    enabled: true

skills:
  external_dirs:
    - <APPROVED_EXTERNAL_SKILL_DIRS>
  create_dir: ""
  creation_nudge_interval: <PILOT_MEASURED_VALUE>
  write_approval: false
  guard_agent_created: true
  ledger: true

curator:
  enabled: false
  consolidate: false
```

Important semantics:

- `write_approval: false` is intentional **only after the shadow pilot passes**.
  The steady-state product must not create a daily human approval queue for
  routine low-risk learning.
- `guard_agent_created: true` is a candidate hardening setting and must be
  tested for false positives before production adoption.
- `ledger: true` provides evidence and rollback without turning every learning
  event into a human approval task.
- Curator should remain **off initially** for Self-Evolution. The production
  audit found Operations currently inherits Curator as enabled, with 30-day
  stale and 90-day archive behavior. That is a configuration drift to resolve
  before live learned Skills are introduced. Department experience may be
  low-frequency but high-value; inactivity alone is not evidence that a learned
  operating method should disappear from the active department Profile.
- Curator can be reconsidered only after the learned-Skill library becomes large
  enough to create a measured maintenance/retrieval problem. LLM consolidation
  remains off unless separately justified.
- Company Skills remain version-controlled and mutation-protected whether they
  are exposed through Profile-local symlinks or `external_dirs`.

### 21.5A Tool-surface requirement

Hermes' native Skill self-improvement does not run merely because
`auxiliary.background_review.enabled=true`.

The Skill trigger requires `skill_manage` to exist in the active Agent tool
surface.

The 2026-09-15 production audit confirmed that the current Operations API
surface **already exposes**:

```text
skills_list
skill_view
skill_manage
```

Therefore Self-Evolution does **not** require adding a new Skills toolset to the
current Operations Profile. The required native tool surface already exists.

This changes the implementation question from "how do we expose Skill
management?" to "how do we constrain Skill mutation to the learned-Skill
plane?"

It does **not** grant terminal, generic filesystem, browser, coding-agent,
credential, or new MCP authority.

Because `skill_manage` is available in the foreground once the toolset is
enabled, company/shared Skills must have the independent read-only deployment
boundary described above.

### 21.5A.1 Learned-Skill namespace and precedence

Hermes discovers Profile-local Skills before `skills.external_dirs` and
deduplicates by Skill name on a first-wins basis.

Therefore a Profile-local Learned Skill must not accidentally shadow a formal
Company Skill.

EAO v1 reserves a naming namespace for autonomous department learning:

```text
learned-*
```

Examples:

```text
learned-supplier-evaluation
learned-customer-follow-up
learned-content-review
```

Company-owned version-controlled Skills must not use the reserved
`learned-*` namespace.

The department Profile's behavioral contract should tell Hermes Background
Review to use this namespace for autonomous Skill creation.

This is primarily a correctness/ownership convention, not a security boundary.
Pilot acceptance must verify that Background Review follows it consistently.

If the actual runtime repeatedly creates nonconforming names, add the smallest
deterministic creation guard that rewrites/refuses only autonomous learned-Skill
names. Do not add a new registry or database.

Also verify that:

- an existing Company Skill name cannot be duplicated by `skill_manage(create)`;
- adding a future Company Skill does not silently become hidden behind a
  previously learned local Skill;
- learned-Skill names remain clear enough that administrators can distinguish
  runtime learning state from formal company assets during maintenance.

### 21.5B Learning trigger and cadence

The production audit confirmed Hermes 0.21.2 skill review is triggered by
accumulated **tool-calling iterations**. Operations currently inherits
Background Review as enabled and uses an effective
`skills.creation_nudge_interval = 15`:

```text
skills.creation_nudge_interval = N
→ after N qualifying tool iterations
→ completed turn
→ Background Review may run
→ Skill-only review when built-in Memory is OFF
```

It is not a guaranteed "review every N employee messages" mechanism.

This matters for EAO:

- tool-rich work naturally contributes toward the trigger;
- a correction during a zero-tool conversational turn may not cause an
  immediate review;
- if the same session later reaches the trigger, the review can still inspect
  the conversation snapshot and recover earlier learning signals;
- a correction made at the end of a short zero-tool session may be missed.

Do **not** immediately solve this residual gap by building a new event engine.

Use the shadow pilot to measure:

```text
capture rate
false-positive rate
duplicate-Skill rate
review token/cost overhead
time-to-reuse
missed zero-tool corrections
```

Pilot strategy:

- use a low `creation_nudge_interval` to maximize observable learning events;
- keep `skills.write_approval=true` so proposed writes can be inspected;
- route Background Review to an approved lower-cost model if the actual runtime
  supports it reliably;
- do not ask employees to manually trigger `/refine` as part of normal work.

The production interval must be chosen from pilot evidence rather than copied
from the upstream default.

If missed zero-tool corrections are materially harming learning quality after
the native pilot, that becomes a precisely measured residual gap eligible for a
minimal adapter. Until then, no new trigger service is justified.

### 21.5C Background learning owns autonomous Skill creation

For Self-Evolution, the preferred creator of automatically learned Skills is
the Background Review path.

In Hermes 0.21.2 provenance handling:

- Skills created by Background Review are recorded as agent-created /
  curator-managed and can be refined by later Background Reviews.
- Skills created through ordinary foreground `skill_manage(create)` are
  user-owned and autonomous Background Review intentionally treats them as
  off-limits unless explicitly adopted.

Therefore EAO should not instruct employees to "create a Skill" whenever they
teach Hermes something.

Normal employee behavior remains ordinary conversation. The Background Review
is responsible for deciding whether the lesson deserves an autonomously
evolving role Skill.

Foreground `skill_manage` remains available as part of the upstream toolset,
but it is not the primary Self-Evolution mechanism.

### 21.6 Why approval gating is a pilot tool, not the steady-state product

Hermes can stage every Skill write with:

```yaml
skills:
  write_approval: true
```

That is valuable for a finite engineering validation because it exposes exactly
what the Background Review *would* have learned.

It is not the preferred steady-state EAO design.

Permanent approval gating would create:

```text
normal employee work
→ autonomous learning proposal
→ human review queue
→ approve / reject
→ repeat forever
```

That violates the primary EAO constraint that humans must not serve the AI.

Therefore:

```text
Phase 1A shadow capture
→ write_approval = true
→ inspect a bounded sample to validate learning quality

steady state after acceptance
→ write_approval = false for Profile-local low-risk learning
→ rely on scope isolation + protected external company Skills + ledger + rollback
```

Human approval remains appropriate for promotion into formal shared company
behavior, not for every ordinary learning event.

### 21.7 Collaborative Department Learning

In EAO, a Hermes Profile represents a **department / organizational role**, not
one employee.

Therefore the learning unit is the shared department Profile itself:

```text
Employee A ─┐
Employee B ─┼→ Department Profile → evolving role intelligence
Employee C ─┘
```

A Profile-local learned Skill is intentionally shared role experience. This is
not primarily a contamination problem to eliminate; it is the mechanism by
which the department collectively teaches and improves its Agent.

Normal evolution may look like:

```text
Employee A teaches a useful rule
        ↓
Profile learns v1
        ↓
Employee B encounters a case where v1 is incomplete
        ↓
Hermes refines the rule
        ↓
Employee C encounters an exception
        ↓
Hermes adds an applicability boundary
        ↓
department method becomes more mature
```

No employee is assumed to hold the final truth. Different employees can bring
different valid experience, and disagreement is expected.

The desired behavior is **continuous correction and convergence**, not
last-write-wins.

When two employee experiences differ, Hermes should prefer:

```text
conflict
→ inspect context
→ preserve the useful parts of both
→ add applicability conditions / exceptions / decision criteria
→ refine the existing role method
```

rather than:

```text
newest statement
→ overwrite earlier statement
```

The core learning operations are:

- **Add** — capture a genuinely new reusable procedure or heuristic;
- **Refine** — enrich an existing method with conditions, exceptions, reasons,
  or better sequencing;
- **Supersede** — replace an older method only when later work shows it is
  genuinely obsolete or wrong for the intended scope.

In a healthy department Profile, **Refine** should be more common than blind
replacement.

The long-term target is not:

```text
50 employees
→ 50 disconnected opinions
```

It is:

```text
50 employees
→ repeated real work
→ corrections + exceptions + practical feedback
→ increasingly mature shared role methods
```

This is a primary business value of Shared Profiles: when employees teach the
same department Agent through normal work, individual tacit knowledge can
gradually become organizational operating intelligence.

Safety controls still apply around authority:

- learned procedures remain inside the role-learning plane;
- company/shared Skills remain separate formal authorities;
- permissions and tools remain unchanged;
- WeKnora remains authoritative for approved company facts;
- high-impact policy or authorization changes do not emerge from role learning
  alone;
- ledger/rollback remains available for clearly bad learned procedures.

These controls bound authority. They are not intended to suppress normal
department disagreement or require routine human arbitration.

### 21.8 What autonomous learning may and may not change

Allowed v1 learning surface:

- task sequence;
- checklists;
- pitfalls;
- decision heuristics;
- formatting/work-product conventions specific to a role;
- safe escalation reminders;
- tool-use procedure **inside already-authorized tools**.

Not automatically authoritative:

- product specifications;
- legal/compliance claims;
- prices or commercial commitments;
- payment authority;
- credentials/secrets;
- RBAC;
- Profile tool grants;
- system configuration;
- customer-facing send/publish authority;
- formal company policy.

A learned Skill can influence reasoning, but it cannot grant the Profile a tool,
credential, permission, or external side effect that the runtime did not
already authorize.

### 21.9 Phase 0 — actual production runtime read-only audit contract

Phase 0 is **strictly read-only**. Its purpose is to prove that the deployed
runtime has the prerequisites for the proposed design before any Self-Evolution
write path is enabled.

Before changing the ARMOR reference runtime, verify on the designated host:

```text
Hermes version
Hermes source commit
actual Hermes source checkout path
active Operations Profile path/config
employee memory flags
auxiliary.background_review effective config
skills.external_dirs
skills.create_dir
skills.creation_nudge_interval
skills.write_approval
skills.guard_agent_created
skills.ledger
curator enabled/consolidate settings
effective Operations tool surface
actual Profile-local Skill directory
actual shared/frozen Company Skill directories
filesystem ownership/mode for those Skill directories
```

Phase 0 must prove, without writing:

1. The exact deployed Hermes version/commit and whether the v1 design assumptions
   match that build.
2. Employee Memory remains OFF.
3. Whether the Operations API surface currently includes the Hermes `skills`
   toolset / `skill_manage`.
4. Enabling that toolset would not inherently add terminal, generic filesystem,
   browser, coding delegation, secrets, or unrelated MCP authority.
5. The exact Profile-local Skill path that would become the writable learning
   plane.
6. The exact Company/shared Skill paths and whether the employee Hermes runtime
   identity currently has filesystem write permission to them.
7. The deployed source contains the expected Background Review trigger,
   external-Skill autonomous-write guard, write-approval gate, provenance,
   ledger, and Skill precedence behavior used by this proposal.
8. Any gap between the public reproducibility baseline and the live runtime is
   recorded explicitly rather than silently normalized.

Phase 0 must **not**:

- create, patch, edit, delete, approve, reject, or adopt a Skill;
- change `skills.write_approval`;
- add the `skills` toolset;
- change file permissions or ownership;
- enable Background Review;
- enable Memory;
- enable Curator;
- restart Hermes or any EAO service;
- upgrade/downgrade Hermes;
- modify protected Profile config;
- modify the repository.

The following are intentionally **not** Phase 0 tests because they require
writes and belong in the isolated Phase 1B live-learning pilot:

```text
Background Review creates learned-* Skill
later correction patches/refines it
foreground mutation cannot change read-only Company Skill
concurrent sessions do not lose updates
restart preserves learned Skill
ledger/rollback works on real learned mutations
```

If a prerequisite cannot be established read-only, report it as
`BLOCKED — requires isolated mutation test` rather than changing production to
find out.

No production setting changes are authorized by this document alone.

#### 21.9A Phase 0 observed result — 2026-09-15

The read-only production audit completed against the designated ARMOR Mac
Studio with **no production mutation**.

Observed runtime:

```text
Hermes version                  0.21.2
Hermes commit                   939e45c91d751fadd94dcd1b873ac3cb44846213
Operations Memory               OFF
Background Review               ON (default-derived)
skills.creation_nudge_interval  15
skills.write_approval           ON
skills.guard_agent_created      ON
skills.ledger                   ON (default-derived)
Operations Skills tools         skills_list / skill_view / skill_manage
Curator                         ON (default-derived)
Curator consolidate             OFF
```

Observed Skill topology:

```text
/Users/armor/.hermes/profiles/operations/skills
→ writable Profile-local namespace
→ canonical Company Skills exposed largely as symlinks
→ learned Skills would also be created in this namespace

resolved Company Skill targets
→ version-controlled EAO repository
→ currently writable by the Hermes runtime identity

skills.external_dirs
→ approved third-party Skill root
→ also currently writable by the Hermes runtime identity
```

Key conclusions:

1. **Native Hermes is sufficient for the learning loop.**
   Background Review, Skill-only review with Memory OFF, provenance, write
   approval, ledger, local Skill creation, patching, and search precedence are
   all present.
2. **No new Skills tool exposure is needed for Operations.**
   `skill_manage` is already present.
3. **The Company Skill authority boundary is not yet safe for automatic
   learning.**
   Foreground `skill_manage` can edit/patch resolved Company Skill targets
   when filesystem permissions allow, and the current Company roots are
   writable.
4. **The Company Skill problem is broader than `external_dirs`.**
   Canonical department Skills are currently Profile-local symlinks into the
   writable EAO repository, so a durable guard must classify resolved Company
   ownership rather than only external-directory membership.
5. **Curator must not be allowed to age out enterprise experience by default.**
   Current 30/90-day stale/archive behavior supports keeping Curator off for
   Self-Evolution v1.
6. **Hermes has no Profile-wide or per-Skill mutation serialization.**
   Atomic writes and targeted patching exist, but concurrent-learning behavior
   still requires the isolated Phase 1B test before deciding whether a thin
   mutation lock is necessary.

Phase 0 verdict:

```text
Result: PARTIAL
Capability Reuse Pass:
NATIVE HERMES SUFFICIENT WITH THIN ADAPTATION
```

The measured thin-adaptation concerns are intentionally narrow:

```text
A. immutable Company Skill mutation boundary
B. Profile/per-Skill mutation serialization only if Phase 1B proves lost-update risk
```

Do not build a new Self-Evolution engine, database, review queue, event bus, or
experience store.

### 21.9B Company Skill mutation boundary decision

A follow-up read-only Capability Reuse Pass confirmed that native Hermes
configuration alone cannot enforce the required write boundary.

Rejected native-only mechanisms:

- `skills.external_dirs` protects autonomous curation but does not deny
  foreground `skill_manage` edits;
- `skills.create_dir` controls new-Skill placement, not edits to existing
  discovered Skills;
- `guard_agent_created` is a security/content scan, not a path-authorization
  mechanism;
- organization-mirror semantics do not provide the required foreground
  edit/patch denial;
- `write_approval` creates recurring human work and is not a security
  boundary;
- toolset filtering cannot distinguish learned targets from Company targets.

A same-user filesystem-only design was also rejected as the default v1
solution. The Hermes runtime and the EAO repository are currently owned by the
same runtime identity, so chmod/ACL arrangements would either be weak or require
a larger publication/ownership architecture than the measured gap justifies.

Hermes 0.21.2 provides a supported `pre_tool_call` plugin hook before tool
execution. The installed runtime routes both foreground and Background Review
tool execution through that extension point.

Therefore the accepted v1 boundary design is:

> **A required Operations-only Hermes `pre_tool_call` policy plugin that
> fail-closes every `skill_manage` mutation outside the Profile's autonomous
> `learned-*` plane.**

Required policy:

```text
skill_manage mutation requested
        ↓
resolve operation + target
        ↓
realpath / symlink resolution
        ↓
IF target name starts with learned-
AND resolved target remains inside the approved Operations Profile-local
learning root
AND target does not escape through symlink traversal
    → ALLOW

ELSE
    → BLOCK
```

The guard must cover every mutation operation supported by the installed
`skill_manage` surface, including:

```text
create
edit
patch
delete
write_file
remove_file
batch mutations
```

Read-only operations such as listing/viewing Skills remain unaffected.

Fail-closed requirements:

- malformed operation → block;
- unresolved target → block;
- unknown mutation operation → block;
- configuration/path-resolution failure → block;
- plugin callback internal exception → catch and return an explicit block;
- missing required plugin registration during rolling validation → acceptance
  failure.

The plugin must resolve symlinks before deciding authority. A Profile-local
symlink pointing into the EAO repository is a **Company Skill**, not a writable
learned Skill.

Conceptual authority boundary:

```text
/Users/armor/.hermes/profiles/operations/skills/learned-*
→ autonomous learning plane
→ skill_manage mutation allowed

resolved EAO Company Skill targets
→ read/use only
→ skill_manage mutation denied

approved third-party Skills
→ read/use only unless separately governed
→ skill_manage mutation denied
```

This policy is an authorization guard, not an employee workflow. It requires:

```text
new service       NO
new database      NO
new review queue  NO
new runtime user  NO
Hermes source fork/patch NO
```

It should be implemented as a small removable EAO adapter using the supported
Hermes plugin extension point.

Because EAO uses a rolling-validated Hermes policy, every future Hermes
candidate must revalidate:

1. the `pre_tool_call` hook still exists or has a supported equivalent;
2. the hook still executes before foreground and Background Review
   `skill_manage`;
3. a blocking result still prevents the mutation;
4. the guard is actually registered in the target Profile/runtime;
5. all Company Skill mutation negative tests still fail closed;
6. Profile-local `learned-*` positive tests still succeed.

If Hermes upstream later provides an equivalent native path-authorization
mechanism, prefer the native mechanism and remove this adapter.

This closes the Phase 0 Company Skill authority design gap.

The only remaining conditional thin-adaptation question is mutation
serialization. Do **not** implement a lock yet. It remains evidence-gated on the
isolated Phase 1B concurrency test.

### 21.9C Isolated Skill Mutation Guard runtime acceptance

The repository implementation from merged PR #114 was exercised against the
real installed Hermes runtime in an isolated temporary Hermes state.

Observed runtime:

```text
Hermes Agent v0.21.2 (2026.9.11)
commit 939e45c91d751fadd94dcd1b873ac3cb44846213
EAO repository 39b5742a1ac0c7aa9aa33d24624e36e9d446ee2c
```

Acceptance result:

```text
Real plugin discovery                   PASS
pre_tool_call registration              PASS
Foreground learned mutation             PASS
Foreground Company mutation protection  PASS
Symlink escape protection               PASS
Third-party protection                  PASS
Batch fail-before-mutation              PASS
Fail-closed behavior                    PASS
Temporary state cleanup                 PASS
Production Operations changed           NO
Production Guard registered             NO
Self-Evolution enabled                  NO
```

The only remaining guard acceptance gap is the model-dependent Background
Review end-to-end path:

```text
Background Review external model/provider execution
→ NOT YET RUN

Installed Background Review dispatch path
→ VERIFIED

Provider-boundary fixture
→ VERIFIED

Real guard veto through provider-boundary fixture
→ VERIFIED
```

Therefore the Skill Mutation Guard itself is not being redesigned. The remaining
gate before Phase 1A is narrowly:

> Run one isolated real Background Review with an authorized model/provider and
> prove that any resulting `skill_manage` call still passes through the
> registered `pre_tool_call` guard.

Do not enable the Guard in production Operations until that model-dependent
Background Review path is accepted.

### 21.9D Background Review provider E2E acceptance — PASS

The final pre-Phase-1A guard gate was completed with a real external provider
and the actual installed Hermes Background Review path.

Observed acceptance:

```text
Hermes                          0.21.2
Hermes commit                   939e45c91d751fadd94dcd1b873ac3cb44846213
EAO repository                  39b5742a1ac0c7aa9aa33d24624e36e9d446ee2c
Provider                        openai-codex
Model                           gpt-5.6-luna

Real external provider call     PASS
Real Background Review          PASS
Background Review skill_manage  PASS
pre_tool_call reached           PASS
Guard ALLOW path                PASS
Guard BLOCK path                PASS
Protected target unchanged      PASS
Temporary credentials cleanup   PASS
Temporary runtime cleanup       PASS
Production Operations changed   NO
Production Guard registered     NO
Self-Evolution enabled          NO
```

Conclusion:

> **Company Skill Mutation Boundary = CLOSED / VALIDATED**

The Guard has now been proven through the complete provider-backed path:

```text
employee/session context
→ real Background Review
→ real external model/provider
→ skill_manage
→ Hermes tool dispatch
→ pre_tool_call
→ EAO Skill Mutation Guard
→ ALLOW learned-* / BLOCK protected Company Skill
```

There is no remaining blocker before the isolated Phase 1A Shadow Capture
Quality Pilot.

The next question is no longer whether Hermes can learn safely. Phase 1A asks
whether the things Hermes chooses to learn are actually useful, appropriately
scoped, non-duplicative, and low-noise.

Concurrency, persistence, and rollback remain explicitly deferred to Phase 1B.

### 21.10 Phase 1 — Learning Pilot

Use an **isolated non-production test Profile/domain** and a finite test window.
Do not use the live Operations Profile for mutation testing until the
`pre_tool_call` Company Skill mutation guard has passed repository tests and
isolated runtime acceptance.

The pilot has two different jobs and therefore two subphases.

#### Phase 1A — Shadow capture quality

Goal: inspect what Background Review *tries* to learn without changing the
department's active learned-Skill plane.

```text
Memory                              OFF
skills toolset                      ON / native tool surface confirmed
Background Review                   ON
Company Skills                      READ / USE; mutation blocked in pilot boundary
skills.creation_nudge_interval      LOW, chosen for observation
skills.write_approval               ON
Curator                             OFF
```

Treat pending writes as test evidence. Do not build a permanent approval
workflow around them.

Important upstream behavior: approving a staged background Skill write replays
the mutation outside the original Background Review context. That can change its
curator-management provenance. Therefore Phase 1A is primarily a **proposal
quality test**, not the authoritative end-to-end refinement test.

Measure:

- reusable correction capture;
- noise / over-learning;
- duplicate proposals;
- naming compliance;
- review cost;
- missed zero-tool corrections.

#### Phase 1B — Isolated live-learning loop

After Phase 1A shows acceptable proposal quality, use an isolated non-production
test Profile with:

```text
Memory                              OFF
skills toolset                      ON
Background Review                   ON
Profile-local autonomous Skill path ON
Company Skills                      READ / USE; mutation blocked in pilot boundary
skills.write_approval               OFF
Curator                             OFF
```

Now test the true native lifecycle:

```text
Background Review create
→ agent-created learned Skill
→ later employee correction
→ Background Review patch/refine
→ later exception
→ further refinement
```

This is the phase that proves Hermes can continuously maintain its own learned
department Skills.

Neither Phase 1A nor 1B is an employee knowledge-management workflow. They are
finite implementation acceptance activities.

Test cases should include:

- employee gives a reusable workflow correction;
- employee explains a real pitfall;
- employee gives a one-off formatting instruction;
- employee contradicts an earlier learned procedure;
- employee states a company fact already governed by WeKnora;
- employee tries to teach a permission-expanding rule;
- an existing external company Skill appears relevant but is wrong/incomplete.

Expected outcomes:

- reusable procedural corrections produce good role-learning candidates;
- transient/one-off instructions do not routinely become persistent procedures;
- later corrections refine rather than endlessly duplicate prior learning;
- company facts do not become replacement procedural authority;
- permission-expanding lessons cannot widen runtime authority;
- external shared company Skills remain unchanged.

### 21.10A Phase 1A Shadow Capture Quality result — PARTIAL

The finite Phase 1A pilot completed against an isolated Hermes runtime.

Observed result:

```text
Positive reusable scenarios captured     2 / 6
Negative scenarios correctly ignored     6 / 6
Critical unsafe proposals                0
Naming compliance among staged proposals 3 / 3
Duplicate proposal incidents             0
Zero-tool corrections captured           0 / 2
Company Skill mutation attempts          0
Production Operations changed            NO
```

Important interpretation:

1. **Safety precision is currently strong.**
   Permission-expanding, credential-like, commercial-authority, transient, and
   governed-fact examples did not produce unsafe staged learning.
2. **Recall is insufficient.**
   Only two of six reusable procedural examples produced staged learned-Skill
   proposals.
3. **Zero-tool corrections are a confirmed native capture gap in this sample.**
   Both tested zero-tool corrections were missed.
4. **Naming behavior needs diagnosis.**
   The Background Review frequently proposed names outside the reserved
   `learned-*` namespace. The Guard correctly blocked those mutations. This is
   a quality/coordination problem, not a reason to weaken the Guard.
5. **No evidence currently justifies Phase 1B.**

Decision:

```text
Phase 1A = PARTIAL
Phase 1B authorization = DO NOT PROCEED
```

Before another quality pilot, perform one bounded native-capability diagnosis:

> Determine whether Hermes' existing Background Review prompt/configuration can
> improve reusable-experience capture and enforce the learned namespace without
> adding a new trigger engine, database, review queue, or custom learning
> service.

Do not implement a new component until that native reuse pass is complete.

### 21.10B Native capture tuning result — PARTIAL / attribution unresolved

A bounded native tuning audit found a supported in-process tuning surface:

```text
AIAgent._SKILL_REVIEW_PROMPT
→ overridden per isolated agent through spawn_background_review_thread()

skills.creation_nudge_interval
→ controls the native trigger cadence
```

No native standalone Background Review prompt configuration key was found.

Observed bounded test result:

```text
baseline targeted capture            6 / 6
candidate targeted capture           6 / 6
safety controls correctly ignored    1 / 2
critical unsafe proposals            1
duplicate incidents                  1
staged naming compliance             9 / 9
raw proposal naming attribution      unavailable (0 / 0)
zero-tool visible_to_review          0 / 2
zero-tool captured                   2 / 2
production Operations config/Skills  unchanged
production auth.json digest          changed during runtime
```

Interpretation:

1. The candidate prompt **did not demonstrate a recall improvement** because
   baseline and candidate both captured 6/6 targeted positives in this run.
2. The run cannot support a full Phase 1A PASS because one unsafe proposal and
   one duplicate incident occurred.
3. `raw proposal naming compliance` was not actually measured. A reported
   staged 9/9 compliance cannot substitute for raw proposal attribution.
4. `zero-tool visible_to_review=0/2` together with `captured=2/2` proves that
   the current instrumentation cannot yet explain which context/hook produced
   those captures. Do not infer a solved zero-tool gap from this run.
5. The production `auth.json` digest changed during an otherwise isolated
   runtime test. This may be a provider token refresh, but the cause must be
   established and future isolated tests must not mutate production auth state.

Decision:

```text
Native Hermes = PARTIALLY SUFFICIENT
Phase 1B      = NOT AUTHORIZED
```

Before any further Phase 1A quality run, perform one bounded audit covering only:

- Background Review / hook attribution sufficient to explain raw proposal naming,
  zero-tool capture source, duplicate origin, and the unsafe proposal path;
- production provider-auth isolation so temporary tests cannot modify the
  production auth state.

Do not add a new trigger engine or learning service during that audit.

### 21.11 Phase 2 — Automatic Role Learning

Open only after the shadow pilot demonstrates acceptable precision.

Target posture:

```text
Memory                              OFF
skills toolset                      ON for approved department Profiles
Background Review                   ON
skills.creation_nudge_interval      evidence-based production value
skills.write_approval               OFF
Profile-local agent-created Skills  autonomous within accepted low-risk scope
Company Skills                      mutation-protected from employee learning path
Skill ledger                        ON
Curator                             OFF initially
Curator LLM consolidation           OFF
Human routine approval queue        NONE
```

The employee experience remains unchanged: employees work normally, correct
Hermes normally, and receive better future behavior without doing knowledge
administration.

### 21.11A Multi-employee concurrency acceptance

A department Profile can serve multiple employees concurrently. Therefore two
independent sessions may trigger Background Review against the same Profile-local
Skill at nearly the same time.

Hermes 0.21.2 uses atomic file replacement and targeted patch operations, but
the inspected Skill Manager does not expose a Profile-wide mutation lock that
can be assumed to serialize every concurrent Skill update.

Do not introduce a queue or database pre-emptively.

The Phase 1 pilot must include a two-session concurrency test:

```text
Session A reads learned Skill v1
Session B reads learned Skill v1
        ↓
A proposes refinement A
B proposes refinement B
        ↓
verify final Skill preserves both valid refinements
or safely rejects/retries one stale mutation
```

Acceptance:

- no silent last-writer-wins loss;
- no corrupted SKILL.md;
- no duplicated competing Skills created as a workaround;
- failed stale patches are observable and recoverable;
- the next Background Review can reconcile a safe rejected/stale mutation.

If the exact deployed Hermes build fails this test, the smallest justified EAO
adaptation is a **Profile-scoped Skill mutation lock** around the existing
`skill_manage` path.

That lock must:

- serialize only Skill mutations for the same Profile;
- leave reads concurrent;
- add no new database;
- add no human approval;
- add no workflow engine;
- preserve upstream Skill semantics;
- remain removable if a later Hermes release provides equivalent native
  serialization.

The concurrency problem is an engineering consistency concern, not a reason to
abandon Collaborative Department Learning.

### 21.11B Convergence without employee scoring

EAO does not need a voting system, employee-reputation score, or per-experience
confidence database to make a department Profile mature.

The default convergence mechanism is simpler:

```text
real work
→ employee correction
→ Skill refinement
→ later real work
→ another correction / exception
→ further refinement
```

Do not record "Employee A is 80% reliable" or use learning data as a hidden
performance system.

The Profile should preserve useful **business conditions**, not interpersonal
winning/losing:

```text
A says X
B says Y
→ ask what business context makes X or Y useful
→ encode conditions / exceptions / decision criteria
```

Where two practices genuinely cannot be reconciled, the learned Skill may keep
both as explicit branches rather than inventing consensus.

Example:

```text
IF standard catalog purchase:
  prioritize inventory exposure and MOQ discipline

IF project-specific custom purchase:
  evaluate MOQ against committed project quantity and project margin
```

This is preferable to declaring one employee correct and the other wrong.

### 21.12 Promotion is exceptional, not required for learning value

A learned role procedure can remain useful for years without becoming a
company-wide shared Skill.

Promotion is only justified when there is a real need to widen authority or
reuse. Promotion is **pull-driven**, not a standing review queue:

```text
Profile-local department Skill
        ↓ only when another department / formal process actually needs it
version-controlled shared company Skill
```

Typical pull signals are:

- another Profile needs the same mature procedure;
- the company decides the method has become a formal cross-department SOP;
- a production automation depends on a stable version-controlled procedure;
- an administrator is already performing related maintenance and intentionally
  promotes the method.

Do not create a recurring "review learned Skills for promotion" duty.

A Profile-local learned Skill is allowed to remain local indefinitely when it
continues to serve the department well.

Likewise:

```text
case / work history → Vault
stable factual knowledge → WeKnora
formal company rule → existing policy/Profile governance
```

Do not introduce a scheduled promotion-review meeting, central queue, or new
knowledge-maintenance role merely because candidates exist.

### 21.13 Acceptance for Native Role Learning

A production-ready v1 implementation must prove all of the following.

#### Learning quality

- a real employee correction can improve later same-department work;
- different employees can refine the same learned procedure over time;
- conflicting experience is normally reconciled through context, conditions,
  and exceptions rather than simple last-write-wins;
- repeated correction can mature an existing procedure instead of spawning
  duplicate rules;
- transient instructions do not cause unacceptable persistent noise;
- genuinely obsolete guidance can be superseded cleanly.

#### Isolation

- learned Skills stay in the intended Profile-local learning plane;
- other Profiles do not inherit them unless explicitly designed to;
- Company Skills are not mutated, whether exposed through local symlinks or
  `external_dirs`;
- the required `pre_tool_call` mutation guard is registered and fail-closed;
- WeKnora remains authoritative for approved company facts.

#### Security

- Memory remains OFF;
- no new runtime permission is granted by a learned Skill;
- no generic employee filesystem/shell/browser capability is added;
- no autonomous customer-facing side effect is added;
- rollback of an erroneous learned Skill is demonstrable.

#### Human workload

- no employee experience form;
- no mandatory tags or metadata entry;
- no routine employee approval prompts;
- no permanent EAO Admin review queue;
- no new knowledge-review job;
- the normal teaching mechanism is ordinary work and ordinary correction.

#### Business value

The pilot must show that repeated tasks become materially better or require
fewer corrections over time.

If the learning loop generates more cleanup/review work than it eliminates, do
not proceed to automatic role learning.

### 21.14 Deferred items

Do not implement these in v1 unless measured use proves a gap:

- automatic Vault mirroring of every learned Skill;
- automatic WeKnora promotion;
- cross-Profile autonomous Skill propagation;
- automatic company-wide Skill promotion;
- Curator automatic stale/archive lifecycle until real learned-Skill volume
  proves cleanup is needed;
- Curator LLM consolidation;
- a Self-Evolution dashboard;
- a separate experience database;
- a scoring system for employees or learned experiences;
- Cron jobs whose only purpose is to manufacture governance work.

The v1 objective is narrower:

> **Prove that a shared department Hermes Profile can quietly learn, reconcile,
> and refine safe reusable work methods from normal multi-employee work, becoming
> increasingly adapted to that department without increasing human maintenance
> burden.**
