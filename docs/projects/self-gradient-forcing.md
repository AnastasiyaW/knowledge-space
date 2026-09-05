---
title: Self Gradient Forcing
category: projects
date: 2026-07-24
tags: [project, self-gradient-forcing, self-gradient-forcing-development, self_gradient_forcing]
aliases: ["Self Gradient Forcing"]
---

# Self Gradient Forcing

**Development line:** `project:self-gradient-forcing` · thread `self-gradient-forcing-development`  
**Last event:** 2026-07-24 · 1 dated since 2026-07-24 · **Researched:** 2026-09-05 · confidence: high

## What it is

Self Gradient Forcing (SGF) is a training method for autoregressive video diffusion. It replays sampled self-generated context so future-frame losses can train causal KV memory without retaining gradients through the entire rollout. The project ships code and checkpoints on Wan2.1 T2V 1.3B and 14B foundations, with framewise and chunkwise settings. The reported training window is 5 seconds; demonstrations and evaluation extend to 60 and 240 seconds. Use it as a research implementation for long-horizon video extrapolation, not as a drop-in hosted video generator.

## Development line

- **2026-07-24 — Self Gradient Forcing project resources were linked.** On 2026-07-24, links connected the project page, source repository, and Hugging Face model page. These links make the project overview, implementation location, and hosted model resource discoverable together. They do not establish whether this was an initial release, a versioned update, or another specific technical milestone.

## What changed

- 2026-07-22 — The paper introduced SGF's bounded two-pass reconstruction to address the context-gradient gap in frozen-cache Self Forcing.
- 2026-07-23 — The authors publicly released the paper, inference and training code, and model checkpoints.
- 2026-07-24 — The linked project, repository, and model collection made the release discoverable; the official material specifies both framewise and chunkwise releases rather than one generic checkpoint.

## How to use this

As of 2026-07-24, practitioners could use the linked project page, GitHub repository, and Hugging Face page to locate Self Gradient Forcing's public overview, implementation, and model resource.

1. Create a Python 3.10 environment, install the repository requirements and FlashAttention, then install the project in development mode.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
2. Run scripts/download_weights.sh; it retrieves Wan2.1 T2V 1.3B/14B bases, Causal-Forcing initializations, SGF checkpoints, and prompts.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
3. Choose the matching release mode and run bash scripts/infer_self_gradient_forcing.sh framewise or chunkwise; use the matching configuration and checkpoint.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
4. For training or adaptation, launch the corresponding framewise or chunkwise training script and preserve the rollout/reconstruction split defined by SGF.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>

## Best practices

- Evaluate long-horizon behavior separately from short clips: the paper treats 5-second VBench as a sanity check and focuses the main comparison on 60- and 240-second extrapolation, where memory errors accumulate.
  — <https://arxiv.org/abs/2607.20368>
- Keep the release setting, configuration, and checkpoint aligned: framewise and chunkwise variants use different cache geometries and are not interchangeable.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>
- Use EMA weights for released or trained checkpoints unless deliberately comparing raw generator weights.
  — <https://github.com/zhuang2002/Self_Gradient_Forcing>

## Superseded by this

- 2026-07-22 — Frozen-cache Self Forcing is superseded by SGF only for the missing context-gradient path: SGF preserves the no-gradient serial rollout but reconstructs the sampled computation so future losses train memory writing. This is not a general deprecation of all Self Forcing workflows.

## Still unknown

- No independently reproduced quality, compute-cost, or compatibility result was found in the reviewed first-party materials; reported long-horizon gains remain author-reported.
- The release material does not establish a stable production support policy or a maintained inference service.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2607.20368 | Self Gradient Forcing: Native Long Video Extrapolation | 2026-09-05 |
| https://github.com/zhuang2002/Self_Gradient_Forcing | zhuang2002/Self_Gradient_Forcing | 2026-09-05 |
| https://huggingface.co/JunhaoZhuang/Self_Gradient_Forcing | JunhaoZhuang/Self_Gradient_Forcing | 2026-09-05 |
| https://zhuang2002.github.io/SelfGradientForcing/ | Self Gradient Forcing: Native Long Video Extrapolation project page | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:self-gradient-forcing`, thread `self-gradient-forcing-development`, 1 dated events 2026-07-24 → 2026-07-24.
- **Practical note:** As of 2026-07-24, practitioners could use the linked project page, GitHub repository, and Hugging Face page to locate Self Gradient Forcing's public overview, implementation, and model resource.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.