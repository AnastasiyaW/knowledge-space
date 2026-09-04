---
title: MetaHuman
category: projects
date: 2022-06-10
tags: [metahuman, metahuman-development-and-applications, metahuman_applications, project]
aliases: ["MetaHuman"]
---

# MetaHuman

**Development line:** `project:metahuman` · thread `metahuman-development-and-applications`  
**Last event:** 2022-06-10 · 1 dated since 2022-06-10 · **Researched:** 2026-09-04 · confidence: high

## What it is

MetaHuman is an Unreal Engine framework for character artists, virtual-production teams, and game developers.

- Asset creation: builds editable face, body, hair, clothing, and material assets.
- Mesh conforming: fits scans, sculpts, and other meshes to an animation-ready MetaHuman.
- Target assembly: packages assets for cinematic or real-time targets.

## Development line

- **2022-06-10 — MetaHuman update introduced custom-head import.** We track landmarks on a textured custom facial mesh and cloud-match it to MetaHuman topology. The system returns a fully rigged character. The release added 23 grooms, ten facial animation loops, six body poses, five facial poses, and UE5 rigging and retargeting compatibility.

## What changed

- **2022-06-10** — Mesh to MetaHuman launched in the Unreal Engine MetaHuman Plugin. We track landmarks on a textured custom facial mesh and cloud-match it to MetaHuman topology. It returns a fully rigged character. The release added 23 grooms, ten facial animation loops, six body poses, five facial poses, and UE5 rigging and retargeting compatibility.
- **2022-06-21** — The linked video cannot currently be retrieved or identified reliably, so no release claim is attached to this date.
- **2023-06-15** — MetaHuman Animator added high-fidelity facial-performance solving from iPhone or stereo head-mounted-camera capture.
- **2024-03-28** — MetaHuman became available in UEFN. Unreal Engine 5.4 introduced the CLO/Marvelous Designer path for dynamic clothing.
- **2025-06-03** — MetaHuman 5.6 left Early Access and moved Creator, Animator, and Mesh to MetaHuman into Unreal Engine. It added parametric bodies, Outfit Assets, real-time animation from supported cameras or audio, and broader licensing.
- **2026-06-17** — MetaHuman 5.8 added full-body Mesh to MetaHuman, MetaHuman Crowds, and further open-sourced technology components.

## How to use this

From 2022-06-10, we can evaluate MetaHuman's custom-head import workflow for digital humans instead of treating it as limited to default character presets.

1. Install Unreal Engine with MetaHuman Creator Core Data, then enable the MetaHuman Creator plugin in the project.
  — <https://dev.epicgames.com/documentation/metahuman/getting-started-with-metahuman-creator-in-unreal-engine>
2. Create a MetaHuman Character asset in the Content Browser, edit its face, body, and materials, then assemble it for the intended Unreal target.
  — <https://dev.epicgames.com/documentation/metahuman/metahuman-creator-in-unreal-engine>
3. For a scan or sculpt, import the mesh and create a MetaHuman Identity. Track a neutral pose, run Identity Solve, then auto-rig or conform the result in the in-engine Creator workflow.
  — <https://dev.epicgames.com/documentation/metahuman/from-mesh>
4. If moving an older web-created character forward, use Quixel Bridge’s Migrate or Import and Migrate path rather than continuing to edit it as a legacy web asset.
  — <https://dev.epicgames.com/documentation/metahuman/metahuman-creator-migration-guide-in-unreal-engine>

## Best practices

- Use a textured FBX or OBJ with visible sclera. Choose OBJ for meshes above 200,000 vertices because FBX import can be much slower.
  — <https://dev.epicgames.com/documentation/metahuman/from-mesh>
- Use a frontal neutral pose with clear facial features. Add side frames only to correct poorly fitted ears or nostrils.
  — <https://dev.epicgames.com/documentation/metahuman/from-mesh>
- For restricted networks, allowlist Epic’s texture-synthesis, auto-rigging, and required S3 endpoints before building a production workflow.
  — <https://dev.epicgames.com/documentation/metahuman/getting-started-with-metahuman-creator-in-unreal-engine>

## Superseded by this

- 2022-06-09 — MetaHuman Creator’s Early Access web-app-centered workflow is obsolete for new UE 5.6+ projects. Creator is integrated into Unreal Engine.
- 2025-06-03 — Mesh to MetaHuman no longer creates a new character in the MetaHuman Creator web application. Create the identity and conform it in Unreal Engine instead.

## Still unknown

- The 2022-06-21 YouTube URL could not be fetched or resolved to a title, author, or publication date. Its relationship to the MetaHuman product-development timeline is therefore unverified.

## Sources

| source | title | read |
|---|---|---|
| https://www.fxguide.com/fxfeatured/huge-update-for-metahuman-import-your-own-head/ | Huge update for MetaHuman: import your own head! | 2026-09-05 |
| https://www.metahuman.com/news/new-release-brings-mesh-to-metahuman-to-unreal-engine-and-much-more | New release brings Mesh to MetaHuman to Unreal Engine, and much more! | 2026-09-05 |
| https://www.metahuman.com/news/delivering-high-quality-facial-animation-in-minutes-metahuman-animator-is-now-available?lang=en-US | Delivering high-quality facial animation in minutes, MetaHuman Animator is now available! | 2026-09-05 |
| https://www.metahuman.com/news/metahuman-comes-to-uefn-dynamic-clothing-with-marvelous-designer-and-more | MetaHuman comes to UEFN, dynamic clothing with Marvelous Designer and more | 2026-09-05 |
| https://www.metahuman.com/news/metahuman-leaves-early-access-with-a-feature-packed-new-release | MetaHuman leaves Early Access with a feature-packed new release | 2026-09-05 |
| https://forums.unrealengine.com/t/metahuman-5-8-released/2729288 | MetaHuman 5.8 Released! | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/getting-started-with-metahuman-creator-in-unreal-engine | Getting Started with MetaHuman Creator in Unreal Engine | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/metahuman-creator-in-unreal-engine | MetaHuman Creator in Unreal Engine | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/from-mesh | From Mesh | 2026-09-05 |
| https://dev.epicgames.com/documentation/metahuman/metahuman-creator-migration-guide-in-unreal-engine | MetaHuman Creator Migration Guide in Unreal Engine | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:metahuman`, thread `metahuman-development-and-applications`, 1 dated events 2022-06-10 → 2022-06-10.
- **Practical note:** From 2022-06-10, we can evaluate MetaHuman's custom-head import workflow when planning digital-human creation, rather than treating it as limited to its default character presets.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
