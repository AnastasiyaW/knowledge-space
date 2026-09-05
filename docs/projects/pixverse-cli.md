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

- JSON output for script and agent pipelines.
- Task and asset management from the terminal.

The current official README requires Node.js 22.12+. Generation consumes account credits. We can use it for automation, but pin the CLI version and check available credits and slots before batch runs.

## Development line

- **2026-03-17 — PixVerse introduced a terminal-facing generation interface.** On 2026-03-17, PixVerse indicated that image and video generation was available through a command-line interface. A linked ClawHub entry distributed the interface for reuse in terminal workflows. This marks a delivery step from web access to the command line.

## What changed

- **2026-03-17** — A link tied PixVerse CLI to terminal media generation, but did not confirm the release date.
- **2026-03-31** — PixVerse announced the CLI and Skills library for developer and agent workflows.
- **2026-07-13** — An official guide documented video, images, voice, music, JSON output, and idempotency keys for production pipelines.
- **2026-09-05** — The current official README specifies Node.js 22.12+, OAuth device flow, V6 as the default video model, and an expanded list of supported models.

## How to use this

As of 2026-03-17, we can consider a terminal PixVerse workflow for image and video generation. Confirm setup, supported operations, and production limits in the official documentation before relying on it.

1. Install the package through npm or run it directly without global installation, then check the CLI version.
  — <https://github.com/PixVerseAI/cli>
2. Run `pixverse auth login`, complete OAuth authentication in the browser, and verify status with `pixverse auth status`.
  — <https://github.com/PixVerseAI/cli>
3. Check credits and available parallel slots with `pixverse account info` and `pixverse account slots` before queuing jobs.
  — <https://github.com/PixVerseAI/cli>
4. Create media with `pixverse create video` or `pixverse create image`. For automation, pass `--json`, save the job ID, wait with `pixverse task wait`, and download via `pixverse asset download`.
  — <https://github.com/PixVerseAI/cli>

## Best practices

- Set model, quality, duration, and aspect ratio explicitly: parameter support depends on the mode and model.
  — <https://github.com/PixVerseAI/cli>
- Pass `--idempotency-key` for batch retries. For parallel dispatch, use `--no-wait`, save task IDs, and poll them in batches.
  — <https://pixverse.ai/en/blog/pixverse-cli-generate-ai-videos-images-from-terminal>
- Keep `--json` enabled in scripts and agent pipelines so stdout stays machine-readable while errors and progress logs remain separate.
  — <https://github.com/PixVerseAI/cli>
- Run `pixverse --version` before large runs, check `pixverse create <mode> --help`, and update the CLI only after verifying changes.
  — <https://pixverse.ai/en/blog/pixverse-cli-generate-ai-videos-images-from-terminal>

## Superseded by this

- 2026-03-17: do not treat this date as a confirmed launch date. The initial availability announcement was on 2026-03-31.
- 2026-09-05: the Node.js 20 requirement from the published Skills card is obsolete. The current official README requires Node.js 22.12+.
- 2026-09-05: covering only video and images is incomplete. The current CLI also documents voice, music, tasks, assets, and workspaces.

## Still unknown

- Official sources do not confirm that the original 2026-03-17 link was published on that date. The practical guide is dated 2026-07-13, and the official CLI announcement is dated 2026-03-31.
- The ClawHub card lists Node.js 20+, while the current official README lists Node.js 22.12+. Follow the README or package help for installation.
- The system response schema lacks dedicated event_findings and new_events fields. Relevant clarifications are included in what changed, supersedes, and unknowns.

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
