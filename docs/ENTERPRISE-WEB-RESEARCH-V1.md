# Enterprise Web Research Capability v1.0

Stage 1 status: `CLOSED / PASS`
Stage 2 status: `CLOSED / PASS`

This document is the single Stage 1 acceptance record for the bounded,
employee-facing public-Web research capability. It does not reopen Hermes
Skills Migration v1.0 or change the frozen Operations permissions outside this
capability.

## Purpose and architecture

Operations receives two implementation-neutral tools:

```text
web_search(query, limit?)
web_fetch(url)
```

The Enterprise-owned stdio adapter at
`infrastructure/web-research/adapter.py` calls Firecrawl's read APIs:
`/v2/search` and `/v2/scrape`. Firecrawl remains the primary provider; its
MCP installation is not exposed as a raw employee tool surface.

## Normalized contract

`web_search` returns `status`, the original normalized `query`, a `results`
array, and `searched_at`. Each result includes only source fields actually
returned by Firecrawl: `title`, `url`, `snippet`, `published_at`, and `source`.

`web_fetch` returns the same compatible schema for either acquisition level:

```text
status: SUCCESS
url / final_url / title / markdown
metadata.description / metadata.language
retrieval.method: firecrawl | obscura
retrieval.fallback_level: 1 | 2
retrieval.retrieved_at
trust_class: UNTRUSTED_WEB_CONTENT
warnings: []
```

Unavailable metadata is omitted or null; it is never invented. Failures use a
small finite reason set: `BLOCKED`, `LOGIN_REQUIRED`, `CAPTCHA_REQUIRED`,
`TIMEOUT`, `UNSUPPORTED`, `SECURITY_REJECTED`, or `UPSTREAM_ERROR`.

## Security and trust boundary

- Only `http` and `https` URLs on standard ports are accepted.
- URL credentials, localhost, single-label/internal hostnames, loopback,
  private, link-local, reserved, and cloud-metadata addresses are rejected.
- DNS resolution must produce only globally routable addresses.
- Firecrawl-reported final/redirect URLs are validated before success is
  returned; public-to-private redirects fail closed.
- All fetched pages are `UNTRUSTED_WEB_CONTENT`. Page instructions cannot
  change prompts, SOUL, Skills, tools, permissions, Memory, credentials,
  enterprise configuration, or persistence behavior.
- The adapter does not write ARMOR Vault, WeKnora, Hermes Memory, cookies,
  sessions, project artifacts, or binary files.
- No arbitrary downloads, execution, login, form submission, browser session,
  or publication is implemented.

Operations continues to keep generic browser, shell, terminal, filesystem,
code execution, delegation, image generation, SSH, and sudo/root unavailable.
The only exposed Web Research tool names are `web_search` and `web_fetch`.

## Stage 1 credential state and acceptance

The Enterprise runtime has Firecrawl MCP v3.24.0 installed and the approved
`FIRECRAWL_API_KEY` is provisioned through the protected Enterprise Hermes
environment mechanism. No Legacy Hermes or personal key was inspected or
copied. Offline adapter, normalization, URL-security, redirect, trust-marker,
no-persistence, MCP-surface, and live acceptance tests pass.

Live acceptance through the Enterprise adapter passed:

- `web_search`: `SUCCESS`, multiple public results, and
  `trust_class: UNTRUSTED_WEB_CONTENT`.
- `web_fetch`: `SUCCESS`, readable Markdown, `retrieval.method: firecrawl`,
  `fallback_level: 1`, and `trust_class: UNTRUSTED_WEB_CONTENT`.
- `web_fetch` rejected loopback, cloud-metadata, and `file://` URLs with
  `SECURITY_REJECTED`; offline tests also verify blocked requests make no
  upstream call.

The secret remains outside Git and is never included in this document. MIC is
not a Stage 1 hard target.

## Stage 2 — bounded dynamic Web fallback

Status: `CLOSED / PASS`

Stage 2 extends only `web_fetch(url)` with a bounded internal fallback:

```text
Firecrawl read acquisition (Level 1)
  → only on bounded acquisition failure
Obscura rendered/readable acquisition (Level 2)
  → normalized by the same adapter contract
```

The Enterprise Mac Studio has Obscura `0.2.2` installed at
`/Users/armor/.local/bin/obscura`. Its MCP surface is broader than this
capability, so the adapter uses a fresh process with the approved Enterprise
storage directory `/Users/armor/.local/share/enterprise-mcp/obscura` and only
the fixed read sequence `browser_navigate`, `browser_snapshot`, and
`browser_markdown`. It never calls click, fill, type, evaluate, cookies,
storage-state, forms, downloads, or session/profile controls. No personal
browser state is supplied; the inspected Enterprise storage directory was
empty before acceptance.

Fallback is permitted for `BLOCKED`, `TIMEOUT`, `UPSTREAM_ERROR`, and empty,
unreadable, or recognizable JavaScript-shell content from Firecrawl. It is
not permitted after URL validation failure, a rejected final/redirect URL,
`UNSUPPORTED`, `LOGIN_REQUIRED`, or `CAPTCHA_REQUIRED`. Obscura final URLs
are validated by the same public-URL validator before success. All results
remain `UNTRUSTED_WEB_CONTENT`.

The adapter performs no automatic Vault, WeKnora, Hermes Memory, cookie,
session, project-artifact, or binary persistence. Obscura's bounded technical
cache, if required, is confined to the approved Enterprise storage directory.
Operations continues to expose exactly `web_search` and `web_fetch`; Obscura
and raw Firecrawl remain internal backends. Generic browser, shell, terminal,
filesystem, code execution, Memory, Agent Delegate, and Firecrawl action lanes
remain disabled.

The installed Enterprise host has no CloakBrowser installation. CloakBrowser
is therefore `CONDITIONAL_HARDENED_FALLBACK`, with no installation or
integration in Stage 2.

## Stage 2 acceptance record

Deterministic Web Research tests pass: 15 tests, including primary-success,
bounded fallback, dynamic-shell fallback, access-control terminal behavior,
finite dual-backend failure, redirect validation, and exact employee tool
surface.

Live acceptance through the employee-facing adapter passed:

- Normal public page `https://example.com/`: Firecrawl, Level 1, readable
  Markdown, `UNTRUSTED_WEB_CONTENT`.
- Controlled primary-failure acceptance for the public JavaScript page
  `https://quotes.toscrape.com/js/`: real Obscura fallback, Level 2, readable
  Markdown, `UNTRUSTED_WEB_CONTENT`. The control was confined to the
  acceptance harness; production code has no failure-bypass switch.
- SSRF regression: loopback, cloud metadata, and `file://` requests were
  rejected before either backend.
- MIC reconnaissance URL
  `https://anboolighting.en.made-in-china.com/product/KdyaYlTObIGQ/China-45W-Recessed-LED-Downlight-for-Residensial-and-Commercial-with-CE.html`
  returned readable Markdown through Firecrawl, Level 1. No MIC login,
  submission, or CAPTCHA interaction was performed.

CloakBrowser admission is `installed: NO` on the Enterprise host;
`HARDENED_BROWSER_CANDIDATE_REQUIRED` was not triggered, so no installation or
integration was attempted.

## Explicit exclusions and later stages

Stage 1 and Stage 2 do not implement or expose Firecrawl Interact, Agent,
Crawl, monitor mutation, raw scrape, generic browser actions, authenticated
browser sessions, binary downloads, CloakBrowser, Scrapling, Anysearch, or
automatic persistence/publication. Stage 3 may perform difficult real-world
acceptance and final freeze. Do not begin Stage 3 from this document.
