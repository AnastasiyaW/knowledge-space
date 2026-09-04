---
title: AvatarArtist — AvatarArtist public release and hosted Space
category: projects
tags: [avatarartist, avatarartist-public-release-and-space, project]
aliases: ["AvatarArtist"]
---

# AvatarArtist — AvatarArtist public release and hosted Space

**Development line:** `project:avatarartist` · thread `avatarartist-public-release-and-space`  
**Events:** 2 dated, 2025-03-27 → 2025-04-09 · **Researched:** 2026-09-04 · confidence: medium

## What it is

AvatarArtist — an open-domain portrait-to-4D-avatar pipeline for creators and researchers who need motion-driven output. - turns one portrait into a parametric 4D representation - renders target frames from the reference image and driving signals - includes released inference and input-processing paths Limit: local use requires Python 3.9, model weights, the separate FaceVerse asset, and processed image/motion inputs; training code remains pending. Verdict: use the local inference path for repeatable experiments; treat the hosted Space as a convenience demo.

## Development line

- **2025-03-27 — AvatarArtist received a public project and source presence.** On 2025-03-27, AvatarArtist was linked to a public project page and a GitHub source repository. This marks a material public-development step because readers could access both project information and its source reference from that date.
- **2025-04-09 — AvatarArtist was linked to a Hugging Face Space.** On 2025-04-09, AvatarArtist was linked to a Hugging Face Space. This is a material follow-on step because it added a hosted public endpoint alongside the earlier project-page and repository references.

## What changed

AvatarArtist — the project moved from a local inference release to local and online demos, while a trainable release is still not documented. - 2025-03-26 (found today): the official repository says inference code and pretrained models were released. - 2025-03-27: the public project page and official repository were recorded, establishing the local code-and-weights workflow. - 2025-03-30 (found today): the official repository lists a Gradio demo release. - 2025-04-02 (found today): the official repository lists an online-demo release. - 2025-04-09: the Hugging Face Space was recorded; no first-party release note reviewed proves a model revision on that date. - 2026-09-04 (found today): the former ant-research GitHub URL redirects to robbyant-research; the repository still lists training code as pending. Limit: no newer version, hardware matrix, or completed training release was found in the first-party sources reviewed. Verdict: AvatarArtist remains an inference-and-demo project, not a documented trainable platform.

## How to use this

As of 2025-04-09, practitioners should consult the AvatarArtist project page and source repository, then use the linked Hugging Face Space as the hosted public access point when evaluating the project.

1. Start with a portrait reference and a driving-motion source; AvatarArtist creates a 4D representation from the portrait and renders frames under the driving signals.
  — <https://kumapowerliu.github.io/AvatarArtist/>
2. Clone the current repository, create the documented Conda environment with Python 3.9, and install requirements.
  — <https://github.com/robbyant-research/AvatarArtist>
3. Download the KumaPower/AvatarArtist weights into `pretrained_model`; obtain `faceverse_v3_1.npy` separately and copy it to both documented FaceVerse paths.
  — <https://github.com/robbyant-research/AvatarArtist>
4. Run `python3 app.py` with the included demo data first; for controlled output, run `inference.py` with image, FaceVerse coefficients, motion inputs, output path, and optional `--select_img`.
  — <https://github.com/robbyant-research/AvatarArtist>
5. For custom media, use the official preprocessing path so the final `dataset` contains the required image, coefficient, motion, and render folders before inference.
  — <https://github.com/robbyant-research/AvatarArtist>
6. Use the browser Space only for a quick manual trial; its accessible page snapshot was marked Sleeping rather than a verified always-on endpoint.
  — <https://huggingface.co/spaces/KumaPower/AvatarArtist>

## Best practices

- Begin with the supplied demo data and the documented preprocessing layout; only the final `dataset` directory is model input, while the other folders are intermediates.
  — <https://github.com/robbyant-research/AvatarArtist>
- Treat `faceverse_v3_1.npy` as required setup, not an optional extra: weights alone do not make the project runnable.
  — <https://github.com/robbyant-research/AvatarArtist>
- Keep work within released inference and data processing; the official to-do still lists training-code release as pending.
  — <https://github.com/robbyant-research/AvatarArtist>
- Use the redirected robbyant-research repository for new setup links; retain the ant-research URL only for historical references.
  — <https://github.com/ant-research/AvatarArtist>
- Do not treat the model card as hosted inference: it lists no Hugging Face Inference Provider deployment.
  — <https://huggingface.co/KumaPower/AvatarArtist>
- Treat the Space as optional exploration rather than a production dependency because the accessible snapshot showed it Sleeping.
  — <https://huggingface.co/spaces/KumaPower/AvatarArtist>

## Superseded by this

- 2025-03-27: using `https://github.com/ant-research/AvatarArtist` as the canonical owner URL is superseded by its observed redirect to `https://github.com/robbyant-research/AvatarArtist` on 2026-09-04.

## Still unknown

- The dated 2025-04-09 event text is unavailable, so its relation to the already-announced online demo cannot be narrowed beyond the linked Space.
- The Space was not run end to end during this review; its current health, cold-start behavior, and latency remain unverified.
- The first-party sources reviewed do not state a supported GPU, VRAM, CUDA, or operating-system matrix.
- No independent experienced-user practice source was found; the practices above are official operational requirements and current distribution observations.

## Sources

| source | title | read |
|---|---|---|
| https://kumapowerliu.github.io/AvatarArtist/ | AvatarArtist: Open-Domain 4D Avatarization | 2026-09-04 |
| https://github.com/ant-research/AvatarArtist | AvatarArtist official PyTorch implementation; redirects to robbyant-research | 2026-09-04 |
| https://github.com/robbyant-research/AvatarArtist | AvatarArtist official PyTorch implementation | 2026-09-04 |
| https://huggingface.co/KumaPower/AvatarArtist | KumaPower/AvatarArtist model card | 2026-09-04 |
| https://huggingface.co/spaces/KumaPower/AvatarArtist | KumaPower/AvatarArtist Hugging Face Space | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:avatarartist`, thread `avatarartist-public-release-and-space`, 2 dated events 2025-03-27 → 2025-04-09.
- **Practical note:** As of 2025-04-09, practitioners should consult the AvatarArtist project page and source repository, then use the linked Hugging Face Space as the hosted public access point when evaluating the project.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
