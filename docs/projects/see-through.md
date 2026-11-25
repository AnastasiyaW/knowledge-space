---
title: See-through
category: projects
date: 2026-04-01
tags: [project, see-through, see-through-release, see_through_release]
aliases: ["See-through"]
---

# See-through

**Development line:** `project:see-through` · thread `see-through-release`  
**Last event:** 2026-04-01 · 1 dated since 2026-04-01 · **Researched:** 2026-11-21 · confidence: high

## What it is

See-through is an Apache-2.0 research project that splits one anime character illustration into up to 23 layers and exports a layered PSD.

- What: single-image layer decomposition for anime characters, with inferred drawing order, for 2.5D animation preparation.
- Users: illustrators and animators preparing layered character art, and researchers building on the method.
- Key capability: fully inpainted, semantically distinct layers, exported to PSD. The changelog describes a V3 model trained with 23 body-part tags.
- Limits: 12 to 16 GB VRAM at 1280 resolution by default; about 10 GB with group offload, which runs about 1.5x slower. Rigging is not covered, and the authors say it is "not Image-to-Live2D" yet.

As of 2026-11, the repository has no GitHub Releases or tags. Its most recent dated changelog entry is 2026-04-14, and commits continued into November 2026.

## Development line

- **2026-04-01 — See-through repository and demo links were shared.** On 2026-04-01, a project item linked the See-through GitHub repository and a Hugging Face Space demo. This provides public access by making both the project source location and an interactive demo discoverable.

## What changed

- 2026-03-31 — repository created (GitHub API metadata).
- 2026-04-14 — changelog: training scripts and configs released for the V3 model with 23 body-part tag training.
- 2026-11-05 to 2026-11-14 — commits changed inference for empty head crops (2026-11-05) and stop inference when head layers are unavailable (2026-11-13). No release tag marks these changes.

## How to use this

1. Create a Python 3.12 conda environment and install PyTorch 2.8.0 with CUDA 12.8 wheels, as the README pins.
  — <https://github.com/shitagaki-lab/see-through>
2. Run commands from the repository root. The UI requires a `workspace/datasets/` folder.
  — <https://github.com/shitagaki-lab/see-through>
3. Run `inference_psd.py --srcp <image> --save_to_psd` to produce a layered PSD. Default VRAM is about 12 to 16 GB at 1280 resolution.
  — <https://github.com/shitagaki-lab/see-through>
4. For less VRAM, use group offload (about 10 GB, about 1.5x slower) or the NF4 path (about 8 GB peak). The README reports NF4 quality at PSNR ~30 dB and SSIM ~0.96 against full precision.
  — <https://github.com/shitagaki-lab/see-through>
5. Try the Hugging Face Space before a local install. The Space page read on 2026-11-21 shows owner metadata only.
  — <https://huggingface.co/spaces/24yearsold/see-through-demo>

## Best practices

- Do not plan for Live2D rigging. The authors say the project does not yet cover it.
  — <https://github.com/shitagaki-lab/see-through>
- Budget for longer runs. Head and body are processed in two stages, which the README says can take longer than the original model.
  — <https://github.com/shitagaki-lab/see-through>
- Record the commit you used for each output. Inference handling changed in November 2026 without a release tag.
  — <https://github.com/shitagaki-lab/see-through/commits/main>

## Superseded by this

- Nothing marked obsolete by this page. The README's V3 (23 body-part tags) training release is the model described in the current README.

## Still unknown

- The demo Space's model and behavior: the page read showed only title, owner and runtime metadata.
- The paper was not read in this research (arXiv 2602.03749 and the DOI are listed by the README).
- Licensing of model weights is not confirmed; the Apache-2.0 license is shown for the code.
- The ModelScope mirror mentioned in the README was not checked.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/shitagaki-lab/see-through | shitagaki-lab/see-through — README and license | 2026-11-21 |
| https://github.com/shitagaki-lab/see-through/commits/main | shitagaki-lab/see-through — commit history | 2026-11-21 |
| https://huggingface.co/spaces/24yearsold/see-through-demo | See-through: Layer Decomposition — Hugging Face Space (metadata only) | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:see-through`, thread `see-through-release`, 1 dated events 2026-04-01 → 2026-04-01.
- **Practical note:** Apache-2.0 SIGGRAPH 2026 layer decomposition tool, up to 23 layers to layered PSD; 12–16 GB VRAM default. No Live2D rigging; pin the commit used because inference changed in November 2026.
- **Confidence:** high for repository facts; the paper and demo model were not verified. Dated supersedes above are the authority for what is obsolete.
