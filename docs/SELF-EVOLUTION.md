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

These remain version-controlled EAO/company assets and may be exposed through
Hermes `skills.external_dirs`.

Hermes 0.21.2 source-level behavior provides an important but limited guard:
autonomous Background Review treats external Skills as externally owned and
refuses to mutate them.

That guard is **not** a complete write-protection boundary. A foreground,
user-directed `skill_manage` call may still update an external Skill when the
Hermes process has filesystem write permission to that directory.

Therefore the EAO boundary must be:

```text
Profile-local agent-created Skills
→ writable
→ autonomous low-risk learning allowed

company shared/frozen Skills in external_dirs
→ readable by the Profile
→ filesystem read-only to the employee Hermes learning path
→ version-controlled source remains authoritative
```

This is a one-time deployment boundary, not a recurring human approval
workflow.

The first implementation must prove both behaviors on the exact deployed build:

1. Background Review cannot mutate an external company Skill.
2. A foreground `skill_manage` attempt also cannot persist changes to that
   company Skill because the deployed company-Skill path is read-only to the
   employee Profile runtime.

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
    - <READ_ONLY_APPROVED_COMPANY_SHARED_SKILL_DIRS>
  create_dir: ""
  creation_nudge_interval: <PILOT_MEASURED_VALUE>
  write_approval: false
  guard_agent_created: true
  ledger: true

curator:
  enabled: true
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
- Curator consolidation remains off initially; automatic lifecycle cleanup is
  lower risk than LLM-driven consolidation and should be evaluated separately.
- Existing company Skill directories remain external/version-controlled.

### 21.5A Tool-surface requirement

Hermes' native Skill self-improvement does not run merely because
`auxiliary.background_review.enabled=true`.

The Skill trigger requires `skill_manage` to exist in the active Agent tool
surface. In EAO, employee API Profiles use explicit toolset allowlists, so the
Self-Evolution pilot must deliberately add the Hermes `skills` toolset to the
target Profile's API surface.

Conceptually:

```yaml
platform_toolsets:
  api_server:
    - skills
    - <existing approved toolsets>
```

The Hermes `skills` toolset contains:

```text
skills_list
skill_view
skill_manage
```

This is a real capability change and must receive the same acceptance treatment
as any other Profile tool-surface change.

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

Hermes 0.21.2 skill review is triggered by accumulated **tool-calling
iterations**:

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
Phase 1 shadow pilot
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

### 21.9 Phase 0 — actual production runtime audit contract

Before changing the ARMOR reference runtime, verify on the designated host:

```text
Hermes version
Hermes source commit
active Operations Profile path/config
employee memory flags
auxiliary.background_review effective config
skills.external_dirs
skills.create_dir
skills.write_approval
skills.guard_agent_created
skills.ledger
curator enabled/consolidate settings
effective Operations tool surface
actual shared/frozen Skill directories
```

Then prove, on the exact build:

1. Memory remains unavailable to the employee Profile.
2. Background Review can still perform Skill-only self-improvement.
3. The target employee Profile exposes the `skills` toolset but does not gain
   terminal, generic filesystem, browser, coding delegation, secrets, or new
   MCP authority merely because Self-Evolution is enabled.
4. A Background Review-created Skill lands only in the intended Profile-local
   Skill directory and is recorded as autonomously managed learning state.
5. A Skill in an EAO company `external_dirs` directory cannot be autonomously
   patched or deleted by Background Review.
6. The deployed company-Skill directory is read-only to the employee learning
   path, and a foreground `skill_manage` mutation attempt cannot persist there.
7. Profile-local Skill create/patch still succeeds.
8. A restart preserves the intended Profile-local learned Skill and does not
   alter the external shared Skill baseline.

No production setting changes are authorized by this document alone.

### 21.10 Phase 1 — Shadow Learning Pilot

Use one bounded Profile/domain and a finite test window.

Temporary pilot posture:

```text
Memory                              OFF
skills toolset                      ON for the pilot Profile
Background Review                   ON
Profile-local autonomous Skill path ON
Company external Skills             READ / USE, filesystem read-only
skills.creation_nudge_interval      LOW, chosen for observation
skills.write_approval               ON temporarily
Curator LLM consolidation           OFF
```

The approval queue is used only by the implementation team to inspect learning
quality during the pilot. It is not an employee workflow and it is not the
target operating model.

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
Company external Skills             filesystem read-only to employee learning path
Skill ledger                        ON
Curator                             ON
Curator LLM consolidation           OFF initially
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
- company `external_dirs` Skills are not autonomously mutated;
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
