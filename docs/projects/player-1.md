---
title: "Player 1: player-1-framework-release — Player 1 Framework Release"
category: "projects"
date: 2026-11-11
tags: ["player-1", "player-1-framework-release", "project"]
aliases: ["Player 1: player-1-framework-release"]
---

# Player 1: player-1-framework-release — Player 1 Framework Release

**Development line:** project:player-1 · thread player-1-framework-release  
**Last event:** 2026-11-11 · 2 dated since 2026-10-14 · **Researched:** 2026-11-25 · confidence: high

## What it is

Player-1 is a post-training framework for developers building general game-control agents.

- Training environments: 16 synthetic training environments for reinforcement learning.
- Checkpoints: Player-1-9B and Player-1-35B-A3B released model weights.
- Benchmarks: MineDojo-300, ViZDoom-10, and 170 GameWorld tasks for evaluation.
- Recipes: SFT and reinforcement-learning recipes from curated gameplay trajectories.

Use it as a reproducible research stack for training and evaluating game-control agents, not as evidence of reliable control in arbitrary games.

## Development line

- **2026-10-14 — Player 1: player-1-framework-release update.** The paper introducing Player-1 was submitted to arXiv. It describes a post-training pipeline that starts with 6,044 gameplay trajectories and trains with PPO in 16 synthetic environments. It reports separate Player-1-9B and Player-1-35B-A3B results.
- **2026-11-11 — Tencent ARC Releases Code and Weights for Player-1 Gaming Agent.** Tencent ARC released the open-source code and model weights for the Player-1 gaming agent, including 9B and 35B variants.
  - The release scope includes Player-1-Data with 6,044 curated trajectories from 172 games, and Player-1-Gym with 16 synthetic 2D and 3D environments. It provides VeRL-based SFT and RL recipes, alongside evaluators for MineDojo-300, ViZDoom-10, and GameWorld. Released checkpoint names are Player-1-9B and Player-1-35B-A3B. (2026.11) — <https://github.com/TencentARC/Player-1>

## What changed

2026-10-14 — Player-1’s research paper introduced the synthetic-experience post-training method, its extended game-control action space, and the 9B and 35B-A3B model lines.

The later release made the research stack runnable. Model checkpoints, Player-1-Data, Player-1-Gym, SFT and RL recipes, and benchmark evaluators are now available from the project repository.

## How to use this

1. Install the Gym dependencies with Python 3.11 or newer, install Playwright Chromium, and run the browser Gym launcher from the repository root.
  — <https://github.com/TencentARC/Player-1>
2. For programmatic environment control, create a GymEnv, reset it with a seed, then send normalized keyboard and relative-pointer actions through step\(\).
  — <https://github.com/TencentARC/Player-1>
3. For model work, follow the documented sequence: supervised fine-tuning on Player-1-Data, reinforcement learning in Player-1-Gym, then evaluation on held-out gameplay benchmarks.
  — <https://github.com/TencentARC/Player-1>

## Best practices

- Keep the training and evaluation split intact. Use Player-1-Gym for synthetic RL experience and report transfer separately on held-out MineDojo, ViZDoom, and GameWorld tasks.
  — <https://github.com/TencentARC/Player-1>
- Preserve the shared keyboard-and-mouse action representation, including relative pointer motion and sustained or composite inputs, rather than reducing gameplay to one-shot clicks.
  — <https://arxiv.org/abs/2610.20584>
- Use visual, camera, scene, and control randomization in the Gym environments when training for transfer beyond one fixed game presentation.
  — <https://github.com/TencentARC/Player-1>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The public repository dates the full release only to 2026.11. The reviewed event fixes the feed date at 2026-11-11, but the repository does not expose a more precise release timestamp.
- The checked public sources do not establish hardware requirements, inference throughput, or independent replication results.
- No practitioner report describing hands-on use, failure modes, or a workaround was found in the reviewed community results.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/TencentARC/Player-1 | TencentARC/Player-1: Player-1: Learning to Play from Synthetic Experience | 2026-11-25 |
| https://arxiv.org/abs/2610.20584 | Player-1: Learning to Play from Synthetic Experience | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:player-1, thread player-1-framework-release, 2 dated events 2026-10-14 → 2026-11-11.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
