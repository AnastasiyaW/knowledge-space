---
title: "Surflo"
category: "projects"
date: 2026-09-10
tags: ["3d_surface_reconstruction", "project", "surflo", "surflo-3d-surface-reconstruction", "surflo-development"]
aliases: ["Surflo"]
---

# Surflo

**Development line:** project:surflo-3d-surface-reconstruction · thread surflo-development  
**Last event:** 2026-09-10 · 2 dated since 2026-06-13 · **Researched:** 2026-11-25 · confidence: high

## What it is

Surflo (Consistent 3D Surface Flow Model with Global State) turns 2 to about 80 unposed RGB views into a 3D surface.

It encodes the input views into a latent of 128 tokens x 512 dims. Flow matching then decodes that latent into oriented surface points (position plus normal), which turn into a clean mesh. The model has 1.39B parameters in total, with 128.8M trainable and a frozen VGGT-1B backbone. The GitHub page lists the work as a NeurIPS 2026 Oral.

## Development line

- **2026-06-13 — Surflo project resources were referenced for 3D surface reconstruction.** On 2026-06-13, the 3D surface reconstruction thread referenced Surflo's project page and GitHub repository. This records a dated entry point to the project, but available evidence identifies no release, version, benchmark, or other project change on that date.
- **2026-09-10 — Release of Surflo 3D surface reconstruction weights and code.** The team released weights and code for Surflo, a 3D reconstruction model from multiple photos, hosted on GitHub and Hugging Face.
  - The GitHub repository (Anttwo/Surflo) is the official implementation. It has configs, examples, install files, scripts, and training code, and links to weights, training data, and eval data. The authors are Antoine Guédon, Shu Nakamura, Nicolas Dufour, Jiahui Lei, Ko Nishino, and Angjoo Kanazawa, from Ecole polytechnique, Kyoto University, Kyutai, and UC Berkeley. It is installed from a source checkout with compiled CUDA extensions because there is no pip package. Ready-made install files cover CUDA 11.8, 12.1, and 12.4. (undated) — <https://github.com/Anttwo/Surflo>
  - The Hugging Face model card (AntoineGuedon/Surflo-v0) is tagged Image-to-3D. It describes feed-forward surface reconstruction from 2-80 unposed RGB images without poses or intrinsics. Output is an oriented point cloud at arbitrary resolution plus an optional mesh. It has 1.39B total parameters, 128.8M trainable, and a frozen VGGT-1B backbone. The checkpoint is released under CC BY-NC 4.0 (non-commercial only) because it embeds Meta's VGGT-1B weights. The code is under the Gaussian-Splatting (Inria/MPII) license for non-commercial research only. (undated) — <https://huggingface.co/AntoineGuedon/Surflo-v0>

## What changed

The authors published official code on GitHub and the checkpoint (Surflo-v0) on Hugging Face. They also link training data, evaluation data, a project page, an arXiv paper, and a video. According to the repository, Surflo beats pointmap feed-forward models in quality. It runs an order of magnitude faster than optimization-based methods like Gaussian Wrapping, which need hundreds of views. Both code and weights are limited to non-commercial use.

## How to use this

1. Clone the repository with submodules (git clone git@github.com:Anttwo/Surflo.git --recursive). Create the conda environment for the CUDA family (cu118, cu121 or cu124) with install/environment-cu118.yml. Run pip install -e ".[demo,texture,train]". Then run install/activate_cuda.sh and install/build_extensions.sh --all, and check with install/verify_install.py.
  — <https://github.com/Anttwo/Surflo>
2. In Python, load the checkpoint with Surflo.from_checkpoint("checkpoint_200.pt", device="cuda"). Call surflo.encode(image_folder, n_images=16) to get the 128x512 global state. Then call scene.reconstruct(mode="guided", num_query_points=100000, ...) and save with save_ply. Optionally call scene.extract_mesh, color_mesh, and save_mesh to get a mesh.
  — <https://huggingface.co/AntoineGuedon/Surflo-v0>
3. Alternatively, run the command line: python scripts/infer.py mode=guided guided=default ckpt=/path/to/checkpoint_200.pt source.image_folder=/path/to/images num_query_points=100000 output_dir=outputs/surflo.
  — <https://huggingface.co/AntoineGuedon/Surflo-v0>

## Best practices

- Use guided=default as the recommended quality/time trade-off (about 47 s and 14 GiB on an H100 with 16 views and 100k points). Use plain mode for a fast, deterministic run without rendering (about 8 s, 8.5 GiB). guided=long (about 95 s) does not improve on default.
  — <https://huggingface.co/AntoineGuedon/Surflo-v0>
- Prefer conda for installation because it gives a self-contained environment with its own nvcc, so nothing on the system has to match. The uv route needs a system CUDA toolkit of 11.8, 12.1, or 12.4.
  — <https://github.com/Anttwo/Surflo>
- Supply landscape images where possible. The model is trained on landscape images only, so portrait images are automatically rotated 90°. If the first view is portrait, the output point cloud or mesh comes out in that rotated frame.
  — <https://github.com/Anttwo/Surflo>
- Treat the checkpoint and code as non-commercial research artifacts (CC BY-NC 4.0 weights, Gaussian-Splatting License code) and do not use them in commercial products.
  — <https://huggingface.co/AntoineGuedon/Surflo-v0>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The linked pages carry no explicit release date, so the 2026-09-10 date comes from the reviewed event.
- Independent benchmark results and community reception are not covered by the linked pages.
- The GitHub page was truncated, so the full installation and demo instructions were not seen.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Anttwo/Surflo | GitHub - Anttwo/Surflo: Official implementation of Surflo: Consistent 3D Surface Flow Model with Global State | 2026-09-10 |
| https://huggingface.co/AntoineGuedon/Surflo-v0 | AntoineGuedon/Surflo-v0 · Hugging Face | 2026-09-10 |

## Agent brief {#agent-brief}

- **Subject:** project:surflo-3d-surface-reconstruction, thread surflo-development, 2 dated events 2026-06-13 → 2026-09-10.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
