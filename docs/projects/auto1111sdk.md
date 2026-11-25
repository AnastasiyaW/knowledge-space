---
title: Auto1111SDK
category: projects
date: 2024-03-05
tags: [auto1111sdk, auto1111sdk-development, project]
aliases: ["Auto1111SDK"]
---

# Auto1111SDK

**Development line:** `project:auto1111sdk` · thread `auto1111sdk-development`  
**Last event:** 2024-03-05 · 2 dated since 2024-02-06 · **Researched:** 2026-09-04 · confidence: medium

## What it is

Auto1111SDK is a Python library for developers driving local Stable Diffusion workflows from code instead of the Automatic1111 WebUI.

- Text-to-image, image-to-image, inpainting, outpainting, and Stable Diffusion upscale.
- ESRGAN/Real-ESRGAN upscaling, CivitAI downloads, custom VAE/SDXL support, and a ControlNet interface.

## Development line

- **2024-02-06 — Auto1111SDK project repository and Colab notebook appeared.** The project used the personal `saketh12/Auto1111SDK` repository path and a Colab demo.
- **2024-03-05 — Auto1111SDK organization repository appeared with the Colab notebook.** On 2024-03-05, the repository moved under the Auto1111SDK GitHub organization alongside the linked Colab notebook. The change marks a public entry point, but the links do not show whether it was a repository migration, a release, or a repost.

## What changed

Auto1111SDK stopped development in early-2024 with no later PyPI release. On 2024-02-06, the project started under the personal `saketh12/Auto1111SDK` repository path with a Colab demo. On 2024-02-16, PyPI published 0.0.95, which remains the latest release in its history. On 2024-03-05, the repository path changed to `Auto1111SDK/Auto1111SDK` while retaining the same Colab file; this shows a publishing path change rather than new code. On 2026-09-04, the GitHub README still documents virtualenv-only installation, the old personal Git install path, and FP32-only ControlNet. The package is now a legacy dependency with unverified current-runtime compatibility.

## How to use this

From 2024-03-05, treat the Auto1111SDK organization repository as the historical project entry point and verify current setup separately.

1. Create a clean Python virtual environment; the project explicitly recommends a virtualenv and says Conda is unsupported.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
2. Install the reproducible last package release with `pip install auto1111sdk==0.0.95`, then verify the version and files against PyPI.
  — <https://pypi.org/project/auto1111sdk/>
3. Place a compatible local checkpoint or `.safetensors` file on disk, construct `StableDiffusionPipeline(path)`, and call `generate_txt2img` with a prompt, dimensions, and steps.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
4. Save the first generated image with `output[0].save(...)`; use this minimal flow as the environment smoke test before adding a larger workflow.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
5. For ControlNet, create `ControlNetModel` with the model name without its extension and an input image, pass it to the pipeline, and provision FP32 VRAM.
  — <https://github.com/Auto1111SDK/Auto1111SDK>

## Best practices

- Use an isolated virtual environment rather than Conda; this is the only environment support boundary stated upstream.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
- Pin Auto1111SDK, Python, PyTorch, CUDA, and model-weight versions in a lockfile or image: the latest published package is pre-alpha 0.0.95 from 2024-02-16.
  — <https://pypi.org/project/auto1111sdk/>
- Do not use the README’s unpinned `pip install git+https://github.com/saketh12/Auto1111SDK.git` for a reproducible workflow; use a reviewed immutable source revision if source installation is necessary.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
- Treat ControlNet as FP32-only and measure GPU memory before committing to it; do not assume the README’s planned FP16 support shipped.
  — <https://github.com/Auto1111SDK/Auto1111SDK>

## Superseded by this

- 2024-02-06 — the personal `saketh12/Auto1111SDK` link is superseded as the canonical reference by the organization path recorded on 2024-03-05; both resolve to the same named project today.
- 2024-02-16 — “install the latest” must not be read as current-generation diffusion support: it resolves to pre-alpha 0.0.95, released on 2024-02-16.
- 2024-03-05 — treating the Git-source install as evidence of newer ControlNet support is obsolete; the current README still documents ControlNet as FP32-only.

## Still unknown

- The Colab notebook at `https://colab.research.google.com/drive/1SekiJ-mdB2V8ogWbyRyF_yDnoMuDGWTl` could not be read without a valid Google session, so its current runtime, package pins, hardware, and execution state are unverified.
- The dated links establish a personal-to-organization GitHub path change on 2024-03-05, but do not establish whether it was a repository transfer, a mirror, or a code release; no release note or commit diff for 2024-03-05 was available.
- Current compatibility with 2026 Python, PyTorch, CUDA, and model formats is not established by the sources read.

## Sources

| source | title | read |
|---|---|---|
| https://github.com/Auto1111SDK/Auto1111SDK | Auto1111SDK/Auto1111SDK repository README | 2026-09-04 |
| https://pypi.org/project/auto1111sdk/ | auto1111sdk PyPI project and release history | 2026-09-04 |
| https://github.com/saketh12/Auto1111SDK | Auto1111SDK repository at the original personal path | 2026-09-04 |

## Agent brief {#agent-brief}

- **Subject:** `project:auto1111sdk`, thread `auto1111sdk-development`, 2 dated events 2024-02-06 → 2024-03-05.
- **Practical note:** From 2024-03-05, treat the Auto1111SDK organization repository as the recorded historical project entry point and validate current setup instructions separately.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.