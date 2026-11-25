---
title: DICEPTION
category: projects
date: 2025-10-02
tags: [diception, diception-development, project]
aliases: ["DICEPTION"]
---

# DICEPTION

**Development line:** `project:diception` · thread `diception-development`  
**Last event:** 2025-10-02 · 2 dated since 2025-04-21 · **Researched:** 2026-09-04 · confidence: medium

## What it is

DICEPTION is an SD3-based diffusion model for practitioners who want one local model for visual-perception outputs.

- Monocular depth and surface normals.
- Pose estimation.
- Entity, semantic, and point-prompted segmentation.

## Development line

- **2025-04-21 — DICEPTION project resources were publicly linked.** On 2025-04-21, links appeared for the project website, its GitHub repository, and a Hugging Face Spaces demo. They established a dated public entry point for the project, its source code, and an interactive demonstration.
- **2025-10-02 — DICEPTION Hugging Face repository was added.** On 2025-10-02, links added the DICEPTION Hugging Face repository alongside the earlier project post. This added a distinct model-repository access point to the dated public trail, without showing which files changed or whether this was a first release.

## What changed

DICEPTION development:

- 2025-02-24/25 — arXiv v1/v2 established the diffusion-based generalist-perception method.
- 2025-04-21 — public entry points were the project page, repository, and web demo. Usable inference code and weights came later in September, so local install did not work yet.
- 2025-09-19 — accepted as a NeurIPS 2025 Spotlight.
- 2025-09-21 — maintainers released inference code and the v1 model.
- 2025-10-02 — files added the Hugging Face model tree with the DICEPTION_v1.pth checkpoint.
- 2026-09-04 — the hosted demo reports RUNTIME_ERROR, so local code plus weights is the usable route.

## How to use this

From 2025-10-02, consult the DICEPTION project site, repository, demo, and Hugging Face repository together when evaluating the project.

1. Clone the repository, create its Python 3.10 Conda environment, and install requirements.
  — <https://github.com/aim-uofa/Diception>
2. Download Stable Diffusion 3 Medium in Diffusers format and DICEPTION_v1.pth, then set --pretrained_model_path and --diception_path to those local directories.
  — <https://huggingface.co/Canyu/DICEPTION/tree/main>
3. Run inference.py with an input image and an exact task token such as `[[image2depth]]`, `[[image2normal]]`, `[[image2pose]]`, `[[image2entity]]`, or `[[image2segmentation]]`.
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
4. For semantic segmentation, append the COCO category to `[[image2semantic]]`; for interactive segmentation, pass normalized y,x points, with at most five points.
  — <https://github.com/aim-uofa/Diception>
5. For datasets, use batch_inference.py with the supplied JSON shape; use --save_npy when depth or normal values are needed rather than only a visualization.
  — <https://github.com/aim-uofa/Diception>

## Best practices

- Provision a CUDA-capable bfloat16 environment before running the released script: it explicitly moves the model to CUDA/bfloat16 and loads the checkpoint onto CUDA.
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
- Start with the maintainers' 28 inference steps and guidance scale 2.0 for general quality; use 1 step and guidance 1.0 only when speed matters, especially for depth or normals.
  — <https://github.com/aim-uofa/Diception>
- Validate at the task's native evaluation format: single-image inference always works at 768×768 and saves a side-by-side input/output image, not an untouched native-resolution prediction.
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
- Download the v1 .pth only from the named model repository and treat it as a PyTorch pickle artifact; the Hub flags pickle imports and the code uses torch.load.
  — <https://huggingface.co/Canyu/DICEPTION/tree/main>
- Do not make the hosted Space a dependency of a workflow until it is repaired; use the released local code and weights instead.
  — <https://huggingface.co/spaces/Canyu/Diception-Demo>
- For commercial use, follow the project's instruction to contact the stated maintainer rather than assuming the academic-use note covers deployment.
  — <https://github.com/aim-uofa/Diception>

## Superseded by this

- 2025-04-21 research/demo-only access: superseded on 2025-09-21 by released local inference code and v1 weights.
- 2025-04-21 demo-first access: obsolete as a current workflow on 2026-09-04 because the hosted Hugging Face Space reports RUNTIME_ERROR.

## Still unknown

- We have no original post text for the 2025-04-21 and 2025-10-02 items, so their wording can only be reconstructed from dated links.
- We found secondary translated summaries but no first-party Chinese operating documentation or independent Chinese execution report; none was used as practical evidence.
- We found no current local end-to-end run, VRAM measurement, or supported-hardware matrix. CUDA/bfloat16 code is implementation evidence, not a passing runtime receipt.
- The current README still lists training and few-shot fine-tuning code as planned, so the paper's 50-image and 1%-parameter adaptation result is not a runnable public workflow.

## Sources

| source | title | read |
|---|---|---|
| https://aim-uofa.github.io/Diception/ | DICEPTION project page | 2026-09-04 |
| https://github.com/aim-uofa/Diception | aim-uofa/Diception README and release notes | 2026-09-04 |
| https://github.com/aim-uofa/Diception/blob/main/inference.py | DICEPTION single-image inference script | 2026-09-04 |
| https://github.com/aim-uofa/Diception/blob/main/models/Renderer.py | DICEPTION renderer and diffusion execution path | 2026-09-04 |
| https://huggingface.co/Canyu/DICEPTION/tree/main | Canyu/DICEPTION model files | 2026-09-04 |
| https://huggingface.co/spaces/Canyu/Diception-Demo | Diception Demo | 2026-09-04 |
| https://arxiv.org/abs/2502.17157 | DICEPTION: A Generalist Diffusion Model for Visual Perceptual Tasks | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:diception`, thread `diception-development`, 2 dated events 2025-04-21 → 2025-10-02.
- **Practical note:** From 2025-10-02, practitioners should consult the DICEPTION project site, source repository, demo, and linked Hugging Face repository together when evaluating the project or locating its public artifacts.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.