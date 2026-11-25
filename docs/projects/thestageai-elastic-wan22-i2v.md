---
title: Elastic-Wan2.2-I2V
category: projects
date: 2026-07-21
tags: [elastic-wan22-i2v, elastic-wan22-i2v-development, project, thestageai-elastic-wan22-i2v]
aliases: ["Elastic-Wan2.2-I2V"]
---

# Elastic-Wan2.2-I2V

**Development line:** `project:thestageai-elastic-wan22-i2v` · thread `elastic-wan22-i2v-development`  
**Last event:** 2026-07-21 · 1 dated since 2026-07-21 · **Researched:** 2026-11-21 · confidence: medium

## What it is

Elastic-Wan2.2-I2V is a set of precompiled TheStage AI Qlip engines for the Wan 2.2 image-to-video 14B model, used through ComfyUI-Qlip.

- What: GPU-architecture-specific acceleration engines for the image-to-video transformer, loaded inside ComfyUI workflows.
- Users: ComfyUI users with an NVIDIA GPU and a TheStage access token.
- Key capability: the ComfyUI-Qlip repository lists a Wan 2.2 I2V test at 640x640, 81 frames, 4 steps, cfg 1.0 on H100. It says LoRA support adds about 5 to 15 percent overhead.
- Limits: engines must be recompiled after a hardware change, and the TensorRT version must match the 10.13 release pinned on the model card. The model card gives no speed or quality numbers. The card's license is proprietary.

As of 2026-11, sources disagree on RTX 5090 support, and no measured Wan 2.2 result for that GPU was found.

## Development line

- **2026-07-21 — TheStage AI published Elastic-Wan2.2-I2V project materials.** On 2026-07-21, TheStage AI posted an update linking to an Elastic-Wan2.2-I2V model repository, a blog article, and the ComfyUI-Qlip repository. The linked materials mark a development milestone for the image-to-video workflow. Link metadata alone does not confirm exact model changes, configuration, or performance claims.

## What changed

- 2026-02-27 — ComfyUI-Qlip repository created (GitHub API). The repository has no tags or releases; its last push was 2026-11-03.
- The model card (read 2026-11-21) lists no version history.

## How to use this

1. Check the requirements on the model card: an NVIDIA GPU with CUDA 12.x, the `qlip.core[nvidia]` package from TheStage's index, and the TensorRT 10.13 release the card pins.
  — <https://huggingface.co/TheStageAI/Elastic-Wan2.2-I2V>
2. Clone ComfyUI-Qlip into ComfyUI's `custom_nodes/`, run `install.py`, and set the access token with `thestage config set`. The repository pins a ComfyUI commit (b615af1c), which the engines require.
  — <https://github.com/TheStageAI/ComfyUI-Qlip>
3. Load engines with the Qlip Engines Loader node, setting `hf_repo` for automatic download. For a manual download, use huggingface-hub.
  — <https://huggingface.co/TheStageAI/Elastic-Wan2.2-I2V>
4. Keep the sampler, LoRAs and prompts from your existing Wan 2.2 workflow; the Qlip nodes accelerate the transformer run.
  — <https://github.com/TheStageAI/ComfyUI-Qlip>
5. Recompile engines after any GPU change.
  — <https://huggingface.co/TheStageAI/Elastic-Wan2.2-I2V>

## Best practices

- Pin ComfyUI and TensorRT versions together. The model card says the TensorRT version must match the one used for compilation.
  — <https://huggingface.co/TheStageAI/Elastic-Wan2.2-I2V>
- Do not run ComfyUI's own requirements install in the same environment. The Qlip page warns against it.
  — <https://github.com/TheStageAI/ComfyUI-Qlip>
- Benchmark on your own GPU. The only published Wan 2.2 I2V timing is the H100 test.
  — <https://github.com/TheStageAI/ComfyUI-Qlip>

## Superseded by this

- Nothing verified as obsolete by this page.

## Still unknown

- The base model is not named on the model card. Its identity as Wan 2.2 I2V 14B rests on the repository name and the ComfyUI-Qlip model list.
- "Elastic" is not defined. The stub's blog title (one expert, FP4, single RTX 5090) returned only a title when fetched, so its claims are unverified.
- RTX 5090 support conflicts: the ComfyUI-Qlip model list includes RTX 5090 for Wan 2.2 I2V, while a search snippet of the same repository says RTX 5090 is "coming soon" for Qlip benchmarks.
- License conflict on the ComfyUI-Qlip page: the License section says "Proprietary. Powered by TheStage AI", while the sidebar shows Apache-2.0.
- No independent quality or speed comparison with the base model was made.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/TheStageAI/Elastic-Wan2.2-I2V | TheStageAI/Elastic-Wan2.2-I2V — model card | 2026-11-21 |
| https://github.com/TheStageAI/ComfyUI-Qlip | TheStageAI/ComfyUI-Qlip — repository | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:thestageai-elastic-wan22-i2v`, thread `elastic-wan22-i2v-development`, 1 dated events 2026-07-21 → 2026-07-21.
- **Practical note:** Precompiled Qlip engines for Wan 2.2 I2V 14B, used via ComfyUI-Qlip; GPU- and TensorRT-version-specific, token required. RTX 5090 support conflicts across sources; verify on your GPU.
- **Confidence:** medium. Requirements verified; performance and license are partly conflicting or unmeasured. Dated supersedes above are the authority for what is obsolete.
