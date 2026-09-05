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

NexVid is a browser extension for watching anime, cartoons and web video in Chrome or Firefox.

- Anime4K GPU upscaling for anime and cartoons.
- Quality and FPS profiles for hardware tuning.
- WebGL shaders and custom filters.
- Presets to save custom configurations.
- Local player for disk files.

Processing runs during playback and requires access to all website data; current release is v1.1.9 from 2026-08-20. We can tune playback in real time, but the extension does not replace video export with neural upscaling.

## Development line

- **2026-04-17 — NexVid browser-extension listings appeared for Chrome and Firefox.** On 2026-04-17, NexVid listings appeared on the Chrome Web Store and Firefox Add-ons. The paired listings mark a distribution step across Chrome and Firefox. Public listings on that date show no version number, feature set, availability status, or change log.

## What changed

- 2025-10-27 — Firefox 1.0.2 became the earliest publicly visible release in AMO history.
- 2025-11-10 — Firefox 1.0.5 added local video support and extra effects.
- 2025-12-01 — Firefox 1.1.0 added dark and minimalist themes, raised maximum FPS, and fixed Twitch. Release 1.1.1 fixed profile selection in the minimal interface on the same day.
- 2026-01-20 — Firefox 1.1.2 added experimental shaders and a resolution threshold to skip high-quality video.
- 2026-03-08 — Firefox 1.1.3 added a website whitelist.
- 2026-04-17 — Chrome 1.1.6 was updated; this confirms a Chrome release, not an identical Firefox release on that date.
- 2026-08-20 — Chrome and Firefox both offer 1.1.9; store listings specify Anime4K, performance profiles, shaders, presets, and a local player.

## How to use this

We check extension availability on the Chrome Web Store and Firefox Add-ons from 2026-04-17, and verify compatibility directly.

1. Install NexVid from the Chrome Web Store or Firefox Add-ons, then open the target web video.
  — <https://chromewebstore.google.com/detail/nexvid-real-time-video-up/hiocbajaikpcckgeagcngaeoioncmbim>
2. Select an Anime4K profile and target FPS for hardware capacity, then set a resolution threshold to skip high-quality sources.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>
3. Build a chain of filters and WebGL shaders if needed, then save it as a preset.
  — <https://chromewebstore.google.com/detail/nexvid-real-time-video-up/hiocbajaikpcckgeagcngaeoioncmbim>
4. Use the built-in local player for disk files instead of expecting an export of the upscaled video.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>

## Best practices

- Start with anime and cartoons because they are the best-suited sources.
  — <https://www.reddit.com/r/upscaling/comments/1sl1vy1/i_made_a_browser_extension_that_let_you_upscale/>
- Do not set FPS above the source rate because the slider limits processed frames rather than creating new ones. Setting a 30 FPS limit on a 60 FPS source causes frame drops.
  — <https://www.reddit.com/r/SideProject/comments/1okqhgx/i_made_a_browser_extension_that_let_you_upscale/>
- Pick a profile based on hardware load, then adjust filters separately. Use unsharp mask and high-pass for sharpness, then save the preset.
  — <https://www.reddit.com/r/upscaling/comments/1sl1vy1/i_made_a_browser_extension_that_let_you_upscale/>
- Check all-sites permission requirements before installing, and restrict the extension to a site whitelist when available.
  — <https://addons.mozilla.org/fr/firefox/addon/nexvid-realtime-video-upscaler/>

## Superseded by this

- 2025-10-31 — Claims that NexVid cannot open local files are obsolete since Firefox 1.0.5 added local video support on 2025-11-10.
- 2026-04-17 — Chrome 1.1.6 is obsolete as the recommended release; the current store listing shows 1.1.9 from 2026-08-20.

## Still unknown

- Public Firefox version history ends at 1.1.3 from 2026-03-08, though the current store listing shows 1.1.9; changelogs between them are missing.
- Chrome v1.1.6 and its stats snapshot are confirmed for 2026-04-17, but no primary changelog documents that update.
- The Chrome listing reports collecting location and user activity, while Firefox lists all-sites access. A comparative permission list for both platforms is missing.

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
