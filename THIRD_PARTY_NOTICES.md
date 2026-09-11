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

## Reference capability dependencies

The current ARMOR reference implementation also uses or validates the following
upstream projects for optional capabilities. Their presence in this table does
not make them mandatory for every Enterprise AI Office deployment.

| Project | Upstream | License / terms observed | EAO role / boundary |
| --- | --- | --- | --- |
| ToolScout v1.0.0 | `licat233/toolscout` | MIT | Shared Agent tool-selection/runtime infrastructure; enabled only where the active capability contract allows it |
| Obscura v0.2.2 | `h4ckf0r0day/obscura` | Apache License 2.0 | Internal bounded Web Research fallback; not an employee generic browser |
| Firecrawl MCP | `firecrawl/firecrawl-mcp-server` | MIT for the MCP server repository; Firecrawl hosted API use is also subject to Firecrawl service terms | Internal Web Research acquisition backend; raw/action-capable tools are not exposed to ordinary Operations users |
| CloakBrowser | `CloakHQ/CloakBrowser` | MIT for the public repository/wrapper observed during review; signed browser binaries, license keys, hosted/commercial features, or product terms may impose additional conditions | Internal hardened Web Research fallback only |
| PaddleOCR | `PaddlePaddle/PaddleOCR` | Apache License 2.0 for the project repository; model assets and third-party dependencies must be checked for the selected deployment | Optional local OCR runtime; not required for ordinary non-OCR workflows |
| OpenAI Whisper | `openai/whisper` | MIT for the project repository | Local media transcription engine for English and other selected non-Chinese languages |
| SenseVoice source | `QwenAudio/SenseVoice` | MIT for source code in the repository | Source/reference implementation for the SenseVoice family used by the local media-transcription path |
| SenseVoiceSmall model | `iic/SenseVoiceSmall` | Model weights are distributed separately; apply the license/terms shown by the exact model card/artifact selected at deployment time | Local ASR model for the validated Chinese/Cantonese-oriented transcription path |
| FFmpeg | `FFmpeg/FFmpeg` | FFmpeg licensing depends on the exact build/configuration; upstream includes LGPL-licensed code and may include GPL components when built with corresponding options | Local media inspection/audio extraction for transcription |

### SenseVoice source / model license boundary

Do not treat the SenseVoice source-code MIT license as the license for every
SenseVoiceSmall model artifact.

The current upstream source identity is `QwenAudio/SenseVoice`, whose
repository license is MIT. The EAO runtime model identifier is
`iic/SenseVoiceSmall`. Model weights are separate distribution artifacts and
must follow the terms on the exact selected model card/release.

Before commercial redistribution, packaging, or mirroring of weights, record
the actual model artifact/version and its applicable model terms. A source-code
license alone is not sufficient evidence for weight redistribution rights.

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
