# Enterprise Web Research Capability v1.0 — Stage 1

Status: `IMPLEMENTED; BLOCKED — REQUIRED INPUT: Enterprise FIRECRAWL_API_KEY`

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
`infrastructure/web-research/adapter.py` calls only Firecrawl's read APIs:
`/v2/search` and `/v2/scrape`. Firecrawl remains the upstream provider; its
MCP installation is not exposed as a raw employee tool surface.

## Normalized contract

`web_search` returns `status`, the original normalized `query`, a `results`
array, and `searched_at`. Each result includes only source fields actually
returned by Firecrawl: `title`, `url`, `snippet`, `published_at`, and `source`.

`web_fetch` returns:

```text
status: SUCCESS
url / final_url / title / markdown
metadata.description / metadata.language
retrieval.method: firecrawl
retrieval.fallback_level: 1
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

## Credential state and acceptance

The Enterprise runtime has Firecrawl MCP v3.24.0 installed, but
`FIRECRAWL_API_KEY` is not provisioned. No Legacy Hermes or personal key was
inspected or copied. Offline adapter, normalization, URL-security, redirect,
trust-marker, no-persistence, and MCP-surface tests pass.

Live Search and Fetch are therefore not claimed. The exact runtime blocker is:

```text
BLOCKED — REQUIRED INPUT: Enterprise FIRECRAWL_API_KEY
```

When the approved Enterprise secret is provisioned outside Git and the runtime
is restarted through normal operations, live acceptance consists of one
harmless Search, one stable public Fetch, and rejected loopback,
cloud-metadata, and `file://` requests. MIC is not a Stage 1 hard target.

## Explicit exclusions and later stages

Stage 1 does not implement or expose Firecrawl Interact, Agent, Crawl,
monitor mutation, raw scrape, generic browser actions, authenticated browser
sessions, binary downloads, Obscura, CloakBrowser, Scrapling, Anysearch, or
automatic persistence/publication.

Stage 2 may evaluate Firecrawl → Obscura → CloakBrowser hardened fallback.
Stage 3 may perform difficult real-world acceptance and final freeze. Neither
stage is implemented or activated here.
