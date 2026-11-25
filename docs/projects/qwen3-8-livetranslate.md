---
title: "Qwen3.8-LiveTranslate: qwen3-8-livetranslate — Qwen3 8 Livetranslate"
category: "projects"
date: 2026-09-22
tags: ["project", "qwen3-8-livetranslate"]
aliases: ["Qwen3.8-LiveTranslate: qwen3-8-livetranslate"]
---

# Qwen3.8-LiveTranslate: qwen3-8-livetranslate — Qwen3 8 Livetranslate

**Development line:** project:qwen3-8-livetranslate · thread qwen3-8-livetranslate  
**Last event:** 2026-09-22 · 6 dated since 2026-09-17 · **Researched:** 2026-11-25 · confidence: high

## What it is

Qwen3.8-LiveTranslate is a real-time speech and video translation model on QwenCloud for live interpretation in applications.

- Speaker separation: distinguishes multiple speakers in conversation.
- Voice cloning: preserves speaker voice timbre from source audio.
- Bilingual output: displays original and translated text simultaneously.
- Context retention: uses prior context and optional images to resolve ambiguities.

Supports 60 input languages and speech output in 29; deployable model ID is `qwen3.8-livetranslate-flash-realtime`.

Use it for API-integrated live interpretation, not as a general chat or tool-calling model.

## Development line

- **2026-09-17 — Qwen3.8-LiveTranslate: qwen3-8-livetranslate update.** Alibaba Cloud published an availability notice for Qwen3.8-LiveTranslate-Flash-Realtime, covering real-time audio and video interpretation with 60 understood languages and speech output in 29.
- **2026-09-18 — Qwen3.8-LiveTranslate: qwen3-8-livetranslate update.** Qwen published its model announcement for interleaved audio-text processing. It covers speaker separation, bilingual synchronized output, and long-context disambiguation. Stated average lagging fell from 2.8 seconds to 2.3 seconds versus the prior generation.
- **2026-09-20 — Qwen3.8-LiveTranslate real-time speech translation launch.** Qwen released the LiveTranslate feature on Alibaba Cloud with DashScope integration. It offers real-time speech translation across 60 languages with voice cloning, low 2.3s latency, and hybrid-MoE architecture.
- **2026-09-20 — Qwen3.8-LiveTranslate real-time translation release.** Qwen released Qwen3.8-LiveTranslate for cloud deployment via Alibaba DashScope. It supports 60 languages with voice cloning, low 2.3s latency via Hybrid-MoE architecture, dual-speaker identification, video-aware disambiguation, and long-context retention.
- **2026-09-20 — Qwen releases AI translator that dubs interlocutors in their own voices.** Qwen3.8 LiveTranslate translates conversations and video with a delay of about 2.3 seconds. It recognizes speech in 60 languages and translates into 29 languages including Russian. It distinguishes multiple speakers, preserves voice timbre, shows original and translation simultaneously, and analyzes on-screen context.
- **2026-09-20 — other reporting on this date.**
  - The official Qwen announcement is dated 2026-09-18, so reporting on 2026-09-20 reflects the launch rather than a distinct product release. It identifies a Hybrid-MoE Thinker–Talker design and gives the 60-input-language/29-spoken-output-language split. (2026-09-18) — <https://qwen.ai/blog?id=qwen3.8-livetranslate>
  - The official announcement narrows the release to simultaneous interpretation with an interleaved audio-text stream. It reports bilingual synchronized output, long-context disambiguation, and speaker separation. (2026-09-18) — <https://qwen.ai/blog?id=qwen3.8-livetranslate>
  - The official announcement supports voice preservation as voice cloning tied to source audio. It specifies 29 spoken-output languages rather than speech output for all 60 supported input languages. (2026-09-18) — <https://qwen.ai/blog?id=qwen3.8-livetranslate>
- **2026-09-22 — Qwen3.8-LiveTranslate real-time translation release.** Qwen released Qwen3.8-LiveTranslate on Alibaba Cloud DashScope. It supports 60 languages with voice cloning, low 2.3s latency via Hybrid-MoE architecture, and video-aware disambiguation.
  - Official sources date the availability notice to 2026-09-17 and the Qwen announcement to 2026-09-18; no reviewed public source documents a separate 2026-09-22 product change. (2026-09-17) — <https://www.aliyun.com/product/news/30919>
  - The guide gives a WebSocket URL for `qwen3.8-livetranslate-flash-realtime`. It requires audio input, keeps image input optional, and notes images can resolve ambiguities in source speech. (undated) — <https://docs.qwencloud.com/developer-guides/speech/realtime-translation>

## What changed

2026-09-17 — Alibaba Cloud published the availability notice for Qwen3.8-LiveTranslate-Flash-Realtime, covering 60 understood languages and speech output in 29. 2026-09-18 — Qwen published the model announcement, specifying an interleaved Thinker–Talker design and a reduction in average lagging from 2.8 seconds to 2.3 seconds.

## How to use this

1. Create a QwenCloud/Model Studio workspace and store the long-term API key on the application server.
  — <https://help.aliyun.cn/zh/model-studio/livetranslate-realtime-websocket-access>
2. Open a regional WebSocket connection with model ID `qwen3.8-livetranslate-flash-realtime`, then wait for `session.created` before sending `session.update`.
  — <https://docs.qwencloud.com/api-reference/speech-translation/livetranslate-realtime/websocket-access>
3. Set the target language and `output_modalities`. Provide audio input for audio-only translation, and enable audio-plus-video only when visual context is needed.
  — <https://docs.bailian.console.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime>
4. Stream audio with `input_audio_buffer.append`. Read `response.text.delta` or `response.audio_transcript.delta` in order, and decode audio chunks when speech output is enabled.
  — <https://docs.bailian.console.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime>
5. Send `session.finish` after the final audio chunk and keep the connection open until `session.finished` arrives.
  — <https://help.aliyun.cn/zh/model-studio/livetranslate-realtime-websocket-access>

## Best practices

- Keep long-term API keys on the server; do not embed them in a browser or mobile application.
  — <https://docs.qwencloud.com/api-reference/speech-translation/livetranslate-realtime/websocket-access>
- Wait for `session.updated` before sending media. Treat server events rather than a successful connection as the completion signal.
  — <https://help.aliyun.cn/zh/model-studio/livetranslate-realtime-websocket-access>
- Use the 3.8-specific event schema instead of reusing Qwen3.5 or Omni request fields, because documented field names differ.
  — <https://help.aliyun.cn/zh/model-studio/livetranslate-realtime-websocket-access>
- Provide 16 kHz input and play translated audio as 24 kHz PCM for the 3.8 default PCM path. Use headphones in microphone demos so translated speech does not feed back into the input.
  — <https://docs.bailian.console.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime>
- Use a small, curated hotword list for fixed terminology; the guide recommends no more than 1,000 hotwords.
  — <https://docs.bailian.console.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime>

## Superseded by this

- Applying Qwen3.5-LiveTranslate event and configuration fields directly to Qwen3.8 is obsolete.
  — <https://help.aliyun.cn/zh/model-studio/livetranslate-realtime-websocket-access>
- Using an Omni `response.create` dialogue flow for Qwen3.8-LiveTranslate is obsolete; the model uses its own translation configuration and events.
  — <https://help.aliyun.cn/zh/model-studio/livetranslate-realtime-websocket-access>

## Still unknown

- Alibaba Cloud's 2026-09-17 notice states the Qwen3.8-LiveTranslate-Flash family supports offline and real-time translation, but public API documentation lists only the realtime model ID. No reviewed public source establishes an offline Qwen3.8 model ID or endpoint.
- No reviewed community report provides concrete post-use findings.

## Sources

| source | title | read |
|---|---|---|
| https://qwen.ai/blog?id=qwen3.8-livetranslate | Qwen3.8-LiveTranslate: Names the speaker. Carries the meaning. | 2026-11-25 |
| https://www.aliyun.com/product/news/30919 | Qwen3.8-Livetranslate-Flash-Realtime real-time audio/video interpretation model launch | 2026-11-25 |
| https://docs.qwencloud.com/api-reference/speech-translation/livetranslate-realtime/websocket-access | Qwen-LiveTranslate-Realtime WebSocket access | 2026-11-25 |
| https://docs.bailian.console.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime | 实时语音/音视频翻译-千问 | 2026-11-25 |
| https://help.aliyun.cn/zh/model-studio/livetranslate-realtime-websocket-access | Qwen-LiveTranslate-Realtime WebSocket 接入 | 2026-11-25 |
| https://docs.qwencloud.com/developer-guides/speech/realtime-translation | Real-time audio and video translation - Qwen | 2026-11-25 |

## Agent brief {#agent-brief}

- **Subject:** project:qwen3-8-livetranslate, thread qwen3-8-livetranslate, 6 dated events 2026-09-17 → 2026-09-22.
- **Practical note:** Sourced usage and practice sections above define limits and integration steps.
- **Confidence:** high. Dated supersedes above identify obsolete configurations.
