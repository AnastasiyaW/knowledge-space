---
title: Cream Typer
category: projects
date: 2026-06-11
tags: [cream-typer, project]
aliases: ["Cream Typer"]
---

# Cream Typer

**Development line:** `project:cream-typer` · thread `cream-typer`  
**Last event:** 2026-06-11 · 1 dated since 2026-06-11 · **Researched:** 2026-11-21 · confidence: low

## What it is

Cream Typer is an MIT-licensed macOS menu-bar app that dictates speech with local whisper.cpp transcription and pastes the text at the cursor.

- Input: Caps Lock toggles recording (first tap starts, second stops).
- Output: 16 modes selected in the menu bar: 15 target languages plus "→ English (from any)"; translation works by changing the language parameter.
- Users: Mac users who dictate in several languages and want audio kept on the machine.
- Limits: macOS only; Apple Silicon is the main target; Windows and Linux are marked "TBD"; the project is small (10 stars and 1 fork at capture).

## Development line

- **2026-06-11 — Cream Typer GitHub repository referenced.** On 2026-06-11, we recorded a direct link to the project's GitHub repository. The source gave no release details, source text, or description of a change. This event does not assert a launch, version, or feature update.

## What changed

- 2026-05-01 — Thai (th) and Vietnamese (vi) language modes added (commit history).
- 2026-05-02 — tray UI updates dispatched to the main thread (fix); README link to user attachments.
- 2026-09-24 — one-command launch and a transcript history that survives a lost paste; CI change to keep ruff away from Markdown code blocks.
- No releases are published on the repository.

## How to use this

1. Confirm you are on macOS; the project targets Apple Silicon. The page says an Intel Mac works without Metal.
  — <https://github.com/adjacentai/cream-typer>
2. Install Python 3.10 or later, cmake and git; run `make setup` (builds whisper.cpp and downloads a model of about 550 MB), then `make`.
  — <https://github.com/adjacentai/cream-typer>
3. Grant Input Monitoring, Microphone and Accessibility permissions in macOS settings before the first dictation.
  — <https://github.com/adjacentai/cream-typer>
4. Choose the language mode in the menu bar before speaking; the output language is set by the mode, not by a speech-detection step.
  — <https://github.com/adjacentai/cream-typer>
5. Keep the history file as your record: each transcription is written to `transcripts.txt` before it is pasted.
  — <https://github.com/adjacentai/cream-typer>

## Best practices

- Check the output mode before dictating, because translation depends on the selected language mode.
  — <https://github.com/adjacentai/cream-typer>
- For Thai dictation, expect lower quality than the large-v3 model; the page states this for the turbo model in use.
  — <https://github.com/adjacentai/cream-typer>

## Superseded by this

- The native `task=translate` flag on the large-v3-turbo model is superseded by the language-swap approach, because the project reports the native flag is broken on that model.

## Still unknown

- Commit dates beyond the five most recent were not read; the page showed six commits in total.
- The MIT license is shown on the page through a link; the LICENSE file was not opened.
- The latency figure (about 0.3–0.5 s for 10 s of speech) is the project's own measurement and was not reproduced.
- Windows and Linux support has no date; it is listed as TBD.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/adjacentai/cream-typer | Cream Typer repository: README, features, requirements | 2026-11-21 |
| https://api.github.com/repos/adjacentai/cream-typer/commits?per_page=5 | GitHub REST API: recent commit dates | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:cream-typer`, thread `cream-typer`, 1 dated event 2026-06-11; commits dated 2026-05-01 → 2026-09-24.
- **Practical note:** macOS only; check the language mode before dictating; treat the latency and quality figures as the project's own.
- **Confidence:** low. Single repository with little activity and no releases. Dated supersedes above are the authority for what is obsolete.
