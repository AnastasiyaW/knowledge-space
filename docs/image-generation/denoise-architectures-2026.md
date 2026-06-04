# Denoise Architectures 2026

2025-2026 landscape of image denoising architectures: NTIRE 2025 winners, SSM/Mamba-based models, inpainting-branch approaches, diffusion-based restoration, and training recipes. Complements [[image-restoration-survey]] (classical survey) and [[sana-denoiser-architecture]] (our SANA design).

## Key Facts

- **NTIRE 2025 winner (SRC-B)**: Restormer+NAFNet hybrid + Wavelet Transform loss; +1.24 dB vs 2023 SOTA on NTIRE benchmark; arxiv 2504.12276
- **MambaIRv2** (CVPR 2025): O(N) SSM, attentive non-causal scan, +0.35 dB vs SRFormer at 9.3% fewer params; arxiv 2411.15269
- **Texture-Aware Mamba** (arxiv 2501.16583): explicit texture-region modulation inside SSM; targets selective smooth-vs-texture preservation
- **LaMa+UFFC** (ICCV 2023): Fast Fourier Convolution with corrected spectrum shift; infinite receptive field for detect-then-inpaint pipelines
- **InstructIR** (ECCV 2024): text-guided "remove X, preserve Y" restoration; github.com/mv-lab/InstructIR
- **DMD2** (NeurIPS 2024): 1-step diffusion distillation; applies to any trained diffusion restoration model post-hoc
- SwinIR production config uses **Charbonnier loss** (not L1 as stated in paper); source: KAIR `train_swinir_denoising_color.json`
- NTIRE runner-up (SNUCV): MambaIRv2 + Xformer + Restormer triple hybrid

## Architecture Landscape

| Model | Year | Class | PSNR ref | Params | Tiling-free | Texture-aware |
|---|---|---|---|---|---|---|
| **NTIRE'25 SRC-B** | 2025 | Transformer+CNN hybrid | +1.24 dB vs prior SOTA | Large | Yes (MDTA+conv) | Partial |
| **NTIRE'25 SNUCV** | 2025 | SSM+Transformer triple | Sub-SRC-B | Large | Yes | Partial |
| **MambaIRv2** | 2025 | SSM (Mamba) | +0.35 dB vs SRFormer | Medium | Yes (linear scan) | Yes (semantic neighbor) |
| **Texture-Aware Mamba** | 2025 | SSM + texture gate | Targets texture domains | Medium | Yes | Yes (explicit) |
| **NAFNet** | 2022 | Pure CNN | 40.30 dB SIDD | ~67M | Yes (fully-conv) | Partial |
| **Restormer** | 2022 | Transformer (MDTA) | SOTA deblur+denoise | ~26M | Yes (O(C²)) | Yes (MDTA) |
| **LaMa+UFFC** | 2022/2023 | Fourier CNN | Preserves source PSNR | ~51M | Yes (FFT global) | Yes (only mask) |
| **InstructIR** | 2024 | Multi-modal transformer | 30-32 dB (text-guided) | Medium | Yes | Yes (prompt-driven) |
| **DMD2** | 2024 | Distillation (1-step) | Matches teacher | Depends on base | Inherits base | Inherits base |
| **DiffBIR/SUPIR** | 2024 | Diffusion (SD/SDXL) | 27-30 dB (perceptual) | 1-15B | No (tiled) | Semantic only |

### Architecture Summaries

**NTIRE 2025 SRC-B** — Restormer encoder (MDTA transposed attention, complexity O(C²)) + NAFNet decoder (SimpleGate, fully-convolutional). Trained with Wavelet Transform loss for multi-resolution frequency supervision + progressive learning schedule. Higher overlap during patch inference. Source: https://arxiv.org/abs/2504.12276

**MambaIRv2** — State Space Model scan across spatial tokens with O(N) complexity. v2 adds *attentive non-causal scan*: tokens query semantically similar distant pixels rather than only following raster order. Eliminates fixed-window receptive field of SwinIR. Source: https://arxiv.org/abs/2411.15269 / https://github.com/csguoh/MambaIR

**Texture-Aware Mamba** (arxiv 2501.16583) — Extends MambaIR with explicit texture modulation gate: entropy-based segmentation of smooth vs textured regions → asymmetric SSM processing (conservative in texture, aggressive in smooth). Designed for fabric/hair/gemstone detail preservation.

**NAFNet** — Removes all nonlinear activations (GELU/Softmax). Uses SimpleGate (`x * y` after split) + Simplified Channel Attention. UNet backbone. Fully convolutional → native full-image inference regardless of resolution. SIDD: 40.30 dB. Source: https://github.com/megvii-research/NAFNet

**Restormer** — Multi-Dconv Head Transposed Attention (MDTA): query/key/value projected across channels, not spatial positions. Complexity O(C²HW) → spatial size does not appear in attention cost. Works on full high-res images. Source: https://github.com/swz30/Restormer

**LaMa** — Fast Fourier Convolution: `Conv(FFT(x)) → IFFT`. Each convolution sees the entire image simultaneously → true global receptive field for inpainting. **UFFC** (Chu et al., ICCV 2023) fixes: spectrum shift, unexpected spatial activation, frequency RF limits via range transform + absolute position embedding + dynamic skip. Source: https://github.com/advimman/lama

**InstructIR** — Text prompt conditions the restoration: "remove dust but preserve fabric texture". Multi-task single model handles denoising, deblurring, deraining, low-light, haze via prompt routing. Source: https://github.com/mv-lab/InstructIR

**DMD2** — Distribution Matching Distillation v2: compress any diffusion restoration model to 1-step via score distillation. Applied post-training. Teacher quality preserved in single forward pass; 10-50× inference speedup. Apply to DiffBIR, SUPIR, or custom restoration diffusion after training completes. See [[diffusion-inference-acceleration]].

**DiffBIR/SUPIR** — Two-stage: degradation removal head (CNN) → latent diffusion refinement (SD/SDXL). Perceptually strong but may hallucinate fine detail absent in input. SUPIR scales to SDXL backbone with identity preservation. Not for strict pixel-fidelity tasks.

## No-Tile Inference

Fixed-window attention (SwinIR) requires tiling at inference → border artifacts at tile seams. Three architectural families eliminate this:

| Approach | Model | Mechanism | Complexity | VRAM scaling |
|---|---|---|---|---|
| **Linear SSM** | MambaIRv2, Texture-Mamba | Sequential state scan, O(N) | O(N) | Linear in pixels |
| **Fully convolutional** | NAFNet, LaMa+UFFC | No attention; FFT or gating | O(N log N) for FFT | Linear |
| **Transposed attention** | Restormer | Attention on channel dim, not spatial | O(C²) | Constant in spatial |
| **Coarse-to-fine** | Pix2PixHD lineage | G1 at low-res + G2 local refine | Multiple passes | Sublinear |

**Why SSM avoids seams**: MambaIRv2 scans tokens in a single pass maintaining a hidden state that accumulates context from the full image before each token's output is computed. No patch boundary is introduced. For very large images (4K+), VRAM grows linearly with pixel count; 96 GB GPU handles ~1500×1500 at fp16 comfortably in one pass.

**Why fully-conv avoids seams**: NAFNet's SimpleGate and channel attention have receptive field bounded only by network depth, not window size. Full image passed as single batch item; VRAM = image area × channels × depth.

**Why Fourier avoids seams**: LaMa's FFT-based convolution is defined globally; the convolution kernel sees all spatial positions simultaneously. No locality assumption → no seam.

**Tiling still needed** for DiffBIR/SUPIR (quadratic attention) and SwinIR. See [[tiled-inference]] and [[temporal-tiling]] for overlap-blending approaches.

## Training

### SwinIR Denoise Recipe (from KAIR production config)

Source: `options/swinir/train_swinir_denoising_color.json` in https://github.com/cszn/KAIR

```python
# Architecture
SwinIR(
    img_size=128,        # patch size during training
    patch_size=1,
    in_chans=3,          # use 1 for grayscale
    embed_dim=180,
    depths=[6, 6, 6, 6, 6, 6],
    num_heads=[6, 6, 6, 6, 6, 6],
    window_size=8,
    mlp_ratio=2,
    upsampler=None,      # no super-resolution
    upscale=1,
)
```

```json
{
  "G_lossfn_type": "charbonnier",
  "G_optimizer_type": "adam",
  "G_optimizer_lr": 2e-4,
  "G_scheduler_type": "MultiStepLR",
  "G_scheduler_milestones": [800000, 1200000, 1400000, 1500000, 1600000],
  "G_scheduler_gamma": 0.5,
  "E_decay": 0.999,
  "H_size": 128,
  "batch_size": 8
}
```

- **Total iterations**: ~1.6M (production); paper reports 500K (early convergence)
- **Noise injection**: online — `noisy = clean + sigma * randn_like(clean)`, sigma ∈ {15, 25, 50}
- **Separate model per sigma level** — not a single universal model
- **Training data**: DIV2K (800) + Flickr2K (2650) + BSD500 (400) + WED (4744) ≈ 8600 images
- **Test benchmarks**: CBSD68, Kodak24, McMaster, Urban100 (color); Set12, BSD68 (gray)

```bash
# Multi-GPU launch (KAIR)
python -m torch.distributed.launch --nproc_per_node=8 --master_port=1234 \
    main_train_psnr.py \
    --opt options/swinir/train_swinir_denoising_color.json \
    --dist True
```

### Loss Recipe for Selective Texture Preservation

Combines pixel fidelity, perceptual, and frequency-domain terms:

```python
def charbonnier(pred, gt, eps=1e-3):
    return torch.sqrt((pred - gt)**2 + eps**2).mean()

total_loss = (
    1.0  * charbonnier(pred, gt)                        # pixel fidelity
  + 0.1  * perceptual_vgg(pred, gt, layers=[1,2,3,4])   # texture structure
  + 0.05 * wavelet_loss(pred, gt, levels=4)              # multi-res frequency
  + 0.05 * lpips(pred, gt)                               # learned perceptual
)
```

For **asymmetric texture preservation** (conservative in structured regions, aggressive in smooth):

```python
# Entropy-based texture mask (high entropy = texture region)
texture_mask = entropy_filter(gt, kernel=11, threshold=0.6)  # returns [0,1] map

L_texture = (texture_mask * (pred - gt).abs()).mean()         # strict in texture
L_smooth  = ((1 - texture_mask) * (pred - gt).abs()).mean()  # relaxed in smooth

total = L_smooth * 0.5 + L_texture * 2.0  # bias toward preservation
```

**NTIRE 2025 Wavelet loss** (from SRC-B winner):

```python
import pywt, torch

def wavelet_loss(pred, gt, wavelet='haar', levels=4):
    loss = 0.0
    p, g = pred, gt
    for _ in range(levels):
        # 2D DWT: returns (LL, (LH, HL, HH))
        p_coeffs = pywt.dwt2(p.cpu().numpy(), wavelet)
        g_coeffs = pywt.dwt2(g.cpu().numpy(), wavelet)
        # L1 on high-frequency sub-bands
        for p_sub, g_sub in zip(p_coeffs[1], g_coeffs[1]):
            loss += torch.tensor(p_sub - g_sub).abs().mean()
        p = torch.tensor(p_coeffs[0])  # descend to LL for next level
        g = torch.tensor(g_coeffs[0])
    return loss
```

### Detect-then-Inpaint Pipeline for Scratch/Dust

```python
# Stage 1: detect defect mask (SAM or fine-tuned Faster R-CNN)
mask = scratch_detector(image)          # binary [H, W], 1 = defect

# Stage 2: LaMa+UFFC fills only masked regions
result = lama_uffc(image, mask)         # pixel-perfect copy outside mask
# PSNR of unmasked regions = source (no degradation)
```

Source: https://github.com/advimman/lama (LaMa); UFFC paper: ICCV 2023 Chu et al.

## Gotchas

- **Issue:** SwinIR paper cites L1 loss, but KAIR production config uses Charbonnier. Training with L1 replicates paper conditions but not the production quality. -> **Fix:** Always use Charbonnier (`G_lossfn_type: charbonnier`, `eps=1e-3`). Verify via `git blame options/swinir/train_swinir_denoising_color.json` in KAIR repo.

- **Issue:** SwinIR's fixed 8×8 window attention creates visible seam lines at tile boundaries on images larger than the training patch size (128px). Higher overlap during inference reduces but does not eliminate artifacts. -> **Fix:** For production on large images, replace SwinIR with MambaIRv2 (no window) or NAFNet (fully-conv). If staying with SwinIR, use `step_size = window_size // 2` overlap and alpha-blend with Hann window — see [[tiled-inference]].

- **Issue:** DiffBIR/SUPIR may hallucinate texture details that were not present in the degraded input. This is by design (generative prior), but unacceptable for forensic or metric-sensitive workflows. -> **Fix:** Use regression models (NAFNet, Restormer, MambaIRv2) when pixel-fidelity PSNR is the primary metric. Use DiffBIR/SUPIR only when perceptual quality dominates.

- **Issue:** LaMa's original Fast Fourier Convolution suffers from spectrum shifting and unexpected spatial activation on images with unusual frequency distributions (e.g., high-contrast jewelry on black background). -> **Fix:** Use UFFC variant (Chu et al., ICCV 2023) which corrects via range transform + absolute position embedding + dynamic skip connection.

- **Issue:** MambaIRv2 sequential scan is slower in wall-clock time than parallel attention at batch=1, because SSM recurrence is inherently sequential. Memory advantage (O(N)) is real; speed advantage only materializes at very large N (>512K tokens) or batch>1. -> **Fix:** Profile on your target resolution. For 1024px images (~1024 tokens at standard patch=1), NAFNet or Restormer may be faster. MambaIRv2 wins decisively at 4K+ (>16K tokens).

- **Issue:** DMD2 distillation requires a high-quality teacher diffusion model as prerequisite; it does not improve a mediocre teacher. -> **Fix:** Train and validate the base diffusion restoration model first (T=20-50 steps, PSNR on hold-out set). Only apply DMD2 after confirmed quality.

## See Also

- [[image-restoration-survey]] — classical survey: SwinIR, NAFNet, Restormer baselines, benchmarks
- [[sana-denoiser-architecture]] — our SANA 1.6B DiT restoration design with channel-concat conditioning
- [[LaMa]] — Fast Fourier Convolution inpainting details
- [[tiled-inference]] — overlap-blending strategies for fixed-window models
- [[temporal-tiling]] — causal tile sequencing for context-aware high-res inference
- [[diffusion-inference-acceleration]] — DMD2, consistency models, and related distillation methods
- [[paired-training-for-restoration]] — training data pipeline and degradation augmentation

### Source References

- NTIRE 2025 denoising challenge report: https://arxiv.org/abs/2504.12276
- NTIRE 2025 CVPR Open Access: https://openaccess.thecvf.com/content/CVPR2025W/NTIRE/papers/Sun_The_Tenth_NTIRE_2025_Image_Denoising_Challenge_Report_CVPRW_2025_paper.pdf
- MambaIR (ECCV 2024): https://arxiv.org/abs/2402.15648
- MambaIRv2 (CVPR 2025): https://arxiv.org/abs/2411.15269
- Texture-Aware Mamba: https://arxiv.org/html/2501.16583v2
- MambaIR GitHub: https://github.com/csguoh/MambaIR
- Awesome-Mamba-Low-Level-Vision: https://github.com/csguoh/Awesome-Mamba-in-Low-Level-Vision
- Two-stage Mamba+diffusion (Sci Reports 2025): https://www.nature.com/articles/s41598-025-07032-3
- NAFNet: https://github.com/megvii-research/NAFNet
- Restormer: https://github.com/swz30/Restormer
- LaMa: https://github.com/advimman/lama
- UFFC (ICCV 2023): https://openaccess.thecvf.com/content/ICCV2023/papers/Chu_Rethinking_Fast_Fourier_Convolution_in_Image_Inpainting_ICCV_2023_paper.pdf
- InstructIR: https://github.com/mv-lab/InstructIR
- Diffusion Restoration Adapter: https://arxiv.org/abs/2502.20679
- KAIR SwinIR training configs: https://github.com/cszn/KAIR
