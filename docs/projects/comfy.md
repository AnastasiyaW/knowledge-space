---
title: "Comfy Cloud — Cloud access"
category: "projects"
date: 2026-11-19
tags: ["cloud-access", "comfy", "project"]
aliases: ["Comfy Cloud"]
---

# Comfy Cloud — Cloud access

Comfy Cloud is a hosted runtime for ComfyUI node graphs, an alternative to self-hosted RunPod or a local desktop install.

**Development line:** project:comfy · thread cloud-access  
**Last event:** 2026-11-19 · 3 dated since 2026-03-03 · **Researched:** 2026-11-20 · confidence: high

## What it is

Comfy Cloud is a managed cloud platform for ComfyUI node graphs. It is built for AI artists, workflow developers and production teams who would otherwise use self-hosted RunPod or a local desktop install. It does four things:

- Browser canvas: runs standard and custom node graphs interactively.
- Custom builds: package proprietary nodes, model weights and custom LoRAs.
- Team workspace: shared, so nobody configures local dependencies.
- REST API: calls workflows from automated generation pipelines.

GPUs run from RTX PRO 6000 with 96 GB VRAM up to NVIDIA B200 with 180 GB VRAM. Billing is per second while a worker is active, and persistent storage is billed per gigabyte monthly. Each plan caps concurrent workers. It fits pipelines that outgrow local consumer VRAM, and it stays compatible with open-source ComfyUI.

## Development line

- **2026-03-03 — Comfy Cloud introduced a free tier.** On 2026-03-03 Comfy Cloud announced a free tier. It widened access to the cloud offering. The tier's features, eligibility and limits are not established.
- **2026-11-19 — Comfy adds custom workflow support to its cloud platform.** Comfy added custom workflows to its cloud service. Users package a local build with custom nodes and LoRAs, share it with a team through the browser, and reach it via API. Billing is per second, from $1.75 to $11.23 per hour depending on GPU. Storage costs $0.20 per GB per month. The feature starts at the Standard tier, and the Team tier allows up to 20 concurrent tasks.
- **2026-11-19 — Comfy adds custom workflow support to its cloud platform.** Comfy announced that its cloud now supports custom workflows. Users package a local build with custom nodes and LoRAs, share it with a team through the browser, and call it via API. Builds run on hardware from RTX PRO 6000 (96 GB VRAM) to B200 (180 GB VRAM). Billing is per second, from $1.75 to $11.23 per hour while workers are active, with network storage at $0.20/GB per month. The feature is on paid plans from Standard up. Standard and Creator are limited to 2 parallel jobs per build, and Team allows up to 20.
- **2026-11-19 — more detail from the same day.**
  - The [release post](https://blog.comfy.org/p/your-custom-comfyui-is-now-in-comfy?r=7xlbaw) lists the GPU fleet, from RTX PRO 6000 (96 GB VRAM) to NVIDIA B200 (180 GB VRAM). It also says custom node packages and Python requirements are parsed automatically. (2026-11-19)
  - The [launch post](https://x.com/ComfyUI/status/2123101758885085511) confirms the browser workflow canvas and team-wide workspace sync for shared environments. It also confirms REST API execution alongside interactive UI sessions. (2026-11-19)

## What changed

Comfy Cloud started with pre-curated default nodes and standard model checkpoints only. Graphs that depended on third-party custom nodes failed in the cloud sandbox, so workflows were hard to move over. Custom builds fixed that: users can import dependency snapshots from a local desktop install. The cloud now runs custom Python dependencies, private nodes and fine-tuned LoRAs, and it offers multi-GPU hardware tiers.

## How to use this

1. Prepare a local ComfyUI workflow or desktop snapshot with the custom nodes, LoRA weights and dependencies it needs.
  — [release post](https://blog.comfy.org/p/your-custom-comfyui-is-now-in-comfy?r=7xlbaw)
2. Upload the custom build configuration under a Standard, Creator or Team account. The dependencies are packaged into a persistent cloud environment.
  — [release post](https://blog.comfy.org/p/your-custom-comfyui-is-now-in-comfy?r=7xlbaw)
3. Pick the GPU, from RTX PRO 6000 (96 GB VRAM) to NVIDIA B200 (180 GB VRAM), by model size and VRAM need.
  — [release post](https://blog.comfy.org/p/your-custom-comfyui-is-now-in-comfy?r=7xlbaw)
4. Run generation in the browser canvas, or wire the deployed workflow into an application through the Comfy Cloud REST API.
  — [launch post](https://x.com/ComfyUI/status/2123101758885085511)

## Best practices

- Check that every custom node and Python dependency resolves cleanly in a local desktop snapshot before packaging a cloud build.
  — [release post](https://blog.comfy.org/p/your-custom-comfyui-is-now-in-comfy?r=7xlbaw)
- Match the GPU to the workflow. Use RTX PRO 6000 for standard high-resolution pipelines and keep B200 for extreme memory loads, so per-second cost stays down.
  — [release post](https://blog.comfy.org/p/your-custom-comfyui-is-now-in-comfy?r=7xlbaw)
- Watch persistent network storage, so monthly data charges do not creep up while the team shares builds.
  — [release post](https://blog.comfy.org/p/your-custom-comfyui-is-now-in-comfy?r=7xlbaw)

## Superseded by this

- Comfy Cloud only supports official pre-installed nodes and cannot run workflows that need custom third-party nodes or private LoRAs.
  — [release post](https://blog.comfy.org/p/your-custom-comfyui-is-now-in-comfy?r=7xlbaw)

## Still unknown

- Community reactions on Reddit and forums are left out, because no discussion links could be verified.
- API throughput limits and network ingress and egress throttling are not specified, beyond the per-build concurrency limits.

## Sources

| source | title | read |
|---|---|---|
| https://blog.comfy.org/p/your-custom-comfyui-is-now-in-comfy?r=7xlbaw | Your custom ComfyUI is now in Comfy | 2026-11-20 |
| https://x.com/ComfyUI/status/2123101758885085511 | ComfyUI on X: Custom Workflows and Builds in Comfy Cloud | 2026-11-20 |

## Agent brief {#agent-brief}

- **Subject:** project:comfy, thread cloud-access, 3 dated events 2026-03-03 → 2026-11-19.
- **Practical note:** see the usage and practice sections above, including their limits.
- **Confidence:** high. The dated supersedes above decide what is obsolete.
