---
title: LTX2.3 Audio Reactive LoRA — LTX Video Models
category: projects
date: 2026-06-13
tags: [ltx-video-models, ltx2-3-audio-reactive-lora, ltx_video_models, project]
aliases: ["LTX2.3 Audio Reactive LoRA"]
---

# LTX2.3 Audio Reactive LoRA — LTX Video Models

**Development line:** `project:ltx2-3-audio-reactive-lora` · thread `ltx-video-models`  
**Last event:** 2026-06-13 · 1 dated since 2026-06-13 · **Researched:** 2026-09-05 · confidence: medium

## What it is

LTX2.3 Audio Reactive LoRA is a LoRA adapter in the fal repository for Lightricks/LTX-2.3, not a standalone base model, built for music visualizer creators.

- Sound response: amplifies sound-driven pulse, particles, light, deformations, and camera movement.
- Pipeline modes: operates in audio-to-video and image+audio-to-video with an audio track, a prompt, and an optional initial frame.

The model card recommends scale 1.0–1.5, 24 fps, and clips of 5–15 s; exact beat detection is not guaranteed. The adapter fits short visualizers with clear geometry, but it does not replace frame-accurate synchronization.

## Development line

- **2026-06-13 — LTX2.3 Audio Reactive LoRA appeared on Hugging Face under fal.** On 2026-06-13, the LTX2.3 Audio Reactive LoRA line was cataloged with a direct Hugging Face link under fal. This provides a public reference point for the line, but available evidence does not establish model capabilities, version details, training data, or usage terms.

## What changed

2026-06-12 — card metadata changed `private: true` to `private: false`; this marks card visibility rather than an independent runtime check. 2026-06-13 — primary history shows no separate dated revision for V1, V2, or the API on this date; the link led to the already visible adapter. 2026-06-15 — a separate V2 file was added; the author's card claimed stronger audio reactivity without providing an independent benchmark.

## How to use this

From 2026-06-13, treat this as a distinct fal-linked LTX video-model line and inspect its Hugging Face model card before adoption; public sources provide no validated configuration or performance guidance.

1. Use LTX-2.3 instead of replacing the base with LTX-2.5: official documentation states that files are incompatible and the LoRA works only with the model on which it was trained.
  — <https://github.com/Lightricks/LTX-2>
2. Send `prompt`, mandatory `audio_url`, and `loras` in the current fal API; `image_url` is optional, and the endpoint allows up to three LoRAs simultaneously.
  — <https://fal.ai/models/fal-ai/ltx-2.3-quality/audio-to-video/lora/api>
3. Add V1 or V2 safetensors from the model card to `loras`, set `transformer: "both"`, and start within the claimed scale range of 1.0–1.5.
  — <https://huggingface.co/fal/ltx2.3-audio-reactive-lora>
4. Pass `image_url` as the initial frame for a more directed clip; keep `match_audio_length` enabled if video duration must follow audio length.
  — <https://fal.ai/models/fal-ai/ltx-2.3-quality/audio-to-video/lora/api>
5. Review the result for text legibility, logo fidelity, and synchronization before publishing.
  — <https://huggingface.co/fal/ltx2.3-audio-reactive-lora>

## Best practices

- Do not mix the adapter with another LTX release line: official documentation states that the LoRA works only with the model on which it was trained.
  — <https://github.com/Lightricks/LTX-2>
- Give the initial frame structures that can move: geometry, layers, particles, light seams, or visualizer shapes.
  — <https://huggingface.co/fal/ltx2.3-audio-reactive-lora>
- Treat clean, controlled visual direction as a practical defense against chaotic artifacts: this reflects a single user run, not a general benchmark.
  — <https://www.reddit.com/r/StableDiffusion/comments/1un6vh3/followup_followup_more_experimentation_with_the/>
- Generate several variations for a complex track and pick the best one; one user test reported better results on sparser arrangements when choosing among roughly three renders.
  — <https://www.reddit.com/r/StableDiffusion/comments/1ulq1jk/followup_i_take_it_back_the_ltx_23_audioreactive/>

## Superseded by this

- 2026-06-12 — The early card state `private: true` is obsolete: a commit changed the visibility flag to `private: false`; this supersedes only the card state.
- 2026-06-15 — The note that only one adapter file exists is obsolete: V2 was added as a separate file; replacing V1 with V2 by default remains unproven.

## Still unknown

- No external primary source dated 2026-06-13 adds facts to the step itself; `event_findings` remains empty.
- Training data, rank/alpha, target modules, and a reproducible training recipe for this specific adapter are not published.
- No independent benchmark compares V1 against V2; the claim of stronger audio reactivity comes from the author's card.
- Local execution, weight downloads, and fal API calls were not tested in this pass; current documentation does not serve as runtime verification.
- The exact applicability of the LTX-2 Community License to specific use cases has not been analyzed.
- Chinese-language searches yielded no independent primary or practical sources for this exact adapter.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/fal/ltx2.3-audio-reactive-lora | fal/ltx2.3-audio-reactive-lora · Hugging Face | 2026-09-05 |
| https://huggingface.co/fal/ltx2.3-audio-reactive-lora/commit/bca5b48eb77552e1f92e9916a22f9b3c6c0f3a66 | Set model card visibility metadata to public · fal/ltx2.3-audio-reactive-lora at bca5b48 | 2026-09-05 |
| https://huggingface.co/fal/ltx2.3-audio-reactive-lora/commit/9d432f6bd21fdda9848b7eeb3a3a12faa01c91ef | Add V2 LoRA as separate file · fal/ltx2.3-audio-reactive-lora at 9d432f6 | 2026-09-05 |
| https://huggingface.co/fal/ltx2.3-audio-reactive-lora/commit/23a333233d1df57d1279fd63a745e854375e8859 | Update model card for V2 · fal/ltx2.3-audio-reactive-lora at 23a3332 | 2026-09-05 |
| https://fal.ai/models/fal-ai/ltx-2.3-quality/audio-to-video/lora/api | Ltx 2.3 Quality Audio to Video API Docs | fal | 2026-09-05 |
| https://github.com/Lightricks/LTX-2 | Lightricks/LTX-2 — official Python inference and LoRA trainer package | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1un6vh3/followup_followup_more_experimentation_with_the/ | Follow-up follow-up: More experimentation with the audio-reactive LoRA for LTX-2.3 | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1ulq1jk/followup_i_take_it_back_the_ltx_23_audioreactive/ | Follow-up: I take it back, the LTX 2.3 audio-reactive LoRA is actually pretty amazing | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:ltx2-3-audio-reactive-lora`, thread `ltx-video-models`, 1 dated events 2026-06-13 → 2026-06-13.
- **Practical note:** From 2026-06-13, treat this as a distinct fal-linked LTX video-model line and inspect its Hugging Face model card before adoption; public sources provide no validated configuration or performance guidance.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.