---
title: HY-WU — Tencent Hunyuan
category: projects
date: 2026-03-06
tags: [hy-wu, project, tencent-hunyuan]
aliases: ["HY-WU"]
---

# HY-WU — Tencent Hunyuan

**Development line:** `project:hy-wu` · thread `tencent-hunyuan`  
**Last event:** 2026-03-06 · 1 dated since 2026-03-06 · **Researched:** 2026-09-06 · confidence: high

## What it is

HY-WU — a local research stack for teams with multi-GPU hardware that need image-to-image edits without training an edit-specific LoRA.

- LoRA generator: creates instance-conditioned LoRA updates and injects them into a frozen backbone.
- Paired model: runs `tencent/HY-WU` alongside `tencent/HunyuanImage-3.0-Instruct`.
- Edit tasks: demonstrates clothing fusion, outfit transfer, face-identity transfer, virtual try-on, and texture synthesis.

## Development line

- **2026-03-06 — HY-WU official project resources became available.** On 2026-03-06, official HY-WU resources went live through a project site, a GitHub repository, and a Hugging Face page. We have no confirmed details on the release version, announcement, or full capabilities.

## What changed

2026-03-06 — HY-WU opened its inference code and model weights for inference with HunyuanImage-3.0-Instruct. 2026-03-07 — the HY-WU technical report appeared on arXiv as v1 as a research paper, not a separate checkpoint. 2026-03-18 — GitHub records commit `a9f4206`, titled “add configurable image size”; current inference accepts `image_size`. 2026-06-18 — arXiv v2 revised the technical report; we found no newer code or weight release.

## How to use this

We can evaluate HY-WU from 2026-03-06 using its project site, source repository, and Hugging Face page. We do not have enough evidence to recommend it for production tasks.

1. Read the community license first and confirm that the intended territory and downstream use are covered.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/LICENSE>
2. Provision the documented multi-GPU capacity before setup: at least 8×40 GB or 4×80 GB VRAM.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
3. Clone `Tencent-Hunyuan/HY-WU`, enter the directory, and install `requirements.txt`.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
4. Run `python infer.py`, or create `WUPipeline` with `tencent/HunyuanImage-3.0-Instruct` as the base model and `tencent/HY-WU` as the parameter generator.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py>
5. Supply a base image, one or more reference images, and an instruction that states both the desired transfer and what must remain unchanged; save the generated image.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py>
6. For the optional local UI, install Gradio and run `python gradio/app.py`.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>

## Best practices

- Start with the upstream matched model pair rather than substituting an unlisted backbone; distilled and other-backbone checkpoints remain unchecked in the project plan.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
- Reproduce the supplied two-image recipe with its explicit preservation instruction, 50 diffusion steps, and fixed seed before changing generation settings.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py>
- Treat GPU capacity as a preflight gate: the upstream documentation explicitly requires multi-GPU inference for the base model.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
- Do not hard-code the README's stated Gradio port: the current app binds port 7860 while the README says 7680; inspect the running endpoint.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/gradio/app.py>
- Do not use the work or its outputs to improve a non-Hunyuan model, and do not operate it in territories excluded by the stated license.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/LICENSE>

## Superseded by this

- 2026-03-07 — arXiv v1 was superseded by arXiv v2, revised 2026-06-18; this does not establish a newer model or weight release.

## Still unknown

- The official Hugging Face model card currently says “March 6, 2025,” which conflicts with the March 6, 2026 license date and repository history; it appears to be a documentation error rather than a separate 2025 launch.
- No independently verified successful local run, throughput measurement, consumer-GPU workaround, or distilled checkpoint was found.
- No later first-party model-weight release was established; arXiv v2 is a report revision, not proof of an implementation update.
- No accessible dated Simplified-Chinese Tencent corporate announcement for the project release was found.

## Sources

| source | title | read |
|---|---|---|
| https://tencent-hy-wu.github.io/ | HY-WU (Part I): An Extensible Functional Neural Memory Framework and An Instantiation in Text-Guided Image Editing | 2026-09-06 |
| https://github.com/Tencent-Hunyuan/HY-WU | Tencent-Hunyuan/HY-WU | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md | HY-WU README | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/LICENSE | Tencent Hunyuan Community License Agreement for HY-WU | 2026-09-06 |
| https://huggingface.co/tencent/HY-WU | tencent/HY-WU model card | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py | HY-WU inference example | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/gradio/app.py | HY-WU Gradio application | 2026-09-06 |
| https://github.com/Tencent-Hunyuan/HY-WU/commits/main | HY-WU commit history | 2026-09-06 |
| https://arxiv.org/abs/2603.07236v2 | HY-WU (Part I) arXiv v2 | 2026-09-06 |
| https://github.com/Tencent-Hunyuan/HY-WU/releases | HY-WU GitHub releases | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:hy-wu`, thread `tencent-hunyuan`, 1 dated events 2026-03-06 → 2026-03-06.
- **Practical note:** We can evaluate HY-WU from 2026-03-06 through its official project site, source repository, and Hugging Face page; the supplied evidence does not justify capability-specific adoption guidance.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
