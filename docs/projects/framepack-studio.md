---
title: FramePack Studio — FramePack Studio development
category: projects
tags: [framepack-studio, framepack-studio-development, framepack_studio, project]
aliases: ["FramePack Studio", "Framepack Studio"]
---

# FramePack Studio — FramePack Studio development

**Development line:** `project:framepack-studio` · thread `framepack-studio-development`  
**Events:** 2 dated, 2025-05-05 → 2025-07-04 · **Researched:** 2026-09-04 · confidence: medium

## What it is

FramePack Studio — a local application built on FramePack for creators who need Original/F1 image-to-video generation and video extension without assembling a separate workflow. - Original and end-frame generation, F1 generation, and video extension; - text, image, video, LoRA, timestamped-prompt, and prompt-blending inputs; - job queues, presets, reproducible metadata, upscaling, interpolation, filters, and looping. Limit: the repository specifies a CUDA GPU with at least 8 GB VRAM, 16 GB recommended, 16 GB system memory, and 80 GB storage; the docs say first launch downloads roughly 30 GB of models. Verdict: use the FP-Studio repository and documentation for a local GPU workflow; do not confuse it with the unrelated browser service at framepack.studio.

## Development line

- **2025-05-05 — FramePack Studio repository was linked.** On 2025-05-05, the dated record associated FramePack Studio with the GitHub repository at colinurbs/FramePack-Studio. It also linked a GreenNeuralRobots The source item, but the supplied evidence does not identify a release, version, or specific capability.
- **2025-07-04 — FramePack Studio documentation and project repository were linked.** On 2025-07-04, the dated record linked FramePack Studio to the FP-Studio/FramePack-Studio GitHub repository and its documentation site. This is a distinct public project-reference step, although the supplied links do not establish whether it announced a release, migration, or feature change.

## What changed

FramePack Studio — the public path moved from a personal-repository URL to the FP-Studio project and documentation, while the newest formal release found remains 0.5.1. - 2025-05-05 — the recorded project link was colinurbs/FramePack-Studio; it now redirects to FP-Studio/framepack-studio. The announcement text is unavailable, so no feature change is attributed to this date. - 2025-06-30 (found today) — v0.5.0 made MagCache the default cache, added Granite prompt enhancement and Florence2 image captioning, published Docker images, and announced the documentation site. - 2025-07-04 — the project links point to the FP-Studio repository and official documentation, confirming the same project identity rather than a second FramePack Studio. - 2025-07-14 (found today) — v0.5.1 made Original use the input image as its first frame and fixed FFmpeg argument ordering for video loops. - 2025-11-14 (found today) — main received package-version updates; no newer release is listed. - 2026-03-07 (found today) — a develop-branch logging change triggered a Docker publish workflow that failed while installing requirements. This warns about the development Docker path; it does not prove that release 0.5.1 cannot run. Limit: the public release page still labels 0.5.1 as latest. Verdict: the project remained active after its last release, but a current deployment should use a pinned, tested build rather than assume latest-develop is publishable.

## How to use this

From 2025-07-04, practitioners should consult the linked FramePack Studio repository together with its documentation site when evaluating or using the project; the dated links alone do not establish a version-specific workflow.

1. Check that the GPU, CUDA/Torch build, memory, and storage meet the documented requirements; choose Pinokio, Docker, Windows automated install, or manual setup for the host.
  — <https://docs.framepackstudio.com/docs/get_started/>
2. Install and start the application. For Docker, clone the repository and run docker compose; for manual installation, create a virtual environment, install requirements and the CUDA-matched Torch build, then run studio.py.
  — <https://docs.framepackstudio.com/docs/get_started/>
3. Open the local interface at http://localhost:7860 after the initial model download completes.
  — <https://docs.framepackstudio.com/docs/get_started/>
4. Choose Original for stronger consistency, Original with Endframe when the final frame matters, F1 for more dynamic motion, or a Video mode to extend an existing clip; provide the applicable image or video input.
  — <https://docs.framepackstudio.com/docs/user_guide/>
5. Write a specific prompt with subject, scene, action, camera, lighting, and framing; use timestamped prompt segments when the action needs to change over time.
  — <https://docs.framepackstudio.com/docs/prompting_guide/>
6. Add jobs to the queue, inspect outputs and saved metadata, then send selected clips to post-processing for operations such as upscaling, interpolation, filters, or loops.
  — <https://docs.framepackstudio.com/docs/user_guide/>

## Best practices

- Match the Torch CUDA build to the GPU and use the documented install route for the host. Pinokio is easiest for a non-technical install but is explicitly harder to troubleshoot.
  — <https://docs.framepackstudio.com/docs/get_started/>
- Install at most one attention library, and do not install SageAttention, FlashAttention, or xFormers on RTX 1000/2000-series GPUs because the docs warn that generation errors can result.
  — <https://docs.framepackstudio.com/docs/get_started/>
- Choose the model by the trade-off: Original generally keeps consistency better, while F1 generally produces more dynamic motion but may pulse between sections.
  — <https://docs.framepackstudio.com/docs/user_guide/>
- Keep the prompt concrete but bounded: name subject, scene, action, camera, lighting, and shot size; the official guide suggests 60–100 words and a logical sequence.
  — <https://docs.framepackstudio.com/docs/prompting_guide/>
- Save metadata JSON and retain a seed for promising runs, so parameters can be restored and compared instead of recreated from memory.
  — <https://docs.framepackstudio.com/docs/user_guide/>
- Treat higher CFG and more aggressive caching as quality-speed trade-offs: CFG above 1 doubles generation time and can add artifacts; lower MagCache thresholds or retention can be faster but deviate more from uncached output.
  — <https://docs.framepackstudio.com/docs/user_guide/>
- Do not assume the develop Docker path is publishable: the last observed develop publishing workflow failed during requirements installation. Pin and test the chosen build.
  — <https://github.com/FP-Studio/framepack-studio/actions/runs/22808835350>

## Superseded by this

- 2025-05-05 — treating colinurbs/FramePack-Studio as a separate current project address; it redirects to FP-Studio/framepack-studio.
- 2025-06-30 — pre-v0.5 assumptions that MagCache was not the default cache or that no documentation site existed.
- 2025-07-14 — v0.5.0-era assumptions about Original input-image handling; v0.5.1 uses the input image as the first frame.
- 2026-03-07 — treating a latest-develop Docker image as a verified deployment route; the observed publishing run failed.

## Still unknown

- The exact text and feature claims of the 2025-05-05 and 2025-07-04 announcements are unavailable; their links establish provenance and identity, not a precise release note.
- The two dated GitHub links resolve to the same FP-Studio project, so they do not indicate two different subjects. A separate browser-oriented service at framepack.studio uses the same name and should not be treated as FP-Studio.
- No first-party Simplified-Chinese documentation or confirmed Chinese operating-report source was found in the observed searches; returned Chinese-language results primarily exposed the unrelated name collision.
- There is no clean-install or successful current Docker deployment receipt here. The documentation, release history, open May 2026 installation report, and failed March 2026 develop publish job show that installation and packaging state may have drifted after v0.5.1.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/colinurbs/FramePack-Studio/ | GitHub - FP-Studio/framepack-studio: Expanding FramePack into a multifunction video creation tool | 2026-09-04 |
| https://github.com/FP-Studio/FramePack-Studio/ | FP-Studio/framepack-studio repository | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio | GitHub - FP-Studio/framepack-studio: Expanding FramePack into a multifunction video creation tool | 2026-09-04 |
| https://github.com/FP-Studio/FramePack-Studio/releases | Releases · FP-Studio/framepack-studio | 2026-09-04 |
| https://docs.framepackstudio.com/docs/get_started/ | Getting Started | FP-Studio | 2026-09-04 |
| https://docs.framepackstudio.com/docs/user_guide/ | User Guide | FP-Studio | 2026-09-04 |
| https://docs.framepackstudio.com/docs/prompting_guide/ | Prompting Guide | FP-Studio | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio/commits/main/ | Commits · FP-Studio/framepack-studio | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio/actions/runs/22808835350 | finish logging implementation · FP-Studio/framepack-studio@648e34a | 2026-09-04 |
| https://github.com/FP-Studio/framepack-studio/issues/382 | Installation Fail for FP-Studio · Issue #382 | 2026-09-04 |
| https://framepack.studio/zh | FramePack Studio | FramePack AI、FramePack Studio 及图像转视频工作流程 | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:framepack-studio`, thread `framepack-studio-development`, 2 dated events 2025-05-05 → 2025-07-04.
- **Practical note:** From 2025-07-04, practitioners should consult the linked FramePack Studio repository together with its documentation site when evaluating or using the project; the dated links alone do not establish a version-specific workflow.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
