---
title: Qwen 3.6 Plus Preview — Public model availability
category: projects
date: 2026-03-31
tags: [project, public-model-availability, qwen, qwen-3-6-plus-preview]
aliases: ["Qwen 3.6 Plus Preview"]
---

# Qwen 3.6 Plus Preview — Public model availability

**Development line:** `project:qwen-3-6-plus-preview` · thread `public-model-availability`  
**Last event:** 2026-03-31 · 1 dated since 2026-03-31 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Qwen 3.6 Plus Preview is a hosted preview model available under `qwen/qwen3.6-plus-preview:free` on OpenRouter.

- Agentic coding, front-end work, and general reasoning.
- 1,000,000-token context window.
- OpenRouter lists it as free, but prompts and completions may be used to improve the model.

## Development line

- **2026-03-31 — OpenRouter availability signal for Qwen 3.6 Plus Preview.** On 2026-03-31, OpenRouter listed an endpoint for Qwen 3.6 Plus Preview marked as free. We note this public-availability signal rather than a verified model launch. The evidence does not establish the operator, capabilities, terms, or whether the endpoint was live on that date.

## What changed

2026-03-31 — Qwen 3.6 Plus Preview became available through OpenRouter as a free preview endpoint; OpenRouter identifies the release date as 2026-03-30.

2026-04-03 — An unresolved community report said the model was unavailable through the international DashScope API, despite availability on Qwen Chat and the free Qwen Code CLI.

## How to use this

From 2026-03-31, we treat Qwen 3.6 Plus Preview as a possible OpenRouter free-endpoint option only after checking current availability and terms. We establish no capability or provenance claims.

1. Create an OpenRouter API key, then send a standard OpenAI-compatible request to `POST /api/v1/chat/completions` with model `qwen/qwen3.6-plus-preview:free`.
  — <https://openrouter.ai/docs/api_reference/overview>
2. Start with a bounded evaluation task such as repository review or long-document analysis; do not submit confidential material because the model page says prompts and completions may be collected for improvement.
  — <https://openrouter.ai/qwen/qwen3.6-plus-preview:free>
3. For quota failures, inspect the key endpoint and honor `Retry-After`; use exponential backoff for 429 responses.
  — <https://openrouter.ai/docs/api_reference/limits>

## Best practices

- Pin the exact model ID and retain outputs from representative tests before making it a dependency, so evaluations remain reproducible.
  — <https://openrouter.ai/qwen/qwen3.6-plus-preview:free>
- Do not send sensitive prompts or completions through this endpoint, because OpenRouter states that they may be collected for model improvement.
  — <https://openrouter.ai/qwen/qwen3.6-plus-preview:free>
- Implement exponential backoff and quota monitoring for free-model requests, because provider capacity and platform limits can return 429 errors.
  — <https://openrouter.ai/docs/api_reference/limits>

## Superseded by this

- 2026-03-31: the assumption that the release date was definitively March 31 is corrected by OpenRouter’s current model page, which lists March 30, 2026.
- 2026-03-31: treating Qwen 3.6 Plus Preview as a local or open-weight Qwen release is unsupported; the verified access path is the hosted OpenRouter listing.

## Still unknown

- No first-party Qwen model card, benchmark report, parameter count, architecture specification, post-preview pricing, or formal availability statement was found for this exact model.
- The April 3 DashScope availability claim is a user report in a Qwen GitHub issue, not a maintainer confirmation.
- The current OpenRouter page remains accessible and labels the model free, but a public page alone does not prove capacity, provider routing, or suitability for production traffic.

## Sources

| source | title | read |
|---|---|---|
| https://openrouter.ai/qwen/qwen3.6-plus-preview:free | Qwen3.6 Plus Preview - API Pricing & Providers | OpenRouter | 2026-09-05 |
| https://openrouter.ai/docs/api_reference/overview | OpenRouter API Reference - Complete Documentation | 2026-09-05 |
| https://openrouter.ai/docs/api_reference/limits | API Credit & Rate Limits - Handle 402 and 429 Errors | 2026-09-05 |
| https://github.com/QwenLM/Qwen3/issues/1838 | Qwen3.6 Plus - International API Access? · Issue #1838 · QwenLM/Qwen3 | 2026-09-05 |
| https://www.ithome.com/0/934/546.htm | 阿里通义千问 Qwen 3.6 Plus 免费预览版上线 OpenRouter | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen-3-6-plus-preview`, thread `public-model-availability`, 1 dated events 2026-03-31 → 2026-03-31.
- **Practical note:** From 2026-03-31, we treat Qwen 3.6 Plus Preview as a possible OpenRouter free-endpoint option only after checking current availability and terms. We establish no capability or provenance claims.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
