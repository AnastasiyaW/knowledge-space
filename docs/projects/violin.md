---
title: Violin
category: projects
date: 2026-05-15
tags: [project, violin]
aliases: ["Violin"]
---

# Violin

**Development line:** `project:violin` · thread `violin`  
**Last event:** 2026-05-15 · 1 dated since 2026-05-15 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Violin is an MIT-licensed CLI, FastAPI app, and Claude Code skill for video translation.

- Transcription to turn speech into text.
- Translation across 33 target languages.
- Dubbing to replace spoken audio tracks.
- Subtitles to generate SRT files.
- Video Q&A to answer questions against video content.

Six style profiles remain experimental. We can use it on permitted video, though the demo warns of translation errors.

## Development line

- **2026-05-15 — Public introduction of the Violin translation project.** Violin appeared publicly on 2026-05-15 with a Together AI article, an open GitHub repository, and its project website. These links establish the project as an open-source translation tool.

## What changed

2026-05-15 — Violin launched as an open ASR → LLM translation → TTS pipeline. The primary source dates the post to 2026-05-14 rather than 2026-05-15. It listed the original models as Together Whisper Large V3, DeepSeek V4 Pro, and Cartesia Sonic 3. The current repository shows version 0.1.1, 33 languages, and swappable Together, OpenAI, and ElevenLabs providers. It has no GitHub Releases. Primary sources do not provide dates for these later updates.

## How to use this

From 2026-05-15, assess Violin through its repository and project site as a public translation project.

1. For local runs, install Python 3.10+, ffmpeg, and the package via `uv tool install violin`. Set the provider key, then run `violin input.mp4 output.mp4 --language Chinese`.
  — <https://github.com/shang-zhu/violin>
2. For the browser interface and REST API, run `violin-api`. Create a job via `POST /jobs`, poll it, and download the video or SRT file.
  — <https://github.com/shang-zhu/violin>
3. For a one-off test, use the web demo. Upload a file or paste a URL, then select the language, voice, subtitles, and voice-over mode.
  — <https://www.violin-ai.com/>

## Best practices

- Translate only owned, public-domain, Creative Commons, or authorized media. The demo restricts permitted URLs to these categories.
  — <https://www.violin-ai.com/>
- Start with the default profile and automatic voice selection. Use a dedicated YAML configuration for custom terminology, and inspect the output because the demo is a research beta.
  — <https://github.com/shang-zhu/violin>
- In production, use `config/prod.yaml`. It limits upload sizes, serializes jobs, and caps ffmpeg concurrency.
  — <https://github.com/shang-zhu/violin>

## Superseded by this

- 2026-05-14 — The initial description named DeepSeek V4 Pro and Qwen3.5-397B-A17B by default. The current README specifies DeepSeek-V4-Pro-0813 for translation and GLM-5.3-Flash for chat, but no date confirms the swap.
- 2026-05-14 — Lack of voice cloning remains an active limit. The repository still lists voice cloning under TODO rather than as a shipping feature.

## Still unknown

- Available primary sources provide no dated post-launch history, so current model settings are not recorded as dated events.
- GitHub shows no releases. We can confirm version 0.1.1 in pyproject.toml, but no source confirms its release date or a PyPI package.
- We must judge dubbing quality on our own language and media, as the public demo warns translations may contain errors.

## Sources

| source | title | read |
|---|---|---|
| https://www.together.ai/blog/violin-open-source-translation-skill | Violin: An open-source video translation skill that breaks language barriers | 2026-09-05 |
| https://github.com/shang-zhu/violin | shang-zhu/violin repository and README | 2026-09-05 |
| https://www.violin-ai.com/ | Violin — Video Narrator | 2026-09-05 |
| https://github.com/shang-zhu/violin/releases | Violin GitHub releases | 2026-09-05 |
| https://raw.githubusercontent.com/shang-zhu/violin/main/pyproject.toml | Violin pyproject.toml | 2026-09-05 |
| https://raw.githubusercontent.com/shang-zhu/violin/main/config/default.yaml | Violin default configuration | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:violin`, thread `violin`, 1 dated events 2026-05-15 → 2026-05-15.
- **Practical note:** From 2026-05-15, assess Violin through its linked repository and project site as a public translation project.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
