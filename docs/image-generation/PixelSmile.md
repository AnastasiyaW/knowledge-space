---
title: PixelSmile
category: models
tags: [facial-expression, lora, qwen-image-edit, identity-preservation, emotion-control, intensity-control, stepfun, fudan, apache-2.0]
---

# PixelSmile

LoRA adapter for [[Step1X-Edit|Qwen-Image-Edit-2511]] that enables fine-grained facial expression editing with continuous intensity control and identity preservation. 12 base expressions, pairwise blending, alpha-controlled intensity.

Paper: arXiv:2603.25728 (March 2026). Authors: Fudan University + StepFun.

## Architecture

**Base model**: Qwen-Image-Edit-2511 (~60 GB bf16)
**Adapter**: LoRA rank 64, alpha 128, dropout 0 → **850 MB** safetensors

### LoRA Targets (full [[MMDiT]] coverage)

```python
target_modules = [
    # Attention projections
    "to_q", "to_k", "to_v",
    "add_q_proj", "add_k_proj", "add_v_proj",
    "to_out.0", "to_add_out",
    # Image FFN
    "img_mlp.net.0.proj", "img_mlp.net.2",
    # Text FFN
    "txt_mlp.net.0.proj", "txt_mlp.net.2"]
```

Two independent LoRA adapters trained: human faces and anime. Only human ("preview") released so far.

## Expression Control Mechanism

### Textual Latent Interpolation

Core technique (see [[textual-latent-interpolation]] for details):

```python
# 1. Encode neutral and target prompts
e_neu = text_encoder("Edit the person to show a neutral expression")
e_tgt = text_encoder("Edit the person to show a happy expression")

# 2. Compute direction vector
delta = e_tgt - e_neu

# 3. Interpolate with intensity alpha
e_cond = e_neu + alpha * delta  # alpha ∈ [0, 1], can exceed 1.0 for exaggeration
```

Applied across ALL token embeddings (method `score_one_all`). Alternative: interpolate only last 6-7 expression-specific tokens.

### 12 Expressions

angry, confused, contempt, confident, disgust, fear, happy, sad, shy, sleepy, surprised, anxious

6 basic + 6 extended. Each controllable from 0 (neutral) to 1 (full intensity) to >1 (exaggerated).

### Expression Blending

Zero-shot pairwise interpolation of expression embeddings. 9 of 15 basic-expression pairs produce plausible compound emotions (e.g., anger + sadness). Failures occur when expressions require physiologically contradictory muscle states (e.g., conflicting mouth positions).

## Identity Preservation

Training uses frozen **ArcFace** (InsightFace glintr100 + scrfd_10g_bnkps detector):

```toml
L_id = 1 - cosine_similarity(ArcFace(generated), ArcFace(ground_truth))
lambda_id = 0.1
```

At inference, identity is preserved implicitly through LoRA's learned behavior — no explicit identity loss computation needed.

## Training

**Data**: FFE Dataset (Flex Facial Expression) — 60K images (30K real + 30K anime)
- Real: ~6000 base identities from public portrait datasets
- Generated via **Nano Banana Pro** with dual-part prompts
- Annotated by **Gemini 3 Pro** with continuous 12-dimensional vectors

**Hardware**: 4x NVIDIA H200, batch 4/GPU, 100 epochs, cosine LR from 1e-4

**Loss function**:
```toml
L = 0.5*(L_FM_a + L_FM_b) + 0.05*L_SC + 0.1*L_ID
```
- `L_FM`: [[flow-matching]] velocity loss
- `L_SC`: Symmetric Contrastive Loss (InfoNCE, temp=0.07) — prevents confusion between similar expressions
- `L_ID`: ArcFace identity loss

**Symmetric joint training**: confusing expression pairs (E_a, E_b) trained bidirectionally in same batch to prevent directional bias.

## Results

| Metric | PixelSmile | GPT-Image | Nano Banana Pro |
|--------|-----------|-----------|-----------------|
| mSCR (confusion, ↓ better) | **0.0550** | 0.1107 | 0.1754 |
| Accuracy-6 | **0.8627** | — | 0.8431 |
| Control Linearity | **0.8078** | — | — |

Human study: 4.48/5 continuity, 3.80/5 identity. Best overall balance.

## Inference

```python
pipe = QwenImageEditPlusPipeline.from_pretrained("Qwen/Qwen-Image-Edit-2511")
pipe.load_lora_weights("PixelSmile/PixelSmile", weight_name="PixelSmile-preview.safetensors")
# 50 steps, 512x512, bf16
```

**VRAM**: 60+ GB bf16 (base model). FP8 → ~30 GB. NF4 → ~18-20 GB.

> Requires `patch_qwen_diffusers.sh` — patches current diffusers for compatibility.

## Gotchas

- Only **preview** weights released. Stable version (better human + anime) coming later.
- Training code **not released** (roadmap).
- MEAD dataset (traditional expression dataset) **significantly underperforms** — synthetic FFE is critical.
- HuggingFace demo requires paid compute (won't run on free tier).

## License

**Apache 2.0** — both code and weights. **Commercially usable.**

## Key Links

- GitHub: github.com/Ammmob/PixelSmile
- HF model: huggingface.co/PixelSmile/PixelSmile
- HF benchmark: huggingface.co/datasets/PixelSmile/FFE-Bench
- Demo: huggingface.co/spaces/PixelSmile/PixelSmile-Demo
