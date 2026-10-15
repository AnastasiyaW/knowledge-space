---
title: "WAN"
category: "projects"
date: 2026-09-26
tags: ["project", "wan", "wan-skills", "wan-video-generation"]
aliases: ["WAN", "Wan", "Wan2.2 dyno"]
---

# WAN

**Development line:** project:wan-skills · thread wan-video-generation  
**Last event:** 2026-09-26 · 6 dated since 2025-09-23 · **Researched:** 2026-09-26 · confidence: low

## What it is

WAN Skills is an Alibaba Wan GitHub package for agent builders. It includes a wan2.7 image-generation-and-editing skill and a PPTX-generation skill. It provides API-call scripts, upload and task-status helpers, and reference instructions. The public repository currently lists two skill directories. Use it for agent-side integration with Wan APIs. It does not show that WAN’s web product has released a video-effects marketplace.

## Development line

- **2025-09-23 — Alibaba Wan 2.5 appeared as a text-to-video model on WaveSpeed.** On 2025-09-23, a WaveSpeed model route identified Alibaba Wan 2.5 as a text-to-video offering. This gave practitioners a named hosted route for video generation with that WAN version.
- **2025-10-01 — Wan 2.2 Lightning assets surfaced for four-step text-to-video workflows.** On 2025-10-01, the linked resources identified a Wan 2.2 Lightning four-step Dyno variant, a matching FP8 ComfyUI artifact, and a workflow page. Together, they point to a faster, workflow-ready inference path for Wan 2.2 text-to-video generation.
- **2026-04-17 — WAN update.** Wan-skills was publicly listed as updated, with two documented skill directories: wan2.7-image-skill and wan-pptx-generator.
- **2026-07-31 — WAN exposed a realtime playground route.** On 2026-07-31, the WAN Create site included a lab playground route labeled realtime. This indicates an interactive realtime entry point for WAN, separate from a model-download or batch-workflow link.
- **2026-09-26 — WAN launches skills platform feature.** WAN launches a platform feature called 'skills' consisting of video manipulation presets, referencing effects originally from Pika. The launch is presented as current even though it is based on last year's effects.
- **2026-09-26 — WAN launches skills feature on its platform.** WAN launched skills \(video manipulation presets\) on its platform. The effects are described as coming from the previous year and are now rebranded as skills. This marks another development step for the WAN project.

## What changed

Public evidence does not independently verify a dated change to the cited WAN web feature. The separately documented Wan-skills repository was last updated on 2026-04-17 and exposes agent-integration skills, not the claimed platform presets.

## How to use this

1. Create an Alibaba Cloud account, activate ModelStudio, and create a DashScope API key.
  — <https://github.com/Wan-Video/Wan-skills>
2. Set DASHSCOPE\_API\_KEY and select the DashScope base URL for the intended region.
  — <https://github.com/Wan-Video/Wan-skills>
3. Clone Wan-skills and install the required skill directory into the AI agent, such as skills/wan2.7-image-skill.
  — <https://github.com/Wan-Video/Wan-skills>
4. For image work, provide a text requirement and optional image URLs. The supplied script submits an asynchronous wan2.7-image task and checks its task status.
  — <https://github.com/Wan-Video/Wan-skills/blob/main/skills/wan2.7-image-skill/scripts/image-generation-editing.py>

## Best practices

- Choose the DashScope regional endpoint explicitly instead of relying on an unstated deployment region.
  — <https://github.com/Wan-Video/Wan-skills>
- Treat image generation as asynchronous and retain the task ID until the status reaches a terminal result.
  — <https://github.com/Wan-Video/Wan-skills/blob/main/skills/wan2.7-image-skill/scripts/image-generation-editing.py>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The cited WAN web page returned no accessible content during review. The claimed 2026-09-26 platform release, its video-manipulation scope, its preset count, and any relationship to Pika effects could not be verified.
- Public material supports an official GitHub project named Wan-skills, but it documents AI-agent API integration for image creation, image editing, and PPTX generation. It does not establish that this is the same product as the cited create.wan.video skills page.
- The two reviewed same-day entries may describe one unavailable platform-page change rather than two independently distinguishable releases.

## Sources

| source | title | read |
|---|---|---|
| https://create.wan.video/lab/skill | WAN Skills | 2026-09-27 |
| https://github.com/Wan-Video/Wan-skills | Wan-Video/Wan-skills | 2026-09-27 |
| https://github.com/wan-video | Wan-Video on GitHub | 2026-09-27 |
| https://github.com/Wan-Video/Wan-skills/blob/main/skills/wan2.7-image-skill/scripts/image-generation-editing.py | image-generation-editing.py | 2026-09-27 |

## Agent brief {#agent-brief}

- **Subject:** project:wan-skills, thread wan-video-generation, 6 dated events 2025-09-23 → 2026-09-26.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** low. Dated supersedes above are the authority for what is obsolete.