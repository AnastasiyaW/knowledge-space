---
title: Krea AI — Video generation
category: organizations
tags: [krea-ai, krea_ai, organization, video-generation]
aliases: ["Krea AI"]
---

# Krea AI — Video generation

**Development line:** `organization:krea-ai` · thread `video-generation`  
**Events:** 3 dated, 2025-04-16 → 2025-08-29 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Krea AI is a browser-based toolkit for designers and video teams that generates, edits, enhances, and animates images and video, and trains reusable styles.

- **Image and Video:** choose its own Krea 2 or a third-party model for the task.
- **Realtime:** use a canvas with live generation from text, drawing, a webcam, or the screen.
- **Edit, Enhancer, and Train:** make local edits, upscale images, and train a LoRA for a style, character, or product.

Documentation for an ordinary video render lists 5–12 seconds, 1–10 minutes, and from 1 000 compute credits.

Krea is a workspace for comparing models and iterating quickly on visuals. Before a specific task, check the model choice, credit limits, and Stage status.

## Development line

- **2025-04-16 — Krea AI surfaced a video experience with an OL Flux identifier.** On 2025-04-16, a dated Krea AI link pointed to its video experience, with URL parameters identifying an OL Flux variant. This is a material step in Krea AI's video-generation development line. The links do not establish the capability details, availability, or launch wording.
- **2025-04-18 — Krea AI linked to its Stage product surface.** On 2025-04-18, a dated Krea AI link pointed to the company's Stage product path. This is a material step in the video-generation line because it identifies a distinct product surface. The links do not establish Stage's feature set, availability, or whether that date marked its launch.
- **2025-08-29 — Krea AI published an announcement for Realtime Video.** On 2025-08-29, Krea AI published a blog page whose URL identifies an announcement for Realtime Video. This is a material development in the company's video-generation line. The links do not establish its operating model, rollout terms, or feature details.

## What changed

Krea AI moved from separate Video and Stage surfaces to a toolkit with its own model and a controllable realtime workflow.

- **2025-04-16:** Video was documented, but the exact release cannot be recovered from the old URL with the `ol_flux` parameter because it now leads to a changing interface.
- **2025-04-18:** Stage offered an experimental 3D-scene workflow: create a scene from text, add and move objects, and export glTF. Confirmation of the details is secondary because the historical specification is unavailable at the original URL.
- **2025-08-29:** Realtime Video added generation faster than playback, with a canvas, text, webcam, and screen capture. The initial announcement is dated 2025-08-27.
- **2025-10-20:** Krea released Realtime 14B, an autoregressive model for long-form realtime video. The company claimed 11 fps on one B200 and first frames in about one second.
- **2026-05-12 and 2026-05-21:** Krea 2 became its own foundation image model, followed by beta LoRA training for Max and Business.
- **2026-09-04:** Current documentation describes Krea as a toolkit of Image, Video, Realtime, Edit, Enhancer, and Train rather than one generator.

## How to use this

From 2025-08-29, practitioners evaluating Krea AI should include its Realtime Video surface in workflow comparisons and independently verify current access, behavior, and capabilities.

1. Open Krea and choose Image or Video for a standard render. Use Realtime when the composition needs live direction.  
   — [Krea guide](https://www.krea.ai/docs/user-guide/get-started/what-is-krea)
2. In Video, choose a model, set the prompt, aspect ratio, duration, and resolution, and add start and end frames if needed.  
   — [Video Models](https://www.krea.ai/docs/user-guide/features/video)
3. In Realtime, enter a prompt, then draw, move figures, upload a reference, or provide a webcam or screen feed. Choose Image or Video as the output.  
   — [Realtime](https://www.krea.ai/docs/user-guide/features/realtime)
4. For a repeatable style, character, or product, open Train. Upload at least three images, choose Krea 2 Medium or Large, check the captions, and connect the finished LoRA in Image.  
   — [Krea 2 LoRA training](https://www.krea.ai/blog/krea-2-lora-training)
5. To change one area, open Edit. Select it with a rectangle, brush, or auto-selection, and describe the replacement. Continue the edit history step by step.  
   — [Krea Edit](https://www.krea.ai/blog/krea-edit)

## Best practices

- Compare several models with the same prompt. Choose based on the required motion, control, and character retention, not the model name.  
  — [Video Models](https://www.krea.ai/docs/user-guide/features/video)
- Start with 5–10-second, lower-cost tests; increase duration and resolution only after choosing a direction.  
  — [Video Models](https://www.krea.ai/docs/user-guide/features/video)
- Describe the action and camera movement explicitly. Use start and end frames, and assemble complex scenes from separate frames first.  
  — [Video Models](https://www.krea.ai/docs/user-guide/features/video)
- Use Realtime for composition and quick tests. Use ordinary Image when you need a deliberate prompt-first render without drawing.  
  — [Realtime](https://www.krea.ai/docs/user-guide/features/realtime)
- For LoRA, keep the first dataset narrow but varied in angles, lighting, and background. Check captions by hand, and do not raise the step count without a reason.  
  — [Krea 2 LoRA training](https://www.krea.ai/blog/krea-2-lora-training)

## Superseded by this

- **2025-04-16** — The conclusion recommending a video model from the old `ol_flux` parameter is outdated. Choose the model in the current picker and check it with the same test.
- **2025-04-18** — The instruction to treat Stage as a documented standalone entry point is outdated. Its historical specification is no longer available at the original URL, so the old workflow needs to be checked again.
- **2025-08-29** — Treating the Realtime Video announcement as the function's final state is outdated. It developed into Realtime 14B on 2025-10-20 and the current canvas-based Realtime workflow.

## Still unknown

- The exact 2025-04-16 product release is unconfirmed. The Video URL remains, but its historical contents and the meaning of the `ol_flux` parameter are unavailable.
- Stage is confirmed as a separate experimental 3D tool in April 2025, but it is unclear whether it was later renamed, moved, or closed. The current `/stage` page does not provide a readable specification.
- The three dates belong to one company but different product surfaces—Video, Stage, and Realtime. They are not three independent companies, but Stage's fate remains unclear.
- The current primary materials are inconsistent: the overview page still names Krea 1 as the main model, while the 2026 releases position Krea 2 as its own foundation model.
- Access to models, plans, credits, and regional restrictions was not checked for a specific account. The figures in the documentation are a guide, not a guarantee of the applicable plan.

## Sources

| source | title | read |
|---|---|---|
| https://www.krea.ai/video?kr_v=ol&krex=ol_flux | Krea Video | 2026-09-04 |
| https://www.krea.ai/stage | Krea Stage | 2026-09-04 |
| https://cgworld.jp/flashnews/01-202504-KreaStage.html | KREAに3Dシーン生成機能「Krea Stage」が追加 | 2026-09-04 |
| https://www.krea.ai/blog/announcing-realtime-video | Announcing Realtime Video | 2026-09-04 |
| https://www.krea.ai/blog/krea-realtime-14b | Krea Realtime 14B: Real-Time, Long-Form AI Video Generation | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-image-model | Introducing Krea 2 | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-lora-training | Krea 2 LoRA training is now available | 2026-09-04 |
| https://www.krea.ai/docs/user-guide/get-started/what-is-krea | What is Krea? | 2026-09-04 |
| https://www.krea.ai/docs/user-guide/features/video | Video Models | Krea Documentation | 2026-09-04 |
| https://www.krea.ai/docs/user-guide/features/realtime | Realtime | Krea Documentation | 2026-09-04 |
| https://www.krea.ai/blog/krea-edit | A New, More Powerful Krea Edit | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `organization:krea-ai`, thread `video-generation`, 3 dated events 2025-04-16 → 2025-08-29.
- **Practical note:** From 2025-08-29, practitioners evaluating Krea AI should include its Realtime Video surface in workflow comparisons, while independently verifying current access, behavior, and capabilities.
- **Confidence:** medium. The dated superseded entries above determine what is obsolete.
