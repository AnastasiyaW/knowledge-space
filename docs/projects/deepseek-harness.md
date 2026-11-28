---
title: "DeepSeek Harness: deepseek-harness-agent-teams — Deepseek Harness Agent Teams"
category: "projects"
date: 2026-11-27
tags: ["deepseek-harness", "deepseek-harness-agent-teams", "project"]
aliases: ["DeepSeek Harness: deepseek-harness-agent-teams"]
---

# DeepSeek Harness: deepseek-harness-agent-teams — Deepseek Harness Agent Teams

DeepSeek Harness is an open-source agent runtime and benchmarking framework on the Cordis plugin architecture, for running and evaluating language models.

**Development line:** project:deepseek-harness · thread deepseek-harness-agent-teams  
**Last event:** 2026-11-27 · 1 dated since 2026-11-27 · **Researched:** 2026-11-28 · confidence: medium

## What it is

DeepSeek Harness gives a language model an execution environment, a tool registry, a session manager and an evaluation pipeline. It is a modular platform for standardizing agent evaluations and running long-horizon coding tasks without a proprietary agent harness.

What it does:

- Prompt loop: orchestrates the prompt-loop steps.
- Event log: records events in an append-only log.
- Prefix caching: optimizes the prompt prefix for caching.
- Sandboxing: runs code through E2B and Playwright/Chromium.
- Benchmark tracking: follows multi-step benchmarks automatically.

Limits: it needs external LLM provider endpoints and sandboxed execution environments. It also requires a strictly stable context prefix.

## Development line

- **2026-11-27 — DeepSeek Harness Benchmark Across Four LLM Aggregators.** A comparison of four AI model aggregators (ProxyAPI, Polza.ai, AITunnel, TeamoRouter) used with DeepSeek Harness. It looks at billing, token consumption and latency.
  - The benchmark runs all four aggregator backends under identical DeepSeek Harness agent tool-calling loops. It measures billing variance, token cache hit rates and request latency. (2026-11-27) — <https://habr.com/ru/articles/1113016/>

## What changed

The framework moved from a local execution environment to a multi-backend agent evaluation platform. Integration grew from direct model API calls to third-party routing aggregators. That added automated token accounting and latency benchmarking across different providers. Architecture updates made append-only event logging and strict prompt prefix caching formal, so benchmark runs stay reproducible.

## How to use this

1. Point DeepSeek Harness at an OpenAI-compatible endpoint URL of the chosen aggregator (ProxyAPI, Polza.ai, AITunnel or TeamoRouter) and add its API key.
  — <https://habr.com/ru/articles/1113016/>
2. Run multi-step agent benchmark tasks through the DeepSeek Harness CLI (dsh). Measure request latency, token consumption and billing consistency across the loops.
  — <https://habr.com/ru/articles/1113016/>

## Best practices

- Profile aggregator latency and prompt cache pass-through before using DeepSeek Harness in multi-step production loops. Aggregators differ significantly in cache billing and response overhead.
  — <https://habr.com/ru/articles/1113016/>
- Keep the prefix byte-for-byte stable across prompt turns, so the aggregator passes prompt caching through and does not bill tokens twice.
  — <https://habr.com/ru/articles/1113016/>

## What practitioners say

- One practitioner ran DeepSeek Harness across four LLM proxy aggregators. Latency varied significantly, and each provider handled token cache pass-through differently. (2026-11-27)
  — <https://habr.com/ru/articles/1113016/>

## Superseded by this

- The assumption that billing and latency are the same on every OpenAI-compatible aggregator backend when driving DeepSeek Harness agent loops.
  — <https://habr.com/ru/articles/1113016/>

## Still unknown

- Release dates and version milestones before the 2026-11-27 benchmark are not confirmed. They could not be checked against the primary public repositories, because only indirect redirects were found, not direct links.
- Whether deepseek-harness-agent-teams is an independent multi-agent orchestration repository or a multi-agent configuration profile of the core DeepSeek Harness runtime. This stays open until the source repository schema can be read directly.

## Sources

| source | title | read |
|---|---|---|
| https://habr.com/ru/articles/1113016/ | DeepSeek Harness Benchmark Across Four LLM Aggregators | 2026-11-28 |

## Agent brief {#agent-brief}

- **Subject:** project:deepseek-harness, thread deepseek-harness-agent-teams, 1 dated events 2026-11-27 → 2026-11-27.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** medium. The dated entries under "Superseded by this" say what is obsolete.
