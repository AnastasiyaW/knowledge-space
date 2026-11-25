---
title: "Pami: pami-part-anchored-hoi-generation — Pami Part Anchored Hoi Generation"
category: "projects"
date: 2026-11-20
tags: ["pami", "pami-part-anchored-hoi-generation", "project"]
aliases: ["Pami: pami-part-anchored-hoi-generation"]
---

# Pami: pami-part-anchored-hoi-generation — Pami Part Anchored Hoi Generation

**Development line:** project:pami · thread pami-part-anchored-hoi-generation  
**Last event:** 2026-11-20 · 2 dated since 2026-11-20 · **Researched:** 2026-11-21 · confidence: medium

## What it is

PAMI generates full-body human-object interactions from text, for graphics and computer vision researchers. It replaces independent trajectory prediction with body-part-anchored motion voting. It does the following:

- Text and a static object mesh in, synchronized full-body human motion and 3D object trajectories out.
- Object motion is expressed relative to several anatomical anchor points, using a voting mechanism inspired by the Hough transform.
- PamiVAE and PamiGen generate a coarse full-body interaction sequence in a structured latent space.
- PamiRefiner fixes contact geometry and removes mesh penetration. It is recursive and senses the surface with long-range probes and short-range proximity sensors.

Limit: it needs existing 3D object geometry, and it stays within the interaction categories found in the benchmark capture sets. The formulation is mechanically sound for multi-contact manipulation. Unanchored generative baselines drift in trajectory and leave objects floating.

## Development line

- **2026-11-20 — PAMI human-object interaction code published.** The PAMI project published its code for generating human-object interactions from text and an object mesh. The repository is linked on GitHub.
- **2026-11-20 — PAMI human-object interaction generation code published.** The authors of PAMI released the code on GitHub. The project generates human-object interactions from text and object meshes.
- **2026-11-20 — other reporting on this date.**
  - The release introduces PAMI \\(Part-Anchored Motion for Text-to-Human-Object Interaction Generation\\) by Chuqiao Li, Xianghui Xie, Yong Cao, Andreas Geiger, and Gerard Pons-Moll. It uses a Hough-transform-inspired anchor-voting mechanism across the PamiVAE, PamiGen, and PamiRefiner stages. Contact recall improves by 14.5% on the InterAct benchmark. (2026-11-20) — <https://github.com/Coral79/PAMI-Code>
  - The repository holds the code for relative body-part coordinate voting. It also holds the recursive surface-sensing refiner, whose long-range probes and short-range proximity sensors prevent object drift and mesh penetration. (2026-11-20) — <https://github.com/Coral79/PAMI-Code>

## What changed

PAMI moves full-body text-to-HOI synthesis away from decoupled human and object trajectory estimation. It uses part-anchored relative motion instead. Earlier baselines treated human poses and object paths as independent or loosely coupled global channels. The result was missed contacts, hand-object penetrations, and drifting trajectories.

PAMI rebuilt the pipeline as a coarse-to-fine hierarchy:

- Object movement is split into relative coordinate systems anchored to key body joints.
- A specialized variational autoencoder learns the interaction manifold.
- A coarse interaction is predicted from the language description.
- Geometric distance sensors refine the local contact points.

The public codebase has reference implementations of the voting autoencoder, the generative diffusion pipeline, and the contact refinement stages.

## How to use this

1. Clone the Coral79/PAMI-Code repository from GitHub. Set up the environment with the required PyTorch, CUDA, and 3D geometry packages.
  — <https://github.com/Coral79/PAMI-Code>
2. Give it a descriptive text prompt and a 3D target object mesh that follows the expected coordinate conventions.
  — <https://github.com/Coral79/PAMI-Code>
3. Run the coarse generation pipeline: PamiGen inside the PamiVAE latent space produces anchor-voted candidate trajectories.
  — <https://github.com/Coral79/PAMI-Code>
4. Run the recursive PamiRefiner to adjust fine contact geometry and resolve foot or hand penetrations against the object surface.
  — <https://github.com/Coral79/PAMI-Code>

## Best practices

- Use object meshes with clean surface geometry and consistent scale, so the refiner's proximity sensors can compute valid contact fields.
  — <https://github.com/Coral79/PAMI-Code>
- Keep the full coarse-to-fine pipeline with PamiRefiner. Coarse latent samples alone leave localized contact penetrations.
  — <https://github.com/Coral79/PAMI-Code>

## Superseded by this

- Direct global trajectory prediction for 3D objects in text-driven HOI synthesis. It treated human and object trajectories as independent channels, and it suffered from object drift and hand penetration.
  — <https://github.com/Coral79/PAMI-Code>

## Still unknown

- The arXiv preprint date and the URL of the standalone project demo page. Search redirects did not lead to verified direct URLs.
- Community usage reports, third-party reproduction benchmarks, and user discussion threads. None have appeared yet on public forums or GitHub issues since the repository went up.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Coral79/PAMI-Code | Coral79/PAMI-Code: Part Anchored Motion for Text-to-Human-Object Interaction Generation | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** project:pami, thread pami-part-anchored-hoi-generation, 2 dated events 2026-11-20 → 2026-11-20.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
