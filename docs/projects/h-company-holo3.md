---
title: Holo3
category: projects
date: 2026-04-02
tags: [h-company-holo3, holo3-model-release, holo3_model_release, project]
aliases: ["Holo3"]
---

# Holo3

**Development line:** `project:h-company-holo3` · thread `holo3-model-release`  
**Last event:** 2026-04-02 · 1 dated since 2026-04-02 · **Researched:** 2026-09-05 · confidence: high

## What it is

Holo3 is a multimodal MoE model for computer use. It accepts text and up to five images, and returns a text action or decision for agent workflows. API models are 35B-A3B and 122B-A10B with a 65 536 token context. Open weights for the original 35B-A3B are released under Apache-2.0. For new integrations, start with the current Holo3.1 line; treat the original Holo3 as an earlier compatible open checkpoint.

## Development line

- **2026-04-02 — H Company released the Holo3 model.** On 2026-04-02, H Company published Holo3 as a new model release. Linked project, API, and model-repository pages indicate the release was intended for both direct use and model access. Without source text or independent research, exact capabilities and release terms remain unconfirmed.

## What changed

- 2026-04-02 — Holo3-35B-A3B open weights released; release page frames Holo3 as a computer-use model and names 122B-A10B as the API flagship.
- 2026-04-15 — HoloTab made the model available through a browser agent application.
- 2026-04-28 — Holotron 3 Nano (30B-A3B) released as a faster separate model for computer automation tasks.
- 2026-06-01 — Holo3.1 expanded the line with 0.8B, 4B, 9B, and 35B-A3B variants, function calling, mobile support, and local quantized weights.

## How to use this

From 2026-04-02, evaluate Holo3 through H Company’s model and API documentation before choosing it for a workflow; verify supported capabilities and access terms on the linked pages.

1. Create a Portal-H account and API key; the free tier gives limited access to the 35B-A3B API.
  — <https://hcompany.ai/holo-models-api>
2. Use `holo3-1-35b-a3b` for time-capped, well-defined tasks; use `holo3-122b-a10b` for complex multi-step scenarios if commercial terms and pricing fit.
  — <https://hcompany.ai/holo-models-api>
3. For local runs of the original open Holo3, download `Hcompany/Holo3-35B-A3B` via Transformers, vLLM, or SGLang and pass messages in the multimodal chat template.
  — <https://huggingface.co/Hcompany/Holo3-35B-A3B>
4. For mobile setups, function calling, or local quantized weights, move to Holo3.1 and match weight size and format to target hardware.
  — <https://hcompany.ai/holo3.1>

## Best practices

- Pick 35B-A3B for latency-sensitive, economical, and well-defined automations; pick 122B-A10B for new or complex multi-step environments.
  — <https://hcompany.ai/holo-models-api>
- Check weight format and runtime before local deployment: original Holo3 is documented for Transformers, vLLM, and SGLang; Holo3.1 adds FP8, Q4 GGUF, and NVFP4.
  — <https://huggingface.co/Hcompany/Holo3-35B-A3B>
- Do not treat zero data retention claims as a substitute for data review: the API does not store prompts and responses by default, but logs account metadata and tokens.
  — <https://hcompany.ai/holo-models-api>

## Superseded by this

- 2026-06-01 — Holo3.1 supersedes original Holo3 as the recommended line for mobile setups, function calling, and local quantized runs.
- 2026-06-01 — Limiting to a single 35B-A3B variant is obsolete: 0.8B, 4B, 9B, and 35B-A3B variants of Holo3.1 are available.

## Still unknown

- For 122B-A10B, the current API page lists a Research only (non-commercial) license; access terms and licensing on the 2 April release date are not separately confirmed.
- Public sources confirm Holo3-35B-A3B released on 2 April, while the main announcement page is dated 31 March; the gap looks like announcement date versus weights release date, but exact publication time is not stated.

## Sources

| source | title | read |
|---|---|---|
| https://hcompany.ai/holo3 | Holo3: Breaking the Computer Use Frontier — H Company, 31 March 2026 | 2026-09-05 |
| https://hcompany.ai/holo-models-api | Holo Models API — H Company | 2026-09-05 |
| https://huggingface.co/Hcompany/Holo3-35B-A3B | Hcompany/Holo3-35B-A3B — Hugging Face | 2026-09-05 |
| https://hcompany.ai/holo3.1 | Holo3.1: Fast & Local Computer Use Agents — H Company, 1 June 2026 | 2026-09-05 |
| https://hcompany.ai/meet-holotab | HoloTab — H Company, 15 April 2026 | 2026-09-05 |
| https://hcompany.ai/holotron3 | Holotron 3 Nano — H Company, 28 April 2026 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:h-company-holo3`, thread `holo3-model-release`, 1 dated events 2026-04-02 → 2026-04-02.
- **Practical note:** From 2026-04-02, practitioners should evaluate Holo3 through H Company’s model and API documentation before selecting it for a workflow; the exact supported capabilities and access terms require verification from the linked pages.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.