---
title: Topaz Labs Astra — Astra development
category: projects

tags: [astra, astra-development, project, topaz-labs:astra]
aliases: ["Topaz Labs Astra"]
---

# Topaz Labs Astra — Astra development

**Development line:** `project:astra` · thread `astra-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: medium

## What it is

Topaz Labs Astra is a cloud tool for AI video creators and restoration.
It runs two modes: Creative draws in new details, and Precise keeps the original structure.
Current models and rendering are already inside Topaz for Web.
The standalone Astra interface closes on 2026-09-30.
Pick Precise for controlled restoration, pick Creative for deliberate generative rework, and check every result.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2025-06-25 — Astra operated as a separate subscription web app, not as a Topaz Video feature. Its focus was generative creative upscale to build new visual material. Community posts from that day show a split workflow: local Starlight Mini for base work, and Astra for fragments needing creative reconstruction. This does not verify the public launch date.
- 2025-12-24 — The Realism Update added Starlight Precise 2, Scene Controls, and batch rendering to Astra.
- 2026-02-20 — The Local Update added cloud Starlight Fast 2, Scene Controls, and Batch Rendering to Astra.
- 2026-03-31 — The Precision Update added cloud Starlight Precise 2.5 for cleaner faces, fabric, and text when upscaling AI video to 4K.
- 2026-05-19 — The Workflows Update added the Hyperion 2 SDR-to-HDR model to Astra.
- 2026-09-03 — Topaz moved Astra models and libraries into Topaz for Web. Subscriptions, credits, and processing costs carry over. The Astra interface shuts down 2026-09-30.

## How to use this

No practitioner workflow change is proposed as of 2025-06-25: the dated link alone establishes no verified product-development fact.

1. Open Topaz for Web and sign in with your Topaz account; files and credits already transferred from Astra.
  — <https://www.topazlabs.com/web/faq>
2. Upload an H.264 MP4 video; run CFR conversion first if the frame rate is variable.
  — <https://docs.topazlabs.com/astra/quick-start>
3. Choose Precise to keep original footage, or Creative to rework details. In Astra 2, set Creativity and Sharpness from 1 to 5 and write a descriptive prompt instead of commands.
  — <https://docs.topazlabs.com/astra/modes-and-models>
4. Set render parameters and range, start processing, wait for completion, and download the output.
  — <https://docs.topazlabs.com/astra/quick-start>

## Best practices

- Split tasks by goal: Precise restores original footage, Creative generates new detail.
  — <https://www.topazlabs.com/astra>
- Check faces, small text, and background subjects frame by frame: user tests from 2025-06-25 showed distortion on distant faces and text after creative reconstruction.
  — <https://community.topazlabs.com/t/starlight-mini-astra/92744>
- Test a short clip before a full render: early user tests showed Astra spent credits even on brief previews.
  — <https://community.topazlabs.com/t/topaz-video-ai-and-astra/92566>

## Superseded by this

- 2025-06-25: treating Astra as a desktop Topaz Video feature is obsolete; it was a separate subscription web app.
- 2026-09-03: instructions to work only through Astra are obsolete; models, library, and credits are now in Topaz for Web, and the Astra interface closes 2026-09-30.

## Still unknown

- The source post text from 2025-06-25 is not available to automated inspection, so we cannot verify whether it was a launch announcement, a review, or a link to an active service.
- The response schema lacks event_findings and new_events fields, so dated changes sit in what_changed.
- No dated primary announcement confirms a public launch on 2025-06-25; a Topaz staff reply that day confirms only the separate subscription web app.

## Sources

| source | title | read |
|---|---|---|
| https://community.topazlabs.com/t/topaz-video-ai-and-astra/92566 | Topaz Video AI and Astra | 2026-09-05 |
| https://community.topazlabs.com/t/starlight-mini-astra/92744 | Starlight Mini + Astra | 2026-09-05 |
| https://docs.topazlabs.com/astra/quick-start | Quick Start | 2026-09-05 |
| https://docs.topazlabs.com/astra/modes-and-models | Modes and Models | 2026-09-05 |
| https://www.topazlabs.com/astra | Astra - Creative Video Upscaling for AI Videos up to 4K Quality | 2026-09-05 |
| https://www.topazlabs.com/updates | Topaz Labs | Updates | 2026-09-05 |
| https://www.topazlabs.com/updates/realism | Topaz Labs | Realism Update | 2026-09-05 |
| https://www.topazlabs.com/updates/local | Topaz Labs | Local Update | 2026-09-05 |
| https://www.topazlabs.com/updates/precision | Topaz Labs | Precision Update | 2026-09-05 |
| https://www.topazlabs.com/web/faq | Astra to Web | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:astra`, thread `astra-development`, 0 dated events - → -.
- **Practical note:** No practitioner workflow change is proposed as of 2025-06-25: the dated link alone establishes no verified product-development fact.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
