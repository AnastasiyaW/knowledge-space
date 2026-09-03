---
title: Vidu
category: projects
tags: [project, vidu]
aliases: ["Vidu"]
---

# Vidu

**Development line:** `project:vidu` · thread `vidu`  
**Events:** 6 dated, 2024-04-27 → 2026-07-29 · **Researched:** 2026-09-03 · confidence: medium

## What it is

Vidu — ShengShu’s hosted video-generation product for creators and developers making controlled shots. — Text-to-video, image-to-video, start/end-frame, and multi-reference video. — API functions also cover templates, extension, lip sync, motion sync, upscale, and audio. Limit: Q3 text-to-video runs for 1–16 seconds; creation is asynchronous and credit-priced. Verdict: use it for generated shots and reference continuity, then retain normal editing and QC for the final sequence.

## Development line

- **2024-04-27 — Vidu debuts as a text-to-video model.** On 2024-04-27, ShengShu Technology and Tsinghua introduced Vidu as a text-to-video model. Contemporary reporting described one-click generation of 1080p videos up to 16 seconds long.
- **2024-08-29 — Vidu Studio becomes the recorded commercial web entry point.** By 2024-08-29, the record linked the Vidu Studio website as a commercial access point for Vidu. The available record identifies the site but does not establish a particular feature release on that date.
- **2025-04-22 — Vidu Q1 release adds first-to-last-frame transitions.** On 2025-04-22, the Vidu record pointed to ShengShu's Vidu Q1 release from the preceding day. The Q1 release introduced first-to-last-frame transitions, text-generated background music, anime improvements, and five-second 1080p output.
- **2025-07-10 — Vidu makes a Character-to-Video workflow available.** By 2025-07-10, Vidu exposed a Character-to-Video creation route, establishing a reference-based way to make video. The available evidence does not determine whether that date was the feature launch, a tutorial publication, or a link refresh.
- **2025-09-21 — Vidu’s Russian web and iPhone channels enter the record.** By 2025-09-21, the record linked Vidu’s Russian-language website and iPhone app listing. These links establish the channels’ availability by that date, but they do not establish the app’s original launch date.
- **2026-07-29 — Vidu’s developer platform becomes a documented product channel.** On 2026-07-29, the record linked Vidu’s developer-platform and retention paths, recording a developer-facing distribution channel alongside the web creator. The supplied walkthrough and retention page could not be read, so this entry does not attribute a specific API, model, or pricing release to the date.

## What changed

Vidu development line: — 2024-04-27: Vidu was announced by Tsinghua University and ShengShu as a text-to-video model; contemporaneous reporting described up to 16-second 1080p output. — 2024-08-29: the record linked vidu.studio; independent reporting says the global web product had gone live by 2024-08-02 with text-to-video and image-to-video. The homepage supplies no archived feature delta for 29 August itself. — 2024-09-16: the record pointed to a Text2Video creation route, but the recorded link is malformed and the old route cannot be rendered today; web text-to-video access is evidenced, not a particular release. — 2024-11-25: the record again linked only the homepage. A dated secondary reproduction of ShengShu’s official WeChat announcement places Vidu 1.5 on 2024-11-13, adding 1–3 image multi-subject reference control; it is likely period context, not a proven match to the 25 November post. — 2025-04-22: Vidu Q1 launched globally on 2025-04-21, shifting the product toward controllable transitions, multi-element input, and timed sound generation. — 2025-07-10: the record used Character2Video, the earlier character-reference workflow. Its current successor is Reference to Video, with 1–7 references for subject, scene, style, camera, and effects control. — 2025-09-21: the record added the iPhone app listing. This records mobile distribution, not a model release or a verified app-launch date. — 2026-07-29: the record shifted to API-platform and retention URLs. The legacy retention path now sends users to login and then a 404; the public API privacy policy was effective 2026-04-29. No model change can be attributed safely to the 29 July record. — Found today: Vidu’s API log records Reference-to-Video with 1–7 images on 2025-08-26 and Q3 variants on that endpoint on 2026-04-13; the current model map lists Q3, Q2, and Q1.

## How to use this

As of 2026-09-03, use vidu.com rather than vidu.studio as the canonical creator entry point; choose Q3, Q2, Q1, or Vidu 2.0 by workflow instead of treating Vidu as text-to-video-only or Q1-only, and use Reference to Video or the developer platform when those workflows are required.

1. 1. Open Vidu and choose the generation mode that matches the shot: text, image, reference, or start/end frame.
  — <https://www.vidu.com/>
2. 2. For a recurring character, object, or scene, choose Reference to Video; upload 1–7 reference images, write the action prompt, set resolution and aspect ratio, then generate and download.
  — <https://go.vidu.com/ai-reference-to-video>
3. 3. For API work, sign in to Vidu Platform, create a named API key, add credits, and inspect usage in the dashboard.
  — <https://platform.vidu.com/docs/quick-start>
4. 4. Submit a generation request with a supported model, prompt, duration, aspect ratio, resolution, and callback URL; use text-to-video when no opening image is required.
  — <https://platform.vidu.com/docs/text-to-video>
5. 5. Persist the task ID and query task state until it is success or failed before handing the returned creation URL to the next workflow step.
  — <https://platform.vidu.com/docs/tasks-list>
6. 6. For batches, submit against the organization concurrency limit and plan queue time rather than treating all requests as simultaneous renders.
  — <https://platform.vidu.com/docs/usage-and-limits>

## Best practices

- Use Reference to Video for multi-shot identity and scene continuity; use Image to Video for animating one image or a simple keyframe shot.
  — <https://go.vidu.com/ai-reference-to-video>
- Prepare a reference pack with front, back, and full-body views plus the recurring props or background; keep prompts explicit and documented for recurring characters.
  — <https://www.vidu.com/blog/how-to-maintain-character-consistency-in-ai-videos>
- Treat generated shots as material for an edit: refine keyframes or composites externally when exact continuity matters.
  — <https://www.vidu.com/blog/how-to-maintain-character-consistency-in-ai-videos>
- Keep API keys off the browser and client code; Vidu explicitly warns against exposing them there.
  — <https://platform.vidu.com/docs/quick-start>
- Use callbacks or task polling and budget for the organization-wide five-task default concurrency rather than retrying queued work.
  — <https://platform.vidu.com/docs/usage-and-limits>
- Use off-peak generation only when a deadline can tolerate up to 48 hours; it is cheaper but delayed.
  — <https://platform.vidu.com/docs/image-to-video>
- Pre-screen requests that may violate policy and do not repeatedly resubmit moderated inputs, since repeated violations can suspend an account.
  — <https://platform.vidu.com/docs/content-moderation>

## Superseded by this

- 2024-04-27 — treating Vidu as a research-only text-to-video announcement is obsolete; it is now a browser product and developer API with multiple generation modes.
- 2024-08-29 and 2024-11-25 — treating vidu.studio as the stable entry point is obsolete; it now redirects to https://www.vidu.com/.
- 2025-04-22 — treating Vidu Q1 as the newest model is obsolete; the current model map lists Q3, Q2, and Q1.
- 2025-07-10 — Character2Video as the current product name and workflow is superseded by Reference to Video.
- 2026-07-29 — treating /retention as a public policy endpoint is obsolete; the legacy route now reaches login then a 404, while the public policy is at /docs/privacy-policy.

## Still unknown

- The record contains no source text, so homepage-only or route-only records cannot be safely mapped to a specific release without an archived page or release note.
- The original 2024 WeChat article, the 2025 official X post, the legacy Text2Video and Character2Video pages, and the Feishu page did not render in this research pass.
- The 2024-11-25 link may refer to Vidu 1.5, but the direct recorded links was only the homepage; that association is contextual, not proven.
- The App Store record proves a mobile listing, not its launch date; it shows SILICONWORLD PTE. LTD. as provider while its privacy declaration names ShengShu AI HK Limited, and the relationship is not resolved here.
- Current capabilities and limits come primarily from vendor documentation; independent quality, reliability, licensing, and regional-availability testing was not performed.

## Sources

| source | title | read |
|---|---|---|
| https://www.vidu.com/ | AI Video Generator for Text, Image & Reference Videos | Vidu AI | 2026-09-03 |
| https://go.vidu.com/ai-reference-to-video | Reference to Video AI — Keep Characters Consistent | Vidu AI | 2026-09-03 |
| https://platform.vidu.com/docs/quick-start | Quickstart | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/function-list | Function List | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/text-to-video | Text to Video | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/image-to-video | Image to Video | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/tasks-list | Get Task List | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/usage-and-limits | Usage and Limits | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/content-moderation | Content Moderation | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/update | Update Notice | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/model-map | Model Map | Vidu API | 2026-09-03 |
| https://platform.vidu.com/docs/privacy-policy | Privacy Policy | Vidu API | 2026-09-03 |
| https://www.vidu.com/blog/how-to-maintain-character-consistency-in-ai-videos | How to Maintain Character Consistency in AI Videos | Vidu AI | 2026-09-03 |
| https://english.www.gov.cn/information/202404/27/content_WS662cfb3fc6d0868f4e8e6822.html | China-developed text-to-video large AI model unveiled in Beijing | 2026-09-03 |
| https://www.nsfc.gov.cn/p1/3381/4121/2826/68583.html | 我国自研视频大模型面向全球上线 | 2026-09-03 |
| https://www.aihub.cn/news/vidu-1-5/ | 生数科技正式发布Vidu 1.5版本，限时免费体验 | 2026-09-03 |
| https://www.prnewswire.com/news-releases/vidu-q1-model-launches-globally-offering-unmatched-realistic-vfx-capabilities-from-generating-cinematic-transitions-to-high-fidelity-sound-effects-with-just-a-few-simple-inputs-302433278.html | Vidu Q1 Model Launches Globally | 2026-09-03 |
| https://apps.apple.com/ru/app/vidu-ai-video-generator/id6742448149 | Vidu - Генератор Видео с ИИ | App Store | 2026-09-03 |
| https://mp.weixin.qq.com/s/xAEYGIoJ0EzhszfmXno3UA | Vidu launch WeChat source page (not rendered by crawler) | 2026-09-03 |
| https://www.vidu.studio/ | AI Video Generator for Text, Image & Reference Videos | Vidu AI (redirect from vidu.studio) | 2026-09-03 |
| https://www.vidu.studio/create/text2video | Vidu Text2Video legacy route (not rendered by crawler) | 2026-09-03 |
| https://x.com/ViduAI_official/status/1914303116209697051 | ViduAI_official post (source text unavailable to crawler) | 2026-09-03 |
| https://www.vidu.com/ru/create/character2video | Vidu Character2Video legacy route (not rendered by crawler) | 2026-09-03 |
| https://shengshu.feishu.cn/wiki/AYDDwwLuEiNYe9kWDWYctPxHn9Q | ShengShu Feishu wiki source page (not accessible in this read) | 2026-09-03 |
| https://platform.vidu.com/ | Vidu Platform landing page (not rendered by crawler) | 2026-09-03 |
| https://platform.vidu.com/retention | Vidu Platform retention route (currently redirects to login then 404) | 2026-09-03 |

## Agent brief {#agent-brief}

- **Subject:** `project:vidu`, thread `vidu`, 6 dated events 2024-04-27 → 2026-07-29.
- **Practical note:** As of 2026-09-03, use vidu.com rather than vidu.studio as the canonical creator entry point; choose Q3, Q2, Q1, or Vidu 2.0 by workflow instead of treating Vidu as text-to-video-only or Q1-only, and use Reference to Video or the developer platform when those workflows are required.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
