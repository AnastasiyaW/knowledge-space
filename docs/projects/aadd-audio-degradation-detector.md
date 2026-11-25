---
title: "AADD (Automatic Audio Degradation Detection): aadd-audio-degradation-detector-release — Aadd Audio Degradation Detector Release"
category: "projects"
date: 2026-11-19
tags: ["aadd-audio-degradation-detector", "aadd-audio-degradation-detector-release", "project"]
aliases: ["AADD (Automatic Audio Degradation Detection): aadd-audio-degradation-detector-release"]
---

# AADD \(Automatic Audio Degradation Detection\): aadd-audio-degradation-detector-release — Aadd Audio Degradation Detector Release

AADD (Automatic Audio Degradation Detection) is an open-source toolkit that tags 12 types of speech degradation for dataset curators.

**Development line:** project:aadd-audio-degradation-detector · thread aadd-audio-degradation-detector-release  
**Last event:** 2026-11-19 · 1 dated since 2026-11-19 · **Researched:** 2026-11-20 · confidence: high

## What it is

AADD is an open-source speech quality toolkit for audio ML practitioners and dataset curators. It is a local alternative to manual audio inspection and commercial quality assurance APIs for cleaning speech training corpora.

Abilities:

- Detects 12 speech degradation categories: background noise, music, reverberation, clipping, low-pass filtering, high-pass filtering, codec compression artifacts, packet loss, mains hum, clicks, pitch shift, and time stretch.
- Scores speech over sliding windows with frame-level multilabel classification every 20 milliseconds.
- Outputs independent sigmoid probabilities, so overlapping segments can carry several defect tags.
- Comes in two sizes: an 88-million parameter Whisper-small encoder base and a 1.3-million parameter lightweight model.

It supports English and Russian speech. Long files need segmentation or sliding window processing. Classification quality outside the trained languages is unverified.

## Development line

- **2026-11-19 — AADD open-source speech degradation detector released.** gertelrina announced AADD \(Automatic Audio Degradation Detection\). It labels 12 types of speech degradation every 20 ms and supports English and Russian. It is built on a Whisper-small base \(88M parameters\) with weights on Hugging Face. It is released under MIT, with a 1.3M-parameter v3-lite variant.
  - The release defines 12 degradation categories \(background noise, music, reverberation, clipping, low-pass, high-pass, codec artifacts, packet loss, mains hum, clicks, pitch shift, and time stretch\). They are evaluated over sliding windows with multilabel sigmoid outputs every 20 ms. (2026-11-19) — <https://github.com/gertelrina/aadd>
  - The release collection publishes pre-trained weights for the full Whisper-small classification backbone \(88M parameters\) and for the compact v3-lite model \(1.3M parameters\), hosted on Hugging Face. (2026-11-19) — <https://hf.co/collections/gertelrina/automatic-audio-degradation-detection>

## What changed

The project began as fine-tuning of an audio encoder to detect fine-grained flaws across frames. It then moved from prototype experiments to an open-source release. The release has a full Whisper-small backbone, a compact lightweight variant, and published model weights for automated dataset audit workflows.

## How to use this

1. Clone the repository and install the dependencies to set up a local evaluation environment.
  — <https://github.com/gertelrina/aadd>
2. Download the pre-trained Whisper-small base or v3-lite detector weights from the Hugging Face collection.
  — <https://hf.co/collections/gertelrina/automatic-audio-degradation-detection>
3. Pass English or Russian speech files into the sliding window inference pipeline. It returns per-frame multilabel degradation predictions at 20 ms resolution.
  — <https://github.com/gertelrina/aadd>
4. Filter or segment speech datasets with category-specific sigmoid thresholds before ASR or TTS training.
  — <https://github.com/gertelrina/aadd>

## Best practices

- Use the Whisper-small 88M model when accuracy on subtle degradations matters. Keep the 1.3M v3-lite model for high-throughput or resource-constrained filtering.
  — <https://hf.co/collections/gertelrina/automatic-audio-degradation-detection>
- Set an independent probability threshold per degradation category, not one aggregate score, because several flaws can occur on the same segment.
  — <https://github.com/gertelrina/aadd>
- Keep input to English and Russian, or validate performance on your domain before using other languages.
  — <https://github.com/gertelrina/aadd>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- Benchmark metrics against other speech quality models \(such as NISQA or DNSMOS\) are not published in the repository documentation.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/gertelrina/aadd | gertelrina/aadd: Automatic Audio Degradation Detection | 2026-11-20 |
| https://hf.co/collections/gertelrina/automatic-audio-degradation-detection | Automatic Audio Degradation Detection - a Hugging Face Collection by gertelrina | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:aadd-audio-degradation-detector, thread aadd-audio-degradation-detector-release, 1 dated events 2026-11-19 → 2026-11-19.
- **Practical note:** see the usage and practice sections above, with their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
