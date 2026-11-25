---
title: EgoForce
category: projects
date: 2026-07-14
tags: [egoforce, egoforce-development, project]
aliases: ["EgoForce"]
---

# EgoForce

**Development line:** `project:egoforce` · thread `egoforce-development`  
**Last event:** 2026-07-14 · 1 dated since 2026-07-14 · **Researched:** 2026-09-05 · confidence: high

## What it is

EgoForce estimates absolute camera-space 3D hand pose and mesh from one egocentric RGB camera.

- Camera support: works with fisheye, perspective, and distorted wide-FOV cameras.
- Bundled assets: includes weights, datasets, and a Gradio/Project Aria demo.
- Benchmark: reports up to 28% lower camera-space MPJPE on HOT3D.

It is research code for calibrated egocentric capture, not a general commercial hand-tracking SDK.

## Development line

- **2026-07-14 — EgoForce public project resources were linked.** On 2026-07-14, the EgoForce development line linked a project page, a source repository, a Hugging Face model page, and a Hugging Face Space. Together, the dated links establish a public entry point for project information, code, model artifacts, and an interactive surface. They make no claims about a specific version, capabilities, benchmarks, or release status.

## What changed

- **2026-05-12** — The DFKI/MPII paper introduced the forearm-guided, ray-space approach.
- **2026-07-14** — The project’s code, model assets, dataset and browser demo were available together.
- **2026-08-09** — An open report documented a left-hand tracking failure on a named HOT3D sequence; no verified fix was found.

## How to use this

As of 2026-07-14, use the linked project page, repository, model page, and Space as the starting points to evaluate or reproduce EgoForce, while verifying their current contents and terms before relying on them.

1. Create the documented Python 3.10 Conda environment and run the repository installer.
  — <https://github.com/dfki-av/EgoForce/tree/main>
2. Download model weights and required assets, then set the dataset root in settings.py.
  — <https://github.com/dfki-av/EgoForce/tree/main>
3. Run experiments/save_predictions.py for a supported dataset, then evaluate the saved prediction file with the matching flags.
  — <https://github.com/dfki-av/EgoForce/tree/main>
4. For a quick visual test, upload a video to the hosted demo or run the repository’s Gradio app locally.
  — <https://huggingface.co/spaces/chris10/EgoForce>

## Best practices

- Treat it as non-commercial research software: the code and weights are CC-BY-NC 4.0, while bundled WiLoR and MANO assets have their own licenses.
  — <https://huggingface.co/chris10/EgoForce>
- Validate camera intrinsics and use the matching prediction/evaluation flags; the authors document an intrinsics-noise sweep and variant-specific output suffixes.
  — <https://github.com/dfki-av/EgoForce/tree/main>
- Test both hands on target sequences before relying on the system: a left-hand HOT3D failure remains open in the public issue tracker.
  — <https://github.com/dfki-av/EgoForce/issues>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- A different May 2026 paper is also named EgoForce, but it is a separate diffusion-based full-body motion-reconstruction project by different authors; the supplied URLs identify the DFKI hand-pose project.
- No dated release note was found that independently confirms why the code, model, data and demo links were grouped on 2026-07-14.
- The open left-hand HOT3D issue establishes a reported failure, not its prevalence or a confirmed fix.

## Sources

| source | title | read |
|---|---|---|
| https://dfki-av.github.io/EgoForce/ | EgoForce project page | 2026-09-05 |
| https://github.com/dfki-av/EgoForce/tree/main | dfki-av/EgoForce official implementation | 2026-09-05 |
| https://huggingface.co/chris10/EgoForce | chris10/EgoForce model repository | 2026-09-05 |
| https://huggingface.co/spaces/chris10/EgoForce | chris10/EgoForce demo | 2026-09-05 |
| https://arxiv.org/abs/2605.12498 | EgoForce: Forearm-Guided Camera-Space 3D Hand Pose from a Monocular Egocentric Camera | 2026-09-05 |
| https://github.com/dfki-av/EgoForce/issues | EgoForce issue tracker | 2026-09-05 |
| https://arxiv.org/abs/2605.13041 | EgoForce: Robust Online Egocentric Motion Reconstruction via Diffusion Forcing | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:egoforce`, thread `egoforce-development`, 1 dated events 2026-07-14 → 2026-07-14.
- **Practical note:** As of 2026-07-14, practitioners should use the linked project page, repository, model page, and Space as the starting points to evaluate or reproduce EgoForce, while verifying their current contents and terms before relying on them.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
