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

Standard [[flow-matching]] velocity loss + task-specific auxiliary losses:

| Loss | Purpose | Lambda | Used By |
|------|---------|--------|---------|
| Flow Matching (L_FM) | Core generation quality | 1.0 | All |
| Identity (ArcFace cosine) | Face preservation | 0.1 | [[PixelSmile]] |
| Symmetric Contrastive | Distinguish similar outputs | 0.05 | [[PixelSmile]] |
| LPIPS | Perceptual similarity | varies | [[RealRestorer]] |

## Commercial Viability

Base model (Qwen-Image-Edit-2511) is **Apache 2.0**. Your LoRA weights are entirely yours. This creates a clean commercial path:

```text
Apache 2.0 base (Qwen) + proprietary LoRA = your product
```

No license contamination from base model. LoRA weights are your IP.

## FLUX.2 Klein 9B Edit LoRA Training

Klein 9B has native multi-reference conditioning (up to 4 images concatenated as latents) - not IP-Adapter, but architecture-level latent-space concatenation. This makes it suitable for face swap, head swap, and paired before/after edit LoRAs.

### Architecture Specifics

- **Parameters**: 9B flow model + 8B Qwen3 text embedder (~17B total)
- **Blocks**: 8 DoubleStreamBlocks + 24 SingleStreamBlocks
- **Text encoder**: Qwen3-8B bundled (NOT separate like FLUX.1 T5+CLIP)
- **Training base**: always use `FLUX.2-klein-base-9B` (undistilled), never the distilled variant
- **FLUX.1-dev adapters incompatible**: hidden_dim mismatch (3072 vs 4096)

### Training Frameworks

| Framework | Strength | Best For |
|-----------|----------|----------|
| SimpleTuner | `use_flux_kontext: true` for native paired training, `model_flavour: "klein-9b"` | Edit LoRAs with before/after pairs |
| AI-Toolkit (ostris) | Most tested (50+ run study), YAML config | Style LoRAs, character LoRAs |
| DiffSynth-Studio | Chinese ecosystem, ready-to-run scripts | Klein + Qwen-Image-Edit |

### Optimal Hyperparameters

Based on Calvin Herbst's 50+ A/B test study:

| Parameter | Value | Notes |
|-----------|-------|-------|
| Linear rank/alpha | 128/64 | Winner across all models |
| Conv rank/alpha | 64/32 | 4:2:2:1 ratio proven optimal |
| LR | 1e-4 | EXTREME sensitivity - 0.005% change degrades quality |
| Optimizer | adamw8bit | Best for faces. Avoid adafactor |
| Weight decay | 0.00001 | 10x lower than default improves grain/texture |
| Scheduler | cosine_with_warmup (10%) | Direct evidence it helps face quality |
| Timestep type | sigmoid | Confirmed by 3 independent sources for face work |
| Noise offset | 0.05-0.1 | Slight contrast improvement |
| Precision | bf16 training + fp8 base | fp8 = better film grain, fp32 = better fidelity |
| Steps | 3000-4000 | For face edit with progressive dataset refinement |
| Save every | 250 steps | Essential - overfitting is non-monotonic on FLUX |

### Dataset Format for Paired Training

SimpleTuner Kontext mode (recommended):

```text
dataset/
  01_start.png      # Before image (source)
  01_start2.png     # Face reference crop (optional)
  01_end.png        # After image (target)
  01.txt            # "EDITFACE open the eyes wider"
```

Caption format: trigger word + specific change description. Describe the CHANGE, not the image. Be consistent across dataset.

### Progressive Dataset Refinement (BFS Method)

The most successful published face swap LoRA (BFS) used:

1. **Phase 1** (~2000 steps): 628 initial pairs, broad diversity
2. **Phase 2** (~4000 steps): narrowed to 138 pairs, best skin-tone matches
3. **Phase 3** (fine-tune): narrowed to 76 high-quality pairs

Start broad, filter to best pairs, continue training. Dataset refinement matters more than progressive resolution.

**Key insight:** dataset quality accounts for ~90% of output quality. Poor datasets produce poor LoRAs regardless of hyperparameters.

### Character/Face LoRA Parameters (Community Consensus)

Based on 50+ A/B tests (Calvin Herbst), BFL official docs, and Chinese community (Zhihu):

| Parameter | Character/Face | Style |
|-----------|---------------|-------|
| Rank | 32 (start), 128 for style | 128/64/64/32 |
| Alpha | rank or rank/2 | 64/32 |
| LR | 1e-4 (reduce to 5e-5 if unstable) | 9.5e-5 |
| Timestep type | **sigmoid** (face LoRA) | shift (BFL default) |
| Scheduler | cosine + warmup (10%) | cosine or constant |
| Steps | 800-1500 (Flux 2 face) | 3000-7000 |
| Dataset | 15-25 images (40+ loses focus) | 20-50 images |
| Class prompts | **DO NOT USE** (hurts Flux) | N/A |
| Regularization images | Yes (6:1 ratio) | Optional |

**Why sigmoid for faces:** targets low-noise timesteps that capture fine identity detail. "Shift" (BFL default) biases toward high-noise timesteps which learn coarse structure. Three independent sources confirm sigmoid for character LoRAs.

**Flux 2 vs Flux 1 convergence:** Flux 2 (including Klein) converges 40-50% faster than Flux 1. Optimal face steps: 800-1500 (Flux 2) vs 1000-2000 (Flux 1). >2000 steps on Flux 2 face = overfitting territory.

**Overfitting non-monotonic (CN finding):** Checkpoint at epoch 6 may be good, epoch 8 overfit, epoch 10 good again. Save every 250-500 steps, test each checkpoint.

### LR Scheduling for Face LoRAs

| Schedule | When to Use | Evidence |
|----------|------------|---------|
| Constant | Short runs (<1500 steps), known good LR | Majority community default |
| Cosine + warmup | 2000-5000 steps, insurance against late overfit | Direct evidence (15 LoRA comparison) |
| Prodigy (LR=1.0) | Uncertain LR, want auto-adaptation | Strongest for face training specifically |
| Polynomial (1e-3→1e-4) | "Aggressive start, conservative end" | ExponentialML experiment |

**Prodigy config:**
```yaml
optimizer: prodigy
learning_rate: 1.0
lr_scheduler: cosine
optimizer_args: decouple=true, use_bias_correction=false, weight_decay=0.05
lr_warmup_steps: 200
```
Prodigy needs 20-30% more steps than AdamW to achieve same convergence.

### ICEdit Diptych Training

Alternative approach: instead of before/after image pairs, place both images side-by-side in a diptych and train the model to understand the "edit" from left to right.

```yaml
[before_image | after_image]  ← concatenated horizontally
Caption: "EDITWORD: [description of change]"
```

Higher data efficiency than separate pairs. The model learns the visual delta rather than memorizing absolute appearances.

### LoRAShop: Training-Free Multi-LoRA Mixing

Merge multiple LoRAs without additional training via weight interpolation in parameter space:

```python
# Weighted average of LoRA delta weights
merged_lora = sum(w_i * lora_i for w_i, lora_i in zip(weights, loras))
# Normalize: weights sum to 1.0
```

Works best when LoRAs target similar content. Quality degrades when mixing LoRAs with very different training objectives (e.g., style + face).

### Layer Targeting for Face Edit

| Approach | Target | Result |
|----------|--------|--------|
| Double-stream only | `double_blocks` attention | Highest face similarity in A/B tests |
| All blocks | All double + single | Baseline |
| Single blocks only | `single_transformer_blocks 0-23` | DiffSynth default |
| Selective | Blocks 7, 12, 16, 20 | Lighter, good LoRAs |

Double-stream blocks handle cross-image interaction (reference latent + main image). For face conditioning, these are most critical.

### Face Crop Preprocessing

- Detection: InsightFace (buffalo_sc) for best diverse-face accuracy, or YOLOv8-face
- Padding: 40-50% around bbox for face swap, 80-100% for head swap
- Minimum: 512x512 face crop, 1024x1024 preferred
- Alignment: prefer eyes-horizontal but Klein tolerates mild rotation
- Include some neck/hair/ears for natural editing context

### Evaluation Metrics

| Metric | Target | Purpose |
|--------|--------|---------|
| ArcFace CSIM | >0.85 | Identity preservation |
| LPIPS | Lower = better | Visual closeness / edit containment |
| Background SSIM | ~1.0 | Non-face region preservation |
| CLIP Score | Task-dependent | Semantic alignment with prompt |

### min_snr_gamma: Incompatible

min_snr_gamma does NOT work with flowmatch scheduler used by Klein. Skip it entirely. Use noise_offset for contrast control instead.

## Gotchas

- Qwen-Image-Edit requires **DiffSynth-Studio** framework, not standard diffusers. LoRA loading path differs.
- PixelSmile requires a diffusers **patch script** (`patch_qwen_diffusers.sh`).
- At rank 64+, LoRA training on 60GB base needs 4x 80GB GPUs. Lower rank (16-32) fits on 2x A100.
- EMA (exponential moving average) on LoRA weights recommended for stability - PixelSmile uses it.
- Data quality matters more than data quantity - synthetic data with VLM scoring outperforms larger messy datasets.
- **Klein 4B and 9B LoRAs are incompatible** - different text encoder sizes (Qwen 3-4B vs Qwen 3-8B).
- **LR sensitivity is extreme on FLUX** - changing by 0.005% can destroy output quality. Use adamw8bit or Prodigy.
- **Overfitting is non-monotonic** - epoch 6 good, 8 bad, 10 good again. Save every checkpoint.
- **Hair is the #1 failure mode** in face editing - hairline, length, shape must match between pairs.
- **Multi-reference cost scales ~3.5x** for 2 refs, ~5x for 3 refs, ~7x for 4 refs.
- **Class prompts HURT Flux training** especially for males and pets.

## See Also

- [[diffusion-lora-training]] - general LoRA training (style, domain, Klein character)
- [[lora-auxiliary-losses]] - ArcFace, DreamBooth prior, masked loss, B-LoRA
- [[flux-klein-9b-architecture]] - Klein block structure, 3D RoPE reference conditioning
- [[flux-klein-character-lora]] - character/identity LoRA specifics
