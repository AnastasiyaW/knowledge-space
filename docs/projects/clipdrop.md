---
title: Clipdrop
category: projects
tags: [clipdrop, clipdrop-image-editing, project]
aliases: ["Clipdrop", "Clipdrop Relight"]
---

# Clipdrop

**Development line:** `project:clipdrop` · thread `clipdrop-image-editing`  
**Events:** 2 dated, 2022-09-09 → 2023-04-08 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Clipdrop is a browser image toolkit for creators combining Photoshop retouching with separate web generators.

- Background and object removal: remove or replace backgrounds, objects, people, and text
- Relighting: adjust lighting on existing images with virtual lights
- Image enhancement: upscale, denoise, uncrop, resize, and generate from text
- Reimagine: run variation generation in Jasper Document Editor on a Business plan

Clipdrop lists nine browser tools; the free Relight quota is 20 uses per 24 hours.

We use the direct web tools for one-off edits and Jasper for the surviving Reimagine workflow.

## Development line

- **2022-09-09 — Clipdrop launched Relight.** Upload an image, position virtual light sources, then download the result.
- **2023-04-08 — Clipdrop launched Stable Diffusion Reimagine.** Create several new variations from one source image rather than reproduce it exactly.

## What changed

Clipdrop moved image editing from standalone web pages into a split between Clipdrop web tools and Jasper's editor.

- 2022-09-09 — Relight was the tracked capability: upload an image, position virtual light sources, then download the result.
- 2023-04-08 — Stable Diffusion Reimagine was the tracked capability: create several new variations from one source image rather than reproduce it exactly.
- 2026-09-04 — the standalone Reimagine URL redirects to the Clipdrop homepage and Reimagine is absent from the nine-tool Clipdrop web catalog; Jasper documents it inside Document Editor, restricted to Business users.
- 2026-09-04 — the Clipdrop site identifies InitML's February 2023 acquisition by Stability and February 2024 sale to Jasper.

The live direct catalog retains Relight but not Reimagine.

Old Reimagine links are stale entry points, not proof that the feature disappeared.

## How to use this

As of 2023-04-08, we track Clipdrop for relighting and Stable Diffusion reimagination workflows, but verify availability and behavior before choosing either tool.

1. Open the direct Clipdrop catalog and choose the single-purpose tool that matches the edit.
  — <https://clipdrop.co/tools>
2. For Relight, upload the source image on the Relight page.
  — <https://clipdrop.co/relight>
3. Move the virtual light sources, assess the result, and download the selected version.
  — <https://clipdrop.co/relight>
4. For Reimagine, add or upload an image in Jasper Document Editor, hover over it, choose Edit, then select Reimagine; Jasper documents this as a Business-plan tool.
  — <https://help.jasper.ai/hc/en-us/articles/25074326466971-How-to-Add-Images-to-Your-Jasper-Content>
5. Before a batch, check the current quota and resolution tier; free Relight is listed at 20 uses per 24 hours and Pro high-resolution Relight at 1,000 per 24 hours.
  — <https://clipdrop.co/pricing>

## Best practices

- Use Reimagine for variation, not preservation: it creates images inspired by the input and does not reproduce its pixels.
  — <https://stability.ai/news-updates/stable-diffusion-reimagine>
- For Cleanup, paint slightly beyond the unwanted object and include its shadows; Clipdrop notes that the larger mask improves reconstruction.
  — <https://clipdrop.co/cleanup>
- Treat the old standalone Reimagine URL as a redirect, then use Jasper Document Editor instead of building a workflow around the legacy page.
  — <https://help.jasper.ai/hc/en-us/articles/25074326466971-How-to-Add-Images-to-Your-Jasper-Content>
- Plan volume before production: the public free quota for Relight, Cleanup, and x2 Upscale is 20 uses per 24 hours.
  — <https://clipdrop.co/pricing>

## Superseded by this

- 2023-04-08 — the standalone Stable Diffusion Reimagine web-page workflow is obsolete: its Clipdrop URL now redirects to the homepage; current documented access is Jasper Document Editor > Edit > Reimagine for Business users.
- 2022-09-09 — treating Clipdrop as an independent InitML product is obsolete: the current Clipdrop site says InitML was acquired by Stability in 2023 and sold to Jasper in 2024.

## Still unknown

- The source provided no independently verifiable content, so it supports no claim.
- No current first-party page located a public standalone Reimagine interface or disclosed its present quota; verified current access is Jasper Document Editor for Business users.

## Sources

| source | title | read |
|---|---|---|
| https://clipdrop.co/ | Create stunning visuals in seconds with AI. | 2026-09-04 |
| https://clipdrop.co/tools | Tools — Clipdrop | 2026-09-04 |
| https://clipdrop.co/relight | Clipdrop - Relight | 2026-09-04 |
| https://clipdrop.co/stable-diffusion-reimagine | Create stunning visuals in seconds with AI. (redirected from Stable Diffusion Reimagine) | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-reimagine | Stable Diffusion Reimagine — Stability AI | 2026-09-04 |
| https://help.jasper.ai/hc/en-us/articles/25074326466971-How-to-Add-Images-to-Your-Jasper-Content | How to Add Images to Your Jasper Content — Jasper Help Center | 2026-09-04 |
| https://clipdrop.co/cleanup | Clipdrop - Cleanup | 2026-09-04 |
| https://clipdrop.co/pricing | Clipdrop - pricing | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:clipdrop`, thread `clipdrop-image-editing`, 2 dated events 2022-09-09 → 2023-04-08.
- **Practical note:** As of 2023-04-08, practitioners should treat Clipdrop as having dated public references for relighting and Stable Diffusion reimagination workflows, while verifying current availability and behavior before selecting either tool.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.