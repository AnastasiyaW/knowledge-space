---
title: LiveEdit
category: projects
date: 2026-06-30
tags: [liveedit, project]
aliases: ["LiveEdit"]
---

# LiveEdit

**Development line:** `project:liveedit` · thread `liveedit`  
**Last event:** 2026-06-30 · 1 dated since 2026-06-30 · **Researched:** 2026-09-06 · confidence: medium

## What it is

LiveEdit is a text-instructed video-to-video editor for Linux and NVIDIA setups. It builds on Wan2.1-T2V-1.3B instead of running as a hosted service.

- Video-to-video editing from text prompts on an input stream.
- Causal chunk processing to keep background and unedited sections intact.
- Autoregressive mask caching for short clips and an extended path for long videos.

## Development line

- **2026-06-30 — LiveEdit project resources were publicly linked.** LiveEdit's official project page, code repository, and model checkpoints were already online. Author timelines place code and checkpoint guidance on 2026-06-24 and preprint v1 on 2026-06-25, so 2026-06-30 is not an author release date.

## What changed

- **2026-06-30:** LiveEdit's official project, source, and model endpoints were already public. The authors placed code and checkpoint instructions on 2026-06-24 and preprint v1 on 2026-06-25, so this is not an author release date.
- **2026-07-13:** arXiv updated the paper to v2 without accompanying code or checkpoint releases.
- **2026-08-05:** The authors documented long-video inference using rolling attention sinks and window-relative RoPE.

## How to use this

1. On Linux with an NVIDIA GPU, create the documented Python 3.10 environment. Install the requirements and FlashAttention. Single-GPU inference works; training scripts require multi-GPU torchrun.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
2. Download Wan-AI/Wan2.1-T2V-1.3B and the documented ar-forcing_002000.pt checkpoint into the paths expected by the repository.
  — <https://huggingface.co/cp-cp/LiveEdit>
3. Create a JSON file containing instruction and source_path. Run infer-local-ar-forcing.sh for the documented V2V path.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
4. Run infer-token-pruning.sh with --save_mask to inspect the cache. Run infer-local-ar-forcing-long.sh for longer clips.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>

## Best practices

- Use the documented 2,000-step ar-forcing_002000.pt checkpoint and its supplied script. Not every weight file in the repository has a standalone recipe.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
- Keep SINK_SIZE smaller than LOCAL_ATTN_SIZE in long-video mode, and test at target clip length. The authors note output degrades past the short-sequence training horizon.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>
- Save mask visualizations during token pruning so we can inspect which regions the cache reuses.
  — <https://github.com/cp-cp/LiveEdit/blob/main/README.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The 2026-06-30 entry supplies only its date and official URLs; the underlying claim is unavailable.
- No independent run has reproduced the reported 12.66 FPS or established a LiveEdit VRAM floor. That speed is an author-reported figure.
- The name LiveEdit is shared: qizhou000/LiveEdit is a separate CVPR 2025 vision-language model editing project. The cp-cp repository, Hugging Face checkpoint, project site, and arXiv preprint identify this video editing project.
- The 2026-06-24 and 2026-08-05 dates come from author README logs, not independent release tracking or third-party quality tests.

## Sources

| source | title | read |
|---|---|---|
| https://live-edit.github.io/ | LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing | ECCV 2026 | 2026-09-06 |
| https://github.com/cp-cp/LiveEdit | GitHub - cp-cp/LiveEdit: LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing | 2026-09-06 |
| https://github.com/cp-cp/LiveEdit/blob/main/README.md | README.md · cp-cp/LiveEdit at main | 2026-09-06 |
| https://huggingface.co/cp-cp/LiveEdit | cp-cp/LiveEdit · Hugging Face | 2026-09-06 |
| https://arxiv.org/abs/2606.26740 | LiveEdit: Towards Real-Time Diffusion-Based Streaming Video Editing | 2026-09-06 |
| https://github.com/qizhou000/LiveEdit | qizhou000/LiveEdit: Lifelong Knowledge Editing for Vision Language Models with Low-Rank Mixture-of-Experts | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:liveedit`, thread `liveedit`, 1 dated events 2026-06-30 → 2026-06-30.
- **Practical note:** Use the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above decide what is obsolete.