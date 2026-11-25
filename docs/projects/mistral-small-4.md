---
title: Mistral Small 4 — Mistral Small
category: projects
date: 2026-03-17
tags: [mistral-small, mistral-small-4, project]
aliases: ["Mistral Small 4"]
---

# Mistral Small 4 — Mistral Small

**Development line:** `project:mistral-small-4` · thread `mistral-small`  
**Last event:** 2026-03-17 · 1 dated since 2026-03-17 · **Researched:** 2026-09-05 · confidence: high

## What it is

Mistral Small 4 combines instruction following, configurable reasoning, tool calling, JSON output, and text-plus-image input with text output. It has 119B total parameters, 6.5B active per token, and a 256k-token context window. Verdict: use it when consolidation matters more than minimal infrastructure; the publisher lists a minimum of four HGX H100s, two HGX H200s, or one DGX B200 for self-hosting.

## Development line

- **2026-03-17 — Mistral Small 4 119B 2603 Eagle repository was linked on Hugging Face.** On 2026-03-17, the record recorded a link to the Hugging Face repository for Mistral Small 4 119B 2603 Eagle. The repository name identifies a Mistral Small 4 model artifact and its 119B, 2603, and Eagle variant labels. The dated link alone does not establish release status, capabilities, license, or access conditions.

## What changed

2026-03-17 — The Mistral-Small-4-119B-2603 Eagle repository made the trained speculative-decoding head available for the 119B A6B base model. 2026-03-16 — Mistral announced the Mistral Small 4 base model: a unified successor path for instruct, reasoning, multimodal, and agentic-coding workloads, released under Apache 2.0.

## How to use this

As of 2026-03-17, practitioners should use the linked Hugging Face repository as the specific artifact to inspect for the Mistral Small 4 119B 2603 Eagle variant, then verify its model card, access terms, and release status before adoption.

1. Install the serving stack specified by the model card: vLLM, Transformers from main, and mistral_common 1.10.0 or later.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
2. Serve the base model with vLLM, enable Mistral tool and reasoning parsers, and attach the Eagle head through vLLM speculative decoding when its added serving complexity is justified.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
3. For ordinary requests set reasoning_effort to none; for difficult tasks set it to high through the OpenAI-compatible client or Mistral API.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>

## Best practices

- Use reasoning_effort="high" with temperature 0.7 for complex prompts; keep reasoning disabled and tune temperature from 0.0 to 0.7 for routine work.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
- Treat the Eagle repository as a speculative-decoding companion to the base model, not as the standalone application model.
  — <https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle>
- Plan self-hosting around the documented accelerator floor before selecting this model; its active-parameter count does not remove its base-weight memory requirements.
  — <https://mistral.ai/news/mistral-small-4/?id=MistralSmall4>

## Superseded by this

- 2026-03-16 — Guidance to select separate Mistral Small instruct, Magistral reasoning, Pixtral multimodal, and Devstral coding models for these four core capability classes is superseded for deployments where one Mistral Small 4 endpoint meets the requirements.

## Still unknown

- The supplied March 17 event links the Eagle repository, while Mistral's first-party announcement and lifecycle page date the base-model release to March 16, 2026. The repository page inspected today does not expose a repository creation date, so its exact publication time remains unverified.
- Mistral's release article gives 6B active parameters per token (8B when embedding and output layers are included), while the Eagle model card says 6.5B active. This answer preserves the model-card figure for the current serving artifact and does not treat the discrepancy as independently resolved.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/mistralai/Mistral-Small-4-119B-2603-eagle | mistralai/Mistral-Small-4-119B-2603-eagle | 2026-09-05 |
| https://mistral.ai/news/mistral-small-4/?id=MistralSmall4 | Introducing Mistral Small 4 | 2026-09-05 |
| https://legal.mistral.ai/ai-governance/models/mistral-small-4/ | Mistral Small 4 — Model Lifecycle | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:mistral-small-4`, thread `mistral-small`, 1 dated events 2026-03-17 → 2026-03-17.
- **Practical note:** As of 2026-03-17, practitioners should use the linked Hugging Face repository as the specific artifact to inspect for the Mistral Small 4 119B 2603 Eagle variant, then verify its model card, access terms, and release status before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
