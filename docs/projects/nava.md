---
title: NAVA
category: projects
date: 2026-06-03
tags: [nava, nava-development, project]
aliases: ["NAVA"]
---

# NAVA

**Development line:** `project:nava` · thread `nava-development`  
**Last event:** 2026-06-03 · 1 dated since 2026-06-03 · **Researched:** 2026-09-06 · confidence: medium

## What it is

NAVA is a local joint audio-video model for text-to-audio-video, first-frame image continuation, audio-only generation, and reference-timbre speech.

- Generates video and stereo scene/speech audio together instead of attaching audio after video generation.
- Uses an Align-then-Fuse MMDiT; reference WAVs map to ordered `<S>…<E>` speech spans.
- 1280×704 at 37 frames/24 fps runs for about six seconds; full-resident inference is documented at 80 GB VRAM, while the FP8 path is about 18 GB.
- Use the maintained local code or ComfyUI path; the official hosted Space was paused when checked.

## Development line

- **2026-06-03 — NAVA public project resources were linked.** On 2026-06-03, NAVA linked its project page, GitHub repository, and Hugging Face page to direct readers to documentation, source code, and model resources.

## What changed

- 2026-05-28 — NAVA paper v1 described a 6.3B Align-then-Fuse MMDiT for joint audio-video generation.
- 2026-05-29 — NAVA reached its official initial model release.
- 2026-05-30 — NAVA uploaded `NAVA.safetensors` and removed the Hub copy of legacy `NAVA.ckpt`.
- 2026-06-01 — NAVA added the `NAVA_fp8.safetensors` lower-VRAM checkpoint.
- 2026-06-03 — NAVA uploaded English and Simplified-Chinese model-card documentation; GitHub also updated the README and optimized inference.
- 2026-06-05 — NAVA added FP8 support for ComfyUI.
- 2026-06-08 — NAVA optimized and cleaned up its ComfyUI implementation.
- 2026-06-15 — NAVA fixed FP8 prompt-rewriter desynchronization and added a vision-language rewrite workflow.
- 2026-06-23 — NAVA updated its Hugging Face Space and Gradio implementation.
- 2026-06-30 — NAVA updated VerseBench inference scripts.

## How to use this

1. Treat the official hosted demo as unavailable for now: its Space was paused when checked; use a local workflow instead.
  — <https://huggingface.co/spaces/baidu/NAVA>
2. Clone the official code, install CUDA-matched PyTorch first, then install NAVA and FlashAttention in the documented order.
  — <https://github.com/ernie-research/NAVA>
3. Download the maintained weights from the current `baidu/NAVA` model page; use `NAVA.safetensors` for bf16 or `NAVA_fp8.safetensors` for the lower-VRAM path.
  — <https://huggingface.co/baidu/NAVA>
4. Put each job in JSONL: use `prompt` for text-to-audio-video, add `image_path` for first-frame conditioning, and add up to two `spk_wavs` for timbre-controlled speech; then choose the matching inference script.
  — <https://github.com/ernie-research/NAVA>
5. For a node workflow, install the official ComfyUI nodes, select `NAVA_fp8.safetensors`, and load one of the supplied example graphs.
  — <https://github.com/ernie-research/NAVA/blob/main/comfyui_nava/README.md>

## Best practices

- Keep the CUDA-matched PyTorch install, editable NAVA install, and `flash-attn --no-build-isolation` as separate steps; do not force-reinstall the requirements file.
  — <https://github.com/ernie-research/NAVA>
- Rewrite short or English prompts before inference, and preserve every `<S>…<E>` speech span unchanged.
  — <https://github.com/ernie-research/NAVA>
- Keep reference WAV order aligned to speech-span order; for ComfyUI, enable T5 offload first and group offload below 48 GB VRAM.
  — <https://github.com/ernie-research/NAVA/blob/main/comfyui_nava/README.md>
- Use FP8 to reduce VRAM, not to expect faster matrix computation; it dequantizes to bf16 at compute time.
  — <https://github.com/ernie-research/NAVA>
- Use consent-approved face and voice references, label generated material as synthetic, and apply provenance or watermarking before redistribution.
  — <https://huggingface.co/baidu/NAVA>
- Default to the current safetensors checkpoints; the Hub deleted `NAVA.ckpt`, although local code retains checkpoint compatibility.
  — <https://huggingface.co/baidu/NAVA/commits/main>

## Superseded by this

- 2026-05-30 — Hub download guidance requiring `NAVA.ckpt` is obsolete: the official Hub removed that artifact and provides safetensors checkpoints; local `.ckpt` compatibility remains.
- 2026-06-05 — Treating NAVA as an 8-GPU script-only workflow is outdated: the official project added an FP8 ComfyUI path.
- 2026-06-15 — Pre-fix FP8 prompt-rewrite guidance is outdated for image-conditioned work: the official code fixed rewriter desynchronization and added VL rewrite.

## Still unknown

- The exact accompanying text of the 2026-06-03 entry is unavailable, so we treat that date as a same-day documentation and inference-update milestone, not an inferred launch announcement.
- No semantic release tags or GitHub Releases map commit-level changes to versioned NAVA releases.
- The official Space was paused when checked, so a successful current hosted-inference run was not verified.
- Official documentation is internally inconsistent: current code defaults to safetensors while parts of the model card still show deleted `NAVA.ckpt` paths.
- No later first-party code or model-history entry was found after 2026-06-30; this does not prove that no update exists outside the checked official histories.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2605.30073 | Native Audio-Visual Alignment for Generation — arXiv:2605.30073 | 2026-09-06 |
| https://ernie-research.github.io/NAVA/ | NAVA · Native Audio-Visual Alignment for Generation | 2026-09-06 |
| https://github.com/ernie-research/NAVA | ernie-research/NAVA — Official Code of NAVA | 2026-09-06 |
| https://github.com/ernie-research/NAVA/commits/main | Commits · ernie-research/NAVA | 2026-09-06 |
| https://huggingface.co/ernie-research/NAVA | ernie-research/NAVA redirect to baidu/NAVA | 2026-09-06 |
| https://huggingface.co/baidu/NAVA | baidu/NAVA · Hugging Face | 2026-09-06 |
| https://huggingface.co/baidu/NAVA/commits/main | Commits · baidu/NAVA | 2026-09-06 |
| https://huggingface.co/baidu/NAVA/blob/main/README_zh.md | README_zh.md · baidu/NAVA | 2026-09-06 |
| https://github.com/ernie-research/NAVA/blob/main/comfyui_nava/README.md | NAVA ComfyUI Nodes | 2026-09-06 |
| https://huggingface.co/spaces/baidu/NAVA | NAVA Audio-Video Generator — Hugging Face Space | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:nava`, thread `nava-development`, 1 dated events 2026-06-03 → 2026-06-03.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
