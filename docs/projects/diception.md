---
title: DICEPTION — DICEPTION development
category: projects
tags: [diception, diception-development, project]
aliases: ["DICEPTION"]
---

# DICEPTION — DICEPTION development

**Development line:** `project:diception` · thread `diception-development`  
**Events:** 2 dated, 2025-04-21 → 2025-10-02 · **Researched:** 2026-09-04 · confidence: medium

## What it is

DICEPTION is an SD3-based diffusion model for practitioners who want one local model for visual-perception outputs. - Monocular depth and surface normals. - Pose estimation. - Entity, semantic, and point-prompted segmentation. Measure/limit: the v1 checkpoint is 4.07 GB; the released script uses CUDA and bfloat16, resizes inputs to 768×768, and has no published VRAM target. Verdict: use it for experimental local multi-task inference, not as a hosted service or documented training stack.

## Development line

- **2025-04-21 — DICEPTION project resources were publicly linked.** On 2025-04-21, a DICEPTION message linked the project website, its GitHub repository, and a Hugging Face Spaces demo. This establishes a dated public entry point for the project, its source code, and an interactive demonstration.
- **2025-10-02 — DICEPTION Hugging Face repository was added to the public record.** On 2025-10-02, a DICEPTION message linked a Hugging Face repository named DICEPTION alongside the earlier project post. This adds a distinct model-repository access point to the project's dated public trail, although the linked evidence alone does not establish which files changed or whether this was a first release.

## What changed

DICEPTION development: - 2025-02-24/25 — found today: arXiv v1/v2 established the diffusion-based generalist-perception method. - 2025-04-21 — the recorded entry points were the project page, repository, and web demo. The maintainers later date usable inference code and weights to September, so this was not yet the current local-install workflow. - 2025-09-19 — found today: accepted as a NeurIPS 2025 Spotlight. - 2025-09-21 — found today: the maintainers released inference code and the v1 model. - 2025-10-02 — the recorded source set added the Hugging Face model tree, which currently contains the same-paper DICEPTION_v1.pth checkpoint. - 2026-09-04 — found today: the hosted demo reports RUNTIME_ERROR; local code plus weights is the current usable route.

## How to use this

From 2025-10-02, practitioners should consult the DICEPTION project site, source repository, demo, and linked Hugging Face repository together when evaluating the project or locating its public artifacts.

1. Clone the repository, create its Python 3.10 Conda environment, and install requirements.
  — <https://github.com/aim-uofa/Diception>
2. Download Stable Diffusion 3 Medium in Diffusers format and DICEPTION_v1.pth, then set --pretrained_model_path and --diception_path to those local directories.
  — <https://huggingface.co/Canyu/DICEPTION/tree/main>
3. Run inference.py with an input image and an exact task token such as [[image2depth]], [[image2normal]], [[image2pose]], [[image2entity]], or [[image2segmentation]].
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
4. For semantic segmentation, append the COCO category to [[image2semantic]]; for interactive segmentation, pass normalized y,x points, with at most five points.
  — <https://github.com/aim-uofa/Diception>
5. For datasets, use batch_inference.py with the supplied JSON shape; use --save_npy when depth or normal values are needed rather than only a visualization.
  — <https://github.com/aim-uofa/Diception>

## Best practices

- Provision a CUDA-capable bfloat16 environment before trying the released script: it explicitly moves the model to CUDA/bfloat16 and loads the checkpoint onto CUDA.
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
- Start with the maintainers’ 28 inference steps and guidance scale 2.0 for general quality; use 1 step and guidance 1.0 only when speed matters, especially for depth or normals.
  — <https://github.com/aim-uofa/Diception>
- Validate at the task’s native evaluation format: single-image inference always works at 768×768 and saves a side-by-side input/output image, not an untouched native-resolution prediction.
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
- Download the v1 .pth only from the named model repository and treat it as a PyTorch pickle artifact; the Hub flags pickle imports and the code uses torch.load.
  — <https://huggingface.co/Canyu/DICEPTION/tree/main>
- Do not make the hosted Space a dependency of a workflow until it is repaired; use the released local code and weights instead.
  — <https://huggingface.co/spaces/Canyu/Diception-Demo>
- For commercial use, follow the project’s instruction to contact the stated maintainer rather than assuming the academic-use note covers deployment.
  — <https://github.com/aim-uofa/Diception>

## Superseded by this

- 2025-04-21 research/demo-only access: superseded on 2025-09-21 by released local inference code and v1 weights.
- 2025-04-21 demo-first access: obsolete as a current workflow on 2026-09-04 because the hosted Hugging Face Space reports RUNTIME_ERROR.

## Still unknown

- No source text was supplied, so the exact wording and intent of the 2025-04-21 and 2025-10-02 items can only be reconstructed from their dated link sets.
- The Chinese research check found secondary translated summaries but no first-party Chinese operating documentation or independent Chinese execution report; none was used as practical evidence.
- No current local end-to-end run, VRAM measurement, or supported-hardware matrix was found. CUDA/bfloat16 code is implementation evidence, not a passing runtime receipt.
- The current README still lists training and few-shot fine-tuning code as planned, so the paper’s 50-image and 1%-parameter adaptation result is not a runnable public workflow.

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
