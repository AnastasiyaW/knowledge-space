---
title: "StepAudio 3: stepaudio-3-realtime-music-voice-design — Stepaudio 3 Realtime Music Voice Design"
category: "projects"
date: 2026-09-17
tags: ["project", "stepaudio-3-realtime-music-voice-design"]
aliases: ["StepAudio 3: stepaudio-3-realtime-music-voice-design"]
---

# StepAudio 3: stepaudio-3-realtime-music-voice-design — Stepaudio 3 Realtime Music Voice Design

**Development line:** project:stepaudio-3-realtime-music-voice-design · thread stepaudio-3-realtime-music-voice-design  
**Last event:** 2026-09-17 · 1 dated since 2026-09-17 · **Researched:** 2026-11-25 · confidence: medium

## What it is

StepAudio 3 is StepFun's audio model family for realtime speech, full-song generation, and voice design.

- StepAudio 3 Realtime: full-duplex conversational model that thinks while speaking and calls tools.
- StepAudio 3 Music: full-song generation with musical structure planning.
- StepAudio 3 TTS: speech synthesis with description-based voice design.
- StepAudio 3 ASR Max: speech recognition pairing acoustic modeling with language context.

## Development line

- **2026-09-17 — StepAudio 3 Release with Realtime, Music, and Voice Design Features.** StepAudio 3 introduces a bidirectional realtime audio-language model, music generation up to 5m30s at 48kHz stereo with structure planning, and voice design across Chinese, English, Japanese, Korean, French, and Spanish. Voice Studio is announced for conversation; music generation announced.
  - The StepAudio 3 Music page notes an MoE architecture with an AR + DiT generation paradigm. It uses ABC-COT to plan song structure, section transitions, and arrangement layers before generation. Inputs are a natural-language caption and lyrics. Controls cover style, vocals, timbre, mood, instruments, key, and tempo. Output is a complete 48kHz stereo song rather than a clip. StepFun reports SOTA results on Audiobox for music quality and MuQ-Similarity for controllability, and competitive results on SongBench for aesthetic quality. The page lists Voice Studio as Coming Soon and mentions an API. (undated) — <https://stepaudiollm.github.io/step-audio-3-music/>
  - The StepFun audio overview page says StepAudio 3 Realtime is true full duplex, so users can interrupt or add a thought without waiting. It tracks hesitation, laughter, and emotion, thinks while speaking on harder questions, and uses tools to complete tasks. StepFun reports 99.7% on Artificial Analysis speech reasoning and 98.9% on conversational dynamics. StepAudio 3 TTS uses shared RVQ tokens with a discrete autoregressive architecture. It generates singing, sound effects, and music, and supports voice design from text descriptions. StepFun reports TTS at 1,755.3 Elo on the Chinese Human-Likeness Arena (+211.1 over the next listed model) and an 82.0% win rate in head-to-head human preference trials. StepAudio 3 ASR Max pairs acoustic modeling with LLM context understanding. (undated) — <https://audio.stepfun.ai/>
  - A dedicated StepAudio 3 Realtime page exists alongside the Gen and Music pages. Its extracted text contains only navigation and an 'Audio understanding: evaluation & method' heading, with no further details. (undated) — <https://stepaudiollm.github.io/step-audio-3-realtime/>

## What changed

The family now includes a realtime conversational model and a song-generation model with explicit structure planning. StepFun reports that StepAudio 3 Realtime ranks first on Artificial Analysis speech reasoning at 99.7% and conversational dynamics at 98.9%. It also reports that StepAudio 3 TTS leads the Chinese Human-Likeness Arena with an Elo of 1,755.3. StepAudio 3 Music produces complete 48kHz stereo songs planned with ABC-COT before generation.

## How to use this

1. For StepAudio 3 Music, write a natural-language caption setting style, vocals, timbre, mood, instruments, key, and tempo, then provide lyrics. The model plans structure and arrangement, then generates the full song.
  — <https://stepaudiollm.github.io/step-audio-3-music/>
2. For voice design, describe the desired voice through timbre, delivery, and emotion—such as a deep, mellow late-night radio host or a warm, velvety alto in English—and supply the script to be spoken.
  — <https://audio.stepfun.ai/>

## Best practices

- Put all musical controls (style, vocals, mood, instruments, key, tempo) in the description so the model carries these conditions through its planning step into generation.
  — <https://stepaudiollm.github.io/step-audio-3-music/>
- Specify character through timbre, delivery, and emotion in the description rather than choosing only a generic voice.
  — <https://audio.stepfun.ai/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Release or availability date of Voice Studio, including the announced music feature.
- Pricing, API access terms, and licensing for each StepAudio 3 model.
- Independent verification of vendor-reported benchmark and arena results.
- The full list of the four functions of StepAudio 3 Music, which the page mentions but does not list.
- Detailed specifications of StepAudio 3 Realtime beyond the overview page.

## Sources

| source | title | read |
|---|---|---|
| https://stepaudiollm.github.io/step-audio-3-music/ | StepAudio 3 Music \| StepFun | 2026-09-17 |
| https://audio.stepfun.ai/ | Voice AI Lab StepFun Audio | 2026-09-17 |
| https://stepaudiollm.github.io/step-audio-3-realtime/ | Step-Audio 3 Realtime \| StepFun | 2026-09-17 |

## Agent brief {#agent-brief}

- **Subject:** project:stepaudio-3-realtime-music-voice-design, thread stepaudio-3-realtime-music-voice-design, 1 dated events 2026-09-17 → 2026-09-17.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
