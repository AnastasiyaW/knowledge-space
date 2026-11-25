---
title: "Genie 4: genie-world-model-line — Genie World Model Line"
category: "projects"
date: 2026-11-18
tags: ["genie-4", "genie-world-model-line", "luma_genie", "project"]
aliases: ["Genie", "Genie 4: genie-world-model-line"]
---

# Genie 4: genie-world-model-line — Genie World Model Line

Genie 4 is a Google DeepMind world model for game developers and roboticists: real-time simulation, not pre-rendered video like Sora or Runway Gen-3.

**Development line:** project:genie-4 · thread genie-world-model-line  
**Last event:** 2026-11-18 · 1 dated since 2026-11-18 · **Researched:** 2026-11-20 · confidence: medium

## What it is

Genie 4 is an interactive generative world model from Google DeepMind. It is for game developers, roboticists and virtual environment researchers who need real-time simulation rather than pre-rendered video, as with Sora or Runway Gen-3.

What it does:

- Navigation: move through generated scenes in real time with keyboard, mouse or controller.
- Rendering: draws frame by frame as you go, reacting to your path and to physical interventions.
- Audio: generates synchronized ambient sound, sound effects and character dialogue.
- Steering: changes the scene live from text prompts or spoken instructions, with no restart of the simulation.
- Grounding: photorealistic visuals and physical reasoning built on Gemini architecture components.

The model runs at 720p, up to 24 frames per second. Sessions are usually limited to several minutes. Fast camera rotation can cause object drift or lose long-term object permanence.

It is a workable base for interactive environments and simulation prototypes. Its spatial consistency is too weak for a persistent game engine.

## Development line

- **2026-11-18 — Genie 4 becomes available.** Google DeepMind announced on 2026-11-18 that Genie 4 is now available.
  - It generates frames in real time at 720p, up to 24 frames per second, with synchronized audio. Scenes can be steered live by text and voice, alongside keyboard and mouse controls. It ships as a research preview for Google AI Ultra subscribers in Project Genie. Early-access partners can stream it through the Gemini API and Google AI Studio. (2026-11-18) — <https://deepmind.google/blog/genie-4-is-now-available/>

## What changed

The Genie line started as passive video-token generation trained on gameplay footage. Early versions gave low-resolution interactive trajectories, with no audio and no live natural-language steering. Later versions added Gemini reasoning backbones and multimodal audio synthesis. That moved the system from offline trajectory synthesis to live, steerable environments with visuals and sound at the same time.

## How to use this

1. Open the Project Genie preview in a supported browser with an authorized Google AI Ultra account. Or get early-access developer credentials for the Gemini API in Google AI Studio.
  — <https://deepmind.google/blog/genie-4-is-now-available/>
2. Give an initial world prompt, either a text description of the scenario or a reference image, to set up the 3D environment.
  — <https://deepmind.google/blog/genie-4-is-now-available/>
3. Move through the environment in real time at 720p, up to 24 frames per second, with keyboard, mouse or gamepad directional controls.
  — <https://deepmind.google/blog/genie-4-is-now-available/>
4. During the session, give text or voice commands to change conditions, objects or scene dynamics on the fly.
  — <https://deepmind.google/blog/genie-4-is-now-available/>

## Best practices

- Keep sessions to one to two minutes, so drift does not build up and the picture stays coherent.
  — <https://deepmind.google/blog/genie-4-is-now-available/>
- Avoid fast 360-degree camera rotations, so objects keep their permanence and the background is not hallucinated.
  — <https://deepmind.google/blog/genie-4-is-now-available/>
- Explore in first person. Wide third-person views show more distortion of scale and physics.
  — <https://deepmind.google/blog/genie-4-is-now-available/>

## Superseded by this

- Earlier Genie world models generated only silent, pre-rendered or fixed-action video, with no real-time multimodal audio.
  — <https://deepmind.google/blog/genie-4-is-now-available/>
- Changing a simulation meant restarting the generation pipeline from a new prompt. Genie 4 steers live, mid-session.
  — <https://deepmind.google/blog/genie-4-is-now-available/>

## Still unknown

- Public pricing, token or minute consumption rates, and general availability beyond Google AI Ultra and trusted testers are not announced.
- Independent community benchmarks and developer postmortems on API latency could not be verified, because no direct forum links were found.
- Parameter counts and local deployment weights have not been disclosed.

## Sources

| source | title | read |
|---|---|---|
| https://deepmind.google/blog/genie-4-is-now-available/ | Genie 4 is now available - Google DeepMind | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:genie-4, thread genie-world-model-line, 1 dated events 2026-11-18 → 2026-11-18.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.

<!-- live-update:d6d01e48ae82645e1a1580f19a18c3cd4ce901c6570b4f414a832a71d2cfbd5d -->
## 2026-11-20 — Google DeepMind releases Genie 4 interactive world model API

Genie 4 is an interactive world model for developers, available in Google AI Studio and the Gemini v1beta Interactions API. It takes keyboard steering in real time and text conditioning while it runs. It outputs 720p at 24 fps with synchronized 48 kHz stereo audio. Generation streams over WebRTC and WebSockets, carries SynthID watermarking, and every session must be closed with a completion call. Interactive world simulation is now sold as a developer API.

## 2026-11-20 — Google launches Genie 4 API with streaming token billing

Genie 4 is an interactive generative simulation endpoint, open only to paid Gemini API accounts. Output uses about 240 video tokens per frame, or 5,760 tokens per second at 24 fps with stereo sound. It costs about $0.10 per second ($6.05 per minute), and billing must be enabled in Google AI Studio. Interactive video streaming now has its own tariff for developer apps.

### Usage and practices

- Enable paid billing on a Google AI Studio account and create a Gemini API key. [Source](https://aistudio.google.com/)
- Start an interactive session with client.interactions.create and set the model to genie-4. [Source](https://aistudio.google.com/)
- Connect to the streaming session over WebRTC or WebSocket and send a world_setup event with a seed prompt or a 16:9 image. [Source](https://aistudio.google.com/)
- Stream the user's steering live, such as WASD navigation and text prompts mid-session, to move through the environment and change it. [Source](https://aistudio.google.com/)
- Call complete() on the interaction object when done, so the server stops generating and billing ends. [Source](https://aistudio.google.com/)
- Call interaction.complete() in every termination and error-handling block, so the stream closes and video output tokens stop being billed. [Source](https://aistudio.google.com/)
- For web clients on WebRTC, create single-use session tokens with interactions.authTokens.create, so the long-term Gemini API key stays private. [Source](https://aistudio.google.com/)
- Place client sessions and backend proxies near serving regions in North America, Western Europe or East Asia, so round-trip latency stays under 150 milliseconds and steering stays responsive. [Source](https://aistudio.google.com/)

### Additional evidence

- 2026-11-20: The model identifier is genie-4 under the v1beta Interactions API. It runs as a bi-directional streaming loop over WebRTC and WebSockets, with SynthID watermarking, and server-side billing stops only after an explicit complete() call. [Source](https://aistudio.google.com/)
- 2026-11-20: Output uses about 240 video tokens per frame (~5,760 tokens per second at 24 fps, including 48 kHz stereo audio). It is billed at about $0.10 per second ($6.05 per minute), on paid-tier Gemini API accounts only. [Source](https://aistudio.google.com/)

### Superseded guidance (retained for history)

- 2026-11-20: Earlier generative video models made pre-rendered clips. They had no real-time control, no mid-stream text conditioning and no synchronized multi-modal audio. [Source](https://aistudio.google.com/)

### Limits and open questions

- The canonical blog and technical paper URLs are not verified. The search results gave grounding redirects, not direct article paths.
- Long-term feedback from practitioners on latency overhead and real-world billing cost is not yet established in public forum threads.


<!-- Retained base: ba59150ff6af8d3245658020d86e3463aab13771; article blob: 16c1e46841a3526e6e17d9121c9cf5d1d3a5c139 -->
