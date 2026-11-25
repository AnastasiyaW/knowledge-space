---
title: GaussianGPT
category: projects

tags: [gaussian-gpt-development, gaussiangpt, project]
aliases: ["GaussianGPT"]
---

# GaussianGPT

**Development line:** `project:gaussiangpt` · thread `gaussian-gpt-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-11-21 · confidence: high

## What it is

GaussianGPT is a transformer that generates 3D Gaussian Splatting scenes autoregressively, token by token, instead of with diffusion or flow matching.

- Research code (MIT license) from a Technical University of Munich research group, published as an arXiv preprint and as a repository.
- Users: researchers working on generative 3D scene representations.
- Key capability: one model covers unconditional scene generation, scene completion and outpainting, and multi-chunk scene synthesis.
- Limits: research-grade code with a fixed CUDA 12.9 / PyTorch 2.8 build stack; the original 3D-FRONT source is no longer available according to the repository README.

Each GPT checkpoint must be paired with its matching VQ-VAE checkpoint. The pipeline first compresses Gaussians into discrete tokens with a sparse 3D autoencoder and vector quantization, then models the tokens with a causal transformer.

## Development line

- (no material events recorded)

## What changed

- 2026-03-27 — arXiv:2603.26661 v1 submitted (arXiv listing).
- 2026-06-18 — Accepted to ECCV 2026 (repository news log).
- 2026-06-19 — Training and inference code released (repository news log).
- 2026-07-01 — Scene-level VQ-VAE and GPT checkpoints released (repository news log).
- 2026-07-02 — Camera-ready paper posted on arXiv (repository news log).
- 2026-07-12 — Object-level (PhotoShape) checkpoints released (repository news log).
- 2026-08-05 — Selected for an oral presentation (repository news log).

## How to use this

1. Read the paper for scope: unconditional generation, scene completion and outpainting over 3D Gaussian scenes. — <https://arxiv.org/abs/2603.26661>
2. Clone the repository and set up the CUDA 12.9 / PyTorch 2.8 environment. Set `TORCH_CUDA_ARCH_LIST` to your GPU architecture and use GCC 13 or older, because MinkowskiEngine fails with GCC 14 or newer. — <https://github.com/nicolasvonluetzow/GaussianGPT>
3. Download a matched pair of checkpoints (VQ-VAE and GPT) from the links in the README. Checkpoints are hosted by the research group; the README lists scene-level (VFront, VFront+ASE) and object-level (PhotoShape) models. — <https://github.com/nicolasvonluetzow/GaussianGPT>
4. Sample with `generate_chunks.py` by passing `checkpoint=` and `vqvae_checkpoint=`; use `complete_chunks.py` for completion and outpainting. — <https://github.com/nicolasvonluetzow/GaussianGPT>

## Best practices

- Pair each GPT checkpoint only with its listed VQ-VAE. — <https://github.com/nicolasvonluetzow/GaussianGPT>
- Install the pinned stack from the README (gsplat, pytorch3d, FlashAttention v2.8.2, the CUDA 12 MinkowskiEngine fork) instead of latest versions. — <https://github.com/nicolasvonluetzow/GaussianGPT>
- On machines with limited RAM, cap compile parallelism with `MAX_JOBS`, because each nvcc job needs several GB. — <https://github.com/nicolasvonluetzow/GaussianGPT>
- Prepare datasets as 3DGS PLY files and build splits with the provided scripts before training. — <https://github.com/nicolasvonluetzow/GaussianGPT>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Quality metrics and benchmark numbers were not checked against the paper's tables; this page makes no quality claim.
- Hardware memory requirements for training and inference are not stated in the README.
- Re-released 3D-FRONT data is suggested by the README as an alternative, but its licensing was not checked.
- Object-level checkpoint behaviour was not tested.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2603.26661 | GaussianGPT: Towards Autoregressive 3D Gaussian Scene Generation (arXiv) | 2026-11-21 |
| https://github.com/nicolasvonluetzow/GaussianGPT | GaussianGPT repository README and news log | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:gaussiangpt`, thread `gaussian-gpt-development`, 0 dated events in the development line; 7 dated release facts in "What changed" from 2026-03-27 to 2026-08-05.
- **Practical note:** As of 2026-11, treat GaussianGPT as a research code release with MIT license. Use matched VQ-VAE and GPT checkpoints, and follow the pinned build stack in the repository README.
- **Confidence:** high for release history and usage (arXiv listing and repository README read); quality claims are unverified. Dated supersedes above are the authority for what is obsolete.
