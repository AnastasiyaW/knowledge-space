---
title: Capybara
category: projects
date: 2026-02-24
tags: [capybara, capybara-development, project]
aliases: ["CAPYBARA", "Capybara"]
---

# Capybara

**Development line:** `project:capybara` · thread `capybara-development`  
**Last event:** 2026-02-24 · 2 dated since 2026-02-17 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Capybara is an open-source inference pipeline for users who need generation and instruction-based editing in one interface.

- Text-to-image (T2I) and text-to-video (T2V) generation.
- Instruction-based image-to-image (TI2I) and video-to-video (TV2V) editing.
- Single runs, CSV batches, distributed inference via Accelerate, and ComfyUI nodes.

Documentation recommends Python 3.11 and CUDA 12.6. FP8 requires NVIDIA Ada/Hopper with compute capability at least 8.9 and torchao. It is a workable integration for local inference, but not a documented production or training platform.

## Development line

- **2026-02-17 — Capybara source, model, and demo resources were linked.** On 2026-02-17, the dated resource set linked Capybara’s source repository and model page together with a Qwen3-VL model and a hosted endpoint. This marks an early public development step for Capybara, though the links alone do not establish exact capability, release status, or their relationship.
- **2026-02-24 — Capybara documentation surfaced ComfyUI and FP8 workflows.** Documentation documented ComfyUI custom nodes, FP8, and a sample workflow. The official README dates these additions to 2026-02-20 for code changes, while 2026-02-24 is the recorded event date.

## What changed

Capybara — on 2026-02-17, the v0.1 inference framework released with T2I, T2V, TI2I, and TV2V. On 2026-02-24, documentation recorded ComfyUI custom nodes, FP8, and a sample workflow. The official README dates those features to 2026-02-20 for code changes, making 2026-02-24 the recorded event date. As of 2026-09-04, the current first-party README still contains only those two dated lines, marks ComfyUI as done, and keeps release unified creation model and training code in TODO.

## How to use this

After 2026-02-24, evaluate Capybara through its ComfyUI documentation, sample workflow, and FP8 guidance rather than the base repository or model page alone.

1. Create an isolated Python 3.11 environment, install PyTorch for CUDA 12.6, and install project dependencies.
  — <https://github.com/xgen-universe/Capybara>
2. Download all required checkpoint components into `ckpts/`. Qwen3-VL-8B-Instruct is needed only when instruction rewriting is enabled.
  — <https://github.com/xgen-universe/Capybara>
3. For a first run, call `inference.py` with `task_type` `t2i` or `t2v`. For `ti2i` and `tv2v`, pass `media_path` and a text instruction.
  — <https://github.com/xgen-universe/Capybara>
4. For batch jobs, prepare a CSV with `img_path` or `video_path` and `instruction`, then pass `csv_path` and `data_root_path`.
  — <https://github.com/xgen-universe/Capybara>
5. For ComfyUI, link the Capybara root into `custom_nodes` and run ComfyUI in the same `capybara` environment.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
6. Load `sample_workflow.json` into the ComfyUI canvas, then adjust `task_type` and the `reference` input for T2I, T2V, TI2I, or TV2V.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/examples/sample_workflow.json>

## Best practices

- Start with the official baseline mode: 480p and 50 steps for video, 720p and 50 steps for images. Raise resolution only after establishing a working baseline.
  — <https://github.com/xgen-universe/Capybara>
- In ComfyUI for TI2I and TV2V, supply the frame or video via `reference`. The node infers aspect ratio from `reference` and fixes `guidance_scale` at 1.0.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Enable FP8 only on Ada/Hopper with `torchao`. This cuts transformer weight memory roughly in half, but promises no speedup and pins the transformer in GPU memory.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Do not mix Python environments between Capybara and ComfyUI. Documentation requires running ComfyUI from the same environment so custom nodes find their dependencies.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Pin the resolved model repository and revision before downloading. The official `xgen-universe` link currently redirects to `Glanty/Capybara`.
  — <https://huggingface.co/xgen-universe/Capybara>

## Superseded by this

- 2026-02-20: the earlier TODO "Add support for ComfyUI" is obsolete because Capybara provides custom nodes and a sample workflow. The native CLI remains supported and is not replaced.

## Still unknown

- Official sources do not explain whether the Hugging Face redirect from `xgen-universe/Capybara` to `Glanty/Capybara` is an ownership transfer, a mirror, or an error. Verify specific files and revision before use.
- First-party documentation provides no VRAM tables, independent benchmarks, or proof of production readiness. Training code also remains unreleased.
- The temporary ngrok demo URL from the 2026-02-17 event could not be opened safely, so its current availability is unconfirmed.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/xgen-universe/Capybara | xgen-universe/Capybara — repository README | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/README.md | Capybara — main README, raw source | 2026-09-04 |
| https://huggingface.co/xgen-universe/Capybara | xgen-universe/Capybara — Hugging Face model page, redirected to Glanty/Capybara | 2026-09-04 |
| https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct | Qwen3-VL-8B-Instruct — Hugging Face model card | 2026-09-04 |
| https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md | Capybara ComfyUI Custom Nodes | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/comfyui/README.md | Capybara ComfyUI Custom Nodes — raw source | 2026-09-04 |
| https://github.com/xgen-universe/Capybara/blob/main/comfyui/examples/sample_workflow.json | Capybara ComfyUI sample workflow | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/comfyui/examples/sample_workflow.json | Capybara ComfyUI sample workflow — raw source | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:capybara`, thread `capybara-development`, 2 dated events 2026-02-17 → 2026-02-24.
- **Practical note:** After 2026-02-24, practitioners evaluating Capybara should consult its ComfyUI documentation, sample workflow, and FP8 guidance rather than relying only on the base repository or model page.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
