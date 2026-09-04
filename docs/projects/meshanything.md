---
title: MeshAnything
category: projects
date: 2024-08-06
tags: [meshanything, meshanything-development, project]
aliases: ["MeshAnything", "MeshAnything V2"]
---

# MeshAnything

**Development line:** `project:meshanything` · thread `meshanything-development`  
**Last event:** 2024-08-06 · 2 dated since 2024-06-17 · **Researched:** 2026-09-04 · confidence: medium

## What it is

MeshAnything V2 is a local post-processing model for technical artists and 3D-pipeline engineers who need a compact triangle mesh from a dense 3D shape, rather than a prompt-to-3D asset generator.

- Takes a supplied mesh or normal-bearing point cloud and predicts an artist-style mesh aligned to that shape.
- Fits after reconstruction, scanning, SDS, or another dense-mesh generator; V2 also exposes local Gradio, CLI, tokenization, and training code.

## Development line

- **2024-06-17 — MeshAnything public project resources were linked.** A VQ-VAE mesh vocabulary plus decoder-only transformer turned a supplied 3D shape into a low-face artist-style triangle mesh.
- **2024-08-06 — MeshAnything V2 public resources were linked.** On 2024-08-06, the MeshAnything thread linked a V2 project page, a distinct V2 source repository, and a Hugging Face Space, with a reference back to the earlier thread item. This marks a later V2-era development point, but the links do not state exact changes, model behavior, or availability status.

## What changed

- 2024-06-17 — MeshAnything made shape-conditioned autoregressive remeshing available: a VQ-VAE mesh vocabulary plus decoder-only transformer turned a supplied 3D shape into a low-face artist-style triangle mesh.
- 2024-08-06 — MeshAnything V2 replaced face-by-face tokenization with Adjacent Mesh Tokenization, shortening sequences by about half and doubling the documented cap from 800 to 1600 faces.
- 2025-04-28 — The official V2 repository added a training commit; its current documentation covers processed Objaverse data, a Michelangelo point encoder, and multi-GPU training and evaluation.

## How to use this

From 2024-08-06, we treat MeshAnything V2 as a separate versioned resource line. Consult its dedicated project page, repository, and Hugging Face Space rather than assuming the 2024-06-17 resources describe V2.

1. Clone the official V2 repository and build its tested local environment: Ubuntu 22.04, CUDA 11.8, Python 3.10.13, PyTorch 2.1.1, FlashAttention, and Gradio.
  — <https://github.com/buaacyw/MeshAnythingV2>
2. Download official Yiwen-ntu/MeshAnythingV2 model weights for local inference; the model card identifies the library repository and lists a 0.5B-parameter model.
  — <https://huggingface.co/Yiwen-ntu/MeshAnythingV2>
3. Supply either a dense input mesh or an N×6 .npy point cloud containing coordinates and normals. For a text or image request, first use an upstream system to produce the dense mesh, then pass its OBJ to MeshAnything.
  — <https://github.com/buaacyw/MeshAnythingV2>
4. For a mesh that did not come from Marching Cubes, run main.py with --mc; start at the default 128 resolution and use --mc_level 8 only when delicate geometry needs 256-resolution preprocessing.
  — <https://github.com/buaacyw/MeshAnythingV2>
5. Run CLI inference with main.py or a local UI with app.py, then inspect the output against the 1600-face cap and downstream topology requirements.
  — <https://github.com/buaacyw/MeshAnythingV2>
6. For training, obtain the processed Objaverse split and Michelangelo point-encoder checkpoint, then use the documented eight-process accelerate training/evaluation commands.
  — <https://github.com/buaacyw/MeshAnythingV2>

## Best practices

- Use a sharp, high-quality mesh from reconstruction, scanning, SDS, or a dense-mesh generator; official guidance warns that weak feed-forward geometry may lack shape detail for the face budget.
  — <https://github.com/buaacyw/MeshAnythingV2>
- Normalize the input to a unit bounding box and keep its up direction at +Y before inference.
  — <https://github.com/buaacyw/MeshAnythingV2>
- Use Marching Cubes preprocessing for non-Marching-Cubes meshes; increase resolution only after comparing added preprocessing time with topology improvement.
  — <https://github.com/buaacyw/MeshAnythingV2>
- Keep the task within the documented 1600-face ceiling rather than expecting a detailed high-poly output.
  — <https://github.com/buaacyw/MeshAnythingV2>
- Do not automate against the official V2 Space: it is paused; use the repository and downloaded weights for a reproducible local route.
  — <https://huggingface.co/spaces/Yiwen-ntu/MeshAnythingV2>
- Treat use under the official repository's S-Lab License as non-commercial until the authors clarify the conflicting model-card license label.
  — <https://raw.githubusercontent.com/buaacyw/MeshAnythingV2/main/LICENSE.txt>
- Before training, check the checked-out filename: the README refers to training_requirements.txt while the repository file list shows training_requirement.txt.
  — <https://github.com/buaacyw/MeshAnythingV2>

## Superseded by this

- 2024-08-06 — MeshAnything V1 guidance capped generated meshes below 800 faces; V2's 1600-face official model replaces that capacity limit for new V2 runs.
- 2025-04-28 — The claim that V2 has no official training path is obsolete: the repository's training commit and current instructions provide one.
- 2026-09-04 — Using the hosted V2 Gradio Space as the current access route is obsolete: the official Space is paused.

## Still unknown

- The official V2 repository license permits non-commercial use, while the official Hugging Face model card labels the model MIT; we do not know which license governs commercial use of the weights.
- The official documentation is tested on Ubuntu 22.04 and CUDA 11.8, but current-driver compatibility and a successful inference run were not independently reproduced here.
- The documentation does not establish preservation of UVs, materials, rigs, watertightness, or animation-readiness; validate those requirements on representative assets before adoption.
- No V3 or post-2025 functional release was identified in the official endpoints checked; that is not proof that an unpublished successor does not exist.

## Sources

| source | title | read |
|---|---|---|
| https://buaacyw.github.io/mesh-anything/ | MeshAnything project page | 2026-09-04 |
| https://github.com/buaacyw/MeshAnything | MeshAnything official repository | 2026-09-04 |
| https://arxiv.org/abs/2406.10163 | MeshAnything: Artist-Created Mesh Generation with Autoregressive Transformers | 2026-09-04 |
| https://buaacyw.github.io/meshanything-v2/ | MeshAnything V2 project page | 2026-09-04 |
| https://github.com/buaacyw/MeshAnythingV2 | MeshAnything V2 official repository | 2026-09-04 |
| https://github.com/buaacyw/MeshAnythingV2/commits/main | MeshAnything V2 commit history | 2026-09-04 |
| https://arxiv.org/abs/2408.02555 | MeshAnything V2: Artist-Created Mesh Generation With Adjacent Mesh Tokenization | 2026-09-04 |
| https://huggingface.co/Yiwen-ntu/MeshAnythingV2 | Yiwen-ntu/MeshAnythingV2 model card | 2026-09-04 |
| https://huggingface.co/spaces/Yiwen-ntu/MeshAnythingV2 | Yiwen-ntu/MeshAnythingV2 Space | 2026-09-04 |
| https://raw.githubusercontent.com/buaacyw/MeshAnythingV2/main/LICENSE.txt | S-Lab License 1.0 for MeshAnything V2 | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:meshanything`, thread `meshanything-development`, 2 dated events 2024-06-17 → 2024-08-06.
- **Practical note:** From 2024-08-06, practitioners should treat MeshAnything V2 as a separate versioned resource line and consult its dedicated project page, repository, and Hugging Face Space rather than assuming the 2024-06-17 resources describe V2.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
