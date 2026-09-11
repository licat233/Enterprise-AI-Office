# ARMOR Phase 4B — Website Article Runtime Closure

Status: partial runtime closure complete; Article Router Save remains fail-closed
behind a missing scoped executor.

This record distinguishes repository and runtime evidence. It does not claim
that a blocked Article capability is HEALTHY, and it does not authorize website
publication, Social Media migration, or unrelated MCP activation.

## Article Runtime

| Concern | Phase 4B result |
|---|---|
| Canonical Skill installed/exposed | `armor-website-article-pipeline` is the only Article entrypoint and is exposed through the existing Operations symlink model |
| `ai-writing-audit` v0.3.1 | Canonical Enterprise copy; standard-library-only CLI; local and Mac Studio tests plus CLI smoke pass |
| Deterministic Article checker | Existing `article-draft-check.py` remains canonical; its tests pass; Phase 4B runtime checker added |
| `ARMOR_VAULT_ROOT` | Protected Enterprise binding resolves to the current Vault; no Skill path hardcodes the physical Vault path |
| Vault standards readable | Required Article stage standards/templates are present under the bound Vault |
| Router target | `02-Projects/Workspaces/Website/Articles/` resolves; `03-Records/Published/` remains evidence-only |
| Router functional | **BLOCKED** — `SCOPED_ROUTER_WRITE_BLOCKED` |
| Operations exposure | Article and audit are exposed as canonical symlinks; Memory remains OFF; terminal/file/browser/code execution remain disabled |
| Article state | `PREPARED` / `BLOCKED_SCOPED_ROUTER_WRITE`, not `RUNTIME_READY` or `HEALTHY` |

The exact missing capability is a callable, scoped Vault-write executor for the
Article package. Operations currently has only the `skills` tool and read-only
WeKnora; Hermes Skill loading does not execute linked scripts. In addition,
`armor-memory/scripts/route.sh` cannot resolve its delegated
`minimal-stable/scripts/armor-route.py` because no usable `ARMOR_ARCH_ROOT` or
local Router implementation is available on the target.

The smallest safe solution is one approved, deterministic Article Router tool
that accepts only the four Article artifacts and writes only beneath the
Router-returned `02-Projects/Workspaces/Website/Articles/` destination, with
path-traversal, Published-path, and arbitrary-file rejection. It must be bound
as a narrow tool; generic shell, terminal, file, SSH, sudo, or browser access
must remain disabled. Until that boundary exists, the Article workflow must
stop before Save.

## Anysearch

Hermes supports `mcp_servers.<name>.tools.include` tool-level allowlisting.
The safe prepared lane is `search`, `extract`, and `batch_search`; browser,
external-write, and account-mutation lanes are not allowed. Anysearch is not
enabled in Operations because the protected `ANYSEARCH_API_KEY` binding is
missing. Health was not probed and is not claimed.

## MCP Regression

| MCP | Classification | Runtime state | Operations exposure |
|---|---|---|---|
| `anysearch` | `OPERATIONS_READ` | `PREPARED` / `BLOCKED_CREDENTIAL` | disabled |
| `firecrawl-mcp` | `OPERATIONS_EXTERNAL_WRITE` | `PREPARED_REPLACEMENT_REQUIRED` | disabled |
| `obscura` | `MACHINE_SPECIFIC_REBIND` | `PREPARED` | disabled |
| `paddle_ocr` | `MACHINE_SPECIFIC_REBIND` | `PREPARED` | disabled |
| `toolscout` | `ADMIN_CONTROL_PLANE` | `PREPARED` | admin/control-plane only |

## Security invariants

Legacy Memory migration: NOT PERFORMED. Automatic website publishing, Social
Media publishing, generic browser write, generic shell, credential values,
personal cookies/sessions, sudo/root, and SSH were not added.

## Validation

The repository checks remain the Phase 4A checks plus the Phase 4B checker and
its unit tests. The Mac Studio acceptance run exercised Skill discovery,
v0.3.1 CLI execution, Vault binding and stage-file resolution, Article target
resolution, Operations permission checks, and Hermes MCP include-filter source
verification. The end-to-end Article run stopped at Router Save as required by
the security boundary; no production Article or publication evidence was
written.
