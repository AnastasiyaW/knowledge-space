---
title: Qwen3-ForcedAligner-0.6B-hf — Qwen3 ASR
category: projects
date: 2026-06-26
tags: [project, qwen3-asr, qwen3-forcedaligner-0-6b-hf]
aliases: ["Qwen3-ForcedAligner-0.6B-hf"]
---

# Qwen3-ForcedAligner-0.6B-hf — Qwen3 ASR

**Development line:** `project:qwen3-forcedaligner-0-6b-hf` · thread `qwen3-asr`  
**Last event:** 2026-06-26 · 1 dated since 2026-06-26 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Qwen3-ForcedAligner-0.6B-hf is a token-classification NAR model for aligning an audio recording with its transcript. It fits when you need timestamps and already have the text, as a replacement for WhisperX.

Capabilities:

- accepts audio, a transcript and a language;
- returns timestamps for words or characters;
- works with a transcript from Qwen3-ASR or another ASR;
- supports Chinese, English, Cantonese, French, German, Italian, Japanese, Korean, Portuguese, Russian and Spanish.

Limit: up to five minutes of speech per request. This is an alignment model, not a standalone speech recognizer.

Verdict: practical for subtitles and segmentation of already-transcribed short speech, if the language is one of the 11 supported.

## Development line

- **2026-06-26 — Qwen3-ForcedAligner-0.6B-hf was linked on Hugging Face.** On 2026-06-26, the Qwen3-ForcedAligner-0.6B-hf Hugging Face model page was linked in the Qwen3 ASR thread. This is a material development-line event because it identifies a specific forced-alignment model artifact. The original post and model-card contents were not provided, so no capabilities, release claims, or usage details are asserted.

## What changed

2026-06-26 — a Transformers-compatible checkpoint, Qwen/Qwen3-ForcedAligner-0.6B-hf, for forced alignment of speech and text was published.

## How to use this

From 2026-06-26, practitioners can treat Qwen3-ForcedAligner-0.6B-hf as an identified forced-alignment model candidate in the Qwen3 ASR line, then verify the model card before adopting it.

1. Install the current Transformers build from source, as the checkpoint card instructs, until a minimum stable version with this architecture is confirmed.
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>
2. Load AutoProcessor and AutoModelForTokenClassification from Qwen/Qwen3-ForcedAligner-0.6B-hf; on GPU use bfloat16 and device_map="auto".
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>
3. Get the transcript and language from Qwen3-ASR or another ASR, then pass the audio, text and language to prepare_forced_aligner_inputs.
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>
4. Run the model without gradients and decode the logits with decode_forced_alignment to get timestamps.
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>

## Best practices

- Feed recordings no longer than five minutes and set one of the 11 supported languages explicitly.
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>
- First check that the transcript matches the recording: the model aligns the text you provide and does not correct ASR errors.
  — <https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/qwen3_asr.md>
- For batched GPU processing, measure torch.compile on your own data; the card cites about 2.5x on A100 at batch size 4, a reference point rather than a guarantee.
  — <https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The official minimum stable Transformers version for the -hf checkpoint is not stated: the card recommends installing from source, although current Transformers documentation already describes this architecture.
- No independent dated publications specific to the -hf checkpoint, beyond the official collection update of 2026-06-26, were found.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B-hf | Qwen/Qwen3-ForcedAligner-0.6B-hf — model card | 2026-09-05 |
| https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/qwen3_asr.md | Transformers documentation: Qwen3-ASR and forced alignment | 2026-09-05 |
| https://arxiv.org/abs/2601.21337 | Qwen3-ASR Technical Report | 2026-09-05 |
| https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B | Qwen/Qwen3-ForcedAligner-0.6B — Qwen ASR package documentation and benchmarks | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:qwen3-forcedaligner-0-6b-hf`, thread `qwen3-asr`, 1 dated events 2026-06-26 → 2026-06-26.
- **Practical note:** From 2026-06-26, practitioners can treat Qwen3-ForcedAligner-0.6B-hf as an identified forced-alignment model candidate in the Qwen3 ASR line, then verify the model card before adopting it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
