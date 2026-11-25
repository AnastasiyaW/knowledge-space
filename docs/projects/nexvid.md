---
title: NexVid — Browser extension distribution
category: projects
date: 2026-04-17
tags: [browser-extension-distribution, nexvid, project]
aliases: ["NexVid"]
---

# NexVid — Browser extension distribution

**Development line:** `project:nexvid` · thread `browser-extension-distribution`  
**Last event:** 2026-04-17 · 1 dated since 2026-04-17 · **Researched:** 2026-09-05 · confidence: medium

## What it is

NexVid is a browser extension for people who watch anime, cartoons, and web video in Chrome or Firefox.
- Anime4K GPU upscaling for real-time video playback.
- Quality and FPS profiles to match hardware performance.
- Filters and WebGL shaders for image adjustment.
- Presets to save shader and filter chains.
- Local player for desktop video files.

Processing runs during playback and requires access to data on all websites; v1.1.9 from 2026-08-20 is current.
It tunes playback, but does not replace video export with neural upscaling.

## Development line

- **2026-04-17 — NexVid browser-extension listings appeared for Chrome and Firefox.** On 2026-04-17, listings for the NexVid browser extension appeared on the Chrome Web Store and Firefox Add-ons. This step expanded distribution across Chrome and Firefox. The source listings do not state a version, feature set, availability status, or changes made on that date.

## What changed

- 2025-10-27 — Firefox 1.0.2 became the earliest publicly visible version in AMO history.
- 2025-11-10 — Firefox 1.0.5 added local videos and extra effects.
- 2025-12-01 — Firefox 1.1.0 added dark and minimalist themes, raised the maximum FPS, and fixed Twitch; 1.1.1 on the same day fixed profile selection in the minimal interface.
- 2026-01-20 — Firefox 1.1.2 added a resolution threshold to skip high-quality sources, along with experimental shaders.
- 2026-03-08 — Firefox 1.1.3 added a website whitelist.
- 2026-04-17 — Chrome 1.1.6 was updated; this confirms a Chrome release, not an identical Firefox release on that date.
- 2026-08-20 — Chrome and Firefox offer 1.1.9; current store descriptions list Anime4K, performance profiles, shaders, presets, and a local player.

## How to use this

From 2026-04-17, practitioners evaluating NexVid should check its browser-extension availability through the Chrome Web Store and Firefox Add-ons, while independently verifying current compatibility and capabilities.

1. Install NexVid from the Chrome Web Store or Firefox Add-ons and open the target web video.
  — <https://chromewebstore.google.com/detail/nexvid-real-time-video-up/hiocbajaikpcckgeagcngaeoioncmbim>
2. Select an Anime4K profile and target FPS to match computer performance, then set a resolution threshold to skip high-quality sources.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>
3. Build a chain of filters and WebGL shaders if needed, then save it as a preset.
  — <https://chromewebstore.google.com/detail/nexvid-real-time-video-up/hiocbajaikpcckgeagcngaeoioncmbim>
4. Open local files with the built-in player instead of expecting an export of an upscaled video.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>

## Best practices

- Start with anime and cartoons; the author notes them as the best sources.
  — <https://www.reddit.com/r/upscaling/comments/1sl1vy1/i_made_a_browser_extension_that_let_you_upscale/>
- Do not raise FPS above the source rate. The slider caps processed frames rather than generating new ones; a limit of 30 FPS on a 60 FPS source can cause dropped frames.
  — <https://www.reddit.com/r/SideProject/comments/1okqhgx/i_made_a_browser_extension_that_let_you_upscale/>
- Select a profile for hardware load, then tune filters separately. The author recommends unsharp mask and high-pass for sharpness before saving a preset.
  — <https://www.reddit.com/r/upscaling/comments/1sl1vy1/i_made_a_browser_extension_that_let_you_upscale/>
- Check the permission for all-site data access before installing, and restrict the extension to a site whitelist when available.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>

## Superseded by this

- 2025-10-31 — Advice that local files cannot open in NexVid is obsolete after local-video support arrived in Firefox 1.0.5 on 2025-11-10.
- 2026-04-17 — Chrome 1.1.6 is obsolete as the recommended version: the current store listing specifies 1.1.9 from 2026-08-20.

## Still unknown

- Public Firefox version history ends at 1.1.3 on 2026-03-08, while the current listing shows 1.1.9; no changelog between them is available.
- Chrome v1.1.6 and its stats snapshot are confirmed for 2026-04-17, but no primary changelog explains the contents of that update.
- The Chrome store lists location and user activity data collection, while the Firefox listing requires data access for all websites; a comparable permissions breakdown across both platforms is not established.

## Sources

| source | title | read |
|---|---|---|
| https://chromewebstore.google.com/detail/nexvid-real-time-video-up/hiocbajaikpcckgeagcngaeoioncmbim | NexVid - Real-time Video Upscaler & Enhancer - Chrome Web Store | 2026-09-05 |
| https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/ | NexVid - Real-time Video Upscaler & Enhancer – Firefox Add-ons | 2026-09-05 |
| https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/versions/ | Historique de versions de NexVid - Real-time Video Upscaler & Enhancer | 2026-09-05 |
| https://chrome-stats.com/d/hiocbajaikpcckgeagcngaeoioncmbim | NexVid: Real-time Video Upscaler & Enhancer | 2026-09-05 |
| https://www.reddit.com/r/upscaling/comments/1sl1vy1/i_made_a_browser_extension_that_let_you_upscale/ | I made a browser extension that let you upscale and enhance videos from your browser in real-time: NexVid | 2026-09-05 |
| https://www.reddit.com/r/SideProject/comments/1okqhgx/i_made_a_browser_extension_that_let_you_upscale/ | I made a browser extension that let you upscale and enhance videos from your browser in real-time: NexVid | 2026-09-05 |
| https://www.reddit.com/r/chrome_extensions/comments/1okqerj/i_made_an_extension_that_let_you_upscale_and/ | I made an extension that let you upscale and enhance videos from your browser in real-time: NexVid | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:nexvid`, thread `browser-extension-distribution`, 1 dated events 2026-04-17 → 2026-04-17.
- **Practical note:** From 2026-04-17, practitioners evaluating NexVid should check its browser-extension availability through the Chrome Web Store and Firefox Add-ons, while independently verifying current compatibility and capabilities.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
