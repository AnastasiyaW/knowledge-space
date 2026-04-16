---
title: "LEMAS: Multilingual TTS and Speech Editing"
description: "LEMAS open-source multilingual TTS and word-level speech editing models - architecture, installation, 10-language support, and comparison to F5-TTS and CosyVoice."
---

# LEMAS: Multilingual TTS and Speech Editing

150K+ hours of multilingual audio training data across 10 languages, yielding two complementary models: zero-shot TTS and word-level speech editing. CC-BY-4.0.

## Models

| Model | Size | Task | Architecture |
|-------|------|------|-------------|
| LEMAS-TTS | 0.3B | Zero-shot TTS | Flow matching (F5-TTS based) |
| LEMAS-Edit | 0.3B | Speech editing | Flow matching + AR codec (VoiceCraft based) |

## Languages

Chinese, English, Spanish, Russian, French, German, Italian, Portuguese, Indonesian, Vietnamese

## LEMAS-TTS

Zero-shot voice cloning: 5-10 second reference clip → generate speech on any of 10 languages.

**Parameters:**
- `nfe_steps` - number of function evaluations (speed/quality trade-off)
- `cfg_strength` - classifier-free guidance strength
- `speed` - output speech rate multiplier
- UVR5 denoising (optional, improves quality on noisy references)

```bash
# Install
conda create -n lemas python=3.10 && conda activate lemas
sudo apt-get install -y ffmpeg  # or conda install -c conda-forge ffmpeg
git clone https://github.com/LEMAS-Project/LEMAS-TTS.git
cd LEMAS-TTS && pip install -r requirements.txt
# Download model weights from HuggingFace to pretrained_models/

# Launch Gradio UI
export PYTHONPATH="$PWD:${PYTHONPATH}"
python lemas_tts/scripts/inference_gradio.py --host 0.0.0.0 --port 7860 --share
```

HuggingFace Space: `LEMAS-Project/LEMAS-TTS`

## LEMAS-Edit

Word-level speech replacement without regenerating the full utterance. Preserves surrounding speech characteristics.

**Two backends:**

| Backend | Languages | Method |
|---------|-----------|--------|
| `lemas_tts` (flow matching) | 10 languages | Same as TTS |
| `lemas_edit` (AR codec) | 7 languages | WhisperX + MMS alignment |

The `lemas_edit` backend provides better naturalness for mid-sentence edits; `lemas_tts` has broader language coverage.

Evaluation: MUSHRA and ABX testing included in `./eval/`.

HuggingFace Space: `LEMAS-Project/LEMAS-Edit`

## Upstream Dependencies

F5-TTS, VoiceCraft, Vocos, UVR5, DeepFilterNet, Seamless-Expressive

## Open TTS Landscape (April 2026)

| Model | Org | Strengths |
|-------|-----|-----------|
| LEMAS-TTS | LEMAS Project | 10 languages, zero-shot, CC-BY-4.0 |
| F5-TTS | - | Base architecture LEMAS builds on |
| CosyVoice 2 | Alibaba | Strong Chinese, multi-speaker |
| Fish Speech | - | Fast inference, good EN/ZH |
| Kokoro TTS | - | High quality EN |
| Orpheus TTS | Canopy AI | Expressive, emotional range |
| Dia | Nari Labs | Dialogue-optimized |

## Voice Cloning Pipeline

For continuous audio generation (e.g., learning systems, voice assistants):

```python
# Architecture pattern for background audio generation
# 1. Claude API → lesson text (~2 min on voice)
# 2. LEMAS-TTS → synthesize to mp3 with cloned voice
# 3. Schedule + notification (plyer / win10toast)
# 4. Auto-play in background

# Container: pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime
# GPU: single modern GPU sufficient for 0.3B model
# Latency: real-time factor < 0.5 on T4 GPU
```

## Gotchas

- **Flow matching requires fixed NFE steps** - unlike diffusion models, LEMAS-TTS doesn't support variable step counts mid-generation. Set NFE once per run.
- **Reference audio quality directly affects output** - noisy or reverberant references produce noisy clones. Run UVR5 denoising on references before use.
- **Language detection is implicit** - the model doesn't auto-detect source language. You must specify the target language explicitly. Mismatched language/text combinations produce degraded output.
- **`lemas_edit` AR codec is slower** - autoregressive generation is slower than flow matching. For low-latency applications, use the `lemas_tts` backend even for editing.

## See Also

- [[tts-models]]
- [[voice-cloning]]
- [[voice-agent-pipelines]]
