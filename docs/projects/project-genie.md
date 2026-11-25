---
title: "Project Genie: project-genie-genie-4-rollout — Project Genie Genie 4 Rollout"
category: "projects"
date: 2026-11-19
tags: ["luma_genie", "project", "project-genie", "project-genie-genie-4-rollout"]
aliases: ["Genie", "Project Genie: project-genie-genie-4-rollout"]
---

# Project Genie: project-genie-genie-4-rollout — Project Genie Genie 4 Rollout

Project Genie is Google DeepMind's tool that builds real-time 3D worlds from text or images, for researchers, game designers and AI developers.

**Development line:** project:project-genie · thread project-genie-genie-4-rollout  
**Last event:** 2026-11-19 · 2 dated since 2026-11-19 · **Researched:** 2026-11-20 · confidence: high

## What it is

Project Genie is an interactive world simulator from Google DeepMind. It is a prototyping tool for dynamic worlds, not a replacement for deterministic 3D game engines.

What it does:

- Generates navigable 3D environments in real time from a text prompt or a reference image.
- Takes interactive steering from the keyboard and mouse.
- Produces synchronized native audio and sound effects.
- Changes a scene mid-session, for example the weather or added objects, without restarting.

The limits: it runs at 720p and 24 frames per second, and continuous interactive streams are capped at bounded durations. Objects drift and physics become inconsistent over long sessions. All visual output carries a SynthID watermark.

## Development line

- **2026-11-19 — Genie 4 begins rolling out in Project Genie for some Google AI Ultra subscribers.** Google started the rollout of Genie 4 in Project Genie to some Google AI Ultra subscribers. Google AI Pro has a waitlist. The documentation says world generation does not consume AI credits during the research prototype stage. The 3-minute session limit in the announcement applies to the updated Genie 3, not to Genie 4.
- **2026-11-19 — Genie 4 rolls out in Project Genie to some AI Ultra subscribers.** Google began rolling out Genie 4 within Project Genie to some Google AI Ultra subscribers. AI Pro has a waitlist. The documentation says world generation does not consume AI credits during the research prototype stage. The three-minute session limit belongs to Genie 3 and does not carry over to Genie 4.
- **2026-11-19 — other reporting on this date.**
  - DeepMind's technical release says Genie 4 runs at 720p and up to 24 frames per second. It has native synchronized audio (ambient sounds, sound effects and dialogue) and is powered by Gemini Omni Flash for physics and visual grounding. Text prompts can steer a session mid-run without resetting the simulation state. (2026-11-19) — <https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/>
  - Google Labs documentation says Project Genie includes an AI Creation Agent and a community gallery for remixing worlds. World generation during the research prototype does not deduct Google AI credits. SynthID watermarking is embedded in all generated sessions. (2026-11-19) — <https://support.google.com/labs/answer/16875695>

## What changed

Project Genie moved from passive world generation to real-time controllable simulation. The model now generates native audio alongside video. It accepts keyboard and mouse navigation, and it changes the world from text prompts during a live session.

Google put the upgraded world model into the Project Genie web research prototype for top-tier subscribers. It also opened developer access through Gemini API endpoints and AI Studio. Session duration limits stay separate, and the research prototype still does not consume credits.

## How to use this

1. Sign in to Project Genie at labs.google/projectgenie with an active Google AI Ultra account, or join the Google AI Pro waitlist.
  — <https://labs.google/projectgenie>
2. Enter a text prompt or upload a reference image. It sets the starting environment, characters and visual style.
  — <https://labs.google/projectgenie>
3. Explore the generated 720p world in real time with the standard keyboard and mouse controls.
  — <https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/>
4. Type text commands to change lighting, weather or scene objects. The session does not reset.
  — <https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/>
5. Share or remix finished worlds in the Project Genie community gallery.
  — <https://support.google.com/labs/answer/16875695>

## Best practices

- Start a world with a short, high-contrast prompt, so spatial ambiguity and early texture drift do not creep in during navigation.
  — <https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/>
- Use mid-session prompts for small changes to atmosphere and lighting, not drastic structural shifts, so the scene stays coherent.
  — <https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/>
- Check the session length before you launch a simulation. The three-minute limit applies only to Genie 3 workflows, and Genie 4 runs under its own prototype stream limits.
  — <https://support.google.com/labs/answer/16875695>

## Superseded by this

- Old claim: Project Genie simulations are restricted to silent video without synchronized native audio.
  — <https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/>
- Old claim: the 3-minute exploration session limit applies to all Project Genie models, Genie 4 included.
  — <https://support.google.com/labs/answer/16875695>

## Still unknown

- The exact stream duration limit for Genie 4 sessions in Project Genie. Public documentation only says the 3-minute limit is specific to Genie 3.
- Developer API pricing and rate limits for Genie 4 in Google AI Studio and the Gemini Interactions API. Public Labs pages do not document them.
- Community reactions on platforms such as Reddit. They were seen only through redirect links, so they could not be checked against permanent canonical URLs.

## Sources

| source | title | read |
|---|---|---|
| https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/ | Genie 4: A new generation of world simulation | 2026-11-20 |
| https://support.google.com/labs/answer/16875695 | Project Genie Help & FAQ | 2026-11-20 |
| https://labs.google/projectgenie | Project Genie - Google Labs | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:project-genie, thread project-genie-genie-4-rollout, 2 dated events 2026-11-19 → 2026-11-19.
- **Practical note:** See the usage and practice sections above, with their limits.
- **Confidence:** high. The dated supersedes above decide what is obsolete.

<!-- live-update:8ed441801c0bb3264b190605012593762aa7c2b9e78ea809d19c3a2e9dc723e9 -->
## 2026-11-20 — Google opens early Project Genie access powered by Genie 4

Google has opened an experimental preview of Project Genie to Google AI Ultra subscribers in the United States. It runs on the Genie 4 world model and generates short-lived, interactive 720p environments with synchronized audio from text and image prompts.

### Usage and practices

- Open Project Genie in a desktop web browser, signed in to a Google AI Ultra account. It works only in supported jurisdictions (US, 18+). [Source](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/)
- Type a description or upload a reference image. It sets the scene layout, the look and the playable character. [Source](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/)
- Move around the generated 3D environment in real time with a standard keyboard and mouse. [Source](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/)
- Change the running simulation by typing or speaking a prompt. It can adjust lighting and weather or add new entities. [Source](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/)
- Describe the environment and the character precisely, or use clean framing images, so the visuals stay coherent once navigation starts. [Source](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/)
- Change the prompt in small steps during a session, not in drastic scene swaps, so physics drift and spatial artifacts stay low. [Source](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/)
- Keep sessions short and use them for concept prototyping. Long runs accumulate drift and break the continuity of the environment. [Source](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/)

### Additional evidence

- 2026-11-20: Genie 4 in Project Genie generates navigable worlds in real time at 720p and up to 24 frames per second. It adds native audio for ambient sound and character dialogue, accepts live prompt changes mid-session, and embeds SynthID watermarks in its outputs. [Source](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/)

### Superseded guidance (retained for history)

- 2026-11-20: Generative world models used to render only passive, non-interactive video. They had no real-time character steering and no native synchronized audio. [Source](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/)

### Limits and open questions

- Pricing, standalone API token rate limits in Google AI Studio, and plans for expansion beyond the initial US tier have not been published.
- Drift tolerances, the maximum duration before spatial decoherence, and the client-side bandwidth needed for 720p streaming are not measured in public documentation.


<!-- Retained base: ba59150ff6af8d3245658020d86e3463aab13771; article blob: 634adf6a4b97ba86138414b2458be79df98f6a2f -->
