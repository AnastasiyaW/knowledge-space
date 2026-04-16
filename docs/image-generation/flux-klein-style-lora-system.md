---
title: FLUX Klein Style LoRA System
category: systems
tags: [klein, style-lora, gemini, training, system-design, style-transfer, captioning]
---

# FLUX Klein Style LoRA System

Architecture and empirical findings for a user-facing style LoRA system on FLUX.2 Klein Base 9B. Based on 56 training jobs, 150 LoRA files, and systematic evaluation across 16 style datasets.

## System Architecture

```yaml
User uploads 5-50 reference images
  ↓
Gemini 2.5 Pro: caption each image (content-only, no style descriptors)
  ↓
ai-toolkit: train rank32 LoRA (1000 steps, ~14 min on H200)
  ↓
At generation:
  - Gemini L1 (style extraction): analyze refs → STYLE_PROFILE
  - Gemini L2 (prompt reformulation): weave style + user prompt
  ↓
Klein Base 9B + LoRA → 2048×2048 output
```

## Training Configuration (Empirically Optimal)

```yaml
# ai-toolkit config
model: FLUX.2-klein-base-9B  # NOT distilled
rank: 32
linear_alpha: 32
conv_rank: 16
conv_alpha: 16
optimizer: adafactor
learning_rate: 1e-4
weight_decay: 1e-4
steps: 1000              # universal safe choice (14 min on H200)
caption_dropout: 0.05
resolution: 1024
noise_scheduler: flowmatch
scheduler: cosine
```

**Production formula for steps:**
- rank32: `max(500, dataset_size × 30)` steps
- rank128: `max(500, dataset_size × 20)` steps + early stopping check

**Early stopping:** rank128 on small datasets (<10 refs) overfit sharply. Dataset bd9 (5 refs, rank128) peaked at step 500 then degraded. rank32 on same dataset: smooth convergence to step 1000.

## Gemini Two-Level Style Pipeline

### L1: Style Extraction

```yaml
INPUT: 1-10 reference images
OUTPUT: STYLE_PROFILE dict
```

STYLE_PROFILE structure:
```yaml
MUST_APPLY (non-negotiable visual elements):
  - COLOR: exact palette with mood preservation
  - TEXTURE: fabric/surface/material quality
  - LIGHTING: quality, direction, color temperature
  - MOOD: emotional tone and atmosphere

ENRICH (add when compatible with user content):
  - SIGNATURE_ELEMENTS: distinctive recurring props or devices
  - WARDROBE_LANGUAGE: specific fabrics, silhouettes, accessories
  - ENVIRONMENT: characteristic settings
  - CAMERA: film stock, lens choice, depth of field
  
PROMPT_SUFFIX_MUST: (always append to prompt)
PROMPT_SUFFIX_ENRICH: (append when scene is compatible)
```

**Gemini model selection:**
- Gemini 2.5 Pro: best style extraction quality
- Gemini 3 Flash Preview (OpenRouter: google/gemini-3-flash-preview): 5× faster for production

### L2: Prompt Reformulation

```yaml
INPUT: STYLE_PROFILE + user prompt
OUTPUT: reformulated prompt (100-200 words)
```

Key rules:
- Style wins on visual decisions (colors, textures, lighting)
- User wins on subject/action/content
- Gender-adaptive wardrobe: "pink ruffle blouse" → "dusty rose cashmere" for males
- Environment transformation: generic "office" → style's specific setting
- SIGNATURE_ELEMENTS are non-negotiable (floating objects, surreal devices)
- No color accuracy flattening: preserve exact saturation, don't let mood words override

## Dataset Size → Quality Matrix (Empirical)

| Refs | Quality | Best Approach |
|------|---------|--------------|
| 30+ | ★★★★★ | Any variant works |
| 10-15 | ★★★★ | GEM+A (Gemini + rank32) |
| 5-7 | ★★★ | GEM+B (Gemini + rank128) |
| 1-3 | ★★ | B_r128 alone (Gemini HURTS small datasets) |
| 2 refs | ★ | Nothing works reliably |

**Critical finding:** Gemini text pipeline helps with 5+ refs but BREAKS 1-3 ref datasets. With very few references, the model can't distinguish style signal from content noise - adding complex text further confuses it.

## Variant Comparison (56 Training Jobs, 16 Boards)

Tested 7 rank/optimizer variants × 5 prompts × 16 style boards. Top performers by win rate:

| Variant | Wins | Win Rate | Notes |
|---------|------|---------|-------|
| GEM+A (Gemini + rank32/adafactor) | 31 | 94% | Best overall |
| GEM+B (Gemini + rank128/adamw8bit) | 25 | 100% | Best on difficult cases |
| B_r128 alone | 16 | 100% | Gemini-free, stable |
| GEM+D (small dataset variant) | 13 | 93% | |
| E_ema / F_wdec | unstable | - | Not recommended |

**Key insight:** rank32 + Gemini beats rank128 + Gemini because lower rank leaves more capacity for text conditioning to work. rank128 captures more style but "crowds out" the Gemini text influence.

## Caption Strategy (Critical)

Style captions must describe WHAT is in the image, NEVER HOW it looks.

```markdown
# CORRECT: trigger + content description
bd9style. A woman with flowing white hair stands beside a white horse in a grassy field

# WRONG: style descriptors
bd9style. Red and white editorial fashion, moody atmospheric lighting
→ Model explains visual richness via text, nothing left for LoRA weights to capture

# ALSO WRONG: identical stub captions for all images
bd9style
→ Works for style transfer but poor generalization to novel prompts
```

**The mechanism:** captions tell the model what to EXCLUDE from LoRA weights. Everything described in caption → associated with text tokens. Everything NOT described → absorbed into LoRA weights. For style LoRA, style must NOT be captioned.

**Caption dropout rate:** 0.05-0.1 for style LoRAs. When dropout fires, entire caption including trigger is dropped. Forces model to learn style independent of text → style activates from LoRA even without trigger.

## Architecture Incompatibilities with Klein 9B

All FLUX.1-dev adapters are **architecturally incompatible** with Klein 9B:

| Technology | Error | Root Cause |
|-----------|-------|-----------|
| USO | dim 3072 vs 4096 | Trained on FLUX.1-dev |
| Redux | dim mismatch | FLUX.1-dev only |
| IP-Adapter | Not trained | No Klein adapter exists |
| RES4LYF | dim mismatch | Redux-based |
| Realism LoRA (XLabs) | dim 3072 | FLUX.1-dev only |
| Shakker Add-Details LoRA | dim 3072 | FLUX.1-dev only |

**Klein 9B hidden dimensions:** hidden_dim=4096, joint_attention_dim=12288 (vs FLUX.1-dev: 3072/4096).

**Klein-native projector (WIP):** SigLIP (1152) → MLP (2 layers) → Klein text space (12288). ~85M trainable params. Needs 50K-200K style pairs to train. No public implementation exists.

## SplitFlux Block Targeting

FLUX architecture analysis shows block-level specialization:
- Blocks 20-29 (double-stream): content, subject identity, composition
- Blocks 30-57 (single-stream): style, texture, lighting

**SplitFlux approach:** train LoRA on blocks 30-57 ONLY. Results:
- 30% faster training (fewer parameters)
- Better style/content separation
- Reduces content leakage (less likely to memorize subjects from training images)

```yaml
# ai-toolkit: target specific blocks
target_blocks: ["single_transformer_blocks.30", ..., "single_transformer_blocks.57"]
```

## Convergence Observations

| Dataset | Refs | rank32 sweet spot | rank128 sweet spot |
|---------|------|------|-------|
| Large (31 refs) | 31 | 500 steps (6 min) | 1000 steps (14 min) |
| Medium (7 refs) | 7 | 1500 steps (21 min) | 1500 steps |
| Small (5 refs) | 5 | 1000 steps (14 min) | 500 steps (overfit after!) |

## ConsisLoRA: Two-Step Content/Style Separation

For datasets with strong content/style coupling:

```text
Step 1 (content LoRA): rank16, 1500 steps
  - Trains on same images
  - Objective: capture content only (what the images depict)

Step 2 (style LoRA): rank16, 2000 steps
  - Trained on top of Step 1
  - Objective: residual after content LoRA = pure style
```

Useful when: training images contain distinctive subjects that shouldn't be in the style LoRA (e.g., specific person, specific object).

## K-LoRA Fusion (Custom Node)

GPU-accelerated LoRA fusion at inference for mixing multiple style LoRAs:

```python
# ComfyUI custom node: K-LoRA
# Merges multiple style LoRAs with weights in 3 seconds on H200
# Avoids sequential application artifacts from standard stacking
fused_lora = klora_merge([lora_a, lora_b, lora_c], weights=[0.5, 0.3, 0.2])
```

## Gotchas

- **Cosine scheduler causes "jumps" at midpoint**: if LR is high when reaching the cosine midpoint, the model can overshoot and produce chaotic checkpoints at that step. Check step 500-600 explicitly for quality degradation.
- **Gemini hurts 1-3 ref datasets**: with very few refs, Gemini text description adds noise that competes with the weak style signal. Use raw LoRA (no text pipeline) for 1-3 ref cases.
- **rank128 fast overfit on small datasets**: 5-image dataset + rank128 = overfitting by step 500-700. rank32 is forgiving enough to reach step 1000 cleanly. Prefer rank32 unless dataset is 30+ refs.
- **adafactor vs adamw8bit**: adafactor is faster and uses less memory. adamw8bit converges more reliably at rank128. For rank32, either works.
- **style_tests/ and production same server**: generating contact sheets and training jobs compete for GPU. Schedule generation passes when no training is running, or reserve separate GPUs.

## See Also

- [[diffusion-lora-training]] - full training parameters
- [[style-reference-ux]] - user-facing UX patterns
- [[flux-klein-9b-inference]] - inference and LoRA stacking
- [[lora-fine-tuning-for-editing-models]] - edit LoRA patterns
