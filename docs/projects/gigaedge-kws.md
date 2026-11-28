---
title: "GigaEdge KWS: gigaedge-kws — Gigaedge Kws"
category: "projects"
date: 2026-11-27
tags: ["gigaedge-kws", "project"]
aliases: ["GigaEdge KWS: gigaedge-kws"]
---

# GigaEdge KWS: gigaedge-kws — Gigaedge Kws

**Development line:** project:gigaedge-kws · thread gigaedge-kws  
**Last event:** 2026-11-27 · 2 dated since 2026-11-27 · **Researched:** 2026-11-28 · confidence: high

## What it is

GigaEdge KWS is an on-device keyword spotting engine for consumer electronics and smart speakers. It replaces fixed wake words with names the user picks. Abilities:

- Streaming audio: a Streaming Conformer encoder with key-value cache.
- Frame classification: sequential 40-millisecond frames, using causal convolution.
- Custom wake phrases: target embeddings are derived from enrollment utterances.
- Offline enrollment and matching: no active network connection needed.

The model scales from 6 million to 30 million parameters. Enrollment audio samples are required to compute the reference embeddings. It gives edge devices with restricted computational budgets an accurate local wake-word trigger.

## Development line

- **2026-11-27 — GigaEdge KWS: User-Defined Wake Word Spotter Based on Streaming Conformer.** Sber developers introduced GigaEdge KWS, a User Defined Spotter (UDS) keyword spotting model. It enables custom wake words on smart speakers through an adapted Streaming Conformer architecture with key-value cache.
- **2026-11-27 — Sber Developers Introduce GigaEdge KWS Custom Spotter Architecture for Smart Speakers.** Developers from Sber introduced GigaEdge KWS, a user-defined spotter (UDS) for custom wake-word recognition. It targets smart speakers like SberBoom 2.0 and interactive AI systems. It is built on a Streaming Conformer architecture with KV-cache inference support.
- **2026-11-27 — other reporting on this date.**
  - Technical details: the Streaming Conformer processes audio in 40 ms frames. It started as a 6 million parameter prototype and was scaled to a 30 million parameter production model to minimize false positives. It classifies step by step, frame by frame, using pseudo-alignment. (2026-11-27) — <https://habr.com/ru/companies/sberbank/articles/1112468/>
  - Production deployment: SberBoom 2.0 and SberBoom Track hardware are supported. A custom wake word is registered by discarding the classification decoder and extracting embeddings directly from the encoder final layer. Calibration used 1.5 million negative false-trigger audio recordings. (2026-11-27) — <https://habr.com/ru/companies/sberbank/articles/1112468/>
  - Sber developers introduced GigaEdge KWS, a custom keyword spotter architecture based on Streaming Conformer for smart speakers. (2026-11-27) — <https://habr.com/ru/companies/sberbank/articles/1112468/>

## What changed

Development moved from fixed wake-word models to a configurable edge acoustic encoder based on the Streaming Conformer architecture. Full-utterance scoring gave way to frame-level classification over 40-millisecond intervals using pseudo-alignment. Early exploration used a 6-million parameter baseline. It was scaled to a 30-million parameter production checkpoint to curtail false positives. Custom phrase enrollment bypasses the classification decoder. Target embeddings are taken directly from the final encoder layer and checked against extensive false-activation datasets.

## How to use this

1. Record a small set of voice repetitions of the chosen custom wake phrase on the client device.
  — <https://habr.com/ru/companies/sberbank/articles/1112468/>
2. Extract reference target acoustic embeddings from the final layer of the Streaming Conformer encoder. Do not invoke the classification decoder.
  — <https://habr.com/ru/companies/sberbank/articles/1112468/>
3. Run the streaming inference pipeline on incoming 40 ms audio frames with key-value cache enabled. It computes similarity against the enrolled embeddings in real time.
  — <https://habr.com/ru/companies/sberbank/articles/1112468/>

## Best practices

- Use key-value caching during Streaming Conformer inference, so quadratic self-attention overhead does not hit low-power edge CPUs.
  — <https://habr.com/ru/companies/sberbank/articles/1112468/>
- Benchmark custom keyword spotter thresholds against extensive negative audio sets and false-activation logs. This balances trigger sensitivity against false alarms.
  — <https://habr.com/ru/companies/sberbank/articles/1112468/>

## Superseded by this

- Keyword spotters had to be hardcoded, or retrained from scratch, for each specific wake word phrase.
  — <https://habr.com/ru/companies/sberbank/articles/1112468/>

## Still unknown

- Whether standalone open-source model weights and inference runtimes are publicly distributed under a permissive license, or restricted to vendor hardware ecosystems.
- Performance on third-party microcontrollers or non-ARM edge architectures is unverified.

## Sources

| source | title | read |
|---|---|---|
| https://habr.com/ru/companies/sberbank/articles/1112468/ | GigaEdge KWS: кастомный споттер на Streaming Conformer | 2026-11-28 |

## Agent brief {#agent-brief}

- **Subject:** project:gigaedge-kws, thread gigaedge-kws, 2 dated events 2026-11-27 → 2026-11-27.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
