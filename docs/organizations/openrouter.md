---
title: OpenRouter
category: organizations

tags: [openrouter, openrouter-access, openrouter-development, organization]
aliases: ["OpenRouter"]
---

# OpenRouter

**Development line:** `organization:openrouter` · thread `openrouter-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-08 · confidence: medium

## What it is

OpenRouter is an OpenAI-compatible API gateway for builders who want to switch among providers without maintaining a separate integration for every vendor.

- Model selection and provider routing.
- Fallbacks, data-policy controls, tools, and structured outputs.
- Text, image/video generation, audio, embeddings, and transcription.

Official material lists 400+ models across 70+ providers. Availability and endpoint support vary. We use it for multi-model products or provider resilience. A direct provider API is simpler for one stable integration.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-05-15 — Russian secondary reporting claimed narrower access to U.S.-vendor models and account top-ups. Email-based reporting supports payment limits but not a confirmed full API shutdown.
- 2026-06-27 — Recipient-reported notices described an intended geography-based API-access stop. Public evidence does not establish a universal account, country, provider, or catalog block.

## How to use this

1. Choose raw HTTP, an OpenRouter client SDK, or its Agent SDK, then authenticate with an OpenRouter API key.
  — <https://openrouter.ai/docs/quickstart>
2. Send a Chat Completions request to https://openrouter.ai/api/v1/chat/completions with a model identifier and messages. An existing OpenAI SDK can use the same base URL.
  — <https://openrouter.ai/docs/quickstart>
3. Query the Models API before production use to filter for modality, supported parameters, pricing, context length, throughput, and latency.
  — <https://openrouter.ai/docs/guides/overview/models>
4. Add explicit provider, retention, and fallback constraints when the workload requires them. Otherwise keep routing behavior dynamic.
  — <https://openrouter.ai/docs/guides/routing/provider-selection>
5. For tool use, let the model request a tool, execute and authorize it in the client, then send the result in the next model call.
  — <https://openrouter.ai/docs/guides/features/tool-calling>
6. For machine-readable output, send a JSON Schema response format and require compatible providers.
  — <https://openrouter.ai/docs/guides/features/structured-outputs>

## Best practices

- For structured output, check endpoint support, use response JSON Schema with strict mode, and set provider.require_parameters=true. Still validate returned data because enforcement varies by provider.
  — <https://openrouter.ai/docs/guides/features/structured-outputs>
- For reproducible or compliance-bound workloads, pin the required model and provider. Disabling fallbacks is a deliberate availability trade-off.
  — <https://openrouter.ai/docs/guides/routing/provider-selection>
- For multi-turn workloads, use a stable session_id and inspect cached_tokens and cache_write_tokens rather than assuming cache savings.
  — <https://openrouter.ai/docs/guides/best-practices/prompt-caching>
- Treat tool calls as untrusted requests. The client owns authorization, execution, and returning tool results to the model.
  — <https://openrouter.ai/docs/guides/features/tool-calling>
- When input-retention requirements apply, set an explicit data_collection policy or require ZDR endpoints rather than relying on default routing.
  — <https://openrouter.ai/docs/guides/routing/provider-selection>

## Superseded by this

- 2026-05-15 — The blanket claim that OpenRouter confirmed a complete Russian API shutdown is unsupported. Dated evidence separates unverified access claims from reported account-payment restrictions.
- 2026-08-10 — Treat pre-update openrouter/auto choices as superseded. The current router uses an updated selection method and can change with recent aggregate usage.
- 2026-08-19 — Treat a completed Stripe transaction as unverified. OpenRouter's announcement said the transaction remained subject to customary closing conditions.

## Still unknown

- No first-party public announcement was located for either dated access step. The official announcements index is negative evidence only and does not rule out account notices.
- The May 15 reports conflict on scope. Available evidence does not establish whether model access, billing, IP geography, or account geography was affected for any particular user.
- The June 27 reports do not prove actual enforcement, Belarus coverage, Russian-IP behavior, or a full all-model shutdown.
- It is unknown whether the May reporting and June notices were one policy sequence or separate billing and model-eligibility changes.

## Sources

| source | title | read |
|---|---|---|
| https://openrouter.ai/docs/quickstart | Quickstart — OpenRouter Documentation | 2026-09-08 |
| https://openrouter.ai/docs/guides/overview/models | OpenRouter Models - Unified Access to 400+ AI Models | 2026-09-08 |
| https://openrouter.ai/docs/guides/routing/provider-selection | Provider Routing - Smart Multi-Provider Request Management | 2026-09-08 |
| https://openrouter.ai/docs/guides/features/tool-calling | Tool & Function Calling - Use Tools with OpenRouter | 2026-09-08 |
| https://openrouter.ai/docs/guides/features/structured-outputs | Structured Outputs - Type-Safe JSON Responses from AI Models | 2026-09-08 |
| https://openrouter.ai/docs/guides/best-practices/prompt-caching | Prompt Caching - Optimize AI Model Costs with Smart Caching | 2026-09-08 |
| https://vc.ru/ai/2927281-openrouter-ogranichivaet-rossiyan-v-dostupe-k-chatgpt | Полная жесть: OpenRouter теперь закрывает россиянам доступ к ChatGPT, Claude и Gemini 😢 — AI на vc.ru | 2026-09-08 |
| https://habr.com/ru/news/1034012/ | OpenRouter перестал принимать платежи для учеток с регионом Россия / Хабр | 2026-09-08 |
| https://www.reddit.com/r/openrouter/comments/1ufjcq3/anyone_else_got_this_openrouter_notice/ | anyone else got this openrouter notice? : r/openrouter | 2026-09-08 |
| https://openrouter.ai/blog/announcements/ | Announcements — OpenRouter Blog | 2026-09-08 |
| https://openrouter.ai/blog/announcements/may-release-spotlight/ | May Release Spotlight — OpenRouter Blog | 2026-09-08 |
| https://openrouter.ai/blog/announcements/openrouter-mcp-server/ | The OpenRouter MCP Server — OpenRouter Blog | 2026-09-08 |
| https://openrouter.ai/blog/insights/every-modality-one-api/ | Every Modality Through One API — OpenRouter Blog | 2026-09-08 |
| https://openrouter.ai/blog/announcements/introducing-the-new-auto-router/ | Model Routing Powered by Wisdom of the Market — OpenRouter Blog | 2026-09-08 |
| https://openrouter.ai/blog/announcements/activity-dashboard/ | Understand your AI usage: every agent, model, and request — OpenRouter Blog | 2026-09-08 |
| https://openrouter.ai/blog/announcements/openrouter-is-joining-stripe/ | OpenRouter is Joining Stripe — OpenRouter Blog | 2026-09-08 |

## Agent brief {#agent-brief}

- **Subject:** `organization:openrouter`, thread `openrouter-development`, 0 dated events - → -.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
