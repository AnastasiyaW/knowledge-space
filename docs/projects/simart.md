---
title: SIMART
category: projects
date: 2026-05-19
tags: [project, simart, simart-development]
aliases: ["SIMART", "SimArt"]
---

# SIMART

**Development line:** `project:simart` · thread `simart-development`  
**Last event:** 2026-05-19 · 2 dated since 2026-03-30 · **Researched:** 2026-09-04 · confidence: high

## What it is

SIMART is a ByteDance Seed research implementation for 3D and robotics practitioners who need to convert a monolithic mesh into articulated parts for simulators. It combines a Qwen3-VL-based MLLM with a Sparse 3D VQ-VAE. It predicts part decomposition, physical metadata, joint types, axes, and limits, then outputs URDF-oriented files. The paper reports 70% fewer geometry tokens than dense voxels. The repository is tested on Python 3.10 and provides local checkpoints rather than a hosted inference endpoint. Use it as a local research pipeline for preparing articulated assets, and validate the generated URDF before relying on it in a simulator.

## Development line

- **2026-03-30 — SIMART project website referenced.** On 2026-03-30, the project website established the first public entry point. The available evidence identifies no specific release, capability, or version.
- **2026-05-19 — SIMART Hugging Face repository referenced.** On 2026-05-19, the ByteDance-Seed/SimArt Hugging Face repository appeared alongside the project page. The available evidence does not establish repository contents, license, or exact release status.

## What changed

- **2026-03-24** — The arXiv preprint introduced SIMART’s unified mesh-to-articulated-asset method, Sparse 3D VQ-VAE, and SIMART-Bench, reporting a 70% token reduction against dense voxel tokens.
- **2026-03-30** — The project page made the research presentation and interactive articulated-asset gallery available, describing structured URDF metadata plus decomposed segments.
- **2026-05-19** — Tracked links added the ByteDance-Seed Hugging Face repository alongside the project page. The model card identifies two checkpoint groups, `simart_mllm/` and `simart_vqvae/`.
- **2026-05-28** — An update appeared on `ByteDance-Seed/SimArt` on Hugging Face. The model card supplies weights without a hosted inference provider.
- **2026-09-05** — The public GitHub README documented local installation, mesh alignment, preprocessing, and inference for GLB inputs.

## How to use this

From 2026-05-19, practitioners should check the linked ByteDance-Seed/SimArt Hugging Face repository alongside the SIMART project site when looking for project materials; the dated evidence does not confirm which artifacts are usable.

1. Clone the implementation, create a Python 3.10 environment, and install `requirements.txt`.
  — <https://github.com/ByteDance-Seed/SimArt>
2. Download both checkpoint groups from the official Hugging Face repository and place them under `./checkpoints` or pass custom paths.
  — <https://huggingface.co/ByteDance-Seed/SimArt>
3. Normalize a raw `.glb` mesh with `scripts/process_raw_objects.py`; render a preview during preprocessing.
  — <https://github.com/ByteDance-Seed/SimArt>
4. Run `inference/infer.py --object_path <processed.glb> --debug` to generate the articulated structure, URDF and debug visualizations.
  — <https://github.com/ByteDance-Seed/SimArt>

## Best practices

- Use a right-handed coordinate system with +Z up and a consistent forward direction; correct rotations for meshes that use a different convention.
  — <https://github.com/ByteDance-Seed/SimArt>
- Render the normalization preview and check that the object is upright and forward-facing before inference, because orientation affects semantic parts such as handles and front legs.
  — <https://github.com/ByteDance-Seed/SimArt>
- Use `--debug` to inspect colored part meshes and joint axes, then verify the produced URDF in the target simulator before using it for robot-policy work.
  — <https://github.com/ByteDance-Seed/SimArt>

## Superseded by this

- 2026-03-24 — Treating SIMART as a paper-only method is obsolete: the repository and checkpoint publication provide a local inference path.
- 2026-05-28 — Assuming SIMART is available through a managed Hugging Face inference provider is unsupported; the official model page states that no provider deploys it.

## Still unknown

- The official Hugging Face model card does not display its own publication timestamp, so no independently dated change can be assigned specifically to the 2026-05-19 event beyond the presence of that repository link.
- The name is ambiguous on the wider web: an unrelated 6G sensing-and-communication platform is also called SimART. The cited ByteDance Seed project, paper, code and weights consistently identify the articulated-3D-assets subject.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2603.23386 | SIMART: Decomposing Monolithic Meshes into Sim-ready Articulated Assets via MLLM | 2026-09-05 |
| https://simart-mllm.github.io/ | SIMART: Decomposing Monolithic Meshes into Sim-ready Articulated Assets via MLLM | 2026-09-05 |
| https://github.com/ByteDance-Seed/SimArt | ByteDance-Seed/SimArt | 2026-09-05 |
| https://huggingface.co/ByteDance-Seed/SimArt | ByteDance-Seed/SimArt | 2026-09-05 |
| https://huggingface.co/MinghanQin/activity/all | Minghan Qin activity | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:simart`, thread `simart-development`, 2 dated events 2026-03-30 → 2026-05-19.
- **Practical note:** From 2026-05-19, practitioners should check the linked ByteDance-Seed/SimArt Hugging Face repository alongside the SIMART project site when looking for project materials; the dated evidence does not confirm which artifacts are usable.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.