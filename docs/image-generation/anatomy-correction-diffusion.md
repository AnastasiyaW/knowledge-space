---
title: "Anatomy Correction in Diffusion Models"
description: "Comprehensive guide to detecting and fixing anatomy mutations (hands, fingers, limbs) in FLUX Klein 9B and other diffusion models - academic methods, ComfyUI tools, training approaches"
---

# Anatomy Correction in Diffusion Models

Methods for detecting and fixing anatomy mutations (extra fingers, distorted hands, missing limbs) in diffusion-generated images. Covers post-processing fixes, during-sampling guidance, training-time solutions, and ComfyUI integration for FLUX Klein 9B.

## Detection Tools

### YOLO-based Hand/Face Detection (ComfyUI Impact Pack)

```javascript
UltralyticsDetectorProvider node (from ComfyUI-Impact-Subpack)
Models: hand_yolov8s.pt, hand_yolov8n.pt (bbox), face_yolov8m.pt
Location: ComfyUI/models/ultralytics/bbox/
```

### HADM - Human Artifact Detection

Dataset: HAD - 37,000+ images annotated for human artifact localization. Detects local (distorted faces/hands) and global (missing/extra limbs) artifacts. Generalizes across unseen generators.

### MediaPipe Hand Landmarks

21 hand keypoints per hand. Finger tips at landmarks 4, 8, 12, 16, 20. Can validate finger count programmatically. Not a ComfyUI node natively - needs custom wrapper.

## During-Sampling Solutions

### NAG - Normalized Attention Guidance

The most promising during-sampling fix for FLUX/Klein. Training-free, works at inference time.

```yaml
Package: ComfyUI-NAG (github.com/ChenDarYen/ComfyUI-NAG)
Supports: FLUX, Flux Kontext, Wan, HunyuanVideo, Chroma, SD3.5, SDXL
```

**Key parameters for FLUX:**

| Parameter | Value | Notes |
|-----------|-------|-------|
| nag_sigma_end | 0.75 | For flow models like FLUX |
| nag_tau | tune first | Controls guidance schedule |
| nag_alpha | tune first | Controls guidance strength |
| nag_scale | tune last | Overall guidance magnitude |

Tune `nag_tau` + `nag_alpha` first, then `nag_scale`. Acts as negative guidance improving structural coherence.

### Flux2Klein-Enhancer (Klein 9B Only)

```yaml
Repo: github.com/capitan01R/ComfyUI-Flux2Klein-Enhancer
Klein 9B ONLY - does not work with other FLUX variants
```

Modifies active text embedding region to improve prompt adherence. Makes anatomical prompt language "stick" better when Klein ignores it:

| Parameter | Anatomy use | Notes |
|-----------|-------------|-------|
| `magnitude` 1.15-1.25 | Gentle: makes anatomy prompts effective | >1.4 causes distortion |
| `contrast` 0.10-0.20 | Sharpens concept separation | High values over-separate |
| `normalize_strength` 0-1 | Balances token emphasis | - |

Combine with anatomy LoRA: enhancer makes the prompt effective, LoRA enforces the anatomy direction. NAG adds a third orthogonal axis - none cancel each other.

### VSF - Value Sign Flip (arXiv 2508.10931)

Inference technique for negative guidance in few-step distilled models. Flips value signs in self-attention to achieve negative guidance effect without CFG. Works in models where standard negative prompts have no effect due to distillation. Complementary to NAG - both target different levels of the attention mechanism.

### Other Guidance Methods

- **PAG** (Perturbed-Attention Guidance): fixes ~80% of finger errors in SDXL at scale=0.3. FLUX support NOT confirmed.
- **SEG, SWG, PLADIS, TPG, FDG, MG**: available via `sd-perturbed-attention` package, FLUX compatibility varies.

## Post-Processing: Detect-and-Inpaint

### HandFixer (ComfyUI Native)

One-click hand repair. Uses FLUX.1-Fill as inpainting backbone.

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Xiangyu-CAS/HandFixer
pip install -r HandFixer/requirements.txt
# Requires: ae.safetensors, clip_l.safetensors, t5xxl_fp16.safetensors, fluxl-fill-dev.safetensors
```

Supports realistic + anime, images from SDXL/DiT/Midjourney. FLUX-Fill recommended over FLUX-dev (better boundary handling).

### HandRefiner (MeshGraphormer)

Most reliable approach for **guaranteed correct finger count**. Reconstructs 3D hand mesh -> depth map -> ControlNet-conditioned inpainting.

```text
ComfyUI node: MeshGraphormer Hand Refiner (in comfyui_controlnet_aux)
Key params: detect_thr=0.6, presence_thr=0.6, control_strength=0.4-0.8
```

Control strength 1.0 causes texture loss. Use 0.4-0.8 range.

### FaceDetailer (Impact Pack)

```text
Key parameters:
  guide_size: 512-768 (reference size for enlarging detected regions)
  denoise: 0.3-0.5 (subtle fix) | 0.5-0.7 (moderate correction)
  noise_mask: True
  force_inpaint: True
  feather: 5-20px
  cycle: 1-2 (2 for badly corrupted faces)
  crop_factor: 3.0
  bbox_threshold: 0.5
  dilation: 0-20
```

For hands: use `DetailerForEach` with `hand_yolov8s.pt`, denoise 0.4-0.6 (lower than faces).

### Generic Inpainting Approach

1. Detect hands with `hand_yolov8s.pt` -> get mask
2. Expand mask with Mask Grow/Dilate node (10-20px)
3. Inpaint with FLUX Fill at denoise 0.75-0.90
4. Prompt override: "detailed hand, five fingers, correct anatomy, perfect hand"

## Academic Methods (2024-2026)

### Post-Processing Papers

| Paper | Venue | Method | Scope |
|-------|-------|--------|-------|
| HandRefiner | ACM MM 2024 | MeshGraphormer 3D mesh -> depth -> ControlNet inpaint | Hands |
| HandCraft | WACV 2025 | MANO parametric model -> depth conditioning | Hands |
| RHanDS | AAAI 2025 | Decoupled structure (mesh) + style guidance | Hands |
| RealisHuman | 2024 | Two-stage: generate realistic part + repaint surrounding | Full body |
| 3D Hand Mesh-Guided | 2025 | State-of-art 3D mesh estimator + double-check algorithm | Hands |

### Training-Time Papers

| Paper | Venue | Method | Data Needed |
|-------|-------|--------|-------------|
| HG-DPO | CVPR 2025 | Direct Preference Optimization, 3-stage curriculum | ~5K-10K pairs (automated) |
| Diffusion-DPO | CVPR 2024 | DPO on 851K crowdsourced preferences | 851K pairs (Pick-a-Pic) |
| FoundHand | CVPR 2025 | 10M hand images, 2D keypoints as universal representation | Pre-trained |
| DiffBody | 2024 | Local semantic info for body part rectification | Training required |

### Hand-Specific Foundation Model

**FoundHand-10M**: 10M hand images with 2D keypoints + segmentation masks. Capabilities: repose hands, transfer appearance, synthesize novel views, zero-shot fix malformed hands. License: CC BY-NC 4.0.

## Hand Fix LoRAs

### Concept Slider LoRA (Zero Images)

Text-based slider requiring no training data:

```yaml
positive: "perfect anatomy, correct hands, five fingers"
unconditional: "broken hands, extra fingers, deformed anatomy"
# Training: 25-50 steps only, rank 4, alpha 1
# Total time: ~5 minutes
```

### Pre-trained LoRAs for Klein 9B

| LoRA | Notes | Weight range |
|------|-------|-------------|
| **klein_slider_anatomy v1.5** (Civitai 2324991) | Anatomy ONLY, no quality effects. v1.0 also fixes quality. Klein-native. | 2.0-4.0 (NOT 0-1 scale) |
| **DPO Klein 9B** (Civitai 2427102) | DPO-trained on anatomy preference pairs. Targets waxy skin + bad arms/legs/hands. | 0.5-1.0 |
| Hand Detail FLUX (Civitai 260852 v3.0) | **FLUX.1 Dev ONLY** - NOT Klein compatible | - |
| Better Hands - Flux | FLUX-specific, check Klein compatibility | 0.5-0.8 |

**Critical:** `klein_slider_anatomy` uses a 1.0-4.0 weight scale, not 0-1. Weight 2.0 = minor fix, 3.0 = prominent fix, 4.0 = maximum. Stacking at 0.5-1.0 has no meaningful effect.

**Stacking order for style + anatomy:**

```sql
1. Style LoRA:              weight 0.7-1.0, strength_clip 0.4-0.6
2. klein_slider_anatomy v1.5: weight 2.0-3.0, strength_clip 0.3-0.5
3. DPO Klein 9B (optional): weight 0.4-0.6

CLIP weight trick: reduce strength_clip on anatomy LoRA more than strength_model.
anatomy LoRA model: 1.0-3.0, clip: 0.3-0.5
This lets anatomy correction affect denoising trajectory while limiting
its influence on text token processing (where style gets encoded).
```

### Asian/Community Anatomy LoRAs

Available on Tensor.Art, Shakker.ai, LiblibAI for Klein 9B:
- **手部肢体修复完善 V5** (Tensor.Art): body + limb repair, V5 with improved hand + torso
- **YesWenwen Hand Repair** (Shakker): dedicated hand repair LoRA
- **Xian-T Hand Repair** (LiblibAI): community-tested for hands/fingers

## Training Data for Anatomy Correction

### DPO Pipeline (Automated)

1. Take 5K-10K prompts with humans/hands
2. Generate 8 images per prompt with different seeds
3. Score with PickScore/HPSv2 for quality ranking
4. Best = winner, worst = loser
5. Optionally: use real photos as winners (hard stage)
6. Effort: ~40K-80K generations, ~2-3 hours on 4x GPU

### Edit LoRA Pairs (Semi-Automated)

**Method: HandRefiner as labeler**

1. Generate batch of images with Klein 9B
2. Run HandRefiner/HandCraft (detect + fix)
3. Before = original, After = HandRefiner output
4. Auto-filter: keep only pairs where hand detector found issues
5. Need human QA pass on results

### Summary Table

| Approach | Data | Time | Quality |
|----------|------|------|---------|
| Text concept slider | 0 images | 5 min | Medium |
| Image concept slider | 4-6 pairs | 2-4 hrs | Medium-High |
| NAG (training-free) | 0 | 0 | Low-Medium |
| HandRefiner pipeline | 0 (pre-trained) | 0 | Medium |
| DPO (full) | 5K-10K pairs | 8-24 hrs training | High |
| Edit LoRA (synthetic) | 500-1000 pairs | 4-8 hrs training | Medium-High |

## Klein 9B Best Anatomy Pipeline

**Step 1 (before LoRAs): generation parameters**

| Parameter | Default | Better anatomy |
|-----------|---------|----------------|
| Steps | 4 | 8+ (dramatic improvement, especially for complex poses) |
| Sampler | euler | res2s (2x compute, better anatomy in complex poses) |
| CFG | 1.0 | 1.2-1.5 (narrow sweet spot - higher breaks) |
| Pose complexity | any | Simpler poses = fewer anatomy failures |

**Recommended pipeline order (effectiveness ranking):**

1. **Generation**: 8+ steps, simpler pose, res2s sampler
2. **LoRA stack**: `klein_slider_anatomy v1.5` weight 2.0-3.0 + optional DPO at 0.5
3. **During sampling**: NAG (`nag_sigma_end=0.75`) + Flux2Klein-Enhancer (magnitude 1.15-1.25)
4. **Post-gen detection**: `hand_yolov8s.pt` + `face_yolov8m.pt` via Impact Pack
5. **If hands bad**: HandFixer or MeshGraphormer -> FLUX Fill inpaint at denoise 0.7
6. **If face bad**: FaceDetailer at denoise 0.4-0.5
7. **Inpainting fallback**: same Klein 9B + same full LoRA stack, mask only bad area, denoise 0.35-0.45
8. **Quality gate**: aesthetic score + hand detection confidence
9. **If still bad**: regenerate with new seed (up to 3-4 attempts)

### Klein 9B Distilled vs Base for Anatomy

| | Distilled 9B | Base 9B |
|---|---|---|
| Steps | 4 (designed), 8 (anatomy fix) | 20-30 |
| CFG | 1.0 only | 3.5-5.0 (more control) |
| Anatomy quality | Poor at 4 steps, better at 8 | Significantly better |
| LoRA + ControlNet | Limited support | Full support |

## Installation

```bash
cd ComfyUI/custom_nodes

# Impact Pack (face/hand detection + detailing)
git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack
git clone https://github.com/ltdrdata/ComfyUI-Impact-Subpack

# HandFixer
git clone https://github.com/Xiangyu-CAS/HandFixer
pip install -r HandFixer/requirements.txt

# ControlNet Auxiliary (MeshGraphormer, OpenPose)
git clone https://github.com/Fannovel16/comfyui_controlnet_aux

# NAG (during-sampling guidance)
git clone https://github.com/ChenDarYen/ComfyUI-NAG

# Required models:
# ComfyUI/models/ultralytics/bbox/hand_yolov8s.pt
# ComfyUI/models/ultralytics/bbox/face_yolov8m.pt
# ComfyUI/models/unet/fluxl-fill-dev.safetensors
```

## Gotchas

- **NAG bug for FLUX**: the ComfyUI-NAG package had a FLUX guidance degradation bug fixed in June 2025. Must use the updated version - older versions make FLUX outputs worse, not better.
- **MeshGraphormer control_strength=1.0 kills texture**: using full control strength from the depth map produces plasticky, over-smoothed hands. Use 0.4-0.8 range for realistic results.
- **Klein distilled CFG must be 1.0**: the distilled model has guidance baked in. CFG > 2.0 produces "deep-fried" artifacts. The base model supports CFG 3.5-5.0 for better anatomy control.
- **4B models have significantly worse anatomy than 9B**: neither 4B variant (distilled or base) achieves acceptable anatomy quality for professional use. Budget for 9B.
- **klein_slider_anatomy weight scale is 1-4, not 0-1**: applying at weight 0.5-1.0 (typical LoRA range) has no meaningful effect. Use 2.0 for minor fixes, 3.0 for prominent artifacts.
- **Inpainting fallback must use same model + same LoRA stack**: using HandFixer (FLUX.1 Fill) on Klein-generated images creates style boundary mismatch. Use Klein 9B for the inpainting pass too.

## See Also

- [[flux-klein-9b-inference]] - optimal inference settings including anatomy hierarchy
- [[face-detection-filtering-pipeline]] - detection tools for quality gating
- [[face-beautify-edit-lora]] - edit LoRA for facial correction
- [[diffusion-lora-training]] - training parameters for Klein LoRAs
- [[lora-fine-tuning-for-editing-models]] - MMDiT editing model patterns
