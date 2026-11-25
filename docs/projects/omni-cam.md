---
title: "Omni Cam: omnicam — Omnicam"
category: "projects"
date: 2026-09-27
tags: ["omni-cam", "omnicam", "project"]
aliases: ["Omni Cam: omnicam"]
---

# Omni Cam: omnicam — Omnicam

**Development line:** project:omni-cam · thread omnicam  
**Last event:** 2026-09-27 · 7 dated since 2026-09-04 · **Researched:** 2026-11-25 · confidence: high

## What it is

OmniCam is a ComfyUI extension for practitioners who need to reconstruct, author, preview, and adapt camera motion for video workflows.

- Video-camera extraction.
- 3D camera layout and keyframing.
- Playblast creation.
- Profile-based motion output.

All three nodes are experimental, and a compatible socket contract does not certify visual results from a downstream model. Use it as a camera-authoring layer ahead of a supported video workflow, not as a finished video renderer.

## Development line

- **2026-09-04 — Omni Cam: omnicam update.** v0.1.0 was published as the first versioned public release.
- **2026-09-07 — OmniCam ComfyUI release.** OmniCam was announced as a set of ComfyUI tools to extract cameras, arrange frames in a 3D viewport, and compile motion for models.
- **2026-09-07 — OmniCam.** A new ComfyUI node for camera control extracts camera motion from video, arranges frames in a 3D viewport, and compiles motion for a target model.
- **2026-09-07 — other reporting on this date.**
  - The announcement followed a versioned public release: v0.1.0 was published on 2026-09-04. The release documentation supplies the otherwise absent version number, but documents no model-compatibility claim for that initial release. (2026-09-04) — <https://github.com/MajoorWaldi/ComfyUI-Majoor-OmniCam/releases>
- **2026-09-09 — Omni Cam: omnicam update.** v0.3.0 added scene reconstruction, drawn camera paths, a Director scene library, viewport tools, and playblast-quality fixes.
- **2026-09-14 — Omni Cam: omnicam update.** v0.3.2 added the spatial camera editor v2, H3 camera-contract work, and initial Agent integration; v0.3.3 was released later that day with security remediation.
- **2026-09-22 — Omni Cam: omnicam update.** v0.4.0 added Director and Extractor workbench work, camera timing, viewport editing improvements, and H3 and Seedance guide-compiler work.
- **2026-09-27 — Omni Cam: omnicam update.** v0.4.1 fixed Registry scanner environment-variable findings and added automatic smoothing for drawn and placed keys.

## What changed

- 2026-09-04 — v0.1.0 established the public versioned release.
- 2026-09-09 — v0.3.0 added scene-reconstruction work, drawn camera paths, a scene library, viewport tools, and playblast-quality fixes.
- 2026-09-11 — v0.3.1 added Director-console foundations, unified asset and character work, starter assets, and queued extraction.
- 2026-09-14 — v0.3.2 added the spatial-camera-editor v2, H3 camera-contract work, and initial Agent integration; v0.3.3 followed with security remediation.
- 2026-09-22 — v0.4.0 added Director and Extractor workbench changes, camera timing, viewport editing improvements, and H3 and Seedance guide-compiler work.
- 2026-09-27 — v0.4.1 fixed Registry scanner environment-variable findings and added automatic smoothing for drawn and placed keys.

## How to use this

1. Install through ComfyUI Manager by searching for Majoor OmniCam, or clone the repository into ComfyUI/custom_nodes and restart ComfyUI.
  — <https://github.com/MajoorWaldi/ComfyUI-Majoor-OmniCam/blob/main/docs/USER_GUIDE.md>
2. Add OmniCam Director, compose the opening frame in the 3D viewport, insert keyframes, preview the shot, and record a playblast when a reference-video workflow needs one.
  — <https://github.com/MajoorWaldi/ComfyUI-Majoor-OmniCam/blob/main/docs/USER_GUIDE.md>
3. Use an Extractor backend only after its optional dependency is installed; auto tries DPVO, then pycolmap, then OpenCV/SIFT.
  — <https://github.com/MajoorWaldi/ComfyUI-Majoor-OmniCam/blob/main/docs/USER_GUIDE.md>
4. Choose a Monitor profile whose representation and downstream socket match the target workflow, then separately check whether that target has visual certification.
  — <https://git.mitgai.net/MajoorWaldi/ComfyUI-Majoor-OmniCam/blob/main/docs/COMPATIBILITY.md>

## Best practices

- Keep the Director MotionScene as the canonical editable state and treat a playblast as motion reference rather than the final render.
  — <https://github.com/MajoorWaldi/ComfyUI-Majoor-OmniCam/blob/main/docs/USER_GUIDE.md>
- Treat Director, Extractor, and Monitor as experimental; validate the Monitor profile and Motion Tracks surface in the target workflow before depending on them.
  — <https://github.com/MajoorWaldi/ComfyUI-Majoor-OmniCam/blob/main/docs/USER_GUIDE.md>
- Do not equate a valid socket or schema contract with visual certification of the downstream model.
  — <https://git.mitgai.net/MajoorWaldi/ComfyUI-Majoor-OmniCam/blob/main/docs/COMPATIBILITY.md>
- Install required models and optional dependencies deliberately: OmniCam does not auto-download them in the background.
  — <https://github.com/MajoorWaldi/ComfyUI-Majoor-OmniCam/blob/main/docs/USER_GUIDE.md>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The supplied 2026-09-07 labels do not identify which v0.1.0 capability set each same-day item intended to emphasize.
- The compatibility table marks the listed Monitor-profile model certifications as pending; it does not establish visual quality for those target-model integrations.
- No independently dated practitioner discussion with a substantive post-use report was found in the reviewed public results.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/MajoorWaldi/ComfyUI-Majoor-OmniCam | MajoorWaldi/ComfyUI-Majoor-OmniCam | 2026-11-25 |
| https://github.com/MajoorWaldi/ComfyUI-Majoor-OmniCam/releases | Releases · MajoorWaldi/ComfyUI-Majoor-OmniCam | 2026-11-25 |
| https://github.com/MajoorWaldi/ComfyUI-Majoor-OmniCam/blob/main/docs/USER_GUIDE.md | OmniCam User Guide | 2026-11-25 |
| https://git.mitgai.net/MajoorWaldi/ComfyUI-Majoor-OmniCam/blob/main/docs/COMPATIBILITY.md | OmniCam Compatibility | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:omni-cam, thread omnicam, 7 dated events 2026-09-04 → 2026-09-27.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
