---
title: GPT-4
category: projects
tags: [announcements, gpt-4, gpt-4-development, gpt_4_architecture, project]
aliases: ["GPT-4"]
---

# GPT-4

**Development line:** `project:gpt-4` · thread `gpt-4-development`  
**Events:** 1 dated, 2023-03-09 → 2023-03-09 · **Researched:** 2026-09-04 · confidence: medium

## What it is

GPT-4 is an older OpenAI model for preserving existing text-only API integrations.

- Text: accepts and returns text.
- Streaming: supports streaming.
- Fine-tuning: supports fine-tuning.
- Chat Completions: documented interface.

8,192-token context; $30 input and $60 output per million tokens; image, audio, video, function calling, and Structured Outputs are not supported.

Retain it only where compatibility is measured; use a newer model for new work.

## Development line

- **2023-03-09 — Pre-release forecast for GPT-4.** On 2023-03-09, Microsoft Germany stated that GPT-4 was expected the following week and would be multimodal. This statement was a pre-release claim about expected capabilities, not a confirmation of release.

## What changed

GPT-4 shifted from a general release to a retired ChatGPT model and legacy API role.

- 2023-03-09: pre-release reports forecast an imminent multimodal launch.
- 2023-03-14: OpenAI announced GPT-4 with text and image input and text output. Public access opened with text, while image input remained in limited alpha.
- 2023-06-22: an architecture entry has no URL, so no architectural change can be verified.
- 2023-07-06: API access became generally available to paying developers, with guidance to use Chat Completions rather than legacy Completions.
- 2025-04-30: OpenAI retired GPT-4 from ChatGPT and replaced it with GPT-4o, while leaving the API active.
- 2026-09-04: the individual model page shows `gpt-4` as an older default model, while the catalog classifies GPT-4 as Deprecated.

Documented operating limits remain an 8,192-token context and $30/$60 per million text tokens.

Treat GPT-4 as a legacy API model for compatibility, not as a choice for ChatGPT.

## How to use this

Treat reports from 2023-03-09 as preliminary until primary documentation confirms release capabilities.

1. Skip ChatGPT for GPT-4, because OpenAI retired it there on 2025-04-30; see the [ChatGPT release notes](https://help.openai.com/en/articles/6825453). Use it only when existing API integrations require measured legacy behavior.
2. Send an authenticated `GET /v1/models/gpt-4` request before deploying to inspect visible model IDs and shutdown dates via the [Models API](https://developers.openai.com/api/reference/resources/models).
3. Post ordered text messages with model set to `gpt-4` through the documented endpoint `POST /v1/chat/completions`, as outlined in [Chat Completions](https://developers.openai.com/api/reference/cli/resources/chat/subresources/completions).
4. Run task-specific evaluations before keeping or replacing GPT-4, deciding by cost, features, and benchmark scores from [evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).

## Best practices

- Run task-specific evaluations continuously and calibrate automated scores with human judgment, following [evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices).
- Maintain human review for high-stakes outputs and provide reviewers with source material to verify answers, per [safety best practices](https://developers.openai.com/api/docs/guides/safety-best-practices).
- Avoid designing GPT-4 workflows around images, audio, tools, or Structured Outputs, as the [GPT-4 model reference](https://developers.openai.com/api/docs/models/gpt-4) lists them as unsupported.
- Keep API keys out of source code, separate staging from production, and set spend alerts before traffic starts, as described in [production best practices](https://developers.openai.com/api/docs/guides/production-best-practices).

## Superseded by this

- 2023-03-09: treating pre-release forecasts as confirmed availability was superseded by OpenAI's 2023-03-14 launch.
- 2023-03-14: guidance to select GPT-4 in ChatGPT became obsolete on 2025-04-30 when ChatGPT replaced it with GPT-4o.
- 2023-03-14: treating image input as an API capability is obsolete because it remained limited alpha at launch and the current `gpt-4` page lists it as unsupported.
- 2023-07-06: general availability guidance is stale because current documentation calls GPT-4 older, categorizes it as Deprecated in the catalog, and requires account verification.

## Still unknown

- The 2023-06-22 `gpt_4_architecture` entry lacks a URL and public text, so no architectural claim can be verified.
- The 2023-03-09 entry and the separate `openai_gpt4` / `gpt4_development` route conflict in the registry, leaving it unclear whether they represent duplicate routes or separate subjects.
- Official documentation contradicts itself: the GPT-4 detail page shows a default `gpt-4` alias, while the catalog lists GPT-4 as Deprecated. An authenticated Models API check must verify access.

## Sources

| source | title | read |
|---|---|---|
| https://www.heise.de/news/GPT-4-is-coming-next-week-and-it-will-be-multimodal-says-Microsoft-Germany-7540972.html | GPT-4 is coming next week and it will be multimodal, says Microsoft Germany — Heise (current access redirected) | 2026-09-04 |
| https://openai.com/index/gpt-4-research/ | GPT-4 — OpenAI | 2026-09-04 |
| https://community.openai.com/t/gpt-4-api-general-availability-and-deprecation-of-older-models-in-the-completions-api/289518 | GPT-4 API general availability and deprecation of older models in the Completions API — OpenAI Developer Community | 2026-09-04 |
| https://openai.com/index/gpt-4-api-general-availability/ | GPT-4 API general availability and deprecation of older models in the Completions API — OpenAI | 2026-09-04 |
| https://help.openai.com/en/articles/6825453 | ChatGPT — Release Notes — OpenAI Help Center | 2026-09-04 |
| https://developers.openai.com/api/docs/models/gpt-4 | GPT-4 Model — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/models/all | All models — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/reference/resources/models | Models — OpenAI API reference | 2026-09-04 |
| https://developers.openai.com/api/reference/cli/resources/chat/subresources/completions | Completions — OpenAI API reference | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/evaluation-best-practices | Evaluation best practices — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/safety-best-practices | Safety best practices — OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/production-best-practices | Production best practices — OpenAI API | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:gpt-4`, thread `gpt-4-development`, 1 dated events 2023-03-09 → 2023-03-09.
- **Practical note:** As of 2023-03-09, treat third-party reports of GPT-4 multimodal release as preliminary until primary documentation confirms availability.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
