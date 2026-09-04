---
title: FLOAT — FLOAT public releases
category: projects
tags: [float, float-public-releases, model_releases, project]
aliases: ["FLOAT"]
---

# FLOAT — FLOAT public releases

**Development line:** `project:float` · thread `float-public-releases`  
**Events:** 2 dated, 2024-12-05 → 2025-07-21 · **Researched:** 2026-09-04 · confidence: medium

## What it is

FLOAT — a PyTorch research implementation that animates a single, mostly frontal portrait from speech audio. - Generates motion in a learned motion-latent space with flow matching. - Produces lip, head, and expressive motion from audio. - Supports emotion redirection and test-time head-motion editing. Limit: the published package is inference-only, research/non-commercial, and tested on Linux with A100 and V100 GPUs. Verdict: use it for reproducible research demos, not as a commercially deployable talking-head stack.

## Development line

- **2024-12-05 — FLOAT project page entered the public record.** On 2024-12-05, the FLOAT development line was linked to its official project page. This is a material public-facing milestone because it establishes a stable project destination in the historical record. The supplied evidence does not identify the page's specific technical claims or release contents.
- **2025-07-21 — FLOAT repository and supplementary resource links entered the public record.** On 2025-07-21, the FLOAT development line was linked to an official GitHub repository and a Google Drive resource. This is a material access milestone because it adds implementation and supplementary-resource destinations beyond the project page. The supplied evidence does not establish the precise contents, version, license, or intended use of the Drive resource.

## What changed

FLOAT — development moved from a published method to a runnable inference package, then to a revised ICCV paper record rather than a versioned product release. - 2024-12-05: FLOAT was presented as flow-matching audio-driven talking-portrait generation with an orthogonal motion latent space and speech-driven emotion. - 2025-02-17 (found today): the official repository says inference code and checkpoints were released under a non-commercial licence, making the method runnable. - 2025-06-26 (found today): the project reported ICCV 2025 acceptance. - 2025-07-21: the official repository and manual checkpoint route pointed to that runnable inference path; no new named model version is identified. - 2025-09-19 (found today): arXiv v5 revised the paper record; it does not state a new inference release. - 2025-11-10 (found today): the main-branch history shows an update commit, but its functional delta is undocumented and GitHub lists no releases. Limit: there is no tagged model-release train or published training code. Verdict: treat the repository and its checkpoints as a research code drop, not a maintained release channel.

## How to use this

As of 2025-07-21, practitioners should consult the official FLOAT repository and its linked supplementary resource in addition to the project page when assessing or reproducing FLOAT; verify the exact artifact contents and usage terms separately.

1. Clone the official repository, create its Conda environment with Python 3.8.5, then install the documented CUDA 11.8 PyTorch build and requirements.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
2. Download the checkpoints with `sh download_checkpoints.sh` and place the main FLOAT, Wav2Vec2, and speech-emotion checkpoint assets in the documented checkpoint layout.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
3. Prepare a mostly frontal single-face portrait and a speech track; begin with automatic face cropping enabled.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
4. Run `generate.py` with `--ref_path`, `--aud_path`, `--seed 15`, `--a_cfg_scale 2`, `--e_cfg_scale 1`, and `--ckpt_path ./checkpoints/float.pth` on a CUDA device.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
5. For an explicit expression, add `--emo` with one of angry, disgust, fear, happy, neutral, sad, or surprise; adjust `--e_cfg_scale` only after a default run.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>

## Best practices

- Use a frontal portrait first. The model was trained on frontal head-pose distributions, and non-frontal inputs can reduce quality.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Keep automatic cropping on unless a measured comparison justifies `--no_crop`; disabling it can reduce performance, while the default crop can add black padding.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Extract vocals before inference when the audio has heavy background music; the authors point to ClearVoice for this preparation.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Start emotion guidance at the documented default of 1; the authors suggest 5–10 only when a stronger expression is required.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>
- Keep work research-only and do not plan on fine-tuning from the official release: its licence is non-commercial and the authors state that training code will not be released.
  — <https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md>

## Superseded by this

- Before 2025-02-17: guidance that FLOAT was only a paper or project-page method and required waiting for official inference code and weights. Superseded by the official inference-code and checkpoint release.
- 2024-12-05: a method-only description is no longer sufficient setup guidance. Superseded by the official README's environment, checkpoint, preprocessing, and CLI instructions; the 2025-07-21 checkpoint link is a route to that runnable package, not evidence of a newly versioned model.

## Still unknown

- The supplied Google Drive checkpoint URL could not be independently read today, so its file contents, checksum, and whether it changed after 2025-07-21 are unverified.
- No first-party Simplified-Chinese FLOAT documentation was found in a targeted search today; Chinese results found were third-party and were not used as evidence.
- The latest visible 2025-11-10 commit is only labelled “update”; no first-party changelog explains its functional effect.
- The official material does not state supported input duration, output resolution, VRAM use, or compatibility beyond its tested Linux A100/V100 setup.

## Sources

| source | title | read |
|---|---|---|
| https://deepbrainai-research.github.io/float/ | FLOAT project page | 2026-09-04 |
| https://github.com/deepbrainai-research/float | FLOAT official GitHub repository | 2026-09-04 |
| https://raw.githubusercontent.com/deepbrainai-research/float/main/README.md | FLOAT README on the main branch | 2026-09-04 |
| https://arxiv.org/abs/2412.01064 | FLOAT: Generative Motion Latent Flow Matching for Audio-driven Talking Portrait | 2026-09-04 |
| https://github.com/deepbrainai-research/float/commits/main/ | FLOAT main-branch commit history | 2026-09-04 |
| https://github.com/deepbrainai-research/float/releases | FLOAT GitHub releases | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:float`, thread `float-public-releases`, 2 dated events 2024-12-05 → 2025-07-21.
- **Practical note:** As of 2025-07-21, practitioners should consult the official FLOAT repository and its linked supplementary resource in addition to the project page when assessing or reproducing FLOAT; verify the exact artifact contents and usage terms separately.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
