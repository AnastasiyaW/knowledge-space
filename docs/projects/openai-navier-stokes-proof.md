---
title: "OpenAI Navier-Stokes proof: openai-navier-stokes-proof — Openai Navier Stokes Proof"
category: "projects"
date: 2026-10-06
tags: ["openai-navier-stokes-proof", "project"]
aliases: ["OpenAI Navier-Stokes proof: openai-navier-stokes-proof"]
---

# OpenAI Navier-Stokes proof: openai-navier-stokes-proof — Openai Navier Stokes Proof

**Development line:** project:openai-navier-stokes-proof · thread openai-navier-stokes-proof  
**Last event:** 2026-10-06 · 8 dated since 2026-09-08 · **Researched:** 2026-11-25 · confidence: medium

## What it is

OpenAI Navier–Stokes proof is a claimed finite-time-singularity construction for three-dimensional incompressible flow, for mathematicians and Lean reviewers.

- Analytical paper, presenting the mathematical construction.
- Lean 4 certificates, providing formal verification.
- Reproducible build instructions, setting up local verification.

The construction requires smooth external forcing and targets Clay alternatives C and D, so it is not an end-user fluid-simulation tool. Inspect and independently check the released formalization before relying on the claim.

## Development line

- **2026-09-08 — OpenAI publishes proof for Navier-Stokes existence and smoothness problem.** OpenAI published a post claiming to solve the Millennium Prize problem. An internal model generated the mathematical text and formalized it in Lean for verification. The release includes an analysis of computational scaling for task solving.
- **2026-09-08 — OpenAI Publishes Navier-Stokes Existence and Smoothness Proof.** OpenAI published a post and proof showing that fluid dynamics can form singularities in finite time. The release pairs textual exposition with Lean formalization verified by an engine. The work ran on a new internal model.
- **2026-09-08 — OpenAI publishes proof and formalization for Navier-Stokes existence and smoothness problem.** OpenAI published a solution to the Millennium Prize problem. The internal proof shows that Navier-Stokes dynamics can form singularities in finite time. The post includes text and a Lean formalization verified by an engine. A new internal model still under training produced the result.
- **2026-09-08 — other reporting on this date.**
  - The release fixes the mathematical scope: the flow starts at rest under smooth external forcing, preserves finite kinetic energy, and targets Clay alternatives C and D. OpenAI identifies the system only as an internal model ahead of GPT-6 Astra. (2026-09-08) — <https://openai.com/index/navier-stokes-solution/>
  - The paper states the core theorem: for every positive viscosity, it builds a three-dimensional incompressible flow with smooth compactly supported force, finite energy, and unbounded velocity before time 1. (2026-09-08) — <https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf>
  - The repository contains Lean 4 code with instructions for local checking: fetch the mathlib cache, then run `lake build`. It points to a Comparator path for independent verification. (2026-09-08) — <https://github.com/openai/NavierStokesAndEuler>
  - The repository documents Lean 4 formalizations of Navier–Stokes and Euler results. It gives `lake exe cache get` and `lake build` steps, and points to Comparator for independent proof checking. (undated) — <https://github.com/openai/NavierStokesAndEuler>
- **2026-09-09 — OpenAI publishes proof for Navier-Stokes millennium problem.** OpenAI claims its internal AI agents solved the Navier-Stokes problem, one of the seven millennium problems. The proof was being translated to Lean for formal verification.
- **2026-09-09 — OpenAI Publishes Proof for Navier-Stokes Millennium Problem.** OpenAI claims internal AI solved the millennium problem, showing fluid motion forms a singularity in finite time under specific initial conditions. The proof was translated into Lean for verification.
- **2026-09-09 — OpenAI resolves Navier-Stokes existence and smoothness problem using agent system.** A system of 10,000 agents resolved the Millennium Prize Navier-Stokes problem. Research wrapped up on September 5, 2026, followed by 17 hours of verification with GPT-6 Astra. Agents sent 2.7 million messages and generated 130 billion tokens.
- **2026-09-09 — other reporting on this date.**
  - OpenAI reports coordinating agents on an internal model produced an analytical proof and Lean formalization for the smooth-forcing result. (2026-09-08) — <https://openai.com/index/navier-stokes-solution/>
  - OpenAI states roughly 10,000 concurrent agents produced the result, followed by 17 hours of Lean formalization and verification. The solving model remains identified only as an internal model. (2026-09-08) — <https://openai.com/index/navier-stokes-solution/>
- **2026-09-10 — OpenAI Navier-Stokes proof: openai-navier-stokes-proof update.** OpenAI updated the concurrent-work section. Its investigation concluded specified Codex prompts could not have influenced the internal system, including through training. (found in research)
- **2026-10-06 — OpenAI Navier-Stokes proof: openai-navier-stokes-proof update.** OpenAI published a related preprint, “Incompressible Box Transport and Finite Computation,” showing forced Navier–Stokes flows that encode finite computation. This is related research, not a revision of the blowup proof. (found in research)

## What changed

The release supplied a paper, a Lean formalization, and a construction with bounded kinetic energy and unbounded velocity under smooth forcing in finite time. A later update added OpenAI’s investigation into whether external user prompts influenced the work. Subsequent preprints extended computability constructions in forced Navier–Stokes flow.

## How to use this

1. Read the paper’s theorem statement to confirm its forced C/D scope matches your problem.
  — <https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf>
2. Clone the Lean repository, install the declared toolchain, run `lake exe cache get`, then run `lake build`.
  — <https://github.com/openai/NavierStokesAndEuler>
3. Follow the ComparatorChallenges instructions in the repository rather than treating a local build as independent verification.
  — <https://github.com/openai/NavierStokesAndEuler>

## Best practices

- Keep the mathematical scope explicit: separate the smooth externally forced construction in alternatives C/D from unforced Navier–Stokes questions.
  — <https://github.com/openai/NavierStokesAndEuler>
- Pin the manuscript revision, then trace assumptions and equation dependencies before relying on an AI-generated formalization.
  — <https://community.openai.com/t/openai-agents-solve-the-navier-stokes-existence-and-smoothness-problem/1395873>
- Run a second proof-checking route; the repository documents Comparator separately from its standard Lean build.
  — <https://github.com/openai/NavierStokesAndEuler>

## What practitioners say

- One practitioner ran an AI review agent on a pinned manuscript to trace assumptions, equations, computational checks, and open questions. They frame this as preparation for human mathematicians, not a replacement. (2026-11-16)
  — <https://community.openai.com/t/openai-agents-solve-the-navier-stokes-existence-and-smoothness-problem/1395873>

## Superseded by this

- The initial concurrent-work wording is superseded by the section with OpenAI’s investigation into specified user inputs.
  — <https://openai.com/index/navier-stokes-solution/>

## Still unknown

- No separate public reporting distinguishes the five URL-backed entries as separate events. They appear to describe the same September 8 release.
- The September 9 entry citing 10,000 agents, 2.7 million messages, 130 billion tokens, 88 hours, and 17 hours matches the first-party post, but the intake item lacks its own URL.
- A local Lean build verifies the certificate only in its declared environment. We did not run it independently or establish external mathematical consensus.

## Sources

| source | title | read |
|---|---|---|
| https://openai.com/index/navier-stokes-solution/ | On the Navier–Stokes Millennium Prize Problem | 2026-11-25 |
| https://openai.com/zh-Hans-CN/index/navier-stokes-solution/ | 关于纳维–斯托克斯千禧年大奖难题 | 2026-11-25 |
| https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf | Finite Time Blowup for Navier–Stokes | 2026-11-25 |
| https://github.com/openai/NavierStokesAndEuler | openai/NavierStokesAndEuler | 2026-11-25 |
| https://github.com/openai/math/tree/main/preprints/Incompressible-Box-Transport-and-Finite-Computation-October-6-2026 | Incompressible Box Transport and Finite Computation | 2026-11-25 |
| https://community.openai.com/t/openai-agents-solve-the-navier-stokes-existence-and-smoothness-problem/1395873 | OpenAI agents solve the Navier–Stokes existence and smoothness problem | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:openai-navier-stokes-proof, thread openai-navier-stokes-proof, 8 dated events 2026-09-08 → 2026-10-06.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
