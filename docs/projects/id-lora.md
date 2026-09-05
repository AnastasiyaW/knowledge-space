---
title: ID-LoRA
category: projects
date: 2026-03-15
tags: [id-lora, id-lora-development, id_lora, project]
aliases: ["ID-LoRA"]
---

# ID-LoRA

**Development line:** `project:id-lora` · thread `id-lora-development`  
**Last event:** 2026-03-15 · 1 dated since 2026-03-15 · **Researched:** 2026-09-05 · confidence: high

## What it is

ID-LoRA is a zero-shot identity-conditioning method for LTX audio-video diffusion, built for creators who need talking-person video without training on each speaker.

- Voice identity transfer from reference audio
- Visual identity conditioning through a first-frame image
- Unified control of scene, spoken words, vocal style, and ambient sound in one prompt

## Development line

- **2026-03-15 — ID-LoRA public project resources linked.** On 2026-03-15, ID-LoRA published links to its project site, source repository, and model profiles. These links point readers to primary resources, but establish no specific release, version, capability, or license.

## What changed

2026-03-15 — ID-LoRA appeared as a research project for unified identity-conditioned audio-video generation on the LTX-2 backbone, linking project, code, and model destinations on 2026-03-15. The initial arXiv paper from 2026-03-10 introduces Identity-Driven In-Context LoRA, negative RoPE temporal positions for reference tokens, and identity guidance. It reports a 73% preference over Kling 2.6 Pro for voice similarity, a 24% cross-environment speaker-similarity gain, and about 3,000 training pairs on one GPU.

## How to use this

As of 2026-03-15, use the linked website and repository to explore ID-LoRA, but verify the version, license, and model availability before adoption.

1. Clone the official repository and install locked dependencies with `uv sync --frozen`; use Python 3.11+ and CUDA 12.x.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
2. Download required base-model components and the ID-LoRA checkpoint with the repository download script.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
3. Provide a first-frame image, a roughly five-second reference-audio file, and a prompt split into `[VISUAL]`, `[SPEECH]`, and `[SOUNDS]` sections.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
4. For current LTX-2.3 use, switch the uv workspace to `ID-LoRA-2.3/packages/*`, then run the two-stage HQ script with the LTX-2.3 checkpoint.
  — <https://github.com/ID-LoRA/ID-LoRA/blob/main/ID-LoRA-2.3/README.md>

## Best practices

- Use reference voice audio close to five seconds; shorter or longer clips can reduce speaker-identity transfer.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
- Put the exact desired transcript in `[SPEECH]`; place speaking style and environmental sound in `[SOUNDS]`, not in the visual description.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>
- Use two-stage HQ on LTX-2.3 for fidelity; choose one-stage with quantization when VRAM or turnaround time is the constraint.
  — <https://github.com/ID-LoRA/ID-LoRA/blob/main/ID-LoRA-2.3/README.md>
- Use only reference image and voice material for which you have authorization.
  — <https://github.com/ID-LoRA/ID-LoRA/tree/main>

## Superseded by this

- 2026-03-24 — native upstream ComfyUI support for LTX2 reference-audio identity transfer partly supersedes the separate ID-LoRA LTX-2.3 ComfyUI custom-node route; original weights need no conversion.

## Still unknown

- We could not retrieve the supplied hf.ru short link, so we do not treat it as evidence.
- Public sources provide no first-party publication date for the LTX-2.3 checkpoint release, so we do not assign it a dated development event.

## Sources

| source | title | read |
|---|---|---|
| https://id-lora.github.io/ | ID-LoRA: Identity-Driven Audio-Video Personalization | 2026-09-05 |
| https://github.com/ID-LoRA/ID-LoRA/tree/main | GitHub — ID-LoRA/ID-LoRA | 2026-09-05 |
| https://github.com/ID-LoRA/ID-LoRA/blob/main/ID-LoRA-2.3/README.md | GitHub — ID-LoRA 2.3: LTX-2.3 Support | 2026-09-05 |
| https://huggingface.co/AviadDahan/LTX-2.3-ID-LoRA-CelebVHQ-3K | Hugging Face — LTX-2.3-ID-LoRA-CelebVHQ-3K | 2026-09-05 |
| https://arxiv.org/abs/2603.10256 | ID-LoRA: Identity-Driven Audio-Video Personalization with In-Context LoRA | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:id-lora`, thread `id-lora-development`, 1 dated events 2026-03-15 → 2026-03-15.
- **Practical note:** As of 2026-03-15, practitioners can use the linked website and source repository as ID-LoRA discovery points, while independently verifying the applicable version, license, and model availability before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.