---
title: ToonComposer
category: projects
date: 2025-08-19
tags: [project, tooncomposer, tooncomposer-public-availability]
aliases: ["ToonComposer"]
---

# ToonComposer

**Development line:** `project:tooncomposer` · thread `tooncomposer-public-availability`  
**Last event:** 2025-08-19 · 2 dated since 2025-08-16 · **Researched:** 2026-09-04 · confidence: medium

## What it is

ToonComposer is a TencentARC post-keyframing model built on Wan2.1-I2V-14B-480P. It takes a colored reference frame, a text prompt, and one or more sketches at chosen frames. It generates an animated cartoon sequence, supports region-wise motion masks, and offers 480p or 608p checkpoints. A 61-frame 480p generation needs about 57 GB VRAM. We use it for controlled short cartoon shots when sparse artist-drawn motion guidance is available. We do not use it as a lightweight general video generator.

## Development line

- **2025-08-16 — ToonComposer's public project and source resources were recorded.** On 2025-08-16, ToonComposer gained a public project page and the TencentARC GitHub repository. These establish public project presentation and source code at that point in the timeline. They do not establish a specific version, capability, or original publication date.
- **2025-08-19 — A hosted ToonComposer Hugging Face Space was recorded.** On 2025-08-19, ToonComposer gained the TencentARC/ToonComposer Hugging Face Space. This adds a hosted public interface to the public project and source code. These links do not establish the Space's exact functions, model revision, or new capabilities.

## What changed

- 2025-08-14 — The paper introduced ToonComposer, sparse sketch injection, spatial low-rank adaptation, and PKBench before the listed release posts.
- 2025-08-16 — TencentARC released the project and code, establishing a unified post-keyframing workflow instead of a separate inbetweening-plus-colorization chain.
- 2025-08-19 — The official Hugging Face Space made the workflow available as a hosted demo alongside the released model.
- 2026-03-24 — The project author reported that the official Hugging Face demo restarted after a temporary Space failure.

## How to use this

As of 2025-08-19, we look for ToonComposer through its public project page, source repository, and hosted Hugging Face Space. We verify the exact capability and revision directly because this line has not been researched.

1. Clone the official repository, create a Python 3.10 Conda environment, and install its pinned requirements.
  — <https://github.com/TencentARC/ToonComposer>
2. Run `python app.py`; it uses cached weights first and otherwise retrieves the Wan2.1 foundation model and ToonComposer checkpoint.
  — <https://github.com/TencentARC/ToonComposer>
3. In the Gradio interface, set prompt, output-frame count, and resolution; provide a colored keyframe and sparse sketches at the frames you want to control.
  — <https://github.com/TencentARC/ToonComposer>
4. Use the official hosted Space when local GPU memory is insufficient.
  — <https://huggingface.co/spaces/TencentARC/ToonComposer>

## Best practices

- Start with one colored reference frame and one sketch, then add sketches only where additional motion control is needed.
  — <https://arxiv.org/abs/2508.10881>
- Use the sketch mask for regions where you want context-driven motion rather than leaving those regions unmarked.
  — <https://github.com/TencentARC/ToonComposer>
- For output variation or failures, adjust seed, sampling steps, CFG scale, position-aware residual scale, and sketch or mask inputs.
  — <https://github.com/TencentARC/ToonComposer>
- Treat the official Space as a fallback for the documented 57 GB-VRAM 480p/61-frame local workload; do not assume an inference-provider deployment exists.
  — <https://huggingface.co/TencentARC/ToonComposer>

## Superseded by this

- 2026-03-24 — Guidance that the official Hugging Face demo was unavailable is obsolete: the project author reported that it worked after a restart.

## Still unknown

- The requested event_findings and new_events fields were not in the schema; their evidence is preserved in what_changed.
- No dated first-party changelog or release history was found that documents model changes after the August 2025 release; the March 2026 demo restart is an availability change, not evidence of a new model version.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/TencentARC/ToonComposer | GitHub — TencentARC/ToonComposer | 2026-09-05 |
| https://huggingface.co/spaces/TencentARC/ToonComposer | Hugging Face Space — TencentARC/ToonComposer | 2026-09-05 |
| https://huggingface.co/TencentARC/ToonComposer | Hugging Face model card — TencentARC/ToonComposer | 2026-09-05 |
| https://arxiv.org/abs/2508.10881 | ToonComposer: Streamlining Cartoon Production with Generative Post-Keyframing | 2026-09-05 |
| https://huggingface.co/TencentARC/ToonComposer/discussions/2 | ToonComposer discussion: Availability? | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:tooncomposer`, thread `tooncomposer-public-availability`, 2 dated events 2025-08-16 → 2025-08-19.
- **Practical note:** As of 2025-08-19, practitioners should look for ToonComposer through its public project page, source repository, and hosted Hugging Face Space, while verifying the exact capability and revision directly because this line has not been researched.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
