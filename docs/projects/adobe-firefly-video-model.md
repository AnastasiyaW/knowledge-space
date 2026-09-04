---
title: Adobe Firefly Video Model — Firefly Video Model rollout
category: projects
date: 2024-10-14
tags: [adobe-firefly-video-model, adobe_firefly, firefly-video-model-rollout, project]
aliases: ["Adobe Firefly Video", "Adobe Firefly Video Model"]
---

# Adobe Firefly Video Model — Firefly Video Model rollout

**Development line:** `project:adobe-firefly-video-model` · thread `firefly-video-model-rollout`  
**Last event:** 2024-10-14 · 2 dated since 2024-09-11 · **Researched:** 2026-09-04 · confidence: high

## What it is

Adobe Firefly Video Model generates short clips from text and images. In Generate video it sits alongside partner models, so we select Firefly Video explicitly.

- Text-to-Video and Image-to-Video with first and last keyframes.
- Aspect ratio, resolution, shot size, camera angle, camera motion, and style controls.
- Export or transfer of clips to Firefly video editor and Premiere.

Clips are 5 seconds at 24 fps in 540p, 720p, or 1080p across 16:9, 9:16, or 1:1 aspect ratios; higher resolution consumes more generative credits. Use it for planned shots, transitions, and b-roll; assemble longer scenes in an editor from individual clips.

## Development line

- **2024-09-11 — Adobe previews a forthcoming video model for Firefly.** On 2024-09-11, Adobe announced that a video model was planned for Firefly. This set the product direction before users had access to video generation.
- **2024-10-14 — Adobe introduces a beta video-generation experience in Firefly.** On 2024-10-14, Adobe opened a beta video-generation experience in the Firefly web application. This moved the model from an announcement into user testing.

## What changed

Adobe Firefly Video Model moved from an initial announcement to general availability inside the multi-model Generate video interface.

- **2024-09-11:** Adobe announced the model and opened a waitlist, promising Text-to-Video, Image-to-Video, reference images, and camera controls for b-roll and filling editorial gaps.
- **2024-10-14:** Selected community members received early access in the Firefly web app, applying Text-to-Video and Image-to-Video to inserts and new elements in existing footage.
- **2025-02-12:** Public beta launched in the updated Firefly web app, offering text and image generation with 1080p at launch.
- **2025-04-24:** Adobe moved Firefly Video Model to general availability out of beta.
- **2025-07-17:** Adobe improved motion accuracy, expanded video controls, added sound effects generation, and broadened partner model choices in the interface.
- **2026-08-18–19:** Current documentation specifies Firefly Video as an explicit model choice in Generate video, while the unified generation and editing workspace remains in beta.

## How to use this

As of 2024-10-14, practitioners could treat Firefly video generation as a beta workflow available through the Firefly web application; on 2024-09-11 it was only a forthcoming capability.

1. Open Firefly, select Video → Generate video, and choose Firefly Video under Model; the interface may default to Veo 3.1 on first launch.
  — <https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html>
2. Set the resolution, aspect ratio, Shot size, Camera angle, and Motion; Firefly Video supports 540p, 720p, or 1080p, and 16:9, 9:16, or 1:1.
  — <https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html>
3. Write a prompt following shot + subject + action + location + aesthetic, then specify style and camera motion.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
4. For a controlled transition, upload a first frame, a last frame, or both; if using two frames, describe the transition in text.
  — <https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html>
5. Generate the clip, then download it or add it to Project media, Timeline, or the clip editor for further assembly.
  — <https://helpx.adobe.com/firefly/web/unified-generation-and-editing-experience/generate-and-edit-content.html>
6. Check credit consumption using the button next to Generate before running; cost depends on the chosen resolution.
  — <https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html>

## Best practices

- Keep prompts specific: shot, subject, action, location, light, color, and style; more than four subjects often confuse the model.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
- Describe action with verbs and pacing, and set camera movement in either the prompt or the Camera control.
  — <https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html>
- Iterate from a base prompt by adding details along one dimension, and save seed, prompt, and settings for similar results.
  — <https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html>
- Use visually compatible keyframes for Image-to-Video and describe the transition; a first frame disables some manual controls, and a last frame disables Motion.
  — <https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html>
- Upload only images you have rights to use; keep the browser tab open and avoid generating across multiple tabs simultaneously.
  — <https://helpx.adobe.com/cn/firefly/web/work-with-audio-and-video/work-with-video/about-generate-video.html>

## Superseded by this

- 2024-09-11: coming soon and waitlist-only status ended with the public beta on 2025-02-12 and general availability on 2025-04-24.
- 2024-10-14: early access for select community members is obsolete; account-level access and general availability on 2025-04-24 replaced it.
- 2025-02-12: public beta status is obsolete after general availability on 2025-04-24.
- 2025-02-12: the 4K coming soon pledge is not a current Firefly Video setting; documentation from 2026-08-18 lists 540p, 720p, and 1080p for this workflow.

## Still unknown

- Specific available models, Image-to-Video, credit costs, and account entitlements were not verified on an active account; Adobe ties access to plan, region, user type, and regulatory limits.

## Sources

| source | title | read |
|---|---|---|
| https://blog.adobe.com/en/publish/2024/09/11/bringing-gen-ai-to-video-adobe-firefly-video-model-coming-soon | Bringing generative AI to video with Adobe Firefly Video Model | Adobe Blog | 2026-09-04 |
| https://blog.adobe.com/en/publish/2024/10/14/generate-video-beta-on-firefly-web-app | Generate Video (beta) on Firefly Web App | Adobe Blog | 2026-09-04 |
| https://blog.adobe.com/en/publish/2025/02/12/meet-firefly-video-model-ai-powered-creation-with-unparalleled-creative-control | Meet Firefly Video Model: AI-Powered creation with unparalleled creative control | Adobe Blog | 2026-09-04 |
| https://news.adobe.com/news/2025/04/adobe-revolutionizes-ai-assisted-creativity-firefly | Adobe Revolutionizes AI-Assisted Creativity with Firefly, the All-In-One Home for AI Content Creation, with New Partner and Firefly Models | 2026-09-04 |
| https://blog.adobe.com/en/publish/2025/07/17/firefly-adds-new-video-capabilities-industry-leading-ai-models-generate-sound-effects-feature | Firefly adds new video capabilities, industry leading AI models, and Generate Sound Effects feature | Adobe Blog | 2026-09-04 |
| https://helpx.adobe.com/sg/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-text-prompts.html | Generate videos using text prompts | Firefly | 2026-09-04 |
| https://helpx.adobe.com/in/firefly/web/work-with-audio-and-video/work-with-video/generate-videos-using-images.html | Generate videos using images | Firefly | 2026-09-04 |
| https://helpx.adobe.com/uk/firefly/web/work-with-audio-and-video/work-with-video/writing-effective-text-prompts-for-video-generation.html | Writing effective text prompts for video generation | Firefly | 2026-09-04 |
| https://helpx.adobe.com/firefly/web/work-with-audio-and-video/work-with-video/use-style-presets-for-video-generation.html | Use style presets for video generation | Firefly | 2026-09-04 |
| https://helpx.adobe.com/firefly/web/unified-generation-and-editing-experience/generate-and-edit-content.html | Generate and edit images and videos in Firefly | Firefly | 2026-09-04 |
| https://helpx.adobe.com/cn/firefly/web/work-with-audio-and-video/work-with-video/about-generate-video.html | 生成视频常见问题 | Firefly | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:adobe-firefly-video-model`, thread `firefly-video-model-rollout`, 2 dated events 2024-09-11 → 2024-10-14.
- **Practical note:** As of 2024-10-14, practitioners could treat Firefly video generation as a beta workflow available through the Firefly web application; on 2024-09-11 it was only a forthcoming capability.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
