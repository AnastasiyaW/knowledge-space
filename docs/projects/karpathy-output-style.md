---
title: "Karpathy Output Style: karpathy-output-style-visual-explanations — Karpathy Output Style Visual Explanations"
category: "projects"
date: 2026-10-22
tags: ["karpathy-output-style", "karpathy-output-style-visual-explanations", "project"]
aliases: ["Karpathy Output Style: karpathy-output-style-visual-explanations"]
---

# karpathy-output-style: visual explanations

**Development line:** project:karpathy-output-style · thread karpathy-output-style-visual-explanations  
**Last event:** 2026-10-22 · 2 dated since 2026-10-22 · **Researched:** 2026-10-23 · confidence: high

## What it is

karpathy-output-style is an open-source tool and prompt skill for developers who use AI coding assistants such as Claude Code and Codex. It makes model reasoning faster to inspect by putting each answer into one of four formats:

- Simplified technical English, derived from the ASD-STE100 standard.
- Editable Excalidraw diagrams for system architecture.
- Self-contained interactive single-file HTML pages with parameter sliders.
- Programmatic explainer animations with voice narration.

Interactive HTML and video need an external rendering runtime or a browser. The tool does not replace the model's own reasoning. It gives a practical way to inspect complex output without reading long text.

## Development line

- **2026-10-22 — karpathy-output-style lets users ask for visual LLM explanations.** The R77 AI channel reported that a developer found the open-source project. It lets users request diagrams, interactive HTML pages or short videos from an LLM. The tool follows Andrej Karpathy's recently proposed output-format approach.
- **2026-10-22 — Diagrams and videos instead of long text answers.** A second report the same day described the project the same way: an LLM returns diagrams, interactive HTML pages or videos instead of long text. It was framed as following Karpathy's recently proposed output-format approach.
- **2026-10-22 — other reporting on this date.**
  - The open-source repository by Ashrya Aggarwal packages Karpathy's output ladder into modular AI agent skills for coding assistants like Claude Code and Codex. It defines a 4-tier progression: ASD-STE100 technical English, Excalidraw diagrams, interactive HTML sandboxes and narrated video clips. (2026-10-22) — <https://github.com/ashryaagr/karpathy-output-style>
  - The tool runs a structured workflow: understand, pick the simplest format, inspect, output. It uses Excalidraw for diagrams, self-contained HTML/Canvas for sliders and text-to-speech services like ElevenLabs for video narration. (2026-10-22) — <https://github.com/ashryaagr/karpathy-output-style>

## What changed

The repository turned Andrej Karpathy's proposed multi-tier explanation ladder into reproducible agent skills. It set four ascending tiers: controlled technical prose, Excalidraw diagrams, standalone HTML sandboxes and narrated video. Integration with agent CLI environments was documented later, so models can pick a visual format by query complexity.

## How to use this

1. Clone the karpathy-output-style repository, or copy the skill definition file into the agent configuration directory.
  — <https://github.com/ashryaagr/karpathy-output-style>
2. Set the agent runtime \(such as Claude Code or Codex\) to load the skill rules during query execution.
  — <https://github.com/ashryaagr/karpathy-output-style>
3. Give the agent a concept or a piece of code to explain. The skill picks between simplified technical text, Excalidraw diagrams, interactive HTML or an explainer video.
  — <https://github.com/ashryaagr/karpathy-output-style>

## Best practices

- Keep to the four-tier ladder: start with the simplest format before asking for heavy interactive HTML or video.
  — <https://github.com/ashryaagr/karpathy-output-style>
- Keep interactive HTML in a single self-contained file with embedded styles and scripts, so it opens in a local browser at once.
  — <https://github.com/ashryaagr/karpathy-output-style>

## Superseded by this

- Unstructured multi-paragraph plain text as the default answer for technical architecture and algorithm explanations.
  — <https://github.com/ashryaagr/karpathy-output-style>

## Still unknown

- The repository summary does not give release tags or version numbers for the initial commit.
- Discussion URLs from Reddit and Hacker News came back through redirect wrappers. They were left out so every cited link loads directly.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/ashryaagr/karpathy-output-style | ashryaagr/karpathy-output-style: AI agent skills for visual and structured LLM outputs | 2026-10-23 |

## Agent brief {#agent-brief}

- **Subject:** project:karpathy-output-style, thread karpathy-output-style-visual-explanations, 2 dated events 2026-10-22 → 2026-10-22.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
