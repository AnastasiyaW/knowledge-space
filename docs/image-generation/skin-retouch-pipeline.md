---
title: Skin Retouch Pipeline
category: pipelines
tags: [skin-retouch, inpainting, detection, lama, patchmatch, frequency-separation, comfyui, low-vram]
---

# Skin Retouch Pipeline

Automated blemish detection and removal pipeline for photos. Two-stage architecture: detect defects -> inpaint with texture preservation. Key constraint: high-frequency skin texture (pores, microrelief) must survive the process.

## Pipeline Architecture

```
Input photo
  -> [Detection] INSID3 or YOLOE + SAM 2
  -> pixel-accurate masks with +5-10px dilation
  -> [Routing] by defect size:
     small (<1% area) -> LaMa or frequency-split
     medium/edge      -> FLUX.1 Fill (8 steps)
     problem cases    -> FLUX.1 Fill (20 steps)
```

Estimated speed on H200 (2048x2048 photo with 5-10 blemishes): ~2.5 seconds total.

## Stage 1: Detection

### INSID3 (Recommended - Training-Free)

One-shot in-context segmentation on frozen DINOv3. Annotate 1-3 reference examples of the defect type -> segments the same category on new images. No training, no decoder, no auxiliary models.

**Why ideal for skin:** one-shot by defect type (annotate 1-3 blemish examples with masks), outputs segmentation masks directly (no SAM refinement needed), Apache 2.0, self-hosted.

```python
from models import build_insid3
model = build_insid3()  # DINOv3 ViT-L default
model.set_reference("ref_acne.png", "ref_mask.png")
model.set_target("new_photo.png")
pred_mask = model.segment()
```

Speed: 3.31 FPS (3.4x faster than GF-SAM, 30x faster than Matcher). Backbones: ViT-S/B for 2 GB VRAM, ViT-L default.

### YOLOE + SAM 2 (Alternative)

YOLOE detects bounding boxes via visual prompt (SAVPE encoder). SAM 2 refines boxes to pixel-accurate masks. Two models but well-tested pipeline.

- **YOLOE**: 4-8 GB VRAM, real-time, 1.4x faster than YOLO-Worldv2. Ultralytics support.
- **SAM 2**: ~8-10 GB VRAM. Already in ComfyUI ecosystem.

### Specialized Acne Detectors

Pre-trained YOLO models exist for face acne (Roboflow yolov8-acne, skin-disease-recognition). ACNE04 dataset available for fine-tuning. These work on selfie-level faces; body shots need fine-tuning on custom data.

### Anomaly Detection Approach (MuSc)

Zero-shot, no training, no prompts. Uses the principle that normal patches have many similar neighbors, anomalies don't. Blemishes = skin anomalies. Proven on industrial inspection (MVTec AD), untested on skin domain but conceptually fitting.

## Stage 2: Inpainting

### For Small Masks (<1% area) - Classical Methods Win

For 2-20px blemishes on uniform skin, **neural networks are overkill and often worse** than classical methods. The task is copying neighboring skin, not generating structure.

#### Frequency-Split Spotfix (0 GB VRAM, recommended)

```python
# For each mask (2-20px blemish):
crop = image[y-32:y+32, x-32:x+32]          # 64x64 window
low_freq = gaussian_blur(crop, sigma=8)
high_freq = crop - low_freq + 0.5

# Replace LF in mask with median of surrounding ring
donor_low = median(low_freq, ring_8_to_30px)
# Copy HF from nearby clean skin patch
donor_hf = patchmatch_nearest(high_freq, mask, radius=50)

result = donor_low + (donor_hf - 0.5)
# Paste back with feathered edge
```

20-100ms per mask, pure CPU + numpy/OpenCV. Texture preserved because HF comes from real skin.

#### PatchMatch + Poisson Blending (0 GB VRAM)

```python
# Dilate mask +3-5px (shift seam away from defect edge)
mask_dilated = cv2.dilate(mask, kernel=5)
result = pypatchmatch.inpaint(image, mask_dilated, patch_size=7)
result = cv2.seamlessClone(result, image, mask, center, cv2.MIXED_CLONE)
```

50-200ms on 512x512 crop. PatchMatch copies real pixel patches, Poisson handles lighting mismatch.

#### Why Classical Beats Neural Here

At 2-20px mask size, there's nothing to "hallucinate" - just copy neighboring skin. PatchMatch preserves actual pores. Neural inpainters (even LaMa) tend to average HF content, producing flat "plastic" skin in the mask region.

### For Medium/Complex Masks - Neural Inpainting

#### LaMa / Big-LaMa (1-2 GB VRAM)

- ~2 seconds on HD image, 7-10% mask area
- Apache 2.0, battle-tested for skin retouch and tattoo removal
- Good on small uniform areas, poor on complex texture boundaries
- Fourier convolutions can flatten skin texture in larger masks
- Use with HF reinjection post-fix (see below)
- **LaMa-Dilated** (Qualcomm, 45.6M, 174 MB): w8a16 quantized ONNX available, 28-32ms on mobile SoCs
- **OpenCV DNN LaMa** (`opencv/inpainting_lama` on HF): runs via `cv2.dnn` without PyTorch, CPU-only path

#### FLUX.1 Fill + Turbo-Alpha (24+ GB VRAM)

- 8 steps with Turbo-Alpha LoRA: ~3-5 seconds on H200
- Best open-source semantic inpainting for skin
- Alimama ControlNet-Inpainting-Beta for direct control
- GGUF variants from 12-16 GB

#### RETHINED (WACV 2025 Oral, 0.5 GB VRAM)

Lightweight CNN for structure + patch replacement for details. Same hybrid principle as frequency-split but end-to-end trained. <=30ms on mobile. Works on UHD. Best "one model for everything" option under 2 GB VRAM.

### HF Reinjection Post-Fix

For any neural inpainter that flattens texture:

```python
# After neural inpaint:
hf_original = original_crop - gaussian(original_crop, sigma=8)
hf_donor = patchmatch(hf_original, mask_ring_30px)
# Replace HF in mask area with donor
result_hf = inpainted_crop - gaussian(inpainted_crop, sigma=8)
result_hf[mask] = hf_donor[mask]
final = gaussian(inpainted_crop, sigma=8) + result_hf
```

Neural-clean low-frequency + real-skin high-frequency. This is the frequency separation principle from professional retouching applied as automated post-processing.

## LoRA Alternative: Single-Pass Edit

Train an edit LoRA on FLUX.2 Klein 9B with before/after blemish pairs (50-200 pairs). The model learns to see and remove defects without explicit detection/masking.

**Pros:** single step, no pipeline complexity.
**Cons:** no control over what gets modified - risk of overcorrecting (smoothing pores, removing moles). Works best as semi-automated with human selection of final result.

See [[lora-fine-tuning-for-editing-models]] for training details.

## Model Specs Reference

| Model | Params | FP32 size | VRAM (512x512) | GPU speed | CPU speed | ONNX | License |
|-------|--------|-----------|----------------|-----------|-----------|------|---------|
| LaMa (regular) | 27M | ~107 MB | ~300 MB | ~30ms | ~200ms | Yes | Apache 2.0 |
| Big-LaMa | 51M | ~208 MB | ~500 MB | ~50ms | ~500ms | Yes | Apache 2.0 |
| LaMa-Dilated | 45.6M | 174 MB | ~400 MB | ~30ms | ~200ms | Yes (Qualcomm w8a16) | Apache 2.0 |
| MAT | ~61M | ~250 MB | ~500-800 MB | ~50ms | ~800ms | No | MIT |
| SD 1.5 Inpaint | ~860M | ~2 GB | 4-6 GB | ~3s | ~30s | Partial | CreativeML |
| OpenCV TELEA | 0 | 0 | 0 | <1ms | <5ms | N/A | BSD |

**SD 1.5 inpainting is rejected for <2 GB VRAM** - even INT8 quantized needs 3.5+ GB. Critical issue beyond VRAM: diffusion models generate new latent content (64px patch for a 20-25px mask), destroying pore-level high-frequency texture outside the mask boundary. Fundamental mismatch with texture preservation requirements.

## VRAM Budget Guide

| VRAM Budget | Detection | Inpainting |
|-------------|-----------|------------|
| **0 GB** (CPU) | INSID3 ViT-S on CPU | Frequency-split or PatchMatch |
| **2 GB** | INSID3 ViT-S/B | RETHINED or LaMa fp16 on 256x256 crops |
| **8 GB** | YOLOE + SAM 2 | LaMa full resolution |
| **24+ GB** | Any | FLUX.1 Fill + Turbo-Alpha (8 steps) |
| **40+ GB** | Any | Qwen-Image-Edit (20B) for complex cases |

## Gotchas

- **DINOv3 patch size (14-16px) may be too coarse** for very small blemishes (2-5px). Feed high-res crops rather than full images to INSID3 for small defect detection.
- **LaMa Fourier convolutions flatten skin texture** in larger masks - always combine with HF reinjection if texture preservation matters.
- **T-Rex2 and DINO-X are cloud-only** - no self-hosting option. Privacy concern for client photos. Use YOLOE or INSID3 instead.
- **No public end-to-end "blemish remover" model exists** with open weights. All production solutions (Lightroom, PortraitPro) are closed. Open-source approach requires assembling detect+inpaint pipeline.
- **Color jitter augmentation destroys skin retouch training** - skin tone consistency is critical for before/after pairs.

## See Also

- [[LaMa]] - Fourier convolution inpainting architecture
- [[lora-fine-tuning-for-editing-models]] - edit LoRA training for single-pass retouch
- [[in-context-segmentation]] - INSID3 and related techniques
- [[flux-klein-9b-inference]] - detail preservation during generation
