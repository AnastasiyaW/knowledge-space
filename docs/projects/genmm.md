---
title: GenMM — GenMM development
category: projects
tags: [genmm, genmm-development, project]
aliases: ["GenMM"]
---

# GenMM — GenMM development

**Development line:** `project:genmm` · thread `genmm-development`  
**Events:** 1 dated, 2023-06-02 → 2023-06-02 · **Researched:** 2026-09-04 · confidence: medium

## What it is

GenMM — a SIGGRAPH 2023 research codebase for technical animators who need new skeletal-motion sequences from one or a few example clips, not a text-to-motion model. - Synthesizes diverse variants, completes motion, follows keyframe poses, creates loops, reassembles motion across heterogeneous skeletons, and changes locomotion trajectories. - The documented local stack is Python 3.8, PyTorch 1.12.1 and CUDA 11.3; the authors report about 0.05 s per motion on a Tesla V100 and 0.2 s on an Apple M1. Verdict: use it through the pinned research stack or the Blender add-on pre-release; modern Python, CUDA and Blender compatibility is unverified.

## Development line

- **2023-06-02 — GenMM public project materials linked.** On 2023-06-02, the GenMM development line was publicly represented by a project page, source repository, and demo link. This is a material public milestone because it made the project and its evaluation entry points available, although the unavailable source text does not establish the exact release claim or technical details.

## What changed

2023-06-02 — GenMM was available through a project page, source repository and browser demo as an example-based, training-free motion-synthesis system. The page documents motion completion, keyframe guidance, looping, reassembly and locomotion. 2023-07-13 — the entry provides only the existing browser-demo endpoint. It identifies no new model, package version or feature, so this is not a confirmed software release. Found today (2026-09-04) — the original GitHub URL redirects to liyuuuu98/GenMM; the current releases page exposes a single Blender add-on pre-release, v0.0.1. The retrieved release page gives only "29 Jul 12:48", not a year, so no full release date is assigned.

## How to use this

From 2023-06-02, practitioners could use the public GenMM project page, source repository, and demo as the entry points for evaluation; the 2023-07-13 demo link alone does not establish a further practical change.

1. Clone the repository and reproduce its documented environment: Python 3.8, PyTorch 1.12.1, CUDA 11.3, docker/requirements.txt and torch-scatter==2.1.1.
  — <https://github.com/wyysf-98/GenMM>
2. Provide a BVH motion clip and run python run_random_generation.py -i <clip.bvh>; use run_random_generation.py for further synthesis configuration.
  — <https://github.com/wyysf-98/GenMM>
3. For Blender, install the listed Python packages into Blender's bundled Python, install the add-on ZIP through Preferences > Add-ons > Install, then select an armature and open the GenMM panel.
  — <https://github.com/wyysf-98/GenMM>
4. For the web demo, select an example with Next, use Generate and Controls, then set frames, noise_sigma, loop, patch_size, coarse_ratio, pyr_factor and optimisation steps.
  — <https://github.com/wyysf-98/GenMM_demo>
5. If the shared demo waits indefinitely, duplicate its Hugging Face Space, obtain your own API URL and replace api_url in Controls.
  — <https://github.com/wyysf-98/GenMM_demo>

## Best practices

- Pin or containerize the documented Python, PyTorch and CUDA versions before changing dependencies; the official instructions do not provide a newer compatibility matrix.
  — <https://github.com/wyysf-98/GenMM>
- Validate final motion in a rig-aware workflow, not only in the browser viewer: the project page warns that its Three.js FBX parser has no foot-contact fix and may create artifacts.
  — <https://weiyuli.xyz/GenMM/>
- When the shared demo is slow, use a duplicated Space with your own API URL rather than repeatedly retrying the CPU-backed shared endpoint.
  — <https://github.com/wyysf-98/GenMM_demo>

## Superseded by this

- 2023-06-02 — the README's in-progress release checklist is obsolete as an availability statement: the repository now contains the local runner and GitHub lists the Blender add-on v0.0.1 pre-release.
- 2023-07-13 — a browser-demo-only workflow is obsolete for repeated work: first-party documentation now provides a copied-Space/private-api recovery path and warns of viewer artifacts and shared-CPU stalls.

## Still unknown

- No first-party source read today provides a 2026-tested Python, PyTorch, CUDA or Blender compatibility matrix.
- The 2023-07-13 entry supplies only the existing demo URL; without its source text, no separate capability or version can be attributed to that date.
- The current release page displays v0.0.1 as a pre-release and gives 29 Jul 12:48, but the retrieved view does not expose the year.
- The browser demo requires JavaScript; live end-to-end generation was not verified in this research.

## Sources

| source | title | read |
|---|---|---|
| https://weiyuli.xyz/GenMM/ | Example-based Motion Synthesis via Generative Motion Matching | 2026-09-04 |
| https://github.com/wyysf-98/GenMM | GitHub — liyuuuu98/GenMM | 2026-09-04 |
| https://weiyuli.xyz/GenMM_demo/ | patch-based_motion_synthesis | 2026-09-04 |
| https://github.com/wyysf-98/GenMM_demo | GitHub — liyuuuu98/GenMM_demo | 2026-09-04 |
| https://github.com/wyysf-98/GenMM/releases | GitHub — GenMM releases | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:genmm`, thread `genmm-development`, 1 dated events 2023-06-02 → 2023-06-02.
- **Practical note:** From 2023-06-02, practitioners could use the public GenMM project page, source repository, and demo as the entry points for evaluation; the 2023-07-13 demo link alone does not establish a further practical change.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
