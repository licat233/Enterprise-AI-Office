# ARMOR Phase 4A — Article and MCP Migration

Status: repository migration contract complete; runtime activation remains
explicitly disabled.

This is Enterprise repository evidence, not a claim that the MacStudio
deployment has been installed or that a live external service is healthy.

## Article capability contract

| Concern | Phase 4A contract |
|---|---|
| Canonical entrypoint | One Enterprise Skill: armor-website-article-pipeline |
| Lifecycle | Research/Brief → SEO/GEO Blueprint → Blueprint Gate → Draft → one Codex Final Editorial Pass → Router Save |
| Ordinary save approval | No second User Approval gate; the ordinary Article request authorizes Vault save |
| Publication boundary | Vault save does not publish a website; website publication remains a separate approval |
| Editable source | 02-Projects/Workspaces/Website/Articles/ |
| Published records | 03-Records/Published/ is only publication evidence or a snapshot |
| Durable artifacts | article-brief.json, seo-blueprint.json, article.md, audit-report.md |
| Audit runtime | Enterprise-supported ai-writing-audit v0.3.1 plus the deterministic Article checker |

The duplicate nested article-pipeline-runtime files were removed. Useful
dispatch and quality-boundary behavior is represented by the one canonical
Skill and the ARMOR Vault standards; no physical runtime fork is retained.

During the Phase 4A probe, the authoritative local ai-writing-audit interface
was v0.3.1. The target Enterprise Hermes runtime did not have that Skill
installed, so the Article capability is PREPARED rather than HEALTHY. A
runtime that cannot resolve v0.3.1 must stop as BLOCKED_EXECUTOR; it may not
downgrade to v0.3.0 or claim a passing audit.

## MCP migration contract

| Definition | Registry definition | Runtime | Enabled | Health |
|---|---:|---|---:|---|
| anysearch | YES | PREPARED | NO | NOT_RUN |
| firecrawl-mcp | YES | PREPARED_REPLACEMENT_REQUIRED | NO | NOT_RUN |
| obscura | YES | PREPARED | NO | NOT_RUN |
| paddle_ocr | YES | PREPARED | NO | NOT_RUN |
| toolscout | YES | PREPARED | NO | NOT_RUN |

The exact classifications are OPERATIONS_READ, OPERATIONS_EXTERNAL_WRITE,
MACHINE_SPECIFIC_REBIND, MACHINE_SPECIFIC_REBIND, and ADMIN_CONTROL_PLANE in
the same order. Employee-facing exposure is disabled. Operations remains
allowlisted to WeKnora only.

## Safety and scope

No secret values, cookies, browser sessions, personal Chrome state, or
personal runtime paths were copied. Legacy Memory migration was not performed.
No website publication, browser action, external write, or live MCP probe was
performed. The five definitions are migrated into the Enterprise control-plane
inventory, while their runtime binding and health acceptance remain open.

Validation commands:

~~~text
python3 scripts/phase4a_migration_check.py
python3 -m unittest discover -s skills/shared/department/armor-website-article-pipeline/scripts -p 'test_*.py' -v
scripts/repository-readiness-check.sh
git diff --check
~~~
