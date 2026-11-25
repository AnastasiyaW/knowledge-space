---
title: "Rollback world-model RL (GE-Sim 2.0): rollback-world-model-rl-research — Rollback World Model Rl Research"
category: "projects"
date: 2026-11-01
tags: ["project", "rollback-world-model-rl", "rollback-world-model-rl-research"]
aliases: ["Rollback world-model RL (GE-Sim 2.0): rollback-world-model-rl-research"]
---

# Rollback world-model RL \(GE-Sim 2.0\): rollback-world-model-rl-research — Rollback World Model Rl Research

**Development line:** project:rollback-world-model-rl · thread rollback-world-model-rl-research  
**Last event:** 2026-11-01 · 1 dated since 2026-11-01 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Rollback is a robotic reinforcement learning method from AgiBot Research.

Most world-model methods run only forward. Rollback returns to earlier decision points in real and simulated runs, tries other actions, and compares their outcomes. That comparison shows which actions worked better, so training needs no value model.

The world model, GE-Sim 2.0, predicts the three camera views and robot joint states. The policy gets the same input in simulation as in the real world.

## Development line

- **2026-11-01 — AgiBot Research presents rollback-based world-model RL without a value model.** AgiBot Research describes a robotic reinforcement learning approach that rolls back to saved world-model states, branches into alternative actions, and trains on the differences. It allocates search budget with MCTS, learns action-level labels from sibling branches without a value model, and collects data during training to fine-tune GE-Sim 2.0.
  - The project page confirms the three mechanisms. (1) Experience-backtracking search restores saved world-model states and tests other action chunks, using MCTS to spend budget where outcomes diverge. (2) Sibling branches from the same state supply action-level labels without training a value model. (3) The robot collects real data during training to fine-tune GE-Sim 2.0, so later searches use a more accurate simulator. In the visualized search tree, each node represents one action chunk of 50 control steps at 30 Hz. Dual-arm AGIBOT Genie-02 real-world tasks reached 69.33% on Jenga, 40.00% on Ball Tossing, and 64.44% on Tabletop Curling. All methods start from the same π0.5 base policy. Baselines are SFT, RECAP, and RISE w/ GE-Sim2, an author reimplementation of RISE on this world model. Co-evolution lowered open-loop RGB L1 error from 19.52 to 12.96 across all 64 validation episodes. That raised Ball Tossing success from 26.67% to 40.00%. The project page provides no code link. (2026-11-01) — <https://rollback-wm.github.io/>

## What changed

Tree-structured comparisons of sibling branches from identical states replace a learned value model. Real data collected during training continuously corrects the world model. On the project page, Rollback beats the top baseline by 10.67 points in Jenga, 11.11 in Ball Tossing, and 11.85 in Tabletop Curling. Final performance exceeds human average in Ball Tossing and Tabletop Curling.

## How to use this

1. Start from a base policy trained on teleoperation data, or use π0.5. Collect real trajectories and retain saved world-model states for their decision points.
  — <https://rollback-wm.github.io/>
2. Run experience-backtracking search by restoring saved world-model states from real and simulated attempts. Test other action chunks and let MCTS spend search budget where outcomes diverge.
  — <https://rollback-wm.github.io/>
3. Compare outcomes across sibling branches starting from the same state. Use those comparisons as action-level labels for policy improvement without a value model.
  — <https://rollback-wm.github.io/>
4. Collect real data continuously while the policy trains. Use that data to fine-tune GE-Sim 2.0, keeping later searches on an accurate simulator.
  — <https://rollback-wm.github.io/>

## Best practices

- Update the world model continuously with real data collected during policy training. The authors report lower open-loop error (19.52 to 12.96) and higher Ball Tossing success (26.67% to 40.00%) than with a frozen world model.
  — <https://rollback-wm.github.io/>
- Compare methods using the same world model and base policy. The authors reimplemented RISE on GE-Sim 2.0 so evaluation isolates backtracking search and tree-structured supervision.
  — <https://rollback-wm.github.io/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- No code release is available on the project page or in linked resources.
- The page shows no publication date beyond a 2026 copyright notice, leaving the event date sourced from the intake brief.
- Results come solely from author reports on a project page, without independent replication.
- The page links a paper whose text was unavailable, leaving training details and ablations unverified.

## Sources

| source | title | read |
|---|---|---|
| https://rollback-wm.github.io/ | Rollback \| AgiBot Research | 2026-11-01 |

## Agent brief {#agent-brief}

- **Subject:** project:rollback-world-model-rl, thread rollback-world-model-rl-research, 1 dated events 2026-11-01 → 2026-11-01.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
