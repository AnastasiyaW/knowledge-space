---
title: Marlin-2B
category: projects
date: 2026-05-21
tags: [marlin-2b, project]
aliases: ["Marlin-2B"]
---

# Marlin-2B

**Development line:** `project:marlin-2b` · thread `marlin-2b`  
**Last event:** 2026-05-21 · 1 dated since 2026-05-21 · **Researched:** 2026-09-05 · confidence: medium

## What it is

Marlin-2B is a 2B video VLM for developers who need timestamped visual indexing.

- Caption: a Scene description plus time-bounded Events.
- Find: a natural-language event query returns a start/end span.

On 2026-09-05, the base model is gated, loads custom code, and has no Hugging Face Inference Provider deployment. Start with bounded captioning or event-location tasks, then test timestamp accuracy on your own footage.

## Development line

- **2026-05-21 — Marlin-2B model page and companion VLM site were shared.** On 2026-05-21, the Marlin-2B development line shared a Hugging Face model page and a companion VLM website. We track this step because it connects the project to public model and usage resources. The dated links alone do not establish the exact release version, capabilities, license, or whether either resource first appeared on that date.

## What changed

- 2026-05-20 — The project said it replaced its BSL 1.1 license with Apache-2.0.
- 2026-05-21 — A provider-support request confirmed the public model identifier, not a hosted endpoint.
- 2026-05-26 — A technical post described the model and its evaluation approach, while audit artifacts remained unreleased.
- 2026-05-29 — An organization-account reply said MLX/MPS was not officially supported yet and named remote NVIDIA plus Hugging Face Transformers as the reference setup.
- 2026-06-24 — The organization listing showed a separate 8-bit MLX distribution line.

## How to use this

We can begin evaluation from the linked Hugging Face model page and companion VLM site starting 2026-05-21, while verifying the model card, supported tasks, license, and exact version before relying on them.

1. Request access to the gated base repository and authenticate; anonymous visitors can list files but cannot download its gated content.
  — <https://huggingface.co/NemoStation/Marlin-2B/tree/main>
2. Install the documented stack: Transformers 5.7 or later, PyTorch 2.11 or later, TorchCodec, qwen-vl-utils, av, and Pillow.
  — <https://huggingface.co/NemoStation/Marlin-2B>
3. Load AutoProcessor and AutoModelForCausalLM with trust_remote_code enabled, BF16, and a CUDA device mapping.
  — <https://huggingface.co/NemoStation/Marlin-2B>
4. Call caption(video) for a parsed scene and event timeline, or find(video, event=...) for a parsed time span.
  — <https://huggingface.co/NemoStation/Marlin-2B>
5. On Apple Silicon, use the separate MLX-8bit route; use a timestamp-aware serving path for temporal grounding rather than a one-shot caption path.
  — <https://huggingface.co/NemoStation/Marlin-2B-MLX-8bit>

## Best practices

- Keep the helper prompt unset unless there is a measured reason to override it. The model card says the canonical training prompt should almost always remain in use.
  — <https://huggingface.co/NemoStation/Marlin-2B>
- Keep the trained preprocessing defaults first: TorchCodec, 2 FPS, 4–240 frames, and about 200K pixels per frame. The default cap covers roughly two minutes.
  — <https://huggingface.co/NemoStation/Marlin-2B>
- Treat span=null or format_ok=false from find() as an unparsable result, not evidence that the event is absent.
  — <https://huggingface.co/NemoStation/Marlin-2B>
- Review remote custom code and pin a reviewed commit hash before enabling trust_remote_code in a production workflow.
  — <https://huggingface.co/docs/transformers/v4.43.3/custom_models>
- Treat reported dense-caption benchmark results as vendor evaluation. The authors said their audit code, prompts, annotations, and GRACE benchmark were still future material in the May 26 post.
  — <https://nemostation.com/blog/marlin-2b-the-map-was-wrong>
- For MLX temporal grounding, preserve per-frame time with a timestamp-aware serving path. The MLX card limits the one-shot route to dense captioning.
  — <https://huggingface.co/NemoStation/Marlin-2B-MLX-8bit>

## Superseded by this

- 2026-05-20 — The previous BSL 1.1 license state was said to be replaced by Apache-2.0.
- 2026-06-24 — The 2026-05-29 statement that MLX/MPS lacked official support is obsolete for the separately listed MLX-8bit distribution; it does not replace the original CUDA/Transformers route.

## Still unknown

- No immutable model-card snapshot, commit SHA, or release record was recovered for 2026-05-21, so we do not backdate current model-card claims to that date.
- Initial publication timestamp of the original checkpoint remains unknown. Primary evidence establishes a May 20 license response and a May 21 provider-support request, not the first upload.
- Hosted-demo availability remains unverified. The demo URL resolved, but exposed no inspectable API contract or successful inference receipt.
- The MLX distribution is a deployment-format change. Retrieved sources do not establish a new core Marlin-2B checkpoint or capability.
- No official minimum NVIDIA VRAM requirement was found.

## Sources

| source | title | read |
|---|---|---|
| https://huggingface.co/NemoStation/Marlin-2B | NemoStation/Marlin-2B · Hugging Face | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B/tree/main | NemoStation/Marlin-2B at main | 2026-09-05 |
| https://huggingface.co/spaces/huggingface/InferenceSupport/discussions/10010 | huggingface/InferenceSupport · NemoStation/Marlin-2B | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B/discussions/1 | NemoStation/Marlin-2B · 👉 Marlin-2B model? "Open Source" -- my ass! | 2026-09-05 |
| https://nemostation.com/blog/marlin-2b-the-map-was-wrong | Part 1: The Map Was Wrong — Nemostation | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B/discussions/9 | NemoStation/Marlin-2B · use marlin on a remote GPU machine ? third party providers ? | 2026-09-05 |
| https://huggingface.co/NemoStation/models | NemoStation (Nemo Station) | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B-MLX-8bit | NemoStation/Marlin-2B-MLX-8bit · Hugging Face | 2026-09-05 |
| https://huggingface.co/docs/transformers/v4.43.3/custom_models | Building custom models · Hugging Face | 2026-09-05 |
| https://vlm.nemostation.com | vlm.nemostation.com | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:marlin-2b`, thread `marlin-2b`, 1 dated events 2026-05-21 → 2026-05-21.
- **Practical note:** We can begin evaluation from the linked Hugging Face model page and companion VLM site starting 2026-05-21, while verifying the model card, supported tasks, license, and exact version before relying on them.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
