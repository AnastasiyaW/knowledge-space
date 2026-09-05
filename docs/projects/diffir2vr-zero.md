---
title: DiffIR2VR-Zero
category: projects
date: 2024-07-14
tags: [diffir2vr-zero, diffir2vr-zero-development, diffir2vr_zero, project]
aliases: ["DiffIR2VR-Zero"]
---

# DiffIR2VR-Zero

**Development line:** `project:diffir2vr-zero` · thread `diffir2vr-zero-development`  
**Last event:** 2024-07-14 · 2 dated since 2024-07-01 · **Researched:** 2026-09-05 · confidence: medium

## What it is

DiffIR2VR-Zero — research code that adapts pretrained image-restoration diffusion models to temporally consistent video restoration. — Blind denoising (`dn`) and super-resolution (`sr`). — Claimed up to 8× super-resolution without task-specific retraining. — Hierarchical latent warping plus flow- and similarity-based token merging. Limit: the launcher defaults to CUDA, has no tagged GitHub release, and the hosted demo reports a build error. use the repository for controlled experiments, not the demo as a production endpoint.

## Development line

- **2024-07-01 — DiffIR2VR-Zero project page and interactive demo entered the public record.** On 2024-07-01, the DiffIR2VR-Zero development line was linked to a project website and a Hugging Face Space. This is a material public project-and-demo presence in the historical record. The sealed evidence does not establish the model version, capabilities, or release status behind those links.
- **2024-07-14 — DiffIR2VR-Zero GitHub repository was linked in the development line.** On 2024-07-14, the DiffIR2VR-Zero development line linked an earlier item alongside the project's GitHub repository. This is treated as a material source-access milestone for the public history. The sealed links alone do not show whether this was a new code release or a reference to code already available earlier.

## What changed

DiffIR2VR-Zero — the method and source arrived in July 2024; later evidence shows paper revisions, a checkpoint-link repair, and an unavailable hosted demo rather than a new product generation. — 2024-07-01: arXiv v1 and the repository’s first commit established the training-free video-restoration method, project page, and local code path. — 2024-07-14: the GitHub route made source checkout explicit. Repository history, checked today, places the initial commit on 2024-07-01, so this is not evidenced as a second algorithmic release. — 2025-12-31 (found today): arXiv v5 was posted. Its metadata does not describe a corresponding runnable-code change. — 2026-01-22 (found today): commit `2cf4737` replaced the unavailable official SD 2.1 checkpoint URL with a mirror; the inference method was unchanged. — 2026-09-04 (found today): the public Hugging Face Space reports a build error, leaving the local repository as the practical entry point. Limit: no fresh end-to-end installation was run in this review. treat it as lightly maintained research code with a working source path but a fragile dependency chain.

## How to use this

From 2024-07-01, practitioners could inspect DiffIR2VR-Zero through its public project and demo links; from 2024-07-14, they could also consult the linked GitHub repository for implementation access, while independently verifying the exact revision and usage terms.

1. Clone the repository, create a Python 3.10 Conda environment, and install `requirements.txt`.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
2. Create `weights/` and manually add `gmflow_sintel-0c07dcb3.pth`; the documented inference path retrieves the remaining DiffBIR v2 and SD 2.1 weights on demand.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
3. Start with the documented denoising baseline: `--version v2 --task dn --upscale 1 --cfg_scale 4.0 --batch_size 10`, with the supplied config, input and output paths, `final_size` and merge ratio.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
4. For super-resolution, switch to `--task sr` and begin with the documented 4× command before attempting the project’s claimed 8× range.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
5. Set an explicit `--seed` for comparable runs and confirm that CUDA is actually available; the launcher otherwise falls back to CPU.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero/blob/main/inference.py>

## Best practices

- Use the local repository rather than the hosted Space until its build failure is resolved.
  — <https://huggingface.co/spaces/Koi953215/DiffIR2VR>
- Pin and independently verify downloaded checkpoints: the maintainer replaced the official SD 2.1 download with a mirror after the official URL became unavailable.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero/commit/2cf4737bfc8319abd8ca399d70cc49a3aaf097a6>
- Begin at the documented 480×854, CFG 4.0, batch size 10 and merge-ratio baseline; change one parameter group at a time while checking detail against temporal stability.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
- Treat the up-to-8× and no-retraining claims as research results, then inspect restored clips for temporal coherence and invented detail on the target footage.
  — <https://jimmycv07.github.io/DiffIR2VR_web/>

## Superseded by this

- 2024-07-01–2024-07-14: use the Hugging Face demo as the operating entry point — obsolete as practical guidance; the accessible Space now reports a build error.
- Before 2026-01-22: rely on automatic download from the official Stable Diffusion 2.1 checkpoint URL — obsolete; the maintainer changed the source because that official URL was unavailable.
- 2024-07-14: interpret the GitHub link as a second code release — unsupported by the repository history, which records the first commit on 2024-07-01.

## Still unknown

- No current CUDA/PyTorch installation or full inference run was independently verified; the repository instructions are source evidence, not a runtime receipt.
- The accessible Hugging Face Space reports a build error, but its page snapshot was crawled two weeks before this review; its exact live runtime was not browser-executed.
- The Space source links `arXiv:2406.06523`, which is the distinct NaRCan video-editing paper. This may be stale metadata or a historical mix-up. The project page, repository and `arXiv:2407.01519` consistently identify DiffIR2VR-Zero, so two distinct DiffIR2VR-Zero subjects are not evidenced.
- No Chinese first-party documentation was found in a separate Simplified-Chinese search lane, so no Chinese-specific operating guidance was added.
- arXiv’s v2–v5 metadata does not explain their substantive changes; those revision dates should not be read as implementation releases.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2407.01519 | DiffIR2VR-Zero: Zero-Shot Video Restoration with Diffusion-based Image Restoration Models | 2026-09-04 |
| https://jimmycv07.github.io/DiffIR2VR_web/ | DiffIR2VR-Zero project page | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero | GitHub — jimmycv07/DiffIR2VR-Zero | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero/commits/main | Commit history — jimmycv07/DiffIR2VR-Zero | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero/blob/main/inference.py | DiffIR2VR-Zero inference.py | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero/commit/2cf4737bfc8319abd8ca399d70cc49a3aaf097a6 | Change sd_v21 model checkpoint URL | 2026-09-04 |
| https://huggingface.co/spaces/Koi953215/DiffIR2VR | DiffIR2VR — Hugging Face Space | 2026-09-04 |
| https://arxiv.org/abs/2406.06523 | NaRCan: Natural Refined Canonical Image with Integration of Diffusion Prior for Video Editing | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:diffir2vr-zero`, thread `diffir2vr-zero-development`, 2 dated events 2024-07-01 → 2024-07-14.
- **Practical note:** From 2024-07-01, practitioners could inspect DiffIR2VR-Zero through its public project and demo links; from 2024-07-14, they could also consult the linked GitHub repository for implementation access, while independently verifying the exact revision and usage terms.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
