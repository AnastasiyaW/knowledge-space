---
title: JoyCaption
category: projects
tags: [joycaption, joycaption-development, project]
aliases: ["JoyCaption"]
---

# JoyCaption

**Development line:** `project:joycaption` · thread `joycaption-development`  
**Events:** 2 dated, 2024-09-26 → 2025-05-13 · **Researched:** 2026-09-04 · confidence: medium

## What it is

JoyCaption is an open image-captioning VLM for diffusion-model dataset builders, a local alternative to paid captioning APIs such as GPT-4o.

- Produces descriptive and concise factual captions.
- Generates diffusion-style prompts and several tag-list formats.
- Runs through Transformers, a batch script, or a vLLM OpenAI-compatible endpoint.

## Development line

- **2024-09-26 — JoyCaption Alpha One Hugging Face Space recorded.** On 2024-09-26, JoyCaption launched as the Hugging Face Space fancyfeast/joy-caption-alpha-one. The demo established Alpha One, without public model details or release notes.
- **2025-05-13 — JoyCaption Beta One public references recorded.** On 2025-05-13, JoyCaption added Beta One with a GitHub repository, a Hugging Face Space, a Hugging Face model page, and a Civitai article. These links established Beta One, without technical comparisons against Alpha One.

## What changed

JoyCaption development line:

- 2024-09-26 — Alpha One launched as a public Hugging Face Space for interactive captioning.
- 2025-05-13 — Beta One added the downloadable model, an updated demo, and local scripts; it improved instruction following over Alpha Two, but stayed in beta.
- Found today — the official README still names Beta One as current; GitHub Releases has no packaged release, and the project has not declared 1.0.

## How to use this

From 2024-09-26, we had the Alpha One Hugging Face Space as a reference; by 2025-05-13, we track Beta One across its repository, Space, model page, and article instead of the old Alpha link.

1. Try the official Beta One demo first and inspect the output mode and generated prompt before automating a workflow.
  — <https://github.com/fpgaminer/joycaption>
2. For local use, load `fancyfeast/llama-joycaption-beta-one-hf-llava` with Transformers, send an image-plus-text message, generate, and decode only the newly generated tokens.
  — <https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava>
3. Choose `Descriptive Caption` for detailed training text or `Straightforward` for concise, concrete labels; express length and tone in the documented prompt form.
  — <https://github.com/fpgaminer/joycaption>
4. For a dataset, run `batch-caption.py` with `--glob` or `--filelist` plus `--prompt` or a weighted `--prompt-file`; captions are written as adjacent `.txt` files.
  — <https://github.com/fpgaminer/joycaption/blob/main/scripts/README.md>
5. For an application endpoint, serve Beta One with vLLM and call its OpenAI-compatible chat-completions API.
  — <https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava>

## Best practices

- Pass `--model` explicitly in batch jobs: the script documentation still defaults to Alpha Two, so accepting its default can select an older model.
  — <https://github.com/fpgaminer/joycaption/blob/main/scripts/README.md>
- Start with Descriptive or Straightforward mode; the maintainer identifies them as the most useful and labels several other modes less stable.
  — <https://github.com/fpgaminer/joycaption>
- Audit labels used for training or decisions, especially for multiple subjects, left/right relations, OCR, and instruction following; Beta One documents residual failures and glitches.
  — <https://github.com/fpgaminer/joycaption>
- In direct LLaVA integrations, preserve the documented chat-template path and inspect input IDs so duplicate BOS tokens do not degrade output.
  — <https://github.com/fpgaminer/joycaption>
- Use 8-bit or 4-bit quantization when native bfloat16 will not fit, rather than assuming the model is lightweight.
  — <https://github.com/fpgaminer/joycaption>

## Superseded by this

- 2024-09-26 — JoyCaption Alpha One: superseded for new work by Beta One, which the official README still identifies as the current model.
- 2024-09-26 — Alpha-era expectations of reliable captioning: superseded by the more capable Beta One workflow, but not by a 1.0 reliability claim.

## Still unknown

- No first-party announcement establishes a post-Beta-One release or confirms active maintenance after the 2025 model and demo updates.
- The cited release article https://civitai.com/articles/14672 returned an error during research, so its release notes were not used.
- The hosted Beta One Space is listed as Running on Zero; it was not executed, so live availability, cold-start time, and output quality were not independently tested.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/fpgaminer/joycaption | JoyCaption — official GitHub repository and README | 2026-09-04 |
| https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava | llama-joycaption-beta-one-hf-llava — Hugging Face model card | 2026-09-04 |
| https://github.com/fpgaminer/joycaption/blob/main/scripts/README.md | JoyCaption batch-caption.py documentation — GitHub | 2026-09-04 |
| https://huggingface.co/spaces/fancyfeast/joy-caption-beta-one | Joy Caption Beta One — Hugging Face Space | 2026-09-04 |
| https://huggingface.co/spaces/fancyfeast/joy-caption-alpha-one | Joy Caption Alpha One — Hugging Face Space | 2026-09-04 |
| https://github.com/fpgaminer/joycaption/releases | JoyCaption releases — GitHub | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:joycaption`, thread `joycaption-development`, 2 dated events 2024-09-26 → 2025-05-13.
- **Practical note:** From 2024-09-26, practitioners could use the Alpha One Hugging Face Space as a public JoyCaption reference; by 2025-05-13, they should also consult the linked Beta One repository, Space, model page, and article rather than relying on the earlier Alpha reference alone.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
