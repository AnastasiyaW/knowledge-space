---
title: NeumaTex
category: projects
date: 2026-07-02
tags: [neumatex, neumatex-development, project]
aliases: ["NeumaTex"]
---

# NeumaTex

**Development line:** `project:neumatex` · thread `neumatex-development`  
**Last event:** 2026-07-02 · 1 dated since 2026-07-02 · **Researched:** 2026-09-05 · confidence: medium

## What it is

NeuMatEx — a research pipeline for graphics and 3D-asset teams that turns a known 3D model plus multi-view images into a relightable neural material rather than PBR texture maps.

- predicts base color, neural-material latents, and uncertainty with the Large Material Reconstruction Model (LMRM)
- refines the result with uncertainty-guided inverse path tracing
- models clearcoat, haze, dust, fuzz, and scattering beyond fixed PBR lobes

## Development line

- **2026-07-02 — NeumaTex project page shared.** LMRM initialization followed by uncertainty-guided inverse rendering, targeting relightable materials whose specular effects would otherwise be baked into PBR base color.

## What changed

2026-07-02 — NeuMatEx was presented as a multi-view neural-material extraction method: LMRM initialization followed by uncertainty-guided inverse rendering, targeting relightable materials whose specular effects would otherwise be baked into PBR base color.

## How to use this

As of 2026-07-02, practitioners should consult the NeumaTex project page before relying on or adopting the project; the sealed link alone does not establish specific capabilities or usage guidance.

1. Assess fit first: the documented method needs a supplied 3D model and a set of multi-view images, not one casual image.
  — <https://nvlabs.github.io/neumatex/>
2. For a research reimplementation, reproduce the two stages: predict base color, neural latents, and uncertainty with LMRM; then refine with uncertainty-guided Monte-Carlo inverse rendering.
  — <https://arxiv.org/abs/2606.26715>
3. Do not plan an ordinary install or inference run yet: the official project page currently links the paper, supplementary PDF, video, and BibTeX, but no source repository or model download.
  — <https://nvlabs.github.io/neumatex/>

## Best practices

- Use calibrated multi-view observations and known geometry, poses, and lighting where possible; the paper notes inverse-rendering recovery is sensitive to ambiguous or poorly calibrated data.
  — <https://arxiv.org/abs/2606.26715>
- Keep the uncertainty-guided test-time optimization stage; the reported ablation shows it improves material decomposition over feed-forward initialization alone and reduces baked-in lighting.
  — <https://arxiv.org/abs/2606.26715>
- Check relighting results and inspect real-world, out-of-domain materials for residual specular artifacts, especially red tinting and artifacts in crevices.
  — <https://arxiv.org/abs/2606.26715>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No public source repository, checkpoint, license, hardware requirement, or reproducible runtime procedure was found on the official project page reviewed on 2026-09-05.
- The 2026-07-02 report said source code was not yet published; availability outside the sources checked here is unverified.
- The supplied display spelling is “NeumaTex”; the official project and arXiv title use “NeuMatEx.”
- event_findings: [{"event_date":"2026-07-02","finding":"The linked work’s official name is NeuMatEx, short for the paper Extracting Neural Materials from Multi-view Images; it is arXiv:2606.26715 by Kim Youwang, Jon Hasselgren, Peter Kocsis, Andrea Weidlich, Tae-Hyun Oh, and Jacob Munkberg. The method requires a 3D model plus multi-view images, rather than being a single-image texture generator.","source_date":"2026-06-25","source_url":"https://arxiv.org/abs/2606.26715"},{"event_date":"2026-07-02","finding":"A contemporaneous report adds the practical release boundary: source code had not been published, so the announcement did not make a runnable public package available.","source_date":"2026-07-02","source_url":"https://nnets.ru/news/nvidia-predstavila-neumatex-novyj-metod-3d-tekstur-po-foto"}]
- new_events: [{"date":"2026-06-25","finding":"The arXiv v1 preprint was posted, establishing the research method before its 2 July coverage: LMRM initialization plus uncertainty-guided inverse rendering for neural materials.","source_date":"2026-06-25","source_url":"https://arxiv.org/abs/2606.26715"}]

## Sources

| source | title | read |
|---|---|---|
| https://nvlabs.github.io/neumatex/ | Extracting Neural Materials from Multi-view Images | 2026-09-05 |
| https://arxiv.org/abs/2606.26715 | Extracting Neural Materials from Multi-view Images | 2026-09-05 |
| https://nnets.ru/news/nvidia-predstavila-neumatex-novyj-metod-3d-tekstur-po-foto | NVIDIA представила NeumaTex: новый метод 3D-текстур по фото. | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:neumatex`, thread `neumatex-development`, 1 dated events 2026-07-02 → 2026-07-02.
- **Practical note:** As of 2026-07-02, practitioners should consult the NeumaTex project page before relying on or adopting the project; the sealed link alone does not establish specific capabilities or usage guidance.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
