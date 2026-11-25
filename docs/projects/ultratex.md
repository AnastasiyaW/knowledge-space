---
title: "Ultratex: ultratex-release-line — Ultratex Release Line"
category: "projects"
date: 2026-11-19
tags: ["project", "ultratex", "ultratex-release-line"]
aliases: ["Ultratex: ultratex-release-line"]
---

# Ultratex: ultratex-release-line — Ultratex Release Line

UltraTex generates 4K PBR textures for 3D meshes from a reference image, an alternative to TEXTure and Paint3D.

**Development line:** project:ultratex · thread ultratex-release-line  
**Last event:** 2026-11-19 · 2 dated since 2026-11-19 · **Researched:** 2026-11-20 · confidence: medium

## What it is

UltraTex is a physically based rendering texture generator for 3D asset creators and technical artists. It competes with multi-view diffusion texturing systems like TEXTure and Paint3D. It does three things:

- Generates unlit albedo color and surface normal maps from several canonical viewpoints.
- Estimates synchronized roughness and metallic channels using vision-language physical priors.
- Projects and blends the multi-view predictions into one 4K UV texture map.

Output is 4K across standard UV unwraps. Full model weights and local training code are not released. The framework separates material albedo from baked environmental lighting. Until open inference code ships, it can only be tried in the online demo.

## Development line

- **2026-11-19 — Meshy AI publishes UltraTex PBR texture generation research.** On 18 November, Meshy AI released a paper on arXiv for UltraTex. The system generates 4K PBR textures for 3D assets from a reference image by separating intrinsic material color from lighting. It predicts unlit color and normals across views, then estimates metallic and roughness. A demo is on Hugging Face. No code is available and the model license is not specified yet.
- **2026-11-19 — Meshy AI publishes UltraTex PBR texture generation research.** On 18 November, Meshy AI's UltraTex work appeared on arXiv. It generates PBR textures for 3D assets from a reference image and separates intrinsic material color from lighting. It predicts per-view albedo and normals, then metallic-roughness, and assembles six-view maps into 4K UV textures. A demo is on Hugging Face and a project page exists. Code and model license were not stated at release.
- **2026-11-19 — more detail from the paper and the demo.**
  - The paper describes a physical knowledge alignment framework. It uses cascaded multi-view diffusion models and VLM semantic priors to separate intrinsic material color from lighting, and it synthesizes 4K PBR maps: albedo, normal, roughness and metallic. (2026-11-18) — <https://arxiv.org/abs/2611.24941>
  - The Hugging Face space by Jingzhi03 demonstrates texture synthesis from a reference image and a 3D mesh. Full training weights and the code repository were not released at publication. (2026-11-19) — <https://huggingface.co/Jingzhi03/UltraTex>

## What changed

UltraTex started as academic research on baked-in lighting in automated 3D texturing. The architecture moved from direct appearance matching to a multi-stage pipeline. It first fixes geometry and diffuse color consistency, then predicts specular and roughness properties. It was shared as a paper plus hosted cloud demos. Source repositories and standalone model weights were held back pending a formal release.

## How to use this

1. Upload an untextured 3D mesh in OBJ or GLB format and a single reference image to the hosted UltraTex interface on Hugging Face.
  — <https://huggingface.co/Jingzhi03/UltraTex>
2. Check the predicted multi-view unlit albedo and surface normal maps, so geometry stays aligned across canonical viewpoints.
  — <https://ultratex.vercel.app/>
3. Export the assembled 4K PBR map set (albedo, normal, metallic, roughness) into a 3D content creation tool or a real-time game engine.
  — <https://arxiv.org/abs/2611.24941>

## Best practices

- Use reference images with diffuse, neutral lighting, so surface color separates cleanly from specular highlights.
  — <https://arxiv.org/abs/2611.24941>
- Prepare input meshes with clean, non-overlapping UV unwrapping before the multi-view feature maps are projected into UV space.
  — <https://ultratex.vercel.app/>

## Superseded by this

- Direct appearance-matching diffusion pipelines predict textures without separating material from lighting. They bake environmental illumination into albedo and distort specular estimation.
  — <https://arxiv.org/abs/2611.24941>

## Still unknown

- Whether the code will be open source, and under what license the model weights fall. Until then nobody can run the pipeline locally.
- Plans to integrate UltraTex into commercial 3D authoring suites or the Meshy platform product line have not been detailed publicly.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2611.24941 | UltraTex: Aligning Physical Knowledge for High-Fidelity PBR Texture Generation | 2026-11-20 |
| https://ultratex.vercel.app/ | UltraTex: Project Page and Gallery | 2026-11-20 |
| https://huggingface.co/Jingzhi03/UltraTex | Jingzhi03/UltraTex Hugging Face Space | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:ultratex, thread ultratex-release-line, 2 dated events 2026-11-19 → 2026-11-19.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** medium. The dated entries under "Superseded by this" decide what is obsolete.
