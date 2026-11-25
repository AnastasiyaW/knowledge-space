---
title: DIRECT
category: projects
date: 2026-06-09
tags: [direct, direct-development, project]
aliases: ["DIRECT"]
---

# DIRECT

**Development line:** `project:direct` · thread `direct-development`  
**Last event:** 2026-06-09 · 1 dated since 2026-06-09 · **Researched:** 2026-09-06 · confidence: medium

## What it is

DIRECT is a pose-controllable object-insertion system for compositors placing a reference object into a background.

- Reference appearance: preserves reference appearance.
- 3D proxy: uses a reconstructed 3D proxy for pose.
- Scene context: conditions on scene context.

Its initial weight package is 987 MB but needs external FLUX, TRELLIS, SigLIP2 and RMBG components. Use it as a local GPU-backed compositing workflow, not a standalone hosted model.

## Development line

- **2026-06-09 — DIRECT project resources were linked.** On 2026-06-09, a DIRECT development-line message linked the project website, source repository, and Hugging Face page. Taken together, those dated links indicate a public-facing project milestone suitable for the development history. We did not review the announcement text or the exact status of each linked resource.

## What changed

- **2026-05** — DIRECT was accepted to ICML 2026; its repository and project page became available.
- **2026-06-04** — DIRECT paper v1 appeared on arXiv, defining the reference-object, 3D-proxy and background workflow.
- **2026-06-09** — superGong published the initial DIRECT Image-to-Image model.
- **2026-06-30** — author activity recorded publication and update of DIRECT-dataset.
- **2026-07** — the repository says training data, training code and preprocessing code were released; it gives no day.

## How to use this

1. Clone the repository, create the tested Python 3.10.18 environment, install PyTorch 2.4.0 with CUDA 11.8, then install requirements and DIRECT.
  — <https://github.com/Gong1130/DIRECT>
2. Before the first run, accept the gated FLUX.1-Fill-dev and RMBG-2.0 licenses, then authenticate with Hugging Face or set HF_TOKEN so the required models can download.
  — <https://github.com/Gong1130/DIRECT>
3. Run `python demo/demo.py --gradio_port 7860 --viser_port 8081`; the interface segments and reconstructs the reference object, then lets you manipulate its 3D pose in the background.
  — <https://huggingface.co/superGong/DIRECT>
4. On a remote machine, forward both ports 7860 and 8081 before opening the local Gradio interface.
  — <https://github.com/Gong1130/DIRECT>

## Best practices

- Use the authors' tested Python 3.10.18, PyTorch 2.4.0 and CUDA 11.8 stack; set CUDA_HOME if compiled extensions cannot find the toolkit.
  — <https://github.com/Gong1130/DIRECT>
- Budget for the full dependency stack: the 987 MB DIRECT package is only its own weights, not the required FLUX, TRELLIS, SigLIP2 and background-removal models.
  — <https://huggingface.co/superGong/DIRECT>
- Check commercial-use terms before deployment: the repository license permits non-commercial use and directs commercial users to contact the contributors.
  — <https://github.com/Gong1130/DIRECT/blob/main/LICENSE.txt>

## Superseded by this

- 2026-07: the June-only assumption that DIRECT had only inference code, a demo and weights is obsolete; the repository says training data, training code and preprocessing code were released.

## Still unknown

- The repository's July release note has no exact day, so that release cannot be emitted as a timestamped new event.
- The README still contains TODO bullets for assets that its dated News section says were released; no immutable release tag cleanly resolves that inconsistency.
- We found no independent current benchmark or local end-to-end run; performance claims remain author-reported.
- Chinese coverage found is a method summary, not an independent Chinese setup guide, failure report or benchmark.

## Sources

| source | title | read |
|---|---|---|
| https://gong1130.github.io/DIRECT/ | DIRECT project page | 2026-09-07 |
| https://github.com/Gong1130/DIRECT | Gong1130/DIRECT repository and release notes | 2026-09-07 |
| https://huggingface.co/superGong/DIRECT | superGong/DIRECT model card | 2026-09-07 |
| https://huggingface.co/superGong/activity/all | superGong Hugging Face activity | 2026-09-07 |
| https://huggingface.co/superGong/DIRECT/tree/2ec64cedd13ed7f2f81edf836ce6a90d503c3683 | DIRECT initial model revision | 2026-09-07 |
| https://arxiv.org/abs/2606.06601 | DIRECT arXiv paper | 2026-09-07 |
| https://github.com/Gong1130/DIRECT/blob/main/LICENSE.txt | DIRECT license | 2026-09-07 |
| https://hyper.ai/cn/papers/2606.06601 | Simplified-Chinese DIRECT method summary | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:direct`, thread `direct-development`, 1 dated events 2026-06-09 → 2026-06-09.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
