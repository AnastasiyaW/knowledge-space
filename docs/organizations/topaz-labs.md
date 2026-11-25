---
title: "Topaz Labs: topaz-labs-wonder-4-image-hdr-2026 — Topaz Labs Wonder 4 Image Hdr 2026"
category: "organizations"
date: 2026-11-19
tags: ["organization", "topaz-labs", "topaz-labs-wonder-4-image-hdr-2026"]
aliases: ["Topaz Labs: topaz-labs-wonder-4-image-hdr-2026"]
---

# Topaz Labs: topaz-labs-wonder-4-image-hdr-2026 — Topaz Labs Wonder 4 Image Hdr 2026

Topaz Wonder 4 and Image HDR are image restoration and HDR models, an alternative to multi-pass Adobe Photoshop and Magnific AI workflows.

**Development line:** organization:topaz-labs · thread topaz-labs-wonder-4-image-hdr-2026  
**Last event:** 2026-11-19 · 2 dated since 2026-11-19 · **Researched:** 2026-11-20 · confidence: medium

## What it is

Topaz Wonder 4 and Image HDR are neural models for image restoration and dynamic-range reconstruction. They are built as an alternative to multi-pass pipelines in Adobe Photoshop and Magnific AI.

- Wonder 4 works on all image regions at once. It upscales, denoises, deblurs, repairs compression artifacts and recovers faces in a single pass, with no manual sliders.
- Image HDR turns standard dynamic range photos into high dynamic range JPEGs, with highlight expansion for HDR displays.

Processing is bound by supported resolution limits. It needs heavy compute or per-generation cloud credits. One region-routed pass replaces several separate enhancement steps.

## Development line

- **2026-11-19 — Topaz releases Wonder 4 and Image HDR models.** Topaz announced two models. Wonder 4 upscales, sharpens and denoises across several regions and is built on a Mixture of Experts architecture. Image HDR converts standard images to JPEG HDR. A Comfy workflow for Wonder 4 was also noted, priced at $0.11 per upscale up to 8 MP, along with a Black Friday discount promotion.
- **2026-11-19 — Topaz Labs releases Wonder 4 and Image HDR models.** Topaz Labs announced two AI models. Wonder 4 is a multi-region upscaling, sharpening and denoising model on a Mixture of Experts architecture. Image HDR converts standard images to JPEG HDR. Wonder 4 workflows in Comfy and a Black Friday discount period were also mentioned.
- **2026-11-19 — other reporting on this date.**
  - The Mixture of Experts architecture routes image regions to specialized sub-networks, so denoising, deblurring, compression repair and face recovery run at the same time with no manual sliders. It deploys across Topaz web, mobile, desktop applications and ComfyUI. (2026-11-19) — <https://www.topazlabs.com/updates/nov2026>
  - Image HDR converts standard dynamic range photos into high dynamic range JPEGs for HDR displays, with highlight and contrast optimization. It is the tonal companion to the Wonder 4 spatial restoration pipeline. (2026-11-19) — <https://www.topazlabs.com/updates/nov2026>

## What changed

Restoration used to chain separate neural networks for denoising, deblurring, sharpening and face reconstruction. That often compounded border artifacts and structural distortion.

Now a Mixture of Experts model analyzes each region in context and sends it to specialized sub-networks at the same time. Manual sliders are gone, replaced by automatic single-pass routing.

Color handling grew from standard dynamic range to automatic HDR JPEG tone reconstruction. Deployment grew from desktop standalone suites to ComfyUI node workflows and API endpoints.

## How to use this

1. Import an image into the Topaz application, the web workspace or a ComfyUI node environment.
  — <https://www.topazlabs.com/updates/nov2026>
2. Select Wonder 4. It upscales, denoises, deblurs and recovers faces in one pass, with no manual sliders.
  — <https://www.topazlabs.com/updates/nov2026>
3. Apply Image HDR when the target is an HDR-capable display. It reconstructs standard dynamic range images as high dynamic range JPEGs.
  — <https://www.topazlabs.com/updates/nov2026>
4. Export the image. Stay within the supported resolution limit of up to 8 MP per generation, under credit-based billing.
  — <https://www.topazlabs.com/updates/nov2026>

## Best practices

- Use Wonder 4 as one single-pass restoration stage. Do not chain separate denoise, deblur and sharpen models, so border artifacts do not compound.
  — <https://www.topazlabs.com/updates/nov2026>
- Keep Image HDR for display pipelines that support HDR gain maps or wide dynamic range. It is not meant for standard print workflows.
  — <https://www.topazlabs.com/updates/nov2026>

## Superseded by this

- Manual multi-stage adjustment of sharpening, denoising and face enhancement sliders is replaced by automatic region routing in a single Mixture of Experts pass.
  — <https://www.topazlabs.com/updates/nov2026>

## Still unknown

- Reddit community discussion and third-party benchmarks could not be confirmed, because no direct URLs were found.
- Local offline GPU requirements and inference benchmarks for Wonder 4 are not fully specified in the cloud and ComfyUI release documentation.

## Sources

| source | title | read |
|---|---|---|
| https://www.topazlabs.com/updates/nov2026 | Topaz Labs November 2026 Updates: Wonder 4 and Image HDR | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** organization:topaz-labs, thread topaz-labs-wonder-4-image-hdr-2026, 2 dated events 2026-11-19 → 2026-11-19.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
