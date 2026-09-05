---
title: DRIFT — Project resources
category: projects
date: 2026-06-04
tags: [drift, project, project-resources]
aliases: ["DRIFT"]
---

# DRIFT — Project resources

**Development line:** `project:drift` · thread `project-resources`  
**Last event:** 2026-06-04 · 1 dated since 2026-06-04 · **Researched:** 2026-09-05 · confidence: high

## What it is

DRIFT is an open claim-centric framework to localize trajectory spans where an unverified or contradicted claim becomes harmful in a deep-research agent. It includes Claim Keeper, Support Seeker, and Dependency Tracer. TELBench provides 1 000 expert-verified trajectory tasks from 2 790 collected runs. It is a reproducible tool to compare trajectory audits and investigate failures, not a live monitoring layer for a running agent.

## Development line

- **2026-06-04 — DRIFT project page and repository were linked.** On 2026-06-04, a dated message associated with DRIFT linked to the DRIFT project page and its GitHub repository. That message places those resources in the development line, but confirms no release, version, technical change, or project-launch claim.

## What changed

2026-06-04 — DRIFT and TELBench were presented as open artifacts for span-level error localization in deep-research agent trajectories.

## How to use this

From 2026-06-04, practitioners evaluating DRIFT use the linked project page and GitHub repository as the available primary resources. The event establishes no installation or workflow change.

1. Clone the repository and install the package in editable mode.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
2. Download encrypted TELBench through Hugging Face and decrypt it with the provided script; the script checks the SHA-256 of the result.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
3. Configure an OpenAI-compatible Chat Completions or Responses API via arguments or an env file and run `drift --setting drift` on JSONL trajectories.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
4. Pass `summary.json` to `drift-eval`; the report contains macro/micro precision, recall, F1, first-error accuracy, and missing or extra identifiers.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>

## Best practices

- Run `bare` first on the same input data and model, then `drift`, so the claim-centric pipeline effect stays separate from the base model.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
- Check the checksum of decrypted TELBench, and do not add downloaded artifacts, the key, or decrypted JSONL to Git.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>
- Do not pass gold labels, annotations, metadata, judge results, or manual notes to the model: evaluation allows only the question and ordered raw span text.
  — <https://huggingface.co/datasets/NJU-LINK/TELBench>
- Keep `--reasoning-effort low` for the Responses API unless a measured reason requires a change: that is the project default for JSON-only prompts.
  — <https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Public primary sources confirm paper submission on 1 June 2026 and its revision v2 on 2 June, but record no separate DRIFT release on 4 June; 4 June remains the event date, not a confirmed release date.
- No primary dated changelog exists after 4 June 2026 to name later code or dataset changes with confidence.

## Sources

| source | title | read |
|---|---|---|
| https://nju-link.github.io/DRIFT/ | DRIFT | Claim-Centric Trajectory Auditing | 2026-09-05 |
| https://github.com/NJU-LINK/DRIFT | NJU-LINK/DRIFT repository | 2026-09-05 |
| https://github.com/NJU-LINK/DRIFT/blob/main/docs/USAGE.md | DRIFT usage guide | 2026-09-05 |
| https://huggingface.co/datasets/NJU-LINK/TELBench | NJU-LINK/TELBench dataset card | 2026-09-05 |
| https://arxiv.org/abs/2606.02060 | Where Do Deep-Research Agents Go Wrong? Span-Level Error Localization in Agent Trajectories | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:drift`, thread `project-resources`, 1 dated events 2026-06-04 → 2026-06-04.
- **Practical note:** From 2026-06-04, practitioners evaluating DRIFT should use the linked project page and GitHub repository as the available primary resources; this evidence does not establish an installation or workflow change.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
