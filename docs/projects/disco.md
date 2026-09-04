---
title: DisCO — DisCO development
category: projects
tags: [disco, disco-development, project]
aliases: ["DISCO", "DisCO", "DisCo"]
---

# DisCO — DisCO development

**Development line:** `project:disco` · thread `disco-development`  
**Events:** 3 dated, 2022-10-20 → 2023-07-11 · **Researched:** 2026-09-04 · confidence: medium

## What it is

DisCO — not one deployable tool, but three task-specific research implementations for image practitioners. - DISCO colorizes grayscale images through global color anchors. - Portrait DisCO corrects close-up facial perspective through 3D-GAN inversion. - Dance DisCo combines reference foreground, background, and target pose to generate human images or video. Limit: the colorization Space reports a runtime error; Portrait DisCO still lists its full system and Hugging Face demo as TODO; hosted dance-demo availability is unverified. Verdict: select and pin the repository by task; none is a successor of the others.

## Development line

- **2022-10-20 — DisCO project page and public demo appeared.** On 2022-10-20, a DisCO project page was linked alongside a public Hugging Face Space. This marks an externally accessible introduction of the project and a way to try it directly.
- **2023-02-26 — Portrait DisCO was presented through a project site.** On 2023-02-26, a dedicated Portrait DisCO project site was linked. It is a distinct public development step in the DisCO line, focused by its presentation on portrait-oriented work.
- **2023-07-11 — DisCo dance project was published with code and a live demo.** On 2023-07-11, a DisCo dance project site was linked together with a GitHub repository and a live Gradio endpoint. This is a material public release step because it paired project documentation with source access and an executable demonstration.

## What changed

2022-10-20 — DISCO: Disentangled Image Colorization via Global Anchors established a SIGGRAPH Asia 2022 colorization workflow with code, checkpoints, and a hosted demo. 2023-02-26 — DisCO: Portrait Distortion Correction with Perspective-Aware 3D GANs appeared as a separate project for correcting close-range portrait distortion. Found today: its repository records IJCV acceptance on 2024-01-03 and an inversion-code release on 2025-02-04, while the full system and Hugging Face demo remain TODO. 2023-07-11 — DisCo: Disentangled Control for Referring Human Dance Generation in Real World appeared as a separate pose-controlled dance-generation project. Found today: its repository records a temporal-module update on 2023-11-30, CVPR 2024 acceptance on 2024-04-08, and IDOL as a DisCo enhancement on 2024-07-15. These dates are not one development line: the projects have different authors, tasks, models, repositories, and release paths.

## How to use this

As of 2023-07-11, practitioners following the DisCO line should look for task-specific public project pages and validate a claimed capability through its linked code or live demo, rather than treating the name alone as one unchanged tool.

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

- 2022-10-20 — using the hosted DISCO colorization Space as the default workflow is obsolete: its page currently reports a runtime error; use the local repository path instead.
- 2023-02-26 — the earlier expectation of a future Portrait DisCO code release is superseded by the 2025-02-04 inversion-code release, but it must not be mistaken for a full-system or hosted-demo release.
- 2023-07-11 — treating the linked Gradio endpoint as a verified current Dance DisCo workflow is obsolete: it could not be fetched on 2026-09-04; use the repository’s local workflow until a hosted endpoint is independently confirmed.
- 2023-07-11 — treating all occurrences of “DisCO” as versions of one project is obsolete; the three records are independent projects sharing a name.

## Still unknown

- The `disco` key combines three independent projects. No primary source establishes a common maintainer, release train, API, model weight, or successor relationship.
- The current Dance DisCo Gradio endpoint could not be fetched during research; this does not prove permanent retirement.
- I did not execute any repository or download checkpoints, so compatibility with current CUDA, PyTorch, and dependency versions is unverified.

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
