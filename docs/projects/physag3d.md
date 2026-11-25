---
title: "PhysAg3D: physag3d-release-announcement — PhysAg3D Release Announcement"
category: "projects"
date: 2026-11-03
tags: ["physag3d", "physag3d-release-announcement", "project"]
aliases: ["Physag3D: physag3d-release-announcement"]
---

# PhysAg3D: physag3d-release-announcement — PhysAg3D Release Announcement

**Development line:** project:physag3d · thread physag3d-release-announcement  
**Last event:** 2026-11-03 · 1 dated since 2026-11-03 · **Researched:** 2026-11-25 · confidence: medium

## What it is

PhysAg3D is a research framework from Peking University, Huawei and collaborators for generating interactive 3D assets from single images.

- Vision-language agent: infers semantic parts, candidate interactions, and physical priors from a single image.
- Pretrained 3D generator: produces a textured whole-object mesh separately from the same image.
- Hierarchical interaction representation: links revisable priors to mechanisms and controlled surfaces.
- Geometric and physical tools: let the agent build parts, joints, deformable regions, and surface bindings.
- Two separate models: keep useful geometry and materials without joint training.

## Development line

- **2026-11-03 — PhysAg3D releases image-to-interactive-3D agent pipeline.** PhysAg3D combines a VLM agent with the TRELLIS.2 3D generator. It turns one image into an interactive 3D asset with joints, deformable zones, and physics priors. Outputs include GLB, Blender, and MuJoCo scenes. Running the pipeline requires Blender, Codex CLI, and a Linux host with at least 28 GB VRAM for TRELLIS.2.
  - The project page is titled 'Bridging 3D Generative and Agentic Models for High-Fidelity and Physically-Interactive Assets'. It describes a three-stage method: infer and generate, construct and bind, then observe and refine. Rendered interactions and execution measurements guide targeted revisions within a fixed budget. On the in-the-wild evaluation (50 objects, 110 predefined semantic actions) it reports a 91.3% Action Completion Rate and an 88.0% Function-and-Visible-Stability pass rate. It also evaluates on the PhysXVerse, PhysX-Mobility and PhysX-Bench benchmarks and compares printer and chair examples against aDSL and PhysX-Omni. The gallery lists 223 generated assets, and the film shows 30 objects in a shared studio with Franka Panda demonstrations on 10 interactive assets. The page cautions that a single image does not uniquely determine hidden mechanisms or material parameters. (undated) — <https://supra-3d.github.io/PhysAg3D/>

## What changed

The project page presents the method with a gallery of 223 generated assets, a studio film, and quantitative results on real photographs and external benchmarks. It covers both rigid articulation and compliant deformation.

## How to use this

1. Open the project page and browse the generated-asset gallery. Filter by category, such as furniture, appliances, electronics or vehicles, or search by name.
  — <https://supra-3d.github.io/PhysAg3D/>
2. Click Interact on an asset to open it in the in-browser 3D viewer and inspect its shape and motion. The page also offers downloads of the asset and the interaction video.
  — <https://supra-3d.github.io/PhysAg3D/>
3. Compare the input image, the generated asset and the interaction clip for each case. For real photographs, use the 'In the wild' qualitative results as a reference for the expected output.
  — <https://supra-3d.github.io/PhysAg3D/>

## Best practices

- Treat the demonstrations as evidence of plausible interactions, not physical validation. Playback and physical validation provide different evidence. The authors note that a single image does not uniquely determine hidden mechanisms or material parameters.
  — <https://supra-3d.github.io/PhysAg3D/>
- Keep refinement bounded. Targeted revisions follow rendered interactions and execution measurements within a fixed budget. Ablations support both bounded refinement and preserving the source surface.
  — <https://supra-3d.github.io/PhysAg3D/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Hardware and software requirements remain unstated on the project page. Blender, Codex CLI, and a Linux host with at least 28 GB VRAM for TRELLIS.2 come from the announcement and were not checked against the repository.
- The page gives no release date, license, or exact contents of the code release.
- The page has no date, and describes the paper only as a research manuscript.

## Sources

| source | title | read |
|---|---|---|
| https://supra-3d.github.io/PhysAg3D/ | PhysAg3D — High-Fidelity, Physically Interactive 3D Assets | 2026-11-03 |

## Agent brief {#agent-brief}

- **Subject:** project:physag3d, thread physag3d-release-announcement, 1 dated events 2026-11-03 → 2026-11-03.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
