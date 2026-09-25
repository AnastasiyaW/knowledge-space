---
title: DanceOPD
category: projects
date: 2026-06-26
tags: [danceopd, danceopd-development, project]
aliases: ["DanceOPD"]
---

# DanceOPD

**Development line:** `project:danceopd` · thread `danceopd-development`  
**Last event:** 2026-06-26 · 1 dated since 2026-06-26 · **Researched:** 2026-09-06 · confidence: high

## What it is

DanceOPD is a training framework for teams that already have compatible flow-matching checkpoints or LoRAs and need one student to combine text-to-image and image-editing behaviors.

- Hard-routes each sample to one frozen capability field.
- Queries a low-noise state from the current student rollout and matches velocity with MSE.
- Documents SD3.5/Diffusers and Z-Image/DiffSynth backends.

## Development line

- **2026-06-26 — DanceOPD project website linked.** On 2026-06-26, the DanceOPD GitHub Pages site went live. The site gave the project a public presence, but the underlying source text was not available.

## What changed

- 2026-06-25 — arXiv v1 was submitted at 17:59:58 UTC, creating the canonical preprint record.
- 2026-06-26 — the v1 manuscript is dated June 26, and the public repository opened with the initial commit `init`.
- 2026-06-30 — `Sync public release contents` added 59 files with 3,208 additions and 76 deletions, including code, configs, data preparation, smoke scripts, and documentation.
- 2026-07-07 — arXiv v2 was submitted without a revision note, leaving its content changes unknown.
- 2026-08-15 — arXiv v3 was submitted. DanceOPD 0.2.0 added task-bound teacher routing, three modes across SD3.5-M and Z-Image, runnable public configs, paper templates, resume support, dual-LoRA support, and CFG-field options.

## How to use this

1. Clone `worldbench/DanceOPD`, install the needed extra set, and run `pip install -e ".[smoke]"` plus `bash scripts/bootstrap_smoke.sh`.
  — <https://github.com/worldbench/DanceOPD>
2. Run the SD3.5 or Z-Image configuration dry run before loading real weights. Install DiffSynth-Studio before full Z-Image training.
  — <https://github.com/worldbench/DanceOPD>
3. Prepare a routed prompt or OmniEdit CSV. Edit routes require `source_image`, and style, background, or environment tasks map to `global_edit` unless overridden.
  — <https://github.com/worldbench/DanceOPD>
4. Configure each frozen teacher as a base checkpoint, full checkpoint, PEFT LoRA, or checkpoint-plus-LoRA. Keep the trainable student LoRA separate.
  — <https://github.com/worldbench/DanceOPD>
5. Use `configs/public` to exercise code or paper templates with compatible assets, then launch with Accelerate and resume from a saved step when needed.
  — <https://github.com/worldbench/DanceOPD>

## Best practices

- Treat the smoke path as a code-health check, not evidence that paper metrics reproduce.
  — <https://github.com/worldbench/DanceOPD>
- For DanceOPD itself, retain the documented default: one hard-routed teacher, one low-noise query (`K=1`), and direct velocity MSE.
  — <https://github.com/worldbench/DanceOPD>
- Do not stack teacher LoRAs on the trainable student adapter. Merge each teacher into a clean frozen teacher module instead.
  — <https://github.com/worldbench/DanceOPD>
- Keep `student_cfg_scale=1.0` when absorbing CFG, adjust the teacher scale, and tune inference CFG separately so effects do not compound.
  — <https://github.com/worldbench/DanceOPD>
- Keep downloadable public substitutes distinct from paper-aligned templates; the paper checkpoints remain unavailable.
  — <https://github.com/worldbench/DanceOPD>

## Superseded by this

- 2026-06-26 — a project-page-only understanding was superseded by the public-code sync on 2026-06-30 and the 0.2.0 toolkit on 2026-08-15.
- 2026-08-15 — an undifferentiated reproduction path is obsolete: public substitute assets and paper-aligned templates are separate, and the paper checkpoints remain unreleased.

## Still unknown

- The project page itself has no publication timestamp. The June 26 event relies on the manuscript's displayed date and repository history, while arXiv v1 was submitted on June 25 UTC.
- arXiv provides no change notes for v2 or v3, so manuscript edits remain unverified.
- No peer-reviewed conference or journal venue was verified; arXiv labels the work a Technical Report.
- No official hardware requirement, wall-clock training estimate, deterministic seed, hosted inference endpoint, or independent reproduction receipt was verified.

## Sources

| source | title | read |
|---|---|---|
| https://danceopd.github.io/ | DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://arxiv.org/html/2606.27377v1 | DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://arxiv.org/abs/2606.27377 | [2606.27377] DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://github.com/worldbench/DanceOPD | GitHub - worldbench/DanceOPD: DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://github.com/worldbench/DanceOPD/commits/main/ | Commits · worldbench/DanceOPD · GitHub | 2026-09-06 |
| https://github.com/worldbench/DanceOPD/commit/08f1230c013bf8fe21295cc95bd01e36e5c2a45b | Sync public release contents · worldbench/DanceOPD@08f1230 · GitHub | 2026-09-06 |
| https://raw.githubusercontent.com/worldbench/DanceOPD/main/CHANGELOG.md | DanceOPD CHANGELOG.md | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:danceopd`, thread `danceopd-development`, 1 dated events 2026-06-26 → 2026-06-26.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
