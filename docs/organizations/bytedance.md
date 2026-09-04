---
title: ByteDance — ByteDance AI development and compute constraints
category: organizations
tags: [bytedance, bytedance-ai-development-and-compute-constraints, bytedance-long-cot-reasoning, bytedance_nvidia_chip_ban, omnihuman, organization]
aliases: ["ByteDance"]
---

# ByteDance — ByteDance AI development and compute constraints

**Development line:** `organization:bytedance` · thread `bytedance-ai-development-and-compute-constraints`  
**Events:** 2 dated, 2025-02-04 → 2025-11-28 · **Researched:** 2026-09-03 · confidence: medium

## What it is

ByteDance — for teams choosing a specific product or model route. Capabilities: consumer and enterprise applications; Seed agents for tool use, coding, and multimodal work; research on video avatars and long-chain-of-thought training. Limit: the official OmniHuman-1 page still says it offers no service or download. Verdict: use a named Doubao or Volcano Engine offering for production; treat OmniHuman and the Long-CoT paper as research until a direct access contract exists.

## Development line

- **2025-02-04 — ByteDance presented OmniHuman-1 for conditioned human animation.** On 2025-02-04, ByteDance Intelligent Creation presented OmniHuman-1, an end-to-end framework for generating human video from a single image and motion signals. The project described audio-only, video-only, and combined conditioning, including support for portrait, half-body, and full-body inputs.
- **2025-11-28 — Report said Chinese regulators blocked ByteDance from using Nvidia chips.** On 2025-11-28, a Reuters report said Chinese regulators had blocked ByteDance from using Nvidia chips, citing The Information. The reported restriction was a material constraint on the company's access to Nvidia-based AI compute.

## What changed

ByteDance — 2025-02-04: OmniHuman-1 demonstrated human-video generation from one image plus audio, video, or both, but explicitly offered no service or download. 2025-08-26 (found today): OmniHuman-1.5 added semantic image-and-voice animation with optional text control, multi-person scenes, and demonstrations over one minute; it remains presented as an original research model. 2025-11-28: Reuters reported that Chinese regulators had barred ByteDance from deploying Nvidia chips in new data centers; ByteDance had not commented, so this changes infrastructure-risk assessment rather than product availability. 2026-02-22: the Long-CoT preprint described deep reasoning, self-reflection, and self-exploration as trainable trajectory structures and proposed Mole-Syn; it was a research result, not a model release. 2026-06-23 (found today): ByteDance announced Seed2.1 access for Doubao and Volcano Engine users, providing a current product-specific route.

## How to use this

From 2025-02-04, practitioners should track ByteDance's human-animation research as a distinct AI capability line; from 2025-11-28, they should treat Nvidia-compute access in China as a reported deployment and capacity risk.

1. Choose the exact model or media product from the Seed catalog before designing an integration; do not start from a generic ByteDance-company assumption.
  — <https://seed.bytedance.com/en/models?view_from=homepage_tab>
2. For agent, coding, reasoning, or multimodal work, use the announced Doubao or Volcano Engine route for Seed2.1 and validate it first on a bounded end-to-end task.
  — <https://seed.bytedance.com/en/blog/seed2-1-officially-released-advancing-ai-productivity>
3. For avatar research, use OmniHuman-1.5 to define an evaluation with an image, voice track, and optional text prompt; do not represent the demonstration as a production API.
  — <https://omnihuman-lab.github.io/v1_5/>
4. For Long-CoT training research, test trajectories containing deep reasoning, self-reflection, and self-exploration against a baseline rather than copying surface keywords.
  — <https://arxiv.org/abs/2601.06002>

## Best practices

- ByteDance — name the product, version, and access route in architecture and procurement records; the current catalog contains distinct models with different capabilities.
  — <https://seed.bytedance.com/en/models?view_from=homepage_tab>
- Seed2.1 — validate completed workflow output, not a single response, because the stated use cases depend on tool use, intermediate results, and repeated validation.
  — <https://seed.bytedance.com/en/blog/seed2-1-officially-released-advancing-ai-productivity>
- OmniHuman-1 — do not install or buy a service claiming to be official: the project page says there are no official services or downloads.
  — <https://omnihuman-lab.github.io/>
- OmniHuman-1.5 — obtain rights and consent for image and voice inputs; the demonstrations are research capability evidence, not a deployment safety workflow.
  — <https://omnihuman-lab.github.io/v1_5/>
- ByteDance infrastructure — treat the Nvidia report as a capacity and supply-risk signal, then recheck applicable regulatory, contractual, and deployment facts before committing production capacity.
  — <https://www.investing.com/news/stock-market-news/chinese-regulators-block-bytedance-from-using-nvidia-chips-the-information-reports-4379649>
- Long-CoT research — preserve and measure reasoning behavior, not trigger phrases; the paper attributes stable learning to structural trajectories rather than keyword imitation.
  — <https://arxiv.org/abs/2601.06002>

## Superseded by this

- 2025-02-04: OmniHuman-1 alone is no longer the current avatar-research reference; OmniHuman-1.5 adds semantic audio/image/text conditioning and multi-person demonstrations, but not a confirmed public service.
- 2025-11-28: an assumption that ByteDance can plan new China data-center capacity around Nvidia hardware is no longer safe; the reported restriction must be rechecked as an infrastructure fact, not treated as a user-facing product change.
- 2026-02-22: treating the Long-CoT preprint as the way to obtain a ByteDance reasoning model is obsolete; Seed2.1 was announced as accessible through Doubao and Volcano Engine on 2026-06-23.

## Still unknown

- ByteDance is an umbrella company: its avatar research, Long-CoT training paper, and chip-procurement report do not form one public tool or one shared user workflow.
- No official public OmniHuman-1 or OmniHuman-1.5 API, weights, pricing, regional availability, or production safety workflow was found; OmniHuman-1 explicitly says it has no services or downloads.
- The Nvidia restriction is a Reuters report attributed to The Information and unnamed employees; no public ByteDance or Chinese-regulator confirmation or current implementation update was found.
- The Long-CoT work is a preprint, and no linked official code, model release, or API was found on its paper page.

## Sources

| source | title | read |
|---|---|---|
| https://www.bytedance.com/en/products?type=services | ByteDance — Our Products | 2026-09-03 |
| https://seed.bytedance.com/en/models?view_from=homepage_tab | Seed Models | 2026-09-03 |
| https://seed.bytedance.com/en/blog/seed2-1-officially-released-advancing-ai-productivity | Seed2.1 Officially Released: Advancing AI Productivity | 2026-09-03 |
| https://omnihuman-lab.github.io/ | OmniHuman-1: Rethinking the Scaling-Up of One-Stage Conditioned Human Animation Models | 2026-09-03 |
| https://arxiv.org/abs/2502.01061 | OmniHuman-1: Rethinking the Scaling-Up of One-Stage Conditioned Human Animation Models | 2026-09-03 |
| https://omnihuman-lab.github.io/v1_5/ | OmniHuman-1.5 | 2026-09-03 |
| https://arxiv.org/abs/2508.19209 | OmniHuman-1.5: Instilling an Active Mind in Avatars via Cognitive Simulation | 2026-09-03 |
| https://www.reuters.com/world/china/chinese-regulators-block-bytedance-using-nvidia-chips-information-reports-2025-11-26/ | Chinese regulators block ByteDance from using Nvidia chips, The Information reports | 2026-09-03 |
| https://www.investing.com/news/stock-market-news/chinese-regulators-block-bytedance-from-using-nvidia-chips-the-information-reports-4379649 | Chinese regulators block ByteDance from using Nvidia chips, The Information reports By Reuters | 2026-09-03 |
| https://arxiv.org/abs/2601.06002 | The Molecular Structure of Thought: Mapping the Topology of Long Chain-of-Thought Reasoning | 2026-09-03 |

## Agent brief {#agent-brief}

- **Subject:** `organization:bytedance`, thread `bytedance-ai-development-and-compute-constraints`, 2 dated events 2025-02-04 → 2025-11-28.
- **Practical note:** From 2025-02-04, practitioners should track ByteDance's human-animation research as a distinct AI capability line; from 2025-11-28, they should treat Nvidia-compute access in China as a reported deployment and capacity risk.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
