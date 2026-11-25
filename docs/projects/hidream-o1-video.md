---
title: "HiDream-O1-Video-1.0: hidream-o1-video — Hidream O1 Video"
category: "projects"
date: 2026-09-17
tags: ["hidream-o1-video", "project"]
aliases: ["HiDream-O1-Video-1.0: hidream-o1-video"]
---

# HiDream-O1-Video-1.0: hidream-o1-video — Hidream O1 Video

**Development line:** project:hidream-o1-video · thread hidream-o1-video  
**Last event:** 2026-09-17 · 1 dated since 2026-09-17 · **Researched:** 2026-11-25 · confidence: medium

## What it is

HiDream-O1-Video-1.0 is a video generation model from HiDream for generating synchronized audio-video clips from text, images or video.

The announcement bills it as HiDream's first native omni-modal video model, producing 1080p clips of 5-20 seconds with synchronized audio and video. The API documentation lists it under the HiDream-O series with model ID HiDream-O1-Video-1.0. The API runs asynchronously: submit a task and poll for the result using task\_id.

## Development line

- **2026-09-17 — HiDream-O1-Video-1.0 Release Announcement.** HiDream announced the first native omni-modal video model, designated HD-V1, taking text, image, and video input to generate 1080p clips 5-20 seconds long. It features physics motion, intent understanding, duration control, and synchronized audio and video. It claimed rank #4 on Artificial Analysis and #8 on Arena.ai image-to-video leaderboards. Available via API only.
  - The API documentation describes HiDream-O1-Video-1.0 as a single-image-to-video model. It takes one reference image as a public URL or Base64 data plus a text prompt, returning one video. Output keeps the input image aspect ratio, with duration either dynamic or fixed at 10 seconds. That scope is narrower than the announcement's text, image, and video input and 5-20 second range. The documentation also lists HiDream-O1-Video-1.1, supporting t2v, i2v, dual for first and last frame, and ref reference tasks, with 480p to 4K output and 5-16 second durations. (undated) — <https://hiharness.ai/docs/hidream_o/video/introduction.html>

## What changed

The model is now available, API only. The announcement ranks it #4 on the Artificial Analysis Image-to-Video (With Audio) leaderboard and #8 on the Arena.ai Image-to-Video leaderboard. The API documentation also lists HiDream-O1-Video-1.1, adding text-to-video, first-frame, first-and-last-frame, and reference-to-video modes.

## How to use this

1. Submit a generation task to the video generation request endpoint using model ID HiDream-O1-Video-1.0. Provide one reference image as a public URL or Base64 data, plus a text prompt.
  — <https://hiharness.ai/docs/hidream_o/video/introduction.html>
2. Read result.task\_id from the response, then poll the video result endpoint with that task\_id until result.status is 1.
  — <https://hiharness.ai/docs/hidream_o/video/introduction.html>
3. For HiDream-O1-Video-1.1, set task\_type to t2v, i2v, dual or ref to choose the generation mode.
  — <https://hiharness.ai/docs/hidream_o/video/introduction.html>

## Best practices

- Follow the per-mode input rules for HiDream-O1-Video-1.1. t2v takes only a text prompt. i2v takes one first-frame image plus text. dual takes two images for first and last frame plus text. For these three modes, do not pass video or audio, and for t2v do not pass images either. ref takes at most 10 images and at most 1 video, with at least one present, plus optional audio and text.
  — <https://hiharness.ai/docs/hidream_o/video/introduction.html>
- Pass wh\_ratio only for t2v and ref tasks in HiDream-O1-Video-1.1. Do not send it for i2v or dual.
  — <https://hiharness.ai/docs/hidream_o/video/introduction.html>
- Use a polling loop rather than waiting on a single response, because the API is asynchronous.
  — <https://hiharness.ai/docs/hidream_o/video/introduction.html>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The announcement describes text, image, and video input and 5-20 second clips. The API documentation describes 1.0 as single-image input with dynamic or 10-second duration. It is unclear whether the documentation lags behind or the announcement overstated capability.
- Leaderboard rankings (#4 Artificial Analysis, #8 Arena.ai) come only from the announcement and could not be verified on the linked documentation.
- Pricing, rate limits, and plans to release open weights are not stated.
- The documentation page carries no date.

## Sources

| source | title | read |
|---|---|---|
| https://hiharness.ai/docs/hidream_o/video/introduction.html | HiDream-O Series Video Models \(API documentation\) | 2026-09-17 |

## Agent brief {#agent-brief}

- **Subject:** project:hidream-o1-video, thread hidream-o1-video, 1 dated events 2026-09-17 → 2026-09-17.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.