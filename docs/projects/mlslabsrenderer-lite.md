---
title: MLSLabsRenderer-Lite
category: projects
date: 2026-07-29
tags: [mlslabsrenderer-lite, project]
aliases: ["MLSLabsRenderer-Lite"]
---

# MLSLabsRenderer-Lite

**Development line:** `project:mlslabsrenderer-lite` · thread `mlslabsrenderer-lite`  
**Last event:** 2026-07-29 · 1 dated since 2026-07-29 · **Researched:** 2026-11-21 · confidence: high

## What it is

MLSLabsRenderer-Lite is a free Unreal Engine 5 plugin for real-time rendering of 3D Gaussian Splatting and 4D Gaussian sequences on Win64.

- Developer: MaLanShan Audio & Video Laboratory, published under the repository owner "mlslabs". The Lite branch sits beside a Pro branch in the same repository.
- Users: Unreal Engine developers who play static .ply splats or .ply sequences in a scene, including Sequencer keyframing.
- Support: UE 5.5, 5.6 and 5.7; Win64 only, per the Fab listing. Needs the EditorScriptingUtilities and PythonScriptPlugin dependencies.
- Limits: developer-reported figures on an RTX 4070 Ti: static 7M+ Gaussians at 50+ FPS, and 4DGS 100K+ Gaussians at 100+ FPS. We did not measure them.

As of 2026-11, the Lite branch is still beta. Its latest tag is Lite_V1.0.0.10_beta (2026-03-27).

## Development line

- **2026-07-29 — Public project and repository reference for MLSLabsRenderer-Lite.** On 2026-07-29, we recorded MLSLabsRenderer-Lite with links to its project site and the MLSLabs Gaussian Splatting Renderer UE repository. The dated links give a public reference point for the renderer. They do not confirm a specific release, feature set, or version.

## What changed

- 2026-03-06 — Lite_V1.0.0.8_beta tagged as separate builds for UE 5.5, 5.6 and 5.7.
- 2026-03-12 — Lite_V1.0.0.9_beta tagged for the same three engine versions.
- 2026-03-27 — Lite_V1.0.0.10_beta, the latest Lite tag. The Fab listing shows the same version as current. We did not read its release notes.

## How to use this

1. Confirm the engine and platform before installing. The Fab listing shows UE 5.5, 5.6 and 5.7 on Win64.
  — <https://www.fab.com/listings/f91b57cc-958d-40dd-a455-2535bf00e588>
2. Take the build tag that matches your engine version. Lite_V1.0.0.10_beta is the latest; 1.0.0.8 and 1.0.0.9 have per-engine tags.
  — <https://github.com/mlslabs/MLSLabsGaussianSplattingRenderer-UE/releases>
3. Enable the EditorScriptingUtilities and PythonScriptPlugin dependencies in the project before loading the plugin.
  — <https://www.fab.com/listings/f91b57cc-958d-40dd-a455-2535bf00e588>
4. Import static scenes as .ply and volumetric content as .ply sequences. Use Sequencer to keyframe playback.
  — <https://www.fab.com/listings/f91b57cc-958d-40dd-a455-2535bf00e588>
5. Benchmark on your own GPU before relying on the developer's RTX 4070 Ti figures.
  — <https://www.fab.com/listings/f91b57cc-958d-40dd-a455-2535bf00e588>

## Best practices

- Match the plugin build to the engine version. The per-engine beta tags (ue5.5, ue5.6, ue5.7) are separate builds.
  — <https://github.com/mlslabs/MLSLabsGaussianSplattingRenderer-UE/releases>
- Treat the Pro branch as a separate product. Its README lists Windows in requirements, while its release notes claim Windows, Linux and Android support; check the platform you need.
  — <https://github.com/mlslabs/MLSLabsGaussianSplattingRenderer-UE>

## Superseded by this

- Lite_V1.0.0.8_beta and Lite_V1.0.0.9_beta are superseded by Lite_V1.0.0.10_beta. Per-engine availability of 1.0.0.10 is not confirmed beyond the Fab listing.

## Still unknown

- Feature differences between Lite and Pro are not stated on the Lite listing.
- The Fab listing shows no license terms. The repository is Apache-2.0 at the repository level; the Lite branch's terms were not confirmed separately.
- The developer's website (read 2026-11-21) shows only a heading in Chinese and no product text, so it is not used as a source for claims.
- Lite_V1.0.0.10_beta release notes were not read.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/mlslabs/MLSLabsGaussianSplattingRenderer-UE | MLSLabsGaussianSplattingRenderer-UE — README and repository | 2026-11-21 |
| https://github.com/mlslabs/MLSLabsGaussianSplattingRenderer-UE/releases | MLSLabsGaussianSplattingRenderer-UE — releases | 2026-11-21 |
| https://www.fab.com/listings/f91b57cc-958d-40dd-a455-2535bf00e588 | MLSLabsRenderer-Lite — Fab listing | 2026-11-21 |
| https://mls4dlive.cn/ | Developer site (no Lite product text) | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:mlslabsrenderer-lite`, thread `mlslabsrenderer-lite`, 1 dated events 2026-07-29 → 2026-07-29.
- **Practical note:** A free Win64 UE 5.5–5.7 plugin for 3DGS and 4DGS playback, latest Lite_V1.0.0.10_beta (2026-03-27). Use the per-engine tag; benchmark the developer's figures on your own GPU.
- **Confidence:** high for the listing and tags; performance figures are developer-reported. Dated supersedes above are the authority for what is obsolete.
