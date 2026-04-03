---
title: LoRA Fine-Tuning for Editing Models
category: techniques
tags: [lora, fine-tuning, mmdit, qwen-image-edit, step1x-edit, peft, commercial, training-recipe]
---

# LoRA Fine-Tuning for Editing Models

Practical patterns for applying LoRA adapters to [[MMDiT]]-based editing models ([[Step1X-Edit]], Qwen-Image-Edit-2511). Demonstrated by [[PixelSmile]] — 850 MB LoRA adds entirely new capability (expression control) to a 60 GB base model.

## Standard Recipe

### Target Modules

Full MMDiT coverage (maximum expressivity):

```python
target_modules = [
    # Image-stream attention
    "to_q", "to_k", "to_v", "to_out.0",
    # Text-stream attention
    "add_q_proj", "add_k_proj", "add_v_proj", "to_add_out",
    # Image FFN
    "img_mlp.net.0.proj", "img_mlp.net.2",
    # Text FFN
    "txt_mlp.net.0.proj", "txt_mlp.net.2",
]
```

### Hyperparameters (PixelSmile reference)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Rank | 64 | Higher than typical (32 works for simpler tasks) |
| Alpha | 128 | 2x rank is standard |
| Dropout | 0 | Common for diffusion LoRA |
| LR | 1e-4 | Cosine schedule |
| Batch | 4/GPU | On H200 |
| Epochs | 100 | Expression task; simpler tasks need fewer |
| Hardware | 4x H200 | Or 4x A100-80GB |
| LoRA size | 850 MB | For rank 64, all targets |

### What to Freeze

- **VAE**: always frozen (autoencoder doesn't need task-specific adaptation)
- **Text encoder**: depends on task. PixelSmile trains it (needs new text→expression mapping). For style transfer, often frozen.
- **Transformer**: LoRA applied here is the core of the adaptation

## Lighter Alternatives

| Coverage | Targets | LoRA Size | Use When |
|----------|---------|-----------|----------|
| Full (PixelSmile) | All attn + all FFN | ~850 MB | New behavior (expressions, restoration) |
| Attention-only | to_q/k/v + add_q/k/v + out | ~500 MB | Style transfer, composition |
| Image-stream only | to_q/k/v + img_mlp | ~350 MB | Visual-only changes (no text reinterpretation) |

Reducing to attention-only drops ~40% LoRA size. Image-stream-only cuts ~60% but loses text conditioning adaptation.

## Training Data Patterns

### Synthetic Generation (PixelSmile approach)
1. Collect base identities from public datasets
2. Generate variations via strong API model (Nano Banana Pro)
3. Annotate with continuous scores via VLM (Gemini 3 Pro)
4. Train LoRA on synthetic pairs

### Full Fine-Tune vs LoRA (MACRO comparison)
[[MACRO]] uses **full fine-tune** (not LoRA) because the task (multi-reference at 6-10 images) requires deep architectural adaptation. LoRA is sufficient when the base model already has the capability but needs behavioral steering.

**Rule of thumb**: if the base model can do the task poorly → LoRA. If it fundamentally can't → full fine-tune.

## Loss Functions for Editing LoRA

Standard [[Flow Matching]] velocity loss + task-specific auxiliary losses:

| Loss | Purpose | Lambda | Used By |
|------|---------|--------|---------|
| Flow Matching (L_FM) | Core generation quality | 1.0 | All |
| Identity (ArcFace cosine) | Face preservation | 0.1 | [[PixelSmile]] |
| Symmetric Contrastive | Distinguish similar outputs | 0.05 | [[PixelSmile]] |
| LPIPS | Perceptual similarity | varies | [[RealRestorer]] |

## Commercial Viability

Base model (Qwen-Image-Edit-2511) is **Apache 2.0**. Your LoRA weights are entirely yours. This creates a clean commercial path:

```
Apache 2.0 base (Qwen) + proprietary LoRA = your product
```

No license contamination from base model. LoRA weights are your IP.

## Gotchas

- Qwen-Image-Edit requires **DiffSynth-Studio** framework, not standard diffusers. LoRA loading path differs.
- PixelSmile requires a diffusers **patch script** (`patch_qwen_diffusers.sh`).
- At rank 64+, LoRA training on 60GB base needs 4x 80GB GPUs. Lower rank (16-32) fits on 2x A100.
- EMA (exponential moving average) on LoRA weights recommended for stability — PixelSmile uses it.
- Data quality matters more than data quantity — synthetic data with VLM scoring outperforms larger messy datasets.
