# Deployment Practices — Lessons from Real Installations

This document captures practical lessons discovered while installing Enterprise AI Office on real hosts.

It is intentionally small and operational. It does not replace `AGENTS.md`, `DEPLOY.md`, company configuration, version-specific upstream documentation, or acceptance contracts. When a practice conflicts with a normative contract, the normative contract wins.

The purpose is to prevent future operators and AI engineering agents from repeating avoidable investigation and installation mistakes.

## 1. Separate the operator machine from the deployment host

A deployment agent may run on an operator workstation while executing commands on the target host through SSH.

Do not assume that Codex, ChatGPT, browser sessions, or local credentials on the deployment host are the same as those on the operator machine.

A valid topology is:

```text
Operator Mac
→ Codex / engineering agent
→ SSH
→ target Mac Studio
→ Enterprise AI Office runtime
```

Every installation command should have an explicit execution boundary: operator-local or target-remote.

This prevents accidental package installation, credential lookup, or filesystem mutation on the wrong machine.

## 2. Keep administrative Web UIs loopback-only and use SSH tunnels

For a single-host/private deployment, WeKnora and Open WebUI administrative/bootstrap surfaces do not need to be exposed to the LAN or Internet merely so an operator can initialize them.

A simple pattern is:

```text
target service: 127.0.0.1:<port>
        ↓
SSH local port forwarding
        ↓
operator browser: 127.0.0.1:<port>
```

Example:

```sh
ssh -N \
  -L 3000:127.0.0.1:3000 \
  -L 8088:127.0.0.1:8088 \
  armor@<target-host>
```

The SSH tunnel exists on the operator machine. A deployment agent running on the remote host should not use the existence of the operator's local `127.0.0.1` tunnel as proof of application state.

Verify bootstrap/provisioning state from the application/API/runtime itself.

## 3. Human bootstrap is different from automated provisioning

Some fresh installations have a legitimate one-time human bootstrap boundary, such as creating the first Open WebUI administrator or WeKnora Owner/Admin account through the supported UI.

After that first authority exists, routine provisioning should use supported server-side/admin APIs where practical rather than repeatedly requiring a live browser session.

Do not disable signup or lock down access before confirming that the first administrator has actually been persisted.

## 4. Persist application secrets before relying on session continuity

Container recreation can invalidate browser sessions when an application secret is generated ephemerally.

For Open WebUI, establish the supported persistent application/WebUI secret before treating browser sessions as durable across controlled restarts/recreates.

A lost session cookie is not evidence that the administrator account or persistent application data was lost. Verify the persistent volume/application state before attempting another bootstrap.

## 5. Keep protected credentials out of Git and normal chat

Use native provider/application UIs or protected runtime input paths for real passwords, API keys, OAuth tokens, and Profile credentials.

Do not place real secret values in:

- public Git repositories;
- `company.yaml` / public company config;
- deployment reports;
- ordinary logs;
- chat transcripts;
- copied command examples.

Temporary secret bridges used during provisioning should be removed after the supported runtime has consumed the credential.

## 6. Model version selection and model identity are separate decisions

Pinning a component version does not require preserving every model choice from an earlier reference demo.

For example:

```text
Hermes version pin
≠ permanent Hermes model choice

WeKnora version pin
≠ permanent embedding provider/model choice
```

The first synthetic reference deployment is evidence that a combination worked. It is not a requirement to reuse that exact provider/model combination for every company deployment.

Record the actual selected model/provider in deployment state.

## 7. Embedding can be remote or local

WeKnora embedding does not have to use a cloud embedding API.

Two practical deployment patterns are supported:

```text
Remote
WeKnora → cloud embedding API

Local
WeKnora → Ollama on the deployment host
```

### Remote API

Good when:

- local compute/memory should be minimized;
- external API use is acceptable;
- recurring API cost is acceptable;
- provider/network dependency is acceptable.

The first synthetic reference deployment used DashScope `qwen3.7-text-embedding` at dimension `1024`. The `3.7` in that model ID is not a `3.7B` local parameter-size recommendation.

### Local embedding

Good when:

- the host has spare compute/memory;
- recurring embedding API cost should be avoided;
- keeping embedding traffic local is desirable;
- fewer external provider credentials/dependencies are preferred.

WeKnora v0.8.0 includes a native local Ollama embedding path, so local embedding does not require adding GPUStack, vLLM, TEI, or another inference platform just to produce vectors.

A useful mixed architecture is:

```text
Hermes reasoning/chat
→ selected remote reasoning model

WeKnora embedding
→ local Ollama embedding model
```

Local embedding does not mean the whole Enterprise AI Office must run a local LLM.

## 8. Validated local embedding starting point

For a multilingual Chinese/English enterprise knowledge base on a capable Apple Silicon host, start with a small mature embedding model before considering 4B/8B-class models.

The first real Mac Studio deployment validated:

```text
Ollama 0.30.8
+ bge-m3
+ 1024-dimensional embeddings
+ WeKnora v0.8.0 native local Ollama path
```

Small qualification evidence from 2026-09-08:

- six sanitized representative documents parsed successfully;
- eight mixed Chinese / English / cross-language retrieval questions all returned relevant source evidence;
- Ollama RSS was observed at approximately 1.75 GB;
- available-memory ratio remained approximately 68–71% on the target host;
- WeKnora and Open WebUI remained healthy with HTTP 200 checks;
- no obvious system slowdown was observed.

Therefore `bge-m3` is the **validated local choice for this Mac Studio deployment** and the preferred starting choice for similar capable Apple Silicon hosts.

Keep `qwen3-embedding:0.6b` as a lighter fallback candidate if a future host has tighter resource constraints or `bge-m3` shows a real deployment-specific problem.

Do not default to 4B/8B-class embedding models merely because the host can run them.

This validation is not a universal performance guarantee. Re-check resource use and retrieval quality when the host class, corpus/languages, WeKnora version, Ollama version, or model changes materially.

## 9. Do a smoke test, not a benchmark project, by default

Embedding qualification should stay proportional to the decision.

A normal deployment usually needs only:

1. roughly 5–10 representative non-sensitive documents;
2. roughly 5–10 representative employee questions;
3. at least one required cross-language query where applicable;
4. confirmation that the expected source is retrieved;
5. a quick check of host responsiveness and Memory Pressure.

If the first candidate works well enough, use it.

Only compare another model or build a deeper benchmark when there is an observed retrieval-quality or resource problem.

The first real Mac Studio deployment followed this rule and stopped after `bge-m3` passed; it did not run an unnecessary A/B benchmark against `qwen3-embedding:0.6b`.

## 10. WeKnora v0.8.0 local Ollama truncation detail

In WeKnora v0.8.0, the local Ollama embedding implementation treats `truncate_prompt_tokens = 0` as a fallback to approximately `511` tokens rather than unlimited input.

Therefore do not infer "unlimited" from a zero value in the UI/config.

Keep ordinary RAG chunks within a safe range or configure/test an explicit value when longer chunks are required.

Re-check this behavior after WeKnora upgrades because it is version-specific.

## 11. Decide embedding before large-scale production ingestion

Embedding model and vector dimension become part of the indexed knowledge representation.

Choose and validate them before ingesting a large production corpus whenever possible.

Changing either later can require re-embedding/reindexing the affected Knowledge Base.

Do not keep switching embedding models casually after production indexing starts.

## 12. Prefer minimal local infrastructure

A capable Mac Studio can run more components than the Enterprise AI Office actually needs.

Do not turn available compute into a reason to install:

- a large local chat LLM;
- a multi-model serving platform;
- a second vector database;
- a large observability stack;
- a workflow engine;
- another scheduler.

Add infrastructure only after a real requirement demonstrates that the current upstream-native path is insufficient.

The deployment objective is a reliable enterprise AI office, not maximum utilization of the host.
