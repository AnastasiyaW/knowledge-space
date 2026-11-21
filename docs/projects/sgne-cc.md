---
title: "Sgne Cc: sgne-cc-weight-geometry-edit — Sgne Cc Weight Geometry Edit"
category: "projects"
date: 2026-11-20
tags: ["project", "sgne-cc", "sgne-cc-weight-geometry-edit"]
aliases: ["Sgne Cc: sgne-cc-weight-geometry-edit"]
---

# Sgne Cc: sgne-cc-weight-geometry-edit — Sgne Cc Weight Geometry Edit

SGNE-CC is a training-free weight edit that stops reasoning loops in small open-weights models, for developers without fine-tuning setups.

**Development line:** project:sgne-cc · thread sgne-cc-weight-geometry-edit  
**Last event:** 2026-11-20 · 1 dated since 2026-11-20 · **Researched:** 2026-11-21 · confidence: medium

## What it is

SGNE-CC is a training-free weight-space edit for small open-weights reasoning models. It is for developers who deploy them without fine-tuning infrastructure. It is an alternative to presence-penalty heuristics and to costly reinforcement learning fine-tuning of compact reasoning models.

What it does:

- Rotates targeted MLP down-projection columns along spherical coordinates.
- Keeps the Euclidean column norms of the modified weight tensors.
- Removes repetitive self-verification loops inside reasoning traces.
- Works directly under deterministic greedy decoding.

It changes about 0.0177% of model parameters through a 603 KB patch. Norm deviation stays under 0.16% after BF16 rounding. Gains concentrate in low-temperature greedy decoding, not in diverse stochastic sampling.

## Development line

- **2026-11-20 — SGNE-CC v2 weight edit applied to DeepSeek-R1-Distill-Qwen-1.5B.** A developer moved the SGNE-CC method from a hybrid Qwen3.5-0.8B model to DeepSeek-R1-Distill-Qwen-1.5B. The edit rotates 205 mlp.down_proj columns (about 0.0177% of parameters, 603 KB patch). It needs no fine-tuning and no change to inference code. Reported results under greedy decoding (T=0): MATH-500 accuracy rose from 65% to 76%, MBPP from 53% to 68%, BBH from 68% to 78%. Unfinished reasoning fell 87%. Average answer length dropped from 10.8k to 4.0k tokens across 1,054 tasks. At T=0.6 accuracy was reported as 73% versus 72%.
  - The method is named Spherical Gated Norm-preserving Edit, Column-Constrained (SGNE-CC), within the weight-space programming paradigm. Column rotations keep the Euclidean norm within 0.16% after BF16 rounding. They target repetitive looping under deterministic greedy decoding, so no sampling penalties are needed at inference. (2026-11-20) — <https://habr.com/ru/articles/1110462/>

## What changed

The method started as a column-constrained spherical norm-preserving edit on hybrid compact models. It changed feed-forward and recurrent projection columns to remove looping. It then moved to distilled reasoning models. The updated version targets down-projection MLP layers, which makes the patch smaller. Validation now covers standard reasoning and coding benchmarks.

## How to use this

1. Get the base DeepSeek-R1-Distill-Qwen-1.5B weights in safetensors format.
  — <https://habr.com/ru/articles/1110462/>
2. Apply the 603 KB column-rotation patch to the 205 designated mlp.down_proj columns. Do not change the architecture or the inference code.
  — <https://habr.com/ru/articles/1110462/>
3. Evaluate with greedy decoding (temperature=0, presence_penalty=0). This gives concise reasoning traces without token-limit loops.
  — <https://habr.com/ru/articles/1110462/>

## Best practices

- Evaluate under deterministic greedy decoding (temperature=0, presence_penalty=0), not sampling penalties. SGNE-CC is tuned to stabilize greedy reasoning paths.
  — <https://habr.com/ru/articles/1110462/>
- Check that Euclidean column norms in mlp.down_proj stay within 0.16% after BF16 rounding, so the numbers stay stable and internal representations do not degrade.
  — <https://habr.com/ru/articles/1110462/>

## Superseded by this

- The old way to curb repetitive reasoning loops in small models was a stochastic sampling workaround (temperature=0.6 with presence_penalty=1.5) or a heuristic weight edit such as MIT-p50c, which lowers greedy benchmark accuracy.
  — <https://habr.com/ru/articles/1110462/>

## Still unknown

- Repository paths and release dates for the first Qwen3.5-0.8B v1 patch are not confirmed. No persistent direct URLs were found.
- Reddit and GitHub discussions of the method did not resolve to persistent, loadable pages.
- Long-term conversational degradation outside math and coding benchmarks is not measured. That includes broader multi-turn evaluations.

## Sources

| source | title | read |
|---|---|---|
| https://habr.com/ru/articles/1110462/ | SGNE-CC v2: Weight editing on DeepSeek-R1-Distill-Qwen-1.5B | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** project:sgne-cc, thread sgne-cc-weight-geometry-edit, 1 dated events 2026-11-20 → 2026-11-20.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
