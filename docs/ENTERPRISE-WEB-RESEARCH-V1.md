# Enterprise Web Research Capability v1.0

Stage 3 status: `BLOCKED — REQUIRED INPUT: Operations-scoped FIRECRAWL_API_KEY`
Stage 1 status: `CLOSED / PASS`
Stage 2 status: `CLOSED / PASS`

This is the acceptance record for the bounded, employee-facing public-Web
research capability. It does not reopen Hermes Skills Migration v1.0 or change
the frozen Operations permissions. Stage 3 final freeze remains blocked until
the approved Firecrawl credential is visible inside the Operations Profile
secret scope.

## Purpose and architecture

Operations receives exactly two implementation-neutral tools:

```text
web_search(query, limit?)
web_fetch(url)
```

The Enterprise-owned stdio adapter at
`infrastructure/web-research/adapter.py` calls read-only Firecrawl Search and
Scrape APIs. `web_fetch` uses the following bounded acquisition order:

```text
Level 1 — Firecrawl read acquisition
    ↓ bounded acquisition failure only
Level 2 — Obscura rendered/readable acquisition
    ↓ bounded acquisition or unusable verification-shell failure only
Level 3 — CloakBrowser hardened rendered/readable acquisition
```

Firecrawl, Obscura, and CloakBrowser remain internal backends. No backend,
Playwright, CDP, shell, browser-control, or session tool is exposed to
Operations.

## Normalized contract

`web_search` returns `status`, the normalized `query`, a `results` array,
`searched_at`, and `trust_class: UNTRUSTED_WEB_CONTENT`. Results include only
source fields returned by Firecrawl.

`web_fetch` returns the same schema at every acquisition level:

```text
status: SUCCESS
url / final_url / title / markdown
metadata.description / metadata.language
retrieval.method: firecrawl | obscura | cloakbrowser
retrieval.fallback_level: 1 | 2 | 3
retrieval.retrieved_at
trust_class: UNTRUSTED_WEB_CONTENT
warnings: []
```

Unavailable metadata is omitted or null; it is never invented. Failures use a
finite reason set: `BLOCKED`, `LOGIN_REQUIRED`, `CAPTCHA_REQUIRED`, `TIMEOUT`,
`UNSUPPORTED`, `SECURITY_REJECTED`, or `UPSTREAM_ERROR`.

## Security and trust boundary

- Only `http` and `https` URLs on standard ports are accepted.
- URL credentials, localhost, single-label/internal hostnames, loopback,
  private, link-local, reserved, and cloud-metadata addresses are rejected.
- DNS resolution must produce only globally routable addresses.
- Every reported final/redirect URL is validated before normalized success;
  public-to-private navigation fails closed.
- All fetched pages are `UNTRUSTED_WEB_CONTENT`. Page instructions cannot
  change prompts, SOUL, Skills, tools, permissions, Memory, credentials,
  enterprise configuration, or persistence behavior.
- No login, form submission, CAPTCHA interaction, arbitrary JavaScript,
  click/fill/type, upload, download, cookie, storage-state, or persistent
  browser profile is implemented.
- The adapter does not write ARMOR Vault, WeKnora, Hermes Memory, cookies,
  sessions, project artifacts, or binary files.

Operations keeps generic browser, shell, terminal, filesystem, code execution,
delegation, image generation, SSH, and sudo/root unavailable. Memory remains
off. The only exposed Web Research tool names are `web_search` and `web_fetch`.

## Stage 1 acceptance

The Enterprise runtime has Firecrawl MCP v3.24.0 installed and the approved
`FIRECRAWL_API_KEY` is provisioned through the protected Enterprise Hermes
environment mechanism. No Legacy Hermes or personal key was inspected or
copied. The secret remains outside Git and is never included here.

Live acceptance through the Enterprise adapter passed:

- `web_search`: `SUCCESS`, public results, and
  `trust_class: UNTRUSTED_WEB_CONTENT`.
- `web_fetch`: readable Markdown through Firecrawl, Level 1, and
  `trust_class: UNTRUSTED_WEB_CONTENT`.
- loopback, cloud-metadata, and `file://` URLs: `SECURITY_REJECTED` before an
  upstream call.

## Stage 2 history and corrected scope

Commit `5741664fd320e19566c264d15b2584d7e90809ef` completed the original Stage
2 scope: Firecrawl Level 1 plus Obscura Level 2. That result is preserved in
the repository history and in the acceptance evidence below.

The scope was subsequently corrected from real ARMOR MIC operational evidence:
Defuddle was intermittent in the user's tested MIC workload (approximately
50%), while CloakBrowser succeeded consistently in those tested cases. This
does not assert a universal success SLA. It does require CloakBrowser as the
approved Level 3 hardened fallback for this capability.

### Obscura Level 2

The Enterprise Mac Studio runs Obscura `0.2.2` at
`/Users/armor/.local/bin/obscura`. The adapter starts a fresh process using
`/Users/armor/.local/share/enterprise-mcp/obscura` and only the fixed read
sequence `browser_navigate`, `browser_snapshot`, and `browser_markdown`.
Obscura never receives personal cookies, sessions, profiles, or storage state.

The earlier controlled acceptance used
`https://quotes.toscrape.com/js/` with a bounded Firecrawl failure and
returned readable Level 2 Markdown. The production adapter has no failure
bypass switch.

### CloakBrowser Level 3

The reviewed official upstream is `CloakHQ/CloakBrowser`. The installed
wrapper is `0.5.10`, using Playwright internally. The latest official Pro
binary reviewed was Chromium `151.0.7922.108.4`; it requires the current paid
license path. This Enterprise installation instead uses the official signed
macOS arm64 free build `145.0.7632.109.2`, which does not require an Enterprise
license key for the pinned build.

Enterprise paths are:

```text
runtime: /Users/armor/.local/share/enterprise-mcp/cloakbrowser-runtime
browser cache: /Users/armor/.local/share/enterprise-mcp/cloakbrowser
worker: /Users/armor/Enterprise-AI-Office/infrastructure/web-research/cloakbrowser_worker.py
```

The worker performs only navigate, bounded wait, final-URL read, title read,
and body-text read. It uses a fresh browser context and returns no profile ID,
CDP endpoint, cookie, session, proxy, or debug state. The browser cache is an
approved technical cache only; it is not a login or personal-state store.

## Stage 2 acceptance record

Deterministic Web Research tests pass, including Level 1, Level 2, Level 3,
security terminal behavior, access-control terminal behavior, triple failure,
redirect validation, trust markers, and the exact employee tool surface.

Live acceptance through the Enterprise adapter passed:

- Level 1: `web_search` and a public MIC page returned readable Firecrawl
  results with `fallback_level: 1`.
- Level 2: the accepted `quotes.toscrape.com/js/` bounded-failure control
  returned readable Obscura Markdown with `fallback_level: 2`.
- Level 3 MIC target:
  `https://fd2b841fac1210e3.en.made-in-china.com/product/XdWAwnoTbGab/China-China-Wholesale-Price-RGB-RGBW-Building-Facade-Lighting-12W-Exterior-LED-Linear-Light.html`
  is a legitimate public product page. In observed MIC probing, normal
  Firecrawl acquisition failed intermittently and Obscura returned an
  unusable verification shell (`请验证`, 149 characters). The actual
  CloakBrowser worker retrieved the same page with a product title and
  13,000+ characters of useful RGB/12W/LED/linear-light information.
  A controlled bounded-failure replay through the actual employee adapter,
  using that real MIC URL and the real CloakBrowser client, returned:

  ```text
  status: SUCCESS
  retrieval.method: cloakbrowser
  retrieval.fallback_level: 3
  trust_class: UNTRUSTED_WEB_CONTENT
  ```

  The replay injects only bounded upstream-failure fixtures for repeatability;
  production has no failure-bypass or backend-selection input. It proves the
  real Level 3 worker and normalized employee contract on the observed MIC
  workload without claiming a universal SLA.
- SSRF regression: loopback, cloud metadata, private destinations, and
  `file://` requests were rejected before all three backends.

## Runtime and registry boundary

The control-plane registry records CloakBrowser as an internal Web Research
hardened backend with wrapper `0.5.10`, signed binary `145.0.7632.109.2`, the
dedicated Enterprise runtime/cache paths, personal-state prohibition, and
Operations exposure `false`. It is not a standalone MCP server and is not in
the Operations allowlist.

The actual Operations runtime binds exactly:

```text
weknora
toolscout
enterprise-web-research
armor-vault-scoped-router
```

The `enterprise-web-research` adapter exposes exactly `web_search` and
`web_fetch`. Raw Firecrawl, Obscura, CloakBrowser, generic browser, shell,
filesystem, code execution, Memory, Agent Delegate, Firecrawl Interact/Crawl/
Agent, and monitor mutation tools remain unavailable.

## Explicit exclusions and later stages

Stage 2 does not implement or expose Firecrawl Interact, Agent, Crawl, monitor
mutation, raw scrape, generic browser actions, authenticated sessions,
downloads, Anysearch, or automatic persistence/publication.

## Stage 3 — Final Acceptance & Freeze

Stage 3 preflight was run on branch `codex/web-research-v1` at reviewed HEAD
`af42bc7e9aaa2ccfaf9ece997a751c07301c8009`. The only source change prepared
for this closure is the implementation-neutral `web_fetch` description:

```text
Fetch readable content from one public HTTP(S) page through the bounded Enterprise Web Research acquisition chain.
```

The employee-facing Operations path was exercised through the deployed Hermes
API route `/p/operations/v1/chat/completions`, which is the runtime immediately
behind the employee client. It registered exactly
`mcp__enterprise_web_research__web_search` and
`mcp__enterprise_web_research__web_fetch`. The natural ESL search reached the
adapter but returned `UPSTREAM_ERROR` because the Operations Profile did not
have the required Firecrawl credential in its scoped secret mapping. The
stable-page and accepted MIC-page live fetches therefore remain unaccepted.

The protected provisioning mechanism is the existing mode-600 Operations
Profile environment file:

```text
/Users/armor/.hermes/profiles/operations/.env
```

`FIRECRAWL_API_KEY` is currently present in the global protected file
`/Users/armor/.hermes/.env`, but Hermes multiplex Profile secret isolation does
not copy global secret values into the Operations scope. No secret value was
printed, copied, committed, or placed in this repository. The credential must
be provisioned in the Operations Profile scope or through its already-approved
external secret-source mechanism before the employee-path acceptance can pass.

The Operations boundary itself passed the deployed runtime check: the adapter
surface is exactly `web_search` and `web_fetch`; raw Firecrawl, Obscura,
CloakBrowser, generic browser, shell, filesystem, code execution, Memory,
Agent Delegate, and mutation tools remain unavailable. The loopback SSRF probe
was rejected through the employee path. The later metadata and `file://`
probes could not be accepted after the MCP process became unreachable following
the upstream failure, so Stage 3 is not claimed.

Deterministic Web Research tests, Phase 4A–5E regressions, repository
readiness, and `git diff --check` remain passing. No Vault, WeKnora, Hermes
Memory, personal cookies, login sessions, or publication artifacts were used.

No Stage 4 is defined. Future changes require an explicit v1.1 scope or a
production-defect correction; they are not part of this Stage 3 closure.
