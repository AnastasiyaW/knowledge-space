---
title: xAI — Grok model development
category: organizations
tags: [grok-model-development, grok_4, grok_release, organization, xai]
aliases: ["xAI"]
---

# xAI — Grok model development

**Development line:** `organization:xai` · thread `grok-model-development`  
**Events:** 1 dated event, 2025-07-08 → 2025-07-08 · **Researched:** 2026-09-04 · confidence: medium

## What it is

xAI makes Grok and provides an API for teams building chat, coding, and agent workflows.

Capabilities:

- Grok 4.6 accepts text and images and returns text;
- Grok 4.6 supports configurable reasoning;
- Grok supports function calling, Web/X Search, and code execution;
- Voice and Imagine APIs are separate.

Limit: Grok 4.6 has a 500k-token context window; below 200k input tokens, its API price is $2 / $0.50 / $6 per 1M input / cached-input / output tokens.

For a new text or coding integration, use the current model rather than the original Grok 4 slug.

## Development line

- **2025-07-08 — xAI’s Grok 4 development milestone.** Grok 4 and Grok 4 Heavy reached subscribers and the xAI API with native tool use and real-time Web/X search.

## What changed

2024-08-15 — “uncensored” is an unverified positioning label. No first-party release record connects it to a Grok version, endpoint, policy, or availability change.

2025-07-08 — The linked social post was not retrievable. The first confirmed product change is 2025-07-09: Grok 4 and Grok 4 Heavy reached subscribers and the xAI API with native tool use and real-time Web/X search.

2026-05-15 — `grok-4-0709` and several older Grok slugs were retired; calls to the old Grok 4 slug redirect to `grok-4.3`.

As of 2026-09-04, Grok 4.6 has been available in the API since 2026-08-12 and is the current default for code and general text work.

## How to use this

As of 2025-07-08, practitioners evaluating xAI’s Grok should revisit model-selection assumptions at the Grok 4 milestone. Verify current capability and access details from primary sources before adopting it.

1. Create an xAI Console account and add credits.
  — <https://docs.x.ai/developers/quickstart>
2. Create an API key and load it through `XAI_API_KEY`.
  — <https://docs.x.ai/developers/quickstart>
3. Select `grok-4.6` for a new general text or coding integration; use a dated slug when output consistency matters.
  — <https://docs.x.ai/developers/models>
4. Send the first request to the Responses API with the xAI SDK or an OpenAI client pointed at `https://api.x.ai/v1`.
  — <https://docs.x.ai/developers/quickstart>
5. Enable Web Search or X Search when an answer depends on current information.
  — <https://docs.x.ai/developers/models>

## Best practices

- Pin a dated model slug for reproducible production behavior. Use `-latest` only when automatic model updates are wanted.
  — <https://docs.x.ai/developers/models>
- Treat current-event questions as a tool-use case. Enable server-side search rather than relying on the model’s training cutoff.
  — <https://docs.x.ai/developers/models>
- For repeated conversations, use a stable `prompt_cache_key` or `x-grok-conv-id`. Keep the prefix append-only and monitor `cached_tokens`.
  — <https://docs.x.ai/developers/advanced-api-usage/prompt-caching/best-practices>
- Budget against both RPS and TPM. Handle HTTP 429 with bounded exponential backoff.
  — <https://docs.x.ai/developers/rate-limits>

## Superseded by this

- 2026-05-15 — The 2025-era `grok-4-0709` deployment target is obsolete: xAI retires it and redirects calls to `grok-4.3`; choose a replacement explicitly to control reasoning and price.
- 2026-08-12 — Default guidance for new general text and coding work moved to `grok-4.6`; this does not itself retire supported `grok-4.3`.

## Still unknown

- The 2024-08-15 reference is an X search URL, not an archived release note; it did not establish the claimed “uncensored” state.
- The 2025-07-08 x.com status URL was inaccessible at review time, so its wording was not used.
- No first-party Simplified Chinese model-specific release or documentation page was found. The fact-bearing sources are English.

## Sources

| source | title | read |
|---|---|---|
| https://x.ai/news/grok-4 | Grok 4 | SpaceXAI | 2026-09-04 |
| https://docs.x.ai/developers/migration/may-15-retirement | Grok Model Retirement on May 15, 2026 | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/release-notes | Release Notes | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/models | Grok Models & Pricing | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/grok-4-6 | Grok 4.6 | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/quickstart | Grok API Quickstart: Get Your API Key | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/advanced-api-usage/prompt-caching/best-practices | Best Practices & FAQ | SpaceXAI Docs | 2026-09-04 |
| https://docs.x.ai/developers/rate-limits | Rate Limits | SpaceXAI Docs | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:xai`, thread `grok-model-development`, 1 dated event 2025-07-08 → 2025-07-08.
- **Practical note:** As of 2025-07-08, practitioners evaluating xAI’s Grok should revisit model-selection assumptions at the Grok 4 milestone. Verify current capability and access details from primary sources before adopting it.
- **Confidence:** medium. The dated superseded entries above are the authority for what is obsolete.

