---
title: Supertonic — Public project reference
category: projects
date: 2026-05-18
tags: [project, public-project-reference, supertonic]
aliases: ["Supertonic"]
---

# Supertonic — Public project reference

**Development line:** `project:supertonic` · thread `public-project-reference`  
**Last event:** 2026-05-18 · 1 dated since 2026-05-18 · **Researched:** 2026-09-05 · confidence: high

## What it is

Supertonic — an ONNX Runtime text-to-speech stack for developers who need a self-hosted alternative to hosted TTS APIs.

- Python SDK, CLI, and loopback HTTP server
- Supertonic-3 with 31 language codes plus `na` fallback
- ten bundled voice styles and Voice Builder JSON import

## Development line

- **2026-05-18 — Supertonic public repository reference.** On 2026-05-18, the Supertonic thread linked to the project's public GitHub repository alongside a source reference. This establishes a dated public reference point for the project without asserting a specific release, feature, or code change.

## What changed

- 2025-12-10 — the Python package and six additional built-in voice styles landed.
- 2026-01-06 — Supertonic 2 expanded the model from English to five languages; its code path stayed on a release branch.
- 2026-01-22 — Voice Builder went live for persistent custom voice profiles.
- 2026-04-29 — Supertonic 3 released with 31-language support, reading-stability improvements, and a v2-compatible public ONNX interface.
- 2026-05-18 — Python SDK 1.3.1 added the local `supertonic serve` HTTP interface; Voice Builder added Supertonic-3 JSON profiles.
- 2026-05-20 — Supertonic 3 became available in Supertone Play and the Supertone API.

## How to use this

Start with the linked public GitHub repository as of 2026-05-18. We have no evidence for version-specific adoption guidance.

1. Install `supertonic`; use Python 3.9 or later.
  — <https://pypi.org/project/supertonic/>
2. Create `TTS(auto_download=True)`, select a bundled voice, synthesize text, and save the WAV output.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
3. Pass a supported ISO language code when known, or `na` for language-agnostic handling.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
4. For HTTP clients, install `supertonic[serve]`, run `supertonic serve --host 127.0.0.1 --port 7788`, then call `/v1/tts` or `/v1/audio/speech`.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>

## Best practices

- Start with the default of eight synthesis steps, then measure quality against latency. Tuning runs from 5–12 steps and speed from 0.7–2.0.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
- Pre-download the roughly 400 MB model asset during CI or deployment setup so the first production request does not pay the download cost.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
- Keep `supertonic serve` on loopback by default. Expose it only behind a reverse proxy.
  — <https://supertone-inc.github.io/supertonic-py/quickstart/>
- Separate the model licence and consent obligations from the MIT Python-source licence, especially when importing a custom voice profile.
  — <https://github.com/supertone-inc/supertonic-py/blob/main/llms.txt>
- Test screen-reader latency and language-specific number reading before accessibility deployment. A Turkish NVDA user reported delays and numeral-pronunciation failures after the v3 release.
  — <https://github.com/supertone-inc/supertonic/issues/144>

## Superseded by this

- 2026-04-29 — Supertonic 3 replaces the five-language Supertonic 2 recommendation for new multilingual deployments. It supports 31 languages and keeps the v2-compatible public ONNX interface. Supertonic 2 remains in use for legacy integrations on its release branch.
- 2026-05-18 — Python embedding is no longer the only official integration path. SDK 1.3.1 added a local HTTP facade, while embedded use remains valid where simpler.

## Still unknown

- We found no first-party Simplified-Chinese documentation in the checked Chinese search lane. Reviewed first-party material was English or Korean, which does not rule out such a page.
- PyPI lists both 1.3.0 and 1.3.1 on 2026-05-18. We found no release notes to treat 1.3.0 as a separate development event.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/supertone-inc/supertonic | GitHub - supertone-inc/supertonic: Lightning-Fast, On-Device, Multilingual TTS — running natively via ONNX. | 2026-09-05 |
| https://pypi.org/project/supertonic/ | supertonic · PyPI | 2026-09-05 |
| https://supertone-inc.github.io/supertonic-py/quickstart/ | Quick Start - supertonic-py | 2026-09-05 |
| https://github.com/supertone-inc/supertonic-py/blob/main/llms.txt | supertonic-py/llms.txt at main · supertone-inc/supertonic-py | 2026-09-05 |
| https://www.supertone.ai/en/work/faster-and-more-accurate-across-31-languages----introducing-supertonic-3 | Faster and more accurate across 31 languages — introducing Supertonic 3! | Supertone | 2026-09-05 |
| https://supertonic3.github.io/ | Supertonic 3 — Lightning-Fast, On-Device, Multilingual TTS | 2026-09-05 |
| https://github.com/supertone-inc/supertonic/issues/144 | supertonic tts turkish language and screen readers · Issue #144 | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:supertonic`, thread `public-project-reference`, 1 dated events 2026-05-18 → 2026-05-18.
- **Practical note:** Start with the linked public GitHub repository as of 2026-05-18. We have no evidence for version-specific adoption guidance.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
