---
title: "GAE (Geometry-Native Autoencoder)"
category: "projects"
date: 2026-09-23
tags: ["gae-geometric-autoencoder", "project"]
aliases: ["GAE geometric autoencoder: gae-geometric-autoencoder"]
---

# GAE (Geometry-Native Autoencoder)

**Development line:** project:gae-geometric-autoencoder · thread gae-geometric-autoencoder  
**Last event:** 2026-09-23 · 2 dated since 2026-09-21 · **Researched:** 2026-11-25 · confidence: high

## What it is

GAE (Geometry-Native Autoencoder) is a 3D world generation model from HKUST and Tencent ARC Lab.

- Latent flow matching: runs directly on a compact per-view latent distilled from Depth Anything 3 multi-level features.
- Joint decoding: turns every generated latent into RGB, depth, camera poses, and point-cloud 3D geometry without post-hoc reconstruction.

## Development line

- **2026-09-21 — GAE paper published.** The paper 'GAE: Learning a Geometry-Native Latent Space for 3D-Consistent World Generation' (arXiv 2609.24981) was published.
- **2026-09-23 — GAE release.** Tencent ARC and HKUST release the model. It compresses 3072-channel geometric features into 128 channels and decodes RGB, depth, camera trajectories, and point clouds. The 1B-parameter architecture conditions on text, reference frames, and metric rays. Its latent space connects perception and generation with four linked outputs: image, depth, camera pose, and 3D geometry.
  - Compression reduces 3,072-dimensional geometry features to a structured 128-dimensional state, about 24x fewer. Every latent decodes into appearance and 3D. The project page lists a 1B-parameter model and four linked outputs from one latent: RGB, depth, camera poses, and 3D point-cloud geometry. (undated, page states 2026) — <https://jiah-cloud.github.io/GAE.github.io/>
  - Flow matching runs on text, clean reference tokens, and metric camera rays. From one observed frame and a metric camera path, GAE generates an 81-view 672 x 378 RGB sequence plus geometry. The page shows indoor scenes (RealEstate10K, ScanNet++) and outdoor scenes. It reports the lowest normalized Chamfer distance on a 64-scene benchmark, ranking first on 40 of 64 scenes. (undated, page states 2026) — <https://jiah-cloud.github.io/GAE.github.io/>
  - The GitHub repository provides the code. Stage 1 builds a codec over frozen Depth Anything 3 (DA3) features, producing a 64- or 128-dimensional latent on the DA3 patch grid. The frozen DPT head extracts depth, rays, and pointmaps, while a learned head predicts RGB. Stage 2 trains one conditional flow model with x-prediction over the standardized latent. The repository had 552 stars and 21 forks when observed. (undated) — <https://github.com/TencentARC/GAE-GeometricAutoEncoder>
  - The Hugging Face model card for GAE-D64-1B describes weights for GAE-64. It is a ~1B-parameter temporal DiT over a 64-dimensional geometry-native latent at 672×378 and 81 views, using metric Plücker camera conditioning and Qwen3-0.6B text. The repository bundles the codec, latent statistics, DA3 feature stats, and the flow transformer, linking the paper (arXiv 2609.24981). (undated) — <https://huggingface.co/TencentARC/GAE-D64-1B>

## What changed

The paper, project page, public code, and a roughly 1B-parameter GAE-64 checkpoint are out. The 64-channel checkpoint generates an 81-view, 672x378 sequence from one reference image with text and metric camera conditioning.

## How to use this

1. Get the code from the GitHub repository and put the GAE-D64-1B files (codec, flow checkpoint) in ckpts/. Then run scripts/run_demo.sh, or run: python scripts/generate.py --image examples/scenes/forest_lake_trail.jpg --prompt-file examples/scenes/forest_lake_trail.txt --flow-ckpt ckpts/flow_gae64.pt --codec-ckpt ckpts/gae_64.pt --output results/forest
  — <https://huggingface.co/TencentARC/GAE-D64-1B>
2. Use gae/ for inference and scripts/demo/, scripts/train/, scripts/eval/ and scripts/data/ for the command-line tools. Recipes are in configs/.
  — <https://github.com/TencentARC/GAE-GeometricAutoEncoder>

## Best practices

- For image-to-video, use the documented settings of 50 Euler steps and classifier-free guidance 2 with one reference view.
  — <https://huggingface.co/TencentARC/GAE-D64-1B>
- Download the frozen DA3-GIANT encoder and DPT head separately from depth-anything/DA3-GIANT-1.1; the model repository does not bundle them.
  — <https://huggingface.co/TencentARC/GAE-D64-1B>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Only GAE-64 (GAE-D64-1B) has weights available. The documentation does not state whether GAE-128 weights are public.
- The license terms do not appear on the project pages.
- The 1B parameter count is given for the full system, and '~1B' for the GAE-64 DiT. The parameter split between the codec and the flow model is not listed.

## Sources

| source | title | read |
|---|---|---|
| https://jiah-cloud.github.io/GAE.github.io/ | GAE · Geometry-Native World Generation (project page) | 2026-09-23 |
| https://github.com/TencentARC/GAE-GeometricAutoEncoder | GitHub - TencentARC/GAE-GeometricAutoEncoder | 2026-09-23 |
| https://huggingface.co/TencentARC/GAE-D64-1B | TencentARC/GAE-D64-1B · Hugging Face | 2026-09-23 |

## Agent brief {#agent-brief}

- **Subject:** project:gae-geometric-autoencoder, thread gae-geometric-autoencoder, 2 dated events 2026-09-21 → 2026-09-23.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
