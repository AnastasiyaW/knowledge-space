---
title: Haiper — Public launch and iOS availability
category: projects
date: 2024-03-16
tags: [haiper, project, public-launch-and-ios-availability]
aliases: ["Haiper"]
---

# Haiper — Public launch and iOS availability

**Development line:** `project:haiper` · thread `public-launch-and-ios-availability`  
**Last event:** 2024-03-16 · 2 dated since 2024-03-13 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Haiper was a cloud video platform for creators and integrators, competing directly with Runway in text-to-video and image-to-video.

- Video generation: text-to-video, image-to-video, keyframe conditioning, video-to-video, and text-to-image.
- Client access: web, iOS, and HTTP API (formerly).

Published 2.x documentation lists 540p and 720p output at 5–8 credits per second, but neither paid access nor a completed new job is verified. Do not choose Haiper for a new production workflow, and treat the API as legacy until an authorized test job succeeds.

## Development line

- **2024-03-13 — Haiper’s official website was publicly referenced.** The service offered free short text-to-video, image animation, and repaint for 2 seconds in HD or up to 4 seconds at lower quality.
- **2024-03-16 — Haiper’s iOS app was publicly linked.** Public links connected to Haiper’s Apple App Store listing and to earlier Haiper materials on 2024-03-16. This documents public iOS app availability or promotion at that time. Available evidence does not establish the app’s capabilities, release status, or accompanying announcement text.

## What changed

- 2024-03-13 — Haiper’s web address became the entry point. The public beta offered free short text-to-video, image animation, and repaint for 2 seconds in HD or up to 4 seconds at lower quality.
- 2024-03-16 — An App Store URL joined the web route. This confirmed an iOS distribution path in product links, though not the app release date.
- 2024-10-21 — Haiper 2.0 and Templates expanded the product from base generation to model versions and template video creation.
- 2024-12-18 — Haiper 2.5 launched in an API integration with VEED, shifting focus toward partner and API workflows.
- 2025-03-20 — Microsoft hired two Haiper cofounders.
- 2025-06-23 — NetMind bought the Haiper AI model, transferring ownership of the technology.
- 2026-09-04 — The domain and API documentation remain live, but no verified new user login, payment, or completed generation exists.

## How to use this

From 2024-03-16, treat Haiper as having a publicly referenced web presence and an iOS distribution path, while verifying current availability and capabilities directly before relying on either.

1. Verify that the provider actually issues an API key after topping up. If no key arrives, stop: the public launch path remains unverified.
  — <https://docs.haiper.ai/api-reference/authentication>
2. With a valid key, submit one single text-to-video job to the documented endpoint and save the generation_id.
  — <https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video>
3. Poll status by generation_id. Handle pending, processing, post_processing, and failed as distinct states.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-status>
4. Request results only after succeed. The detail endpoint returns the video URL and outputs.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-detail>

## Best practices

- Do not store the sole copy of a video or project in the Haiper cloud: user reports from early February 2025 document site outages and lost projects after shutdown.
  — <https://uk.trustpilot.com/review/haiper.ai>
- Pass is_public=false explicitly for client assets: the published API sets the default to true.
  — <https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video>
- Build rate limits into your client: documentation caps traffic at 500 HTTP requests per minute and 40 concurrent generations; do not retry blindly on 429.
  — <https://docs.haiper.ai/api-reference/rate-limits>
- Do not query details before status returns succeed: request status first and detail second to prevent false successes and empty links.
  — <https://docs.haiper.ai/api-reference/endpoint/get-creation-detail>

## Superseded by this

- 2024-03-05—2024-03-13: Advice to sign up for the free consumer beta and generate videos in the web app is obsolete for new users; consumer access is unverified following events in 2025.
- 2024-03-16: Advice to install the app via the original App Store URL is obsolete as an active onboarding route; the URL returned no live product page during inspection.
- 2024-12-18: The Haiper 2.5 API announcement with VEED is a historical description of integration, not proof that the API or partner route accepts new jobs today.
- Historical pricing from published documentation is not a live offer until key provisioning and a successful job are confirmed.

## Still unknown

- Haiper issued no official dated statement on closing its consumer product; February 2025 shutdown relies on user reports and secondary sources rather than company notice.
- No authorized API job ran and no new key issuance was verified, so published documentation may be an abandoned legacy artifact.
- The original App Store URL returned no live listing during inspection; its regional status, delisting, and accessibility to existing users remain unconfirmed.
- NetMind confirmed purchasing the model, but whether NetMind offers it to new users today remains unverified.

## Sources

| source | title | read |
|---|---|---|
| https://haiper.ai/ | Haiper - AI Video Generator | 2026-09-04 |
| https://apps.apple.com/app/id6468952574 | Apple App Store URL, app id 6468952574 | 2026-09-04 |
| https://techcrunch.com/2024/03/05/competition-in-ai-video-generation-heats-up-as-deepmind-alums-unveil-haiper/ | Competition in AI video generation heats up as DeepMind alums unveil Haiper | 2026-09-04 |
| https://testapp.haiper.ai/home | Unlock Creativity with AI Content Generator Tools | Haiper | 2026-09-04 |
| https://testapp2.haiper.ai/blog/haiper-partners-with-veed | Haiper Launches Its 2.5 Model-Powered API with VEED | 2026-09-04 |
| https://sifted.eu/articles/microsoft-haiper-ai-hires-video-sora-inflection/ | Exclusive: Microsoft scoops up talent from AI video startup Haiper | 2026-09-04 |
| https://sifted.eu/articles/haiper-ai-sold-for-parts | Exclusive: Haiper AI sold for parts after Microsoft poaches cofounders | 2026-09-04 |
| https://uk.trustpilot.com/review/haiper.ai | Haiper Reviews | Read Customer Service Reviews of haiper.ai | 2026-09-04 |
| https://docs.haiper.ai/llms.txt | Haiper documentation index | 2026-09-04 |
| https://docs.haiper.ai/pricing | Pricing for Haiper Web App & iOS App - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/authentication | Authentication - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/2-0-text-to-video | Text to Video - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/get-creation-status | Get Creation Status - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/endpoint/get-creation-detail | Get Creation Detail - Haiper | 2026-09-04 |
| https://docs.haiper.ai/api-reference/rate-limits | Rate Limits - Haiper | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:haiper`, thread `public-launch-and-ios-availability`, 2 dated events 2024-03-13 → 2024-03-16.
- **Practical note:** From 2024-03-16, practitioners should treat Haiper as having a publicly referenced web presence and an iOS distribution path, while verifying current availability and capabilities directly before relying on either.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
