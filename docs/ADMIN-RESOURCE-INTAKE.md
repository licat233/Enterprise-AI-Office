# Administrator Resource Intake

> Administrator-facing entry point for introducing useful knowledge, tools, MCPs, services, or third-party Skills into Enterprise AI Office.
>
> This document is a router into existing EAO authorities. It does not create a new runtime, approval system, installer, knowledge store, or security boundary.

## Purpose

When an administrator discovers something useful, the default action is **review first, mutate later**.

~~~text
Discover resource
        ↓
Administrator / EAO review
        ↓
Capability Reuse Pass
        ↓
Classify the resource
        ↓
Use the existing authoritative intake/admission path
        ↓
Human approval where required
        ↓
Native or governed ingestion / installation
        ↓
Scoped exposure and authorization
        ↓
Verification
~~~

Core invariants:

~~~text
Reuse before build
Low friction != automatic production mutation
Installed != Exposed != Authorized
Prompt != security boundary
~~~

EAO Admin is a **review / governance entry point**, not a production superuser.

## I found something useful — what do I do?

| Resource | Start here | Authoritative path |
| --- | --- | --- |
| PDF, DOCX, Markdown, TXT, webpage, URL, research report, operating guide, durable factual/reference knowledge | [Knowledge Intake v1](KNOWLEDGE-INTAKE.md) | EAO Admin review → human confirmation → native WeKnora ingestion → retrieval verification |
| Tool, CLI, MCP Server, SaaS/API integration, external backend, scheduler, database, workflow engine, infrastructure component | [Capability Reuse Pass](CAPABILITY-REUSE-PASS.md) | Reuse existing authority first; add the smallest governed change only if a real capability gap remains |
| Third-party Skill | [Capability Reuse Pass](CAPABILITY-REUSE-PASS.md) → [Third-Party Skill Admission Standard](SKILL-ADMISSION.md) | DIRECT / ADAPT / DELEGATE / REJECT |

For MCP-specific inventory and exposure rules, also consult [MCP Control Plane](MCP-CONTROL-PLANE.md).

## Knowledge

Knowledge Intake v1 is already closed and frozen:

~~~text
KNOWLEDGE INTAKE V1:
CLOSED / FROZEN / PASS
~~~

The high-level path is:

~~~text
Discover source
→ EAO Admin Review
→ classify value / authority / duplication / conflict / KB / metadata
→ human confirmation
→ native WeKnora ingestion
→ parse/index acceptance
→ KB-scoped retrieval verification
→ optional Hermes verification
~~~

Knowledge Authority:

~~~text
WeKnora
~~~

Accepted administrator boundary:

~~~text
EAO Admin Review Plane:
ACTIVE / ACCEPTED

EAO Admin Knowledge Mutation:
BLOCKED / DISABLED
~~~

EAO Admin reviews and recommends. A human administrator performs the native WeKnora mutation. See [Knowledge Intake v1](KNOWLEDGE-INTAKE.md) for file, URL, manual text/Markdown, metadata, duplicate/conflict, parse/index, and retrieval-acceptance procedures.

## Tools, MCPs, services, and components

A newly discovered tool is not automatically a new EAO capability.

Start with the mandatory [Capability Reuse Pass](CAPABILITY-REUSE-PASS.md):

~~~text
existing EAO capability
→ Hermes native capability
→ installed / frozen Skills
→ Open WebUI / WeKnora native capability where relevant
→ existing governed EAO integrations
→ official upstream capability
→ third-party Skill admission when applicable
→ thin adapter
→ new infrastructure only as last resort
~~~

A valid result is:

~~~text
NO NEW COMPONENT REQUIRED
~~~

If a real gap remains, use the repository's normal governed change path:

~~~text
short-lived branch
→ explicit configuration / implementation
→ validation
→ Pull Request
→ merge
→ deployment
→ scoped Profile exposure
→ acceptance
~~~

For MCPs, use [MCP Control Plane](MCP-CONTROL-PLANE.md) for inventory and control-plane rules.

Do not grant EAO Admin generic shell, package-manager, Docker, SSH, filesystem, root, or equivalent production authority merely to make installation easier.

Tool/component introduction currently uses **Capability Reuse Pass + component-specific governance + repository governance**. There is no separate frozen “Tool Intake v1” contract.

## Third-party Skills

Third-party Skill intake starts with:

~~~text
Capability Reuse Pass
→ Third-Party Skill Admission Standard
~~~

The normative admission order is:

~~~text
DIRECT
→ ADAPT
→ DELEGATE
→ REJECT
~~~

- **DIRECT** — use the upstream Skill unchanged when it is portable and compatible with already-approved target Profile capabilities.
- **ADAPT** — add the smallest compatibility layer needed; do not fork the whole Skill for minor runtime assumptions.
- **DELEGATE** — keep genuinely backend-native work in an already-authorized Codex / Claude Code execution boundary.
- **REJECT** — reject duplication, unjustified privilege, unacceptable supply-chain/licensing risk, or excessive maintenance/security cost.

Security invariants:

~~~text
Skill procedure != runtime authority
trusted repository != every Skill approved
~~~

Admitting a Skill does not automatically grant shell, filesystem, credentials, package installation, delegation, external writes, or privileged network access. Permission remains bound to the target Profile and approved runtime.

The current authority is [Third-Party Skill Admission Standard](SKILL-ADMISSION.md). Existing pilot/runtime/production acceptance documents are evidence; they do not replace the normative admission standard.

## Who performs the actual mutation or installation?

Review and execution are intentionally separated.

Use the existing authoritative surface for the side effect:

- **Knowledge** → native WeKnora administration.
- **Repository-governed Tool / component changes** → Git / GitHub governance and approved technical execution.
- **MCP exposure/configuration** → existing EAO MCP/component control plane.
- **Third-party Skills** → supported Hermes external Skill mechanisms, thin adapters, or an already-authorized specialist backend according to SKILL-ADMISSION.md.
- **Component-native administration** → the component's approved administrative surface.

EAO Admin does not become a generic production mutation engine.

## Exposure after installation

After any Tool, MCP, service integration, or Skill is admitted, evaluate separately:

~~~text
Installed?
Exposed?
Authorized?
~~~

Installation alone does not make a capability available to every employee or Profile.

Exposure must remain least-privilege and Profile-scoped. Authorization must come from authenticated runtime controls, credentials, ACLs, allowlists, and component-native permissions — not prompt wording.

## Quick examples

### A useful PDF

~~~text
PDF
→ Knowledge Intake v1
→ EAO Admin review
→ human confirmation
→ native WeKnora upload
→ parse/index acceptance
→ retrieval verification
~~~

### A useful MCP Server

~~~text
MCP Server
→ Capability Reuse Pass
→ check whether current EAO/Hermes/MCP capabilities already satisfy the need
→ if a real gap remains, review component-specific security/maintenance impact
→ governed repository change
→ scoped exposure
→ acceptance
~~~

### A useful third-party Skill

~~~text
Skill repository
→ Capability Reuse Pass
→ SKILL-ADMISSION.md
→ inspect actual source/runtime requirements
→ DIRECT / ADAPT / DELEGATE / REJECT
→ governed admission
→ scoped exposure
→ acceptance
~~~

## Related authorities

- [Knowledge Intake v1](KNOWLEDGE-INTAKE.md)
- [Enterprise Knowledge Standard](KNOWLEDGE.md)
- [Capability Reuse Pass](CAPABILITY-REUSE-PASS.md)
- [Third-Party Skill Admission Standard](SKILL-ADMISSION.md)
- [MCP Control Plane](MCP-CONTROL-PLANE.md)
- [Repository Governance](REPOSITORY-GOVERNANCE.md)

When these documents overlap, follow the [Documentation Map](README.md) authority order.
