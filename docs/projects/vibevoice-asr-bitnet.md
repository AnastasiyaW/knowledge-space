---
title: VibeVoice-ASR-BitNet — Public availability
category: projects
date: 2026-08-02
tags: [project, public-availability, vibevoice, vibevoice-asr-bitnet]
aliases: ["VibeVoice-ASR-BitNet"]
---

# VibeVoice-ASR-BitNet — Public availability

**Development line:** `project:vibevoice-asr-bitnet` · thread `public-availability`  
**Last event:** 2026-08-02 · 1 dated since 2026-08-02 · **Researched:** 2026-11-21 · confidence: high

## What it is

VibeVoice-ASR-BitNet is Microsoft's MIT-licensed, compressed speech recognition model for CPU inference, run through the VibeASR.cpp runtime.

- What: ASR model, 4.62 GB reduced to 1.58 GB. The repository says the 7B Qwen2.5 language model was replaced by Qwen2.5-1.5B; the VAE is I8_S and the language model is I2_S with Q6_K parts.
- Users: developers who need multilingual transcription on CPUs without a GPU.
- Key capability: real-time factor below 1 with 3 or more threads on the card's AMD EPYC benchmark, on x86 (AVX2) and ARM (NEON).
- Limits: word error rate is higher than the 7B model, for example AISHELL4 19.83 to 27.45 and AMI-ihm 17.42 to 21.36. Accented and dialectal speech may degrade more. Windows builds need MinGW-w64, GCC or Clang; MSVC is not supported.

As of 2026-11, the repository has no tagged releases. The model card and the repository disagree on one speed figure (see Still unknown).

## Development line

- **2026-08-02 — VibeVoice-ASR-BitNet was linked to public code, model, and demo resources.** On 2026-08-02, public links connected VibeVoice-ASR-BitNet to the VibeASR.cpp repository, a Hugging Face model page, and a Hugging Face demo space. The links show public access, but they do not confirm the release version, capabilities, or whether the resources launched that day.

## What changed

- 2026-07-23 — VibeASR.cpp repository created (GitHub API metadata).
- 2026-09-15 — last push to the VibeASR.cpp repository (GitHub API metadata). The repository has no releases or tags.

## How to use this

1. Clone VibeASR.cpp with submodules, then build a Release target with CMake 3.14 or newer and a C++11 compiler. Windows users should use MinGW Makefiles.
  — <https://github.com/microsoft/VibeASR.cpp>
2. Download the pre-quantized models from the Hugging Face model page into `models/vibeasr`.
  — <https://huggingface.co/microsoft/VibeVoice-ASR-BitNet>
3. Run the `asr_infer` CLI on a WAV file with the VAE and language model paths and a thread count of at least 3 for real-time use.
  — <https://github.com/microsoft/VibeASR.cpp>
4. Optionally run the Gradio demo (`demo/gradio_asr_demo.py`) on a local port.
  — <https://github.com/microsoft/VibeASR.cpp>
5. Test on your own audio before relying on accuracy, especially for accented or noisy speech. Compare with the 7B model if word error rate matters more than size.
  — <https://huggingface.co/microsoft/VibeVoice-ASR-BitNet>

## Best practices

- Use at least 3 threads. The card reports real-time factor 1.98 at 1 thread and 0.77 at 3 threads on the EPYC benchmark.
  — <https://huggingface.co/microsoft/VibeVoice-ASR-BitNet>
- Choose the 7B model for accented or dialectal audio where the gap is large, for example AISHELL4.
  — <https://huggingface.co/microsoft/VibeVoice-ASR-BitNet>
- On Windows, use MinGW-w64. MSVC is not supported.
  — <https://github.com/microsoft/VibeASR.cpp>

## Superseded by this

- Nothing marked obsolete. The full-precision VibeVoice-ASR-7B remains the accuracy reference, not a superseded model.

## Still unknown

- Audio length limits are not specified on the model card.
- The demo Space page showed only its title, the microsoft owner and runtime metadata. Which model it runs was not confirmed.
- Real-time factor at 1 thread conflicts: 1.98 on the model card versus 1.58 in the repository README. The repository's accuracy table uses the 7B FP16 baseline, while its size table uses the 1.5B FP16 model. We did not resolve either.
- The language list differs: the card names English, Chinese, French, Italian, Korean, Portuguese, Vietnamese and "more", while the tags say 7 languages.
- No GPU path is documented for this variant.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/microsoft/VibeASR.cpp | microsoft/VibeASR.cpp — README and license | 2026-11-21 |
| https://api.github.com/repos/microsoft/VibeASR.cpp | microsoft/VibeASR.cpp — repository metadata | 2026-11-21 |
| https://huggingface.co/microsoft/VibeVoice-ASR-BitNet | microsoft/VibeVoice-ASR-BitNet — model card | 2026-11-21 |
| https://huggingface.co/spaces/microsoft/vibevoice-asr-bitnet-demo | VibeVoice ASR BitNet — Hugging Face Space (metadata only) | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:vibevoice-asr-bitnet`, thread `public-availability`, 1 dated events 2026-08-02 → 2026-08-02.
- **Practical note:** Microsoft's MIT-licensed CPU ASR model (1.58 GB) run via VibeASR.cpp. Use 3+ threads; word error rate is higher than the 7B model, especially on accented speech. Windows needs MinGW, not MSVC.
- **Confidence:** high for license, files and build steps; the 1-thread speed figure conflicts across sources. Dated supersedes above are the authority for what is obsolete.
