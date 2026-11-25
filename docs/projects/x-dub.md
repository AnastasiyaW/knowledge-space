---
title: X-Dub — Project development
category: projects
date: 2026-03-28
tags: [project, project-development, x-dub]
aliases: ["X-Dub"]
---

# X-Dub — Project development

**Development line:** `project:x-dub` · thread `project-development`  
**Last event:** 2026-03-28 · 1 dated since 2026-03-28 · **Researched:** 2026-09-05 · confidence: high

## What it is

X-Dub is an Apache-2.0 code-and-weights release for video-to-audio lip synchronization. The public model is X-Dub (Wan-5B), built on Wan2.2-TI2V-5B rather than the paper’s internal X-Dub (internal-1B).

- Mouth motion editing: syncs video mouth motion to supplied audio.
- Character support: handles human and non-human faces.
- Face cropping: auto-crops the head area.

Typical inference needs about 21 GB VRAM and currently supports one person per video. Use it for local single-subject redubbing when GPU memory and occasional flicker or identity drift are acceptable.

## Development line

- **2026-03-28 — X-Dub public project resources were linked.** On 2026-03-28, a dated X-Dub entry linked the project website, GitHub repository, and Hugging Face page. The links confirm public code and weights without introducing a new release, version, or technical change.

## What changed

- 2025-12-31 — The paper and project page introduced ContextDubBench and the self-bootstrapping, mask-free visual-dubbing method.
- 2026-03-19 — Inference code and pretrained weights for the public Wan-based X-Dub release were published.
- 2026-03-28 — X-Dub became available across the project page, GitHub repository, and Hugging Face weights.
- 2026-05-15 — The project reported acceptance to ICML 2026.

## How to use this

As of 2026-03-28, consult the X-Dub project site, GitHub repository, and Hugging Face page when evaluating public resources. The linked entry provides code and weights rather than a distinct setup procedure.

1. Clone the official repository, create a Python 3.10 Conda environment, and install the listed Python, OpenMMLab, and editable-project dependencies.
  — <https://github.com/KlingAIResearch/X-Dub>
2. Download `KlingTeam/X-Dub` into `checkpoints/`, then move the bundled DWPose models to `dwpose_tools/models/`.
  — <https://github.com/KlingAIResearch/X-Dub>
3. Run `infer_lip_sync_pipeline.py` with a video, replacement audio, `X-Dub_model.safetensors`, output directory, and initial settings of `ref_cfg_scale=2.5`, `audio_cfg_scale=10.0`, and 30 inference steps.
  — <https://github.com/KlingAIResearch/X-Dub>
4. Review the output for crop jitter, flicker, color drift, and noisy frames before publishing edited media.
  — <https://github.com/KlingAIResearch/X-Dub>

## Best practices

- Use single-person footage with a face that remains trackable. Online DWPose loses fast-moving heads and fails in multi-person scenes.
  — <https://github.com/KlingAIResearch/X-Dub>
- Start with 25–50 inference steps. More steps cost runtime and lack exhaustive evaluation.
  — <https://github.com/KlingAIResearch/X-Dub>
- Tune `ref_cfg_scale` and `audio_cfg_scale` per clip to trade reference-appearance fidelity against audio-driven mouth movement.
  — <https://github.com/KlingAIResearch/X-Dub>
- Clearly label generated or edited media. Do not use the system for deceptive impersonation.
  — <https://github.com/KlingAIResearch/X-Dub>

## Superseded by this

- 2026-03-19 — The paper's internal X-Dub (internal-1B) is not the downloadable implementation. The public release is X-Dub (Wan-5B), which swaps the backbone and uses multi-stage SFT instead of LoRA tuning.
- 2026-03-19 — Do not assume parity with the paper model in production. The public release runs about 2× slower, can flicker or drift, and reports severe noisy frames in roughly 2% of cases.

## Still unknown

- No first-party source assigns a distinct product change specifically to 2026-03-28. The official repository dates the public release to 2026-03-19. We treat 2026-03-28 as confirmation of availability, not a separate model version.
- The public repository says quantitative comparisons with the internal paper model will be reported in a future update; no such comparison was verified here.

## Sources

| source | title | read |
|---|---|---|
| https://hjrphoebus.github.io/X-Dub/ | X-Dub: From Inpainting to Editing: A Self-Bootstrapping Framework for Context-Rich Visual Dubbing | 2026-09-05 |
| https://github.com/KlingAIResearch/X-Dub | KlingAIResearch/X-Dub — official repository | 2026-09-05 |
| https://huggingface.co/KlingTeam/X-Dub | KlingTeam/X-Dub — model card and weights | 2026-09-05 |
| https://arxiv.org/abs/2512.25066 | From Inpainting to Editing: A Self-Bootstrapping Framework for Context-Rich Visual Dubbing | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:x-dub`, thread `project-development`, 1 dated events 2026-03-28 → 2026-03-28.
- **Practical note:** As of 2026-03-28, practitioners should consult the X-Dub project site, GitHub repository, and Hugging Face page when evaluating the project or locating its public resources; this evidence does not establish a specific setup or usage procedure.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.