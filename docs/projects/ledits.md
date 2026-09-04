---
title: LEDITS
category: projects
date: 2023-12-03
tags: [ledits, ledits-development, project]
aliases: ["LEDITS", "LEDITS++"]
---

# LEDITS

**Development line:** `project:ledits` · thread `ledits-development`  
**Last event:** 2023-12-03 · 2 dated since 2023-07-04 · **Researched:** 2026-09-04 · confidence: medium

## What it is

LEDITS is an image editing pipeline for modifying real images with semantic text prompts instead of a generic img2img pass.

- Inversion: inverts the input image before editing.
- Guidance: applies one or several concept prompts.
- Masking: uses implicit masks to confine changes to relevant regions.
- Integration: exposes Stable Diffusion and SDXL pipelines in Diffusers.

The original LEDITS Space is paused, and the Diffusers implementation does not guarantee perfect inversion. Use LEDITS++ locally for Stable Diffusion or SDXL semantic edits; use the authors’ implementation when inversion fidelity is the deliverable.

## Development line

- **2023-07-04 — LEDITS public demo and Hugging Face Space were linked.** On 2023-07-04, the LEDITS development thread linked a public web demo, the Hugging Face Space, and the repository for editing-images/ledits. These links do not establish release scope, model version, or capabilities.
- **2023-12-03 — LEDITS++ public demo and Hugging Face Space were linked.** On 2023-12-03, the thread linked a public LEDITS++ demo, the Hugging Face Space, and the repository for editing-images/leditsplusplus. It also linked back to LEDITS. These links do not confirm the exact technical relationship between LEDITS and LEDITS++.

## What changed

- 2023-07-04 — LEDITS combined Edit-Friendly DDPM inversion with SEGA semantic guidance for real-image editing on Stable Diffusion v1.5.
- 2023-12-03 — LEDITS++ introduced SDE-DPM-Solver++ inversion, per-edit implicit masking, and native simultaneous edits.

## How to use this

As of 2023-12-03, distinguish the original LEDITS public artifacts from the separately linked LEDITS++ artifacts and consult the matching Hugging Face Space or repository for the variant you intend to use.

1. Choose `LEditsPPPipelineStableDiffusion` for Stable Diffusion or `LEditsPPPipelineStableDiffusionXL` for SDXL, then load a compatible base checkpoint on CUDA.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
2. Call `invert(image=...)` for each new source image before invoking the editing pipeline; the edit always uses the last inversion.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
3. Use `source_prompt` only when guided inversion helps; an empty source prompt disables that guidance.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
4. Pass one or more `editing_prompt` values and align `reverse_editing_direction`, `edit_guidance_scale`, and `edit_threshold` with those prompts; direction controls whether each concept is increased or decreased.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
5. Inspect the inversion reconstruction and edit result; if exact inversion is required, use the authors’ repository rather than the Diffusers implementation.
  — <https://github.com/ml-research/ledits_pp>

## Best practices

- Use a seeded `torch.Generator` when comparing parameter changes so inversion is deterministic.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
- Treat `skip` as an edit-strength control: lower values make stronger changes to the input image.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
- Set `edit_threshold` to the edit footprint: use a smaller value for whole-image changes such as style transfer, and a value proportional to the affected region for local edits.
  — <https://arxiv.org/html/2311.16711v1>
- Keep the implicit intersection mask by default; add `user_mask` only when the automatic mask does not match the required region.
  — <https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp>
- For research reproduction or a hard reconstruction-fidelity requirement, prefer the authors’ implementation because its README states that Diffusers does not guarantee perfect inversion.
  — <https://github.com/ml-research/ledits_pp>

## Superseded by this

- 2023-07-04 — Treating the original LEDITS Gradio Space as an operational entry point is obsolete: the Space is paused; retain it as historical code rather than a dependable workflow.
- 2023-12-03 — Hosted-demo-only usage is obsolete: since 2024-03-15, Diffusers has shipped LEDITS++ pipeline APIs for Stable Diffusion and SDXL.
- 2023-12-03 — Treating the paper’s perfect-reconstruction result as a blanket library guarantee is obsolete: the authors state that the Diffusers implementation does not guarantee perfect inversion.

## Still unknown

- The primary sources do not explicitly label LEDITS++ as a versioned replacement for the 2023 LEDITS demo; they are treated here as closely related work, not a proven product-version lineage.
- The LEDITS++ Space is displayed as Running on Zero, but no image generation was executed during this check; that is not proof of dependable hosted availability.
- No current cross-model evaluation against newer general-purpose image editors was identified, so this does not claim that LEDITS++ remains best-in-class outside its Stable Diffusion and SDXL integration.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/html/2307.00522 | LEDITS: Real Image Editing with DDPM Inversion and Semantic Guidance | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/ledits | LEDITS Space | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/ledits/tree/main | LEDITS Space source tree | 2026-09-04 |
| https://arxiv.org/html/2311.16711v1 | LEDITS++: Limitless Image Editing using Text-to-Image Models, arXiv v1 | 2026-09-04 |
| https://leditsplusplus-project.static.hf.space/index.html | LEDITS++ project page | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/leditsplusplus | LEDITS++ Space | 2026-09-04 |
| https://huggingface.co/spaces/editing-images/leditsplusplus/tree/main | LEDITS++ Space source tree | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/ledits_pp | Diffusers LEDITS++ pipeline API | 2026-09-04 |
| https://github.com/ml-research/ledits_pp | ml-research/ledits_pp official implementation | 2026-09-04 |
| https://huggingface.co/papers/2311.16711 | Hugging Face paper page for LEDITS++ | 2026-09-04 |
| https://huggingface.co/posts/sayakpaul/117997091400234 | Diffusers 0.27.0 release post | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:ledits`, thread `ledits-development`, 2 dated events 2023-07-04 → 2023-12-03.
- **Practical note:** As of 2023-12-03, practitioners should distinguish the original LEDITS public artifacts from the separately linked LEDITS++ artifacts and consult the corresponding Hugging Face Space or repository for the variant they intend to use.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
