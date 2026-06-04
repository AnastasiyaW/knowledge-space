---
title: Visible Watermark Detection and Removal
category: techniques
tags: [watermark, inpainting, detection, florence2, sam2, lama, iopaint, batch-processing, fine-tuning]
---

# Visible Watermark Detection and Removal

Removing visible logos, text overlays, and branding from images. Distinct from invisible/forensic watermarks (SynthID, Tree-Ring) — those are adversarial signal-in-noise problems with no overlap here.

## Key Facts

- Bottleneck is **detection**, not removal — a bad mask produces unfixable artifacts regardless of inpainting model
- Pipeline is always 3-stage: triage → detect+mask → inpaint; each stage is fine-tunable independently
- [[object-removal-inpainting]] covers the general inpainting layer; this article focuses on watermark-specific detection and routing
- [[LaMa]] is the default inpaint backend — 2-4 GB VRAM, Apache-2.0, no hallucinations
- Commercial APIs (Dewatermark.ai, WatermarkRemover.io) cannot be fine-tuned; use as baseline only
- Dataset reference: CLWD (200-class color, ships with WDNet), LOGO-H (HF: `vinthony/watermark-removal-logo`), visible-watermark-pita (~20K pairs, HF), ILAW (large-area marks, 2025)

## Pipeline Architecture

```text
[image] → (0) triage: watermark present? → (1) detect → mask → (2) inpaint → [clean image]
```

**Stage 0 — triage.** Binary classifier routes images without watermarks around the heavy pipeline. Critical for batch dataset cleaning (30-60% skip rate typical on scraped product photos).

**Stage 1 — detection + masking.** Produces a binary mask. For known/recurring logos: precomputed template mask (deterministic, faster, zero recall error). For unknown marks: open-vocab text-prompt detection.

**Stage 2 — inpainting.** Branch on background type:
- Clean studio background or gradient → [[LaMa]] / Big-LaMa (no hallucinations, fast, CPU-capable)
- Mark overlapping product detail (stone facets, metal reflection) → diffusion inpainting at low denoise strength

End-to-end specialized models (SLBR, SplitNet, WDNet) fuse stages 1+2, but the split pipeline is easier to diagnose and fine-tune per stage.

## Stage 1: Detection and Masking Models

| Model | Role | License | Fine-tune |
|---|---|---|---|
| `prithivMLmods/Watermark-Detection-SigLIP2` (HF) | Binary triage classifier | Apache-style | Yes |
| Florence-2 base/large (`microsoft/Florence-2-large`) | Text-prompt → bbox | MIT | Yes (VLM captioning format) |
| Grounding DINO (`IDEA-Research/GroundingDINO`) | Open-vocab bbox, stronger on small logos | Apache-2.0 | Yes |
| SAM 2 / 2.1 (`facebookresearch/sam2`) | bbox/point → precise mask | Apache-2.0 | Yes |
| Grounded-SAM-2 (`IDEA-Research/Grounded-SAM-2`) | GDINO/Florence-2 + SAM2 in one pass | Apache-2.0 | Per-component |
| `watermark-segmentation` (MiT-B5/SegFormer) | Direct binary mask, no bbox stage | MIT | Designed for it (hours on single GPU) |
| `yolov8n-watermark-detection` (HF) | Lightweight bbox detector | AGPL-3.0 | Yes |

**Routing logic:**
- Known logo family → template mask (skip detector entirely)
- Mixed/unknown marks → Florence-2 or Grounding DINO prompt `"watermark, text overlay, logo"` → SAM2 for pixel mask
- AGPL on YOLOv8: toxic for closed commercial production; use GDINO or Florence-2

**Recall on semi-transparent marks** (opacity 15-40%) is the main failure mode across all detectors. Fine-tuning on synthetic pairs with low alpha values fixes most of it.

```python
# Grounded-SAM-2 one-pass example (Apache-2.0 components)
from groundingdino.util.inference import load_model, predict
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

gd_model = load_model("GroundingDINO_SwinT_OGC.py", "groundingdino_swint_ogc.pth")
sam2 = SAM2ImagePredictor(build_sam2("sam2_hiera_large.pt"))

boxes, logits, phrases = predict(
    model=gd_model, image=image,
    caption="watermark . text overlay . logo",
    box_threshold=0.30, text_threshold=0.25
)
sam2.set_image(np.array(image))
masks, _, _ = sam2.predict(box=boxes[0], multimask_output=False)
# dilate mask 4-8px before inpaint
```

## Stage 2: Inpainting Models

### Non-Diffusion (Specialized)

| Model | Year | License | Notes |
|---|---|---|---|
| SLBR (`bcmi/SLBR-Visible-Watermark-Removal`) | 2021 | Unspecified | Self-calibrated localization + background refinement; strong reliable baseline; weak on opaque large marks. arXiv:2108.03581 |
| SplitNet (`vinthony/deep-blind-watermark-removal`) | 2021 | Unspecified | Blind (no mask needed); weights partially released. arXiv:2012.07007 |
| WDNet (`MRUIL/WDNet`) | 2021 | Unspecified | Provides CLWD dataset. arXiv:2012.07616 |
| SSNet (`hellloxiaotian/SSNet`) | 2024 | Unspecified | **Self-supervised — no clean/watermarked pairs needed.** Also denoises. Best for batch cleaning without clean references |
| RORem (`leeruibin/RORem`) | CVPR 2025 | **Apache-2.0** | Human-in-the-loop trained robust eraser; fine-tunable; commercially safe alternative to FLUX Fill |
| MorphoMod | 2025 | — | Morphological dilation approach; +50.8% over prior SOTA on CLWD/LOGO/Alpha1. arXiv:2502.02676 |
| Large-Area Watermark Removal (AAAI 2025) | 2025 | — | Inpainting-prior adapter; PSNR 26.81 / SSIM 0.924 / LPIPS 0.094 on large marks; tolerates coarse masks. arXiv:2504.04687 |

**License note:** SLBR/SplitNet/WDNet/SSNet have no explicit license — research use acceptable, commercial use is legally ambiguous. For production revenue pipeline, use RORem (Apache-2.0) or the MIT/Apache inpainting stack.

### Diffusion Inpainting

| Model | License | Use case |
|---|---|---|
| LaMa / Big-LaMa via IOPaint | Apache-2.0 | Studio backgrounds, gradients, periodic textures; no hallucinations; 2-4 GB VRAM |
| SDXL Inpainting | OpenRAIL-M | Commercially safe; reconstructs structural detail under mark |
| FLUX.1 Fill [dev] | Non-Commercial | Best semantic coherence; ~24-34 GB FP16 (Q4 GGUF ~7.5 GB); outputs can be sold but model itself cannot be deployed commercially without BFL license |
| `prithivMLmods/Kontext-Watermark-Remover` (HF) | Follows FLUX.1-Kontext-dev | Ready LoRA trained on ~150 pairs; useful pre-fine-tune baseline |

See [[object-removal-inpainting]] for VRAM requirements, MAT, BrushNet, and general inpaint model comparison.

```bash
# IOPaint batch CLI (Apache-2.0, archived Aug 2025 but fully functional)
pip install iopaint

# Single image
iopaint run --model=lama --device=cuda \
  --image ./input.png --mask ./mask.png --output ./out/

# Directory batch
iopaint run --model=lama --device=cuda \
  --image ./images/ --mask ./masks/ --output ./cleaned/
```

## End-to-End and Recent Models (2024-2026)

- **Qwen-Image-Edit** (Alibaba, Aug 2025) — 20B instruction-following foundation model; natural language `"remove the watermark in the bottom-left corner"` works directly without explicit mask; Apache-2.0; open-weight, fine-tunable. HF: `Qwen/`
- **OmniEraser** (2025) — object + effect removal with ControlNet variant. `PRIS-CV/Omnieraser`
- **WMFormer++** — ~44.6 dB PSNR on LOGO-H (best classical metric); **no code released** — academic reference only. arXiv:2308.10195
- **RIRCI** — two-stage for heavy occlusion cases; **no code released**. arXiv:2312.14383

## Tooling

- **IOPaint** (`Sanster/IOPaint`, Apache-2.0) — bundles LaMa/MAT/ZITS/MIGAN/SD; real CLI batch; CPU/GPU/Apple Silicon; best production batch eraser despite Aug 2025 archive
- **comfyui-inpaint-nodes** (`Acly/comfyui-inpaint-nodes`) — LaMa/MAT/Fooocus-inpaint nodes for ComfyUI; cleanest inpaint stack
- **Grounded-SAM-2** (`IDEA-Research/Grounded-SAM-2`) — single-command GDINO+SAM2 pipeline
- **rem-wm** (`Damarcreative/rem-wm`) — Florence + lama-cleaner combined tool

## Fine-Tuning Escalation Path

Start at step 0, measure, escalate only when needed.

**Step 0 — out-of-box baseline.** IOPaint + Big-LaMa + Florence-2/GDINO+SAM2 masks. Benchmark on 50-100 representative images; identify which stage breaks.

**Step 1 — fine-tune detector** (when detection misses faint/small/semi-transparent marks).
Florence-2 or Grounding DINO on synthetic bbox/mask pairs. Hours on a single GPU; highest ROI of all escalation steps.

```python
# watermark-segmentation (MIT) — simplest fine-tune target for mask-only
# Ships train.py, M-series / single 4090 viable
# Input: pairs of (image, binary_mask_png)
# Training time: 4-8h on 4090 for 5K pairs
```

**Step 2 — fine-tune [[LaMa]]** (when studio-background fills are blurry under large masks).
```bash
# github.com/advimman/lama
# config: configs/training/
# Key: load_checkpoint_path for warm-start from Big-LaMa weights
# VRAM: ~16 GB (fits single 4090); self-supervised (masks generated on-the-fly)
```

**Step 3 — diffusion inpainting LoRA** (when mark overlaps product detail requiring texture synthesis).
- FLUX.1 Fill LoRA: needs mask-aware trainer (`Sebastian-Zok/FLUX-Fill-LoRa-Training` or SimpleTuner). Rank 32-48, 800-1500 steps, 24+ GB VRAM FP8, ~2-4h on 4090. **LoRAs from FLUX.1-dev do not transfer to Fill** (different architecture). Non-commercial license applies to model; outputs may be sold under BFL terms.
- SDXL Inpainting LoRA/DreamBooth: OpenRAIL-M (commercially cleaner). Rank 32, paired mask data, ~16-24 GB VRAM.

**Step 4 — fine-tune RORem** (Apache-2.0, CVPR 2025) for heaviest cases where all above fail. Commercially safe, code + dataset public at `leeruibin/RORem`.

## Synthetic Pair Generation

Required for all fine-tuning. Standard technique (arXiv:2403.05807):
take clean images → overlay marks (known logos + random text) with randomized scale, opacity, rotation, blend mode, position → produces (watermarked, clean) pairs + **free masks** (exact placement known).

```python
import cv2
import numpy as np
from PIL import Image

def apply_synthetic_watermark(clean_img: np.ndarray, logo: np.ndarray,
                               alpha: float = None, pos: tuple = None) -> tuple:
    """Returns (watermarked_img, binary_mask)."""
    alpha = alpha or np.random.uniform(0.15, 0.85)
    h, w = clean_img.shape[:2]
    lh, lw = logo.shape[:2]

    # Random scale and position
    scale = np.random.uniform(0.08, 0.25)
    logo_resized = cv2.resize(logo, (int(lw * scale * w / lw), int(lh * scale * h / lh)))
    lh, lw = logo_resized.shape[:2]

    px = pos[0] if pos else np.random.randint(0, max(1, w - lw))
    py = pos[1] if pos else np.random.randint(0, max(1, h - lh))

    watermarked = clean_img.copy().astype(float)
    region = watermarked[py:py+lh, px:px+lw]
    if logo_resized.shape[2] == 4:  # RGBA
        logo_alpha = logo_resized[:, :, 3:4] / 255.0 * alpha
        logo_rgb = logo_resized[:, :, :3]
    else:
        logo_alpha = alpha
        logo_rgb = logo_resized

    watermarked[py:py+lh, px:px+lw] = region * (1 - logo_alpha) + logo_rgb * logo_alpha

    mask = np.zeros((h, w), dtype=np.uint8)
    mask[py:py+lh, px:px+lw] = (logo_alpha.squeeze() > 0.05).astype(np.uint8) * 255

    return watermarked.clip(0, 255).astype(np.uint8), mask
```

Available ready-made datasets for bootstrapping: CLWD (WDNet repo), LOGO-H (HF), visible-watermark-pita (HF), ILAW (arXiv:2504.04687 supplementary).

## License Summary

| Component | License | Commercial |
|---|---|---|
| watermark-segmentation, Florence-2 | MIT | Yes |
| Grounding DINO, SAM 2, LaMa, IOPaint, RORem | Apache-2.0 | Yes |
| SDXL Inpainting | OpenRAIL-M | Yes (with use restrictions) |
| Qwen-Image-Edit | Apache-2.0 | Yes |
| FLUX.1 Fill [dev] | Non-Commercial | Model: No. Outputs: Yes (BFL commercial license required for deployment) |
| SLBR / SplitNet / WDNet / SSNet | Unspecified | Legally ambiguous — research OK |
| yolov8n-watermark-detection | AGPL-3.0 | Toxic for closed-source production |

## Gotchas

- **Issue:** Detection missing semi-transparent marks (opacity < 40%) even after prompt tuning -> **Fix:** Generate synthetic pairs specifically at alpha 0.10-0.45 and fine-tune watermark-segmentation (MIT, explicit fine-tune support); this is almost always the actual recall bottleneck, not the inpainting model.
- **Issue:** FLUX.1 Fill LoRA trained on FLUX.1-dev weights does not work — zero effect or artifacts -> **Fix:** Train directly on FLUX.1-Fill-dev checkpoint; the architectures differ (Fill has additional inpainting conditioning channels). Use `Sebastian-Zok/FLUX-Fill-LoRa-Training` which handles this; do not reuse dev LoRAs.
- **Issue:** `yolov8n-watermark-detection` used in commercial pipeline triggers AGPL copyleft obligation -> **Fix:** Replace with Grounding DINO (Apache-2.0) + SAM2 (Apache-2.0); slightly heavier but commercially clean.
- **Issue:** IOPaint Big-LaMa blurs fine texture (gem facets, metal highlights) under large masks -> **Fix:** Route marks overlapping product detail to diffusion inpainting (SDXL-Inpaint or FLUX Fill) at low denoise (0.5-0.65); keep LaMa for marks on background only. See [[object-removal-inpainting]] for routing logic.
- **Issue:** Visible watermark research overlaps with invisible/forensic watermark papers in search results (SynthID, Tree-Ring, UnMarker USENIX 2025) -> **Fix:** Filter for keywords "visible watermark removal", "CLWD dataset", "LOGO-H benchmark"; ignore anything mentioning "steganography", "provenance", "C2PA", or "adversarial attack on detector".

## See Also

- [[object-removal-inpainting]] — general erasure models (EraDiff, TurboFill, BrushNet, PowerPaint) and VRAM comparison table
- [[LaMa]] — FFC architecture, Big-LaMa vs standard variants, IOPaint integration
- [[paired-training-for-restoration]] — supervised training with synthetic degradation pairs
- [[in-context-segmentation]] — SAM2 and Grounded-SAM-2 masking patterns
- [[segmentation-dataset-preparation]] — preparing mask datasets for detector fine-tuning
- [[diffusion-lora-training]] — LoRA fine-tuning for FLUX Fill and SDXL inpainting
- Awesome-Visible-Watermark-Removal: github.com/bcmi/Awesome-Visible-Watermark-Removal
- SLBR: github.com/bcmi/SLBR-Visible-Watermark-Removal / arXiv:2108.03581
- SSNet: github.com/hellloxiaotian/SSNet
- RORem (CVPR 2025): github.com/leeruibin/RORem
- Grounded-SAM-2: github.com/IDEA-Research/Grounded-SAM-2
- IOPaint: github.com/Sanster/IOPaint
- FLUX.1-Fill-dev: huggingface.co/black-forest-labs/FLUX.1-Fill-dev
- Kontext-Watermark-Remover: huggingface.co/prithivMLmods/Kontext-Watermark-Remover
- Large-Area Removal AAAI 2025: arXiv:2504.04687
- MorphoMod: arXiv:2502.02676
- Self-supervised synthetic pairs: arXiv:2403.05807
