---
title: AMD — AMD AI Compute Platform
category: organizations
tags: [amd, amd-ai-compute-platform, amd_mi300x, instinct-mi300x, organization]
aliases: ["AMD"]
---

# AMD — AMD AI Compute Platform

**Development line:** `organization:amd` · thread `amd-ai-compute-platform`  
**Events:** 2 dated, 2023-06-14 → 2025-08-13 · **Researched:** 2026-09-03 · confidence: medium

## What it is

AMD — a compute platform for teams running AI, HPC, PCs and graphics; its data-center route is Instinct hardware plus ROCm. — MI455X and Helios for large-scale inference, training and fine-tuning. — MI430X for scientific HPC and sovereign AI. — ROCm builds for PyTorch, TensorFlow, JAX, vLLM and related tooling. Limit: support is an exact hardware, OS, firmware, driver, ROCm and framework-version tuple; MI430X is expected in 2027 and Helios volume deployments in H2 2026. Verdict: use AMD where the complete configuration is listed in the current ROCm matrix, not merely because the GPU is AMD-branded.

## Development line

- **2023-06-14 — AMD expanded its data-center AI portfolio around Instinct MI300X.** On 2023-06-14, AMD’s linked materials documented an expansion of its data-center portfolio associated with the Instinct MI300 series and the MI300X thread. The accompanying PyTorch 2.0 link places the announcement in an AI software-ecosystem context. The supplied links alone do not establish detailed specifications, availability, or customer adoption.
- **2025-08-13 — AMD published a GPT-OSS-120B chatbot Space.** On 2025-08-13, the dated link pointed to an AMD-owned Hugging Face Space for a GPT-OSS-120B chatbot. This is a public-facing model-demo or deployment step in AMD’s AI platform presence. The supplied link does not establish the backend hardware, model provenance, current availability, or service guarantees.

## What changed

AMD, 2023-06-14 — detailed Instinct MI300X: CDNA 3, up to 192 GB HBM3, an eight-GPU platform, Q3 sampling, and PyTorch 2.0 day-zero support with ROCm 5.4.2. AMD, 2023-11-03 — released Adrenalin 23.11.1 for Windows Radeon systems, adding DirectML optimizations for Stable Diffusion, Lightroom, DaVinci Resolve and Procyon; this was a separate client-driver track, not an Instinct/ROCm server release. AMD, 2025-08-13 — the named `amd/gpt-oss-120b-chatbot` Space was a demo reference; its endpoint is now access-restricted, so it establishes no current serving stack or support contract. AMD, 2026-07-23 (found today) — launched the Instinct MI400 family: MI455X for frontier AI and AI factories, MI430X for sovereign AI and HPC, with ROCm as the common software route.

## How to use this

From 2023-06-14, practitioners should evaluate AMD’s Instinct MI300X and associated PyTorch ecosystem as an AI-compute platform option; from 2025-08-13, they can use AMD’s GPT-OSS-120B Space as a deployment/demo reference, while independently verifying current technical and service details.

1. Start in the selector and record the exact GPU, OS, kernel or firmware, driver, ROCm, Python and framework versions; proceed only with a listed compatible configuration.
  — <https://rocm.docs.amd.com/en/develop/compatibility/compatibility-matrix.html>
2. Install the AMD GPU driver and ROCm by the current supported method; the guide recommends package-manager installation on Linux and a tarball for portable Windows setups when unsure.
  — <https://rocm.docs.amd.com/en/develop/install/rocm.html>
3. Use the PyTorch selector for the exact hardware, OS and version, then choose the matching AMD container or pip installation path.
  — <https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html>
4. Validate the ROCm SDK after installation with `rocm-sdk targets` and `rocm-sdk test`.
  — <https://rocm.docs.amd.com/en/develop/install/rocm.html>
5. Validate the framework before a workload: `python -c "import torch; print(torch.cuda.is_available())"` should print `True` when PyTorch and ROCm detect the GPU.
  — <https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html>

## Best practices

- Do not mix firmware, driver, ROCm and framework versions from different release lines; ROCm requires the coordinated stack shown in its compatibility matrix.
  — <https://rocm.docs.amd.com/en/develop/compatibility/compatibility-matrix.html>
- Use the matching AMD ROCm PyTorch container or wheel rather than an arbitrary binary, then run the documented detection check before scheduling work.
  — <https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html>
- Treat MI455X/Helios and MI430X as separate availability tracks: verify the OEM deployment path, and do not plan production MI430X capacity before its stated 2027 availability.
  — <https://www.amd.com/en/products/accelerators/instinct/mi400.html>
- For Radeon laptops and all-in-ones, prefer the OEM-provided driver when system-specific features or support matter.
  — <https://www.amd.com/en/support/kb/release-notes/rn-rad-win-23-11-1>

## Superseded by this

- AMD, 2023-06-14: MI300X sampling-era specifications and ROCm 5.4.2/PyTorch 2.0 guidance are historical; current selection should use MI400, ROCm 10 and the live compatibility matrix.
- AMD, 2023-11-03: Adrenalin 23.11.1 is a historic Windows driver release, not current software-selection guidance; current ROCm installation documentation points to a later Adrenalin 26.8.1 release.
- AMD, 2025-08-13: a named gpt-oss chatbot demo is not current deployment guidance because no active support, hardware or serving contract could be verified.

## Still unknown

- The `amd/gpt-oss-120b-chatbot` endpoint returned HTTP 401 during review; its current availability, model revision, accelerator and service terms are unknown.
- The dated items span Instinct/ROCm data-center hardware, Radeon Windows drivers and a hosted model demo. They are not one technical release sequence; only the company identity is shared.
- Per-OEM MI400 availability, pricing and support lifecycle were not verified.

## Sources

| source | title | read |
|---|---|---|
| https://www.amd.com/en/newsroom/press-releases/2023-6-13-amd-expands-leadership-data-center-portfolio-with-.html | AMD Expands Leadership Data Center Portfolio with New EPYC CPUs and Shares Details on Next-Generation AMD Instinct Accelerator and Software Enablement for Generative AI | 2026-09-03 |
| https://www.amd.com/en/support/kb/release-notes/rn-rad-win-23-11-1 | AMD Software: Adrenalin Edition 23.11.1 Release Notes | 2026-09-03 |
| https://huggingface.co/spaces/amd/gpt-oss-120b-chatbot | amd/gpt-oss-120b-chatbot | 2026-09-03 |
| https://newsroom.amd.com/news/aai-2026-mi400-instinct-update/ | AAI 2026: AMD Launches AMD Instinct MI400 Series GPUs for Frontier AI, HPC | 2026-09-03 |
| https://www.amd.com/en/products/accelerators/instinct/mi400.html | AMD Instinct MI400 Series GPUs | 2026-09-03 |
| https://www.amd.com/zh-cn/newsroom/press-releases/aai-2026-mi400-instinct-update.html | AAI 2026：AMD推出面向前沿AI与HPC的AMD Instinct MI400系列GPU | 2026-09-03 |
| https://rocm.docs.amd.com/en/develop/install/rocm.html | Install AMD ROCm 10.0.0 | 2026-09-03 |
| https://rocm.docs.amd.com/en/develop/compatibility/compatibility-matrix.html | ROCm 10.0.0 compatibility matrix | 2026-09-03 |
| https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/frameworks/pytorch/install.html | Install PyTorch for ROCm | 2026-09-03 |

## Agent brief {#agent-brief}

- **Subject:** `organization:amd`, thread `amd-ai-compute-platform`, 2 dated events 2023-06-14 → 2025-08-13.
- **Practical note:** From 2023-06-14, practitioners should evaluate AMD’s Instinct MI300X and associated PyTorch ecosystem as an AI-compute platform option; from 2025-08-13, they can use AMD’s GPT-OSS-120B Space as a deployment/demo reference, while independently verifying current technical and service details.
- **Confidence:** medium. Dated supersedes above are the authority for what is obsolete.
