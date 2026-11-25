---
title: AvatarArtist
category: projects
date: 2025-04-09
tags: [avatarartist, avatarartist-public-release-and-space, project]
aliases: ["AvatarArtist"]
---

# AvatarArtist

**Development line:** `project:avatarartist` · thread `avatarartist-public-release-and-space`  
**Last event:** 2025-04-09 · 2 dated since 2025-03-27 · **Researched:** 2026-09-05 · confidence: medium

## What it is

AvatarArtist is an open-domain portrait-to-4D-avatar pipeline for creators and researchers who need motion-driven output.

- portrait conversion: turns one portrait into a parametric 4D representation
- frame rendering: renders target frames from the reference image and driving signals
- pipeline access: includes released inference and input-processing paths

## Development line

- **2025-03-27 — AvatarArtist launched its public project page and official repository.** This established the local code-and-weights workflow.
- **2025-04-09 — AvatarArtist linked to a Hugging Face Space.** No reviewed first-party release note proves a model revision on that date.

## What changed

AvatarArtist moved from a local inference release to local and online demos. A training release is still not documented.

- 2025-03-26: the official repository announced inference code and pretrained models.
- 2025-03-27: the public project page and official repository established the local code-and-weights workflow.
- 2025-03-30: the official repository listed a Gradio demo release.
- 2025-04-02: the official repository listed an online-demo release.
- 2025-04-09: the Hugging Face Space appeared; no reviewed first-party release note proves a model revision on that date.
- 2026-09-04: the former ant-research GitHub URL redirected to robbyant-research; the repository still lists training code as pending.

## How to use this

As of 2025-04-09, consult the AvatarArtist project page and repository, then test the linked Hugging Face Space for hosted evaluation.

1. Start with a portrait reference and a driving-motion source; AvatarArtist creates a 4D representation from the portrait and renders frames under the driving signals.
  — <https://kumapowerliu.github.io/AvatarArtist/>
2. Clone the repository, create the documented Conda environment with Python 3.9, and install requirements.
  — <https://github.com/robbyant-research/AvatarArtist>
3. Download the KumaPower/AvatarArtist weights into `pretrained_model`; obtain `faceverse_v3_1.npy` separately and copy it to both documented FaceVerse paths.
  — <https://github.com/robbyant-research/AvatarArtist>
4. Run `python3 app.py` with the demo data first; for controlled output, run `inference.py` with image, FaceVerse coefficients, motion inputs, output path, and optional `--select_img`.
  — <https://github.com/robbyant-research/AvatarArtist>
5. For custom media, use the official preprocessing path so the final `dataset` contains the required image, coefficient, motion, and render folders before inference.
  — <https://github.com/robbyant-research/AvatarArtist>
6. Use the browser Space only for a quick manual trial; its accessible page snapshot was marked Sleeping rather than an active endpoint.
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

- The dated 2025-04-09 event text is unavailable, so we cannot tie it to the online demo beyond the linked Space.
- We did not run the Space end to end during review, leaving current health, cold-start behavior, and latency unverified.
- First-party sources give no supported GPU, VRAM, CUDA, or operating-system matrix.
- We found no community experience reports; these practices come from official requirements and distribution state.

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
