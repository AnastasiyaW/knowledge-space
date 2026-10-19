---
title: "Fizgig: fizgig-v6-0-1-refmod-support — Fizgig V6 0 1 Refmod Support"
category: "projects"
date: 2026-10-17
tags: ["fizgig", "fizgig-v6-0-1-refmod-support", "project"]
aliases: ["Fizgig: fizgig-v6-0-1-refmod-support"]
---

# Fizgig: fizgig-v6-0-1-refmod-support — Fizgig V6 0 1 Refmod Support

**Development line:** project:fizgig · thread fizgig-v6-0-1-refmod-support  
**Last event:** 2026-10-17 · 1 dated since 2026-10-17 · **Researched:** 2026-10-19 · confidence: medium

## What it is

Fizgig is an open-source suite for LoRA training and model fine-tuning on local and cloud GPUs. It trains character LoRA adapters with an isolation method, so each identity stays distinct when several people share one image.

- Multi-identity training: several characters in a single adapter file
- Differential Output Preservation: adapted from AI-Toolkit foundations
- Fused-token class decoupling: separates unique subject triggers from base class words
- Synthetic negative pairs: protect strangers in the background
- Base model support: works with flow-matching and diffusion architectures

It needs at least two distinct subjects during training. With that in place, identities do not cross-contaminate, and there is no manual inpainting after generation.

## Development line

- **2026-10-17 — Fizgig releases LoRA Isolation for multi-identity LoRA training.** On 2026-10-17 a Fizgig developer announced LoRA Isolation. It trains two identities into one LoRA and keeps other people in the image distinct. In a reported test on Krea 2, stranger face spread dropped from 48 of 50 to 0 of 50. The announcement links release notes for v8.4.0 and the GitHub repository.
  - Fizgig developer Peter Neill (@shootthesound) described how LoRA Isolation is built. It combines Differential Output Preservation (DOP) adapted from Ostris AI-Toolkit, fused-token class decoupling and synthetic stranger negative pairs. Across 50 test generations on Krea 2 he showed zero stranger face bleeding. (2026-10-17) — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
  - Release v8.4.0 adds multi-subject folder setup to the Subjects card on the Training tab. It automates trigger-class token fusion and the negative-pair training setup. (2026-10-17) — <https://github.com/shootthesound/Fizgig/releases/tag/v8.4.0>
  - A video walkthrough sets up two distinct subject folders on the Subjects card. It formats captions with unique triggers and class descriptors, so fused tokens are generated automatically. (2026-10-17) — <https://youtu.be/CNh4sN5vN_8>

## What changed

Work moved from basic character fine-tuning to multi-subject identity separation, built on differential output preservation and negative-pair training. Automated caption-to-token fusion came next, along with support for newer open-weights image backends.

## How to use this

1. Put datasets for at least two distinct identities in separate folders on the Subjects card in the Fizgig Training tab.
  — <https://github.com/shootthesound/Fizgig/releases/tag/v8.4.0>
2. Start each caption with the unique trigger token, then a comma, then the class descriptor (e.g., 'zwxem, a woman smiling'). Fizgig uses this to build internal fused tokens.
  — <https://github.com/shootthesound/Fizgig>
3. Turn on LoRA Isolation in the training configuration. It combines Differential Output Preservation with automatic synthetic stranger image pairing.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
4. At inference, use the fused trigger token and describe the other subjects in the scene. Identity boundaries hold and faces do not bleed.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## Best practices

- Train at least two distinct characters together, even if you want only one. This forces the network to separate identity tokens from base human class tokens.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
- Leave the trigger token out when prompting background characters or crowds. The base model then renders its default varied faces without leakage.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>
- When pairing multi-person negative composites in training, write captions in causal order, with stranger descriptors first.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## What practitioners say

- Practitioners report that multi-identity isolation fixes a common problem: character LoRAs overwriting background faces and secondary characters in group scenes. (2026-10-17)
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## Superseded by this

- The earlier advice was single-subject LoRA training with generic class tokens like 'man' or 'woman'. In multi-person prompts it caused heavy face bleeding onto strangers.
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/>

## Still unknown

- The thread is named fizgig-v6-0-1-refmod-support, but the event and release notes we reviewed cover v8.4.0. The release date and implementation details of version 6.0.1 refmod support could not be determined from the available search results.

## Sources

| source | title | read |
|---|---|---|
| https://www.reddit.com/r/StableDiffusion/comments/1x8aplh/fizgig_lora_isolation_a_new_process_for_more/ | Fizgig LoRA Isolation: A new process for multi-identity training without face bleeding | 2026-10-19 |
| https://github.com/shootthesound/Fizgig/releases/tag/v8.4.0 | Release v8.4.0: LoRA Isolation Support · shootthesound/Fizgig | 2026-10-19 |
| https://github.com/shootthesound/Fizgig | shootthesound/Fizgig: LoRA and fine-tuning studio | 2026-10-19 |
| https://youtu.be/CNh4sN5vN_8 | Fizgig LoRA Isolation Walkthrough and Multi-Subject Workflow | 2026-10-19 |
| https://youtu.be/8uW5NdL5b20 | Fizgig LoRA Training Tutorial: Preventing Face Bleed | 2026-10-19 |

## Agent brief {#agent-brief}

- **Subject:** project:fizgig, thread fizgig-v6-0-1-refmod-support, 1 dated events 2026-10-17 → 2026-10-17.
- **Practical note:** use the sourced usage and practice sections above, with their limits.
- **Confidence:** medium. The dated supersedes above decide what is obsolete.
