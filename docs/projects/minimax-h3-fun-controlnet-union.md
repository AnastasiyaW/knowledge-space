---
title: MiniMax-H3-Fun-Controlnet-Union — MiniMax H3 Fun ControlNet Union
category: projects
date: 2026-08-24
tags: [minimax-h3-fun-controlnet-union, minimax_h3_fun_controlnet_union, project]
aliases: ["MiniMax-H3-Fun-Controlnet-Union"]
---

# MiniMax-H3-Fun-Controlnet-Union — MiniMax H3 Fun ControlNet Union

**Development line:** `project:minimax-h3-fun-controlnet-union` · thread `minimax-h3-fun-controlnet-union`  
**Last event:** 2026-08-24 · 1 dated since 2026-08-24 · **Researched:** 2026-09-05 · confidence: high

## What it is

MiniMax-H3-Fun-Controlnet-Union provides control conditioning for the MiniMax-H3 base video generator in VideoX-Fun.

- Unified checkpoint: runs Canny, Depth, HED, MLSD, and Pose guidance.
- Video-to-video: transfers motion into new video frames.
- Video inpainting: edits masked video regions.

Control weights require the base model, and the base transformer plus Qwen3-VL exceed 80 GB VRAM when loaded together. Choose this setup when motion structure matters more than standalone text-to-video generation and GPU offload is available.

## Development line

- **2026-08-24 — MiniMax H3 Fun ControlNet Union linked with a VideoX-Fun example.** On 2026-08-24, VideoX-Fun published an example directory for MiniMax H3 Fun alongside the MiniMax-H3-Fun-Controlnet-Union repository on Hugging Face. The integration connects the control checkpoint to an implementation example, though release details were not independently verified.

## What changed

2026-08-24 — VideoX-Fun added the `examples/minimax_h3_fun` directory, and ControlNet-Union for MiniMax-H3 became available as a standalone control model.

2026-08-27 — ComfyUI prepared support for checkpoint loading, video conditioning, inpainting conditioning, and control streams, but PR #15860 remains open.

## How to use this

Evaluate the VideoX-Fun MiniMax H3 Fun example alongside MiniMax-H3-Fun-Controlnet-Union starting 2026-08-24.

1. Clone VideoX-Fun and create `models/Diffusion_Transformer`. Place the base MiniMax-H3 model and `MiniMax-H3-Fun-Controlnet-Union.safetensors` in separate directories as specified in the model card.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
2. Set the base model path, `minimax_h3_control.yaml`, control weights path, control video, and prompt in `examples/minimax_h3_fun/predict_v2v_control.py`, then run the script.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
3. Run `predict_v2v_control_inpaint.py` instead of the standard control-video script for mask-based editing.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
4. Enable `model_group_offload` or `model_cpu_offload_and_qfloat8` on a single 80 GB GPU. The base transformer and Qwen3-VL cannot fit into memory at the same time.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>

## Best practices

- Keep `guidance_scale = 1.0` because the checkpoint is guidance-distilled; higher values reapply guidance and degrade quality.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Keep the control network layout intact so the weights load: maintain `control_blocks_places: [0, 10, 20, 30, 40]`, `control_in_dim: 49`, and disabled audio control.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Start with `control_context_scale = 1.0` to follow the control video; lower it only to weaken control influence, while `0.0` disables control entirely.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Check the MiniMax H3 Community License before distribution or hosted use: it excludes the EU, UK, Republic of Korea, and USA from the Applicable Territory, and sets separate terms once revenue exceeds USD 20 million per year.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The exact public release timestamp for the Hugging Face repository is not confirmed beyond 2026-08-24 because the commit view shows relative time instead of an ISO timestamp.
- ComfyUI PR #15860 remains open; confirming release support requires a merged PR or release receipt.
- `event_findings` and `new_events` serve as schema extensions required by the task but absent from the base schema.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/aigc-apps/VideoX-Fun/tree/main/examples/minimax_h3_fun | VideoX-Fun — examples/minimax_h3_fun | 2026-09-05 |
| https://github.com/aigc-apps/VideoX-Fun/commits/main/examples/minimax_h3_fun | VideoX-Fun — history for examples/minimax_h3_fun | 2026-09-05 |
| https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union | alibaba-pai/MiniMax-H3-Fun-Controlnet-Union model card | 2026-09-05 |
| https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0 | Update Weights — MiniMax-H3-Fun-Controlnet-Union | 2026-09-05 |
| https://github.com/Comfy-Org/ComfyUI/pull/15860 | ComfyUI PR #15860 — Support MiniMax-H3 fun controlnet | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:minimax-h3-fun-controlnet-union`, thread `minimax-h3-fun-controlnet-union`, 1 dated events 2026-08-24 → 2026-08-24.
- **Practical note:** Evaluate the VideoX-Fun MiniMax H3 Fun example alongside the MiniMax-H3-Fun-Controlnet-Union checkpoint starting 2026-08-24; exact setup details remain unverified.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.