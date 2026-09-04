---
title: DALL-E 2 — Commercial adoption
category: projects
tags: [dalle-2, dalle-2-commercial-adoption, dalle_2_commercial_adoption, dalle_2_commercialization, project]
aliases: ["DALL-E 2"]
---

# DALL-E 2 — Commercial adoption

**Development line:** `project:dalle-2` · thread `dalle-2-commercial-adoption`  
**Events:** 1 dated, 2022-06-22 → 2022-06-22 · **Researched:** 2026-09-04 · confidence: medium

## What it is

DALL-E 2 — OpenAI’s 2022 prompt-to-image model, now a legacy dependency rather than a usable API product. - formerly generated images from text prompts - was used for early editorial image workflows Limit: OpenAI marks it deprecated and removed from the API. Verdict: migrate existing integrations to GPT-Image-2; do not start new DALL-E 2 work.

## Development line

- **2022-06-22 — Cosmopolitan documented a DALL-E 2 cover experiment.** On 2022-06-22, the linked Cosmopolitan coverage documented a cover experiment involving DALL-E 2. It provided an early visible example of the system appearing in a commercial editorial context. The supplied links do not establish the collaboration's terms or wider commercial scope.

## What changed

DALL-E 2 — 2022-06-22: Cosmopolitan used it in an editorial-cover workflow, with human art direction and manual placement of the masthead and cover lines because generated text was unreliable. 2022-06-30: a dated report described a user pricing survey, signalling monetization research rather than a published price or general launch; its full text was unavailable at review. 2026-09-04 (found today): OpenAI marks DALL-E 2 deprecated and removed from the API, and recommends GPT-Image-2 for current generation and editing. Limit: the editorial-use event and current retirement status are readable; the pricing-survey detail is not. Verdict: the development line ends in retirement, not a current DALL-E 2 product path.

## How to use this

As of 2022-06-22, practitioners could recognize DALL-E 2's entry into visible editorial use, but should not infer official pricing or licensing policy from the unverified 2022-06-30 user report.

1. Inventory legacy requests and workflows that name `dall-e-2`; do not send new requests to it because the model is removed from the API.
  — <https://developers.openai.com/api/docs/models/dall-e-2>
2. For a single prompt-to-image generation or one-shot edit, move the workflow to `gpt-image-2` through the Image API.
  — <https://developers.openai.com/api/docs/guides/image-generation>
3. For iterative or conversational image editing, use the Responses API image-generation tool so edits can continue with image context.
  — <https://developers.openai.com/api/docs/guides/image-generation>

## Best practices

- Treat this as a migration, not a model-selection exercise: OpenAI recommends GPT-Image-2 for supported image generation and editing.
  — <https://developers.openai.com/api/docs/models/dall-e-2>
- Use the Image API for one-shot work and the Responses API for multi-turn editable image flows.
  — <https://developers.openai.com/api/docs/guides/image-generation>
- In the replacement workflow, write explicit constraints, make small single-change iterations, and restate details that must remain unchanged to prevent drift.
  — <https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide>
- Set output size and quality deliberately; the current prompting guide treats outputs above 2560×1440 as experimental for GPT-Image-2.
  — <https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide>

## Superseded by this

- 2022-06-22: treating DALL-E 2 as an available choice for a new commercial editorial workflow is obsolete; the API model is removed as of the 2026-09-04 check.
- 2022-06-30: treating pricing-survey or waitlist research as a path to current DALL-E 2 access is obsolete; supported current integrations should use GPT-Image-2.

## Still unknown

- The 2022-06-30 Reddit pricing-survey report could not be retrieved today, so its wording, respondents, prices, and commercial outcome are unverified.
- The two historical development threads appear to concern the same product: one covers editorial adoption and the other prospective monetization.
- This review establishes that the API model is removed; it did not verify whether any archival front-end access still exists, which would not constitute a supported integration path.

## Sources

| source | title | read |
|---|---|---|
| https://developers.openai.com/api/docs/models/dall-e-2 | DALL·E 2 Model | OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/models/gpt-image-2 | GPT-Image-2 Model | OpenAI API | 2026-09-04 |
| https://developers.openai.com/api/docs/guides/image-generation | Image generation | OpenAI API | 2026-09-04 |
| https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide | GPT Image Generation Models Prompting Guide | 2026-09-04 |
| https://www.cosmopolitan.com/lifestyle/a40314356/dall-e-2-artificial-intelligence-cover/ | DALL-E 2 Makes Its First-Ever Magazine Cover for Cosmopolitan | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:dalle-2`, thread `dalle-2-commercial-adoption`, 1 dated events 2022-06-22 → 2022-06-22.
- **Practical note:** As of 2022-06-22, practitioners could recognize DALL-E 2's entry into visible editorial use, but should not infer official pricing or licensing policy from the unverified 2022-06-30 user report.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
