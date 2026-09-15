# EAO Qwen3 Retrieval Candidate — Phase 1 Evidence

Last updated: 2026-09-15

## Decision

**Candidate status: NOT READY for production migration review.** The candidate services are installed, registered in WeKnora, and pass the checks recorded here. Retrieval quality has not been compared against the production baseline because the deployed WeKnora Evaluation path cannot consume the prepared EAO seed or select an embedding model per run. Production remains on BGE-M3. No production knowledge-base binding or index was changed.

## Production and candidate roles

| Role | Current production | Candidate / evaluation |
| --- | --- | --- |
| Embedding | `bge-m3:latest`, 1024 dimensions; existing production KBs remain bound to it | Ollama `qwen3-embedding:0.6b`, 1024 dimensions; registered in WeKnora, not made default or bound to a production KB |
| Reranking | Disabled in the production retrieval path | `Qwen3-Reranker-0.6B` served by `llama-server`; registered in WeKnora, not bound to a production KB or agent |

The matching 1024 dimensions do not make BGE-M3 and Qwen3 vectors interchangeable. A Qwen query vector must never be compared with BGE-M3 document vectors. Any future comparison must use isolated indexes or test KBs and must preserve the current production index for rollback.

## Candidate serving and connectivity

Ollama 0.34.0 already had `qwen3-embedding:0.6b`; it was reused without downloading it again. WeKnora's model manager registered it as an Ollama embedding candidate at `http://host.docker.internal:11434` and detected dimension 1024. The model connectivity/dimension check and embedding request passed.

The reranker uses the existing `/opt/homebrew/bin/llama-server` installation (llama.cpp 0.4.1, build 10964) with the `ggml-org/Qwen3-reranker-0.6B-Q8_0-GGUF:Q8_0` model and these bounded settings:

```text
host: 127.0.0.1
port: 18181
context: 4096
parallel slots: 1
Web UI: disabled
```

The candidate is registered in WeKnora through its compatible remote/OpenAI-style rerank provider at `http://host.docker.internal:18181/v1`. WeKnora's model connectivity test passed. A direct multi-document `/v1/rerank` request ranked the matching ARMOR fact first and returned the expected `index` / `relevance_score` result shape. These checks do not constitute a full WeKnora retrieval query through a candidate KB.

WeKnora-app reached `http://host.docker.internal:18181/health` both before and after service persistence was configured. The reranker listens on host loopback; the Docker host name is the stable bridge address used by the application. Container IP addresses are dynamic and are not used. The existing `host.docker.internal` SSRF allowlist entry was reused without broadening network access.

## Persistence and rollback

The reranker runs as the user LaunchAgent `com.eao.qwen3-reranker`, following the Mac host's existing user-level LaunchAgent convention. `RunAtLoad` starts it when the user session loads, including after reboot and login; `KeepAlive` restarts an exited process. Logs are written beneath the private EAO runtime directory. The service binds to loopback only.

Recovery was tested by sending `SIGKILL` to the service. `launchd` started a new process (run count advanced to 2), `/health` returned `{"status":"ok"}`, and WeKnora-app reached the host-bridge health endpoint again. This validates restart after user-session startup; it does not claim the user LaunchAgent is available before login.

Rollback is bounded: unload the candidate LaunchAgent, stop the Qwen embedding model if it is loaded, and remove the two candidate model registrations through WeKnora's model manager if desired. Keep BGE-M3 installed and retain all existing production KB bindings and indexes. No production migration or rollback of production data has occurred.

## Resource observations

Measurements were taken on the authorized Mac Studio while normal EAO services were present. They are host-specific observations, not general performance guarantees.

| Candidate check | Observed result |
| --- | --- |
| Qwen embedding output | 1024 dimensions |
| Qwen embedding first call | 1.84 s including cold load |
| Qwen embedding warm calls | 10 calls: P50 13.6 ms, P95 14.9 ms, maximum 16.3 ms |
| Qwen embedding runtime | About 5.8 GB reported by `ollama ps` with the direct API's default 32K context; 100% GPU offload |
| WeKnora dimension-detection request | About 820 MB with a reported 256-token context during that request |
| Memory during Qwen embedding load | Free memory moved from about 50% idle to 27%; it returned to 44–50% after unload |
| Swap observation | About 1,426 MB at the initial reading, 1,452 MB after the embedding check, and 1,672 MB after subsequent candidate checks and unload; attribution is cumulative across the session |
| Reranker startup | Health became available in about 6 seconds after launch |
| Reranker memory | RSS about 1.35 GB after the 30-document test; host free memory 47% at the final reading |

Reranker latency used five requests per candidate count with 30 realistic product-record text chunks (median input text about 330–370 characters). The first 5-document series included a cold/warm outlier, so its P95 is not a steady-state estimate.

| Candidate documents | P50 | P95 | Maximum |
| ---: | ---: | ---: | ---: |
| 5 | 190 ms | 744 ms | 744 ms |
| 10 | 360 ms | 375 ms | 375 ms |
| 20 | 761 ms | 840 ms | 840 ms |
| 30 | 1,117 ms | 1,161 ms | 1,161 ms |

No instability was observed during these bounded tests. The swap readings alone do not establish a sustained growth rate. The 5.8 GB figure is an upper-bound observation for a direct request using Ollama's default 32K context; it is not the observed footprint of WeKnora's smaller 256-token dimension-detection request.

## Native Evaluation reuse check

The deployed WeKnora source is v0.8.0, commit `1edcd54`. Its Evaluation subsystem exists, but the deployed contract is not sufficient for this EAO benchmark:

- The evaluation handler accepts dataset, KB, chat, and rerank identifiers; it does not accept an embedding model identifier.
- When a KB is supplied, Evaluation copies the embedding binding from that KB. Without one, it chooses a listed/default embedding model. It cannot make a controlled BGE-versus-Qwen embedding comparison for one run.
- The dataset service ignores the requested dataset ID and returns the bundled `DefaultDataset()` Parquet data. There is no deployed native import path for this custom EAO seed.
- Evaluation creates a temporary KB and knowledge entries and deletes them at completion; task state is in memory. Running it here would use the bundled generic sample rather than the prepared EAO questions, so no such run was started.

This differs from a previously described Evaluation contract that included `EmbeddingModelID`. The deployed v0.8.0 source was inspected directly and is the evidence used here. No WeKnora source patch or separate benchmark framework was introduced. The prerequisite for a quality comparison is a supported native Evaluation path that accepts the EAO dataset and an explicit candidate embedding binding, or a future deployed WeKnora version that supplies those capabilities.

## Benchmark preparation and method

A protected local seed contains 30 query/gold rows derived from the current ARMOR product reference, the working ESL technical view, the reviewed Product Model/SKU-derived view, and EAO knowledge-governance documents. Its schema records query, language, expected source, expected fact/behavior, category, and notes. Product-specific rows remain in private runtime evaluation storage and are not committed to the public repository.

Seed coverage is intentionally smaller than the 100-query target because the source corpus has authority and conflict limitations:

| Category | Seed rows |
| --- | ---: |
| Chinese factual retrieval | 4 |
| English factual retrieval | 4 |
| Cross-language retrieval | 4 |
| Product model / specification | 8 |
| SOP / governance | 5 |
| Long-document localization | 2 |
| Ambiguity / conflicting sources | 3 |
| **Total** | **30** |

Two current employee-safe source views are marked `working`, so their rows require source-owner confirmation before a formal golden set. The product CSV includes an internally conflicting HM-S4 record; its expected behavior is to surface the conflict and stop, not to select a voltage. Raw product rows are not treated as primary evidence where controlled datasheets or certifications are required.

When the native evaluation limitation is resolved, compare the following with identical queries, corpus snapshot, chunking, retrieval parameters, chat model, and hardware:

| Configuration | Embedding | Reranker |
| --- | --- | --- |
| A | BGE-M3 | Off |
| B | Current production settings | Current production setting |
| C | Qwen3-Embedding-0.6B | Off |
| D | Qwen3-Embedding-0.6B | Qwen3-Reranker-0.6B |

Track Recall@5, Recall@10, MRR, top-1/top-5 relevant hits, source correctness, cross-language retrieval, product/specification accuracy, authoritative-source hit rate, P50/P95 retrieval latency, error rate, and memory impact. Do not tune embedding, reranker, top-k, thresholds, query rewrite/expansion, or chunking simultaneously.

## Acceptance gate and current result

Production migration requires all of the following:

- Recall@5 or MRR improves by at least 5% relative to baseline;
- no meaningful regression in cross-language retrieval, product/model retrieval, specification accuracy, or authoritative-source hit rate;
- healthy memory pressure, no sustained swap growth or service instability, and preferably P95 retrieval latency no more than 1.5 seconds above baseline;
- no crashes, vector-dimension mismatch, mixed embedding space, malformed rerank response, or production KB mutation.

**Current gate: NOT PASSED / quality not evaluated.** Baseline-versus-candidate retrieval metrics are unavailable because the native Evaluation path cannot run this seed or select candidate embeddings. The direct service/resource checks passed, but they cannot establish the quality gate or full retrieval latency. Production stays on BGE-M3; no production re-embedding, default switch, KB rebinding, BGE deletion, index deletion, or knowledge rewrite was performed.
