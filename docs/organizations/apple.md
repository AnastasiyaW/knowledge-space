---
title: Apple — Apple AI: research releases to product capabilities
category: organizations
tags: [apple, apple-ai-research-to-product, apple_gaudi, apple_intelligence, open_source_release, organization]
aliases: ["Apple"]
---

# Apple — Apple AI: research releases to product capabilities

**Development line:** `organization:apple` · thread `apple-ai-research-to-product`  
**Events:** 3 dated, 2022-08-05 → 2026-06-09 · **Researched:** 2026-09-03 · confidence: medium

## What it is

Apple — a device and software platform company whose usable AI surface is Apple Intelligence for people with supported Apple hardware and Swift teams building system-aware apps. - On devices: writing, image, search, translation, notification, and Shortcut features. - In apps: Foundation Models for typed generation and tool use; App Intents for Siri, Spotlight, and Shortcuts. Limit: support varies by device, OS, language, and region; eligible iPhone, iPad, Mac, and Vision Pro devices need 7 GB of storage. Verdict: use Apple Intelligence as a gated platform integration; treat GAUDI and NeuMan as separate 2022 research code.

## Development line

- **2022-08-05 — Apple published the Gaudi machine-learning repository.** On 2022-08-05, Apple publicly published the ml-gaudi repository on GitHub. This is a dated public release of an Apple machine-learning research project and belongs in the organization’s AI development history.
- **2022-08-17 — Apple published the Neuman machine-learning repository.** On 2022-08-17, Apple publicly published the ml-neuman repository on GitHub. This is a separate dated public release of Apple machine-learning work and documents continued public AI research activity.
- **2026-06-09 — Apple announced new Apple Intelligence capabilities for everyday experiences.** On 2026-06-09, Apple announced Apple Intelligence capabilities intended for everyday experiences. The linked Apple Newsroom page and accompanying video make this a material product-facing milestone in Apple’s AI development history.

## What changed

Apple development line: - 2022-08-05 — GAUDI made Apple research code available for generative 3D scenes represented as radiance fields, including conditioning from text or RGB images. It was a research implementation, not a platform API. - 2022-08-17 — NeuMan made a reference implementation available for reconstructing a background and animatable person from one video. Its documented Python 3.7, PyTorch 1.8, and CUDA environment makes it a reproduction workflow, not an Apple-device runtime. - 2026-06-09 — Apple’s June 8 release announced the next Apple Intelligence architecture, including new system features and natural-language Shortcut construction. The release described iOS 27-era features as developer testing, public beta, or fall availability rather than a completed worldwide rollout. - Found today (2026-09-03) — Apple’s current developer path is Foundation Models plus App Intents; Apple Support documents hardware, storage, language, and regional gates for available features.

## How to use this

As of 2026-06-09, practitioners tracking Apple should distinguish its public machine-learning research releases from its product-facing Apple Intelligence announcements, while following both as connected evidence of the company’s AI development.

1. Check hardware, OS, free storage, device/Siri language, and regional availability. Update the device, enable Apple Intelligence in Settings > Apple Intelligence & Siri, then keep it on Wi-Fi and power while on-device models download.
  — <https://support.apple.com/en-ie/121115>
2. For a Swift app, start with Foundation Models when the feature needs language or multimodal generation, structured output, or tool calls; select the model/provider for the task rather than assuming an on-device model fits every workload.
  — <https://developer.apple.com/apple-intelligence/>
3. Expose app actions and content through App Intents and entities so they can be discovered through Siri, Spotlight, and Shortcuts.
  — <https://developer.apple.com/apple-intelligence/>
4. For a personal automation, use Shortcuts’ Use Model action, choose an output type that the next action can consume, and test the full flow with real app entities.
  — <https://developer.apple.com/videos/play/wwdc2025/260/>

## Best practices

- Gate onboarding and feature paths on actual hardware, OS, storage, language, and region; do not present unsupported features as available.
  — <https://support.apple.com/en-ie/121115>
- Use guided generation for typed outputs, test varied prompts against representative samples, and evaluate results before relying on a model-driven feature.
  — <https://developer.apple.com/documentation/technologyoverviews/generative-models?changes=_2%2C_2>
- Expose only useful entity properties to model workflows, provide Find actions or indexing for discovery, and supply parameter summaries and suggestions for Spotlight and Shortcuts.
  — <https://developer.apple.com/videos/play/wwdc2025/260/>
- Keep June 2026 capabilities behind availability checks: Apple’s release labels them testing, beta, or later-year rollout and notes language and regional variation.
  — <https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/>

## Superseded by this

- 2022-08-05/2022-08-17: GAUDI and NeuMan are superseded as guidance for integrating an Apple-platform AI feature. Foundation Models and App Intents are the current route; the repositories remain relevant only for their separate research and reproduction problems.
- 2026-06-08 preview status: the assumption that every iOS 27 or Siri AI feature was generally available is obsolete. Apple’s announcement labels the new features testing, beta, or later-year availability and retains regional and language limits.

## Still unknown

- GAUDI, NeuMan, and Apple Intelligence are not a documented single product lineage. No first-party source read today connects either 2022 repository to the Apple Intelligence product or SDK.
- The June 2026 page still describes iOS 27-era features as future testing, beta, or fall availability. A post-announcement release note was not found that proves every announced feature is live in every region as of 2026-09-03.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/apple/ml-gaudi | GAUDI: A Neural Architect for Immersive 3D Scene Generation — apple/ml-gaudi | 2026-09-03 |
| https://github.com/apple/ml-neuman | NeuMan: Neural Human Radiance Field from a Single Video — apple/ml-neuman | 2026-09-03 |
| https://www.apple.com/newsroom/2026/06/apple-intelligence-brings-powerful-ai-capabilities-into-everyday-experiences/ | Apple Intelligence brings powerful AI capabilities into everyday experiences | 2026-09-03 |
| https://developer.apple.com/apple-intelligence/ | Apple Intelligence — Apple Developer | 2026-09-03 |
| https://support.apple.com/en-ie/121115 | How to get Apple Intelligence — Apple Support | 2026-09-03 |
| https://developer.apple.com/documentation/technologyoverviews/generative-models?changes=_2%2C_2 | Generative models and machine learning — Apple Developer Documentation | 2026-09-03 |
| https://developer.apple.com/videos/play/wwdc2025/260/ | Develop for Shortcuts and Spotlight with App Intents — WWDC25 | 2026-09-03 |

## Agent brief {#agent-brief}

- **Subject:** `organization:apple`, thread `apple-ai-research-to-product`, 3 dated events 2022-08-05 → 2026-06-09.
- **Practical note:** As of 2026-06-09, practitioners tracking Apple should distinguish its public machine-learning research releases from its product-facing Apple Intelligence announcements, while following both as connected evidence of the company’s AI development.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
