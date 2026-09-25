---
title: Aleph 2.0 — Runway Aleph
category: projects
date: 2026-05-23
tags: [project, runway-aleph, runway-aleph-2]
aliases: ["Aleph 2.0"]
---

# Aleph 2.0 — Runway Aleph

**Development line:** `project:runway-aleph-2` · thread `runway-aleph`  
**Last event:** 2026-05-23 · 1 dated since 2026-05-23 · **Researched:** 2026-09-06 · confidence: medium

## What it is

Aleph 2.0 is Runway’s in-context editor for existing footage, built for teams that need to change a product, background, lighting, or style without rebuilding the shot.

- Keyframe propagation across relevant frames and multi-shot sequences.
- Video generation from video plus text or optional image guidance.
- Export in MP4, ProRes, PNG sequence, or 10-bit SDR; HDR needs a separate conversion step.

Inputs run 2–30 seconds, up to 1080p and 30 fps; the Dev API rate is 28 credits per second with a 56-credit minimum. We use it for source-faithful retouching; test complex moving additions before promising delivery.

## Development line

- **2026-05-23 — Runway introduced Aleph 2.0.** On 2026-05-23, a dated first-party Runway product link identified Aleph 2.0 as a development milestone in the Aleph line. That link names the product, but establishes no specific capabilities, availability terms, pricing, or technical changes.

## What changed

- 2026-05-21 — Aleph 2.0 launched with Edit Studio for paid desktop-web plans, adding 30-second 1080p, localized frame-led edits, and multi-shot propagation.
- 2026-05-23 — Aleph 2.0’s supplied product page records the current product scope, but is undated and does not establish a distinct release or change on this date.
- 2026-06-02 — Aleph 2.0 reached Runway Dev as `aleph2` for video-to-video editing with text and timestamped keyframes.
- 2026-06-22 — Aleph 2.0 became available as a timestamped keyframe node in Figma Weave.
- 2026-07-14 — Aleph 2.0 became callable through Runway MCP’s Edit Video tool.
- 2026-07-30 — Runway Dev sunset `gen4_aleph`; API callers must migrate to `aleph2`.
- 2026-08-10 — Edit Studio gained ProRes 4444 with PCM audio and PNG-sequence export for full-clip Aleph 2.0 edits.
- 2026-08-20 — Aleph 2.0 gained 10-bit Rec.709 SDR delivery; it still does not render native HDR.

## How to use this

1. Open Edit Studio in Runway’s desktop web app and start from an existing video clip.
  — <https://runway.com/news/introducing-aleph-2-and-edit-studio>
2. Upload a 2–30 second, up-to-1080p, maximum-30-fps clip.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
3. Choose a keyframe where the target is clearly visible: a wide frame for an environment change and a close frame for a detail change.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
4. Write an action plus the desired transformation; add a reference image only when it helps guide the subject, product, or style.
  — <https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide>
5. Preview and refine the keyframe edit, select the chosen version, then generate the video.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
6. Choose MP4, ProRes, or PNG sequence before a full-clip generation; a ranged edit always returns MP4.
  — <https://help.runwayml.com/hc/en-us/articles/54396547993491-Exporting-Videos-in-ProRes-and-PNG-Sequence-Formats>

## Best practices

- Start with a short, targeted prompt: an action verb plus the requested transformation; add detail only when needed.
  — <https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide>
- Preview the edited keyframe before paying for video generation, and iterate the image edit until the change is right.
  — <https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio>
- Use Extra motion only when the new movement is absent from both the original clip and the edited keyframe.
  — <https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide>
- For aspect-ratio expansion, use a single-shot clip without cuts and confirm that the preview preserves the original composition.
  — <https://help.runwayml.com/hc/en-us/articles/52264567609363-Expanding-a-video-s-aspect-ratio-with-Edit-Studio>
- Select the delivery format before generation: it cannot be changed afterward, and ProRes or PNG sequence requires a full-clip edit.
  — <https://help.runwayml.com/hc/en-us/articles/54396547993491-Exporting-Videos-in-ProRes-and-PNG-Sequence-Formats>
- Treat one independent seven-scenario test as directional: it found Aleph strongest for conservative packshot, text, and retouch work, while complex newly moving subjects needed cleanup.
  — <https://journal.everypixel.com/runway-aleph-2-vs-gemini-omni>

## Superseded by this

- 2026-06-02 — Prefer `aleph2` over the deprecated `aleph2_alpha` API alias.
- 2026-07-30 — `gen4_aleph` is no longer a usable Runway Dev model identifier; calls fail and must move to `aleph2`.
- 2026-08-20 — Do not plan for native HDR from Aleph 2.0: its current API output is 10-bit SDR, with HDR requiring `/v1/video_to_hdr` afterward.

## Still unknown

- The supplied product page is undated, so its exact contents on 2026-05-23 cannot be reconstructed; the dated launch is 2026-05-21.
- Lineage remains unverified because multiple subject keys share the same history; do not claim a predecessor relationship until it is reviewed.
- No first-party Simplified-Chinese Aleph 2.0 documentation was found; Chinese-language results were third-party tutorials and were not used for the core claims.
- Runway’s generic Edit Studio guide still says Expand is coming soon, while its dedicated Expand Ratio guide documents it as active; the activation date is unknown.

## Sources

| source | title | read |
|---|---|---|
| https://runwayml.com/product/aleph-2 | Aleph 2.0 | Runway (redirects to runway.com) | 2026-09-06 |
| https://runway.com/product/aleph-2 | Aleph 2.0 | Runway | 2026-09-06 |
| https://runway.com/news/introducing-aleph-2-and-edit-studio | Introducing Aleph 2.0 and Edit Studio | 2026-09-06 |
| https://docs.dev.runwayml.com/api-details/api_changelog/ | API Changelog & Updates | Runway Dev | 2026-09-06 |
| https://runway.com/news/aleph-2-in-figma-weave | Aleph 2.0 Is Now in Figma Weave | 2026-09-06 |
| https://runway.com/changelog | Product Updates & Changelog | Runway AI | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/51683104370451-Creating-with-Edit-Studio | Creating with Edit Studio | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide | Aleph 2.0 Prompting Guide | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/54396547993491-Exporting-Videos-in-ProRes-and-PNG-Sequence-Formats | Exporting Videos in ProRes and PNG Sequence Formats | 2026-09-06 |
| https://help.runwayml.com/hc/en-us/articles/52264567609363-Expanding-a-video-s-aspect-ratio-with-Edit-Studio | Expanding a video's aspect ratio with Edit Studio | 2026-09-06 |
| https://docs.dev.runwayml.com/guides/models/ | Available AI Models | Runway Dev | 2026-09-06 |
| https://docs.dev.runwayml.com/guides/pricing/ | API Pricing & Costs | Runway Dev | 2026-09-06 |
| https://journal.everypixel.com/runway-aleph-2-vs-gemini-omni | Runway Aleph 2 vs Gemini Video Omni | 2026-09-06 |

## Agent brief {#agent-brief}

- **Subject:** `project:runway-aleph-2`, thread `runway-aleph`, 1 dated events 2026-05-23 → 2026-05-23.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.