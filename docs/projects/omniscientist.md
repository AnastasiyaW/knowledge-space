---
title: OmniScientist
category: projects

tags: [omniscientist, project]
aliases: ["OmniScientist"]
---

# OmniScientist

**Development line:** `project:omniscientist` · thread `omniscientist`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-06 · confidence: medium

## What it is

OmniScientist is an open local research workflow for people who want to turn a raw-data folder and an open question into a traceable candidate paper.

- Inputs: reads images, waveforms, audio, video, point clouds, trajectories, tables, and formulas.
- Stages: runs ideation, experiment, and writeup stages with code and artifact traces.
- Outputs: produces TeX/PDF output with numbers linked to recorded executions.

The authors report 36 real-data cases. The reference engine allows two automatic re-ideation backtracks by default. We use it as an auditable computational-research scaffold, not as proof that a generated scientific claim is correct.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-08-13 — The technical report was first submitted to arXiv.
- 2026-08-16 — v0.1.0 publicly released the desktop workbench, terminal agent, and Claude Code skill.
- 2026-08-18 — v0.1.1 added release-wide SHA256SUMS verification.
- 2026-08-21 — This is not a verified release or commit date: the official history jumps from 2026-08-20 to 2026-08-22; v0.1.1 was the most recent tagged release at that point.
- 2026-08-23 — v0.1.2 added DeepSeek V4 Flash Vision support and fixed PDF-review rendering.
- 2026-08-24 — v0.1.3 added multilingual workspace and page support.
- 2026-08-25 — v0.1.6 was released with desktop, terminal, and skill bundles.
- 2026-08-28 — v0.2.0 shipped desktop packages as a Windows installer, macOS ZIP, and Linux DEB.
- 2026-09-02 — v0.2.1 became the latest verified release; current README guidance retires the standalone CLI in favor of the desktop app or skill.

## How to use this

1. Download the v0.2.1 desktop package for the platform, or unpack omnisci-skill.zip into ~/.claude/skills. Verify the release checksum before installing.
  — <https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.1>
2. Give the desktop workspace or installed skill a folder of raw data and an open research direction. Use the local workspace to inspect the resulting run log and artifacts.
  — <https://omni-scientist.github.io/>
3. Define the data and open direction in series.json for a scriptable reference-engine run. Run agentic.py with --stage run rather than an isolated stage.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md>
4. Configure the reasoning backbone and an image-capable perception model separately when using the reference engine.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md>

## Best practices

- Use --stage run for a real engine run. Single stages are for debugging and do not perform automatic backtracking.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md>
- Start with an open, falsifiable direction and inspect the raw evidence before choosing an analysis method.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/skill/omnisci/SKILL.md>
- Record every reported number from script stdout, use real retrieved references, and treat a passing numeric gate as provenance evidence rather than scientific validation.
  — <https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/skill/omnisci/SKILL.md>
- Verify downloaded release assets against SHA256SUMS before installation.
  — <https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.1>

## Superseded by this

- 2026-09-02 — Standalone CLI installation guidance from the v0.1.x line is obsolete for a new installation: the current README says the terminal edition was discontinued in v0.2.1.
- 2026-09-02 — v0.2.0 is superseded by v0.2.1 as the latest verified release.

## Still unknown

- The exact wording and intended claim of the 2026-08-21 announcement is unavailable, so it cannot be classified more narrowly than a reference to the official project.
- The official site uses month-level August news, while GitHub carries the precise release chronology; GitHub is the source of truth for version dates.
- First-party documentation has a drift: v0.2.1 release prose still mentions a terminal agent, but the current README says the standalone CLI is discontinued and the v0.2.1 assets contain only desktop packages and the skill.
- No first-party or independently reproducible Simplified-Chinese operating report was found for a Chinese-language practice recommendation.
- The technical report's evaluation results are author-reported; no independent replication was verified here.

## Sources

| source | title | read |
|---|---|---|
| https://omni-scientist.github.io/ | OmniScientist: An Omni-Modal Omni-Discipline AI Scientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist | Omni-Scientist/OmniScientist repository and current README | 2026-09-07 |
| https://arxiv.org/abs/2608.13558 | OmniScientist: An Omni-Modal Omni-Discipline AI Scientist | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.0 | OmniScientist 0.1.0 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.1 | OmniScientist 0.1.1 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/commits/main | OmniScientist main-branch commit history | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.2 | OmniScientist 0.1.2 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.3 | OmniScientist 0.1.3 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.1.6 | OmniScientist 0.1.6 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.0 | OmniScientist 0.2.0 release | 2026-09-07 |
| https://github.com/Omni-Scientist/OmniScientist/releases/tag/v0.2.1 | OmniScientist 0.2.1 release | 2026-09-07 |
| https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/docs/USAGE.md | OmniScientist Usage guide | 2026-09-07 |
| https://raw.githubusercontent.com/Omni-Scientist/OmniScientist/main/skill/omnisci/SKILL.md | OmniScientist agent skill instructions | 2026-09-07 |

## Agent brief {#agent-brief}

- **Subject:** `project:omniscientist`, thread `omniscientist`, 0 dated events - → -.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
