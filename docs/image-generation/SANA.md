---
title: SANA
category: models
tags: [text-to-image, dit, flow-matching, efficient, 1.6b, 600m, 4.8b, linear-attention, dc-ae, litela, mix-ffn, gemma, nvlabs, jewelry-retouching]
aliases: ["SANA 1.5", "SANA 1.6B", "SANA-Sprint", "SANA-Video"]
---

# SANA (Efficient High-Resolution Image Synthesis)

Efficient DiT from NVlabs/MIT Han Lab. 600M-4.8B params with competitive quality at 1024-4096px. Uses **linear attention O(n)**, **DC-AE 32× compression**, and **Gemma-2-2B** text encoder. ICLR 2025 Oral.

## Current Status (Verified 2026-08-27)

The SANA name now covers several related but non-interchangeable branches. Select the artifact before applying performance, memory, or licensing claims.

| Branch | Current artifact state | Intended use |
|---|---|---|
| SANA / SANA 1.5 / Sprint | Released image-generation code and checkpoints | Text-to-image and image refinement |
| SANA-Video (2025) | Released research implementation; Diffusers integration followed | Earlier causal video generation |
| SANA-WM (2026) | Released 2.6B world-model branch | 720p interactive/world simulation, up to one minute, 6-DoF control |
| SANA-Video2 (2026) | Training/inference code and **5B 720p checkpoint released 2026-08-19** | Current 720p video generation |
| SANA-Video2 14B | Architecture/config discussed, but no 14B checkpoint in the official repository | Research reference only; do not select for a runnable recipe |

The August 4, 2026 report that Video2 had no public weights was accurate at the time and is now **superseded** for the 5B model. It remains accurate for the 14B checkpoint as of this verification date.

The official Video2 page reports a 5-second, 720p, 40-step 5B benchmark on one H100, including a 13.06-second Sol Engine result. Treat this as a pinned benchmark context, not a consumer-GPU runtime estimate.

## Architecture — Full Detail

### Model Variants

| Variant | Params | Depth | Hidden | Heads | FFN (2.5× MLP) |
|---------|--------|-------|--------|-------|----------------|
| Sana-0.6B | 590M | 28 blocks | 1152 | 16 | 2880 |
| Sana-1.6B | 1604M | 20 blocks | 2240 | 20 | 5600 |
| Sana-1.5 4.8B | 4800M | 60 blocks | 2240 | 20 | 5600 |

0.6B = deeper but narrower. 1.6B = shallower but wider. 4.8B scales ONLY depth (20→60), width same as 1.6B.

### SanaBlock Structure (AdaLN-Zero)

```bash
Input x → LayerNorm → modulate(shift1, scale1) → Linear Self-Attention (LiteLA)
        → LayerNorm → modulate(shift2, scale2) → Cross-Attention (standard, with text)
        → LayerNorm → modulate(shift3, scale3) → Mix-FFN (GLUMBConv)
Output x (residual at each stage, 6 modulation params per block via scale_shift_table)
```

### Linear Attention (LiteLA with ReLU Kernel)

```python
# Standard quadratic: O(N^2)
# Attention = softmax(QK^T / sqrt(d)) * V

# SANA linear: O(N * d^2)
# phi(x) = ReLU(x)
# Shared terms: S = sum_j phi(K_j)^T * V_j   (shape d×d, computed ONCE)
#               Z = sum_j phi(K_j)^T          (shape d×1, computed ONCE)
# Output_i = phi(Q_i) * S / (phi(Q_i) * Z + eps)
```

**Trade-off:** linear attention alone degrades quality. Compensated by Mix-FFN with 3×3 depthwise convolution that captures local spatial info lost by ReLU kernel (no softmax locality bias).

**Triton kernel fusion:** ReLU activation + precision conversions + padding + division fused into matmul → ~10% speed acceleration.

**Position encoding:** "NoPE" (No Positional Embeddings) — 3×3 depthwise conv in Mix-FFN implicitly encodes position. Alternatively supports RoPE `theta=10000, axes_dim=[0,16,16]`.

### Mix-FFN (GLUMBConv)

Replaces standard MLP:
```text
Linear(d → d×2.5) → DW-Conv3×3 → SiLU → Gate (GLU) → Linear(d×1.25 → d)
```
The 3×3 depthwise conv = key to making linear attention work. Provides local receptive field that ReLU linear attention lacks.

### DC-AE (Deep Compression Autoencoder) — F32C32P1

**32× spatial compression, 32 latent channels, patch size 1.**

| Resolution | SD/FLUX (F8, P2) tokens | SANA (F32, P1) tokens | Reduction |
|-----------|-------------------------|------------------------|-----------|
| 512×512 | 1024 | **256** (16×16) | 4× |
| 1024×1024 | 4096 | **1024** (32×32) | 4× |
| 2048×2048 | 16384 | **4096** (64×64) | 4× |
| 4096×4096 | 65536 | **16384** (128×128) | 4× |

4× fewer tokens + O(n) linear attention = **orders of magnitude** faster at high res.

Reconstruction quality (ImageNet): rFID 0.34, PSNR 29.29, SSIM 0.84, LPIPS 0.05.

**Tiling supported:** `pipe.vae.enable_tiling(tile_sample_min_height=1024, tile_sample_min_width=1024)` — enables 4K within 22 GB VRAM.

Two versions: `dc-ae-f32c32-sana-1.0`, `dc-ae-f32c32-sana-1.1` (improved), `dc-ae-lite-f32c32` (faster/smaller).

### Text Encoder: Gemma-2-2B-IT

Decoder-only LLM (not T5). 6× faster than T5-XXL. Max 300 tokens.

**Critical:** decoder-only outputs have variance orders of magnitude larger than T5. Solution: **RMSNorm** after encoder + learnable scale 0.01 (`y_norm: true, y_norm_scale: 0.01`).

**Complex Human Instruction (CHI):** leverages Gemma's in-context learning → +2.2 GenEval points.

## Training

### Loss & Scheduler

[[flow-matching]] velocity prediction: `v_theta(x_t, t) = epsilon - x_0`. Timestep sampling: logit-normal (mean=0.0, std=1.0). Flow shift: 3.0.

### Optimizer: CAME

```yaml
optimizer: CAMEWrapper
lr: 1e-4
betas: [0.9, 0.999, 0.9999]
epsilon: [1e-30, 1e-16]
weight_decay: 0.0
grad_clip: 0.1
warmup: 2000 steps, constant after
```

SANA 1.5 uses **CAME-8bit** — block-wise 8-bit first-order moments, 32-bit second-order. 25% memory reduction vs AdamW.

### Resolution Schedule

Skip 256px entirely. Start at 512px → finetune to 1024 → 2K → 4K.

### Multi-Caption Labeling

4 VLMs generate captions (VILA-3B, VILA-13B, InternVL2-8B, InternVL2-26B). CLIP-score sampler selects per iteration.

### SFT: 3M samples filtered by CLIP > 25 from 50M pre-training set.

## SANA 1.5 Key Improvements

1. **Depth-growth paradigm (1.6B → 4.8B):** remove last 2 blocks of trained 1.6B → add 40 new blocks with Partial Preservation Init (identity mappings) → 60% fewer training steps
2. **QK-normalization:** RMSNorm on Q,K for stable large-model training
3. **Depth pruning:** block importance metric → prune middle blocks, keep head/tail → quick recovery with ~100 fine-tune steps
4. **Inference-time scaling:** generate N candidates, select best via VILA-Judge (fine-tuned NVILA-2B). GenEval: 0.81 → **0.96** with 2048 candidates. 1.6B + scaling **outperforms** 4.8B without

## Benchmarks

| Model | Params | FID↓ | CLIP↑ | GenEval↑ | Speed (A100) |
|-------|--------|------|-------|----------|-------------|
| FLUX-dev | 12.0B | 10.15 | 27.47 | 0.67 | 0.04 img/s |
| SD3-medium | 2.0B | 11.92 | 27.83 | 0.62 | 0.28 img/s |
| **Sana-0.6B** | 0.6B | **5.81** | 28.36 | 0.64 | **1.7 img/s** |
| **Sana-1.6B** | 1.6B | **5.76** | 28.67 | 0.66 | **1.0 img/s** |
| **Sana-1.5 1.6B** | 1.6B | 5.70 | 29.12 | **0.82** | 1.0 img/s |
| **Sana-1.5 4.8B** | 4.8B | 5.99 | 29.23 | 0.81 | 0.26 img/s |

Sana-1.6B = **23× faster** than FLUX-dev. At 4K: **106× faster** (9.6s vs 469s).

## SANA-Sprint (Distilled, 1-4 Steps)

Hybrid distillation: sCM (continuous consistency) + LADD (latent adversarial).

| Steps | FID | GenEval | Latency (H100) |
|-------|-----|---------|-----------------|
| 1 | 7.04 | 0.72 | **0.1s** |
| 2 | 6.76 | — | 0.24s |
| 4 | 6.48 | 0.76 | 0.32s |

Outperforms FLUX-schnell (7.94 FID) while 10× faster. ICCV 2025 Highlight.

## SANA Video and World-Model Branches

### SANA-Video (2025 generation)

The original video branch introduced Block Causal Linear Attention and Causal Mix-FFN. Its reported 2B/720p/16 FPS results belong to that release and must not be copied onto Video2 or SANA-WM.

Key for [[temporal-tiling]]: causal attention is structurally relevant to tiles-as-frames, but this is an architectural analogy rather than a supported SANA workflow.

### SANA-WM (2026 world model)

SANA-WM is a 2.6B interactive world model rather than a rename of SANA-Video. The official project describes 720p generation, sequences up to one minute, and 6-DoF camera control. Validate controller format and checkpoint license against the exact release before integration.

### SANA-Video2 (2026 generation)

Video2 is the current generation branch. The official repository added training code, inference code, architecture details, and a 5B 720p checkpoint on 2026-08-19. A 14B variant is described but is not a runnable public checkpoint in the repository.

The project-page paper benchmark and the released-checkpoint guide use different run shapes:

| Context | Frames/duration | FPS | Steps | Purpose |
|---|---|---:|---:|---|
| Project-page H100 benchmark | 5-second clip | Not a released-recipe default | 40 | Paper/engine comparison only |
| Public 5B checkpoint guide | 193 frames / approximately 8.04 seconds | 24 | 50 | Current released-checkpoint example |

For a reproducible released-checkpoint evaluation, start from the public guide and record:

```yaml
artifact: SANA-Video2-5B
revision: <immutable-checkpoint-or-repository-revision>
resolution: 720p
frames: 193
fps: 24
duration_seconds: 8.04
steps: 50
gpu: <exact-model>
engine: <official-or-baseline-runtime>
seed: <integer>
refiner_enabled: <true-or-false>
```

Do not substitute the 14B label into this recipe. Use 5 seconds/40 steps only when reproducing the paper benchmark, not as the public-checkpoint default. Do not compare H100 timing to a local GPU without measuring the same frames/duration, resolution, steps, runtime, and refiner state.

## VRAM

| Config | VRAM |
|--------|------|
| 0.6B 1024px bf16 | ~16 GB |
| 1.6B 1024px bf16 | ~16-24 GB |
| 4K with VAE tiling | ~22 GB |
| 4K + 4-bit quant + offload | **< 8 GB** |
| W8A8 quantized 1024px | Very low, 0.37s on 4090 |

## Fine-Tuning / LoRA

Official support via diffusers `train_dreambooth_lora_sana.py`. See [[diffusion-lora-training]] for full training pipeline details.

**LoRA targets:** `attn.to_k, attn.to_q, attn.to_v, attn.to_out.0` + optionally FFN/MLP.

**Settings:** LR 1e-4, 500 steps, batch 1, grad accum 4, bf16. Requires peft >= 0.14.0.

**Dataset requirements:**
- DreamBooth (subject): 3-5 images minimum
- Style/domain LoRA: 20-30 images recommended
- Format: 1024x1024+ resolution, detailed captions with rare trigger token ("sks")

**Memory optimization flags:** `--offload` (CPU offload text encoder + VAE), `--cache_latents` (precompute VAE latents), `--use_8bit_adam`.

**ControlNet** also supported — ControlNet-Transformer architecture for SANA backbone.

### Self-Refinement (img2img)

SANA-Sprint supports img2img via `SanaSprintImg2ImgPipeline`:

```python
from diffusers import SanaSprintImg2ImgPipeline
import torch

pipe = SanaSprintImg2ImgPipeline.from_pretrained(
    "Efficient-Large-Model/Sana_Sprint_1.6B_1024px_diffusers",
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")

# Multi-pass refinement (replaces SDXL refiner pattern)
refined = pipe(
    prompt="a high quality detailed photo",
    image=initial_image,
    strength=0.3,            # 0.3 = mild refinement, 0.7 = heavy change
    num_inference_steps=4    # Sprint is 1-4 steps
).images[0]
```

**Flow matching img2img mechanics:** SANA uses flow matching, not DDPM. `strength` parameter interpolates between the encoded input image and pure noise: `x_t = (1-strength)*image_latent + strength*noise`. This differs from DDPM's noise scheduling - there is no "add noise then denoise" step, it's direct interpolation.

**Multi-pass recipe:**
```text
txt2img 1024px (strength=1.0) → img2img strength=0.3-0.4 → img2img strength=0.2
```

**SDXL refiner has no flow matching equivalent**: SDXL refiner uses high-timestep sampling which is DDPM-specific. SANA's img2img is the functional replacement but works differently under the hood.

**DemoFusion incompatible with SANA**: DemoFusion relies on UNet skip connections for multi-scale global context. SANA's transformer architecture doesn't have these. Use FreeScale or APT for high-res tiling instead.

See [[flow-matching]] for full details on flow matching img2img.

## Development History

| Date | Branch | Event | Temporal status |
|---|---|---|---|
| 2024-10-22 | SANA image | Repository/project surfaced publicly | Historical discovery |
| 2024-11-21 | SANA image | Training, inference, metrics code, and 1.6B models available | Current foundation |
| 2025-10-01 | SANA-Video | Preview reported | Superseded by released implementation |
| 2025-10-27 | SANA-Video | Official release | Historical/current for that branch |
| 2025-11-06 | SANA-Video | Diffusers integration reported by the project | Current integration history |
| 2025-12-24 | SANA-Video | Code/checkpoint availability reported | Superseded by later branches, retained |
| 2026-03 | SANA image/video tooling | 720p LTX-VAE path and LTX2 refiner-to-2K update | Current only for that pipeline |
| 2026-05 | SANA-WM | 2.6B world-model branch published | Current branch |
| 2026-08-04 | SANA-Video2 | Announcement observed without weights | Superseded for 5B on 2026-08-19 |
| 2026-08-19 | SANA-Video2 | Code plus 5B 720p checkpoint released | Current |

## Practical Selection

- Use SANA/SANA 1.5 for efficient image generation and documented image LoRA workflows.
- Use Sprint only when its one-to-four-step distilled behavior is explicitly desired; do not reuse standard step counts.
- Use SANA-Video2 5B for the current official runnable Video2 path.
- Use SANA-WM only for interactive/world-model experiments with its own controller contract.
- Do not plan a 14B Video2 deployment until an official checkpoint and license are present.

## Research Coverage and Open Gaps

- English primary evidence: official repository, official Video2 project page, and papers.
- Chinese query lane: searched, but no qualified first-party Chinese source was retained in the bounded pass.
- Open proof gap: a fully reproducible consumer-GPU matrix pinned to checkpoint hashes, runtime versions, and refiner state.
- Community performance reports remain secondary until reproduced with the same settings.

### Community reports

- [Issue #156](https://github.com/NVlabs/Sana/issues/156) reports a community 1.6B training path on 24 GB using offload. The contributor explicitly called the patch messy; an official contributor pointed to the project's CAME-8bit configuration as a better memory-saving direction. Treat the issue as a technique lead, not a drop-in recipe.
- [Issue #297](https://github.com/NVlabs/Sana/issues/297) records an unresolved MacBook Pro M3/MPS case where `Sana_600M_512px_diffusers` with `float16` produced a uniform gray image without an exception. Test `float32` as a diagnostic, but no maintainer-confirmed fix was present.
- Neither issue concerns the released Video2 5B checkpoint. Do not transfer their image-model settings to Video2.

## Gotchas

- **Issue:** Treating “SANA-Video” as one continuously versioned checkpoint -> **Fix:** record the branch (`Video`, `WM`, or `Video2`), model size, checkpoint revision, and release date.
- **Issue:** Selecting Video2 14B because it appears in architecture tables -> **Fix:** use the released 5B checkpoint; 14B is not a public runnable artifact as of 2026-08-27.
- **Issue:** Repeating the August 4 “no weights” statement as current -> **Fix:** mark it superseded by the August 19 5B release while retaining it as historical context.
- **Issue:** Generalizing H100 latency or old 2B video benchmarks -> **Fix:** preserve hardware, engine, duration, resolution, steps, and branch in every comparison.
- **Issue:** Using the paper's 5-second/40-step benchmark as the released-checkpoint recipe -> **Fix:** start from the public guide's 193 frames, 24 FPS, and 50 steps unless intentionally reproducing the benchmark.
- **Issue:** Applying an image-model offload/MPS workaround to Video2 -> **Fix:** require the exact branch, checkpoint, issue URL, and runtime before reuse.

## Agent Brief

When answering a SANA question, first identify `image`, `Sprint`, `Video`, `WM`, or `Video2`. Prefer the official repository and project page over news summaries. Return historical claims with a temporal label (`current`, `superseded`, or `unknown`). Never recommend Video2 14B as downloadable unless a newer first-party checkpoint is verified. For deployment advice, request or report the exact artifact revision, GPU, runtime, resolution, duration, steps, and refiner state.

## License

**Code: Apache 2.0. Weights: NSCL v2-custom** (check specific terms for commercial use).

## Key Links

- GitHub: https://github.com/NVlabs/Sana
- SANA-Video2: https://nvlabs.github.io/Sana/Video2/
- Released Video2 checkpoint guide: https://github.com/NVlabs/Sana/blob/main/docs/sana_video2.md
- Community offload report: https://github.com/NVlabs/Sana/issues/156
- Open MPS gray-output report: https://github.com/NVlabs/Sana/issues/297
- HF: https://huggingface.co/Efficient-Large-Model/
- Papers: https://arxiv.org/abs/2410.10629 (SANA), https://arxiv.org/abs/2501.18427 (1.5), https://arxiv.org/abs/2503.09641 (Sprint)
- SANA-Video: https://arxiv.org/abs/2509.24695
- DC-AE: https://github.com/mit-han-lab/efficientvit
- Training framework: happyin-research/sana-fm/ (local)
