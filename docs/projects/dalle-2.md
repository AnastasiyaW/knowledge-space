---
title: DALL-E 2 — Commercial adoption
category: projects
date: 2022-06-22
tags: [dalle-2, dalle-2-commercial-adoption, dalle_2_commercial_adoption, dalle_2_commercialization, project]
aliases: ["DALL-E 2"]
---

# DALL-E 2 — Commercial adoption

**Development line:** `project:dalle-2` · thread `dalle-2-commercial-adoption`  
**Last event:** 2022-06-22 · 1 dated since 2022-06-22 · **Researched:** 2026-09-04 · confidence: medium

## What it is

DALL-E 2 — OpenAI’s 2022 prompt-to-image model, now a legacy dependency rather than a usable API product.

- image generation from text prompts
- editorial image workflows for early commercial experiments

## Development line

- **2022-06-22 — Cosmopolitan documented a DALL-E 2 cover experiment.** On 2022-06-22, Cosmopolitan documented a cover experiment using DALL-E 2. It showed the system in a commercial editorial context. The links do not establish collaboration terms or wider commercial scope.

## What changed

On 2022-06-22, Cosmopolitan used DALL-E 2 in an editorial cover workflow. Human art directors placed the masthead and cover lines manually because generated text was unreliable.
On 2022-06-30, a dated report described a user pricing survey about monetization, not a published price or general launch. We could not read the full report text at review.
On 2026-09-04, OpenAI marked DALL-E 2 deprecated and removed from the API, and recommended GPT-Image-2 for generation and editing.
We can verify the editorial experiment and the model retirement, but not the pricing survey details. The development line ends in retirement, not a current DALL-E 2 product path.

## How to use this

As of 2022-06-22, we see DALL-E 2 enter commercial editorial use. We do not infer official pricing or licensing policy from the unverified 2022-06-30 user report.

1. Inventory legacy workflows that name `dall-e-2`; do not send new requests to it because OpenAI removed the model from the API.
  — <https://developers.openai.com/api/docs/models/dall-e-2>
2. For single prompt-to-image generation or one-shot editing, move the workflow to `gpt-image-2` through the Image API.
  — <https://developers.openai.com/api/docs/guides/image-generation>
3. For conversational or iterative image editing, use the Responses API image-generation tool so edits keep image context.
  — <https://developers.openai.com/api/docs/guides/image-generation>

## Best practices

- Treat this as a migration, not a model choice, because OpenAI recommends GPT-Image-2 for supported image generation and editing.
  — <https://developers.openai.com/api/docs/models/dall-e-2>
- Use the Image API for one-shot tasks and the Responses API for multi-turn editable flows.
  — <https://developers.openai.com/api/docs/guides/image-generation>
- In the replacement workflow, write explicit constraints, make small single-change iterations, and restate unchanged details so images do not drift.
  — <https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide>
- Set output size and quality deliberately: the prompting guide treats output sizes above 2560×1440 as experimental for GPT-Image-2.
  — <https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide>

## Superseded by this

- 2022-06-22: treating DALL-E 2 as an available choice for new commercial editorial workflows is obsolete because OpenAI removed the API model by 2026-09-04.
- 2022-06-30: treating pricing-survey or waitlist research as a path to DALL-E 2 access is obsolete; supported integrations should use GPT-Image-2.

## Still unknown

- We could not retrieve the 2022-06-30 Reddit pricing survey, so its wording, respondents, prices, and commercial outcome remain unverified.
- The two historical development threads appear to cover the same product: editorial adoption and prospective monetization.
- We confirmed the API model is removed, but we did not verify whether archival front-end access still exists; it does not offer a supported integration path.

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
