---
title: "Lift: lift-controllable-video-generation — Lift Controllable Video Generation"
category: "projects"
date: 2026-10-09
tags: ["lift", "lift-controllable-video-generation", "project"]
aliases: ["Lift: lift-controllable-video-generation"]
---

# Lift: lift-controllable-video-generation — Lift Controllable Video Generation

**Development line:** project:lift · thread lift-controllable-video-generation  
**Last event:** 2026-10-09 · 2 dated since 2026-09-29 · **Researched:** 2026-11-28 · confidence: high

## What it is

LIFT \(Layout-In-Future Video Generation under Large Viewpoint Change via On-Policy Self-Distillation\) is a unified image-to-video framework. Given a first frame, the user sets a camera path and the layout of the final frame with bounding boxes and local text prompts. LIFT then generates a video that goes from the input image to that layout while following the camera trajectory, even when the camera reveals regions not visible in the first frame. The backbone is a diffusion transformer conditioned on the first frame, a text caption, a camera trajectory \(Plücker ray embeddings\) and a spatiotemporal layout. It is fine-tuned from Wan2.1-Fun-V1.1-1.3B-Control-Camera. Authors are from UC San Diego, University of Virginia, Meta, Amazon and Lambda.

## Development line

- **2026-09-29 — Lift: lift-controllable-video-generation update.** The LIFT paper \(arXiv 2609.38146\) was listed on Hugging Face Papers as published on Sep 29. (found in research)
- **2026-10-09 — LIFT framework released for controllable video generation with future layout control.** The recorded link on 2026-10-09 introduced LIFT, a framework for controlled video generation that adds future-frame layout control to camera trajectory control. Video runs from a first frame to a specified last frame following the camera path; it supports large viewpoint changes, object boxes in the last frame as control signals, and two modes \(camera only, camera plus layout\). Links to GitHub, Hugging Face and a demo were provided.
  - The project page confirms the framework and adds details. It is an image-to-video model with last-frame layout control, trained by on-policy self-distillation from a dense-layout teacher. It has two inference modes: single-condition \(camera trajectory only\) and dual-condition \(camera trajectory plus last-frame layout\). The paper reports better video quality, future-layout controllability and camera controllability than the compared methods \(Uni3C, GEN3C, MagicMotion, Direct-a-Video\). The LIFT-Vista dataset has 120,898 clips, including a 58,272-clip subset with joint layout and camera annotations. Layouts average 5.5 objects per clip across 8,302 categories, and 84.8% of clips contain objects invisible in the first frame. (undated page) — <https://jsxzs.github.io/LIFT/>
  - The GitHub repository \(Apache-2.0\) provides installation instructions \(Conda or Apptainer\), a download recipe for the LIFT checkpoint, the LIFT-Vista dataset and the Wan2.1 base model, and an inference example in examples/example1. One set of released weights serves both the camera-only and camera-plus-last-frame-layout modes. LIFT-Vista clips are 81 frames at 16 FPS. (undated page) — <https://github.com/jsxzs/LIFT>
  - The Hugging Face model card \(Overdog/LIFT, Apache-2.0, image-to-video\) lists two checkpoints: LIFT/transformer, the last-frame layout student trained by dual-mode on-policy self-distillation, and LIFT\_dense\_layout\_teacher/transformer, the teacher fine-tuned on dense per-frame layouts. It links the paper arXiv 2609.38146 and a demo Space. (undated page) — <https://huggingface.co/Overdog/LIFT>

## What changed

Camera controls only set viewpoint trajectories and text prompts give only coarse guidance. LIFT adds an explicit last-frame layout as a control signal for what appears in the future view and where. To learn from this sparse signal, a dense-layout teacher is distilled into a last-frame-layout student by on-policy self-distillation. The authors also curated the LIFT-Vista dataset. The code, weights, dataset and a demo Space are public.

## How to use this

1. Clone the repository and create the environment: git clone https://github.com/jsxzs/LIFT.git, create a Python 3.12 conda environment, and install requirements.txt \(with the cu126 PyTorch index\) plus flash-attention. An Apptainer image can be built from env.def instead.
  — <https://github.com/jsxzs/LIFT>
2. Download the weights with the Hugging Face CLI. Get the Wan2.1-Fun-V1.1-1.3B-Control-Camera base model, the LIFT checkpoint \(hf download Overdog/LIFT\) and, optionally, the LIFT-Vista dataset \(Overdog/LIFT-Vista\).
  — <https://github.com/jsxzs/LIFT>
3. Prepare the inputs: a first frame, a camera trajectory, and the last-frame layout as bounding boxes with local text prompts. Start from the provided examples/example1 folder, then generate the shot.
  — <https://jsxzs.github.io/LIFT/>

## Best practices

- Use the dual-condition mode \(camera trajectory plus last-frame layout\) when you need to control what appears in newly revealed regions. Use the single-condition mode when only the camera path matters. One checkpoint covers both.
  — <https://jsxzs.github.io/LIFT/>
- Specify the final-frame layout with bounding boxes plus local text prompts for each object. This is the interface the model was trained on, and it helps most under large viewpoint changes.
  — <https://github.com/jsxzs/LIFT>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The pages do not state hardware requirements or generation time.
- The demo Space page loaded without visible details, so its capabilities are not confirmed here.
- The project and repository pages carry no release date, so the exact public code and weights release date is unknown.

## Sources

| source | title | read |
|---|---|---|
| https://jsxzs.github.io/LIFT/ | LIFT: Layout-In-Future Video Generation under Large Viewpoint Change via On-Policy Self-Distillation \(project page\) | 2026-10-09 |
| https://github.com/jsxzs/LIFT | GitHub - jsxzs/LIFT | 2026-10-09 |
| https://huggingface.co/Overdog/LIFT | Overdog/LIFT · Hugging Face | 2026-10-09 |

## Agent brief {#agent-brief}

- **Subject:** project:lift, thread lift-controllable-video-generation, 2 dated events 2026-09-29 → 2026-10-09.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
