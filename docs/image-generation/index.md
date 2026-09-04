---
title: Image Generation
type: MOC
---

# Image Generation

## Architectures
- [[MMDiT]] - MMDiT is the Stable Diffusion 3 multimodal transformer pattern: modality-specific representations participate in joint attention; implementation APIs and LoRA target names vary by model revision.
- [[flow-matching]] - Flow matching trains a continuous vector field along a chosen probability path; scheduler, path, and inference settings are checkpoint-specific rather than universal diffusion defaults.
- [[block-causal-linear-attention]] - Block causal linear attention is SANA-Video's trained long-video mechanism with a fixed-size cumulative attention state; it is not a generic plug-in for arbitrary image tiling or DiTs.
- [[DC-AE]] - Use DC-AE only with a diffusion model and latent contract it was trained for; high compression reduces latent-token work but does not make it a drop-in VAE replacement.
- [[SANA]] - SANA architecture
- [[sana-denoiser-architecture]] - A SANA-based restorer is a research proposal, not an implemented pipeline; it requires model-compatible conditioning, paired-data baselines, fidelity evaluation, and separate high-resolution tests before deployment.
- [[qwen-image]] - Qwen-Image generation/editing artifacts and version history
- [[transformers-v5]] - Transformers v5 moves checkpoint conversion into the loader, but every integration must be pinned to an installed release, runtime contract, checkpoint, and adapter test; current main-branch APIs are not universal compatibility.

## FLUX Models
- [[flux-klein-9b-inference]] - FLUX.2 [klein] 9B inference must follow the published model variant, checkpoint, scheduler, and license; benchmark the exact text or edit workflow instead of copying generic sampler, VRAM, or LoRA rules.
- [[flux-kontext]] - FLUX Kontext model
- [[comfyui-flux2klein-enhancer]] - Third-party multi-reference identity/detail conditioning for Klein

## Training & Fine-tuning
- [[diffusion-lora-training]] - Diffusion LoRA training is a version-bound adapter experiment; bind the exact base checkpoint, architecture, runtime, adapter format, authorized data, and evaluation split, and select rank, schedule, targets, and optimizer only from measured held-out behavior rather than copied recipes.
- [[lora-fine-tuning-for-editing-models]] - An editing LoRA is compatible only with its exact base checkpoint, architecture, runtime, and adapter format; train from authorized paired evidence, sweep capacity and schedule on held-out edits, and prove both requested change and preservation before release.
- [[Text-to-LoRA]] - Text-to-LoRA is a Sakana AI hypernetwork that creates task adapters for documented LLM target families from textual task descriptions; it is not a drop-in generator for diffusion-model LoRAs.
- [[paired-training-for-restoration]] - Paired restoration training learns a declared degraded-to-target mapping; it needs source-aligned and rights-cleared pairs, a model-compatible conditioning path, holdouts separated by source, and evaluation that distinguishes measured recovery from plausible invention.
- [[rights-first-text-to-mask-training]] - Rights-aware dataset contracts for grounding, masks, alpha, and multilingual queries

## Inference & Optimization
- [[diffusion-inference-acceleration]] - Diffusion acceleration is a model-and-runtime-specific trade-off; measure warm and steady-state latency, memory, output fidelity, and reproducibility for the exact checkpoint and workflow.
- [[tiled-inference]] - Tiled inference is a model-bound high-resolution strategy; partitioning, overlap, blending, global context, coordinate mapping, and output review must be evaluated together on the pinned pipeline, while detection tiles and generative or retouch tiles remain separate contracts.
- [[temporal-tiling]] - Temporal tiling is a model-specific research experiment for cross-tile consistency, not a direct reuse of video memory; bind the tile plan and runtime state, compare against an overlap baseline, and validate seams, composition, and cost on held-out images.
- [[low-vram-inference-strategies]] - Low-VRAM inference is a measured runtime configuration, not a hardware-tier promise; pin the model and backend, select only documented quantization, offload, or tiling paths, and record peak memory, latency, output fidelity, and failure behavior on the actual device.
- [[textual-latent-interpolation]] - Textual latent interpolation is a model-specific conditioning experiment: preserve non-target inputs, bind it to an exact encoder and adapter, sweep the requested range, and prove controllability and preservation instead of assuming semantic linearity.

## Editing & Restoration
- [[Step1X-Edit]] - Step1X-Edit is a StepFun multimodal image-editing family with release-specific pipelines; pair each checkpoint with its documented Diffusers branch and verify model and artifact terms independently.
- [ACE++](ACE++.md) - ACE++ provides reference-driven image creation and editing through task-specific LoRA workflows and a general FFT model; use the published base-model pairing and verify its terms.
- [[LaMa]] - LaMa is a Fourier-convolution inpainting model for large masks and resolution generalization; use it with a compatible checkpoint and test texture continuity separately from semantic object restoration.
- [[image-restoration-survey]] - Image restoration must declare the degradation and fidelity target; choose a task-compatible deterministic or diffusion method, then validate measured recovery separately from plausible but invented detail.
- [[RealRestorer]] - RealRestorer is a large image-editing-model restoration workflow for nine documented degradation types; use the repository's patched local runtime and evaluate fidelity separately from benchmark scores.
- [[retouch-patch-harmonization]] - Build color-consistent defect-inpainting training pairs
- [[perspective-calibration-for-compositing]] - Recover camera geometry before inserting or relighting objects
- [[color-checker-and-white-balance]] - Color checker and white-balance correction requires a measured physical chart or a separately validated estimator; detector output and a generated checker are not colorimetric ground truth.
- [[grayscale-overlay-nn-architectures]] - Grayscale overlay prediction is a paired, pixel-aligned retouching task; preserve the blend contract and no-op baseline, bind every source/target pair and mask, and evaluate the composited image plus the map before releasing an automated adjustment.

## Specialized Models
- [[Calligrapher]] - Calligrapher customizes text imagery from style references through FLUX.1-Fill-dev, SigLIP, masks, and project weights; treat typography accuracy and licensing as separate acceptance checks.
- [[PixelSmile]] - PixelSmile is a release-bound facial-expression editing project; pin its published human preview, base model, patched runtime, consented source image, and expression review rather than treating benchmark numbers or adapters as general guarantees.
- [[X-Dub]] - X-Dub is a public Wan2.2-TI2V-5B-based visual-dubbing release; validate single-person cropping, identity, temporal stability, audio rights, and model terms on every target video.
- [[FLAIR]] - FLAIR is a training-free flow-based posterior-sampling framework for inverse imaging; use its published configuration and verify fidelity, observed-data consistency, and base-model terms on the target task.
- [[MACRO]] - MACRO is a structured multi-reference dataset, benchmark, and set of model-specific fine-tuning assets; validate the compatible base model and artifact terms before deployment.
- [[MARBLE]] - MARBLE performs material transfer, blending, and parametric material edits through CLIP-space controls over a pretrained image generator; validate object geometry, illumination, and artifact licenses for each workflow.
- [[ATI]] - ATI adds trajectory-conditioned object, local, and camera motion control to its Wan2.1-based image-to-video workflow; preserve the published model, checkpoint, and localhost editor boundaries.
- [[comfyui-sensenova-u1]] - Official SenseNova U1/U1.5 versus third-party ComfyUI wrapper

## Segmentation
- [[in-context-segmentation]] - In-context segmentation transfers a supplied reference mask through a named vision model; its output is a candidate mask, not ground truth, and requires reference provenance, target review, uncertainty handling, and source-disjoint validation.

## Additional References

- [[anatomy-correction-diffusion]] - Anatomy correction is a diagnose-mask-condition-inpaint workflow; use geometry-aware research methods and model-matched editing tools, then visually verify every edited hand or limb against the source.
- [[color-correction-by-numbers]] - Color correction is valid only against a declared measurement target, illuminant, camera or profile, working space, and viewing transform; neutral samples and chart patches are evidence when their provenance is known, while scene averages and skin-color ratios are not universal ground truth.
- [[color-space-and-gamma-reference]] - Color management is a versioned chain of input interpretation, working space, creative transforms, display or view transform, and output encoding; camera or container labels and generic gamma rules are insufficient without the exact profile, transform version, metadata policy, and validation display.
- [[color-theory-for-ml]] - Color guidance for ML is a task-specific representation and evidence contract: name the source encoding, illuminant or viewing assumptions, target transform, palette intent, and human-review purpose; artistic harmony, spectral labels, and psychological associations are hypotheses, not universal labels or model controls.
- [[comfyui-wan-vace-video-joiner]] - A ComfyUI Wan VACE video join is a release-bound community workflow, not a generic transition node; pin its workflow revision, ComfyUI/custom-node/model dependencies, input frame/timestamp/color contracts, generated bridge and loop policy, intermediate artifacts, and visual/audio review before publishing a joined clip.
- [[defect-detection-small-objects]] - Defect and small-object detection produces reviewable candidates, not automatic quality truth; bind the model, capture protocol, annotation or normal-reference policy, slicing or merge mapping, thresholds, and source-disjoint evaluation before any inspection or workflow decision.
- [[denoise-architectures-2026]] - A denoising architecture is selected against a declared degradation and fidelity target, not a leaderboard or family name; bind capture/noise assumptions, model and checkpoint, preprocessing/tiling/color path, authorized train/evaluation splits, task and preservation metrics, and visual review before accepting generated or restored detail.
- [[diffusion-distillation-cdm]] - Continuous-Time Distribution Matching (CDM) is a research method for few-step diffusion distillation, not a drop-in speed switch; bind the paper/code/checkpoint and license, teacher/student parameterization and schedule, training/distributed runtime, source-disjoint quality/diversity/preservation evaluation, and rollback-ready serving evidence before use.
- [[edge-softness-and-compositing]] - Measure the edge instead of choosing it: 10-90 transition width, robust outline fitting
- [[face-beautify-edit-lora]] - A face edit LoRA is a paired, consent-aware local-edit training task; bind the adapter to its exact base model and validate the requested correction separately from identity preservation.
- [[face-detection-filtering-pipeline]] - Face filtering is a provenance-preserving candidate-selection pipeline; detector boxes and landmarks support review, but they do not establish identity, consent, image realism, or training suitability.
- [[flowinone-unified-multimodal-generation-via-image-flow]] - FlowInOne is a research release for visual-prompt image-in/image-out flow matching; bind the exact paper, checkpoint, code/runtime, license, task and input rendering contract, and source-disjoint task/preservation evaluation, and do not generalize paper benchmarks into production capability or commercial-use claims.
- [[flux-attention-manipulation]] - Attention interventions in FLUX-family DiTs are research- and implementation-specific; use the exact model's exposed attention path, preserve its conditioning contract, and validate composition rather than treating maps as causal proof.
- [[flux-klein-9b-architecture]] - FLUX.2 [klein] architecture claims must be tied to the named official release and artifact; the public family supports text-to-image and reference editing, but internal block layouts, encoder wiring, quantization, and adapter compatibility are not safe to infer across variants or runtimes.
- [[flux-klein-capability-map]] - A FLUX.2 [klein] capability is usable only when the exact variant, checkpoint, license, runtime or provider endpoint, input contract, and output review are attested at execution time; family-level generation and editing support does not authorize every adapter, service, commercial use, or editing result.
- [[flux-klein-character-lora]] - An identity LoRA is a sensitive, version-bound adapter trained only from authorized images under a defined purpose; bind consent, base checkpoint and adapter format, data and deletion policy, and source-disjoint likeness and preservation review, and never treat a generated identity match as verified identity.
- [[flux-klein-jewelry-photography]] - Jewelry imagery is a source-controlled product workflow: preserve the approved asset, material and geometry evidence, color pipeline, and rights boundary, then release only after visual and factual QA.
- [[flux-klein-style-lora-system]] - A FLUX.2 [klein] style LoRA is a version-bound data-and-evaluation workflow; separate style from subject data, preserve rights and provenance, and validate transfer on held-out content.
- [[fp8-quantization-optimization-for-e4m3]] - FP8 E4M3 quantization is a release- and backend-specific numerical contract; bind the tensor format, scaling recipe, supported operations and hardware, calibration or amax evidence, serialization/runtime path, and quality/latency/memory measurements, and never substitute clipping or another format silently.
- [[frequency-decomposition-editing]] - Frequency decomposition is a declared transform, not a semantic edit map; record color domain, transform or filter, boundary and reconstruction policy, edit masks, and output review, and distinguish mathematically reconstructed signal from generated or visually plausible detail.
- [[in-context-segmentation-with-insid3-and-dinov3]] - INSID3 with DINOv3 transfers a supplied reference mask through a named frozen-backbone release as a candidate segmentation, not ground truth; bind the repository and model revisions, license and access, reference/mask provenance, preprocessing and resolution, positional-bias configuration, uncertainty policy, and source-disjoint review before use.
- [[intrinsic-decomposition]] - Intrinsic decomposition is an ambiguity-bound estimate of reflectance and illumination, not ground truth; bind the image-formation assumptions, model and version, color domain, residual policy, source evidence, and task-specific review before using its albedo or shading outputs for editing or relighting.
- [[lora-auxiliary-losses]] - LoRA auxiliary losses are experiment-specific objectives, not a portable recipe; bind the base model, adapter format, data rights, loss implementation, weighting search range, validation split, and task/preservation evaluation, and treat identity or mask losses as sensitive controls rather than proof of likeness.
- [[lora-identity-disentanglement-in-flux2-klein-9b]] - A FLUX.2 [klein] 9B identity LoRA is a version-, data-, and rights-bound adapter experiment; bind the official base release and terms, adapter/runtime format, authorized identity references, label/caption and preservation policy, source-disjoint identity and non-target evaluation, and review before any use.
- [[megastyle-flux-style-transfer]] - MegaStyle is a research code, model, and dataset release for image style transfer; bind the exact repository/artifact revision and license, base-model/runtime dependency, reference and prompt provenance, rendering and output contract, source-disjoint style/content/preservation evaluation, and human review before publishing or training on results.
- [[object-removal-inpainting]] - Object removal is a constrained edit: bind the source asset, permitted object, mask, model contract, and protected regions, then validate scene continuity and factual preservation before release.
- [[pixel-art-generation]] - Pixel-art generation is a constrained asset workflow, not a style prompt; bind the logical grid, palette, alpha and animation/sprite contract, source and training rights, model or raster tool release, deterministic export path, and human review of readability, geometry, and factual detail before delivery.
- [[plugin-inference-ux]] - ML plugin inference UX is an explicit host-and-job-state contract: pin the host API, document snapshot and model versions, cancellation and progress behavior, cache and invalidation keys, preview provenance, non-destructive commit, and measured latency rather than promising universal responsiveness.
- [[recurrent-depth-transformer]] - Recurrent-depth transformers reuse a version-specific shared block across iterations; bind the published architecture, checkpoint and runtime, recurrence budget, cache and termination behavior, and measured quality/cost, and do not infer latent reasoning, early exit, stability, or deployability from the family name.
- [[segmentation-dataset-preparation]] - Segmentation dataset preparation is a lineage and supervision contract: bind source/rights, annotation policy and mask semantics, group-disjoint splits, augmentation and interpolation behavior, class coverage, and release metrics, and fail closed on leakage, unreviewed labels, or incompatible targets.
- [[skin-retouch-pipeline]] - Skin retouching is a consent-aware, scope-limited correction workflow; preserve identity, texture, and protected traits, keep every mask and edit auditable, and require review of all changed skin.
- [[spatialedit-16b-geometric-control-for-diffusion-based-image-editing]] - SpatialEdit-16B is a multimodal diffusion transformer (MM-DiT) framework designed for precise
- [[style-reference-ux]] - Style-reference UX must separate temporary influence from saved training, style from content/structure, and local data from third-party processing, while making strength and provenance visible to the user.
- [[synthetic-dataset-pipeline]] - Synthetic detection data is a labeled candidate corpus, not automatic ground truth; preserve generator and source provenance, review annotations, prevent split leakage, and validate on real held-out data.
- [[tile-position-encoding]] - Tile position encoding is a model-specific spatial contract, not a universal channel recipe; bind the full-image coordinate frame, crop/overlap and padding policy, encoding family and injection point, model release and training distribution, and seam/geometry evaluation before treating tiled outputs as globally coherent.
- [[upscaler-evaluation]] - Choose an upscaler by measured fidelity on the actual source class, not benchmark labels or a universal default; preserve source/output provenance, evaluate artifacts and factual detail, and keep generative outputs out of factual training targets.
- [[videomama-diffusion-based-video-matting]] - VideoMaMa is a video matting framework that converts coarse segmentation masks into pixel-perfect
- [[watermark-removal]] - Removing visible logos, text overlays, and branding from images
