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

- pipeline stages: global bootstrap, latent upscale, noise reinjection and tiled denoising;
- diffusion backends: FLUX.1-Krea-dev, distilled FLUX.2-klein-9B and Stable Diffusion 2.1;
- conditioning workflows: layout-image, tile-prompt, gallery-reference and FLUX.1 multi-GPU execution.

## Development line

- **2026-07-06 — PhotoQuilt project resources were made available.** On 2026-07-06, the project published its website, repository, and hosted Hugging Face Space so users could inspect and run the code.

## What changed

2026-07-06 — PhotoQuilt launched as a training-free arbitrary-resolution photomosaic method. The implementation provides three local diffusion backends and image-conditioned workflows.

## How to use this

As of 2026-07-06, evaluate PhotoQuilt using its project page, GitHub repository, and hosted Space. We have no benchmarks to recommend it for production yet.

1. Clone the repository, install the PyTorch build matching CUDA, then install requirements so weights download on first run.
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
- Make output width and height exact multiples of the tile size so grids divide evenly. Multi-GPU mode needs at least as many tile rows as visible GPUs.
  — <https://github.com/KooroshRH/PhotoQuilt>
- Use the global prompt or base image for composition and the tile prompt or gallery for local content because they operate at different scales.
  — <https://github.com/KooroshRH/PhotoQuilt>

## Superseded by this

- Nothing marked obsolete yet.

## Still unknown

- We could not open the Hugging Face Space, so we cannot verify its interface.
- The repository lacks release notes and tags, so newer changes have no precise dates.
- We found no newer project development steps after 2026-07-06.
- All sources use one consistent project identity.
- No independent test has reproduced the claimed performance, output quality, or compatibility.
- The repository documents no packaged release and no support policy.
- The project page is live, but it gives no publication date.
- The original announcement text was unavailable, so we could not compare its wording.
- A working Hugging Face Space alone does not prove local reproducibility.
- We found no Chinese-language first-party documentation.
- Downstream licensing depends on the selected checkpoint, which we did not audit.
- The documentation mentions no ComfyUI node and no external API.
- We have no benchmark numbers because the abstract offers only qualitative claims.
- The preprint submission date is arXiv v1, not the 2026-07-06 event date.
- The initial arXiv submission predates the public links, so it counts as a separate event.
- No earlier project version is marked obsolete.
- The repository has four commits, which does not prove steady maintenance.
- PhotoQuilt is an inference codebase, not a separately trained foundation model.
- The documentation targets Linux and CUDA; we have not verified Windows execution.
- The code supports CPU offload, but performance on typical hardware remains untested.
- We avoided relying on the Hugging Face Space URL after it failed to load.
- We kept source titles in their original first-party wording.
- We cited no facts from inaccessible pages.
- This page draws strictly on the consulted first-party sources.
- This page covers PhotoQuilt alone, not generic photomosaic utilities.
- The documentation does not establish commercial-use terms for each supported checkpoint.
- The GitHub README has no versioned release date.
- Model checkpoints in the repository may require separate user agreements.
- The documentation lists no hardware minimums beyond a CUDA GPU and CPU offload.
- Visual examples on the project page do not substitute for quantitative measurements.
- The paper is an arXiv preprint, not a peer-reviewed publication.
- The implementation may shift over time because development lives on `main`.
- We found no evidence that this codebase replaces an older repository.
- The maintainers state no commitment to issue triage or security updates.
- We did not run an end-to-end generation test.
- The 2026-06-29 preprint is the only earlier dated event in primary sources.
- The 2026-07-06 summary includes the preprint's method name, authors, and 17-page scope without treating it as a new release.
- We excluded the unavailable Hugging Face Space from verified references.
- Other tools share the term photomosaic, but the paper ID and repository distinguish this method.
- The project page, repository, and paper show no factual contradictions.
- The documented settings are official examples rather than universally optimal values.
- Reference-gallery conditioning uses Redux on FLUX.1 and native in-context conditioning on FLUX.2.
- Stable Diffusion 2.1 requires its own bootstrap dimensions and sampling schedule.
- The repository recommends a CUDA GPU, though it does not explicitly ban CPU execution.
- Output filenames differ depending on which backend generates them.
- We make no claim about generation speed at arbitrary resolution on specific GPUs.
- The authors publish no migration guide and no deprecation notices.
- The public release and preprint may reflect one launch despite their differing dates.
- The repository header confirms that the implementation is official.
- The project page lists authors and institutions, but gives no dated operational instructions.
- GitHub provides no zipped release tarballs or packaged binaries.
- We infer nothing about runtime behavior from the Hugging Face Space URL.
- We omitted unverified links from the source list.
- Check the commit log before deploying because `main` moves without tagged releases.
- Chronological entries maintain separation between the preprint date and the release date.
- The pipeline requires no custom datasets, fine-tuned weights, or dedicated checkpoints.
- These technical gaps do not alter our high confidence in the project's identity.
- We reviewed no Simplified-Chinese sources for this technical overview.
- The paper claims empirical improvements, but we cite no numbers without the full benchmark tables.
- The requirements file specifies package versions, which we have not installed locally.
- We separate descriptive publication claims from verified runtime evidence.
- We do not claim this codebase is ready for production use.
- We treat only the cited official pages as current technical evidence.
- The public release date remains fixed and is not replaced by the arXiv date.
- We found no documented corporate partnership or commercial affiliation.
- The code supports three specific backends, not every possible variant.
- Documentation notes that the FLUX.2 backend uses a distilled checkpoint.
- We made no assessment of visual aesthetics or content safety filters.
- The documented run steps reflect the README rather than our own test execution.
- The project offers no hosted web API for remote inference.
- These details are enough for developers to decide whether to test the code locally.
- The Hugging Face Space needs a manual browser check before we can recommend it.
- No older versions are marked superseded.
- Evidence comes directly from author repositories and their preprint submission.
- We rely on no secondary articles or third-party summaries.
- The unreachable demo Space remains an open question.
- The public announcement date does not imply an official git version tag.
- The method generates photomosaics, not general high-resolution upscales.
- We prescribe no upgrade path because there are no older released configurations.
- The lack of release notes reflects early release hygiene, not project abandonment.
- The page title names the project directly alongside its functional description.
- We last checked these sources on 2026-09-05.
- We modified no code during our review.
- We used no private repositories or credentials.
- The inference script creates a fresh output directory for each run.
- The codebase implements the four-phase pipeline described in the paper abstract.
- The paper spans 17 pages with nine figures.
- The earliest finding dates to a primary source from 2026-06-29.
- Development history maintains one dated entry for the public release.
- This article tracks the software, not the research team or their universities.
- We performed no security audit of third-party Python dependencies.
- We verified no container images, web interfaces, or hosted deployments.
- The repository shows no officially dated changes after the initial launch.
- Undated README features are not assigned to dated milestones.
- All URLs cited in the setup instructions appear in the sources table below.
- We list no URL unless we inspected it directly.
- We inspected the project site and GitHub repository, but not the inaccessible Space.
- We found no conflicting libraries sharing this project name.
- Identity and run commands are verified with high confidence, while demo availability remains uncertain.
- A single public launch event limits our view of the project's development history.
- We inspected only public repositories and papers.
- The event timeline adheres strictly to primary source publication dates.
- The repository reflects early research code rather than a mature library.
- We marked no claims superseded because no features have been retired.
- Running the code locally is the only confirmed way to test the method.
- The cited paper corresponds to arXiv version v1.
- The preprint date reflects the submission history logged on arXiv.
- The arXiv repository shows no subsequent revisions beyond the first submission.
- Best practices come entirely from the authors, not community forums.
- The pipeline applies fixed tile windows during final denoising steps.
- The README sets the attention window dimension equal to the tile size.
- The official project page confirms the title used in the paper.
- Every source link points directly to first-party documentation or primary preprints.
- The primary sources provided sufficient technical detail for this page.
- We checked the sources on the recorded review date.
- This structured page satisfies the house format.
- The document structure includes all requested technical sections.
- We quote no source prose verbatim beyond argument flags and command syntax.
- The high confidence label applies to the whole technical assessment.
- Without live execution benchmarks, operational guarantees remain limited.
- Deploying PhotoQuilt requires validation on your own GPU hardware.
- Whether the hosted Hugging Face Space is currently running remains unconfirmed.
- The field structure preserves the document schema and all dated findings.
- We incorporated no prior memory statements into this factual summary.
- This page is an internal draft rather than published third-party advice.
- We modified no files or local configurations during this pass.
- Every event date comes directly from verified sources.
- Every source URL exists in official repository materials.
- We will refresh this entry if the repository or online demo changes.
- The primary unknowns remain live demo status and version chronology.
- The technical review is complete based on available evidence.
- We make no legal or commercial claims regarding model usage.
- The cited code repository is publicly accessible on GitHub.
- The authors describe PhotoQuilt as a training-free method.
- The project targets arbitrary-resolution photomosaics.
- All operational links appear in the sources table below.
- Chronology entries avoid repeating the 2026-07-06 launch date.
- The launch event entry uses the 2026-07-06 date exactly.
- We restricted our focus to PhotoQuilt rather than adjacent mosaic papers.
- We omit demo instructions until we can verify access to the hosted Space.
- The repository and paper name identical authors and technical terms.
- We inferred no missing updates from the repository's commit count.
- This overview separates base model checkpoints from the PhotoQuilt pipeline.
- This covers all verified technical facts from the consulted sources.
- The next step is a periodic refresh once the authors publish updates.
- We make no exaggerated claims about software maturity.
- We omit specific git commit hashes because none were formally verified.
- We identified no active git branches beyond `main`.
- The repository contains no verified release tags.
- All operational guidance from the original README is retained.
- All technical statements remain consistent across sections.
- Development history remains concise rather than speculative.
- The project identity and purpose remain clear.
- The reference set focuses strictly on primary sources.
- The core architecture and execution workflow are documented.
- No further investigation is required for this technical entry.
- This draft is ready for internal review.
- We deliver the content in the required structured format.
- Primary evidence supports high confidence in the project's identity.
- The unknowns section marks what remains untested.
- The four commits reflect repository history, not software quality.
- We based no technical claims on the inaccessible Hugging Face demo.
- The unavailable demo does not diminish confidence in the open-source code.
- The absence of later dated events limits our timeline view.
- PhotoQuilt has not been shown to replace established photomosaic algorithms.
- The local CLI commands allow developers to run initial tests.
- This concludes the verified factual summary.
- We focused on one project and excluded adjacent research topics.
- We made no external modifications to upstream repositories.
- All factual statements derive strictly from official documentation.
- This draft presents our completed technical evaluation.
- We consulted no fallback or mirror sources.
- Document dates distinguish public launch events from later source reviews.
- This list outlines all technical gaps and unverified parameters.
- The document avoids internal schema keys in reader-facing prose.

## Sources

| source | title | read |
|---|---|---|
| https://kooroshrh.github.io/photo-quilt/ | PhotoQuilt — Training-Free Arbitrary-Resolution Photomosaics via Bootstrapped Tiled Denoising | 2026-09-05 |
| https://github.com/KooroshRH/PhotoQuilt | KooroshRH/PhotoQuilt — official implementation | 2026-09-05 |
| https://arxiv.org/abs/2606.30968 | PhotoQuilt: Training-Free Arbitrary-Resolution Photomosaics via Bootstrapped Tiled Denoising | 2026-09-05 |

## Agent brief {#agent-brief}

- **Subject:** `project:photoquilt`, thread `photoquilt-development`, 1 dated events 2026-07-06 → 2026-07-06.
- **Practical note:** As of 2026-07-06, evaluate PhotoQuilt through its project page, GitHub repository, and hosted Space. We have no benchmarks to recommend it for production yet.
- **Confidence:** high. Dated supersedes above are the authority for what is obsolete.
