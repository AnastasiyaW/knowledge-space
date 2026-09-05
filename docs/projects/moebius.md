---
title: Moebius — Public availability
category: projects
date: 2026-06-20
tags: [moebius, project, public-availability]
aliases: ["Moebius"]
---

# Moebius — Public availability

**Development line:** `project:moebius` · thread `public-availability`  
**Last event:** 2026-06-20 · 1 dated since 2026-06-20 · **Researched:** 2026-09-05 · confidence: high

## What it is

Moebius is an open image-inpainting framework for developers who supply an image and matching mask.
- Pretrained, Places2, CelebA-HQ, and FFHQ checkpoints for domain-specific fills.
- Repository inference path for scripted local runs.
- Hugging Face Diffusers loading path for pipeline integration.

It runs with 226M parameters at 26.01 ms per step on the authors’ tested GPU. It works as a specialist for masked fills and object removal, not a hosted general-purpose generation service.

## Development line

- **2026-06-20 — Moebius project resources were shared publicly.** On 2026-06-20, a message about Moebius linked the project website, its GitHub repository, and its Hugging Face page. We treat this as a material public-availability milestone because it directs readers to the project's public-facing resources, while the exact release or capability cannot be established from the supplied links alone.

## What changed

2026-06-20 — Moebius was available as a project page, public repository, and Hugging Face model; first-party material identifies it as a 0.22B image-inpainting specialist.

Event finding for 2026-06-20 — the June 18, 2026 repository announcement says the scope was training code, inference code, and public weights, with checkpoints for pretrained, Places2, CelebA-HQ, and FFHQ variants; it was not a packaged GitHub release.

New events: 2026-06-16 — the repository was first submitted publicly, according to its dated project news. 2026-06-17 — arXiv v1 (2606.19195) was submitted, documenting the LλMI backbone and latent-space multi-granularity distillation. 2026-06-18 — the authors announced ECCV 2026 acceptance, released the preprint, code, and weights. 2026-06-19 — the project reported reaching Hugging Face’s daily number-one ranking; this is visibility evidence, not a model revision. 2026-06-25 — the project reported a weekly Hugging Face rank of 4/105; this is visibility evidence, not a model revision.

## How to use this

As of 2026-06-20, practitioners should consult Moebius's project, code, and Hugging Face pages as the starting point for evaluation; this evidence alone does not establish a specific version, capability, license, or deployment recommendation.

1. Clone the repository, create the documented environment, and install its pinned requirements before using the repository workflow.
  — <https://github.com/hustvl/Moebius>
2. Download the VAE plus the pretrained or task-specific checkpoint, keeping the documented weight directory layout.
  — <https://github.com/hustvl/Moebius>
3. Put each source image and its mask in separate directories with matching filenames, then run infer.infer_moebius with the selected model config, checkpoint, input directories, output directory, CFG value, batch size, and worker count.
  — <https://github.com/hustvl/Moebius>
4. For the Hub path, install diffusers, transformers, and accelerate, then load hustvl/Moebius through DiffusionPipeline; validate its output against the repository path before adopting it for masked editing.
  — <https://huggingface.co/hustvl/Moebius>

## Best practices

- Use the repository’s image-and-mask inference path for inpainting; its file layout and command explicitly encode the mask-based workflow.
  — <https://github.com/hustvl/Moebius>
- Choose a checkpoint aligned to the image domain—Places2 for natural scenes, CelebA-HQ or FFHQ for portraits—and do not treat benchmark claims as proof for an unrelated domain.
  — <https://hustvl.github.io/Moebius/>
- Pin the repository’s listed Torch, Diffusers, Transformers, and flash-linear-attention versions when reproducing its workflow; the Hub page presents a separate generic Diffusers example.
  — <https://github.com/hustvl/Moebius>
- Treat the reported 26.01 ms-per-step and over-15x speedup as authors’ benchmark claims, not a deployment latency guarantee.
  — <https://arxiv.org/abs/2606.19195>

## Superseded by this

- 2026-06-18 — guidance that Moebius was only a paper or project page is obsolete: first-party materials say code and weights were released.
- 2026-09-05 — guidance to install a GitHub release artifact is unsupported: the repository’s releases page shows no releases. Use source checkout and Hub checkpoints instead.

## Still unknown

- The Hugging Face page labels the model license MIT, while the repository README says Apache-2.0 for code and pretrained weights. Confirm the intended license with the maintainers before a commercial deployment.
- The supplied schema has no event_findings or new_events fields; their required content is retained in what_changed.
- No independent hardware reproduction was found for the reported 26.01 ms-per-step or over-15x speed claim.
- The generic Hugging Face Diffusers example appears prompt-only, while the repository documents image-and-mask inpainting; the Hub pipeline’s exact masking interface was not independently verified.

## Sources

| source | title | read |
|---|---|---|
| https://hustvl.github.io/Moebius/ | Moebius Project Page | 2026-09-05 |
| https://github.com/hustvl/Moebius | hustvl/Moebius repository | 2026-09-05 |
| https://huggingface.co/hustvl/Moebius | hustvl/Moebius model card | 2026-09-05 |
| https://arxiv.org/abs/2606.19195 | Moebius: 0.2B Lightweight Image Inpainting Framework with 10B-Level Performance | 2026-09-05 |
| https://github.com/hustvl/Moebius/releases | Moebius GitHub releases | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:moebius`, thread `public-availability`, 1 dated events 2026-06-20 → 2026-06-20.
- **Practical note:** As of 2026-06-20, practitioners should consult Moebius's project, code, and Hugging Face pages as the starting point for evaluation; this evidence alone does not establish a specific version, capability, license, or deployment recommendation.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
