---
title: MACRO
category: models
tags: [multi-reference, dataset, fine-tuning, bagel, omnigen2, qwen-image-edit, customization, novel-view, apache-2.0]
aliases: ["MACRO-400K"]
---

# MACRO (Multi-Reference Image Generation)

Dataset + benchmark + fine-tuning recipe that fixes quality degradation when generation models receive many (6-10) reference images. Not a new architecture — applied to existing models (Bagel, OmniGen2, Qwen-Image-Edit).

Paper: arXiv:2603.25319 (March 2026). Authors: HKU MMLab + Meituan.

## Problem

Models like Bagel, OmniGen2, Qwen-Image-Edit support `<image N>` placeholders for multi-reference generation, but quality drops sharply at 6+ images. Root cause: **training data bottleneck** — existing datasets dominated by 1-2 reference pairs with no structured supervision for dense inter-reference dependencies.

## Solution: Data-Centric

### MACRO-400K Dataset

400K samples, up to 10 references per sample, average 5.44 references. Four task categories (100K each):

| Task | Description | Sources |
|------|-------------|---------|
| **Customization** | Multi-subject composition | OpenSubject, MVImgNet, DL3DV, WikiArt |
| **Illustration** | Image from multimodal context | OmniCorpus-CC-210M web crawl |
| **Spatial** | Novel view synthesis | G-buffer Objaverse, Pano360, Polyhaven |
| **Temporal** | Future frame prediction | OmniCorpus-YT videos |

Balanced across reference count brackets: 1-3 / 4-5 / 6-7 / 8-10.

**Construction pipeline**: Split → Generate (Gemini + Nano APIs) → Filter (LLM scoring + bidirectional VLM assessment). The generation step uses proprietary APIs — pipeline not fully reproducible, but the resulting dataset is fully released.

### Dynamic Resolution Scaling

At inference, input images automatically downsized as count increases:
- 1-2 images: 1M px
- 3-5 images: 590K px
- 6+ images: 262K px

### Training Recipe

**Full fine-tune** (not LoRA). Per-model framework:

| Model | Framework | Training | Size |
|-------|-----------|----------|------|
| Bagel (14.7B, MoT) | FSDP + FLEX packing | LR 2e-5, 10 epochs, VAE frozen | ~29.5 GB |
| OmniGen2 | Native framework | Same hyperparams | — |
| Qwen-Image-Edit | DiffSynth + DeepSpeed | Same hyperparams | ~98.6 GB |

T2I co-training: 10% text-to-image data mixed in to preserve general T2I capability.

## Results (MacroBench)

4000 samples, 16 sub-categories, LLM-scored:

| Model | Open? | Score | vs Base |
|-------|-------|-------|---------|
| Nano Banana Pro | No | 6.12 | — |
| GPT-Image-1.5 | No | 5.89 | — |
| **Macro-Bagel** | **Yes** | **5.71** | +88% (base: 3.03) |
| Macro-OmniGen2 | Yes | — | significant improvement |
| Macro-Qwen | Yes | — | mitigates severe drops at 6-10 |

Macro-Bagel approaches Nano Banana Pro in Customization, **surpasses it in Spatial tasks**.

### Ablation Insights

- Sharpest gains between 1K-10K samples, diminishing returns 10K-20K
- Upweighting large-input samples (2:2:3:3 ratio) helps without hurting low-input
- Cross-task co-training provides synergistic benefits — spatial training helps customization

## Inference

```python
# Bagel variant
from inference_bagel import generate
result = generate(model, prompt="...", reference_images=[img1, img2, ...], resolution=768)
# Default: 768x768
```

**VRAM**: 40-80 GB depending on model variant. `enable_model_cpu_offload` supported for OmniGen2.

## License

| Component | License |
|-----------|---------|
| Code | Apache 2.0 (HF; GitHub has no LICENSE file) |
| All 3 model weights | **Apache 2.0** |
| MACRO-400K dataset | **CC-BY-4.0** |

**Fully commercially usable** — code, weights, and dataset.

## Gotchas

- Dataset construction uses proprietary Gemini/Nano APIs — cannot recreate dataset, but can use the released one
- GitHub repo has no explicit LICENSE file yet (fresh project, 3 days old)
- Full fine-tune requires multi-GPU setup (FSDP) — not a quick LoRA
- Training code released but expects specific framework versions

## Key Links

- GitHub: github.com/HKU-MMLab/Macro
- HF models: huggingface.co/Azily/ (Macro-Bagel, Macro-OmniGen2, Macro-Qwen-Image-Edit)
- HF dataset: huggingface.co/datasets/Azily/Macro-Dataset
- Project page: macro400k.github.io
