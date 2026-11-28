---
title: "Wevisone Vl: wevisone-vl-release — Wevisone Vl Release"
category: "projects"
date: 2026-10-28
tags: ["project", "wevisone-vl", "wevisone-vl-release"]
aliases: ["Wevisone Vl: wevisone-vl-release"]
---

# Wevisone Vl: wevisone-vl-release — Wevisone Vl Release

**Development line:** project:wevisone-vl · thread wevisone-vl-release  
**Last event:** 2026-10-28 · 2 dated since 2026-10-23 · **Researched:** 2026-11-28 · confidence: high

## What it is

WeVisOne-VL is a Qwen3-VL-based vision-language model for teams that need boxes, points, text coordinates, masks or alpha mattes from one image workflow. It covers detection, referring localization, counting, pointing, OCR, segmentation and matting. Its pixel decoder has 9.6 million parameters, while released checkpoints include 2B and 4B variants. The practical verdict is that it can consolidate several image-region tasks, but its local environment should be validated before deployment.

## Development line

- **2026-10-23 — Tencent releases WeVisOne-VL-2B unified vision model.** A post from the GreenNeuralRobots channel describes Tencent's WeVisOne-VL-2B, a single 2B-parameter vision model built on Qwen3-VL that handles detection, open-vocabulary localization, object counting, point prompting, OCR with coordinates, text-prompted segmentation, and alpha matting. It is limited to single images and is noted as weak on complex transparency and heavy occlusion. Code and model links were shared.
  - The official model-repository history records the release of WeVisOne-VL-2B weights and model card at 06:43, providing a precise public release record for the 2B checkpoint. (2026-10-23) — <https://huggingface.co/tencent/WeVisOne-VL-2B/commits/main>
  - The model card identifies the released checkpoint as Tencent/WeVisOne-VL-2B, built on Qwen3-VL with a 9.6M-parameter pixel decoder for object-level and pixel-level perception. (2026-10-23) — <https://huggingface.co/tencent/WeVisOne-VL-2B>
- **2026-10-28 — Wevisone Vl: wevisone-vl-release update.** The WeVisOne-VL-2B repository updated its model weights to BF16; the commit notes that BF16 inference defaults were retained. (found in research)

## What changed

Model release \(2026-10-23\): Tencent published WeVisOne-VL-2B weights and its model card. Weight revision \(2026-10-28\): the 2B repository changed model-weight storage to BF16 while retaining BF16 inference defaults.

## How to use this

1. Clone the repository, create the documented environment, install its requirements and install the package in editable mode.
  — <https://github.com/Tencent/WeVisOne-VL>
2. Load either the 2B or 4B checkpoint, convert the input to RGB and call \`model.predict\` with the task and task-specific query.
  — <https://github.com/Tencent/WeVisOne-VL>
3. Consume the documented output type for the selected task: boxes, points, text with boxes, masks or alpha mattes.
  — <https://github.com/Tencent/WeVisOne-VL>

## Best practices

- Handle \`None\` as an absent-target result for referring queries instead of treating it as a detected object.
  — <https://github.com/Tencent/WeVisOne-VL>
- Resolve the current dependency set in a tested environment before deployment: a practitioner reports that the documented Python 3.10 setup conflicts with a pinned matplotlib version requiring Python 3.11 or later.
  — <https://github.com/Tencent/WeVisOne-VL/issues/15>

## What practitioners say

- One practitioner reports that following the documented Python 3.10 installation path fails because the pinned matplotlib dependency requires Python 3.11 or later; the issue had no recorded maintainer resolution when read. (2026-11-24)
  — <https://github.com/Tencent/WeVisOne-VL/issues/15>

## Superseded by this

- The pre-2026-10-28 2B weight-storage revision is superseded by the BF16 weight update; BF16 inference defaults remain in effect.
  — <https://huggingface.co/tencent/WeVisOne-VL-2B/commits/main>

## Still unknown

- The inspected public materials do not provide an independently reproduced assessment of performance under heavy occlusion or complex transparency.
- The repository announces later training-code availability only by month, so no exact-date training-code release event is included.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Tencent/WeVisOne-VL | Tencent/WeVisOne-VL | 2026-11-28 |
| https://github.com/Tencent/WeVisOne-VL/blob/main/README_zh-CN.md | WeVisOne-VL README \(Simplified Chinese\) | 2026-11-28 |
| https://huggingface.co/tencent/WeVisOne-VL-2B | tencent/WeVisOne-VL-2B | 2026-11-28 |
| https://huggingface.co/tencent/WeVisOne-VL-2B/commits/main | Commit history · tencent/WeVisOne-VL-2B | 2026-11-28 |
| https://github.com/Tencent/WeVisOne-VL/issues/15 | Installation failure: Python version incompatibility between README and requirements.txt · Issue \#15 | 2026-11-28 |

## Agent brief {#agent-brief}

- **Subject:** project:wevisone-vl, thread wevisone-vl-release, 2 dated events 2026-10-23 → 2026-10-28.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
