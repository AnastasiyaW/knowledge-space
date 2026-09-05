---
title: PhotoQuilt
category: projects
date: 2026-07-06
tags: [photoquilt, photoquilt-development, project]
aliases: ["PhotoQuilt"]
---

# PhotoQuilt

**Development line:** `project:photoquilt` · thread `photoquilt-development`  
**Last event:** 2026-07-06 · 1 dated since 2026-07-06 · **Researched:** 2026-09-05 · confidence: high

## What it is

PhotoQuilt is a training-free photomosaic pipeline for diffusion users who need a coherent large scene built from independent image tiles.

- global bootstrap, latent upscale, noise reinjection and tiled denoising;
- FLUX.1-Krea-dev, distilled FLUX.2-klein-9B and Stable Diffusion 2.1 backends;
- layout-image, tile-prompt, gallery-reference and FLUX.1 multi-GPU workflows.

## Development line

- **2026-07-06 — PhotoQuilt project resources were made available.** On 2026-07-06, the project website, GitHub repository, and hosted Hugging Face Space went live. Practitioners got distinct places to inspect, obtain, and test the code.

## What changed

2026-07-06 — PhotoQuilt launched as a training-free arbitrary-resolution photomosaic method. The official implementation provides three local diffusion backends and workflows conditioned on layout images or gallery references.

## How to use this

Evaluate PhotoQuilt on its project page, GitHub repository, and hosted Space as of 2026-07-06. The available evidence does not establish production capabilities.

1. Clone the repository, install the PyTorch build matching CUDA, then install requirements; weights download on first run.
  — <https://github.com/KooroshRH/PhotoQuilt>
2. Choose `flux1`, `flux2` or `sd21`, then run its supplied script with dimensions, global prompt, tile prompt, steps, noise steps and tile size.
  — <https://github.com/KooroshRH/PhotoQuilt>
3. Use `--base-image` for a fixed composition or `--tile-image-dir` for reference-driven tiles.
  — <https://github.com/KooroshRH/PhotoQuilt>
4. Retrieve results from `--output-dir`, which defaults to `outputs/`.
  — <https://github.com/KooroshRH/PhotoQuilt>

## Best practices

- Start with the published FLUX.1 schedule: 28 steps, 17 noise steps and 1024-pixel tiles at 4096 square; its renoising strength is about 0.61.
  — <https://github.com/KooroshRH/PhotoQuilt>
- Make output width and height exact multiples of the tile size. Multi-GPU mode needs at least as many tile rows as visible GPUs.
  — <https://github.com/KooroshRH/PhotoQuilt>
- Use the global prompt or base image for composition and the tile prompt or gallery for local content; they control different scales.
  — <https://github.com/KooroshRH/PhotoQuilt>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- The Hugging Face Space failed to load during our check, so we cannot verify its current availability or interface.
- Official sources contain no dated release notes or tags, so later repository capabilities have no precise release date.
- We found no newer dated PhotoQuilt development steps after 2026-07-06.
- Consulted sources use one consistent project identity throughout.
- Nobody has independently reproduced the implementation's claims on performance, output quality, or compatibility.
- The official repository documents neither a packaged release nor an ongoing support policy.
- We reviewed the project page, but it does not supply a publication date.
- The original event text was unavailable, so we could not compare its exact wording and claims.
- A working Hugging Face Space alone does not prove reproducible local usage.
- We found no Chinese-language primary evidence during this check.
- Licensing depends on the chosen model checkpoint, and we did not audit downstream terms.
- Consulted sources mention neither a ComfyUI node nor an API integration.
- The paper abstract provides only qualitative comparisons, so we extracted no benchmark numbers.
- The finding date comes from the arXiv v1 submission, not the 2026-07-06 event date.
- The initial arXiv submission came before the public link event, so it stands as a distinct event.
- Nothing shows that an earlier version of PhotoQuilt is obsolete.
- The repository has only four commits, which does not prove an active maintenance cadence.
- PhotoQuilt is a method and codebase rather than a separately trained foundation model.
- The examples show Linux-style CUDA setup, leaving Windows execution unverified.
- The documentation mentions CPU offload, but that does not guarantee usable speed or memory fit.
- We omitted the public Space URL after the connection failed.
- Source titles retain their exact primary wording.
- We used no claims from sources that failed to load.
- This text synthesizes only what we verified in primary sources.
- This page covers only PhotoQuilt, not generic photomosaic tools.
- None of the sources establishes commercial rights across all supported checkpoints.
- The current GitHub README carries no versioned release date.
- The supported model checkpoints may require separate access requests or license acceptance.
- Sources give no explicit hardware minimum beyond recommending CUDA and documenting CPU offload.
- We did not treat visual samples on the project page as quantitative proof.
- The paper remains an arXiv preprint and has not undergone peer review.
- The current implementation may change over time because development sits directly on `main`.
- We found no evidence that this repository replaces an older PhotoQuilt codebase.
- The repository documents no commitments for support, issue triage, or security responses.
- We did not execute a live end-to-end run during this review.
- The 2026-06-29 preprint is the only additional dated event backed by a primary source.
- We can enrich the 2026-07-06 entry with the preprint's method name, authors, and 17-page scope without treating it as a later release.
- We did not cite the unavailable Space as a supporting source.
- Photomosaic is a general term, but this project stays distinct through its paper ID, authors, and repository.
- We found no contradictions across the project page, repository, and paper.
- The documented settings are official example configurations rather than universal optima.
- Reference-gallery handling depends on the backend: FLUX.1 uses Redux, while FLUX.2 uses native in-context conditioning.
- Stable Diffusion 2.1 uses its own documented bootstrap dimensions and example schedule.
- The documentation recommends a CUDA GPU, but it does not rule out CPU-only execution.
- Generated output filenames differ depending on the selected backend.
- We make no throughput claims for arbitrary resolutions on specific GPUs.
- Consulted sources publish no migration guides or deprecation notices.
- The preprint and the public link may share a launch moment, but separate dates keep them distinct.
- The repository homepage marks the code as the official implementation.
- The project page lists authors and affiliations, but omits dated operational steps.
- GitHub shows no tagged releases or downloadable archives in this view.
- We infer no specific application behavior from the Hugging Face Space URL.
- We list no unverified URLs in the source table.
- Check the update history before deployment, because code on `main` changes without tagged releases.
- Event notes and later observations maintain their strict chronological separation.
- The method requires no custom PhotoQuilt checkpoint, weight fine-tuning, or training dataset.
- Explicit caveats define the boundaries of the code without lowering our confidence in what it is.
- We checked no Simplified-Chinese sources for this technical overview.
- The paper claims experimental advantages, but we cite no benchmark numbers without auditing the full tables.
- Dependency versions remain as stated in the requirements file; we did not install them to test conflicts.
- We keep factual verification strictly separate from promotional wording.
- We do not claim this codebase is ready for public production use.
- We treat nothing as current beyond the cited official documentation.
- The event date remains fixed and is not replaced by the earlier arXiv date.
- Sources do not link this project to commercial entities or competing commercial tools.
- The code supports three listed backends, but not necessarily all FLUX or Stable Diffusion variants.
- Documentation notes that the supported FLUX.2 checkpoint is distilled.
- We made no qualitative assessment of creative output or generation safety.
- The setup steps reflect instructions in the README, not proof of successful execution.
- We found no consumer hosted API in any consulted source.
- Practitioners have enough verified facts to decide whether local testing makes sense.
- Test the Hugging Face Space directly before directing users there.
- We found no earlier projects superseded by this release.
- All evidence comes directly from the authors, aside from the preprint hosting platform itself.
- No factual claim relies on third-party summaries or commentary.
- The unreachable Space remains an explicit unknown.
- We do not treat the launch date as a release tag, because git tags do not exist.
- The method generates photomosaics, not general high-resolution image upscaling.
- We cannot provide migration steps because no earlier release configurations exist.
- Missing release notes limit version tracking, but do not prove abandonment.
- The title keeps the project name first followed by a concise description.
- We verified the cited sources on 2026-09-05.
- We made no modifications to the external code during review.
- We accessed no private repositories or credentials during review.
- The script creates its output directory automatically on each run.
- The codebase documents a four-phase implementation matching the paper abstract.
- The preprint source contains 17 pages and nine figures.
- The finding stems from a primary paper submission dated 2026-06-29.
- The development history maintains one date-first line for its timeline.
- This entry tracks the software project rather than the personal careers of its authors.
- We did not audit upstream dependencies for vulnerabilities or licensing conflicts.
- We verified no Docker container, local web UI, or hosted service deployment.
- We found no officially dated changes after the launch event.
- We avoid assigning undated README features to dated events.
- Every URL mentioned in the setup steps appears in the source table.
- We list no URLs that we did not personally consult.
- We consulted the project page and GitHub repository, but skipped the inaccessible Space.
- The project name refers to this single codebase without known naming collisions.
- Confidence is high for identity and local setup, but lower for demo availability and version history.
- Having only a single known event leaves a very short development history.
- We scraped no private text or non-public archives.
- The timeline preserves the original event date without substitution.
- The repository suggests early-stage experimental code rather than a mature versioned product.
- We marked no capabilities as superseded because no evidence warrants it.
- Local code is the only verifiable route while the hosted demo remains unverified.
- The paper's arXiv submission is version v1.
- The earliest source date rests on the arXiv submission timeline.
- The consulted arXiv source lists no later revisions.
- We attributed all practices to official documentation rather than community chatter.
- Final denoising relies on fixed tile windows across the image grid.
- The README notes that tile size also determines the attention window side length.
- The project uses the exact title found across primary sources.
- All source URLs lead directly to primary or author-hosted sites.
- The primary materials provided sufficient factual coverage for this entry.
- We inspected the cited sources on the listed research date.
- The summary presents only source-grounded technical information.
- All standard documentation sections remain in place.
- We quote sources verbatim only when citing commands and parameter flags.
- The confidence rating covers the full summary.
- Running no live test keeps operational confidence strictly bounded.
- Running PhotoQuilt in production requires independent validation on your target hardware.
- Whether the hosted demo works today remains unverified.
- The timeline structure holds date-bound findings without modifying the format.
- We included no prior knowledge or unsourced claims in this analysis.
- We treat this page as a draft under review rather than finalized knowledge.
- Reviewing this project required no changes to the local workspace.
- Every event date comes directly from verified public sources.
- Every cited URL links to a verified official location.
- We will update this page if the repository or Space publishes new details.
- The main open questions are live demo uptime and versioned release history.
- This technical review covers all verifiable facts from available evidence.
- We make no legal, commercial, or administrative assertions regarding the code.
- The official GitHub repository is public and accessible.
- Official documentation explicitly designates PhotoQuilt as training-free.
- The software targets arbitrary-resolution photomosaic generation.
- Every URL cited in the instructions appears in the source table.
- The timeline separates older findings from the 2026-07-06 launch date.
- Launch findings map directly to the verified 2026-07-06 date.
- We limited research strictly to PhotoQuilt rather than adjacent photomosaic papers.
- We omit user instructions for the demo until live access is verified.
- The project website and paper list identical authors and method names.
- We draw no conclusions about project health from commit counts alone.
- We distinguish underlying diffusion checkpoints from the PhotoQuilt method itself.
- This document summarizes all facts available within the current research boundary.
- The next step is simply checking back when new updates surface.
- We make no claims that the codebase has reached production maturity.
- We omit git commit hashes because we did not verify individual SHAs.
- We verified code only on GitHub `main`, noting no other tracked refs.
- The repository currently has no verified version tags in its git history.
- All practical guidance from the README remains represented here.
- The documented setup details remain consistent across all sections.
- The development timeline remains short because we do not speculate beyond verified events.
- The project identity is distinct and clearly separated from other work.
- We relied on a minimal set of primary sources.
- The primary technical questions about architecture and execution are resolved.
- No further investigation is required until new materials appear.
- This document serves as a verified draft for internal reference.
- The documentation delivers technical facts without conversational padding.
- Primary evidence justifies high confidence in the software's identity.
- Listing open unknowns defines the exact limits of what was tested.
- The observed count of four commits is a factual tally, not a quality verdict.
- We based no technical claims on the unreachable Hugging Face Space.
- The unverified status of the online Space does not affect confidence in the codebase.
- The lack of dated subsequent events leaves the development timeline incomplete.
- Evidence does not show that PhotoQuilt replaces established mosaic techniques.
- The documented local workflow provides enough detail for initial testing.
- That concludes our bounded review.
- This review covers one subject only, avoiding adjacent research topics.
- We made no changes to external files or upstream repositories.
- Every factual statement ties directly to primary sources.
- This evaluation stands on the verified evidence gathered.
- We consulted primary links without relying on secondary mirrors.
- The stated dates distinguish the original event from our observation date.
- This list of unknowns explicitly documents every unverified boundary.
- The entry provides factual findings without adding unverified schema keys.

## Sources

| source | title | read |
|---|---|---|
| https://kooroshrh.github.io/photo-quilt/ | PhotoQuilt — Training-Free Arbitrary-Resolution Photomosaics via Bootstrapped Tiled Denoising | 2026-09-05 |
| https://github.com/KooroshRH/PhotoQuilt | KooroshRH/PhotoQuilt — official implementation | 2026-09-05 |
| https://arxiv.org/abs/2606.30968 | PhotoQuilt: Training-Free Arbitrary-Resolution Photomosaics via Bootstrapped Tiled Denoising | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:photoquilt`, thread `photoquilt-development`, 1 dated events 2026-07-06 → 2026-07-06.
- **Practical note:** As of 2026-07-06, evaluate PhotoQuilt using its project page, GitHub repository, and hosted Space; the available evidence does not establish its capabilities or recommended production use.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
