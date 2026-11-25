---
title: Context-Matched Distillation
category: projects
date: 2026-08-21
tags: [context-matched-distillation, nvidia-cmd, nvidia-cosmos, project]
aliases: ["Context-Matched Distillation"]
---

# Context-Matched Distillation

**Development line:** `project:nvidia-cmd` · thread `context-matched-distillation`  
**Last event:** 2026-08-21 · 1 dated since 2026-08-21 · **Researched:** 2026-09-05 · confidence: high

## What it is

Context-Matched Distillation (CMD) is NVIDIA’s causal distribution-matching distillation method and checkpoint release for autoregressive image-to-video generation.

- Chunk-1 or chunk-4 generation.
- Long rollouts.
- Camera-conditioned variants.

The released CMD code and derivatives are non-commercial research and education only. The underlying Cosmos base model also requires access approval. Use it to evaluate interactive causal image-to-video research, not as a drop-in commercial video stack.

## Development line

- **2026-08-21 — Context-Matched Distillation resources published.** On 2026-08-21, NVIDIA published the Context-Matched Distillation (CMD) project page, code repository, model page, and image-to-video demo. These links opened the project to public inspection.

## What changed

- 2026-08-13 — CMD paper introduced causal teacher scoring, Prefix Scoring, and Prefix Corruption for few-step autoregressive video distillation.
- 2026-08-19 — The Hugging Face CMD repository was created.
- 2026-08-21 — CMD was documented with its project page, code repository, model repository, and an image-to-video demo link.
- 2026-08-23 — NVIDIA added the CMD model card and checkpoints, covering short, long, and camera-conditioned chunk-1/chunk-4 variants.
- 2026-08-24 — NVIDIA updated the model card with the arXiv citation.
- 2026-08-30 — The model repository added config.json.

## How to use this

As of 2026-08-21, evaluate CMD by examining the linked code, model page, documentation, and demo together.

1. Request access to the Cosmos-Predict2.5 2B base model before running CMD.
  — <https://huggingface.co/nvidia/Cosmos-Predict2.5-2B>
2. Clone CMD, create the Python 3.10 conda environment, install requirements and FlashAttention, then install the package in development mode.
  — <https://github.com/nv-tlabs/cmd>
3. Download all CMD checkpoints, or download only the checkpoint needed for a chosen variant.
  — <https://huggingface.co/nvidia/cmd>
4. Match the checkpoint to its supplied configuration, image, prompt, block size, local-attention window, and requested output-frame count; the repository gives a chunk-4 short-video invocation.
  — <https://github.com/nv-tlabs/cmd>
5. Run the supplied example runner for one of the short, long, or camera-conditioned variants before replacing the example inputs.
  — <https://github.com/nv-tlabs/cmd>

## Best practices

- Treat checkpoint and configuration pairing as an invariant: t denotes frame duration and l denotes local-attention length, while chunk-1 and chunk-4 use different generation granularity.
  — <https://huggingface.co/nvidia/cmd>
- Evaluate long rollouts on representative inputs: autoregressive errors accumulate, degrading temporal consistency, fine detail, faces, hands, text, and fast motion.
  — <https://huggingface.co/nvidia/cmd>
- Do not expect the public DL3DV setup to reproduce reported quality; it is only an end-to-end pipeline check, while the reported training data is not released.
  — <https://github.com/nv-tlabs/cmd>
- Keep CMD use and derivatives non-commercial unless licensing changes; redistribution must retain the license and notices.
  — <https://github.com/nv-tlabs/cmd/blob/main/LICENSE>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The Hugging Face commit history dates the initial CMD repository to 2026-08-19 and the checkpoint and model-card upload to 2026-08-23, while the 2026-08-21 event already carried the model URL. The link list may have been enriched after the dated event; this cannot be resolved from the available first-party history.
- The public demo page was reachable as a Hugging Face Space but exposed no reproducible runtime settings or availability guarantee.
- No first-party post-release benchmark or production-deployment evidence was found; paper results remain research evidence rather than a production SLA.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2608.13391 | Context-Matched Distillation: Teacher Causality for Autoregressive Video Distillation | 2026-09-05 |
| https://hmrishavbandy.github.io/cmd-site/ | Context-Matched Distillation project page | 2026-09-05 |
| https://github.com/nv-tlabs/cmd | nv-tlabs/cmd | 2026-09-05 |
| https://huggingface.co/nvidia/cmd | nvidia/cmd model card | 2026-09-05 |
| https://huggingface.co/nvidia/cmd/commits/main | nvidia/cmd commit history | 2026-09-05 |
| https://huggingface.co/spaces/hugging-apps/cmd-i2v-demo | NVIDIA CMD Image to Video demo | 2026-09-05 |
| https://huggingface.co/nvidia/Cosmos-Predict2.5-2B | Cosmos-Predict2.5-2B model card | 2026-09-05 |
| https://github.com/nv-tlabs/cmd/blob/main/LICENSE | NVIDIA OneWay Noncommercial License | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:nvidia-cmd`, thread `context-matched-distillation`, 1 dated events 2026-08-21 → 2026-08-21.
- **Practical note:** As of 2026-08-21, practitioners evaluating CMD should consult the linked code repository, model page, project documentation, and image-to-video demo together rather than treating the announcement as an unsupported research reference.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
