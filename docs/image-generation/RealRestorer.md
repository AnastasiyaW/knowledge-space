---
title: RealRestorer
category: models
tags: [image-restoration, step1x-edit, deblur, denoise, dehaze, derain, compression-artifacts, low-light, moire, flare, reflection, non-commercial]
---

# RealRestorer

Image restoration model built on [[Step1X-Edit]]. Handles 9 degradation types via text-prompted editing. Ranks 1st among open-source restoration models, 3rd overall (behind Nano Banana Pro and GPT-Image-1.5).

Paper: arXiv:2603.25502 (March 2026). Authors: Southern University of Science and Technology + StepFun + Shenzhen Institutes of Advanced Technology.

## Architecture

Inherits [[Step1X-Edit]] architecture with custom modifications:

| Component | Class | Notes |
|-----------|-------|-------|
| Text Encoder | Qwen2_5_VLForConditionalGeneration | Standard **Qwen 2.5 VL** |
| Transformer | RealRestorerTransformer2DModel | Modified Step1X-Edit transformer |
| VAE | RealRestorerAutoencoderKL | Custom autoencoder |
| Scheduler | RealRestorerFlowMatchScheduler | [[Flow Matching]] |

Key insight: large-scale editing models already have strong generalization for restoration tasks — they understand "fix this" instructions. RealRestorer fine-tunes specifically for degradation removal.

## Supported Degradation Types

Prompt-driven — specify degradation type in text:

| Type | English Prompt | Chinese Prompt |
|------|---------------|----------------|
| Blur | "Remove blur" | "去除模糊" |
| Compression | "Remove compression artifacts" | "去除压缩伪影" |
| Moire | "Remove moire patterns" | "去除摩尔纹" |
| Low-light | "Enhance low-light image" | "增强低光照图像" |
| Noise | "Remove noise" | "去除噪点" |
| Flare | "Remove lens flare" | "去除镜头光晕" |
| Reflection | "Remove reflections" | "去除反射" |
| Haze | "Remove haze" | "去除雾霾" |
| Rain | "Remove rain" | "去除雨滴" |

## Benchmark (RealIR-Bench)

464 real-world degraded images. Metric: `FS = 0.2 * VLM_Score_Diff * (1 - LPIPS)`.

| Model | Open Source | Final Score |
|-------|-----------|-------------|
| Nano Banana Pro | No | 0.153 |
| GPT-Image-1.5 | No | 0.150 |
| **RealRestorer** | **Yes** | **0.146** |
| Qwen-Image-Edit-2511 | Yes | 0.127 |
| FLUX.1-Kontext-dev | Yes | 0.056 |

## Inference

```python
# Requires patched diffusers fork (not PyPI)
pipe = RealRestorerPipeline.from_pretrained("RealRestorer/RealRestorer", torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()
result = pipe(prompt="Remove blur from this image", image=degraded, num_inference_steps=28, guidance_scale=3.0)
```

**VRAM**: ~34 GB at 1024x1024 in bf16. Requires flash-attn 2.7.2.

## Gotchas

- Requires their **forked diffusers** — not pip-installable. Must clone and install locally.
- Checkpoint versions v1.0 and v1.1 exist — use latest.
- Qwen-Image-Edit-2511 variant (without RealRestorer fine-tune) already scores 0.127 on same benchmark — the delta from fine-tuning is +15%.
- Upcoming: Qwen-Image-Edit-2511 version (different from current Step1X-Edit base).

## License

| Component | License |
|-----------|---------|
| Code | Apache 2.0 |
| Weights (~41.8 GB) | **Non-commercial academic research only** |
| RealIR-Bench | Academic |

> HuggingFace metadata says apache-2.0 but README explicitly restricts weights to non-commercial. **Cannot use commercially.**

## Key Links

- GitHub: github.com/yfyang007/RealRestorer
- HF weights: huggingface.co/RealRestorer/RealRestorer
- HF benchmark: huggingface.co/datasets/RealRestorer/RealIR-Bench
- Demo: huggingface.co/spaces/dericky286/RealRestorer-Demo
