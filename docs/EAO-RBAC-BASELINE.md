# EAO Operations Employees Permission Baseline v1

## Status

Status: CLOSED / FROZEN / PASS
Date: 2026-09-11

Future changes require a new explicit task and baseline version.

The baseline is an Open WebUI permission baseline. It does not change Hermes
architecture, WeKnora credential scope, Vault policy, the Skills set, service
versions, ports, Tailscale, authentication, or passwords.

## Permission resolution

    Role
      -> Open WebUI group membership
      -> default feature permissions
      -> resource ACL
      -> Hermes assistant/profile

Open WebUI group permissions are intentionally empty for the employee groups;
employees inherit the default feature baseline and receive only the model ACLs
listed below. Group permissions are additive. A user who belongs to multiple
groups receives the union of their grants, so mutually exclusive roles must
not be assigned to the same user without an explicit review.

## Employee default baseline

### Allowed

- Basic chat, edit/delete message, continue, regenerate, feedback, export,
  temporary chat, speech-to-text, text-to-speech, file upload, and web upload.
- Folders, notes, and calendar.
- Model access only through an explicit resource ACL.
- General Assistant and Operations Assistant through explicit READ ACLs only.
- Company Knowledge retrieval through Hermes and WeKnora; no Open WebUI
  Knowledge Workspace access is required.
- Approved Operations Skills and approved Enterprise Web Research remain
  bounded by the Hermes Operations profile.

### Denied

- Workspace management and settings, including models, knowledge, prompts,
  tools, functions, skills, channels, automations, webhooks, and direct tool
  servers.
- Sharing, public share links, chat import, access-grant administration,
  API-key administration, and user/group administration.
- Chat controls, valves, system-prompt editing, parameter editing, call, and
  multiple-model mode.
- Native web search, image generation, code interpreter, and memories.
- Model write/manage/share ACLs, Knowledge write/manage, Tool create/manage,
  and Skill manage are denied.
- Forced temporary-chat mode is disabled; users retain the temporary-chat
  option.

## Group and model ACLs

| Group | Resource | Permission | Boundary |
|---|---|---|---|
| All Employees | General Assistant | READ | No write/manage/share ACL |
| Operations Employees | Operations Assistant | READ | No write/manage/share ACL |

The Operations Employees group has no workspace permission grants. The
Operations Assistant has no Open WebUI Knowledge attachment. Company
Knowledge is reached through the Hermes Operations profile and WeKnora's
retrieve-only MCP contract.
Open WebUI Knowledge records = 0 is intentional. WeKnora access uses the
shared scoped service credential with full_access=false,
capabilities=["retrieve"], and scope=Company Knowledge. The credential value
is never stored in this repository.

## Operations execution path

    Employee
      -> Operations Assistant
      -> Hermes /p/operations
      -> Operations profile
      -> operations-weknora MCP namespace
      -> Company Knowledge retrieval

The operations-weknora name is a profile-local MCP namespace required to avoid
same-process MCP-name collision when the general and operations profiles share
one gateway. The command, arguments, environment contract, tools, and WeKnora
service remain unchanged. The Operations profile also pins
platforms.api_server.enabled: false so it uses the shared multiplexed gateway
listener rather than attempting a second port binding.

## Evidence and snapshots

Sanitized, secret-free, mode 0600 snapshots are stored at:

- docs/rbac/snapshots/operations-before-v1.json
- docs/rbac/snapshots/operations-after-v1.json

The after snapshot records the effective default baseline, group permissions,
model ACLs, and native Open WebUI resource counts. Before/after model ACLs and
resource counts were unchanged; the intended changes were the default feature
permissions and the Operations group permission object.

## Acceptance boundary

Success requires both conditions:

1. An Operations Employee can use Operations Assistant to retrieve Company
   Knowledge through /p/operations and WeKnora.
2. The same employee has no Open WebUI management permissions or write/manage/
   share ACL over the assistant.
