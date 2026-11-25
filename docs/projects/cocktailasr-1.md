---
title: "Cocktailasr 1: cocktailasr-1 — Cocktailasr 1"
category: "projects"
date: 2026-09-16
tags: ["cocktailasr-1", "project"]
aliases: ["Cocktailasr 1: cocktailasr-1"]
---

# Cocktailasr 1: cocktailasr-1 — Cocktailasr 1

**Development line:** project:cocktailasr-1 · thread cocktailasr-1  
**Last event:** 2026-09-16 · 2 dated since 2026-08-24 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Xiaomi-CocktailASR-1 is a target-speaker speech recognition model from Xiaomi for transcribing one speaker from mixed audio.

- Target speaker extraction: isolates the reference voice from single- or multi-speaker audio.
- Large-scale multi-speaker training: trained on multi-talker datasets.
- Negative rejection: returns an empty result when the reference speaker is absent.
- Chain-of-Thought mode: exposes step-by-step reasoning during transcription.

## Development line

- **2026-08-24 — Cocktailasr 1: cocktailasr-1 update.** The Hugging Face repository Ease3/Xiaomi-CocktailASR-1 appeared, with metadata showing last modified 2026-08-25.
- **2026-09-16 — CocktailASR-1 (Xiaomi) - Multi-speaker SOTA ASR with target speaker extraction.** Two-stage processing extracts the target speaker via a voice reference and transcribes the clean signal. It ignores background speech and multi-talker noise, accepting 3-second reference audio.
  - The [README](https://github.com/xiaomi-research/xiaomi-cocktailasr-1/blob/main/README_en.md) reports WER on simulated mixtures: 4.11 on LibriMix 2mix, 12.29 on LibriMix 3mix, 2.90 on LibriSpeechMix 2mix, and 4.91 on LibriSpeechMix 3mix. Prior SOTA marks were 4.84 and 12.23 on LibriMix, and 5.4 and 7.6 on LibriSpeechMix. On meeting audio, it records 21.81 on AMI SDM and 20.63 on AliMeeting Far, compared to prior SOTA of 22.0 and 27.5. Qwen3-ASR, Gemini, and StepAudio trail behind on simulated mixtures.
  - On single-speaker audio with matched voice samples, non-empty WER reaches 1.73 on LibriSpeech and 6.57 on AliMeeting-near, matching Qwen3-ASR-1.7b. The false rejection rate on positive samples spans 0.01–0.73% across tested sets. Unrelated reference rejection hits 79.59% on LibriSpeech neg, 75.35% on Aishell neg, and 68.54% on Chinese in-house neg. CoT mode trims WER slightly, moving from 4.11 to 3.87 on LibriMix 2mix. — [README](https://github.com/xiaomi-research/xiaomi-cocktailasr-1/blob/main/README_en.md)
  - The model runs as a PyTorch custom-code model (tag mic_asr) via transformers AutoModel with trust_remote_code. The model card defines it as a target-speaker ASR SpeechLLM taking a reference clip alongside mixed or single-speaker audio. An interactive demo runs under hugging-apps/cocktail-asr-target-speaker. — [Ease3/Xiaomi-CocktailASR-1](https://huggingface.co/Ease3/Xiaomi-CocktailASR-1)

## What changed

Xiaomi released the weights, code, and an interactive demo. The README reports top WER scores across multi-speaker benchmarks (LibriMix, LibriSpeechMix, AMI SDM, AliMeeting Far), single-speaker accuracy matching standard ASR models, and negative rejection for absent speakers.

## How to use this

1. Load the model using transformers: `AutoModel.from_pretrained("Ease3/Xiaomi-CocktailASR-1", trust_remote_code=True, torch_dtype="bfloat16").cuda().eval()`. Pass the target speaker reference clip with the mixed audio to transcribe that single voice.
  — <https://huggingface.co/Ease3/Xiaomi-CocktailASR-1>
2. Run the Hugging Face Space demo to test target-speaker recognition without local setup.
  — <https://huggingface.co/spaces/hugging-apps/cocktail-asr-target-speaker>

## Best practices

- Provide a clean reference clip of the desired speaker. Unrelated reference audio triggers empty outputs, rejecting roughly 69–80% of samples in README tests. Valid speakers occasionally trigger false rejections too, so handle empty returns in application logic.
  — <https://github.com/xiaomi-research/xiaomi-cocktailasr-1/blob/main/README_en.md>
- Turn on Chain-of-Thought mode when reasoning traces are required. It yields only minor WER improvements in README benchmarks.
  — <https://github.com/xiaomi-research/xiaomi-cocktailasr-1/blob/main/README_en.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The documentation omits minimum and maximum reference audio durations; the 3-second figure lacks confirmation in linked sources.
- Test benchmarks cover English and Chinese, but documentation provides no official list of supported languages.
- Model weights reside in a personal namespace (Ease3) without documented relationship to the official xiaomi-research repository.
- Full Quick Start guidance and license details remain unstated in the page text.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/xiaomi-research/xiaomi-cocktailasr-1/blob/main/README_en.md | xiaomi-cocktailasr-1 README_en.md (xiaomi-research, GitHub) | 2026-09-16 |
| https://huggingface.co/Ease3/Xiaomi-CocktailASR-1 | Ease3/Xiaomi-CocktailASR-1 (Hugging Face model card) | 2026-09-16 |
| https://huggingface.co/spaces/hugging-apps/cocktail-asr-target-speaker | Xiaomi-CocktailASR-1 demo Space (hugging-apps, Hugging Face) | 2026-09-16 |

## Agent brief {#agent-brief}

- **Subject:** project:cocktailasr-1, thread cocktailasr-1, 2 dated events 2026-08-24 → 2026-09-16.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.