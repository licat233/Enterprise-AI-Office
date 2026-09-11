---
type: "project-record"
status: "active"
created: "2026-09-09"
updated: "2026-09-09"
---

# Phase 4C — Scoped Vault Router Closure and MCP Runtime Activation

Phase 4C closes the Phase 4B fail-closed boundary without widening employee
permissions. The Enterprise repository now owns the deterministic ARMOR Router
used by `armor-memory`; `ARMOR_ARCH_ROOT` is not required at runtime.

## Scoped Vault capability

The `armor-vault-scoped-router` stdio MCP exposes exactly:

- `route_work_product` — closed-enum deterministic path mapping;
- `save_article_package` — atomic save of exactly `article-brief.json`,
  `seo-blueprint.json`, `article.md`, and `audit-report.md`.

The save operation always resolves `work-product + website + article` through
the Router. It rejects unknown files, extra arguments, absolute or traversal
package identifiers, symlink escapes, non-file targets, and any Published
source destination. It never accepts an arbitrary destination or generic file
operation. `ARMOR_VAULT_ROOT` is supplied as runtime environment only.

## MCP runtime truth

The registry records registration, installation, configuration, profile
exposure, and health independently. Firecrawl uses Hermes native
`mcp_servers.<name>.tools.include` filtering; no replacement adapter is
required. Anysearch is registered as a remote MCP and remains disabled because
`ANYSEARCH_API_KEY` is not bound. Firecrawl is installed and read-filtered but
has the same credential blocker until `FIRECRAWL_API_KEY` is supplied.

Obscura v0.2.2 is installed from the upstream arm64 macOS release with a new
Enterprise storage directory. No personal browser profile, cookies, storage
state, or login session is imported. PaddleOCR 0.8.5 runs from a dedicated
Enterprise venv with the official local PP-OCRv6 provider and is not exposed
to Operations because raw OCR file access is not needed for the Operations
workflow.

## ToolScout boundary

ToolScout is shared agent infrastructure, not an administrator-only control
plane. Its canonical Skill is exposed through the Enterprise shared Skill
source and the Operations Profile receives only the eight ToolScout MCP tools.
Tool-memory uses the normal user-level runtime path
`~/.config/toolscout/tool-memory`; it is not Hermes Memory, ARMOR Vault
authority, or WeKnora truth. General and Operations Hermes Memory remain OFF.

The global Hermes rule invokes ToolScout only immediately before incidental
commodity code or dependency installation. It is not a task-start hook and the
full Skill rules are not copied into SOUL.

The official ToolScout universal macOS release is installed and its x86_64
slice is used through a tiny launcher because the native arm64 slice exits
with signal 9 on this host. The configured MCP path and all eight MCP tools
are healthy under the Rosetta fallback; the native-arm64 probe remains
recorded as a runtime caveat in the registry.

## Website Article acceptance

The controlled fixture acceptance sequence is:

```text
Intake → Brief → SEO/GEO Blueprint → Blueprint Gate → Draft
→ ai-writing-audit v0.3.1 → deterministic checker
→ Codex Final Editorial contract → scoped save → read-back
```

The fixture is isolated and is not published to the production website. The
Article source remains under `02-Projects/Workspaces/Website/Articles/`.
`03-Records/Published/` remains reserved for evidence or an explicitly
requested snapshot.
