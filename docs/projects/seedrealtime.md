---
title: SeedRealtime
category: projects
date: 2026-08-06
tags: [project, seedrealtime, seedrealtime-development]
aliases: ["SeedRealtime"]
---

# SeedRealtime

**Development line:** `project:seedrealtime` · thread `seedrealtime-development`  
**Last event:** 2026-08-06 · 1 dated since 2026-08-06 · **Researched:** 2026-09-05 · confidence: medium

## What it is

SeedRealtime is a native audio-visual full-duplex LLM for real-time conversation across continuous audio, video, and text.

- Speech binding: connects spoken words to visual context.
- Conversational timing: decides when to speak.
- Interference handling: manages interruptions.
- Proactive reminders: triggers alerts with tool calls.

ByteDance reports half as many audio-visual pacing problems versus unnamed cascaded systems. We found no public weights, API, pricing, or technical report. It is a deployed product capability, not a documented developer platform.

## Development line

- **2026-08-06 — SeedRealtime release announcement.** The first-party release is dated 2026-08-05 and names the model SeedRealtime. ByteDance states the model rolled out fully. The release reports a halving of audio-visual conversational-pacing issues compared to cascaded models.

## What changed

2026-04-09 — Seeduplex added native full-duplex speech to Doubao. ByteDance framed visual input as the next step.

2026-08-06 — SeedRealtime delivered that audio-visual step. The first-party announcement is dated 2026-08-05, not 2026-08-06. It names the model SeedRealtime and confirms a full rollout.

The 2026-08-05 announcement lists three stated capabilities: joint audio-visual understanding, proactive interaction, and conversational timing. It illustrates seven scenarios. In end-to-end human evaluation, conversational-pacing issues were reduced by half against cascaded models. That is the only comparative figure ByteDance disclosed.

The 2026-04-09 Seeduplex rollout in Doubao was speech-only and positioned visual input as future work. It is an earlier predecessor rather than a separate SeedRealtime release.

## How to use this

From 2026-08-06, treat SeedRealtime as an announced audio-visual full-duplex model line. Check the primary release material before relying on any claim of capability or availability.

1. Test continuous camera-and-voice interaction in the consumer rollout. ByteDance provides no SDK, API, model download, or integration workflow.
  — <https://seed.bytedance.com/en/blog/seedrealtime-audio-visual-full-duplex-llm-released-toward-omni-modal-natural-interaction>

## Best practices

- Do not treat SeedRealtime as a developer dependency until ByteDance publishes an API, weights, or integration documentation. Treat public claims as product behavior rather than reproducible benchmark results.
  — <https://www.eesel.ai/blog/seedrealtime>
- Set explicit requirements for turn-taking and interference handling when evaluating real-time agents. SeedRealtime identifies timing, background chatter, and multi-person scenes as unresolved operating conditions.
  — <https://seed.bytedance.com/en/blog/seedrealtime-audio-visual-full-duplex-llm-released-toward-omni-modal-natural-interaction>

## Superseded by this

- 2026-04-09 — SeedRealtime adds native video and temporal understanding to Seeduplex's speech-only design. It does not invalidate Seeduplex's reported deployment claims.

## Still unknown

- ByteDance's public announcement does not document API access, weights, pricing, a technical paper, parameter count, system requirements, or a reproducible benchmark protocol.
- The cited event is dated 2026-08-06, but the first-party announcement is dated 2026-08-05. The one-day difference likely reflects posting dates rather than a second product change.

## Sources

| source | title | read |
|---|---|---|
| https://seed.bytedance.com/en/blog/seedrealtime-audio-visual-full-duplex-llm-released-toward-omni-modal-natural-interaction | SeedRealtime Audio-Visual Full-Duplex LLM Released: Toward Omni-Modal Natural Interaction | 2026-09-05 |
| https://seed.bytedance.com/en/blog/introducing-seed-full-duplex-speech-llm-attentive-listening-robust-interference-suppression-enabling-more-natural-interaction | Introducing Seed Full-Duplex Speech LLM: Attentive Listening, Robust Interference Suppression, Enabling More Natural Interaction | 2026-09-05 |
| https://www.eesel.ai/blog/seedrealtime | SeedRealtime: what ByteDance’s audio-visual model actually does | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:seedrealtime`, thread `seedrealtime-development`, 1 dated events 2026-08-06 → 2026-08-06.
- **Practical note:** From 2026-08-06, practitioners evaluating SeedRealtime should treat it as a publicly announced audio-visual full-duplex model line and consult the primary release material before relying on any capability or availability claim.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.