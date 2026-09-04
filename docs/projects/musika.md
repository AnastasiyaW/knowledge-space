---
title: MUSIKA
category: projects
date: 2022-10-21
tags: [musika, project]
aliases: ["MUSIKA", "Musika"]
---

# MUSIKA

**Development line:** `project:musika` · thread `musika`  
**Last event:** 2022-10-21 · 2 dated since 2022-08-19 · **Researched:** 2026-09-04 · confidence: medium

## What it is

MUSIKA is an open TensorFlow GAN pipeline for generating arbitrary-length waveform music in a trained domain with tempo and note-density controls instead of text prompts.

- Hierarchical latent representations to encode and reconstruct audio.
- Unconditional and tempo- or note-density-conditioned generation for music.
- Custom dataset encoding to train from scratch or fine-tune a checkpoint.

Requirements pin TensorFlow 2.10.0 and Gradio 3.3.1, while the official Space reports a build error. Use it as local legacy research code for controlled experiments, not as an available hosted tool.

## Development line

- **2022-08-19 — MUSIKA project website linked.** On 2022-08-19, the MUSIKA project website became a public reference point. The announcement and specific change were not detailed.
- **2022-10-21 — MUSIKA repository and Hugging Face Space linked.** On 2022-10-21, public links connected to the MUSIKA GitHub repository, Hugging Face Space, and a channel reference. The links did not specify a release or model revision for that day.

## What changed

2022-08-19 — MUSIKA’s project page described non-autoregressive, arbitrary-length waveform generation, with unconditional and tempo- or note-density-conditioned examples.  
2022-10-21 — GitHub and Hugging Face became linked operational paths. Closely dated launch material specified 44.1 kHz stereo output, a new demo, and custom-data training or fine-tuning.

## How to use this

As of 2022-10-21, use the linked GitHub repository and Hugging Face Space as public entry points for MUSIKA. Treat claimed release details as unverified until original posts or linked resources are checked.

1. Create the documented local environment: Conda with Python 3.9 and FFmpeg. Use CUDA 11.2 and cuDNN 8.1 for an NVIDIA GPU, then clone the repository and install its requirements.
  — <https://github.com/marcoppasini/musika>
2. Run `python musika_test.py` for the local Gradio interface. It defaults to Techno weights; use `--load_path checkpoints/misc` for the diverse-music checkpoint.
  — <https://github.com/marcoppasini/musika>
3. For batch output, run `python musika_generate.py --load_path checkpoints/misc --num_samples 10 --seconds 120 --save_path generations` and adjust count and duration.
  — <https://github.com/marcoppasini/musika>
4. For a custom domain, encode recordings with `musika_encode.py`, then either train from scratch or fine-tune the `misc` or `techno` checkpoint.
  — <https://github.com/marcoppasini/musika>

## Best practices

- Fine-tune only on a narrow target domain with limited timbre diversity; use scratch training for diverse data. Start from the documented 0.00004 learning rate and reduce it to 0.00002 if training becomes unstable or produces NaNs.
  — <https://github.com/marcoppasini/musika>
- Keep encoding and training `max_lat_len` aligned. The default expects at least 47-second inputs; lowering it to 256 supports about 23-second inputs.
  — <https://github.com/marcoppasini/musika>
- Before committing to a dataset, encode then decode representative audio and listen to the reconstruction: it is the documented upper bound on generation quality. Expect the universal autoencoder to be weaker on vocal-heavy material.
  — <https://github.com/marcoppasini/musika>
- Disable mixed precision on unsupported GPUs; if local CUDA/XLA fails, use `--xla False` rather than treating the default acceleration path as mandatory.
  — <https://github.com/marcoppasini/musika>

## Superseded by this

- 2022-10-20 — The 22.05 kHz paper implementation is retained in `22kHz/`; repository guidance identifies the 44.1 kHz implementation as current.
- 2026-09-04 — “Try the online demo” is not current operating guidance: the official Space’s most recently observed state is a build failure, so use a local clone until it is repaired.

## Still unknown

- The exact text and intent of the two dated references are unavailable, so their scope cannot be reconstructed beyond the linked destinations and dated corroboration.
- The October 44.1 kHz association relies on a dated secondary archive that embeds a developer post from 2022-10-20; the original social post was not retrievable directly.
- No fresh local install or generation test was run, so compatibility with current Python, CUDA, and GPU environments is unverified.
- The retrieved Space page was cached; its build status may have changed after that observation.

## Sources

| source | title | read |
|---|---|---|
| https://marcoppasini.github.io/musika | Musika! Fast Infinite Waveform Music Generation | 2026-09-04 |
| https://arxiv.org/abs/2208.08706 | Musika! Fast Infinite Waveform Music Generation | 2026-09-04 |
| https://github.com/marcoppasini/musika | marcoppasini/musika — Fast Infinite Waveform Music Generation | 2026-09-04 |
| https://raw.githubusercontent.com/marcoppasini/musika/main/requirements.txt | musika requirements.txt | 2026-09-04 |
| https://huggingface.co/spaces/marcop/musika | Musika — a Hugging Face Space by marcop | 2026-09-04 |
| https://huggingface.co/marcop/musika_ae/commit/4572cc3d89d024e14db630b1796c93afdf1186ff | add model card · marcop/musika_ae at 4572cc3 | 2026-09-04 |
| https://note.com/yamkaz/n/n395a9bc3f161 | 日刊 画像生成AI (2022年10月22日) | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:musika`, thread `musika`, 2 dated events 2022-08-19 → 2022-10-21.
- **Practical note:** As of 2022-10-21, use the linked GitHub repository and Hugging Face Space as dated public entry points for MUSIKA. Treat claimed release details as unverified until original posts or linked resources are researched.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.