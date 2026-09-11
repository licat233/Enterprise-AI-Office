# Operations Employees RBAC Implementation Record

## Result

    EAO Operations RBAC v1
    Status: CLOSED / FROZEN / PASS
    Date: 2026-09-11
    Target: armor@MacStudio.local
    Open WebUI: v0.11.3, 0.0.0.0:13000 -> 8080

This record describes the implemented production state and its acceptance
evidence. It does not authorize future permission expansion.

## Implemented state

- The employee default baseline keeps ordinary chat, file/web upload,
  export, speech, temporary chat, folders, notes, and calendar available.
- Workspace administration, sharing, public share links, import, access
  grants, API keys, chat controls, valves, system-prompt/parameter editing,
  native web search, image generation, code interpreter, memories, call, and
  multiple-model mode are disabled.
- All Employees has READ access to General Assistant.
- Operations Employees has READ access to Operations Assistant.
- Both employee groups have an empty Open WebUI group-permission object; no
  employee group has workspace grants or write/manage/share ACLs.
- Operations Assistant has no native Open WebUI Knowledge attachment. Native
  Open WebUI knowledge, tool, function, skill, prompt, and similar management
  resources remain unavailable to employees.

## Knowledge-path verification

The tested path was:

    employee -> Operations Assistant -> Hermes /p/operations
             -> Operations profile -> operations-weknora MCP -> Company Knowledge

For the explicit WeKnora-only tests, the employee instructed the assistant not
to use web search or external sources. The Operations log recorded
mcp__operations_weknora__list_knowledge_bases and
mcp__operations_weknora__hybrid_search; no external web tool was used in these
tests.

| Test | Question class | Result | Status |
|---|---|---|---|
| A | Product input voltage for the 25 mm LED neon acrylic tube light | 24V; source filename armor-employee-product-knowledge-phase1a.csv | PASS |
| B | Meaning of ESL | Electronic Shelf Label; source filename armor-esl-technical-knowledge.md | PASS |
| C | Unsupported annual Enterprise AI Office lease cost | Explicit evidence was absent; assistant said the information was unavailable and did not guess | PASS |

The direct server-side evidence and the employee-visible answers agree. The
WeKnora contract remains retrieve-only and tenant-scoped.
Open WebUI Knowledge records = 0 is intentional. The shared WeKnora service
credential is scoped to Company Knowledge with full_access=false and
capabilities=["retrieve"]; the credential itself is excluded from this record.

## Regression and safety checks

- Operations Employee UI: PASS. Controls and management surfaces were absent;
  the employee could select General Assistant and Operations Assistant.
- Operations model routing: PASS. Group-only preview exposed Operations
  Assistant without workspace or knowledge grants.
- Admin boundary: PASS. Admin UI remained available only to the admin surface;
  employee APIs remained authenticated and unauthenticated model access
  returned HTTP 401.
- File upload: PASS. A non-production test file was accepted by the employee
  composer; the exact test artifact was removed after verification and the
  pre-existing file-row count was restored.
- Conversation persistence: PASS. The three post-fix test conversations were
  visible in the employee conversation history after completion.
- Restart persistence: PASS. Open WebUI was restarted without recreating its
  database or data volume; health and RBAC assertions remained valid.
- LAN access: PASS through macstudio.local:13000; Tailscale admin access was
  also verified.
- Runtime listeners: PASS. Only the established Open WebUI, Hermes, WeKnora,
  and local helper listeners were present; no new production port was added.
- Hermes Skills and Enterprise Web Research configuration: PASS and retained;
  explicit Knowledge-only tests did not invoke web research.

## Minimal Hermes runtime repairs

Two profile-local corrections were required for the requested route to be
real, without changing the Hermes or WeKnora architecture:

1. The secondary Operations profile explicitly disables its own API-server
   binding and therefore uses the existing multiplexed gateway listener.
2. Its existing WeKnora MCP key is named operations-weknora within that
   profile so both general and Operations MCP registrations coexist in the
   shared Hermes process.

No new service, credential, knowledge base, port, Skill, or external system
was introduced.

## Evidence files and change control

The sanitized before/after snapshots are in
docs/rbac/snapshots/operations-before-v1.json and
docs/rbac/snapshots/operations-after-v1.json. They contain no secrets or
personal data and are mode 0600 on the production host.

The implementation was applied to the production runtime and documented on
the current repository branch. The checked-in routing overlay is
infrastructure/hermes/operations-routing.example.yaml. Future changes require
a new explicit task and baseline version.
