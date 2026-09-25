---
title: Ling-3.0-flash — Model availability
category: projects
date: 2026-07-27
tags: [ling-3-0-flash, ling_flash, model-availability, project]
aliases: ["Ling-3.0-flash"]
---

# Ling-3.0-flash — Model availability

**Development line:** `project:ling-3-0-flash` · thread `model-availability`  
**Last event:** 2026-07-27 · 1 dated since 2026-07-27 · **Researched:** 2026-09-08 · confidence: high

## What it is

Ling-3.0-flash is an Ant Group text-generation MoE for teams building coding, tool-using, and long-context agents.

- Native hybrid-linear MoE architecture with reasoning and tool calling.
- OpenRouter route exposes a 262,144-token context and up to 32,768 output tokens.

124B total parameters, about 5.1B active per token; the OpenRouter route is text-only. It works for agent workloads, but we must keep JSON validation and tool execution in the application.

## Development line

- **2026-07-27 — Ling-3.0-flash received a dated OpenRouter model reference.** On 2026-07-27, an entry linked to OpenRouter's public model page for InclusionAI Ling-3.0-flash. That provides a dated public reference for the model, but does not establish its launch date, capabilities, or current service availability.

## What changed

- 2026-07-23 — Ant Ling v2.0.0 made Ling-3.0-flash available in chat and through OpenAI- and Anthropic-compatible APIs, with a deep-thinking toggle.
- 2026-07-24 — The formal release announcement added a limited free-access period on Ant Ling and OpenRouter.
- 2026-07-27 — Ant Ling v2.0.1 added the Explore module; it was not a Ling-3.0-flash model release or provider-listing change.
- 2026-08-02 — The official base-weight repository was initialized and populated.
- 2026-08-04 — Official FP8 and INT4 weight repositories were initialized and populated.

## How to use this

1. Send an OpenAI-compatible Chat Completions request to OpenRouter with the exact model ID `inclusionai/ling-3.0-flash`, a bearer key, and `messages`.
  — <https://openrouter.ai/docs/quickstart>
2. Keep prompt plus completion within the current 262,144-token context; cap a completion at 32,768 tokens or lower for the workload.
  — <https://openrouter.ai/inclusionai/ling-3.0-flash>
3. For tool use, send `tools` and `tool_choice`, execute the returned call in the client, append its result, and make the next model request.
  — <https://openrouter.ai/docs/guides/features/tool-calling>
4. During a production pilot, send `X-OpenRouter-Metadata: enabled` and retain the returned routing metadata to see the selected provider and fallback attempts.
  — <https://openrouter.ai/docs/guides/features/router-metadata>

## Best practices

- Treat OpenRouter price, availability, and provider figures as current observations rather than a fixed model property; recheck them before making a budget or latency commitment.
  — <https://openrouter.ai/inclusionai/ling-3.0-flash>
- Do not rely on `response_format` for strict JSON on the current OpenRouter route: its model page says JSON is not enforced. Validate parsed output in the application.
  — <https://openrouter.ai/inclusionai/ling-3.0-flash>
- Keep tool execution client-controlled: the model proposes a call, while the application performs it and returns its result.
  — <https://openrouter.ai/docs/guides/features/tool-calling>
- For a strict JSON-schema workload, use only an endpoint that currently advertises structured-output support and require supported parameters in routing preferences.
  — <https://openrouter.ai/docs/guides/features/structured-outputs>
- For self-hosting, start from the publisher's sampling recipe (`temperature=0.6`, `top_p=0.95`, `top_k=20`) and its runtime-specific parser configuration rather than copying it blindly to another gateway.
  — <https://huggingface.co/inclusionAI/Ling-3.0-flash>

## Superseded by this

- 2026-07-27 — Treating the OpenRouter-linked event date as the Ling-3.0-flash launch date; the official changelog puts the model launch on 2026-07-23 and the July 27 change is Explore.
- 2026-08-03 — Launch-period free API access; the formal announcement set its end at 23:00 Beijing time, so it is not current pricing guidance.

## Still unknown

- No archived first-listing evidence establishes that OpenRouter first exposed this model on 2026-07-27; the dated link proves only an observation on that date.
- The current OpenRouter provider set, prices, routing, and feature matrix are volatile and were not projected backward into the July event.
- Ling-3.0-flash-VL is a separately named multimodal model; the reviewed sources do not establish that it is a checkpoint update of this text-only model.

## Sources

| source | title | read |
|---|---|---|
| https://openrouter.ai/models/inclusionai/ling-3.0-flash | OpenRouter model URL supplied with the dated event | 2026-09-08 |
| https://openrouter.ai/inclusionai/ling-3.0-flash | Ling 3.0 Flash - API Pricing & Benchmarks | OpenRouter | 2026-09-08 |
| https://developer.ant-ling.com/en/docs/getting-started/changelog/ | Changelog | Ant Ling | 2026-09-08 |
| https://developer.ant-ling.com/zh-CN/blogs/ling-3.0-flash-release | Ling-3.0-flash：智以密胜 | Ant Ling | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash | inclusionAI/Ling-3.0-flash | Hugging Face | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash/commits/main | Commits · inclusionAI/Ling-3.0-flash | Hugging Face | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash-fp8/commits/main | Commits · inclusionAI/Ling-3.0-flash-fp8 | Hugging Face | 2026-09-08 |
| https://huggingface.co/inclusionAI/Ling-3.0-flash-int4/commits/main | Commits · inclusionAI/Ling-3.0-flash-int4 | Hugging Face | 2026-09-08 |
| https://openrouter.ai/docs/quickstart | OpenRouter Quickstart Guide | 2026-09-08 |
| https://openrouter.ai/docs/guides/features/tool-calling | Tool & Function Calling - Use Tools with OpenRouter | 2026-09-08 |
| https://openrouter.ai/docs/guides/features/router-metadata | Router Metadata - Inspect Routing Decisions on Every Response | 2026-09-08 |
| https://openrouter.ai/docs/guides/features/structured-outputs | Structured Outputs - Type-Safe JSON Responses from AI Models | 2026-09-08 |

## Agent brief {#agent-brief}

- **Subject:** `project:ling-3-0-flash`, thread `model-availability`, 1 dated events 2026-07-27 → 2026-07-27.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.