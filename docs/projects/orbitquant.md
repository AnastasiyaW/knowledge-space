---
title: OrbitQuant
category: projects

tags: [orbitquant, orbitquant-development, project]
aliases: ["OrbitQuant"]
---

# OrbitQuant

**Development line:** `project:orbitquant` · thread `orbitquant-development`  
**Last event:** - · 0 dated since - · **Researched:** 2026-09-05 · confidence: high

## What it is

OrbitQuant is a Python library and post-training quantization method for image and video diffusion transformers.

- RPBH rotation.
- Shared Lloyd–Max codebooks.
- W2A4–W4A6 recipes.
- Transformers, Diffusers, and PyTorch integrations.
- Packed CUDA, Triton, and Metal execution.

Module coverage does not prove preserved quality on unknown architectures, so we measure output before publishing an artifact. This is a practical path to data-free low-bit inference, but not a universal replacement for model quality checks.

## Development line

- The dated line is not written up yet; what is known stands in the sections below.

## What changed

- 2026-07-07 — Published the OrbitQuant method page for calibration-free weight-and-activation quantization of image and video diffusion transformers.
- 2026-07-09 — PyPI released the initial OrbitQuant 0.1.0–0.1.6 package series.
- 2026-07-10 — Released versions 0.2.0–0.3.1.
- 2026-07-11 — Released version 0.4.0.
- 2026-07-12 — Released version 0.5.0.
- 2026-07-14 — Released versions 0.6.0–0.9.0.
- 2026-08-04 — Published version 0.9.2 as the current release in the verified registry.

## How to use this

As of 2026-07-07, treat OrbitQuant as an unresearched project reference. Verify its purpose, capabilities, and status before using it in practice.

1. Install the Hugging Face integration: `pip install "orbitquant[hf]"`.
  — <https://github.com/iamwavecut/OrbitQuant>
2. Load the model and inspect machine-readable coverage via `inspect_linear_module_policy()` before conversion; check skipped and unsupported modules separately.
  — <https://github.com/iamwavecut/OrbitQuant>
3. For Transformers, pass `OrbitQuantConfig(target_policy="auto")` to `from_pretrained()`, then save the packed artifact with `save_pretrained()`.
  — <https://github.com/iamwavecut/OrbitQuant>
4. For Diffusers, create `build_diffusers_pipeline_quantization_config(...)`, quantize the `transformer` component, and load the pipeline in BF16.
  — <https://github.com/iamwavecut/OrbitQuant>
5. In ComfyUI, connect the matching OrbitQuant loader to the source Diffusers pipeline, set local `artifact_path`, and route the returned pipeline downstream in the graph.
  — <https://pypi.org/project/comfyui-orbitquant/>

## Best practices

- Do not update Triton separately from PyTorch: the package uses Triton from PyTorch Linux wheels as a CUDA fallback.
  — <https://github.com/iamwavecut/OrbitQuant>
- For unknown architectures, check policy coverage and measure generation quality first; automatic module discovery does not guarantee output quality.
  — <https://github.com/iamwavecut/OrbitQuant>
- Use `auto_fused` for packed runtime, and keep `dequant_bf16` strictly as an explicit compatibility and debug path.
  — <https://pypi.org/project/comfyui-orbitquant/>
- Check the manifest, checksums, source metadata, bit settings, and target policy before loading a ComfyUI artifact.
  — <https://pypi.org/project/comfyui-orbitquant/>

## Superseded by this

- 2026-08-04 — OrbitQuant versions before 0.9.2 are not the current release in verified PyPI release history.
- 2026-07-09 — Later releases replaced the early 0.1.0–0.1.6 series; check PyPI for the active version before new installs.

## Still unknown

- The method page and paper describe research OrbitQuant, while the PyPI and GitHub code is presented as a clean-room implementation. We do not attribute practical interfaces or later release notes to the original 2026-07-07 publication.
- No primary dated changelog explains substantive differences across package versions 0.1.0–0.9.2; release dates and version numbers are confirmed, but not the full scope of changes.

## Sources

| source | title | read |
|---|---|---|
| https://saurabhcantina.github.io/orbitquant/ | OrbitQuant: Data-Agnostic Quantization for Image and Video Diffusion Transformers | 2026-09-05 |
| https://arxiv.org/abs/2607.02461 | OrbitQuant: Data-Agnostic Quantization for Image and Video Diffusion Transformers | 2026-09-05 |
| https://github.com/iamwavecut/OrbitQuant | iamwavecut/OrbitQuant | 2026-09-05 |
| https://pypi.org/project/orbitquant/ | orbitquant · PyPI | 2026-09-05 |
| https://pypi.org/project/comfyui-orbitquant/ | comfyui-orbitquant · PyPI | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:orbitquant`, thread `orbitquant-development`, 0 dated events - → -.
- **Practical note:** As of 2026-07-07, treat OrbitQuant as an unresearched project reference and verify its purpose, capabilities, and status before using it in practice.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
