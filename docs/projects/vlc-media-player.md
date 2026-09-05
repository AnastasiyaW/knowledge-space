---
title: VLC media player — Video enhancement
category: projects
date: 2023-04-13
tags: [project, video-enhancement, vlc, vlc-media-player, vlc_rtx_vsr]
aliases: ["VLC", "VLC media player"]
---

# VLC media player — Video enhancement

**Development line:** `project:vlc-media-player` · thread `video-enhancement`  
**Last event:** 2023-04-13 · 1 dated since 2023-04-13 · **Researched:** 2026-09-05 · confidence: medium

## What it is

VLC media player is an open-source media player for users who need a single client instead of the OS default player: local files, discs, network URLs, NAS, and Chromecast.

- Hardware decoding, HDR, and 360° video.
- Track selection for external and embedded subtitles and audio.
- Playback for network streams and browsing for network folders.

Hardware decoding depends on the platform and hardware.

For regular playback, install current stable VLC rather than the old experimental RTX build.

## Development line

- **2023-04-13 — VLC tested NVIDIA RTX Video Super Resolution integration.** On 2023-04-13, VLC made a testing build available with support for NVIDIA RTX Video Super Resolution. This was a development step toward GPU-assisted video upscaling during playback, distributed through a dedicated experimental archive.

## What changed

2023-04-13 — A dedicated Windows build of VLC 3.0.19 RTX Vetinari enabled NVIDIA RTX Video Super Resolution by default on RTX 30/40.

2025-01-13 — VLC for Android 3.6.0 added Remote Access and parental controls.

2026-01-08 — Stable VLC 3.0.23 added Windows ARM64 support, a dark theme for Windows/Linux, codec updates, and stability and security fixes.

## How to use this

From 2023-04-13, practitioners with compatible NVIDIA RTX hardware could evaluate VLC's experimental GPU video-upscaling path using the linked testing build, rather than treating it as a standard stable-release capability.

1. Install current stable VLC 3.0.23 for desktop; Windows provides x64 and ARM64 builds.
  — <https://images.videolan.org/vlc/releases/3.0.23.html>
2. Open a local file through Media → Open File, or drag it into the VLC window.
  — <https://docs.videolan.me/vlc-user/desktop/3.0/en/basic/media.html>
3. For a stream, choose Media → Open Network Stream, paste the URL, and press Play.
  — <https://docs.videolan.me/vlc-user/desktop/3.0/en/basic/media.html>
4. On Android, install the current version of VLC to play files, network streams, and DVD ISOs, and access NAS or shared folders.
  — <https://images.videolan.org/vlc/download-android.html>

## Best practices

- Keep desktop VLC updated: 3.0.23 includes security and stability fixes for demuxers.
  — <https://images.videolan.org/news.html>
- On Android, use hardware decoding when the device supports it; use software decoding on older devices.
  — <https://images.videolan.org/vlc/download-android.html>
- Select subtitle and audio tracks in playback controls or the disc dialog rather than transcoding the file in advance.
  — <https://docs.videolan.me/vlc-user/desktop/3.0/en/basic/media.html>

## Superseded by this

- 2023-04-13 — VLC 3.0.19 RTX was a testing build for RTX Video Super Resolution rather than a standard desktop release; the supported 3.0.23 release (2026-01-08) replaces it for general use.
- 2025-01-13 — Android 3.6.0 is no longer current: Android 3.7.0 was released on 2026-02-25.

## Still unknown

- The social post from 2025-01-13 was unreadable; the official announcement on the same day confirms the VLC for Android 3.6.0 release, but not the exact text of the post.
- The VLC and VLC RTX VSR topics belong to the same project, but track separate product lines: the standard desktop and mobile player, and a temporary Windows build with NVIDIA RTX VSR.

## Sources

| source | title | read |
|---|---|---|
| https://downloads.videolan.org/testing/vlc-rtx-upscaler/ | VLC 3.0.19 RTX Vetinari - VideoLAN | 2026-09-05 |
| https://images.videolan.org/news.html | News - VideoLAN | 2026-09-05 |
| https://images.videolan.org/vlc/releases/3.0.23.html | VLC 3.0.23 Vetinari - VideoLAN | 2026-09-05 |
| https://docs.videolan.me/vlc-user/desktop/3.0/en/basic/media.html | Media — VLC Desktop User Documentation 3.0 documentation | 2026-09-05 |
| https://images.videolan.org/vlc/download-android.html | Official Download of VLC media player for Android - VideoLAN | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:vlc-media-player`, thread `video-enhancement`, 1 dated events 2023-04-13 → 2023-04-13.
- **Practical note:** From 2023-04-13, practitioners with compatible NVIDIA RTX hardware could evaluate VLC's experimental GPU video-upscaling path using the linked testing build, rather than treating it as a standard stable-release capability.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
