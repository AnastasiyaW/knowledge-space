---
title: "Otus: llm-loop-diagnosis — Llm Loop Diagnosis"
category: "projects"
date: 2026-09-03
tags: ["llm-loop-diagnosis", "otus", "project"]
aliases: ["Otus: llm-loop-diagnosis"]
---

# Otus: llm-loop-diagnosis — Llm Loop Diagnosis

**Development line:** project:otus · thread llm-loop-diagnosis  
**Last event:** 2026-09-03 · 1 dated since 2026-09-03 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Otus: llm-loop-diagnosis is an incident-response method to troubleshoot repeated LLM generation in production.

We classify token, fragment, and semantic loops, inspect length and latency distributions, reproduce the failure, and apply bounded repetition detection before changing sampling. Token n-gram detection catches repeated fragments, but it does not detect semantic loops. The sequence works for incident response, though the main scenario is a synthetic reconstruction rather than a measured production postmortem.

## Development line

- **2026-09-03 — Habr article published on 2026-09-03 diagnosing LLM looping failures in production, identifying diagnostic signals, token limit constraints, and infrastructure load without error logs.** An article on LLM production diagnostics details signal detection and loop prevention without relying on error logs.
  - vLLM official API documentation confirms that `repetition_detection` detects repetitive output n-grams and stops generation early. This avoids generations running until the maximum token limit. It provides an engine-level guard for repeated fragments, not semantic loops. (undated) — <https://docs.vllm.ai/en/stable/api/vllm/entrypoints/openai/completion/protocol/>
  - Qwen official guidance gives non-greedy sampling settings for Qwen3 thinking mode: temperature 0.6, top-p 0.95, top-k 20, and min-p 0. The documentation warns that greedy decoding can cause endless repetitions. (undated) — <https://qwen.readthedocs.io/en/stable/getting_started/quickstart.html>

## What changed

We separate token repetition, repeated fragments, and semantic loops. A repeated tail on a length-limited completion is a diagnostic signal, not proof. We reproduce the run and compare configurations before changing any sampling parameters.

## How to use this

1. Classify the symptom into a single-token repeat, a repeated fragment, or a semantic loop. Record completion reason, output-length distribution, repeated tail, latency, and serving-configuration diffs before changing parameters.
  — <https://habr.com/ru/companies/otus/articles/1067766/>
2. Reproduce the failing request and change one variable at a time. Test prompt structure first if infrastructure did not change. Otherwise compare engine version, chat template, KV-cache settings, and quantization.
  — <https://habr.com/ru/companies/otus/articles/1067766/>
3. For vLLM deployments, configure `repetition_detection` only after testing representative outputs. It acts as an output-token n-gram guard that ends detected repetitions early.
  — <https://docs.vllm.ai/en/stable/api/vllm/entrypoints/openai/completion/protocol/>
4. For Qwen3 thinking-mode workloads, start with the vendor non-greedy sampling guidance and keep a generation-length budget.
  — <https://qwen.readthedocs.io/en/stable/getting_started/quickstart.html>

## Best practices

- Track a degeneration rate that combines length-limited repeated tails and detector stops. Measure retry rate, wasted output tokens, and quality separately so early truncation is not mistaken for a fix.
  — <https://habr.com/ru/companies/otus/articles/1067766/>
- Calibrate repetition detection on production outputs. Repetitions in JSON, code, tables, and tool arguments are often legitimate.
  — <https://habr.com/ru/companies/otus/articles/1067766/>
- Avoid greedy decoding for Qwen3 thinking mode. Start from the vendor baseline sampling settings instead.
  — <https://qwen.readthedocs.io/en/stable/getting_started/quickstart.html>
- Set separate budgets for generation and service limits. Generation needs output-token, wall-clock, and repetition thresholds. The service needs request deadlines, concurrency limits, and circuit breakers.
  — <https://habr.com/ru/companies/otus/articles/1067766/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The public article does not name the specific 30B model in its reconstructed case.
- The main incident scenario is synthetic. The article describes an external Qwen3 incident, but provides no public link to that community report.
- We found no independent practitioner discussion of this exact Otus diagnostic method.
- Token-level repetition controls do not prevent semantic loops.

## Sources

| source | title | read |
|---|---|---|
| https://habr.com/ru/companies/otus/articles/1067766/ | LLM зацикливается: как найти причину, не трогая параметры? | 2026-11-25 |
| https://docs.vllm.ai/en/stable/api/vllm/entrypoints/openai/completion/protocol/ | vLLM completion protocol API reference | 2026-11-25 |
| https://qwen.readthedocs.io/en/stable/getting_started/quickstart.html | Qwen Quickstart | 2026-11-25 |
| https://qwen.readthedocs.io/zh-cn/latest/getting_started/quickstart.html | Qwen 快速开始 | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:otus, thread llm-loop-diagnosis, 1 dated events 2026-09-03 → 2026-09-03.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.