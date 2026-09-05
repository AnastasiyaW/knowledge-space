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

- NCA and Local Pattern Producing Network (LPPN) train jointly.
- Core modes cover 2D morphogenesis, PBR textures, textures on meshes, and 3D textures.
- Experimental modes cover dynamic textures, radiance field, and voxel growth.

The repository is built for training, without a packaged release or ready Colab. The README still lists Colab and testing as TODO items. It fits reproducible NCA experiments, not production image generation.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

2026-07-11 — Cells2Pixels arrived as a SIGGRAPH 2026 implementation. A coarse cellular grid evolves through local updates. The LPPN decodes interpolated cell states and local coordinates into images or surface properties at arbitrary resolution.

## How to use this

As of 2026-07-11, treat Cells2Pixels as a project requiring source review through its website and repository; no practitioner workflow change is justified from the dated links alone.

1. Install dependencies with `pip install -r requirements.txt`. Kaolin is optional for runs without meshes.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
2. Download datasets and input directory structures with `python scripts/download_data.py`.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
3. Run training with `python train.py --config <path>`. Start with `configs/nca2d/growing.yaml` for 2D growth, `configs/nca2d/pbr_texture.yaml` for PBR, `configs/meshnca/texture.yaml` for meshes, or `configs/nca3d/3d_texture.yaml` for 3D.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
4. Pass `--test` after training to load the checkpoint and save images and rollout videos into the configured outputs directory.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
5. Test model behavior in the interactive canvas by choosing a mode, adjusting the LPPN scale, and clicking or touching the NCA.
  — <https://cells2pixels.github.io/>

## Best practices

- Match PyTorch and Kaolin versions with requirements. Kaolin is needed only for mesh rendering and rasterization.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
- Do not present dynamic texture, radiance-field growth, or voxel growth as paper results. The README separates these experimental modes from the four paper training modes.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>
- Evaluate models with a saved checkpoint and an explicit test rollout instead of relying on the training run alone.
  — <https://github.com/TheDevilWillBeBee/Cells2Pixels>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The project page and README provide no dated repository changelog, so publication dates for code, demos, and specific configs cannot be verified.
- No confirmed packaged release, checkpoint catalogue, or supported production workflow exists.

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
