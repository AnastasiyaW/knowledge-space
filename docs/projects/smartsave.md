---
title: "Smartsave: comfyui-smartsave — Comfyui Smartsave"
category: "projects"
date: 2026-09-15
tags: ["comfyui-smartsave", "project", "smartsave"]
aliases: ["Smartsave: comfyui-smartsave"]
---

# Smartsave: comfyui-smartsave — Comfyui Smartsave

**Development line:** project:smartsave · thread comfyui-smartsave  
**Last event:** 2026-09-15 · 2 dated since 2026-09-06 · **Researched:** 2026-11-25 · confidence: high

## What it is

SmartSave is a free, open-source ComfyUI custom node that sorts generated images and videos into subject folders using local Ollama (default llama3.2:3b).

- Subject sorting: routes images and videos into dedicated directories to avoid one giant output folder.
- Local inference: runs prompt classification through local Ollama so data stays on your machine.

## Development line

- **2026-09-06 — Smartsave: comfyui-smartsave update.** SmartSave v1.0.0 was published on Civitai as a production release (the page was later updated on 2026-09-14).
- **2026-09-15 — SmartSave - Automatic folder sorting for AI generations.** SmartSave sorts AI outputs into folders by reading prompts with local Ollama. The tool is available on GitHub and Civitai.
  - Civitai documents the node features. The model extracts characters, creators, usernames, LoRA triggers, and single- or multi-word identities anywhere in a prompt. The image node saves a raw PNG master with workflow metadata and a compressed JPEG sharing copy with prompt info in EXIF. A separate SmartSave Video node writes an MP4 master and a WebM copy. When classification is uncertain, files route to Unsorted instead of guessing. The v1.0.0 Auto-Sort was tested on a 1,539-file library, and all 15 regression tests pass. (2026-09-14) — <https://civitai.com/models/2917165/comfyui-smartsave-or-ollama-powered-dynamic-output-sorting>

## What changed

The Civitai page lists the v1.0.0 production release, published Sep 6, 2026 and updated Sep 14, 2026.

- Classification fixes: improves detection for single-word identities and LoRA triggers.
- Safe fallbacks: routes ambiguous prompts to Unsorted instead of guessing.
- File saving: makes image and video saving safer.
- Auto-Sort utility: organizes existing ComfyUI libraries and recovers misclassified outputs.

## How to use this

1. Place the repository in ComfyUI/custom_nodes/ComfyUI-SmartSave and install dependencies from requirements.txt.
  — <https://civitai.com/models/2917165/comfyui-smartsave-or-ollama-powered-dynamic-output-sorting>
2. Install Ollama and pull the default model with `ollama pull llama3.2:3b`, then restart ComfyUI so the SmartSave nodes appear in the node list.
  — <https://civitai.com/models/2917165/comfyui-smartsave-or-ollama-powered-dynamic-output-sorting>
3. To organize an existing library, run auto_sort_preview.bat first (nothing is moved), review proposed changes, then run auto_sort_apply.bat.
  — <https://civitai.com/models/2917165/comfyui-smartsave-or-ollama-powered-dynamic-output-sorting>

## Best practices

- Preview the Auto-Sort plan before applying it. Existing canonical SmartSave folders are trusted by default, and collision protection prevents overwriting destination files.
  — <https://civitai.com/models/2917165/comfyui-smartsave-or-ollama-powered-dynamic-output-sorting>
- Keep files with insufficient prompt evidence in Unsorted rather than forcing a category. Use Auto-Sort to recover them later.
  — <https://civitai.com/models/2917165/comfyui-smartsave-or-ollama-powered-dynamic-output-sorting>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The linked GitHub repository and release pages were not among the supplied pages, so their contents were not checked.
- The Civitai page does not report classification accuracy beyond the 1,539-file library test.

## Sources

| source | title | read |
|---|---|---|
| https://civitai.com/models/2917165/comfyui-smartsave-or-ollama-powered-dynamic-output-sorting | ComfyUI-SmartSave \| Ollama-Powered Dynamic Output Sorting - v1.0.0 \(Civitai\) | 2026-09-15 |

## Agent brief {#agent-brief}

- **Subject:** project:smartsave, thread comfyui-smartsave, 2 dated events 2026-09-06 → 2026-09-15.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
