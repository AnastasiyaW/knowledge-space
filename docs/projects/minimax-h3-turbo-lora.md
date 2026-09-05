---
title: MiniMax-H3 Turbo LoRA
category: projects
date: 2026-08-06
tags: [minimax-h3-turbo-lora, minimax_h3_turbo_lora, project]
aliases: ["MiniMax-H3 Turbo LoRA"]
---

# MiniMax-H3 Turbo LoRA

**Development line:** `project:minimax-h3-turbo-lora` · thread `minimax-h3-turbo-lora`  
**Last event:** 2026-08-06 · 1 dated since 2026-08-06 · **Researched:** 2026-09-05 · confidence: high

## What it is

MiniMax-H3 Turbo LoRA is a community adapter and ComfyUI node set for MiniMax-H3 text-to-video and image-to-video workflows.

- Joint audio-video sampling with fewer steps.
- Base support for full and pruned H3 checkpoints.
- Custom sampler for separate audio and video schedules.

Sampling takes 4 steps minimum, with 6–8 steps preferred; audio and intense motion remain a preview. Use it for fast iteration, but check fast-motion shots against the base workflow.

## Development line

- **2026-08-06 — MiniMax-H3 Turbo LoRA resource bundle documented.** On 2026-08-06, we linked the MiniMax-H3 Turbo LoRA model resource to a demo Space, a ComfyUI integration repository, and a ComfyUI-oriented model resource. The workflow now covers model distribution, demonstration, and ComfyUI use. The linked resources alone do not prove their separate release dates, versions, authorship, or performance claims.

## What changed

- 2026-08-06 — The public ComfyUI integration added the Turbo LoRA loader and 4-step sampler, pruned and curve base support, runtime adapter application, and a low-VRAM switch.
- 2026-08-07 — The v4 step-600 EMA checkpoint became the default recommendation; guidance narrowed practical sampling to 4–8 steps and kept v1 step-850 only for heavy motion at four steps.
- 2026-08-08 — The node integration fixed an AdaLN injection mismatch for audio-reference conditioning.
- 2026-08-10 — The integration corrected modulation-segment calculation through the AdaLN time-table lookup.
- 2026-08-12 — The integration merged an audio-reference AdaLN-row fix.
- 2026-08-14 — The integration merged a further upstream contribution; keep the custom node current.

## How to use this

From 2026-08-06, evaluate MiniMax-H3 Turbo LoRA through the linked model and ComfyUI integration, not as an isolated checkpoint. Verify live compatibility, licensing, and setup requirements before use.

1. Install `Larryvrh/ComfyUI-MiniMax-H3-Turbo` with ComfyUI-Manager or clone it into `ComfyUI/custom_nodes`, then restart ComfyUI.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>
2. Download the Turbo LoRA `.safetensors` into `ComfyUI/models/loras/` and install the MiniMax-H3 base model, VAEs, and text encoder.
  — <https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora>
3. Start from an official H3 text-to-video or image-to-video workflow; place the Turbo LoRA node between the diffusion-model loader and `SamplerCustomAdvanced`, then feed that sampler from MiniMax-H3 Turbo Sampler.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>
4. Set the scheduler to `simple`, strength to 1.0, and begin at 6–8 steps; use 4 only when speed matters more than motion quality.
  — <https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora>

## Best practices

- Use `minimax_h3_turbo_v4_step600_ema.safetensors` for most shots; reserve v1 step-850 for fast, heavy motion at exactly four steps.
  — <https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora>
- Keep `low_vram` off for sharper runtime application; turn it on only after an out-of-memory error, accepting softer output on quantized bases.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>
- Keep the Turbo Sampler in the graph across ComfyUI updates; it adapts to native `ModelSamplingAV` support and preserves correct audio scheduling on older builds.
  — <https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo>

## Superseded by this

- 2026-08-07 — v1 step-850 is no longer the default; v4 step-600 EMA replaces it except for four-step heavy motion.
- 2026-08-06 — The adapter was limited to non-pruned H3 bases; the custom node added support for pruned and curve variants.

## Still unknown

- The adapter and its node are community releases, not an official MiniMax Turbo product.
- No independent benchmark ranks quality or speed across GPUs, resolutions, durations, and motion types.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/larryvrh/MiniMax-H3-Turbo-Lora | larryvrh/MiniMax-H3-Turbo-Lora · Hugging Face | 2026-09-05 |
| https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo | Larryvrh/ComfyUI-MiniMax-H3-Turbo · GitHub | 2026-09-05 |
| https://github.com/Larryvrh/ComfyUI-MiniMax-H3-Turbo/commits/main/ | Commit history for Larryvrh/ComfyUI-MiniMax-H3-Turbo · GitHub | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:minimax-h3-turbo-lora`, thread `minimax-h3-turbo-lora`, 1 dated events 2026-08-06 → 2026-08-06.
- **Practical note:** From 2026-08-06, evaluate MiniMax-H3 Turbo LoRA through the linked model and ComfyUI integration, not as an isolated checkpoint. Verify live compatibility, licensing, and setup requirements before use.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
