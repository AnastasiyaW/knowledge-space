---
title: FlashMemory-Deepseek-V4 — DeepSeek Optimizations
category: projects
date: 2026-06-15
tags: [deepseek-optimizations, deepseek_optimizations, flashmemory-deepseek-v4, project]
aliases: ["FlashMemory-Deepseek-V4"]
---

# FlashMemory-Deepseek-V4 — DeepSeek Optimizations

**Development line:** `project:flashmemory-deepseek-v4` · thread `deepseek-optimizations`  
**Last event:** 2026-06-15 · 1 dated since 2026-06-15 · **Researched:** 2026-11-21 · confidence: medium

## What it is

FlashMemory-DeepSeek-V4 is an MIT-licensed learned retriever that picks the KV-cache chunks DeepSeek-V4 sparse attention needs next, keeping them on GPU.

- Scope: a modified sglang serving fork, launch scripts (prefill, decode, router), data-generation tools and training code, plus the retriever weights on Hugging Face.
- Users: operators serving long-context DeepSeek-V4 who are limited by GPU memory or concurrency.
- Key capability: at 1M context the paper reports GPU KV cache down 90% (3.73 to 0.37 GB) and 2.8× aggregate throughput on 8 × H20.
- Limits: needs a DeepSeek-V4 checkpoint and the forked sglang; all benchmark figures are self-reported; at 1M context, concurrency is capped by host DRAM.

## Development line

- **2026-06-15 — FlashMemory-Deepseek-V4 linked to GitHub and Hugging Face.** On 2026-06-15, FlashMemory-Deepseek-V4 was linked to a GitHub repository and a Hugging Face page. Public sources do not establish release contents, capabilities, or changes from an earlier version.

## What changed

- 2026-06-07 — Hugging Face model repository created (Hugging Face API, `createdAt`).
- 2026-06-08 — arXiv:2606.09079 v1 submitted, titled "FlashMemory-DeepSeek-V4: Lightning Index Ultra-Long Context via Lookahead Sparse Attention"; v3 posted 2026-07-20.
- 2026-07-17 — repository cleanup: single offload path, refreshed sglang fork, training and data tools added; performance and architecture figures added to the README.
- 2026-07-18 — README gained the arXiv link; the Hugging Face repository was last modified the same day.
- The repository has no releases; 14 commits at capture, the latest dated 2026-07-18.

## How to use this

1. Read arXiv:2606.09079 for the method (a Neural Memory Indexer trained apart from the backbone) and the LongBench-v2, LongMemEval and RULER setup.
  — <https://arxiv.org/abs/2606.09079>
2. Obtain a DeepSeek-V4 checkpoint and the retriever weights from Hugging Face (default `top3_R930_joint.pt`).
  — <https://github.com/libertywing/FlashMemory-Deepseek-V4>
3. Install the bundled sglang fork with `pip install -e sglang/python` and `sgl_kernel==0.3.21`.
  — <https://github.com/libertywing/FlashMemory-Deepseek-V4>
4. Launch the prefill, decode and router setup with the included scripts; the reference benchmarks ran on 8 × H20 with TP8.
  — <https://github.com/libertywing/FlashMemory-Deepseek-V4>
5. Tune KMAX on your workload: higher values give fuller recall and lower throughput.
  — <https://github.com/libertywing/FlashMemory-Deepseek-V4>

## Best practices

- Benchmark accuracy on your own long-context task before adoption; the reported accuracy figures are the authors' own.
  — <https://github.com/libertywing/FlashMemory-Deepseek-V4>
- Compare against the README's ablations (recency-only and random selection at the same KV budget) to confirm the learned retriever helps on your data.
  — <https://github.com/libertywing/FlashMemory-Deepseek-V4>
- Pin the repository commit: the 2026-07-17 cleanup changed the offload path and sglang version.
  — <https://api.github.com/repos/libertywing/FlashMemory-Deepseek-V4/commits?per_page=3>

## Superseded by this

- The native Lightning Indexer is superseded by the learned retriever when this path is enabled, according to the README.

## Still unknown

- Minimum hardware: the README gives only the 8 × H20 reference configuration.
- Several optimizations are environment-gated; the full list of gates was not captured.
- Independent reproduction of the benchmarks: none found; the repository has one open issue at capture.
- Throughput headline differs: the README headline says 2.7× at 1M context; its table and the paper say 2.8× aggregate throughput.
- The Hugging Face model card's license and tags were read through the API only.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/libertywing/FlashMemory-Deepseek-V4 | Repository README and overview | 2026-11-21 |
| https://arxiv.org/abs/2606.09079 | FlashMemory-DeepSeek-V4: Lightning Index Ultra-Long Context via Lookahead Sparse Attention | 2026-11-21 |
| https://huggingface.co/api/models/libertywing/FlashMemory-Deepseek-V4 | Hugging Face API: model dates and license | 2026-11-21 |
| https://api.github.com/repos/libertywing/FlashMemory-Deepseek-V4/commits?per_page=3 | GitHub REST API: recent commit dates | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:flashmemory-deepseek-v4`, thread `deepseek-optimizations`, 1 dated event 2026-06-15; paper 2026-06-08 (v3 2026-07-20); repository commits to 2026-07-18.
- **Practical note:** Needs a DeepSeek-V4 checkpoint and the bundled sglang fork; benchmark on your own workload; pin the commit.
- **Confidence:** medium. Paper and README are primary but the benchmarks are self-reported and unreproduced. Dated supersedes above are the authority for what is obsolete.
