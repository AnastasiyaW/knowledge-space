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

Violin is an MIT-licensed CLI, FastAPI app, and Claude Code skill for video translation and dubbing.

- Transcription: extracts speech from video.
- Translation: translates dialogue across target languages.
- Dubbing: generates replacement voice audio.
- SRT subtitles: creates timed caption files.
- Video Q&A: answers questions about video content.

Supports 33 target languages; six style profiles marked experimental.

Practical for permitted video, though the public demo warns of possible translation errors.

## Development line

- **2026-05-15 — Public introduction of the Violin translation project.** On 2026-05-15, Violin was publicly associated with a Together AI article, an open GitHub repository, and its project website. The dated links indicate a public introduction of an open-source, translation-oriented project and establish its initial public references.

## What changed

2026-05-15 — Violin appeared as an open pipeline combining ASR, LLM translation, and TTS. The primary source dates the post to 2026-05-14 instead of 2026-05-15. It listed the original models as Together Whisper Large V3, DeepSeek V4 Pro, and Cartesia Sonic 3. The current repository shows version 0.1.1, 33 languages, swappable Together/OpenAI/ElevenLabs providers, and no GitHub Releases. We cannot reliably date those later changes from available primary sources.

## How to use this

From 2026-05-15, practitioners should consider Violin a publicly reachable translation-oriented project and assess it through its linked repository and project site.

1. For local use, install Python 3.10+, ffmpeg, and the package via `uv tool install violin`. Set a provider key, then run `violin input.mp4 output.mp4 --language Chinese`.
  — <https://github.com/shang-zhu/violin>
2. For the web UI and REST API, run `violin-api`. Create a job via `POST /jobs`, poll it, and download the video or SRT file.
  — <https://github.com/shang-zhu/violin>
3. For a quick check, use the web demo. Upload a file or paste a URL, then pick a language, voice, subtitles, and voice-over mode.
  — <https://www.violin-ai.com/>

## Best practices

- Translate only owned, public-domain, or Creative Commons media, or content with explicit permission. The demo restricts input URLs to this rule.
  — <https://www.violin-ai.com/>
- Start with the default profile and automatic voice selection. Use a separate YAML config for terminology and check the output, because the demo is marked as a research beta.
  — <https://github.com/shang-zhu/violin>
- In production, use `config/prod.yaml`. It limits uploads, serializes jobs, and caps ffmpeg concurrency.
  — <https://github.com/shang-zhu/violin>

## Superseded by this

- 2026-05-14 — The initial description defaulted to DeepSeek V4 Pro and Qwen3.5-397B-A17B. The current README specifies DeepSeek-V4-Pro-0813 for translation and GLM-5.3-Flash for chat, but no date confirms the switch.
- 2026-05-14 — Missing voice cloning remains an active limit. The repository still lists it under TODO rather than as an available feature.

## Still unknown

- Available primary sources provide no dated history after launch. We do not record current model settings as new dated events.
- GitHub shows no releases. Version 0.1.1 appears in pyproject.toml, but available sources confirm neither a release date nor a PyPI distribution.
- Users must evaluate dubbing quality on their own language and footage. The public demo warns that translations may contain errors.

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
- **Practical note:** From 2026-05-15, practitioners should consider Violin a publicly reachable translation-oriented project and assess it through its linked repository and project site.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
