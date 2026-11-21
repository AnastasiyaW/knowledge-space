---
title: DLSS 4.5 — Graphics technology
category: projects
date: 2026-03-11
tags: [dlss, graphics-tech, graphics_tech, project]
aliases: ["DLSS 4.5"]
---

# DLSS 4.5 — Graphics technology

**Development line:** `project:dlss` · thread `graphics-tech`  
**Last event:** 2026-03-11 · 1 dated since 2026-03-11 · **Researched:** 2026-11-21 · confidence: medium

## What it is

DLSS 4.5 is the version of NVIDIA's AI upscaling and frame generation suite named in NVIDIA's March 2026 GeForce RTX announcement for GDC 2026.

- Components: Super Resolution, Frame Generation, Multi Frame Generation, Ray Reconstruction and Reflex (companion).
- Users: game developers who integrate DLSS, and GeForce RTX gamers who enable it in games.
- Key capability: DLSS 4.5 adds Dynamic Multi Frame Generation, which adjusts the generated-frame count to a target frame rate, and a 6X mode.
- Limits: Multi Frame Generation requires GeForce RTX 50 Series or RTX PRO Blackwell GPUs; the 4.5 features need Game Ready Driver 595.79 WHQL or newer.

## Development line

- **2026-03-10 — NVIDIA published its GDC 2026 GeForce RTX announcements.** On 2026-03-10 NVIDIA published a GeForce RTX announcement for GDC 2026. We keep the official NVIDIA link on the DLSS 4.5 line as a milestone until we review the source. The dated link alone does not show DLSS 4.5 features, availability, or performance. (The stub recorded 2026-03-11; the article byline reads March 10, 2026.)

## What changed

- 2026-03-10 — DLSS 4.5 named in NVIDIA's GDC 2026 announcement; DLSS 4.5 Super Resolution available to all GeForce RTX gamers in the NVIDIA app.
- 2026-03-31 — DLSS 4.5 Dynamic Multi Frame Generation and 6X mode released as DLSS overrides in an opt-in NVIDIA app beta for GeForce RTX 50 Series owners. NVIDIA says an official release will follow at a later date.
- 2026-10-16 — the DLSS 4.5 Unreal Engine plugin package is dated 2026.10.16 and labeled v8.9.0 on NVIDIA's developer page (the page was last updated October 2026).
- Announced integrations: NVIDIA's March list gave launch dates for several titles (for example Samson on April 8 and Directive 8020 on May 12); none of those launches was re-verified as of 2026-11.

## How to use this

1. Enable DLSS 4.5 Super Resolution in games that list it; it is available in the NVIDIA app for GeForce RTX gamers.
  — <https://www.nvidia.com/en-us/geforce/news/gdc-2026-nvidia-geforce-rtx-announcements/>
2. For Dynamic Multi Frame Generation and 6X mode, use a GeForce RTX 50 Series or RTX PRO Blackwell GPU and opt in through the NVIDIA app beta (Settings > About).
  — <https://www.nvidia.com/en-us/geforce/news/gdc-2026-nvidia-geforce-rtx-announcements/>
3. Install GeForce Game Ready Driver 595.79 WHQL or newer for all DLSS 4.5 features.
  — <https://www.nvidia.com/en-us/geforce/news/gdc-2026-nvidia-geforce-rtx-announcements/>
4. For integration, use the DLSS plugins listed on NVIDIA's developer page; the Unreal Engine plugin is v8.9.0 (2026.10.16). Unity Super Resolution needs Unity 2021.2 Beta or newer.
  — <https://developer.nvidia.com/rtx/dlss>
5. Check each game's own DLSS settings before assuming a feature is present; NVIDIA's list is announced integrations, not verified releases.
  — <https://www.nvidia.com/en-us/geforce/news/gdc-2026-nvidia-geforce-rtx-announcements/>

## Best practices

- Set a target frame rate with Dynamic Multi Frame Generation rather than a fixed multiplier, since NVIDIA describes it as adjusting the multiplier to reach the target.
  — <https://www.nvidia.com/en-us/geforce/news/gdc-2026-nvidia-geforce-rtx-announcements/>
- Use Ray Reconstruction for ray-traced scenes; NVIDIA describes it as replacing hand-tuned denoisers with AI-generated pixels.
  — <https://developer.nvidia.com/rtx/dlss>

## Superseded by this

- No DLSS feature is shown as removed. DLSS 4.5 adds Dynamic Multi Frame Generation and a second-generation transformer model to DLSS 4, per NVIDIA's descriptions.

## Still unknown

- Whether the 6X mode and Dynamic Multi Frame Generation have reached a general release: the March announcement says only that an official release will follow.
- Frame Generation hardware requirements by GPU generation: the developer page gives no version-specific list, and the announcement names only the Multi Frame Generation hardware.
- Status of the 20 announced DLSS 4.5 integrations as of 2026-11: launch dates were given in March and were not re-checked.
- The stub's event date (2026-03-11) differs from the article byline (2026-03-10); we list the byline date.

## Sources

| source | title | read |
|---|---|---|
| https://www.nvidia.com/en-us/geforce/news/gdc-2026-nvidia-geforce-rtx-announcements/ | NVIDIA GDC 2026 GeForce RTX announcements | 2026-11-21 |
| https://developer.nvidia.com/rtx/dlss | NVIDIA DLSS developer page | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:dlss`, thread `graphics-tech`, 1 dated event (NVIDIA GDC 2026 announcement, 2026-03-10); Dynamic MFG beta 2026-03-31; plugin 2026.10.16.
- **Practical note:** Dynamic MFG and 6X were a beta in March 2026; verify per-game support before promising a feature. Driver 595.79 WHQL or newer is required for all 4.5 features.
- **Confidence:** medium. Announcement and developer page are primary; per-game status and general availability are unverified. Dated supersedes above are the authority for what is obsolete.
