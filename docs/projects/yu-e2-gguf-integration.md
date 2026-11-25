---
title: "YuE2 GGUF audio model: yu-e2-gguf-integration — Yu E2 Gguf Integration"
category: "projects"
date: 2026-09-15
tags: ["project", "yu-e2-gguf-integration"]
aliases: ["YuE2 GGUF audio model: yu-e2-gguf-integration"]
---

# YuE2 GGUF audio model: yu-e2-gguf-integration — Yu E2 Gguf Integration

**Development line:** project:yu-e2-gguf-integration · thread yu-e2-gguf-integration  
**Last event:** 2026-09-15 · 2 dated since 2026-09-13 · **Researched:** 2026-11-25 · confidence: medium

## What it is

YuE2 GGUF audio model runs YuE2-3B text-to-music inside audio.cpp for pure C++ inference without Python.

audio.cpp provides ggml audio inference across speech recognition, voice conversion, TTS, and music generation. The project packages native GGUF weights for YuE2-3B in BF16, Q8_0, and Q4_0, along with F32 and F16 VAE files.

## Development line

- **2026-09-13 — YuE2 GGUF audio model integration reduces VRAM requirements.** audio.cpp added YuE2 support in GGUF so the model runs in 8-9 GB VRAM instead of 24 GB. Release artifacts list prebuilt binaries.
  - The model card lists BF16, Q8_0, and Q4_0 YuE2-3B GGUF files with F32 and F16 VAE files. On an RTX 5090 in audio.cpp server mode, longform tests reached 12535 MiB peak VRAM for BF16 with F32 VAE. Q8_0 with F16 VAE took 8867 MiB, and Q4_0 with F16 VAE took 7755 MiB. Real-time factors were 0.2688, 0.1992, and 0.1997. The card states the model is merged into main. (undated) — <https://huggingface.co/audio-cpp/Yue2-3B-GGUF>
  - The audio.cpp repository tags yue2 and music-generation. It runs on Windows, Linux, and macOS across NVIDIA, AMD, Apple Silicon, and CPU-only setups. All released model families support GGUF loading. (2026-09-15) — <https://github.com/0xShug0/audio.cpp/tree/dev>
- **2026-09-15 — YuE2 GGUF audio model: yu-e2-gguf-integration update.** audio.cpp release v0.8.1 added independent AR and NAR LoRA adapters for YuE2 across CLI and server, plus AR LoRA selection in WebUI. The release also added six new model families. (found in research)

## What changed

audio.cpp added YuE2 support using GGUF weights. On an RTX 5090 longform test, peak VRAM measured 12535 MiB for BF16 with F32 VAE. Q8_0 with F16 VAE used 8867 MiB, and Q4_0 with F16 VAE used 7755 MiB. The model card states support merged into main, whereas the announcement pointed to dev. Release 0.8.1 later added LoRA support for YuE2.

## How to use this

1. Download the Yue2-3B GGUF repository from Hugging Face and build audio.cpp. Run audiocpp_cli with --task gen --family yue2 --model <YUE2_GGUF> --backend cuda, and pass the style and lyrics via --request-option and --text.  
  — <https://huggingface.co/audio-cpp/Yue2-3B-GGUF>
2. To use lower-VRAM Q4_0 weights, add --session-option yue2.model_gguf=yue2-3b-q4_0.gguf and --session-option yue2.vae_gguf=yue2-vae-f16.gguf. For Q8_0, use yue2-3b-q8_0.gguf with the same F16 VAE.  
  — <https://huggingface.co/audio-cpp/Yue2-3B-GGUF>

## Best practices

- Pair the quantized main model (Q8_0 or Q4_0) with the F16 VAE to get the measured VRAM savings. Listen to the comparison files against BF16 before choosing a quantization, since the card generates them from identical prompts and seeds.  
  — <https://huggingface.co/audio-cpp/Yue2-3B-GGUF>
- Check the license before commercial use. The model card lists the GGUF repository as cc-by-nc-4.0 and points to the upstream license.  
  — <https://huggingface.co/audio-cpp/Yue2-3B-GGUF>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The linked pages do not confirm the earlier 24 GB requirement. In the project's test, the BF16 build peaked at about 12.5 GB.
- Measured VRAM figures come from one RTX 5090 test with one longform example. Other GPUs and prompts may differ.
- The linked pages do not show prebuilt binary artifacts on the release page, leaving that claim unverified.
- The Hugging Face model card carries no publication date.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/0xShug0/audio.cpp/tree/dev | GitHub - 0xShug0/audio.cpp at dev | 2026-09-15 |
| https://huggingface.co/audio-cpp/Yue2-3B-GGUF | audio-cpp/Yue2-3B-GGUF · Hugging Face | 2026-09-15 |

## Agent brief {#agent-brief}

- **Subject:** project:yu-e2-gguf-integration, thread yu-e2-gguf-integration, 2 dated events 2026-09-13 → 2026-09-15.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.