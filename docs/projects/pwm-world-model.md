---
title: "Alaya Lab: Programmable World Model (PWM)"
category: "projects"
date: 2026-10-11
tags: ["project", "pwm-world-model"]
aliases: ["Alaya Lab: pwm-world-model"]
---

# Alaya Lab: Programmable World Model (PWM)

Alaya Lab's Programmable World Model (PWM) is an explicit-state framework for generative worlds that separates world state from video rendering.

**Development line:** project:pwm-world-model · thread pwm-world-model  
**Last event:** 2026-10-11 · 3 dated since 2026-09-05 · **Researched:** 2026-11-25 · confidence: medium

## What it is

Programmable World Model (PWM) is an explicit-state framework for generative worlds. It separates state tracking from visual rendering.

- State executor: maintains the world state and advances it under player actions and world rules.
- Deterministic compiler: projects state-augmented 3D oriented bounding boxes (OBBs) into pixel-aligned controls.
- Video model: renders the visual observation.
- VLM agent: writes executable world specifications from a reference image and open-ended language.

## Development line

- **2026-09-05 — Alaya Lab: pwm-world-model update.** Alaya Lab released the PWM project page, according to the repository's news list. (found in research)
- **2026-09-11 — Programmable World Model (Alaya Lab).** Announcement of a Programmable World Model where the world state exists as explicit data separate from video frames, featuring agent-written rules, state tracking, and deterministic compilation for video generation.
  - The project page describes the loop in four parts: a state executor, a deterministic compiler that outputs state-augmented 3D OBBs as pixel-aligned controls, a video model renderer, and a VLM-based agent that writes the world specification from a reference image and language. Its demos cover persistent events (a death event applied to the canonical world state), off-screen persistence (a -130° pan reveals entities kept in state), rule-driven event triggers (a vehicle enters and stops as the world program dictates), and open-domain worlds (the same OBB interface and compiler drive a different world). The long-horizon demo is a 30-second autoregressive rollout with a crowd of entities and no drift across 897 frames. (undated page; observed 2026-10-11) — <https://alaya-lab.github.io/pwm/>
  - The repository describes PWM as 'explicit world state, generative rendering', where a coding agent reads and writes the explicit world state. As of the observed page, the release roadmap lists the project page, technical report PDF, inference code and pretrained weights, with the code and weights marked coming soon. The repository had 213 stars and 8 forks. (undated page; observed 2026-10-11) — <https://github.com/AlayaLab/pwm>
- **2026-10-11 — Alaya Lab: pwm-world-model update.** Alaya Lab released PROWBench, a benchmark for evaluating whether video models render what programs specify. (found in research)

## What changed

Video world models usually keep state implicitly in visual histories. That makes state difficult to inspect, edit or verify. Off-screen entities and latent facts like health or relations are easily lost.

PWM separates world-state tracking from visual rendering so world facts remain queryable, modifiable and verifiable. Entities persist off-screen, events remain irreversible, and the same state drives any camera angle or visual style.

## How to use this

1. Supply a reference image and an open-ended language description. The VLM-based agent turns them into an executable world specification covering entities, rules and events.
  — <https://alaya-lab.github.io/pwm/>
2. Run the state executor to advance the canonical world state under player actions (the demos show W/A/S/D input) and world rules. The deterministic compiler then projects the state into pixel-aligned controls, and the video model renders the frames.
  — <https://alaya-lab.github.io/pwm/>
3. Inference code and pretrained weights are not yet released (listed as coming soon), so hands-on use is not yet possible. Follow the repository for the release.
  — <https://github.com/AlayaLab/pwm>

## Best practices

- Keep hidden facts and rules, such as health, relations and event triggers, in structured records and executable code instead of visual history. This lets an agent construct and update them.
  — <https://alaya-lab.github.io/pwm/>
- Treat explicit state as the source of truth. Query, edit and verify it directly, and change camera or visual style without altering the underlying world.
  — <https://github.com/AlayaLab/pwm>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Inference code, pretrained weights and the technical report are not yet released.
- The pages give no quantitative benchmark results; PROWBench is only announced.
- The project page is dated 2026-09-05 in the repository news, while the reviewed announcement is dated 2026-09-11.
- The pages do not name the underlying video model or the VLM used by the agent.

## Sources

| source | title | read |
|---|---|---|
| https://alaya-lab.github.io/pwm/ | Programmable World Model (Alaya Lab project page) | 2026-10-11 |
| https://github.com/AlayaLab/pwm | GitHub - AlayaLab/PWM: Programmable World Model: explicit world state, generative rendering | 2026-10-11 |

## Agent brief {#agent-brief}

- **Subject:** project:pwm-world-model, thread pwm-world-model, 3 dated events 2026-09-05 → 2026-10-11.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
