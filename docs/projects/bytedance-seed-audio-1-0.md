---
title: Seed Audio 1.0 — Seed Audio
category: projects
date: 2026-07-22
tags: [bytedance-seed-audio-1-0, project, seed-audio]
aliases: ["Seed Audio 1.0"]
---

# Seed Audio 1.0 — Seed Audio

**Development line:** `project:bytedance-seed-audio-1-0` · thread `seed-audio`  
**Last event:** 2026-07-22 · 1 dated since 2026-07-22 · **Researched:** 2026-09-05 · confidence: high

## What it is

Seed Audio 1.0 is a ByteDance audio model for creators of video, games, ads, and podcasts.

- Speech and dialogue from a prompt with voice or image references.
- Sound effects and ambience generated in the same pass.

The confirmed external API limits inputs to three audio references of 30 seconds each. Official material claims up to two minutes of audio in one pass.

The model is an alternative to TTS and manual sound design for draft audio scenes. Voice reference rights remain the user's responsibility.

## Development line

- **2026-07-22 — Seed Audio 1.0 product page and BytePlus activation path.** On 2026-07-22, public links connected the official Seed Audio 1.0 product page and a BytePlus Voice console activation path. Together, those dated official links mark a public-facing product and onboarding step for the project. They do not establish the exact announcement wording, feature set, availability, or release scope.

## What changed

2026-07-22 — Seed Audio 1.0 became available through BytePlus as a single model for speech, sound effects, and atmosphere. The official announcement is dated 2026-07-20, so the July 22 date marks appearance in the feed rather than the primary announcement.

2026-07-20 — ByteDance described the model as a full sound scene generator. Speech timing is configurable down to 100 ms. A single pass can produce up to two minutes of audio with continuation.

## How to use this

We can evaluate Seed Audio 1.0 through Seed and BytePlus Voice as of 2026-07-22. Confirm activation eligibility, availability, and capabilities before relying on it.

1. Activate Seed Audio in BytePlus through the console and create a project.
  — <https://console.byteplus.com/voice/new/setting/activate?projectName=default>
2. Describe the scene in one prompt: characters, lines, emotion, environment, and key sounds. Set line entry points when needed.
  — <https://seed.bytedance.com/en/blog/from-speech-to-audio-creation-introducing-the-seed-audio-1-0-audio-creation-model>
3. For programmatic calls, pass the required prompt, label audio references as @Audio1–@Audio3, and save the result URL.
  — <https://fal.ai/models/bytedance/seed-audio-1.0/api>

## Best practices

- Use only authorized voice references. Official documentation explicitly limits voice cloning to authorized samples.
  — <https://seed.bytedance.com/en/blog/from-speech-to-audio-creation-introducing-the-seed-audio-1-0-audio-creation-model>
- Do not block the application on async requests. Poll the queue or use a webhook instead.
  — <https://fal.ai/models/bytedance/seed-audio-1.0/api>
- Keep the API key on the server rather than in the browser or client application.
  — <https://fal.ai/models/bytedance/seed-audio-1.0/api>

## Superseded by this

- 2026-07-20: audio scenes no longer require assembling speech, effects, and atmosphere as isolated clips. Seed Audio 1.0 handles them in a single scene prompt, but results and source voice rights still require verification.

## Still unknown

- The official project page returned no technical specifications during verification, and the BytePlus console requires interactive access. Current pricing, available regions, and the exact BytePlus API contract remain unconfirmed.
- The entry is dated 2026-07-22, but primary ByteDance material is dated 2026-07-20. The two-day gap is unexplained.

## Sources

| source | title | read |
|---|---|---|
| https://seed.bytedance.com/en/seedaudio1_0 | ByteDance Seed — Seed Audio 1.0 project page | 2026-09-05 |
| https://console.byteplus.com/voice/new/setting/activate?projectName=default | BytePlus Voice — Seed Audio activation | 2026-09-05 |
| https://seed.bytedance.com/en/blog/from-speech-to-audio-creation-introducing-the-seed-audio-1-0-audio-creation-model | From Speech to Audio Creation | Introducing the Seed Audio 1.0 Audio Creation Model | 2026-09-05 |
| https://fal.ai/models/bytedance/seed-audio-1.0/api | Seed Audio 1.0 Text to Audio API Docs | fal | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:bytedance-seed-audio-1-0`, thread `seed-audio`, 1 dated events 2026-07-22 → 2026-07-22.
- **Practical note:** As of 2026-07-22, practitioners can treat Seed Audio 1.0 as an official product path to evaluate through Seed and BytePlus Voice, while confirming activation eligibility, availability, and capabilities before relying on it.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
