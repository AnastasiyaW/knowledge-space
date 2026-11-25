---
title: FASTER
category: projects
date: 2026-03-20
tags: [faster, project]
aliases: ["FASTER"]
---

# FASTER

**Development line:** `project:faster` · thread `faster`  
**Last event:** 2026-03-20 · 1 dated since 2026-03-20 · **Researched:** 2026-09-05 · confidence: medium

## What it is

FASTER is an open-source fast-action sampling and streaming deployment method for teams fine-tuning flow Vision-Language-Action policies, not a standalone robot policy.

- Horizon-Aware Schedule prioritizes near-term actions.
- Streaming client-server path dispatches early actions while later actions refine.
- Current code builds on JAX openpi and documents π0.5 and AgileX Piper workflows.

## Development line

- **2026-03-20 — FASTER public website and repository were linked.** The public repository recorded two README updates to document the project and paper state.

## What changed

2026-03-19: The FASTER paper entered arXiv as v1. 2026-03-20: The public repository recorded two README updates to document the project and paper state. 2026-04-29: arXiv v2 appeared without a technical changelog. 2026-04-30: FASTER v1.0 open-sourced the official implementation. 2026-05-16: arXiv v3 became the current paper version without a revision note.

## How to use this

As of 2026-03-20, use the FASTER public website and GitHub repository for project documentation and source access; we have verified no further usage or release claim.

1. Start from a JAX openpi flow-policy workflow and an already mapped robot platform; use `pi05_faster_agilex` as the maintained reference rather than treating FASTER as a pretrained standalone policy.
  — <https://github.com/innovator-zero/FASTER>
2. Clone with submodules, then create the documented uv environment using `GIT_LFS_SKIP_SMUDGE=1 uv sync` and `GIT_LFS_SKIP_SMUDGE=1 uv pip install -e .`.
  — <https://github.com/innovator-zero/FASTER>
3. Prepare a LeRobot v2.1 dataset and platform input/output mapping, then compute normalization statistics for the FASTER config.
  — <https://github.com/innovator-zero/FASTER>
4. Fine-tune π0.5 with `pi05_faster_agilex` and point the policy server at the resulting checkpoint.
  — <https://github.com/innovator-zero/FASTER>
5. Run the policy server and robot-controller client over WebSocket; select asynchronous HAS or streaming inference according to the task’s reaction-time requirement.
  — <https://github.com/innovator-zero/FASTER>

## Best practices

- Learn the original openpi workflow before adapting FASTER.
  — <https://github.com/innovator-zero/FASTER>
- Keep HAS inference settings `alpha` and `u0` matched to the values used during training.
  — <https://github.com/innovator-zero/FASTER>
- Set controller delay one step above measured inference delay to cover runtime and network variation, and keep execution horizon at least as large as delay.
  — <https://github.com/innovator-zero/FASTER>
- Use wired LAN for remote inference to reduce latency and packet loss.
  — <https://github.com/innovator-zero/FASTER>
- Reserve streaming with a small execution horizon for highly dynamic tasks; on ordinary pick-and-place or folding tasks it can add motion jitter.
  — <https://github.com/innovator-zero/FASTER>
- Respect the documented memory limits and the current boundary: full π0.5 fine-tuning was tested on Ubuntu 22.04, and multi-node training is not supported.
  — <https://github.com/innovator-zero/FASTER>

## Superseded by this

- 2026-04-30: the v1.0 open-source release superseded the earlier state where FASTER had no public implementation.
- 2026-05-16: arXiv v3 superseded arXiv v1 as the current paper text.

## Still unknown

- Official materials provide no checkpoint download and no complete reproduction recipe for the reported real-robot table-tennis setup; documentation assumes locally trained checkpoints.
- arXiv timestamps v2 and v3 without a technical changelog, so their exact deltas from v1 remain unknown.
- We found no first-party Simplified-Chinese technical documentation; available Chinese explanations are secondary.

## Sources

| source | title | read |
|---|---|---|
| https://innovator-zero.github.io/FASTER/ | FASTER: Rethinking Real-Time Flow VLAs | 2026-09-06 |
| https://github.com/innovator-zero/FASTER | FASTER: Rethinking Real-Time Flow VLAs | 2026-09-06 |
| https://arxiv.org/abs/2603.19199 | [2603.19199] FASTER: Rethinking Real-Time Flow VLAs | 2026-09-06 |
| https://github.com/innovator-zero/FASTER/commits/main | Commits · innovator-zero/FASTER | 2026-09-06 |
| https://github.com/innovator-zero/FASTER/releases/tag/v1.0 | Release FASTER Open-source · innovator-zero/FASTER | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:faster`, thread `faster`, 1 dated events 2026-03-20 → 2026-03-20.
- **Practical note:** As of 2026-03-20, use the FASTER public website and GitHub repository as starting points for project documentation and source access; we have verified no further usage or release claim.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
