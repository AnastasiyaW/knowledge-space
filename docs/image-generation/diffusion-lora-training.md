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

```
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

## See Also

- [[lora-fine-tuning-for-editing-models]] - MMDiT-specific LoRA (Step1X-Edit, Qwen-Image-Edit)
- [[flux-klein-9b-inference]] - optimal inference settings for trained LoRAs
- [[SANA]] - SANA architecture and training details
- [[flow-matching]] - training objective for modern diffusion models
