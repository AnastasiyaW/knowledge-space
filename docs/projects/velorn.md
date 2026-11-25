---
title: Velorn
category: projects
date: 2026-07-13
tags: [project, velorn, velorn-development]
aliases: ["Velorn"]
---

# Velorn

**Development line:** `project:velorn` · thread `velorn-development`  
**Last event:** 2026-07-13 · 1 dated since 2026-07-13 · **Researched:** 2026-11-21 · confidence: high

## What it is

Velorn is a GPL-3.0 open-source AI video workstation for ComfyUI users. It covers generation, timeline editing and export in one desktop app.

- What: a desktop video editor (timeline, trimming, keyframes, captions, export) with Visuals and Sound tabs for image, video, voice and sound generation.
- Users: ComfyUI creators producing complete videos. It works with a local ComfyUI install, cloud backends, or a GPU shared by another creator.
- Key capability in 0.4.0: GPU sharing (Beta), phone access through a browser (needs 0.4 or newer), the Velo assistant, and Director Mode for timed lyric files.
- Limits: GPU sharing is labelled experimental and may find no available GPU. Cloud generation is billed through the user's own Comfy credits. Heavy local video needs significant VRAM and disk.

As of 2026-11, the latest app release is v0.4.1 (2026-11-19).

## Development line

- **2026-07-13 — Velorn public development and release references.** On 2026-07-13, an update linked the project website and the GitHub releases page. The links point to public development activity, but they do not establish a specific release, version, or changes.

## What changed

- 2026-08-27 — v0.3.31: animated GIF import and export, a Discover section, timeline zoom hotkeys.
- 2026-08-28 — v0.3.32: GPU-accelerated optical-flow slow motion, transparent media, editable caption cues.
- 2026-09-10 — v0.3.33: slow playback shortcuts, independent keyframe zoom, safer keyboard handling.
- 2026-09-15 — v0.3.34: trimming, multi-clip Inspector, volume envelopes, clip EQ, redesigned Export workspace.
- 2026-09-26 — v0.3.36: hardware encoder check for imported video, with CPU fallback; preparation jobs run one at a time. v0.3.35 the same day fixed export slowdown.
- 2026-10-12 — v0.3.37: timeline gap closing, repeated splitting, audio-analysis crash fixes.
- 2026-11-18 — song-engine-v1 pre-release: model files for lyric timing; not an app release.
- 2026-11-19 — v0.4.0: Visuals and Sound tabs, GPU sharing (Beta), phone access, Velo assistant. v0.4.1 the same day makes finished results save from any storage location.

## How to use this

1. Download the build for your OS from the GitHub releases page: Windows (installer or portable), macOS (Apple Silicon or Intel), or Linux (AppImage or deb).
  — <https://github.com/VelornLabs/velorn/releases>
2. Choose where jobs run: local ComfyUI, cloud, a shared GPU, or a mix in one project. ComfyUI is not required for the Visuals and Sound tabs.
  — <https://velorn.ai/>
3. Start from a guided preset that matches your hardware: low-VRAM local, high-quality local, cloud quality, or music video.
  — <https://velorn.ai/>
4. For cloud steps, use your own Comfy credits. The site says the price is shown before each charge.
  — <https://velorn.ai/>
5. For phone review, install v0.4 or newer on the computer and open it from a phone browser over the internet.
  — <https://velorn.ai/>

## Best practices

- Use v0.4.1 or newer. v0.4.1 fixes the case where a finished video showed "It finished, but couldn't be saved".
  — <https://github.com/VelornLabs/velorn/releases>
- Treat GPU sharing as experimental and keep a local or cloud fallback. The site says it is off until enabled.
  — <https://velorn.ai/>
- Check the Velo assistant's "Full access" setting before enabling it: the site says it lets the assistant run commands and work with files on the computer.
  — <https://velorn.ai/>

## Superseded by this

- The 0.3.x line lacks the Visuals and Sound tabs, GPU sharing, and phone access introduced in 0.4.0. Use 0.4.1 for those features.

## Still unknown

- Commercial terms beyond the repository license. The repository API shows GPL-3.0, and the site does not name a license. We did not assess what that means for distribution.
- The model list on the site (LTX, WAN, Qwen, Kling, Topaz) was not verified model by model.
- Cloud prices are not shown on the site.
- The song-engine-v1 model files were not inspected.

## Sources

| source | title | read |
|---|---|---|
| https://velorn.ai/ | Velorn — product site | 2026-11-21 |
| https://github.com/VelornLabs/velorn/releases | VelornLabs/velorn — releases | 2026-11-21 |
| https://api.github.com/repos/VelornLabs/velorn | VelornLabs/velorn — repository metadata (GPL-3.0, release dates) | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:velorn`, thread `velorn-development`, 1 dated events 2026-07-13 → 2026-07-13.
- **Practical note:** GPL-3.0 desktop AI video editor for ComfyUI. Use v0.4.1 (2026-11-19) for phone access and Visuals/Sound tabs; treat GPU sharing as beta.
- **Confidence:** high for release dates and repository license; feature claims are from the vendor site. Dated supersedes above are the authority for what is obsolete.
