---
title: ComfyUI
category: projects
date: 2026-09-03
tags: [comfy-cloud-pricing, comfyui, comfyui-development, comfyui_core_updates, comfyui_desktop, ecosystem_grants, product_updates, project]
aliases: ["Comfy Cloud", "ComfyUI"]
---

# ComfyUI

**Development line:** `project:comfyui` · thread `comfyui-development`  
**Last event:** 2026-09-03 · 28 dated since 2023-11-24 · **Researched:** 2026-09-05 · confidence: medium

## What it is

ComfyUI-H3VAE_TRT is a third-party ComfyUI extension by lihaoyun6. It compiles MiniMax-H3 VAE ONNX models into TensorRT engines and loads them as a VAE. This is a custom-node integration, not a release of the MiniMax-H3 model or a core ComfyUI update.

ComfyUI itself is a node-graph interface and generation engine for images, video, 3D and audio. It runs locally (Desktop on Windows or macOS ARM, portable on Windows, or manual install) or as the managed Comfy Cloud. Cloud runs on RTX 6000 Pro with 96 GB VRAM. On the pricing page checked 2026-09-04, the Standard plan is $20 per month with 4200 credits and a 30-minute limit per run. Partner Nodes call paid closed-API models, App Mode hides a graph behind an input form, and Comfy MCP lets agents build and run workflows.

## Development line

- **2023-11-24 — ComfyUI Publishes Stable Video Diffusion Workflows.** On 2023-11-24, ComfyUI published first-party Stable Video Diffusion example workflows for image-to-video generation. The examples documented model placement and controls for frame count, motion, frame rate, and classifier-free guidance.
- **2024-06-12 — ComfyUI Core Adds SD3 Support.** On 2024-06-12, ComfyUI added SD3 support to its core engine in commit 8c4a9be. The change established native engine support for building SD3 workflows.
- **2024-09-16 — ComfyUI Adds SD3 and Flux Inpainting ControlNet Support.** On 2024-09-16, ComfyUI added support for AliMama ControlNet models for SD3 and Flux inpainting in commit f48e390. The change expanded structurally conditioned inpainting workflows for those model families.
- **2024-10-21 — ComfyUI V1 Introduces a New Interface and Desktop Beta.** On 2024-10-21, ComfyUI introduced its V1 interface and opened closed-beta Desktop packaging. The release added a bundled Manager, tabs, settings, model and workflow browsers, and model-download assistance. The original interface moved to a maintenance path.
- **2024-12-06 — ComfyUI Responds to the Ultralytics Package Compromise.** On 2024-12-06, ComfyUI documented its response to malicious Ultralytics 8.3.41 and 8.3.42 packages encountered through some custom-node dependency chains. The project distinguished the compromised dependency from ComfyUI core and added Manager warnings and version pinning.
- **2025-07-28 — ComfyUI Adds Day-Zero Wan 2.2 Support.** On 2025-07-28, ComfyUI added native day-zero support for Wan 2.2. The release provided official mixture-of-experts text-to-video and image-to-video workflows and packaged model files.
- **2025-08-13 — ComfyUI Expands Wan 2.2 Fun InP and Control Workflows.** On 2025-08-13, ComfyUI added Wan 2.2 Fun InP, Control, and LightX2V support. The workflows enabled first-and-last-frame generation, structural controls, and faster four-step generation with LoRA acceleration.
- **2025-08-26 — ComfyUI Adds Native Qwen-Image DiffSynth ControlNet Support.** On 2025-08-26, ComfyUI added native Qwen-Image DiffSynth ControlNet support. The update expanded controllable image generation and documented optional cache-based workflow acceleration. The release also added Union LoRA support, EasyCache and Blackwell optimizations.
- **2025-08-27 — ComfyUI Adds Hosted Gemini and Local Qwen-Image Control Paths.** On 2025-08-27, ComfyUI added two distinct execution paths: Google Gemini 2.5 Flash Image through credit-billed Partner Nodes and local InstantX Qwen-Image Unified ControlNet workflows. The local workflows supported canny, depth, pose, and soft-edge controls.
- **2025-08-28 — Second Comfy Challenge Expands the Community Workflow Program.** On 2025-08-28, ComfyUI expanded its community showcase and workflow-learning program through the second Comfy Challenge. This was an ecosystem and education milestone rather than a core runtime release.
- **2025-09-24 — ComfyUI Adds Wan 2.2 Animate and Qwen Image Editing Workflows.** On 2025-09-24, ComfyUI added native workflows for Wan 2.2 Animate and Qwen-Image-Edit-2509. They supported performer-driven character animation and replacement as well as multi-image editing.
- **2025-10-07 — ComfyUI 0.3.63 Makes Subgraphs Publishable.** On 2025-10-07, ComfyUI 0.3.63 made subgraphs publishable as reusable blueprint nodes. The release also redesigned selection tooling for graph editing.
- **2025-10-09 — ComfyUI Adds Sora 2 Partner Nodes.** On 2025-10-09, ComfyUI made Sora 2 and Sora 2 Pro available through paid Partner Nodes. The integration supported text-to-video and image-to-video generation with sound.
- **2025-10-22 — ComfyUI 0.3.66 Improves Subgraph and Template Tooling.** On 2025-10-22, ComfyUI 0.3.66 added a parameter panel for subgraphs. The release also redesigned workflow-template discovery and filtering.
- **2025-11-04 — Comfy Cloud Leaves the Waitlist for Public Beta.** On 2025-11-04, Comfy Cloud moved from waitlist to public beta. The date was found on 2026-09-04.
- **2025-11-26 — Comfy Cloud Expands Infrastructure and Feature Allowances.** On 2025-11-26, Comfy Cloud announced a move to RTX 6000 Pro infrastructure, replacing the A100 base machine, and support for using personal LoRAs. It also described longer Pro runs and unified credits across Cloud GPU execution and Partner Nodes.
- **2025-12-30 — ComfyUI Begins Moving Its Canonical Repository to Comfy-Org.** On 2025-12-30, ComfyUI began moving its canonical GitHub repository from comfyanonymous/ComfyUI to Comfy-Org/ComfyUI. The move was scheduled for 2026-01-06. GitHub redirects were retained, and users were advised to update their Git remotes.
- **2026-01-27 — ComfyUI Adds Day-Zero Z-Image Support.** On 2026-01-27, ComfyUI added day-zero support for the non-distilled Z-Image model. The release included an official workflow and model-specific sampling guidance, with 30–50 recommended steps and CFG 3–5.
- **2026-02-05 — ComfyUI Ecosystem Announces an Open-Model Grant Initiative.** On 2026-02-05, the ComfyUI ecosystem announced an open-model grant initiative described as a $1 million program alongside the Anima launch. The initiative was presented as funding for open model development.
- **2026-03-02 — Comfy Cloud Announces a Free Tier.** On 2026-03-02, Comfy Cloud announced a free tier of 400 credits per month. The pricing page checked on 2026-09-04 shows five free runs without a card instead, so the 400-credit figure is superseded.
- **2026-03-04 — Comfy Cloud Leaves Beta.** On 2026-03-04, Comfy Cloud left beta. The date was found on 2026-09-04.
- **2026-03-10 — ComfyUI Introduces App Mode, App Builder and ComfyHub.** On 2026-03-10, ComfyUI added App Mode, which hides a graph behind an input form, App Builder for defining inputs and outputs, and ComfyHub for sharing an app by link. The date was found on 2026-09-04.
- **2026-03-26 — ComfyUI Introduces Stable Dynamic VRAM Management.** On 2026-03-26, ComfyUI documented Dynamic VRAM as a stable mechanism for reducing memory pressure and out-of-memory failures on supported Nvidia systems on Windows and Linux. It lowers system RAM use by unloading weights more economically. Its guidance emphasized measuring total workflow time instead of isolated iteration speed.
- **2026-07-23 — Comfy for Teams Launches.** On 2026-07-23, Comfy for Teams added a shared workspace, a pooled credit balance, one billing account and member administration. The date was found on 2026-09-04.
- **2026-08-18 — Comfy MCP Opens for Local and Cloud.** On 2026-08-18, Comfy MCP became available for both Local and Cloud. Agents can read the environment, assemble and run workflows, and install models and nodes. The date was found on 2026-09-04.
- **2026-08-26 — ComfyUI v0.34.0 Adds Video Formats and Dynamic VRAM for ROCm.** On 2026-08-26, ComfyUI v0.34.0 added new video save formats and HDR output, expanded model support, and enabled Dynamic VRAM by default for ROCm 7.14 and later. The research of 2026-09-04 records it as the last verified stable release; see Still unknown for a conflicting version.
- **2026-09-02 — Launch of ComfyUI H3VAE TensorRT integration.** The maintainer announced a TensorRT MiniMax-H3 VAE version for ComfyUI that can increase speed up to 1.7x.
  - The extension provides separate Compiler and Loader nodes. The checked source revision is 1b72e7439e1fc306b9dfbfd3d485866553b5960e, committed later on September 2; the original announcement did not identify a release tag. (2026-09-02) — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>
- **2026-09-03 — ComfyUI update.** An independent tester reported 48.8s versus 36.6s for the same 2.0MP, six-second VAE decode on an RTX 4090 with 24GB, ComfyUI 0.34.2 and TensorRT 10.12. At 768p the result was 19.6s versus 18.0s. This is one workload-specific decode test, not an overall generation-speed claim.

## What changed

The maintainer reports up to 1.7x faster MiniMax-H3 VAE processing in a third-party ComfyUI integration. The claim concerns VAE encode/decode, not end-to-end video generation. The source announcement date is retained separately from the subsequent research.

## How to use this

1. Clone the extension into ComfyUI/custom_nodes and install its requirements using the Python environment that runs ComfyUI.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>
2. Download the encoder and decoder ONNX files from the maintainer's linked model repository, including accompanying .data files when supplied. Put them under ComfyUI/models/vae.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>
3. Build the engines with MiniMax-H3 TRT VAE Compiler, then load them with MiniMax-H3 TRT VAE Loader.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>

### Core ComfyUI platform

1. Choose the environment: Local for your own GPU, offline work and full freedom to add extensions; Comfy Cloud for managed GPU and a ready model set.
  — <https://docs.comfy.org/get_started/cloud>
2. For Local, use a supported install: Desktop on Windows or macOS ARM, portable on Windows, or manual install for other supported systems and GPUs.
  — <https://docs.comfy.org/installation/system_requirements>
3. Open a built-in official template for the task; ComfyUI checks for missing models and dependencies.
  — <https://docs.comfy.org/interface/features/template>
4. Install third-party nodes through Manager only from a trusted source, restart ComfyUI and check the load log.
  — <https://docs.comfy.org/installation/install_custom_node>

## Best practices

- Pin a working ComfyUI version and update through stable releases; use nightly only for a measured need for a new feature or model.
  — <https://docs.comfy.org/installation/update_comfyui>
- Start from an official native template and keep the workflow JSON or PNG with its metadata; this reduces path, model and graph-structure errors.
  — <https://docs.comfy.org/interface/features/template>
- Treat a custom node as third-party executable code: check author, purpose and dependencies, and avoid obscure ZIP builds.
  — <https://docs.comfy.org/installation/install_custom_node>
- Pin the semantic version of a registry node: the version is recorded in the workflow, and a published Registry release stays unchanged.
  — <https://docs.comfy.org/registry/overview>
- Before a mass Update All in the legacy Manager, save a snapshot; after restoring, restart and verify the graph.
  — <https://docs.comfy.org/manager/legacy-ui>
- In Desktop, do not edit the bundled resource/ComfyUI folder, because an update may recreate it; keep models and user data in external folders.
  — <https://docs.comfy.org/installation/desktop/windows>
- Before a long Cloud queue, check the run limit and balance: monthly included credits reset, and Partner Nodes draw from the same pool.
  — <https://comfy.org/pricing>
- Do not read high VRAM use under Dynamic VRAM as a leak by itself; compare OOM rate, system RAM use and load time before disabling the mode.
  — <https://blog.comfy.org/p/dynamic-vram-in-comfyui-saving-local>
- For a recipient who needs only parameters and output, publish App Mode rather than the full editable graph.
  — <https://docs.comfy.org/interface/app-mode>
- For the H3VAE extension: measure VAE decode separately from total generation time, and compare at your target resolution. The independent test found a much smaller gain at 768p than at 2.0MP.
  — <https://note.com/seal309midorin/n/nb75b14bbab4e>
- Below 12GB VRAM, the maintainer suggests the w4a16_awq decoder. Treat this as an author recommendation, not a guarantee that the complete video workflow will fit your GPU.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README_zh.md>

## Superseded by this

- For the H3VAE extension: nothing marked obsolete yet.
- 2024-10-21 — the closed-beta Desktop and the Cloud waitlist are obsolete: Cloud reached public beta on 2025-11-04 and left beta on 2026-03-04.
- 2024-10-21 — the claim of a ready Desktop for Windows, macOS and Linux no longer matches the current matrix: ready builds are documented for Windows and macOS ARM, and Linux needs manual or self-hosted install.
- 2025-11-26 — the A100 base Cloud machine was replaced by RTX 6000 Pro Blackwell with 96 GB VRAM.
- Before 2026-01-06 — the git remote github.com/comfyanonymous/ComfyUI is superseded by github.com/Comfy-Org/ComfyUI; old links still redirect.
- 2026-03-02 — the promised 400 free monthly credits conflict with the pricing page checked on 2026-09-04, which shows five free runs without a card. Use the current pricing page for purchase and planning.
- 2026-03-25 — describing Dynamic VRAM as NVIDIA-only is incomplete after v0.34.0, which enabled it by default for ROCm 7.14 and later.

## Still unknown

- The original announcement does not identify an immutable release tag or the installed version.
- The maintainer's maximum 1.7x claim is not an independent benchmark of complete video generation.
- A Chinese community guide was located, but its page could not be retrieved in the root verification pass. Chinese coverage here is first-party documentation; no independent Chinese benchmark is claimed.
- No workflow was executed on our GPU for this article. Hardware measurements are attributed to their authors.
- The name ComfyUI covers different surfaces: open-source core, Desktop, Comfy Cloud, Partner Nodes, App Mode and ComfyHub, MCP and a grant program. They share one ecosystem but not one install, billing or trust model.
- Events dated 2025-10-24, 2025-12-26, 2026-02-21 and the 2026-05-12 price change have no readable primary source, so their content is not recorded.
- The AI grant page (comfy.org/ai-grant) gave no readable current terms. The 2026-02-05 launch date, amount and application status are not confirmed.
- Free-tier sources conflict: the 2026-03-02 announcement offered 400 credits per month, while the pricing page on 2026-09-04 shows five free runs. The pricing page was taken as current; a new account was not tested.
- Version conflict: the research of 2026-09-04 records v0.34.0 as the last verified stable release, while the 2026-09-03 tester report above used ComfyUI 0.34.2. This is not reconciled with a release page.
- Three X/Twitter posts cited by the research could not be read; no product change is attributed to them.
- Installation, Cloud billing, Partner Nodes and MCP were not run in a real account; the platform facts come from documentation and public releases.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md | Maintainer README, English, pinned source revision | 2026-09-05 |
| https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README_zh.md | Maintainer README, Simplified Chinese, translated into English synthesis | 2026-09-05 |
| https://note.com/seal309midorin/n/nb75b14bbab4e | Independent Japanese RTX 4090 VAE decode test, public excerpt | 2026-09-05 |
| https://blog.comfy.org/p/comfyui-v1-release | ComfyUI V1 Release (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://blog.comfy.org/p/comfyui-now-supports-qwen-image-controlnet | ComfyUI Now Supports Qwen Image ControlNet (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://blog.comfy.org/p/comfy-cloud-is-now-in-public-beta | Comfy Cloud Is Now in Public Beta (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://blog.comfy.org/p/comfyui-repo-will-moved-to-comfy | ComfyUI Repo Will Be Moved to Comfy Organization (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://blog.comfy.org/p/z-image-day-0-support-in-comfyui | Z-Image Day 0 Support in ComfyUI (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://blog.comfy.org/p/free-tier-arrives-in-comfy-cloud | Free Tier Arrives in Comfy Cloud (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://blog.comfy.org/p/comfy-cloud-is-out-of-beta-and-its | Comfy Cloud Is Out of Beta (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://blog.comfy.org/p/from-workflow-to-app-introducing | From Workflow to App: Introducing App Mode, App Builder, and ComfyHub (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://blog.comfy.org/p/dynamic-vram-in-comfyui-saving-local | Dynamic VRAM in ComfyUI: Saving Local System RAM (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://blog.comfy.org/p/comfy-for-teams-is-here | Comfy for Teams Is Here (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://blog.comfy.org/p/open-sourcing-comfy-mcp-on-local | Open-Sourcing Comfy MCP on Local and Cloud (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.34.0 | Release v0.34.0 · Comfy-Org/ComfyUI (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://comfy.org/pricing | Pricing — Comfy Cloud (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://docs.comfy.org/get_started/cloud | Comfy Cloud — Official ComfyUI Cloud Platform (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://docs.comfy.org/installation/system_requirements | ComfyUI System Requirements (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://docs.comfy.org/interface/features/template | Templates — ComfyUI Built-in Workflow Templates (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://docs.comfy.org/installation/install_custom_node | How to Install Custom Nodes in ComfyUI (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://docs.comfy.org/installation/update_comfyui | How to Update ComfyUI (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://docs.comfy.org/registry/overview | ComfyUI Registry Overview (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://docs.comfy.org/manager/legacy-ui | Managing Custom Nodes with the Legacy UI (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://docs.comfy.org/installation/desktop/windows | Windows Desktop — Local Self-Hosted (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://docs.comfy.org/interface/app-mode | ComfyUI App Mode Guide (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |
| https://docs.comfy.org/tutorials/partner-nodes/overview | Partner Nodes Overview (carried from PR #108) | 2026-09-04 (PR #108; not re-fetched) |

## Agent brief {#agent-brief}

- **Subject:** `project:comfyui`, thread `comfyui-development`, 28 dated events 2023-11-24 → 2026-09-03.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.

<!-- live-update:542d36681e0384ef91df7cb913a469eddd1bd5adb679d7dcb9da8c869c400e19 -->
## 2026-10-23 — ComfyUI v0.42.5 maintenance patch published

Comfy-Org published ComfyUI v0.42.5 on GitHub. It is a maintenance release in the v0.42 track, with routine core fixes and node upkeep.

### Usage and practices

- Install: take the official release build, or clone the repository into your local Python environment. [Source](https://github.com/Comfy-Org/ComfyUI)
- Models: put checkpoints, text encoders and VAE weights into their matching subfolders under the models folder. [Source](https://github.com/Comfy-Org/ComfyUI)
- Launch: start the backend server with the main script, and the web canvas opens. [Source](https://github.com/Comfy-Org/ComfyUI)
- First graph: connect a model loader, prompt conditioning, latent sampling and VAE decode as a directed acyclic graph, then queue the prompt. [Source](https://github.com/Comfy-Org/ComfyUI)
- Updates: follow the point releases through the tagged release stream on GitHub. [Source](https://github.com/Comfy-Org/ComfyUI/releases)
- Large graphs: put related blocks into labelled group boxes and use reroute nodes so the connections do not tangle. [Source](https://github.com/Comfy-Org/ComfyUI)
- Memory: reuse one loaded model and VAE across downstream conditioning branches instead of adding duplicate loaders to GPU memory. [Source](https://github.com/Comfy-Org/ComfyUI)
- Custom nodes: check that a minimal baseline graph runs before adding third-party extensions. [Source](https://github.com/Comfy-Org/ComfyUI/releases)
- Production: read the release tags and changelogs before updating, so a schema change or a custom node does not break. [Source](https://github.com/Comfy-Org/ComfyUI/releases)

### Additional evidence

- 2026-10-23: The official v0.42.5 release brings incremental maintenance, bug fixes and stability improvements to core node execution and dependency management within the v0.42 series. [Source](https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.42.5)

### Superseded guidance (retained for history)

- 2026-10-23: Running one monolithic all-in-one local install, with no version-tagged core releases and no package separation. [Source](https://github.com/Comfy-Org/ComfyUI/releases)

### Limits and open questions

- We did not find the commit-level changes or the individual pull request numbers for v0.42.5.
- Community discussion of how v0.42.5 performs could not be verified against a direct source.
- In Simplified Chinese we found only secondary tutorials, not direct technical release pages, so that side is still a gap.


<!-- Retained base: 11c29423c88576f7a36f6181d0b1721f3eef80c5; article blob: e8f40d3a16e3cc034944e038fe697b76728af963 -->
