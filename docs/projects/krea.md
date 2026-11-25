---
title: Krea
category: projects
date: 2026-05-13
tags: [krea, krea-2-release, krea-product-development, krea_realtime_video, project]
aliases: ["Krea", "Krea 2", "Krea Video Restyle"]
---

# Krea

**Development line:** `project:krea` · thread `krea-product-development`  
**Last event:** 2026-05-13 · 5 dated since 2025-01-24 · **Researched:** 2026-11-21 · confidence: medium

## What it is

Krea is an AI image and video generation platform with a web app, an iOS app, and its own image models, including Krea 2, announced on 2026-05-12.

- Users: creators and designers who need style control and moodboard-driven image generation.
- Key capability: Krea 2 supports style references and moodboards; open weights (Raw and Turbo) were published on 2026-06-22 for LoRA training and fast inference.
- Limits: Krea's own claims (for example, outputs in 15 seconds or less) are unverified; pricing and plan tiers were not found on the product page; the open-weight license terms need a direct check.

## Development line

- **2025-01-24 — Train (not verified in this research).** The stub recorded an official Train page; its content and date were not checked.
- **2025-07-03 — Video Restyle (not verified in this research).** The stub recorded a Video Restyle surface; not checked.
- **2025-09-17 — Realtime (not verified in this research).** The Realtime page returned no readable text when fetched.
- **2026-03-03 — iOS app (date not verified).** The App Store listing shows version 1.5.5 but does not show the first-release date; the stub's date was not confirmed.
- **2026-05-13 — Krea 2 (date corrected to 2026-05-12).** Krea's Krea 2 FAQ states it was announced on May 12, 2026.

## What changed

- 2026-05-12 — Krea 2 announced as Krea's first foundation image model "built completely from scratch" (product page FAQ).
- 2026-06-22 — Krea 2 open weights (Raw and Turbo, v1.0) published on Hugging Face (model card).
- 2026-10-19 — iOS app version 1.5.5, "bug fixes and improvements" (App Store; the year is not shown on the page).

## How to use this

1. As of 2026-11, start from the Krea 2 page for the current hosted image workflow, and use "Try K2" from that page for hosted access. — <https://www.krea.ai/krea-2>
2. For self-hosting or fine-tuning, use Krea 2 Raw for LoRA training and Krea 2 Turbo for inference, as the model card advises. — <https://huggingface.co/krea/Krea-2-Raw>
3. For mobile access, install "Krea: AI Images and Videos" from the App Store; the listing developer is Krea AI. — <https://apps.apple.com/ru/app/krea-ai-images-and-videos/id6742134132>
4. Check plan and pricing on the site before a batch project; the product page gave no pricing. — <https://www.krea.ai/krea-2>

## Best practices

- Use style references for a specific look and moodboards for open-ended exploration; the product page recommends moodboards for "more open-ended aesthetics." — <https://www.krea.ai/krea-2>
- Train LoRAs on Raw and run them on Turbo, as the model card advises. — <https://huggingface.co/krea/Krea-2-Raw>
- Read the Krea 2 Community License on the model card before commercial use; secondary summaries disagree on its terms. — <https://huggingface.co/krea/Krea-2-Raw>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Train, Video Restyle, and Realtime: current capabilities, models, and limits were not verified.
- The first-release date of the iOS app.
- Pricing, plan tiers, and usage limits as of 2026-11.
- The full terms of the Krea 2 Community License.
- The "Krea 3" editing-model claims ("edits in under 8 seconds") were not verified.

## Sources

| source | title | read |
|---|---|---|
| https://www.krea.ai/krea-2 | Krea 2 (product page and FAQ) | 2026-11-21 |
| https://apps.apple.com/ru/app/krea-ai-images-and-videos/id6742134132 | Krea: AI Images and Videos (App Store) | 2026-11-21 |
| https://huggingface.co/krea/Krea-2-Raw | Krea 2 Raw model card (search snippet) | 2026-11-21 |

## Agent brief {#agent-brief}

- **Subject:** `project:krea`, thread `krea-product-development`, 5 dated events 2025-01-24 → 2026-05-13 (Krea 2 corrected to 2026-05-12; others not verified).
- **Practical note:** As of 2026-11, evaluate Krea 2 through its official page and open weights. Treat Train, Video Restyle, and Realtime as unverified until their pages are read.
- **Confidence:** medium. Krea 2 page and App Store listing read; Train, Video Restyle, and Realtime pages not usable. Dated supersedes above are the authority for what is obsolete.
