---
title: "Rtx 30 Bf16 Unlock: rtx-30-bf16-unlock-gpu-selector-kernel-module — Rtx 30 Bf16 Unlock Gpu Selector Kernel Module"
category: "projects"
date: 2026-10-23
tags: ["project", "rtx-30-bf16-unlock", "rtx-30-bf16-unlock-gpu-selector-kernel-module"]
aliases: ["Rtx 30 Bf16 Unlock: rtx-30-bf16-unlock-gpu-selector-kernel-module"]
---

# Rtx 30 Bf16 Unlock: rtx-30-bf16-unlock-gpu-selector-kernel-module — Rtx 30 Bf16 Unlock Gpu Selector Kernel Module

**Development line:** project:rtx-30-bf16-unlock · thread rtx-30-bf16-unlock-gpu-selector-kernel-module  
**Last event:** 2026-10-23 · 1 dated since 2026-10-23 · **Researched:** 2026-11-28 · confidence: low

## What it is

A GPL-2.0 Linux kernel module that sets the speed selectors on GA102 and GA104 \(RTX 3000 series\) GPUs before the NVIDIA driver loads. The method grew out of unlockers for CMP cards. The report is that BF16 on these chips was held back by speed selectors, not by the hardware. Packages exist for Arch, Debian and Fedora, and a separate repository covers Windows.

## Development line

- **2026-10-23 — BF16 throughput unlock method released for GA102/GA104 RTX 30-series GPUs.** A kernel-module method was published that enables BF16, FP16 and TF32 throughput on GA102 and GA104 \(RTX 3000 series\) cards by activating speed selectors before the NVIDIA driver loads. Reported results for an RTX 3090 Ti in an 8192-cube matrix multiply: BF16 rises from 87.5 to 157.4 TFLOPS, FP16 from 87.5 to 118.4, and TF32 from 42.6 to 82.6. The GPL-2.0 kernel code has packages for Arch, Debian and Fedora, with a separate Windows repository; the post warns of firmware, stability and warranty risks.
  - A thread on r/comfyui, titled "It turns out RTX 3000 series can run bf16 almost..." \(title truncated in the URL\), shows the finding was also being discussed in the ComfyUI community. The page content was not available, so no further detail is added. (undated) — <https://www.reddit.com/r/comfyui/comments/1xcvl1o/it_turns_out_rtx_3000_series_can_run_bf16_almost>

## What changed

On 2026-10-23 the method was published with reported results for an RTX 3090 Ti in an 8192-cube matrix multiply. BF16 rises from 87.5 to 157.4 TFLOPS, FP16 from 87.5 to 118.4, and TF32 from 42.6 to 82.6. The author warns of nonstandard firmware, possible instability and loss of warranty.

## How to use this

No verified usage steps yet - see the development line and the sources.

## Best practices

- Before applying the unlock, weigh the stated risks: it needs nonstandard firmware, can cause instability, and can void the warranty. It works only on GA102 and GA104 cards, so confirm the GPU model first.
  — <https://www.reddit.com/r/comfyui/comments/1xcvl1o/it_turns_out_rtx_3000_series_can_run_bf16_almost>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The linked page's text was not available, so its details are unverified beyond its title.
- The benchmark numbers come from a single reported RTX 3090 Ti test and have not been independently reproduced.
- Exact installation steps and the long-term stability of the unlock are not documented here.
- Whether the unlock affects real workloads such as ComfyUI image generation is unknown.

## Sources

| source | title | read |
|---|---|---|
| https://www.reddit.com/r/comfyui/comments/1xcvl1o/it_turns_out_rtx_3000_series_can_run_bf16_almost | Reddit r/comfyui: It turns out RTX 3000 series can run bf16 almost... | 2026-10-23 |

## Agent brief {#agent-brief}

- **Subject:** project:rtx-30-bf16-unlock, thread rtx-30-bf16-unlock-gpu-selector-kernel-module, 1 dated events 2026-10-23 → 2026-10-23.
- **Practical note:** See the sourced usage and practice sections above, including their limits.
- **Confidence:** low. Dated supersedes above are the authority for what is obsolete.
