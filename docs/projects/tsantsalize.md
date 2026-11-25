---
title: TSANTSALIZE — Public model availability
category: projects
date: 2026-06-19
tags: [ltx_2_3, project, public-model-availability, tsantsalize]
aliases: ["TSANTSALIZE"]
---

# TSANTSALIZE — Public model availability

**Development line:** `project:tsantsalize` · thread `public-model-availability`  
**Last event:** 2026-06-19 · 1 dated since 2026-06-19 · **Researched:** 2026-09-05 · confidence: medium

## What it is

TSANTSALIZE is an LTX-2.3 video-to-video IC-LoRA for ComfyUI users who want a deliberate small-head effect on a speaking performer.

- Reshapes the speaking subject from a reference clip.
- Keeps voice processing outside the adapter in a bundled audio workflow.

## Development line

- **2026-06-19 — TSANTSALIZE Hugging Face model resource recorded.** TSANTSALIZE entered use as an LTX-2.3 IC-LoRA to shrink a speaking subject's head. The release note is dated 2026-06-18 and specifies video-to-video with first-frame conditioning. Voice alteration stays in a workflow-side audio chain.

## What changed

2026-06-19: TSANTSALIZE entered use as an LTX-2.3 IC-LoRA to shrink a speaking subject's head. The release note is dated 2026-06-18 and specifies video-to-video with first-frame conditioning. Voice alteration stays in a workflow-side audio chain.

## How to use this

Check the linked Hugging Face repository for the recorded public TSANTSALIZE model resource from 2026-06-19, and verify its files, license, and usage instructions independently.

1. Download the TSANTSALIZE checkpoint and included ComfyUI workflow from the model repository.
  — <https://huggingface.co/TheBurgstall/tsantsalize>
2. Run it with an LTX-2.3-compatible ComfyUI video-to-video workflow and a speaking-person reference clip; the adapter does not itself transform the voice.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
3. For a mild proportion change, use LoRA strength around 0.5; for the intended effect, use the creator-reported 1.2 setting. Add `tsantsalize` to the prompt; `tiny head` can help.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
4. Use the supplied audio nodes separately when altered audio is wanted: the workflow applies pitch shifting, vocal high-pass processing, and MelBand RoFormer separation.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
5. Before running it on a current LTX installation, verify that the adapter, base model, nodes, and workflow version match; LTX documents version matching as required for IC-LoRAs.
  — <https://docs.ltx.io/open-source-model/usage-guides/ic-lo-ra>

## Best practices

- Start with a single person speaking to camera. The creator reports materially less predictable results on other footage.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
- Keep strength at or below 1.2 for the full effect, and use about 0.5 when only a small adjustment is wanted. Settings above 1.2 caused identity drift in the creator’s tests.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
- Do not treat negative strength as a proven way to enlarge heads: the creator did not test it for this adapter and reported that it had failed on earlier IC-LoRAs.
  — <https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/>
- Match reference-video resolution and frame rate to the generation, test a simple clip first, and compare output with and without the adapter before attempting a complex shot.
  — <https://docs.ltx.io/open-source-model/usage-guides/ic-lo-ra>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The exact checkpoint filename, license, immutable revision, workflow JSON, and all custom-node dependencies were not independently recovered from the model repository.
- No dated port, successor, benchmark, or verified LTX-2.5 compatibility test was found.
- The creator’s 1.2 LoRA-strength setting is not demonstrably equivalent to the current LTX-2.5 `attention_strength` control, which is documented on a 0–1.0 scale.
- The release note is dated 2026-06-18 while the recorded event is 2026-06-19; the evidence does not establish whether 19 June was a separate model revision or later circulation of the same release.
- Hugging Face search snapshots conflict: a model-catalog snapshot lists TSANTSALIZE as updated on 2026-06-18, while a profile snapshot says it was updated five days earlier without a calendar date or revision. That is insufficient to create a later dated event.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/TheBurgstall/tsantsalize | TheBurgstall/tsantsalize model repository | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1u9aux9/tsantsalize_the_most_useless_iclora_youll/ | TSANTSALIZE — the most useless IC-LoRA you'll download today | 2026-09-05 |
| https://docs.ltx.io/open-source-model/usage-guides/ic-lo-ra | IC-LoRA | LTX Documentation | 2026-09-05 |
| https://docs.ltx.io/open-source-model/integration-tools/ic-lo-ra-adapters | IC-LoRA Adapters | LTX Documentation | 2026-09-05 |
| https://huggingface.co/TheBurgstall | TheBurgstall | Hugging Face | 2026-09-05 |
| https://huggingface.co/TheBurgstall/models | TheBurgstall models | Hugging Face | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:tsantsalize`, thread `public-model-availability`, 1 dated events 2026-06-19 → 2026-06-19.
- **Practical note:** From 2026-06-19, practitioners should check the linked Hugging Face repository as the recorded public TSANTSALIZE model resource, while verifying its current files, license, and usage instructions independently.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
