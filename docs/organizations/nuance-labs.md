---
title: "Nuance Labs: nuance-labs-nuplex-emma — Nuance Labs Nuplex Emma"
category: "organizations"
date: 2026-11-12
tags: ["nuance-labs", "nuance-labs-nuplex-emma", "organization"]
aliases: ["Nuance Labs: nuance-labs-nuplex-emma"]
---

# Nuance Labs: nuance-labs-nuplex-emma — Nuance Labs Nuplex Emma

**Development line:** organization:nuance-labs · thread nuance-labs-nuplex-emma  
**Last event:** 2026-11-12 · 1 dated since 2026-11-12 · **Researched:** 2026-11-14 · confidence: medium

## What it is

Nuance Labs is an AI research company. It builds real-time full-duplex conversational avatars for developers and customer-facing interactive systems. Its core product, Nuplex, is one audiovisual model. It replaces the usual cascade of speech recognition, a language model, voice synthesis and video generation.

- Real-time video and audio in both directions.
- Backchanneling: the avatar nods and smiles while the user is speaking.
- Interruption handling: the user can cut in mid-conversation.
- Developer access through a live streaming API.

Limits: output watermarking is mandatory, likeness is licensed, and the platform blocks cloning of third-party voices and faces.

Turn-taking latency is lower than in cascaded avatar services. Deployment still depends on high-bandwidth two-way streaming.

## Development line

- **2026-11-12 — Nuance Labs releases Nuplex 1.0 model and Emma real-time avatar.** Nuance Labs is a US startup founded by former Apple researchers. It released Nuplex 1.0, an end-to-end full-duplex audiovisual model, and opened the interactive Emma avatar to the public on the web. Developers get a preview of the Nuplex Live API. The company reported a blind benchmark result of 89% human-level response speed across 1785 test questions. It said the launch includes licensed likeness, mandatory watermarking and blocked cloning of third-party faces and voices.
  - The founders are Fangchang Ma, Edward Zhang and Karren Yang, all formerly at Apple. Investors are Lightspeed, Accel and NVIDIA. Nuplex 1.0 handles perception and generation in one model. It targets conversational latency below 500 ms with non-verbal backchanneling at the same time. Developer preview access comes through the Nuplex Live API. (2026-11-12) — <https://app.nuancelabs.ai/>

## What changed

Conversational avatars moved from turn-by-turn pipelines to an end-to-end full-duplex model. Nuance Labs launched the Nuplex foundation model, the public Emma avatar demo and a developer API preview. The avatar listens and produces audio and video at the same time. Licensing and watermarking rules are there so voices and likenesses are not copied without consent.

## How to use this

1. Open the Emma avatar web demo in a supported browser and allow microphone and camera access to test real-time conversation.
  — <https://app.nuancelabs.ai/>
2. Request access to the Nuplex Live API developer preview to get streaming credentials.
  — <https://app.nuancelabs.ai/>
3. Open a two-way audio and video stream to the Nuplex Live endpoints. Send user input and receive synchronized avatar video and audio packets.
  — <https://app.nuancelabs.ai/>

## Best practices

- Use a low-latency connection and a stable microphone, so packets are not dropped and backchanneling and interruption detection keep working.
  — <https://app.nuancelabs.ai/>
- Follow the likeness licensing terms and the watermarking policy. Do not feed in third-party or unlicensed voice and face data.
  — <https://app.nuancelabs.ai/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Direct links to the Nuplex Live API preview documentation and pricing could not be reached through public search without logging in.
- The reported 89% human-level response speed across 1,785 benchmark test questions has no independent verification in peer-reviewed venues yet.
- We could not get verified direct links to community discussions on forums such as Reddit or Hacker News, because search results came back wrapped in redirects.

## Sources

| source | title | read |
|---|---|---|
| https://app.nuancelabs.ai/ | Nuance Labs - Interactive Emma Avatar & Nuplex Live | 2026-11-14 |

## Agent brief {#agent-brief}

- **Subject:** organization:nuance-labs, thread nuance-labs-nuplex-emma, 1 dated events 2026-11-12 → 2026-11-12.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
