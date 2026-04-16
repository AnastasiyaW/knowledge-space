---
title: Step1X-Edit
category: models
tags: [image-editing, step1x, stepfun, mmdit, flow-matching, qwen-vl, open-source, apache-2.0]
aliases: ["Qwen-Image-Edit", "Qwen-Image-Edit-2511"]
---

# Step1X-Edit

Open-source image editing foundation model by **StepFun** (Shanghai). De facto standard open backbone for instruction-based image editing (2025-2026). Qwen-Image-Edit-2511 by Alibaba/Qwen is a production-tuned variant of this architecture.

## Architecture

```text
Input Image → VAE Encode → image latent (z)
Text Instruction → Qwen 2.5 VL → text embeddings (c)
                         ↓
              MMDiT Transformer Blocks
         (joint attention over z and c)
                         ↓
              VAE Decode → edited image
```

Three core components:

| Component | Implementation | Trainable? | Size |
|-----------|---------------|------------|------|
| Text Encoder | **Qwen 2.5 VL** (vision-language model) | Yes (usually) | ~7B params |
| Transformer | [[MMDiT]] with joint attention | Yes / LoRA | ~20B+ params |
| VAE | Custom autoencoder (RealRestorerAutoencoderKL variant) | Usually frozen | ~200M params |

Total weights: **~40-60 GB** in bf16 depending on variant.

### Why Qwen VL instead of CLIP

Previous editing models (InstructPix2Pix, MagicBrush) used CLIP as text encoder. CLIP encodes text only — it cannot "see" the input image at encoding time. Qwen 2.5 VL is a full vision-language model:
- Processes both the text instruction AND the input image
- Understands spatial relationships ("move the cup to the left")
- Reasons about what to change vs what to preserve
- Generates richer conditional embeddings

This is the key architectural innovation that separates Step1X-Edit generation models from prior approaches.

### Scheduler

Uses [[flow-matching]] instead of DDPM/DDIM. Default inference: 28 steps, guidance_scale 3.0. Faster convergence, more stable at low step counts.

## Variants

| Model | Maintainer | License | Notes |
|-------|-----------|---------|-------|
| Step1X-Edit | StepFun | Apache 2.0 | Original |
| Qwen-Image-Edit-2511 | Alibaba/Qwen | Apache 2.0 | Production variant, DiffSynth-Studio framework |
| RealRestorerTransformer2DModel | RealRestorer team | Academic only (weights) | Modified for restoration |

## Inference

```python
from diffsynth import QwenImageEditPlusPipeline
pipe = QwenImageEditPlusPipeline.from_pretrained("Qwen/Qwen-Image-Edit-2511", torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()
result = pipe(prompt="change the background to a beach", image=input_image, num_inference_steps=28, guidance_scale=3.0)
```

**VRAM**: ~40 GB at 1024x1024 in bf16. With CPU offload — fits on 24 GB but slower. FP8 quantization → ~20-30 GB.

## Downstream Models Built on This Architecture

- [[RealRestorer]] — image restoration (9 degradation types)
- [[PixelSmile]] — facial expression editing (LoRA rank 64, 850 MB)
- [[MACRO]] Qwen variant — multi-reference generation (full fine-tune)

## Commercial Use

**Apache 2.0** — fully permitted for commercial use. Both Step1X-Edit and Qwen-Image-Edit-2511. This makes it the go-to backbone for commercial editing products, unlike models with NC restrictions.

## Key Links

- Step1X-Edit GitHub: github.com/stepfun-ai/Step1X-Edit
- Qwen-Image-Edit HF: huggingface.co/Qwen/Qwen-Image-Edit-2511
- Framework: DiffSynth-Studio (github.com/modelscope/DiffSynth-Studio)
