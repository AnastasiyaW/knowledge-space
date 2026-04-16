---
title: FLUX.2 Klein Character / Identity LoRA
category: techniques
tags: [lora, training, klein, character, identity, face, proportion, pulid]
aliases: ["Klein Character LoRA", "Klein Identity LoRA", "Klein Person LoRA"]
---

# FLUX.2 Klein Character / Identity LoRA

Training LoRAs to preserve a specific person's identity with FLUX.2 Klein 9B. Covers optimizer requirements, caption strategy, proportion fixes, and inference-time enhancement.

## Dataset Requirements

| Parameter | Value | Notes |
|-----------|-------|-------|
| Minimum images | 8-12 | Well-curated beats quantity |
| Composition mix | 1/3 / 1/3 / 1/3 | Headshots / half-body / full-body |
| Lighting variety | Required | At least 3 different setups |
| Background variety | Recommended | Helps generalization |
| Resolution | 1024px | Match training resolution |

**Minimal path (DiffSynth-Studio, 4B):** 8-12 images, 900-1500 steps on Klein 4B — works with 16GB VRAM.

## Optimizer and Hyperparameters

**adafactor FAILS on Klein 9B for character training.** This is a known issue — adafactor's adaptive scaling does not converge correctly for identity preservation, causing the face to collapse to a generic average by ~1K steps.

```toml
# diffusion-pipe config (recommended)
[optimizer]
type = 'AdamW8bitKahan'
lr = 1e-4
betas = [0.9, 0.999]
weight_decay = 0.01
```

### RunComfy Standard Recipe

| Parameter | Value |
|-----------|-------|
| Optimizer | adamw8bit |
| LR | 1e-4 |
| Steps | 2K-4K (character) / 7K (style) |
| Network dims | 16-32 (conservative) |
| Repeats | 90-120 per image |
| Precision | fp8 for model, bf16 for LoRA |

### Herbst Recipe (50+ runs, maximum quality)

| Parameter | Value |
|-----------|-------|
| Network dims | 128/64/64/32 (linear/linear_alpha/conv/conv_alpha) |
| Weight decay | 0.00001 |
| Steps | 7K (also works for character at this rank) |
| LR | 1e-4 (constant, no decay) |
| LR schedule | constant |

## Caption Strategy

The captioning strategy for identity LoRA is counter-intuitive:

**Rule: describe scene and pose, NEVER describe face features.**

```yaml
# CORRECT - identity stored in LoRA weights
"jane_doe, standing in sunlit garden, casual jeans and white blouse,
 three-quarter view, bokeh background"

"jane_doe, seated at cafe table, morning coffee, side profile,
 warm natural light from window"

# WRONG - identity leaks into text space
"jane_doe, brown eyes, oval face, sharp cheekbones, dark wavy hair,
 smiling, studio lighting"
```

**Why this works:** The model learns to associate everything NOT described in the caption with the trigger token. Face features described in text get anchored to text tokens, making the LoRA rely on prompting rather than being self-contained.

### Trigger Word Placement

Always put trigger word **first** in caption:

```
{trigger_word}, [scene], [background], [lighting], [pose/framing]
```

No comma after trigger word is needed; sentence-style captions work fine.

## Proportion Issues Fix (Big Heads Problem)

### Cause

Two compounding factors:
1. **Dataset bias**: if 90% of training images are headshots, the model associates the identity trigger with headshots
2. **Distillation artifacts**: Klein distilled variant has built-in head-emphasis from its training data

### Fix: 1/3 Composition Rule

```
Dataset breakdown:
- 33% close shots (shoulders up)
- 33% half-body (waist up)
- 33% full-body
```

### Caption Composition Explicitly

```yaml
"jane_doe, full body shot, standing, arms at sides, white studio"
"jane_doe, half body, seated at desk, hands visible on table"
"jane_doe, close portrait, turned slightly to camera"
```

Explicitly naming the framing in captions reinforces the proportion distribution.

### Two-Stage Training Workaround

If composition fix alone doesn't resolve artifacts:
1. **Stage 1**: Train character LoRA on curated 1/3 dataset (as above)
2. **Stage 2**: Short fine-tune (500-1K steps) on full-body only images at lower LR (5e-5)

## Inference Enhancement: PuLID-Flux2

PuLID-Flux2 boosts identity consistency at inference without retraining:

```python
# PuLID-Flux2 pipeline
from pulid_flux2 import PuLIDPipeline

pipe = PuLIDPipeline.from_pretrained("flux-2-klein-base-9b")
pipe.load_lora("my_character_lora.safetensors")

result = pipe(
    prompt="jane_doe in Paris cafe",
    id_images=["ref1.jpg", "ref2.jpg"],  # up to 8 references
    id_weight=0.8,                        # 0.5-1.0
    num_inference_steps=20,
)
```

**Mechanism**: InsightFace face analysis + EVA-CLIP visual features → identity tokens injected into Klein double blocks via cross-attention. Multi-reference via 3D RoPE time offsets (separate temporal position per reference).

| References | Quality Gain | VRAM Cost |
|-----------|-------------|-----------|
| 1 | Baseline boost | +2GB |
| 3-4 | Best balance | +4GB |
| 8 | Maximum | +8GB (sequence limit risk) |

## ai-toolkit Config Snippet

```yaml
# ai-toolkit character LoRA
job: extension
config:
  name: "klein_character_jane"
  process:
    - type: standard_training
      network:
        type: lora
        linear: 32
        linear_alpha: 32
      train:
        optimizer: adamw8bit
        lr: 1e-4
        steps: 3000
        batch_size: 1
        gradient_accumulation_steps: 2
        gradient_checkpointing: true
      model:
        name_or_path: "flux-2-klein-base-9b"
        is_flux: true
        quantize: true  # fp8
      datasets:
        - folder_path: "data/jane_doe/"
          caption_ext: txt
          num_repeats: 100
```

## Gotchas

- **adafactor convergence failure**: switching from adafactor to adamw8bit is not optional on Klein 9B for character training. adafactor works for style LoRA but fails for identity LoRA — symptom is gradual face averaging toward a "stock photo" face.
- **Repeats math**: 90-120 repeats × 10 images = 900-1200 effective training samples per epoch. Too few repeats (<50) with 10 images = undertraining even at 3K steps.
- **4B vs 9B character quality**: 4B trains on 16GB but produces lower identity fidelity than 9B. Use 4B for prototyping, 9B for production.
- **Face feature leakage**: even a few images with face-descriptive captions in a 12-image dataset can significantly reduce LoRA identity strength. All captions must follow the scene-only rule.
- **PuLID requires base model at inference**: PuLID-Flux2 injects into double blocks, which are less effective in distilled Klein. Use base model + LoRA + PuLID for maximum identity quality.

## See Also

- [[diffusion-lora-training]] - general LoRA training pipeline, tool comparison
- [[flux-klein-9b-architecture]] - Klein block structure, Qwen3 encoder, 3D RoPE
- [[anatomy-correction-diffusion]] - fixing proportion/anatomy artifacts
- [[lora-fine-tuning-for-editing-models]] - edit LoRA (before/after pairs)
