---
title: PrunaVAED — LTX Video
category: projects
date: 2026-08-03
tags: [ltx-video, ltx_video, project, prunavaed]
aliases: ["PrunaVAED"]
---

# PrunaVAED — LTX Video

**Development line:** `project:prunavaed` · thread `ltx-video`  
**Last event:** 2026-08-03 · 1 dated since 2026-08-03 · **Researched:** 2026-09-05 · confidence: high

## What it is

PrunaVAED is a pruned decoder video VAE for LTX-2.3 that replaces only the decoding of existing LTX-2.3 latents. It keeps the LTX-2.3 encoder and latent format, works with distilled and two-stage LTX-2.3 pipelines, and is not a T2V model, a denoiser or a general-purpose VAE. On an H100 80 GB at bf16 and batch size 1, the authors claim a 1.67–2.08x speedup; measure on other hardware. Practical verdict: a narrow optimization of the LTX-2.3 decode stage, not a way to speed up all generation.

## Development line

- **2026-08-03 — PrunaVAED entered the LTX Video integration thread.** A drop-in decoder for `diffusers/LTX-2.3-Diffusers`, not a new video generator.

## What changed

2026-07-28 — PrunaVAED support was merged into ComfyUI: it requires the converted `pruna_ltx2.3_vae_comfy_bf16.safetensors`, and the PR describes about 2x faster LTX-2.3 decoding. 2026-08-03 — PrunaVAED was recorded as an LTX video development step; primary materials clarify its scope: a drop-in decoder for `diffusers/LTX-2.3-Diffusers`, not a new video generator.

Note on the 2026-08-03 event: the ComfyUI PR is dated 2026-07-28 and was already merged, so this is not a new August integration but an earlier fact that explains the integration state on the event date.

## How to use this

As of 2026-08-03, practitioners should evaluate PrunaVAED from the linked Hugging Face resource and check the linked ComfyUI pull request for integration status before relying on it in an LTX Video workflow.

1. Download the weights repository, install the demo dependencies and run `demo/demo_distilled_decode.py`; it creates videos of the stock LTX-2.3 VAE and PrunaVAED from one latent and prints the decode time.
  — <https://huggingface.co/PrunaAI/PrunaVAED>
2. For LTX-2, download the PrunaVAED weights and the Gemma encoder, then run the distilled pipeline or `ti2vid_two_stages_hq`; for image-to-video add `--image path/to/image.jpg 0 0.8`.
  — <https://huggingface.co/PrunaAI/PrunaVAED>
3. In ComfyUI use the support from the merged PR and the converted bf16 file named by the PR author; replace the video VAE only, not the audio VAE or the transformer.
  — <https://github.com/Comfy-Org/ComfyUI/pull/15129>

## Best practices

- First compare both decoders on the same latent at your target length and resolution: the published numbers come from a single H100 80 GB, bf16, batch size 1.
  — <https://huggingface.co/PrunaAI/PrunaVAED>
- Do not apply the model to arbitrary VAE latents and do not expect bit-exact output; it was verified only on two LTX-2.3 pipelines.
  — <https://huggingface.co/PrunaAI/PrunaVAED>
- Before commercial use or redistribution, check the limits of the LTX-2 Community License Agreement.
  — <https://huggingface.co/PrunaAI/PrunaVAED>

## Superseded by this

- 2026-07-28 — for ComfyUI, the assumption that PrunaVAED needs only an external custom-node solution is outdated: support was merged in ComfyUI PR #15129.
- 2026-08-03 — the description of PrunaVAED as a full video-generation model is outdated: the current model card explicitly limits its role to the decoder for LTX-2.3.

## Still unknown

- The model card does not give the original publication date of the repository, so the date the weights were opened cannot be reliably matched to the 2026-08-03 event.
- No independent benchmark on consumer GPUs exists; the stated speed and VRAM figures are confirmed only by the author's test on an H100 80 GB.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/PrunaAI/PrunaVAED | PrunaAI/PrunaVAED model card | 2026-09-05 |
| https://github.com/Comfy-Org/ComfyUI/pull/15129 | Support PrunaVAED (faster LTX2.3 decoder) — ComfyUI pull request #15129 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:prunavaed`, thread `ltx-video`, 1 dated events 2026-08-03 → 2026-08-03.
- **Practical note:** As of 2026-08-03, practitioners should evaluate PrunaVAED from the linked Hugging Face resource and check the linked ComfyUI pull request for integration status before relying on it in an LTX Video workflow.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
