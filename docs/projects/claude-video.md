---
title: claude-video
category: projects
date: 2026-07-27
tags: [claude-video, claude-video-development, claude_video, project]
aliases: ["claude-video", "claude-video (watch)"]
---

# claude-video

**Development line:** `project:claude-video` · thread `claude-video-development`  
**Last event:** 2026-07-27 · 1 dated since 2026-07-27 · **Researched:** 2026-09-05 · confidence: medium

## What it is

claude-video is a `/watch` skill for video analysis for agents.

- Input: takes a URL or a local file.
- Extraction: pulls frames and subtitles.
- Audio fallback: uses Whisper when subtitles are missing.
- Result handoff: passes output to the agent.

The default limit for long videos is up to 100 frames; `token-burner` mode is unlimited. It fits screen recordings, video clips, and targeted timestamps, but context cost grows with the number of frames.

## Development line

- **2026-07-27 — claude-video repository publicly referenced.** On 2026-07-27, an entry linked to the bradautomates/claude-video GitHub repository. This is the earliest public reference in the project history and provides a concrete source to inspect.

## What changed

- 2026-07-27 — repository link recorded. Primary sources show no separate commit or release on that exact date.
- 2026-06-29 — version 0.2.0 added four detail modes, frame deduplication, automatic splitting of long audio for Whisper, and a portable skill package for multiple hosts.

## How to use this

From 2026-07-27, treat the linked bradautomates/claude-video GitHub repository as the source for implementation and usage details.

1. Install the skill for Claude Code through the marketplace, or for Codex and other Agent Skills hosts with `npx skills add bradautomates/claude-video -g`.
  — <https://github.com/bradautomates/claude-video>
2. Run `/watch <URL-or-path> <question>`. It supports URLs handled by yt-dlp, and local MP4, MOV, MKV, and WebM files.
  — <https://github.com/bradautomates/claude-video>
3. Pass `--start` and `--end` for a targeted excerpt. This samples frames more densely while spending fewer context tokens.
  — <https://github.com/bradautomates/claude-video>
4. Select `transcript`, `efficient`, `balanced`, or `token-burner`. If subtitles are missing, set a Groq key for `whisper-large-v3` or an OpenAI key for `whisper-1`.
  — <https://github.com/bradautomates/claude-video>

## Best practices

- Narrow the time window with `--start` and `--end` for questions about a specific moment, instead of scanning the full video.
  — <https://github.com/bradautomates/claude-video>
- Start with `transcript` for videos with subtitles or `efficient` for a fast visual pass; save `token-burner` for cases that justify the cost of many frames.
  — <https://github.com/bradautomates/claude-video>
- Keep frame deduplication enabled: by default it discards nearly identical frames before applying the limit.
  — <https://github.com/bradautomates/claude-video>
- Do not append comments after the `WATCH_DETAIL` value: this previously caused a silent fallback to the default mode, fixed in commit 83da59f.
  — <https://github.com/bradautomates/claude-video/commit/83da59f>

## Superseded by this

- 2026-04-24 — the standalone `commands/watch.md` wrapper and non-self-contained skill layout were replaced by the `skills/watch/` package in version 0.2.0.
- 2026-04-24 — the Windows instruction using `python3` is obsolete: on Windows, run scripts with `python`.
- 2026-04-24 — the early fixed limit of `--max-frames=80` was replaced by limits tied to the detail mode.

## Still unknown

- The dated event provides only the repository URL. No first-party release or commit dated 2026-07-27 was found, so there is no source-backed addition for that date.
- The schema lacks `event_findings` and `new_events` fields; the 2026-06-29 release stays in `what_changed` rather than as a separate structured event.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/bradautomates/claude-video | bradautomates/claude-video — README and current usage documentation | 2026-09-05 |
| https://raw.githubusercontent.com/bradautomates/claude-video/main/CHANGELOG.md | claude-video changelog — version 0.2.0 dated 2026-06-29 | 2026-09-05 |
| https://github.com/bradautomates/claude-video/commit/83da59f | Fix WATCH_DETAIL silently falling back to default | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:claude-video`, thread `claude-video-development`, 1 dated events 2026-07-27 → 2026-07-27.
- **Practical note:** From 2026-07-27, treat the linked bradautomates/claude-video GitHub repository as the source to inspect for implementation and usage details.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
