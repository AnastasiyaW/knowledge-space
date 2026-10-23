---
title: d-OPSD — Research paper and code release
category: projects
date: 2026-06-21
tags: [d-opsd, project, research-paper-and-code-release]
aliases: ["d-OPSD"]
---

# d-OPSD — Research paper and code release

**Development line:** `project:d-opsd` · thread `research-paper-and-code-release`  
**Last event:** 2026-06-21 · 1 dated since 2026-06-21 · **Researched:** 2026-09-05 · confidence: medium

## What it is

d-OPSD is a research framework for post-training diffusion language models. It builds a self-teacher from the model's own answer as suffix conditioning, moves supervision from tokens to denoising steps, and was compared with RLVR and SFT on four reasoning benchmarks. The authors report about 10% of RLVR's optimization steps. Public code exists, but the source shows no ready model and no independent replication of the results.

## Development line

- **2026-06-21 — d-OPSD research paper and code repository linked.** The self-generated answer is used as suffix context for the teacher, and the loss is computed over denoising steps.

## What changed

2026-06-21 — d-OPSD was presented as OPSD for dLLMs: the self-generated answer is used as suffix context for the teacher, and the loss is computed over denoising steps.

## How to use this

From 2026-06-21, practitioners should treat d-OPSD as a project with a linked research paper and public code repository, and consult both before evaluating or attempting to use it.

1. Create a Conda environment from `env.yml` and activate `dOPSD`.
  — <https://github.com/xingzhejun/d-opsd-code>
2. Replace or patch `trl/trainer/grpo_trainer.py` and `utils.py` with the versions from the repository; this is required for the allowed number of generations and for aligning the teacher prompt and output.
  — <https://github.com/xingzhejun/d-opsd-code>
3. Run the script for the set you need: GSM, math, Countdown or Sudoku from `d-opsd/run`.
  — <https://github.com/xingzhejun/d-opsd-code>
4. Point the evaluation script at your checkpoint, save the generations, and compute accuracy with `eval/parse_and_get_acc.py`.
  — <https://github.com/xingzhejun/d-opsd-code>

## Best practices

- Pin the TRL version and apply both of the authors' trainer-file replacements, not only `grpo_trainer.py`.
  — <https://github.com/xingzhejun/d-opsd-code>
- On A100 and H100 set `BATCH_DIVIDE=8` to avoid OOM; the value `4` in the scripts is meant for B200.
  — <https://github.com/xingzhejun/d-opsd-code>
- Before comparing with the paper's results, check Python 3.10, CUDA 12.9 and the configuration in `used-env.txt`; the authors list A100/H100/B200.
  — <https://github.com/xingzhejun/d-opsd-code>

## Superseded by this

- 2026-08-17 — the early environment instruction, which replaces only `grpo_trainer.py`, is outdated: the README also requires replacing `utils.py` because of TRL fixes and the warning format.

## Still unknown

- d-OPSD is easy to confuse with the identically named D-OPSD for step-distilled image diffusion models (arXiv:2605.05204); this material refers to the dLLM work of Luo et al., arXiv:2606.18195.
- The authors claim an advantage on four benchmarks and about 10% of RLVR's steps, but the sources checked show no independent replication, no checkpoint release and no production integration.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/papers/2606.18195 | Learning from the Self-future: On-policy Self-distillation for dLLMs | 2026-09-05 |
| https://arxiv.org/abs/2606.18195 | Learning from the Self-future: On-policy Self-distillation for dLLMs | 2026-09-05 |
| https://github.com/xingzhejun/d-opsd-code | xingzhejun/d-opsd-code | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:d-opsd`, thread `research-paper-and-code-release`, 1 dated events 2026-06-21 → 2026-06-21.
- **Practical note:** From 2026-06-21, practitioners should treat d-OPSD as a project with a linked research paper and public code repository, and consult both before evaluating or attempting to use it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
