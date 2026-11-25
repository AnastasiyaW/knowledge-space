---
title: "Embodied First Exam: embodied-first-exam-benchmark-release — Embodied First Exam Benchmark Release"
category: "projects"
date: 2026-11-18
tags: ["embodied-first-exam", "embodied-first-exam-benchmark-release", "project"]
aliases: ["Embodied First Exam: embodied-first-exam-benchmark-release"]
---

# Embodied First Exam: embodied-first-exam-benchmark-release — Embodied First Exam Benchmark Release

Embodied First Exam is a containerized benchmark that tests coding agents on physical robot control tasks.

**Development line:** project:embodied-first-exam · thread embodied-first-exam-benchmark-release  
**Last event:** 2026-11-18 · 1 dated since 2026-11-18 · **Researched:** 2026-11-23 · confidence: high

## What it is

Embodied First Exam is a containerized robotics evaluation framework for coding agents. It tests physical control, not visuomotor policy learning. The benchmark has 1,156 tasks in 35 task suites across 47 robot platforms. Agents can control a robot directly, generate control code, or train a policy. Each mode runs in standard sensor-only, real-time or privileged simulation settings.

Success is roughly 77 percent with privileged simulator access. It drops to approximately 30 to 34 percent with sensor-only observations and restricted resets. This is an agent-centric baseline: physical reasoning and real-world execution remain major failure modes for language and coding agents.

## Development line

- **2026-11-18 — Embodied First Exam benchmark tests coding agents on physical robots.** Researchers released the Embodied First Exam (EFE), a containerized benchmark of 1156 tasks across 47 simulated robots. It tests whether general coding agents can act on physical robots. Top agents reached about 77% success with full simulator state and unlimited resets. They fell to about 30% when limited to onboard sensors and restricted resets.
  - The benchmark has 1,156 tasks in 35 task suites across 47 robot platforms. 745 of the tasks are adapted from existing benchmarks. It adds 9 new suites: continuous contact manipulation (RoboARC, DexHandExam, RoboPaint), dynamic whole-body interaction (RoboDynamicExam), and spatial safety engineering (iSpatialGym, Embodied Safety Exam, RoboEngineer). (2026-11-18) — <https://arxiv.org/abs/2611.12177>
  - The framework supports three control paradigms: direct action output, programmatic control code generation, and policy training. It has three evaluation modes: Standard (onboard sensors, no resets), Realtime (the simulation clock keeps running while the agent reasons), and Privileged (full state access, unlimited resets). Leading coding models reach approximately 34% success on the standard core splits. (2026-11-18) — <https://github.com/mll-lab-nu/embodied-first-exam>
  - Failure diagnosis is automated and runs in several stages. Auxiliary coding agents break execution trajectories into parts. They pinpoint whether a failure comes from planning, affordance perception, or physical contact dynamics. (2026-11-18) — <https://arxiv.org/abs/2611.12177>

## What changed

The benchmark grew from adapted manipulation suites into new areas. These are dynamic control, dexterous hand execution, multi-robot coordination, and automated stage-based failure attribution across different robot embodiments.

## How to use this

1. Clone the benchmark repository and set up the containerized simulation environment with the provided Docker container.
  — <https://github.com/mll-lab-nu/embodied-first-exam>
2. Configure the target robot platform. Pick among the 35 task suites and the evaluation modes (Standard, Realtime, or Privileged).
  — <https://github.com/mll-lab-nu/embodied-first-exam>
3. Connect an evaluation agent set up for direct control, programmatic code generation, or policy training.
  — <https://github.com/mll-lab-nu/embodied-first-exam>
4. Run the evaluation harness. It produces task success metrics and stage-level failure attribution diagnostics.
  — <https://github.com/mll-lab-nu/embodied-first-exam>

## Best practices

- Run the Privileged setting first, so you know the task is kinematically feasible and solvable in code before the Standard or Realtime runs.
  — <https://arxiv.org/abs/2611.12177>
- Read the stage-level failure traces, not only the aggregate success rate. They show whether a failure comes from perception, kinematic limits, or dynamic contact.
  — <https://github.com/mll-lab-nu/embodied-first-exam>
- Generate control code instead of sending low-level step-by-step motor commands when directing multi-joint manipulators through complex multi-stage tasks.
  — <https://arxiv.org/abs/2611.12177>

## Superseded by this

- Evaluating embodied agents only on narrow pick-and-place tasks, with single fixed visuomotor policies and full simulator reset privileges.
  — <https://arxiv.org/abs/2611.12177>

## Still unknown

- Runtime hardware requirements and licensing for third-party proprietary robot simulation environments across all 9 new suites were not detailed in public abstracts.
- Independent community replication reports and developer forum discussion remain limited after the initial release.

## Sources

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2611.12177 | Embodied First Exam: An Agent-Native Benchmark for Robotics | 2026-11-23 |
| https://github.com/mll-lab-nu/embodied-first-exam | mll-lab-nu/embodied-first-exam: Embodied First Exam Benchmark | 2026-11-23 |

## Agent brief {#agent-brief}

- **Subject:** project:embodied-first-exam, thread embodied-first-exam-benchmark-release, 1 dated events 2026-11-18 → 2026-11-18.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
