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

claude-video is a `/watch` skill for video analysis across URLs and local files.

- Frame extraction from local files and web video.
- Subtitle extraction, falling back to Whisper when subtitles are missing.
- Result handover to the agent.

The default limit for long videos is up to 100 frames; `token-burner` mode has no limit.

We use it for screen recordings, video clips, and targeted time ranges, but context cost grows with frame count.

## Development line

- **2026-07-27 — claude-video repository publicly referenced.** On 2026-07-27, a public link pointed to the bradautomates/claude-video GitHub repository. This is the earliest public reference in this development line and gives a concrete project source to consult.

## What changed

- **2026-07-27** — A link pointed to the repository, with no separate commit or release dated that day in primary sources.
- **2026-06-29** — Version 0.2.0 added four detail modes, frame deduplication, automatic long audio splitting for Whisper, and a portable skill package across hosts.

## How to use this

From 2026-07-27, we inspect the linked bradautomates/claude-video GitHub repository for implementation and usage details.

1. Install the skill for Claude Code through the marketplace, or for Codex and other Agent Skills hosts run `npx skills add bradautomates/claude-video -g`.
  — <https://github.com/bradautomates/claude-video>
2. Run `/watch <URL-or-path> <question>`; this accepts URLs supported by yt-dlp as well as local MP4, MOV, MKV, and WebM files.
  — <https://github.com/bradautomates/claude-video>
3. Pass `--start` and `--end` for a specific segment to get denser frames with less context consumption.
  — <https://github.com/bradautomates/claude-video>
4. Choose `transcript`, `efficient`, `balanced`, or `token-burner`; if subtitles are missing, configure a Groq key for `whisper-large-v3` or an OpenAI key for `whisper-1`.
  — <https://github.com/bradautomates/claude-video>

## Best practices

- Limit the time window with `--start` and `--end` for questions about a specific moment instead of scanning the full video.
  — <https://github.com/bradautomates/claude-video>
- Start with `transcript` for subtitled videos or `efficient` for a fast visual pass; save `token-burner` for cases that justify high frame costs.
  — <https://github.com/bradautomates/claude-video>
- Keep frame deduplication enabled: it discards near-identical frames before applying the limit.
  — <https://github.com/bradautomates/claude-video>
- Do not add comments after the `WATCH_DETAIL` value: this previously triggered a silent fallback to the default mode, fixed in commit 83da59f.
  — <https://github.com/bradautomates/claude-video/commit/83da59f>

## Superseded by this

- 2026-04-24 — The separate `commands/watch.md` wrapper and non-contained skill layout are replaced by the `skills/watch/` package in version 0.2.0.
- 2026-04-24 — The Windows instruction specifying `python3` is obsolete: run scripts on Windows using `python`.
- 2026-04-24 — The early fixed `--max-frames=80` limit is replaced by limits tied to the detail mode.

## Still unknown

- The event dated 2026-07-27 provides only the repository URL, with no first-party release or commit found for that date.
- The 2026-06-29 release has no separate event entry and remains tracked in changes.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/bradautomates/claude-video | bradautomates/claude-video — README and current usage documentation | 2026-09-05 |
| https://raw.githubusercontent.com/bradautomates/claude-video/main/CHANGELOG.md | claude-video changelog — version 0.2.0 dated 2026-06-29 | 2026-09-05 |
| https://github.com/bradautomates/claude-video/commit/83da59f | Fix WATCH_DETAIL silently falling back to default | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:claude-video`, thread `claude-video-development`, 1 dated events 2026-07-27 → 2026-07-27.
- **Practical note:** From 2026-07-27, treat the linked bradautomates/claude-video GitHub repository as the source for implementation and usage details.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
