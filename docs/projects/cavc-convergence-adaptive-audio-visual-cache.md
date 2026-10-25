---
title: "Cavc Convergence Adaptive Audio Visual Cache: cavc-audio-visual-diffusion-caching — Cavc Audio Visual Diffusion Caching"
category: "projects"
date: 2026-10-23
tags: ["cavc-audio-visual-diffusion-caching", "cavc-convergence-adaptive-audio-visual-cache", "project"]
aliases: ["Cavc Convergence Adaptive Audio Visual Cache: cavc-audio-visual-diffusion-caching"]
---

# Cavc Convergence Adaptive Audio Visual Cache: cavc-audio-visual-diffusion-caching — Cavc Audio Visual Diffusion Caching

**Development line:** project:cavc-convergence-adaptive-audio-visual-cache · thread cavc-audio-visual-diffusion-caching  
**Last event:** 2026-10-23 · 2 dated since 2026-10-23 · **Researched:** 2026-10-25 · confidence: medium

## What it is

CAVC (Convergence-Adaptive Audio-Visual Cache) is a training-free caching framework for diffusion models that generate audio and video together. It speeds up joint sampling by caching the audio denoiser's outputs. Video keeps its full, uncompressed refinement.

- Cache-tolerant regime detection: finds the intermediate sampling steps where audio denoising and cross-modal attention can be skipped.
- Continuous video denoising: the video denoiser runs through the whole sampling trajectory, so motion and temporal quality do not degrade.
- Terminal joint steps: joint audio-video denoising comes back at the end to remove cross-modal drift and restore sync.

1.10x to 1.35x wall-clock speedup on standard benchmarks, with no retraining. The gain depends on how many intermediate steps are marked cache-tolerant.

It works as a drop-in speedup for joint audio-visual diffusion models where audio can drift in the middle steps but video needs full temporal computation.

## Development line

- **2026-10-23 — CAVC audio-visual diffusion caching framework announced on arXiv.** On 2026-10-23 an arXiv preprint (2610.30854) introduced CAVC, a training-free, modality-asymmetric caching method for audio-visual diffusion generation. It caches audio denoiser outputs in the middle of sampling and keeps refining video. Joint steps return at the end. The paper reports 1.10-1.35x wall-clock acceleration with competitive audio fidelity and alignment.
- **2026-10-23 — CAVC: training-free modality-asymmetric caching for audio-visual diffusion generation.** The preprint, published 2026-10-23, caches and reuses the audio denoiser output in the middle sampling stage while video denoising keeps refining. A few joint denoising steps come back at the end. The authors report 1.10–1.35x wall-clock acceleration on several public benchmarks, with competitive audio fidelity and audio-visual alignment.
- **2026-10-23 — other reporting on this date.**
  - The preprint describes the modality-asymmetric recoverability mechanism and the sandwich-structured compute schedule. According to the paper, audio drift from intermediate caching can be fixed by the terminal joint steps, while caching the video denoiser leaves permanent spatio-temporal artifacts. (2026-10-23) — <https://arxiv.org/abs/2610.30854>
  - The paper compares CAVC with standard joint sampling across public audio-visual diffusion models. It reports 1.10x to 1.35x faster wall-clock inference with competitive audio fidelity and AV sync metrics. (2026-10-23) — <https://arxiv.org/abs/2610.30854>

## What changed

Earlier joint audio-visual diffusion pipelines ran full joint denoising for both audio and video latents at every timestep. Cross-modal attention became a significant compute bottleneck. CAVC reorganises this into a sandwich-style schedule based on modality-asymmetric recoverability. Intermediate audio denoising is skipped, video keeps its full trajectory, and joint refinement returns for the final sampling steps.

## How to use this

1. Find the cache-tolerant regime in the model's sampling trajectory. It usually falls in the intermediate diffusion timesteps.
  — <https://arxiv.org/abs/2610.30854>
2. In the intermediate phase, cache and reuse the audio denoiser outputs and skip cross-modal attention. Keep the video denoiser running in full, without caching.
  — <https://arxiv.org/abs/2610.30854>
3. For the final steps, restore full joint denoising across both modalities. This removes cross-modal drift and locks audio-visual sync.
  — <https://arxiv.org/abs/2610.30854>

## Best practices

- Do not cache video denoiser outputs across intermediate steps. Video lacks the asymmetric recoverability of audio, so it gets temporal blur and motion degradation that cannot be recovered.
  — <https://arxiv.org/abs/2610.30854>
- Keep a large enough window of joint denoising steps at the end of sampling, so audio fidelity and precise timing against the video are guaranteed.
  — <https://arxiv.org/abs/2610.30854>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- An official open-source repository and specific script integration paths have not been verified in public code repositories.
- Exact tuning thresholds for finding the cache-tolerant regime in different audio-visual diffusion architectures still depend on empirical testing.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2610.30854 | CAVC: Convergence-Adaptive Audio-Visual Cache for Diffusion Generation | 2026-10-25 |

## Agent brief {#agent-brief}

- **Subject:** project:cavc-convergence-adaptive-audio-visual-cache, thread cavc-audio-visual-diffusion-caching, 2 dated events 2026-10-23 → 2026-10-23.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
