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

LingBot-World 2.0, also called LingBot-World-Infinity, is a world-model release for researchers and developers building navigable image-to-video worlds.

- Unbounded-stream generation for continuous video.
- Action-conditioned interaction across camera and movement controls.
- Agentic pilot and director concept for environment steering.

The public local checkpoint is `robbyant/lingbot-world-v2-14b-causal-fast` (14B) with documented 480p multi-GPU inference; Reactor exposes `reactor/lingbot-world-2` at 1664×960 and 48 fps. Use Reactor for an application prototype and the 14B repository release for non-commercial research, not as a turnkey self-hosted real-time deployment.

## Development line

- **2026-07-09 — LingBot-World 2.0 public development resources were linked.** On 2026-07-09, public links connected LingBot-World 2.0 to a project page, GitHub repository, Hugging Face collection, and Reactor page. This marks a public project milestone, though the sources do not establish release contents, capabilities, or operational status.

## What changed

- 2026-07-08 — The technical report was submitted to arXiv, describing the 14B model and a planned 1.3B counterpart.
- 2026-07-09 — LingBot-World 2.0 released its technical report, inference code, and models. The release’s usable open checkpoint was specifically `lingbot-world-v2-14b-causal-fast`; the 14B causal-pretrain, 14B bidirectional, and 1.3B variants remained listed as TODO. The step added causal long-horizon generation, a distilled real-time variant, broader action/text-event controls, multi-player support, and a pilot/director agent harness.
- 2026-07-10 — The repository renamed a causal class; this was a code-maintenance update rather than a documented new model capability.
- 2026-07-14 — The repository revised a video prompt description; this was a documentation-level update, not a separately announced model release.

## How to use this

As of 2026-07-09, practitioners should treat LingBot-World 2.0 as a distinct project line and consult its linked project, code, model-collection, and product resources before evaluating or adopting it.

1. For a hosted prototype, scaffold a Reactor application with `npx create-reactor-app my-lingbot-world-2-app --model=lingbot-world-2`.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
2. Open a session with model name `reactor/lingbot-world-2`, upload a reference image, set a text prompt, then send `start`; generation fails until both image and prompt are set.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
3. Drive the running world with longitudinal and lateral movement, look controls, or `set_camera_pose`; change conditions mid-stream with `set_prompt`.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
4. For local research inference, clone the repository, install its requirements with Torch 2.4+ and FlashAttention, download `robbyant/lingbot-world-v2-14b-causal-fast`, then run the provided multi-GPU causal-fast command or `run_fast.sh`.
  — <https://github.com/robbyant/lingbot-world-v2>

## Best practices

- Compose prompts as separate base, camera, movement, event, and vertical-control layers; keep each layer responsible for one control axis so prompts do not contradict active motion.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/prompt-guide>
- Keep the worst-case composed prompt below roughly 2,000 characters; trim event clauses before the base identity and control contracts.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/prompt-guide>
- Treat movement as persistent state and send an explicit idle command; very brief taps can miss the next chunk boundary.
  — <https://docs.reactor.inc/model-api-reference/lingbot-world-2/overview>
- Do not plan on official deployment code for the open model; the repository explicitly withholds it, and its license is CC BY-NC-SA 4.0 for non-commercial use.
  — <https://github.com/robbyant/lingbot-world-v2>

## Superseded by this

- 2026-07-09 — LingBot-World 1.0 guidance is superseded for Reactor users by World 2’s two-axis navigation, native camera poses, and mid-stream prompt steering.
- 2026-07-09 — Treating every announced 14B and 1.3B variant as downloadable is obsolete: the repository’s documented public checkpoint is the 14B causal-fast variant, while the other listed variants were TODO.

## Still unknown

- The July 9 announcement says the real-time variant can drive 720p at 60 fps, while current Reactor documentation specifies 1664×960 at 48 fps. These are different delivery paths or configurations; the sources do not establish an apples-to-apples benchmark.
- The public repository says its deployment code will not be released, so the exact hardware, serving stack, and latency needed to reproduce the official real-time service are not documented.
- The arXiv report describes a 1.3B counterpart, but the public repository’s July 9 TODO list did not provide downloadable 1.3B weights or inference code.

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
- **Practical note:** As of 2026-07-09, practitioners should treat LingBot-World 2.0 as a distinct project line and consult its linked project, code, model-collection, and product resources before evaluating or adopting it.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
