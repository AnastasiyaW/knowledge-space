---
title: Echo LongVideo
category: projects
date: 2026-06-05
tags: [echo-longvideo, echo-longvideo-public-release, echo_longvideo, project]
aliases: ["Echo LongVideo"]
---

# Echo LongVideo

**Development line:** `project:echo-longvideo` · thread `echo-longvideo-public-release`  
**Last event:** 2026-06-05 · 1 dated since 2026-06-05 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Echo LongVideo is the long-video sub-project of JoyAI-Echo 1.5 for multi-shot audio and video with identity, voice, and scene transfer across editable shots.
- R2V with text, optional first frame, and up to 7 ordered audio-visual memory slots.
- Joint audio and video generation, BF16/FP8/FP4 inference, and a local Director Agent.
FP4 weights take 22,81 GB; the 24 GiB profile requires precomputed conditioning.
This is a local inference stack for testing, not an established production service.

## Development line

- **2026-06-05 — Echo LongVideo public project resources were linked.** On 2026-06-05, Echo LongVideo was referenced through a public project page, a GitHub repository, and a Hugging Face model page. This dated resource set identifies the public documentation, source, and model-distribution locations; the evidence does not establish the specific release contents.

## What changed

2026-06-05 — Hugging Face received a README update; the project page described a technical report claiming 5-minute coherent stories, A/V memory, and 7,5× acceleration, while code and weights were framed as future open-source. 2026-06-22 — root README dates the release of JoyAI-Echo 1.0 and keeps it in branch `echo1.0`; the original pipeline was T2V/multi-shot without I2V. 2026-08-24 — arXiv v1 introduced JoyAI-Echo 1.5; the long-video variant added composable cross-shot A/V memory to combine text, visual, and memory conditions. 2026-08-27 — Git commit published the long-video release of JoyAI-Echo 1.5. 2026-08-28 — documentation announced JoyAI-Echo 1.5 / Echo-LongVideo: code, weights, R2V inference, consumer-GPU profiles, and Director Agent. 2026-08-31 — documentation updated the claimed long-video duration to 10+ minutes; this is a claim update, not separate proof of a new checkpoint or benchmark.

## How to use this

As of 2026-06-05, practitioners should consult Echo LongVideo's linked project page, source repository, and Hugging Face page when assessing or attempting to use the project, rather than relying on an unverified secondary description.

1. Check the [LTX-2 Community License](https://github.com/jd-opensource/JoyAI-Echo/blob/main/LICENSE) before downloading or deploying: organizations with annual revenue from US$10 million require a separate commercial license; keep license restrictions when redistributing.
2. Clone the repository and work only inside `echo_longvideo`; the reference environment is Python 3.11, PyTorch 2.8, CUDA 12.8, `ffmpeg` in PATH, and `scripts/setup_msst.py` as detailed in the [README](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md).
3. Download exactly one 1.5 checkpoint — BF16, FP8, or FP4 — along with `gemma-3-12b`; match it to the same inference configuration and verify the manifest and SHA256SUMS on [Hugging Face](https://huggingface.co/jdopensource/JoyAI-Echo).
4. Build the R2V request with a text prompt, an optional first frame, and up to seven ordered image/audio memory slots; run `inference.py` with the matching YAML config from the [guide](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md).
5. For a target 24 GiB GPU, use the consumer FP4 profile and precompute conditioning; actual headroom depends on the GPU, driver, and request shape as documented in the [guide](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md).

## Best practices

- Do not mix environments, checkpoint directories, or entrypoints of Echo LongVideo with Echo-WM: upstream treats them as separate projects on [GitHub](https://github.com/jd-opensource/JoyAI-Echo).
- Check `checkpoint.json` in the weights directory and the root `SHA256SUMS` before the first inference run on [Hugging Face](https://huggingface.co/jdopensource/JoyAI-Echo).
- Pin the full commit SHA for reproducible installs: GitHub provides no published release artifact under [releases](https://github.com/jd-opensource/JoyAI-Echo/releases).
- Start with the supplied `examples/the_last_visa/requests/` set that the standard configuration handles before substituting your own R2V requests, per the [README](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md).

## Superseded by this

- 2026-08-28 — the state "code and weights will be released later" is obsolete: 1.5 documentation announces code, weights, and R2V inference as released.
- 2026-08-28 — for fresh installs, the 1.0 instruction "only T2V, I2V not supported" is obsolete: 1.5 uses R2V with an optional first frame, and 1.0 remains in the archive branch `echo1.0`.

## Still unknown

- The formal release date for 1.0 is ambiguous: Hugging Face history shows an initial commit, license, and uploads on 2026-06-02, a README update on 2026-06-05, while the root README lists the release on 2026-06-22.
- There is no versioned GitHub Release; the 1.5 release commit is dated 2026-08-27, and the README announcement is 2026-08-28.
- No primary evidence shows a successful local E2E run, universal minimum VRAM/RAM, actual speed, or output quality; 24 GiB is a target consumer profile, not a guarantee.
- License terms require manual review: the README states academic/research/non-commercial use, while the bundled LTX-2 Community License allows restricted use and requires a paid license for Commercial Entities with revenue from US$10 million.
- The repository also contains Echo-WM, but upstream isolates it as a separate project with a different environment and checkpoint tree; Echo-WM events are excluded from this line.

## Sources

| source | title | read |
|---|---|---|
| https://echo-team-joy-future-academy-jd.github.io/Echo-LongVideo-Page/ | JoyAI-Echo: Pushing the Frontier of Long Audio-Visual Generation | 2026-09-05 |
| https://huggingface.co/jdopensource/JoyAI-Echo/commits/main | Commits · jdopensource/JoyAI-Echo | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo | JoyAI-Echo repository and dated news | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md | JoyAI-Echo/echo_longvideo/README.md at main · jd-opensource/JoyAI-Echo | 2026-09-05 |
| https://huggingface.co/jdopensource/JoyAI-Echo | jdopensource/JoyAI-Echo · Hugging Face | 2026-09-05 |
| https://arxiv.org/abs/2608.23383 | Long-Horizon Audio-Visual Generation for Persistent Stories and Interactive Worlds | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/commits/main/ | Commits · jd-opensource/JoyAI-Echo · GitHub | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/tree/echo1.0 | GitHub - jd-opensource/JoyAI-Echo at echo1.0 | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/blob/main/LICENSE | LTX-2 Community License Agreement | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/releases | Releases · jd-opensource/JoyAI-Echo | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:echo-longvideo`, thread `echo-longvideo-public-release`, 1 dated events 2026-06-05 → 2026-06-05.
- **Practical note:** As of 2026-06-05, practitioners should consult Echo LongVideo's linked project page, source repository, and Hugging Face page when assessing or attempting to use the project, rather than relying on an unverified secondary description.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
