---
title: "Focusgui: focusgui-adapter-release — Focusgui Adapter Release"
category: "projects"
date: 2026-10-21
tags: ["focusgui", "focusgui-adapter-release", "project"]
aliases: ["Focusgui: focusgui-adapter-release"]
---

# Focusgui: focusgui-adapter-release — Focusgui Adapter Release

**Development line:** project:focusgui · thread focusgui-adapter-release  
**Last event:** 2026-10-21 · 1 dated since 2026-10-21 · **Researched:** 2026-11-28 · confidence: medium

## What it is

FocusGUI is a lightweight adapter for omni-modal GUI agents, described in a 2026 preprint by researchers at Nanyang Technological University and Alibaba Group. It scores seven evidence channels \(text/history, screen, audio, video, interaction state, full-modal hidden features, screen spatial features\) against a step-specific decision reference. It compresses the weighted evidence into a 64-dimensional latent, projects that latent back into the decoder's embedding space, and adds it as a zero-initialized residual to four existing prompt positions. The backbone stays frozen and no extra prompt tokens are added.

## Development line

- **2026-10-21 — FocusGUI lightweight adapter for omnimodal GUI agents announced.** A post introduced FocusGUI, a lightweight adapter for omnimodal GUI agents. It combines seven input channels, reweights them per step, compresses them into a 64-number latent that is injected into decoder embeddings, freezes the base model, and trains only the adapter on next-action supervision without relevance labels.
  - The project page confirms the announced design and adds detail: 128-dimensional channel projections, a 64-dimensional latent, a zero-initialized residual added to four existing prompt positions with no extra prompt tokens, and training from next-action token negative log-likelihood alone. Trainable parameters are 1.15–1.45 M. It was evaluated on OmniGUI \(29 applications, 708 episodes, 2,572 action steps, episode-disjoint splits\) with best Type and Exact Match in 24 of 24 backbone-by-category cells. Authors are from Nanyang Technological University and Alibaba Group. (undated \(page labelled Preprint · 2026\)) — <https://fyzhang1.github.io/FocusGUI/>

## What changed

The project page presents the method as a response to what the authors call Sequential Distraction, where uniformly exposing all context at every step lets irrelevant signals cause wrong actions that feed back into later observations. It reports that FocusGUI raises overall Type Match by 33.2 percentage points and Exact Match by 3.0x \(from 11.2% to 33.5%\) over the frozen backbone, averaged across four omni-modal backbones. It also reports a Type Match gain of 30.1 over the strongest existing enhancement method.

## How to use this

1. Start from a frozen omni-modal GUI-agent backbone and keep its encoders, decoder and language-model head unchanged; attach the FocusGUI adapter, which is the only trained component.
  — <https://fyzhang1.github.io/FocusGUI/>
2. Map the seven channels \(text/history, screen, audio, video, interaction state, full-modal hidden features, screen spatial features\) to a shared 128-dimensional space, and compute step-specific channel weights against a decision reference derived from the current observation.
  — <https://fyzhang1.github.io/FocusGUI/>
3. Aggregate the weighted channels into a 64-dimensional latent, project it into the decoder embedding space, and add it as a zero-initialized residual to four existing prompt positions before the action boundary.
  — <https://fyzhang1.github.io/FocusGUI/>
4. Train for three epochs with AdamW \(learning rate 2e-4, weight decay 1e-3\) using next-action token negative log-likelihood as the only supervision.
  — <https://fyzhang1.github.io/FocusGUI/>

## Best practices

- Train from action supervision alone; the page states that neither modality-relevance labels nor backbone fine-tuning are required.
  — <https://fyzhang1.github.io/FocusGUI/>
- Keep the full original observation and backbone parameters intact and inject only a small residual into existing prompt embeddings, so the native agent is preserved \(the non-intrusive principle\).
  — <https://fyzhang1.github.io/FocusGUI/>
- Use episode-disjoint splits when evaluating on OmniGUI, as the authors do.
  — <https://fyzhang1.github.io/FocusGUI/>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The page is undated beyond 'Preprint · 2026', and the results are the authors' own, with no independent replication found in the supplied pages.
- The page excerpt names neither the four backbones other than Qwen2.5-Omni \(used in the ablation\) nor the baseline enhancement methods.
- The page does not say whether code and weights are released; the excerpt only shows Paper and Code links without their targets.

## Sources

| source | title | read |
|---|---|---|
| https://fyzhang1.github.io/FocusGUI/ | FocusGUI — Focused Omni-Modal GUI Agents | 2026-10-21 |

## Agent brief {#agent-brief}

- **Subject:** project:focusgui, thread focusgui-adapter-release, 1 dated events 2026-10-21 → 2026-10-21.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
