---
title: PixVerse CLI — Terminal generation
category: projects
date: 2026-03-17
tags: [pixverse, pixverse-cli, project, terminal-generation]
aliases: ["PixVerse CLI"]
---

# PixVerse CLI — Terminal generation

**Development line:** `project:pixverse-cli` · thread `terminal-generation`  
**Last event:** 2026-03-17 · 1 dated since 2026-03-17 · **Researched:** 2026-09-05 · confidence: medium

## What it is

PixVerse CLI is a command-line interface for PixVerse subscribers to generate video, images, and audio from prompts or references.

- Media generation from text prompts and reference files.
- JSON output for scripts and agent pipelines.
- Task and asset management via dedicated CLI commands.

Requires Node.js 22.12+; generation consumes account credits. It fits automation workflows, but we must pin the CLI version and check available credits and concurrency slots before running batch jobs.

## Development line

- **2026-03-17 — PixVerse introduced a terminal-facing generation interface.** PixVerse opened command-line access to its image and video generation on 2026-03-17. A linked ClawHub entry distributed the interface for terminal workflows. The project moved generation from web access into the terminal.

## What changed

2026-03-17 — PixVerse CLI was linked to terminal media generation, but the link does not confirm the release date.  
2026-03-31 — PixVerse announced the CLI and the Skills library for developer and agent workflows.  
2026-07-13 — The official practical guide detailed video, images, voice, music, JSON output, and idempotency keys for production pipelines.  
2026-09-05 — The current official README specifies Node.js 22.12+, an OAuth device flow, V6 as the default video model, and an expanded list of supported models.

## How to use this

As of 2026-03-17, we can use PixVerse from the terminal for image and video generation, but we must verify setup and production limits in the official documentation first.

1. Install the package with npm or run it directly, then check the CLI version.
  — <https://github.com/PixVerseAI/cli>
2. Run `pixverse auth login`, complete browser OAuth authentication, and check status with `pixverse auth status`.
  — <https://github.com/PixVerseAI/cli>
3. Check credits and available concurrency slots with `pixverse account info` and `pixverse account slots` before queuing batches.
  — <https://github.com/PixVerseAI/cli>
4. Generate media with `pixverse create video` or `pixverse create image`; pass `--json` for automation, save the task ID, wait with `pixverse task wait`, and download with `pixverse asset download`.
  — <https://github.com/PixVerseAI/cli>

## Best practices

- Set model, quality, duration, and aspect ratio explicitly, because supported options depend on the mode and model.
  — <https://github.com/PixVerseAI/cli>
- Pass `--idempotency-key` for batch retries, and use `--no-wait` to send jobs in parallel, save their IDs, and poll them in batches.
  — <https://pixverse.ai/en/blog/pixverse-cli-generate-ai-videos-images-from-terminal>
- Keep `--json` enabled in scripts and agent runs so stdout stays machine-readable while progress and errors stay separate.
  — <https://github.com/PixVerseAI/cli>
- Run `pixverse --version` and check `pixverse create <mode> --help` before large runs, and update the CLI only after verifying changes.
  — <https://pixverse.ai/en/blog/pixverse-cli-generate-ai-videos-images-from-terminal>

## Superseded by this

- 2026-03-17: we cannot treat this as the confirmed launch date; the initial availability announcement was 2026-03-31.
- 2026-09-05: the Node.js 20 requirement from the published Skills card is obsolete; the current official README requires Node.js 22.12+.
- 2026-09-05: covering only video and images is incomplete; the current CLI also documents voice, music, tasks, assets, and workspaces.

## Still unknown

- The official source does not confirm that the original link from 2026-03-17 was published that day: the current practical guide is dated 2026-07-13, and the official CLI availability announcement is dated 2026-03-31.
- The ClawHub card lists Node.js 20+, while the current official README specifies Node.js 22.12+; follow the README or the installed package help for installation.
- The system response schema lacks separate event_findings and new_events fields; relevant clarifications sit in what_changed, supersedes, and unknowns.

## Sources

| source | title | read |
|---|---|---|
| https://pixverse.ai/en/blog/pixverse-cli-generate-ai-videos-images-from-terminal | PixVerse CLI: Generate AI Videos and Images in Terminal | 2026-09-05 |
| https://clawhub.ai/PixVerse-Official/pixverse-ai-image-and-video-generator | PixVerse AI Image and Video Generator | 2026-09-05 |
| https://github.com/PixVerseAI/cli | PixVerseAI/cli — official command-line interface | 2026-09-05 |
| https://pixverse.ai/en/blog/pixverse-evolves-from-creation-tool-to-production-platform | PixVerse Evolves From Creation Tool to Production Platform With New Studio and Developer Releases | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:pixverse-cli`, thread `terminal-generation`, 1 dated events 2026-03-17 → 2026-03-17.
- **Practical note:** As of 2026-03-17, practitioners should consider a terminal-based PixVerse workflow for image and video generation, while confirming setup, supported operations, and production suitability in the official documentation before relying on it.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
