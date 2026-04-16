---
title: Diffusion LoRA Training
category: techniques
tags: [lora, training, flux, klein, sana, dataset, learning-rate, fine-tuning, diffusion-pipe, ai-toolkit, simpletuner]
aliases: ["LoRA Training Pipeline", "Diffusion Fine-Tuning"]
---

# Diffusion LoRA Training

Practical patterns for LoRA fine-tuning of diffusion models (FLUX Klein 9B, [[SANA]], SDXL). Covers dataset preparation, training tools, hyperparameters, and multi-trainer comparison.

## Dataset Preparation

### Size Guidelines

| Task | Minimum | Recommended | Max Useful |
|------|---------|-------------|------------|
| Single subject (DreamBooth) | 3-5 | 5-10 | 15 |
| Style (photography style) | 15-20 | 25-30 | 50 |
| Domain (product category) | 30-50 | 50-100 | 200 |
| Complex domain + variations | 50+ | 100-200 | 500 |

### Caption Quality

Detailed captions are more important than data quantity. Include:
- Material, texture, lighting setup
- Camera angle, focal length, depth of field
- Background description, environment
- Style attributes specific to the domain

```yaml
Good: "sks jewelry photo, 18k gold engagement ring with oval cut diamond,
       soft studio lighting, dark velvet background, macro photography,
       sharp focus on gemstone facets"

Bad:  "ring on dark background"
```

### Trigger Words

Use rare token (e.g., "sks") as trigger word for DreamBooth. Define one per LoRA style. The token must not collide with existing vocabulary meanings.

### Image Requirements

- Resolution: 1024x1024 minimum (match training resolution)
- Format: PNG preferred (lossless), JPG acceptable if high quality
- Variety: mix angles, lighting, compositions within the domain
- Quality: curated > quantity. Remove blurry, poorly lit, atypical examples.

## FLUX Klein 9B LoRA Training

### Critical Rules (From 50+ Training Runs)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Network dims | 128/64/64/32 | linear/linear_alpha/conv/conv_alpha (4:2:1:1 ratio) |
| Weight decay | 0.00001 | 1/10th default for balanced analog texture |
| Learning rate | **DO NOT CHANGE** | Even 0.005% change destroys image quality on Flux architecture |
| Optimal steps | ~7,000 | 3K = too raw, beyond 7K = anatomical distortion |
| Trigger word | One per style | Required for activation |

### Klein-Specific Notes

- Train on **base** model (klein-base-9b), NOT distilled
- 9B uses `qwen_3_8b` text encoder; 4B uses `qwen_3_4b`
- 4B LoRA NOT compatible with 9B and vice versa
- FP8 transformer saves significant VRAM during 9B training

## SANA LoRA Training

### Recommended Recipe

```bash
accelerate launch train_dreambooth_lora_sana.py \
  --pretrained_model_name_or_path=Efficient-Large-Model/Sana_1600M_1024px_BF16_diffusers \
  --instance_data_dir=data/dreambooth/jewelry \
  --output_dir=trained-sana-lora \
  --mixed_precision=bf16 \
  --instance_prompt="a photo of sks jewelry" \
  --resolution=1024 \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --use_8bit_adam \
  --learning_rate=1e-4 \
  --lr_scheduler=constant \
  --lr_warmup_steps=0 \
  --max_train_steps=500 \
  --validation_prompt="A photo of sks jewelry on black velvet" \
  --validation_epochs=25 \
  --seed=0 \
  --cache_latents \
  --offload
```

### SANA Training Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Learning rate | 1e-4 | Standard for SANA LoRA |
| Max steps | 500 | Fast convergence (vs 7K for FLUX) |
| Resolution | 1024 | Native SANA resolution |
| Effective batch | 4 | batch 1 x grad_accum 4 |
| Precision | bf16 | Required |
| Optimizer | 8-bit AdamW | Memory efficient |
| LR scheduler | constant | No warmup needed |

### LoRA Configuration

Target layers: `attn.to_k, attn.to_q, attn.to_v` for attention-only LoRA.

LoRA scaling = `alpha / rank`:
- alpha = rank: scaling factor 1.0 (standard)
- alpha < rank: subtler modifications
- alpha > rank: amplified effect

### Memory Optimizations

- `--offload`: CPU offload text encoder + VAE when not in use
- `--cache_latents`: precompute VAE latents, remove VAE from GPU
- `--use_8bit_adam`: bitsandbytes 8-bit optimizer

## Two-Stage Domain Training

**Stage 1: Domain LoRA** - teaches what the domain looks like:
- 20-50 high-quality domain images with detailed captions
- Standard T2I DreamBooth/LoRA training
- Learns materials, lighting, textures, compositions

**Stage 2: Task-specific** - teaches what to DO:
- Build on domain LoRA or merge it
- Paired data for editing tasks (before/after)
- InstructPix2Pix-style training for edit LoRAs

For txt2img domain generation, Stage 1 alone is sufficient.

## Training Tool Comparison

| Feature | diffusion-pipe | ai-toolkit | SimpleTuner | kohya_ss |
|---------|---------------|------------|-------------|----------|
| Pipeline parallelism | DeepSpeed | No | No | No |
| Multi-GPU | Native hybrid | Limited | Data parallel | Data parallel |
| LoRA format (Klein) | ComfyUI native | Diffusers | Diffusers | Diffusers |
| Progressive resolution | No | No | **Yes** | No |
| Text encoder LoRA | No (pre-cache) | Yes | Yes | Yes |
| Masked training | **Yes** | No | No | No |
| LR scheduling | warmup only | Full set | Full set | Full set |
| Prodigy optimizer | Not documented | Yes | Yes | Yes |
| Resume training | Pain-free | Yes | Yes | Yes |
| Windows | WSL2 only | Native | Native | Native |
| Config format | TOML | YAML | JSON + env | TOML |

### diffusion-pipe Unique Features

**Masked training**: provide binary mask per image - white regions train, black regions are masked from loss. Ideal for face-only training (train on face, ignore background/clothing).

**Pipeline parallelism**: Klein 9B splits across multiple GPUs via DeepSpeed. With `pipeline_stages=2`, model divides across 2 GPUs.

**ComfyUI-native LoRA format**: no conversion needed for Klein inference in ComfyUI.

### diffusion-pipe Klein Config

```toml
[model]
type = 'flux2'
diffusion_model = '/path/to/flux-2-klein-base-9b.safetensors'
vae = '/path/to/flux2-vae.safetensors'
text_encoders = [
  {path = '/path/to/qwen_3_8b.safetensors', type = 'flux2'}
]
dtype = 'bfloat16'
diffusion_model_dtype = 'float8'
timestep_sample_method = 'logit_normal'
shift = 3

[adapter]
type = 'lora'
rank = 32
dtype = 'bfloat16'

[optimizer]
type = 'AdamW8bitKahan'
lr = 5e-5
betas = [0.9, 0.99]
weight_decay = 0.01
```

### Dataset Config (diffusion-pipe)

```toml
resolutions = [1024]
enable_ar_bucket = true
min_ar = 0.5
max_ar = 2.0
num_ar_buckets = 7
num_repeats = 1
```

## Klein 9B Character / Identity LoRA

Training a LoRA to preserve a specific person's identity requires a different approach from style LoRA.

### Critical: Optimizer Choice

**adafactor FAILS on Klein 9B** for character training. Use `adamw8bit`.

```yaml
# diffusion-pipe
[optimizer]
type = 'AdamW8bitKahan'
lr = 1e-4
betas = [0.9, 0.999]
weight_decay = 0.01
```

```toml
# ai-toolkit / SimpleTuner equivalent
optimizer: adamw8bit
lr: 1e-4
```

### Minimal Dataset Recipe (RunComfy standard)

| Parameter | Value | Notes |
|-----------|-------|-------|
| Images | 8-12 | Curated, varied angles + lighting |
| Steps | 2K-4K | Character identity; style = 7K |
| Repeats | 90-120 | Compensates for small dataset |
| Rank | 16-32 | RunComfy conservative; Herbst uses 128/64 |
| LR | 1e-4 | Same sensitivity warning as style LoRA |
| Optimizer | adamw8bit | **adafactor will fail** |

**Alternative recipe (Herbst, 50+ runs):**
- Rank 128/64/64/32, weight_decay 0.00001, 7K steps — universal winner for both style and character quality

### Caption Format for Identity LoRAs

```
trigger_token, [scene description], [lighting], [pose]
```

**Key rules:**
- Put trigger word FIRST
- Describe scene, background, lighting, pose
- **Do NOT describe face features** (eye color, nose shape, face shape) — this forces those features INTO the LoRA weights rather than being excluded
- The model learns what's NOT described; face features must stay in LoRA, not float free in text space

```yaml
Good: "john_doe portrait, standing in office, warm overhead lighting, three-quarter view"
Bad:  "john_doe, blue eyes, sharp jawline, dark hair, studio lighting"  # locks features to text
```

### Proportion Issues Fix (Big Heads Problem)

Cause: dataset dominated by headshots (90%) + distillation artifacts.

**Fix: 1/3 dataset rule**
```
33% headshots (shoulders up)
33% half-body
33% full-body
```

**Caption composition explicitly:**
```
"john_doe, full body shot, standing, arms visible, white studio backdrop"
"john_doe, half body, casual seated pose, table in foreground"
```

### PuLID-Flux2 for Inference Enhancement

Apply after training to boost identity consistency without retraining:
- InsightFace + EVA-CLIP → identity tokens injected into Klein double blocks
- Supports up to 8 reference images (multi-reference via 3D RoPE time offsets)
- Does not require paired training data

## Auxiliary Losses for LoRA Training

Additional loss terms beyond standard diffusion loss for specialized training goals.

### ArcFace Identity Loss

Preserves facial identity during edit LoRA training:

```python
from insightface.app import FaceAnalysis

face_app = FaceAnalysis(providers=['CUDAExecutionProvider'])
face_app.prepare(ctx_id=0)

def arcface_loss(generated, target, weight=0.1):
    gen_embedding = face_app.get(generated)[0].embedding
    target_embedding = face_app.get(target)[0].embedding
    cos_sim = F.cosine_similarity(gen_embedding, target_embedding, dim=0)
    return weight * (1 - cos_sim)
```

Use when: edit LoRA must preserve identity across transformations (relight, restyle).

### DreamBooth Prior Preservation

Prevents language drift (model forgets general concept while learning specific instance):

```bash
# In ai-toolkit
prior_preservation: true
prior_preservation_weight: 1.0
class_prompt: "a person"  # generic class prompt
num_class_images: 200
```

Prior images generated by base model before training begins. Loss = main loss + prior_weight × class_loss.

### Masked Loss (diffusion-pipe)

Train only on specific regions — essential for face LoRA where background should not influence weights:

```toml
# diffusion-pipe dataset config
[[dataset.image_config]]
path = "data/faces/"
masks_path = "data/masks/"  # white = train region, black = ignore
masked_loss = true
```

Mask generation: face segmentation (BiSeNet, SAM2) → erode 10px → apply as binary mask.

### B-LoRA: Content vs Style Disentanglement

Target specific transformer block groups to separate content (structure) from style:

```python
# B-LoRA: content preservation blocks
content_blocks = [f"transformer.single_transformer_blocks.{i}" for i in range(0, 12)]
# style-only blocks
style_blocks = [f"transformer.double_transformer_blocks.{i}" for i in range(0, 8)]
```

Training content blocks = structural/identity LoRA. Training style blocks = style-only LoRA.

### Concept Slider LoRA

Train on contrast pairs (attribute A vs. attribute B) to create a directional slider:

```python
# Dataset: paired images, one with attribute, one without
# positive_prompts = ["sharp details", ...]
# negative_prompts = ["soft details", ...]
# Model learns the direction in latent space
# Inference: LoRA weight -2 to +2 controls attribute strength
```

## LR Scheduling for Diffusion LoRA

The learning rate VALUE matters far more than the schedule shape for FLUX/Klein.

### Schedule Options

| Schedule | Use Case | Notes |
|----------|----------|-------|
| constant | Klein 9B (recommended) | Most controlled; Herbst default |
| constant_with_warmup | General purpose | 100-200 warmup steps |
| cosine | "Safe upgrade" from constant | Gradual decay, rarely hurts |
| Prodigy | When unsure of LR value | Self-tuning, sidesteps sensitivity |
| warmup_only | Not standard | Rarely used standalone |

**Community consensus (Calvin Herbst, 50+ Klein runs):** constant schedule, because Klein's LR sensitivity makes any decay risky. Better to nail the LR value than rely on schedule to compensate.

**Chinese community consensus (Zhihu/Bilibili practitioners):** For face/character LoRA, `adamw8bit + 1e-4 + constant` is the safe combination. Avoid `3e-4 + AdamW8bit` - causes unrealistic facial shadows and wrinkles.

### Steps vs Dataset Size (Chinese Community Rule)

| Dataset Size | Steps | Rationale |
|-------------|-------|-----------|
| 10-20 images | 1K-2K | "images × 100" rule widely cited |
| 20-30 images | 2K-3K | Sweet spot for face LoRA |
| 30-50 images | 3K-4K | >50 images at 4K steps = overfitting risk |

**Critical finding:** FLUX training curves are non-monotonic. Epoch 6 may look good, epoch 8 overfitted, epoch 10 normal again. Always save every checkpoint and evaluate empirically - don't trust the curve.

### Prodigy: Self-Tuning LR

```toml
[optimizer]
type = 'prodigy'
# No lr needed — Prodigy estimates it
d_coef = 1.0
weight_decay = 0.01
safeguard_warmup = true
```

Useful when starting a new architecture without established LR priors. May still overfit if steps are too many.

**Prodigy gotcha:** last few epochs can cause hand deformities. Save earlier checkpoints and test at epoch N-2 before accepting the final.

### DiffSynth-Studio Official Klein 9B Config

All Klein variants (4B, 9B, 9B-Base) use the same base config in DiffSynth-Studio:

```yaml
learning_rate: 1e-4
epochs: 5
lora_rank: 32
max_pixels: 1048576   # = 1024x1024
dataset_repeat: 50
gradient_checkpointing: true
lora_base_model: "dit"
target_modules:
  - to_q, to_k, to_v, to_out.0
  - add_q_proj, add_k_proj, add_v_proj, to_add_out
  - linear_in, linear_out, to_qkv_mlp_proj
  - single_transformer_blocks.*.attn.to_out
```

## Overfitting Detection

| Symptom | Cause | Fix |
|---------|-------|-----|
| Training images reproduced exactly | Too many steps / too few images | Reduce steps, add data diversity |
| Anatomical distortion | Training past optimal point | Stop at ~7K steps (FLUX) |
| Color/style collapse | LR too high | Reduce LR (carefully for FLUX) |
| Prompt ignored | Overfit to training captions | More diverse captions, lower rank |
| Artifacts at high LoRA strength | Training instability | Lower alpha, add weight decay |

## Dependencies

```bash
# SANA LoRA (diffusers)
pip install diffusers[training] peft>=0.14.0 accelerate bitsandbytes wandb
# From source for latest:
pip install git+https://github.com/huggingface/diffusers.git

# diffusion-pipe
pip install deepspeed  # heavy dependency
```

## Gotchas

- **FLUX LR sensitivity**: the FLUX architecture is extremely sensitive to learning rate changes. The documented "DO NOT CHANGE" warning comes from 50+ training runs showing even 0.005% deviation destroys output quality. This is architecture-specific - SANA and SDXL are far more forgiving.
- **Klein 4B/9B LoRA incompatibility**: different text encoders (4B vs 8B Qwen) mean LoRAs trained on one model cannot be loaded on the other. Always verify model variant before training.
- **diffusion-pipe on Windows**: requires WSL2. Direct Windows execution is not supported due to DeepSpeed dependency.
- **Cache latents for SANA**: failing to use `--cache_latents` keeps the VAE on GPU throughout training, wasting 2-4 GB VRAM that could be used for larger batch size or higher rank.
- **adafactor + Klein = broken character LoRA**: adafactor adaptive scaling does not converge properly with Klein 9B's architecture for identity training. Symptom: identity collapses to average face by 1K steps. Fix: switch to adamw8bit.
- **Face feature captions destroy identity LoRA**: describing specific face features (eye color, face shape) in captions teaches the model to associate those features with text tokens rather than embedding them in LoRA weights. Result: LoRA has low identity fidelity. Always caption scene/context/pose, never face attributes.
- **Big heads from headshot-only datasets**: Klein (and diffusion models generally) develop distorted proportions when trained on 90%+ headshots. Always mix headshot/half-body/full-body at roughly equal ratios.
- **Training on distilled Klein**: edit LoRAs and character LoRAs must train on base model (klein-base-9b), not distilled variants. Distilled models have simplified conditioning that disrupts paired training.
- **Class prompt hurts FLUX character LoRA**: unlike DreamBooth for SDXL where class prompt (e.g., "a photo of a person") helps prior preservation, using class prompts for FLUX/Klein character LoRA degrades results — especially for male subjects and pets. FLUX already has strong identity priors; class prompt fights against the trigger word learning.
- **No trigger word needed for face LoRA**: Chinese community finding — trigger word has no detectable impact on high-precision face LoRA quality. FLUX handles person identity well without explicit token. Using a trigger word is optional, not required.
- **Regularization images greatly improve generalization**: for face/character LoRAs, including regularization images (similar subjects without the identity) significantly improves out-of-distribution generalization. Highly recommended even for small datasets (10-30 images).

## See Also

- [[lora-fine-tuning-for-editing-models]] - MMDiT-specific LoRA (Step1X-Edit, Qwen-Image-Edit)
- [[flux-klein-9b-inference]] - optimal inference settings for trained LoRAs
- [[flux-klein-9b-architecture]] - Klein architecture details (block structure, Qwen3 encoder)
- [[flux-klein-character-lora]] - detailed character LoRA workflow
- [[anatomy-correction-diffusion]] - fixing anatomical artifacts post-training
- [[SANA]] - SANA architecture and training details
- [[flow-matching]] - training objective for modern diffusion models
