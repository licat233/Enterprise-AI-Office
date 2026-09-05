# Third-Party Projects and License Boundaries

Enterprise AI Office is an integration architecture and operating framework. It does not relicense the independent upstream software used by a deployment.

The repository's own original content is licensed under the root `LICENSE` (Apache License 2.0). Each upstream project remains governed by its own license, notices, commercial terms, service terms, trademarks, and release policies.

This file is informational and should be rechecked against the exact versions used by a production deployment.

## Core upstream projects

| Project | Upstream | License / terms observed at project bootstrap | Role in Enterprise AI Office |
| --- | --- | --- | --- |
| WeKnora | `Tencent/WeKnora` | MIT for the project, with additional third-party component notices in upstream `LICENSE` | Enterprise knowledge platform |
| Hermes Agent | `NousResearch/hermes-agent` | MIT | Primary agent runtime |
| Open WebUI | `open-webui/open-webui` | Open WebUI License (custom terms) | Multi-user employee Web client |
| hermes-webui | `nesquena/hermes-webui` | MIT | Hermes administrative Web client |
| Codex | `openai/codex` | Apache License 2.0 | Specialized coding execution |
| Claude Code | Anthropic distribution / `anthropics/claude-code` project resources | Governed by Anthropic's applicable software/service terms; do not assume the Enterprise AI Office Apache-2.0 license applies | Specialized coding execution |
| Model Context Protocol | MCP ecosystem/specification and selected implementations | Depends on the specific MCP package/server used | Tool/integration protocol |

## WeKnora

At the time this project baseline was created, WeKnora's upstream `LICENSE` states that the project is licensed under MIT except for listed third-party components governed by their respective licenses.

Production adopters must retain and comply with upstream notices for the exact WeKnora release they deploy.

Upstream:

`https://github.com/Tencent/WeKnora`

## Hermes Agent

At the time this baseline was created, Hermes Agent's upstream repository contains an MIT License.

Upstream:

`https://github.com/NousResearch/hermes-agent`

## Open WebUI

Open WebUI is not covered by this repository's Apache-2.0 license.

At the time this baseline was created, Open WebUI's upstream `LICENSE` contains its own license terms and includes a branding condition. In particular, the license text states that altering/removing/replacing Open WebUI branding is prohibited except in specified circumstances, including deployments/distributions with no more than 50 end users in a rolling 30-day period, specific written permission, or an applicable enterprise license.

Companies planning to rebrand Open WebUI, especially deployments above that threshold, must review the current upstream license and obtain any permission/license required for their intended use.

This architecture does not require removing Open WebUI branding.

Upstream:

`https://github.com/open-webui/open-webui`

## hermes-webui

The `nesquena/hermes-webui` project used by the current reference architecture contains an MIT License at the time of this baseline.

Because multiple projects may use similar `hermes-webui` names, deployments must record the exact repository and commit/version in `state/DEPLOYMENT-STATE.md`.

Upstream:

`https://github.com/nesquena/hermes-webui`

## Codex

The `openai/codex` repository contains an Apache License 2.0 at the time of this baseline.

Use of hosted OpenAI services, accounts, APIs, subscriptions, or model services may also be governed by separate applicable service terms. The open-source repository license should not be interpreted as replacing service terms.

Upstream:

`https://github.com/openai/codex`

## Claude Code

Claude Code is treated by this architecture as an external specialist coding tool.

Do not assume Claude Code is licensed under this repository's Apache-2.0 terms. Review Anthropic's current applicable distribution, product, service, subscription, and usage terms before enterprise deployment.

Project resources:

`https://github.com/anthropics/claude-code`

## Model providers

LLM, embedding, reranking, VLM, speech, Web search, browser, and other providers may have their own:

- API terms;
- privacy/data-use terms;
- retention policies;
- regional availability;
- commercial restrictions;
- rate limits;
- acceptable-use policies.

A company's production deployment must evaluate the providers it actually configures.

## MCP servers and Skills

Enterprise AI Office may connect third-party MCP servers and install/use third-party Hermes Skills.

Each MCP server/Skill is an independent dependency unless explicitly authored in this repository.

Before production use:

- identify source;
- pin/version where appropriate;
- review license;
- review permissions/tool surface;
- review required credentials;
- review network/filesystem behavior;
- follow the security standard in `docs/SECURITY.md`.

## No implied trademark rights

The Enterprise AI Office license does not grant trademark rights to WeKnora, Tencent, Hermes, Nous Research, Open WebUI, OpenAI, Codex, Anthropic, Claude, or other third-party names/marks.

Names are used for descriptive interoperability/reference purposes.

## Maintenance rule

Before a release or major architecture update, recheck licenses/terms for the exact upstream versions used by the reference implementation.

If an upstream license materially changes, update this file and assess whether the reference architecture or distribution instructions must change.
