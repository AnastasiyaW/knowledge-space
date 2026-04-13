# Retouch4me: Competitive Analysis

Date: 2026-04-03
Context: Architectural and product analysis for building a competing retouching product.

---

## Company Profile

- **Legal entity:** RELU OU (Estonia, Tallinn, Vesivarava 50-201)
- **Founded:** March 28, 2021. Registration: 16194437
- **Founder:** Oleg Sharonov (also author of 3D LUT Creator)
- **Background:** professional developer, started with virtual synthesizers. 8 years retouching experience + 2 years deep learning study
- **Revenue:** EUR 2.63M (2023), CAGR 19%
- **Users:** 70+ countries
- **Funding:** bootstrapped (no external rounds found)

---

## Product Line

### 13 Photo Plugins

Each plugin = separate neural network trained for specific retouching task:

| Plugin | Task | Price |
|--------|------|-------|
| Heal | Blemish/pimple removal | $124 |
| Dodge & Burn | Automated high-end D&B | $149 |
| Skin Tone | Skin tone correction, evening | $124 |
| Mattifier | Remove oily sheen/highlights | $124 |
| Portrait Volumes | Add depth and volume | $124 |
| Skin Mask | Generate skin mask (face/body) | $124 |
| Eye Vessels | Red vessel removal | $124 (bundle) |
| Eye Brilliance | Eye glare enhancement | $124 (bundle) |
| White Teeth | Teeth whitening | $124 |
| Fabric | Fabric wrinkle removal | $124 |
| Clean Backdrop | Background cleanup | $149 |
| Stray Hair | Stray hair removal | $124 |
| Dust | Dust/particle removal | $124 |

**Free:** Panel (Photoshop panel), Frequency Separation, Glasses Glare Removal (in Apex), Face Make Lifting (in Apex).

### 2 Video Plugins

| Plugin | Task | Price | Standard |
|--------|------|-------|---------|
| Dust OFX | Video dust/particle removal | $349 | OFX |
| Color Match OFX | Video color matching | n/a | OFX |

OFX support: DaVinci Resolve 18+, Nuke, VEGAS Pro, Natron, Assimilate SCRATCH.

### Apex - Cloud All-in-One

Strategic flagship product. Includes all plugins; inference runs on Retouch4me servers (cloud-only).
Works standalone + as plugin (Photoshop, Lightroom, Affinity Photo).
No local hardware requirement.

### Arams - Standalone App

All plugins in one app, batch processing (unlimited), built-in file management, no Photoshop required.

---

## Pricing

### Perpetual License (local plugins)
- $124-149 per plugin, lifetime
- Free updates forever
- 3 activations (1 active + 2 backup)
- Hardware-bound

### Cloud Credits (Panel / Apex)

| Package | Price | Per-photo |
|---------|-------|-----------|
| Trial | Free | 20 retouches |
| 100 retouches | $20 (one-time) | $0.20 |
| Basic | $20/mo | 200 ($0.10) |
| Pro | $35/mo | 500 ($0.07) |
| Business | $90/mo | 1500 ($0.06) |

1 credit = 1 downloaded retouched photo (any number of tools can be applied).

---

## Technical Architecture

### Inference Engine

**Critical finding: Retouch4me uses a proprietary inference engine.**

From Oleg Sharonov interviews: tried several ML training frameworks but none suitable for desktop deployment inside Photoshop. Built custom engine for full control.

- **NOT ONNX, NOT TensorFlow, NOT PyTorch** for inference
- Custom engine with **OpenCL** for GPU acceleration
- CPU inference via Intel OpenCL 1.1+
- Requirement: GPU 4GB+ VRAM or Intel CPU with OpenCL

### Neural Network Architecture

- **CNN (Convolutional Neural Networks)** - core
- **Encoder-decoder** architectures
- **Partial convolutions** - for damaged region inpainting
- **Perceptual losses** - optimization on perceptual metrics (features from pretrained networks), not pixel-wise L2
- Each plugin = separate network trained on "before/after" pairs from professional retouchers

### Model Sizes

- Heal installer: ~35-41 MB (Windows), ~20 MB (macOS)
- **Models bundled in installer** - no separate weight download
- Implies compact CNNs (tens of MB per module)
- Optimized for OpenCL inference

### Processing Modes

**On-Device (local):**
- Custom OpenCL engine
- GPU or CPU
- Requires 4GB+ VRAM
- Fully offline after activation

**Cloud Retouch (Panel/Apex):**
- Inference on Retouch4me servers
- Server: `retoucher.hz.labs.retouch4.me`
- REST API with task endpoints
- No local hardware requirement

---

## Cloud API

**Base URL:** `https://retoucher.hz.labs.retouch4.me/api/v1/`

Key endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/info/limits` | GET | File limits (formats, size, resolution) |
| `/retoucher/getFile/{id}` | GET | Retrieve processed file |
| task creation | POST | Create retouching task |
| task status | GET | Check task status |

**Limits:** PNG/JPG/JPEG, max 100 MB, max 250 megapixels.

**Professional mode:** `mode=professional`, `layers=1` → server returns ZIP with separate layers.

---

## System Requirements

**Windows:** Win 7/10/11 x64, 6GB RAM, CPU 1.2GHz x64, GPU 4GB+ VRAM with OpenCL OR Intel CPU with OpenCL 1.1+. Recommended: RTX 3050 8GB / RTX 4070Ti 12GB.

**macOS:** 10.14+ (10.15+ for new products), Mac 2015+ (Intel, M1-M4 natively supported).

---

## Licensing and Protection

### License Model
- 1 active key + 2 backup keys (3 total activations)
- Hardware configuration bound
- Max 2 simultaneous active devices
- Hardware change invalidates key; use backup
- Extra key: via support only, minimum 6 months after purchase

### Mechanism
- Hardware-bound activation
- **No self-service deactivation** (no user dashboard)
- Old activations cannot be removed technically
- Changing laptop: contact support for new activation

### Anti-Piracy State

From Russian-language forums (diakov.net, 4pda.to):
- "Treated" (cracked) versions exist with verification disabled
- Retouch4me claims many crashes caused by pirated versions
- Pirated versions sometimes destabilize legitimate plugins installed alongside
- Norton antivirus sometimes flags plugins (likely due to protection obfuscation)

---

## Weaknesses (Competitive Opportunities)

### Primary Weaknesses

1. **Price:** $124-149 per plugin. Full suite = $1500+. High barrier for emerging market photographers.

2. **Fragmentation:** 13 separate plugins. No single unified solution (Apex is cloud-only, no offline mode).

3. **License UX (top complaint):** Hardware binding with no self-service deactivation. Users lose activations when changing hardware. Must contact support. 6-month wait for additional keys. Primary Trustpilot complaint.

4. **Minimal user control:** Single strength slider. No region-specific control, masks, presets, fine-tuning.

5. **OpenCL-only:** No CUDA-specific optimizations, no Metal shaders. ONNX Runtime would cover CUDA/DirectML/CoreML/OpenVINO.

6. **No SDK/embeddable:** Plugin or API only. No option to embed in custom pipeline.

7. **Apex cloud lock-in:** Apex works ONLY via cloud, no offline mode.

### Technical Architecture Opportunities

| Retouch4me Approach | Better Alternative |
|--------------------|--------------------|
| Proprietary OpenCL engine (significant investment) | ONNX Runtime (CUDA/DirectML/CoreML/OpenVINO) - faster development + broader compatibility |
| In-process Photoshop filter | Out-of-process daemon with IPC (crash isolation) |
| 13 separate plugins | Single product with toggleable modules |
| No user dashboard | License self-service portal |

---

## Competitive Positioning Summary

**Retouch4me strengths:** 8+ years market presence, professional retoucher training data, proven quality, perpetual licensing preferred by photographers, expanding into video.

**Their vulnerabilities (our opportunity):**
1. Price + fragmentation → single product at lower price point
2. License UX → self-service dashboard, flexible transfer
3. No fine-tuning → strength per region, layer masks, presets
4. No SDK → embeddable library for custom pipelines
5. OpenCL-only → ONNX Runtime for better GPU coverage
6. Cloud-only Apex → unified local+cloud with offline fallback

---

## Gotchas

- **Hardware-bound activation without self-service deactivation is the #1 UX complaint** on Trustpilot. This is a solvable problem (implement a device management dashboard) and a strong differentiator.
- **OpenCL requirement (4GB+ VRAM) limits market reach.** ONNX Runtime DirectML works on any DX12 GPU (down to integrated graphics for simpler models), and CoreML uses Apple Neural Engine on modern Macs.
- **Pirated versions causing instability in legitimate installs** suggests their protection interacts with the host process in ways that create collateral damage. Clean out-of-process architecture avoids this.
- **Norton flagging the plugins** is a customer support burden. Known obfuscation techniques trigger AV heuristics. Balance between protection strength and false-positive rate.
- **"No dashboard" is not a security feature** - it's a UX failure. Self-service deactivation with device limits (e.g., 2 concurrent, 5 total transfers per year) is strictly better: reduces support load, improves satisfaction, doesn't meaningfully weaken protection.
- **Installer-bundled models (~35-41 MB)** mean update frequency is bottlenecked by full reinstall. Separate model download infrastructure allows model updates without app updates.
