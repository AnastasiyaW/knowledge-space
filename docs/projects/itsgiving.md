---
title: "Itsgiving: itsgiving"
category: "projects"
date: 2026-09-12
tags: ["itsgiving", "project"]
aliases: ["Itsgiving: itsgiving"]
---

# Itsgiving: itsgiving

**Development line:** project:itsgiving · thread itsgiving  
**Last event:** 2026-09-12 · 2 dated since 2026-09-12 · **Researched:** 2026-09-12 · confidence: medium

## What it is

ItsGiving is a Python webcam tool for meeting participants. It detects face expressions and hand/body poses, then overlays matching images or GIFs. It publishes the result as a virtual camera.

It includes 14 built-in reactions, custom assets and poses, and a calibrated v2 detector. It requires Python 3.11 or 3.12. On first run, it downloads three MediaPipe models totaling about 15 MB.

Use the calibrated v2 script. The project documents v1 as fixed-threshold legacy behavior.

## Development line

- **2026-09-12 — ItsGiving - Face/Gesture-to-Meme Streaming Tool.** A webcam tool that tracks face/gestures and shows matching memes in a stream. It integrates with Zoom, Meet, Discord and Teams.
  - The project documents 14 reactions and virtual-camera output for Zoom, Meet, Teams, Discord and OBS. The recommended implementation is \`its\_giving\_v2.py\`. It records a seven-second neutral-face baseline and scores expressions against it. (undated re) — <https://github.com/gazijarin/itsgiving>
  - The project documents 14 reactions and virtual-camera output for Zoom, Meet, Teams, Discord and OBS. The recommended implementation is \`its\_giving\_v2.py\`. It records a seven-second neutral-face baseline and scores expressions against it. (undated re) — <https://github.com/gazijarin/itsgiving>
- **2026-09-12 — ItsGiving Webcam Tool with Face/Gesture Tracking and Meme Integration.** A webcam tool that tracks face/gestures and shows matching memes in a stream. It integrates with Zoom, Meets, Discord and Teams.
  - The project documents 14 reactions and virtual-camera output for Zoom, Meet, Teams, Discord and OBS. The recommended implementation is \`its\_giving\_v2.py\`. It records a seven-second neutral-face baseline and scores expressions against it. (undated re) — <https://github.com/gazijarin/itsgiving>
  - The project documents 14 reactions and virtual-camera output for Zoom, Meet, Teams, Discord and OBS. The recommended implementation is \`its\_giving\_v2.py\`. It records a seven-second neutral-face baseline and scores expressions against it. (undated re) — <https://github.com/gazijarin/itsgiving>

## What changed

The public repository documents a calibrated v2 implementation alongside the fixed-threshold v1 implementation. No separately dated public development step beyond the reviewed date was verified.

## How to use this

1. Create a Python 3.11 or 3.12 virtual environment and install the pinned requirements.
  — <https://github.com/gazijarin/itsgiving>
2. Run \`python its\_giving\_v2.py --calibrate\`. Remain neutral for the seven-second calibration, then run \`python its\_giving\_v2.py\`.
  — <https://github.com/gazijarin/itsgiving>
3. Install a virtual-camera backend for the operating system. Start ItsGiving before the meeting application, then select the published virtual camera in that application's video settings.
  — <https://github.com/gazijarin/itsgiving>

## Best practices

- Keep the dependency pins unchanged. The documented MediaPipe, NumPy and OpenCV compatibility constraints are coupled.
  — <https://github.com/gazijarin/itsgiving>
- Use v2 and recalibrate when needed. Its expression thresholds use the user's neutral-face baseline.
  — <https://github.com/gazijarin/itsgiving>
- When adding a pose, check the pose order before lowering thresholds. The first matching pose wins. Use the HUD and an arm count to tune false triggers.
  — <https://github.com/gazijarin/itsgiving>
- Test reactions before using them in a meeting. The output can trigger automatically and is visible to all call participants.
  — <https://github.com/gazijarin/itsgiving>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The public repository page is undated. It corroborates the reviewed 2026-09-12 entries, but it does not establish the precise release time or show which of the two same-day records corresponds to a distinct project change.
- The reviewed VK URL could not be retrieved publicly during this research.
- No useful Simplified-Chinese source about this specific project was found.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/gazijarin/itsgiving | gazijarin/itsgiving — It's giving... | 2026-09-13 |

## Agent brief {#agent-brief}

- **Subject:** project:itsgiving, thread itsgiving, 2 dated events 2026-09-12 → 2026-09-12.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
