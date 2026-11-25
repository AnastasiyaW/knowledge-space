---
title: "OpenResearch"
category: "projects"
date: 2026-09-18
tags: ["openresearch-alphaiv", "project"]
aliases: ["Openresearch Alphaiv: openresearch-alphaiv"]
---

# OpenResearch

**Development line:** project:openresearch-alphaiv · thread openresearch-alphaiv  
**Last event:** 2026-09-18 · 1 dated since 2026-09-18 · **Researched:** 2026-11-25 · confidence: medium

## What it is

OpenResearch is an alphaXiv harness and workspace that turns coding agents into researchers.

It is MIT-licensed, local-first, and ships as a desktop app and a standalone CLI (orx).

- Literature and hypotheses: reviews papers, builds hypotheses, runs experiments, and saves research artifacts.
- Agent support: connects to Claude Code, Codex, OpenCode, Cursor, and Google Antigravity.
- Local models: runs local models through OpenCode.

## Development line

- **2026-09-18 — OpenResearch: Transforming Coding Agents into Researchers.** OpenResearch is a local workspace that transforms coding agents into researchers. It supports parallel experiments, autonomous cycles, git-native experiment trees, and reproducible runs across local, SSH, Slurm, Kubernetes, and Ray environments.
  - The repository describes OpenResearch as an alphaXiv local-first harness and workspace for research agents under the MIT license. Agents review literature, test hypotheses, run experiments, and save research artifacts. Supported agents are Claude Code, Codex, OpenCode, Cursor, and Google Antigravity. Literature search integrates alphaXiv, bioRxiv, and PubMed. Compute runs on local machines, SSH, Slurm, Kubernetes, Modal, Tinker, Ray, Hugging Face Jobs, or managed OpenResearch compute. A local SQL database records every experiment, keeping logs, code, and artifacts on your machine. Official release builds send opt-out, coarse product analytics and detailed agent feedback tied to a random installation ID. The repository showed about 8.5k stars when observed. (2026-09-18) — <https://github.com/alphaXiv/OpenResearch>

## What changed

The project repository is public. It provides a desktop app for macOS, Windows (beta), and Linux, plus the orx CLI with a local dashboard. Compute runs locally, over SSH, on Slurm, Kubernetes, Modal, Tinker, Ray, Hugging Face Jobs, or through managed OpenResearch compute. A local SQL database records all experiments, keeping logs, code, and artifacts on the user's machine.

## How to use this

1. Download the desktop app for macOS (11+), Windows (beta, requires Git for Windows), or Linux (x86_64 or ARM64, glibc 2.35+). This is the recommended path.
  — <https://github.com/alphaXiv/OpenResearch>
2. Alternatively, install the standalone CLI on macOS or Linux with `curl -LsSf https://openresearch.sh/install.sh | sh`. Run `orx up` to open the local dashboard at http://127.0.0.1:4791.
  — <https://github.com/alphaXiv/OpenResearch>
3. Select a supported agent (Claude Code, Codex, OpenCode, Cursor, or Google Antigravity), or run local models through OpenCode with LM Studio, oMLX, Rapid-MLX, Ollama, or a custom endpoint. Then pick the compute target for experiments.
  — <https://github.com/alphaXiv/OpenResearch>

## Best practices

- Use the signed and notarized desktop app on a managed Mac where device-management policies block the unsigned CLI from install.sh. Install the orx command from Settings → Updates → Install the orx command.
  — <https://github.com/alphaXiv/OpenResearch>
- Ground hypotheses in the literature through alphaXiv, bioRxiv, and PubMed integrations. Let agents check the local experiment database of past results to decide what to try next.
  — <https://github.com/alphaXiv/OpenResearch>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The visible repository text does not confirm per-session git worktree isolation, immutable commit archives, or the exact reproducibility guarantees from the announcement.
- The visible repository text does not state a release date or version number.
- Usage analytics details beyond the opt-out notice were cut off in the page text.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/alphaXiv/OpenResearch | GitHub - alphaXiv/OpenResearch: Turn your coding agents into research agents | 2026-09-18 |

## Agent brief {#agent-brief}

- **Subject:** project:openresearch-alphaiv, thread openresearch-alphaiv, 1 dated events 2026-09-18 → 2026-09-18.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
