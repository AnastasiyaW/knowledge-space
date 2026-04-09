---
title: X-Dub
category: models
tags: [visual-dubbing, lip-sync, video-editing, wan2.2, dit, audio-driven, inpainting-to-editing, kling, kuaishou, long-video]
aliases: ["X-Dub Wan-5B"]
---

# X-Dub

Visual dubbing model that edits lip movements in video to match new audio, preserving identity and pose. Built on **Wan2.2-TI2V-5B** backbone. Key innovation: mask-free editing instead of masked inpainting. Handles videos >1 minute without quality drift.

Paper: arXiv:2512.25066 (Dec 2025). Code released March 2026. Authors: Kling Team (Kuaishou) + Tsinghua + Beihang + HKUST + CUHK.

> **Important**: released model is NOT the internal paper model. Internal used proprietary 1B DiT + LoRA. Public uses Wan2.2-5B + multi-stage SFT. Internal model cannot be released due to company policy.

## Architecture

### Two-Phase Self-Bootstrapping

**Phase 1 — Generator (training only)**: DiT inpainter creates "lip-altered counterparts" — same video with different lip movements. This produces paired training data: (original video, lip-altered video + audio).

**Phase 2 — Editor (the released model)**: DiT learns **mask-free** editing from generated pairs. At inference, takes full video + new audio → edits only lips.

```
Reference Video → VAE Encode → ref_latents ─┐
                                              ├─ concat along channels → DiT Blocks → VAE Decode → Dubbed Video
Random Noise ────────────────→ noise_latents ─┘
                                                    ↑ cross-attention
Audio → Whisper + Wav2Vec2 → AudioProjModule ───────┘
Text prompt → umt5-xxl → text embeddings (cross-attn, target only)
```

### Core Components

| Component | Implementation | Size |
|-----------|---------------|------|
| DiT backbone | Wan2.2-TI2V-5B (modified) | ~5B params |
| VAE | Wan2.2_VAE | Video autoencoder |
| Text encoder | umt5-xxl | Same as Wan2.2 |
| Audio encoder 1 | Whisper Large-v2 | ~3 GB |
| Audio encoder 2 | Wav2Vec2-base-960h | ~360 MB |
| Pose detection | DWPose (YOLOX + RTMPose) | For face cropping |

Total download: **~30.2 GB**.

### Audio Processing

Dual audio encoder — both features concatenated and projected:

```python
# Combined audio features
whisper_features  # dim=1280, high-level speech
wav2vec_features  # dim=768, low-level audio
combined = concat([whisper, wav2vec])  # dim=2048

# AudioProjModule: 4 layers of attention + FFN
# intermediate_dim=1536, 24 heads
# Output dim=3072 (matches DiT dimension)
# Injected via cross-attention in DiT blocks
```

### Inpainting → Editing (Key Insight)

Traditional lip-sync (Wav2Lip, VideoReTalking): mask mouth region → inpaint. Problem: partial context → artifacts at boundaries, inconsistent lighting/texture.

X-Dub editor: sees **entire frame** without masks. Treats dubbing as full-frame editing. The model decides what to change based on audio signal, not based on a mask. Result: coherent lighting, no boundary artifacts, handles occlusions naturally.

## Long Video Handling

Sliding-window clip-based inference with temporal stitching:

| Parameter | Value |
|-----------|-------|
| Clip length | 77 frames |
| Overlap | 5 frames (motion conditioning) |
| Resolution | 512×512 (face crop) |
| FPS | 25 (fixed) |

**Continuity mechanisms:**
1. **Motion overlap**: last 5 frames of previous clip → VAE-encode → inject as first frames of next clip's denoising
2. **Latent stitching**: average latents at clip boundaries (`smooth_transition_latent`)
3. **Border replacement**: at each denoising step, border pixels replaced with noised reference latents
4. **Color correction**: per-clip, prevents color drift
5. **Single VAE decode**: all latent segments concatenated temporally → decoded in one pass

## Identity Preservation

1. **Reference latent concat**: `[ref_latents, noise_latents]` along channel dim — full appearance info
2. **Asymmetric attention**: self-attention across ref+target (identity flows), but text/audio cross-attention on target only
3. **Triple CFG** with dynamic schedule:

```python
# Three noise predictions:
pred_nega     # no ref, no audio
pred_posi_r   # ref only
pred_posi_ra  # ref + audio

# Combine:
final = pred_nega + ref_scale * (pred_posi_r - pred_nega) + audio_scale * (pred_posi_ra - pred_posi_r)

# Dynamic schedule through denoising:
# ref_scale: cosine decay 100% → 30% (early: prioritize identity)
# audio_scale: t^1.5 ramp up (later: prioritize lip sync)
```

Default: `ref_cfg_scale=2.5`, `audio_cfg_scale=10.0`.

## Inference

```bash
python -m x_dub.infer --video input.mp4 --audio speech.wav --output dubbed.mp4
```

**VRAM: ~21 GB** (aggressive model offloading between stages). 30 denoising steps at 512×512. Slow — no distillation or caching in public release.

## Gotchas

- **No license file** — GitHub shows `license: null`. pyproject.toml says Apache-2.0 for DiffSynth framework portion only. **Usage rights ambiguous.**
- **Not the paper's model** — different backbone, different training strategy. Quantitative comparison is TODO.
- **Single-person only** — multi-person support on roadmap.
- **~2% noisy frame rate** — small percentage of outputs have severely noisy frames.
- **Face cropping simplified** — DWPose landmark-based vs paper's FLAME-mesh. Can cause jitter with rapid head movement.
- **No training code** — inference only.
- **Heavy dependencies** — OpenMMLab stack (mmengine, mmcv, mmdet, mmpose) + DiffSynth-Studio + Whisper + Wav2Vec2.
- **512×512 fixed** — face crop resolution, pasted back into original video.
- Works on non-human characters (cartoons, animals) — Wan-5B version is actually better at this than internal.

## Results

Key advantages over Wav2Lip / VideoReTalking:
- No mask artifacts (mask-free editing)
- Works on stylized/animated characters
- Handles occlusions and challenging lighting
- >1 minute videos without drift

Public Wan-5B vs internal model:
- Slightly weaker temporal stability (occasional flickering)
- Slightly weaker identity consistency
- ~2x slower inference
- **Better** generalization to non-human characters

## Relation to Other Models

- Built on **Wan2.2** (Alibaba video generation model) — same VAE, text encoder, DiT architecture
- Uses DiffSynth-Studio framework (same as [[Step1X-Edit|Qwen-Image-Edit]])
- Audio approach similar to AniPortrait, DreamTalk but with dual encoder (Whisper + Wav2Vec2)

## Key Links

- GitHub: github.com/KlingAIResearch/X-Dub
- HF weights: huggingface.co/KlingTeam/X-Dub
- Project page: hjrphoebus.github.io/X-Dub
- Paper: arxiv.org/abs/2512.25066
