---
title: Cosmos 3 Edge
category: projects
date: 2026-07-21
tags: [cosmos-3-edge, nvidia-cosmos-3-edge, project]
aliases: ["Cosmos 3 Edge"]
---

# Cosmos 3 Edge

**Development line:** `project:nvidia-cosmos-3-edge` · thread `cosmos-3-edge`  
**Last event:** 2026-07-21 · 1 dated since 2026-07-21 · **Researched:** 2026-09-05 · confidence: high

## What it is

Cosmos 3 Edge is a 4B open-weight multimodal world model for robotics, autonomous-driving, and smart-space teams.

- Inputs: accepts text, images, video, and action trajectories.
- Outputs: produces text, images, video, and actions.
- Policy: provides a DROID manipulation variant.

The current generator release is image-to-video focused at 832×480, 121 frames, and 20 denoising steps. Use it for local physical-AI prototyping when its supported generator and reasoner paths match the deployment target.

## Development line

- **2026-07-21 — NVIDIA released Cosmos3-Edge on Hugging Face.** On 2026-07-21, NVIDIA's Hugging Face blog and model-repository links for Cosmos3-Edge were recorded. Together, they indicate an official public availability milestone for the project, making it material to its development history. The supplied links do not establish capability, license, or deployment details.

## What changed

- **2026-07-21** — Cosmos3-Edge and Cosmos3-Edge-Policy-DROID released on 2026-07-20 as 4B models under OpenMDW 1.1; the release added a compact multimodal base model and a DROID manipulation-policy variant.
- **2026-08-25** — NVIDIA updated Edge generator weights, defaults, examples, and benchmarks; the maintained generator recipe became image-to-video only, replacing earlier Edge text-to-image and text-to-video examples.

## How to use this

From 2026-07-21, practitioners tracking Cosmos 3 Edge should treat NVIDIA's Hugging Face model repository as an official evaluation and reference point, while verifying capabilities, licensing, and deployment requirements from the underlying materials before use.

1. Download a fresh local snapshot of the model before using the updated generator recipe.
  — <https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62>
2. For single-GPU reasoning, serve Cosmos3-Edge with vLLM and its OpenAI-compatible API; use vLLM 0.23.0 or later.
  — <https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md>
3. For generator inference, use the current image-to-video parameters: 832×480, 121 frames, 20 steps, guidance 6.0, and flow shift 12.0.
  — <https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62>

## Best practices

- Refresh local snapshots when tracking main; the August update changed weights, defaults, examples, and benchmarks.
  — <https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62>
- Do not load Edge through Cosmos3OmniForConditionalGeneration; its separate Transformers integration uses AutoModelForImageTextToText and Cosmos3EdgeForConditionalGeneration.
  — <https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md>
- Keep guardrails enabled unless an explicit deployment decision accepts the compliance responsibility; disabling them is server-wide.
  — <https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md>
- Bundle the vision tower in local exports for offline image or video reasoning; otherwise it may need to fetch components from the Hub.
  — <https://github.com/NVIDIA/cosmos-framework/blob/main/docs/inference.md>

## Superseded by this

- 2026-08-25 — Edge text-to-image and text-to-video generator examples are obsolete; the maintained Edge generator examples are image-to-video only.
- 2026-08-25 — Earlier Edge generator defaults are obsolete; use the refreshed checkpoint and 480p image-to-video recipe.

## Still unknown

- The current Cosmos Framework inference guide calls Edge a 2B model, while the NVIDIA model card and release announcement identify it as 4B. The 4B figure is used here because it is stated in the model card’s architecture section and release material; NVIDIA should reconcile the documentation.
- The response schema does not expose separate event_findings or new_events fields. The 2026-07-21 finding and the separate 2026-08-25 update are retained in what_changed.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/blog/nvidia/cosmos3edge | Introducing Cosmos 3 Edge | 2026-09-05 |
| https://huggingface.co/nvidia/Cosmos3-Edge | nvidia/Cosmos3-Edge model card | 2026-09-05 |
| https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62 | Cosmos3-Edge checkpoint and inference recipe update — August 2026 | 2026-09-05 |
| https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md | Cosmos 3 cookbooks | 2026-09-05 |
| https://github.com/NVIDIA/cosmos-framework/blob/main/docs/inference.md | Cosmos Framework inference guide | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:nvidia-cosmos-3-edge`, thread `cosmos-3-edge`, 1 dated events 2026-07-21 → 2026-07-21.
- **Practical note:** From 2026-07-21, practitioners tracking Cosmos 3 Edge should treat NVIDIA's Hugging Face model repository as an official evaluation and reference point, while verifying capabilities, licensing, and deployment requirements from the underlying materials before use.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.