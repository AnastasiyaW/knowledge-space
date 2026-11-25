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

MiniMax-H3-Fun-Controlnet-Union is a control adapter for the MiniMax-H3 base video generator, built for VideoX-Fun users.

- Unified checkpoint to run Canny, Depth, HED, MLSD, and Pose conditioning.
- Video-to-video pipeline to direct generation from control video.
- Video inpainting pipeline to edit masked areas.

Control weights are not standalone; base transformer and Qwen3-VL together exceed 80 GB VRAM. Choose it when motion structure matters more than standalone text-to-video generation and offload is available.

## Development line

- **2026-08-24 — MiniMax H3 Fun ControlNet Union linked with a VideoX-Fun example.** On 2026-08-24, a project update linked the MiniMax-H3-Fun-Controlnet-Union Hugging Face repository to a VideoX-Fun example directory for MiniMax H3 Fun. The link connects the model weights to an implementation example. Setup details and release capabilities were not verified independently.

## What changed

2026-08-24 — VideoX-Fun added the `examples/minimax_h3_fun` directory, and ControlNet-Union for MiniMax-H3 became available as a separate control model. 2026-08-27 — ComfyUI prepared checkpoint loading, video and inpainting conditioning, and control stream application, but PR #15860 remains open.

## How to use this

Evaluate the VideoX-Fun MiniMax H3 Fun example alongside MiniMax-H3-Fun-Controlnet-Union starting from 2026-08-24; exact setup and capabilities remain unverified.

1. Clone VideoX-Fun and create `models/Diffusion_Transformer`. Place the MiniMax-H3 base model and `MiniMax-H3-Fun-Controlnet-Union.safetensors` into separate directories as specified in the model card.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
2. In `examples/minimax_h3_fun/predict_v2v_control.py`, set the base model, `minimax_h3_control.yaml`, the control weights path, the control video, and the prompt, then run the script.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
3. For mask editing, run `predict_v2v_control_inpaint.py` instead of the standard control-video script.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
4. On a single 80 GB GPU, enable `model_group_offload` or `model_cpu_offload_and_qfloat8`; do not expect the base transformer and Qwen3-VL to fit together in memory.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>

## Best practices

- Keep `guidance_scale = 1.0`. The checkpoint is guidance-distilled, so higher values reapply guidance and degrade the output.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Keep the control network layout fixed. The configuration must preserve `control_blocks_places: [0, 10, 20, 30, 40]`, `control_in_dim: 49`, and disabled audio control, or weights fail to load.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Start with `control_context_scale = 1.0`. Lower it only to weaken control video tracking; `0.0` disables control conditioning completely.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>
- Check the MiniMax H3 Community License before distribution or hosted use. It excludes EU, UK, Republic of Korea, and USA from Applicable Territory and sets special terms for revenue over USD 20 million annually.
  — <https://huggingface.co/alibaba-pai/MiniMax-H3-Fun-Controlnet-Union/commit/4d670e9e8f1c96b001a8b8ddec0a269de448a1b0>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- `event_findings` and `new_events` were added as object extensions because the task requires them while the system JSON schema omits them.
- Public release of the Hugging Face repository before 2026-08-24 remains unconfirmed; the commit page shows relative time instead of an ISO timestamp.
- PR #15860 in ComfyUI remains open; confirming release support requires an upstream merge or release receipt.

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
- **Practical note:** Evaluate the VideoX-Fun MiniMax H3 Fun example alongside the MiniMax-H3-Fun-Controlnet-Union artifact from 2026-08-24; exact setup and capabilities remain unverified.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.