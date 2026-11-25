---
title: DisCO
category: projects
date: 2023-07-11
tags: [disco, disco-development, project]
aliases: ["DISCO", "DisCO", "DisCo"]
---

# DisCO

**Development line:** `project:disco` · thread `disco-development`  
**Last event:** 2023-07-11 · 3 dated since 2022-10-20 · **Researched:** 2026-09-04 · confidence: medium

## What it is

DisCO covers three task-specific research implementations for image practitioners rather than one deployable tool.

- DISCO colorizes grayscale images through global color anchors.
- Portrait DisCO corrects close-up facial perspective through 3D-GAN inversion.
- Dance DisCo combines reference foreground, background, and target pose to generate human images or video.

## Development line

- **2022-10-20 — DisCO project page and public demo appeared.** Disentangled Image Colorization via Global Anchors established a SIGGRAPH Asia 2022 colorization workflow with code, checkpoints, and a hosted demo.
- **2023-02-26 — Portrait DisCO was presented through a project site.** Portrait Distortion Correction with Perspective-Aware 3D GANs appeared as a separate project for correcting close-range portrait distortion. The repository records IJCV acceptance on 2024-01-03 and an inversion-code release on 2025-02-04, while the full system and Hugging Face demo remain TODO.
- **2023-07-11 — DisCo dance project was published with code and a live demo.** Disentangled Control for Referring Human Dance Generation in Real World appeared as a separate pose-controlled dance-generation project. The repository records a temporal-module update on 2023-11-30, CVPR 2024 acceptance on 2024-04-08, and IDOL as a DisCo enhancement on 2024-07-15.

## What changed

- 2022-10-20 — DISCO: Disentangled Image Colorization via Global Anchors established a SIGGRAPH Asia 2022 colorization workflow with code, checkpoints, and a hosted demo.
- 2023-02-26 — DisCO: Portrait Distortion Correction with Perspective-Aware 3D GANs appeared as a separate project for correcting close-range portrait distortion. The repository records IJCV acceptance on 2024-01-03 and an inversion-code release on 2025-02-04, while the full system and Hugging Face demo remain TODO.
- 2023-07-11 — DisCo: Disentangled Control for Referring Human Dance Generation in Real World appeared as a separate pose-controlled dance-generation project. The repository records a temporal-module update on 2023-11-30, CVPR 2024 acceptance on 2024-04-08, and IDOL as a DisCo enhancement on 2024-07-15.

These dates do not form one development line. The three projects have different authors, tasks, models, repositories, and release paths.

## How to use this

As of 2023-07-11, check task-specific public project pages and validate capabilities through linked code or a live demo, rather than treating the name as one unchanged tool.

1. For grayscale colorization, clone the repository, create its documented Python 3.8 / PyTorch / CUDA environment, download a checkpoint into `checkpoints`, place images in `data`, then run the supplied inference script.
  — <https://github.com/MenghanXia/DisentangledColorization>
2. For portrait perspective correction, initialize EG3D and Deep3DFaceRecon, download the FFHQ checkpoint, create the supplied Conda environment, set input and model paths in `example_configs/config.py`, run preprocessing, then run the correction script.
  — <https://github.com/lightChaserX/DisCO>
3. For dance image editing, download the fine-tuning checkpoint and SD Image Variations dependency, set their paths in the supplied Jupyter notebook, and launch it on a local GPU.
  — <https://github.com/Wangt-CN/DisCo>

## Best practices

- For DISCO colorization, retain the default 256×256 inference unless you have validated another setting: the authors mark original-resolution `--no_resize` output as unstable. Use absolute paths and fix `--seed` when comparing results.
  — <https://github.com/MenghanXia/DisentangledColorization>
- For Portrait DisCO, validate the EG3D and Deep3DFaceRecon dependency chain before processing images, and treat the released inversion code as narrower than a complete public product because the full system and hosted demo are still listed as TODO.
  — <https://github.com/lightChaserX/DisCO>
- For Dance DisCo, use the documented local notebook for an initial image workflow; for human-specific fine-tuning, prepare masks and skeletons with Grounded-SAM and OpenPose, then tune learning rate and U-Net unfreezing first.
  — <https://github.com/Wangt-CN/DisCo>

## Superseded by this

- 2022-10-20 — using the hosted DISCO colorization Space as the default workflow is obsolete because its page currently reports a runtime error. Use the local repository path instead.
- 2023-02-26 — the earlier expectation of a future Portrait DisCO code release is superseded by the 2025-02-04 inversion-code release. Do not mistake it for a full-system or hosted-demo release.
- 2023-07-11 — treating the linked Gradio endpoint as a verified current Dance DisCo workflow is obsolete because it could not be fetched on 2026-09-04. Use the repository’s local workflow until a hosted endpoint is independently confirmed.
- 2023-07-11 — treating all occurrences of “DisCO” as versions of one project is obsolete. The three records are independent projects sharing a name.

## Still unknown

- The `disco` key combines three independent projects. No primary source establishes a common maintainer, release train, API, model weight, or successor relationship.
- The current Dance DisCo Gradio endpoint could not be fetched during research; this does not prove permanent retirement.
- We did not execute any repository or download checkpoints, so compatibility with current CUDA, PyTorch, and dependency versions is unverified.

## Sources

| source | title | read |
|---|---|---|
| https://menghanxia.github.io/projects/disco.html | DISCO: Disentangled Image Colorization via Global Anchors | 2026-09-04 |
| https://huggingface.co/spaces/menghanxia/disco | Disco - a Hugging Face Space by menghanxia | 2026-09-04 |
| https://github.com/MenghanXia/DisentangledColorization | MenghanXia/DisentangledColorization | 2026-09-04 |
| https://portrait-disco.github.io/ | DisCO: Portrait Distortion Correction with Perspective-Aware 3D GANs | 2026-09-04 |
| https://github.com/lightChaserX/DisCO | lightChaserX/DisCO | 2026-09-04 |
| https://disco-dance.github.io/ | DisCo: Disentangled Control for Referring Human Dance Generation in Real World | 2026-09-04 |
| https://github.com/Wangt-CN/DisCo | Wangt-CN/DisCo | 2026-09-04 |
| https://5e42cfd7d54823fd8a.gradio.live/ | DisCo Gradio demo endpoint | 2026-09-04 |
| https://7b2faca424cdb265fc.gradio.live/ | DisCo project-page Gradio demo endpoint | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:disco`, thread `disco-development`, 3 dated events 2022-10-20 → 2023-07-11.
- **Practical note:** As of 2023-07-11, practitioners following the DisCO line should look for task-specific public project pages and validate a claimed capability through its linked code or live demo, rather than treating the name alone as one unchanged tool.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
