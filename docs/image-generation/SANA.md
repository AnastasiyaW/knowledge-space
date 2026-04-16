---
title: SANA
category: models
tags: [text-to-image, dit, flow-matching, efficient, 1.6b, 600m, 4.8b, linear-attention, dc-ae, litela, mix-ffn, gemma, nvlabs, jewelry-retouching]
aliases: ["SANA 1.5", "SANA 1.6B", "SANA-Sprint", "SANA-Video"]
---

# SANA (Efficient High-Resolution Image Synthesis)

Efficient DiT from NVlabs/MIT Han Lab. 600M-4.8B params with competitive quality at 1024-4096px. Uses **linear attention O(n)**, **DC-AE 32× compression**, and **Gemma-2-2B** text encoder. ICLR 2025 Oral.

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

## SANA-Video

Block Causal Linear Attention + Causal Mix-FFN for video. 2B params, 720p, up to 1 min, 16 FPS. **52× faster** than Wan-2.1-14B (36s vs 1897s for 5s clip). VBench: 84.05 vs Wan: 83.73.

Key for [[temporal-tiling]]: SANA-Video's causal attention = same mechanism needed for tiles-as-frames.

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

## License

**Code: Apache 2.0. Weights: NSCL v2-custom** (check specific terms for commercial use).

## Key Links

- GitHub: github.com/NVlabs/Sana
- HF: huggingface.co/Efficient-Large-Model/
- Papers: arxiv.org/abs/2410.10629 (SANA), 2501.18427 (1.5), 2503.09641 (Sprint)
- SANA-Video: arxiv.org/abs/2509.24695
- DC-AE: github.com/mit-han-lab/efficientvit
- Training framework: happyin-research/sana-fm/ (local)
