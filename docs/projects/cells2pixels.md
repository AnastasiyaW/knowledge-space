---
title: Cells2Pixels
category: projects

tags: [cells2pixels, cells2pixels-development, project]
aliases: ["Cells2Pixels"]
---

# Cells2Pixels

**Development line:** `project:cells2pixels` · thread `cells2pixels-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: high

## What it is

Cells2Pixels is the code and interactive demo of Neural Cellular Automata: From Cells to Pixels for generative graphics researchers.

- Jointly trained NCA and Local Pattern Producing Network (LPPN).
- 2D morphogenesis, PBR textures, mesh textures, and 3D textures.
- Experimental dynamic textures, radiance fields, and voxel growth.

The repository is for training, with no packaged release and no ready Colab; the README still marks Colab and testing as TODO. Suitable for reproducible NCA experiments, not as a ready image generator.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-11 — Cells2Pixels is presented as the SIGGRAPH 2026 implementation. A coarse cell grid evolves through local updates. The LPPN decodes interpolated cell states and local coordinates into images or surface properties at arbitrary resolution.

## How to use this

As of 2026-07-11, treat Cells2Pixels as a project requiring source review through its website and repository; no practitioner workflow change is justified from the dated links alone.

1. Install dependencies with `pip install -r requirements.txt`; Kaolin is optional for experiments without meshes.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
2. Download datasets and input directory structure: `python scripts/download_data.py`.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
3. Run training via `python train.py --config <path>`; start with `configs/nca2d/growing.yaml` for 2D growth, `configs/nca2d/pbr_texture.yaml` for PBR, `configs/meshnca/texture.yaml` for meshes, and `configs/nca3d/3d_texture.yaml` for 3D.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
4. Add `--test` after training to load the checkpoint and save an image and rollout video to the configured outputs directory.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
5. Use the interactive canvas to inspect model behavior quickly: select a mode, adjust LPPN scale, and perturb the NCA by clicking or tapping.
  — <https://cells2pixels.github.io/>

## Best practices

- Keep PyTorch and Kaolin versions aligned with requirements; Kaolin is needed only for mesh rendering and rasterization.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
- Do not treat experimental dynamic texture, radiance-field growth, or voxel growth modes as paper results: the README separates them from the four paper training modes.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
- Evaluate the model using a saved checkpoint and an explicit test rollout, not just the training run.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The project page and README lack a dated repository changelog, so we cannot date the release of the code, demo, or individual configs reliably.
- No confirmed packaged release, ready checkpoint catalog, or supported production workflow was found.

## Sources

| source | title | read |
|---|---|---|
| https://cells2pixels.github.io/ | Neural Cellular Automata: From Cells to Pixels | 2026-09-05 |
| https://github.com/TheDevilWillBeBee/Cells2Pixels | TheDevilWillBeBee/Cells2Pixels — official implementation | 2026-09-05 |
| https://arxiv.org/abs/2506.22899 | Neural Cellular Automata: From Cells to Pixels | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:cells2pixels`, thread `cells2pixels-development`, 0 dated events - → -.
- **Practical note:** As of 2026-07-11, treat Cells2Pixels as a project requiring source review through its website and repository; no practitioner workflow change is justified from the dated links alone.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
