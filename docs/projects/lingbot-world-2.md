---
title: LingBot-World 2.0
category: projects
date: 2026-07-09
tags: [lingbot-world, lingbot-world-2, lingbot-world-2-development, project]
aliases: ["LingBot-World 2.0"]
---

# LingBot-World 2.0

**Development line:** `project:lingbot-world-2` · thread `lingbot-world-2-development`  
**Last event:** 2026-07-09 · 1 dated since 2026-07-09 · **Researched:** 2026-09-05 · confidence: high

## What it is

LingBot-World 2.0, also called LingBot-World-Infinity, generates navigable image-to-video worlds for researchers and developers. It supports unbounded streaming, action conditioning, and a pilot or director agent harness. The public local checkpoint is `robbyant/lingbot-world-v2-14b-causal-fast` (14B). The repository documents 480p multi-GPU inference, while Reactor hosts `reactor/lingbot-world-2` at 1664×960 and 48 fps. We use Reactor for prototypes and the 14B repository release for non-commercial research, not for self-hosted real-time deployment.

## Development line

- **2026-07-09 — LingBot-World 2.0 public development resources were linked.** On 2026-07-09, a record linked LingBot-World 2.0 to its project page, GitHub repository, Hugging Face collection, and Reactor page. This marks a public milestone, though the source does not detail release contents, capabilities, or operational status.

## What changed

- **2026-07-08** — The technical report reached arXiv, describing the 14B model and a planned 1.3B counterpart.
- **2026-07-09** — LingBot-World 2.0 published its report, code, and models. The working open checkpoint was `lingbot-world-v2-14b-causal-fast`. The 14B causal-pretrain, 14B bidirectional, and 1.3B variants remained listed as TODO. The release added causal long-horizon generation, a distilled real-time variant, action and text controls, multi-player support, and a pilot/director harness.
- **2026-07-10** — The repository renamed a causal class for code maintenance, with no new capability.
- **2026-07-14** — The repository revised a video prompt description in documentation, without a new model release.

## How to use this

As of 2026-07-09, treat LingBot-World 2.0 as its own line. Review the project page, repository, model collection, and Reactor docs before adopting it.

1. For a hosted prototype, scaffold a Reactor application with `npx create-reactor-app my-lingbot-world-2-app --model=lingbot-world-2`.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
2. Open a session with model name `reactor/lingbot-world-2`, upload a reference image, set a text prompt, then send `start`. Generation fails until both image and prompt are present.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
3. Steer the running world with longitudinal and lateral movement, look controls, or `set_camera_pose`. Update conditions mid-stream with `set_prompt`.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
4. For local research inference, clone the repository, install requirements with Torch 2.4+ and FlashAttention, download `robbyant/lingbot-world-v2-14b-causal-fast`, then run the provided multi-GPU causal-fast command or `run_fast.sh`.
  — <https://github.com/robbyant/lingbot-world-v2>

## Best practices

- Separate prompts into base, camera, movement, event, and vertical-control layers. Keep each layer on one control axis so prompts do not fight active motion.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/prompt-guide>
- Keep total prompt length under roughly 2,000 characters. Trim event clauses before base identity or control rules.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/prompt-guide>
- Treat movement as persistent state and send an explicit idle command. Short taps can miss the chunk boundary.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
- Do not expect official deployment code for the open model. The repository withholds it, and the license is CC BY-NC-SA 4.0 for non-commercial use.
  — <https://github.com/robbyant/lingbot-world-v2>

## Superseded by this

- **2026-07-09** — LingBot-World 1.0 notes are obsolete on Reactor. World 2 replaces them with two-axis navigation, camera poses, and mid-stream prompt steering.
- **2026-07-09** — Expecting every announced 14B and 1.3B model to download is obsolete. Only the 14B causal-fast checkpoint is public; the rest remain TODO.

## Still unknown

- The July 9 post claims the real-time model runs 720p at 60 fps, while Reactor specifies 1664×960 at 48 fps. The sources provide no direct comparison.
- The repository withholds deployment code. Hardware requirements, serving stack, and latency for official real-time serving remain undocumented.
- The arXiv paper describes a 1.3B counterpart, but the July 9 repository TODO list provides no downloadable 1.3B weights or code.

## Sources

| source | title | read |
|---|---|---|
| https://technology.robbyant.com/lingbot-world-v2 | LingBot-World 2.0 project page | 2026-09-05 |
| https://github.com/robbyant/lingbot-world-v2 | Robbyant/lingbot-world-v2 | 2026-09-05 |
| https://huggingface.co/collections/robbyant/lingbot-world-v2 | LingBot-World-V2 collection | 2026-09-05 |
| https://www.reactor.inc/lingbot-world-2 | LingBot World 2 — Reactor | 2026-09-05 |
| https://arxiv.org/abs/2607.07534 | Infinite Worlds with Versatile Interactions | 2026-09-05 |
| https://github.com/robbyant/lingbot-world-v2/commits/main | LingBot-World-V2 commit history | 2026-09-05 |
| https://huggingface.co/robbyant/lingbot-world-v2-14b-causal-fast | robbyant/lingbot-world-v2-14b-causal-fast | 2026-09-05 |
| https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview | LingBot World 2 overview | 2026-09-05 |
| https://docs.reactor.inc/model-api-reference/lingbot-world-2/prompt-guide | LingBot World 2 prompt guide | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:lingbot-world-2`, thread `lingbot-world-2-development`, 1 dated events 2026-07-09 → 2026-07-09.
- **Practical note:** As of 2026-07-09, treat LingBot-World 2.0 as a distinct line. Review the project, code, collection, and product docs before adoption.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
