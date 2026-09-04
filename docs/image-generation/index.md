---
title: Image Generation
type: MOC
---

# Image Generation

## Architectures
- [[MMDiT]] - MMDiT is the Stable Diffusion 3 multimodal transformer pattern: modality-specific representations participate in joint attention; implementation APIs and LoRA target names vary by model revision.
- [[flow-matching]] - Flow matching for diffusion models
- [[block-causal-linear-attention]] - Block causal linear attention is SANA-Video's trained long-video mechanism with a fixed-size cumulative attention state; it is not a generic plug-in for arbitrary image tiling or DiTs.
- [[DC-AE]] - Use DC-AE only with a diffusion model and latent contract it was trained for; high compression reduces latent-token work but does not make it a drop-in VAE replacement.
- [[SANA]] - SANA architecture
- [[sana-denoiser-architecture]] - SANA denoiser design
- [[qwen-image]] - Qwen-Image generation/editing artifacts and version history
- [[transformers-v5]] - Transformers v5 for diffusion

## FLUX Models
- [[flux-klein-9b-inference]] - FLUX Klein 9B inference guide and best practices
- [[flux-kontext]] - FLUX Kontext model
- [[comfyui-flux2klein-enhancer]] - Third-party multi-reference identity/detail conditioning for Klein

## Training & Fine-tuning
- [[diffusion-lora-training]] - LoRA training for diffusion models
- [[lora-fine-tuning-for-editing-models]] - LoRA fine-tuning for editing models
- [[Text-to-LoRA]] - Text-to-LoRA is a Sakana AI hypernetwork that creates task adapters for documented LLM target families from textual task descriptions; it is not a drop-in generator for diffusion-model LoRAs.
- [[paired-training-for-restoration]] - Paired training for image restoration
- [[rights-first-text-to-mask-training]] - Rights-aware dataset contracts for grounding, masks, alpha, and multilingual queries

## Inference & Optimization
- [[diffusion-inference-acceleration]] - Inference acceleration techniques
- [[tiled-inference]] - Tiled inference for high-resolution generation
- [[temporal-tiling]] - Tiles as temporal sequence
- [[low-vram-inference-strategies]] - Low-VRAM inference strategies
- [[textual-latent-interpolation]] - Textual latent interpolation

## Editing & Restoration
- [[Step1X-Edit]] - Step1X-Edit is a StepFun multimodal image-editing family with release-specific pipelines; pair each checkpoint with its documented Diffusers branch and verify model and artifact terms independently.
- [ACE++](ACE++.md) - ACE++ provides reference-driven image creation and editing through task-specific LoRA workflows and a general FFT model; use the published base-model pairing and verify its terms.
- [[LaMa]] - LaMa is a Fourier-convolution inpainting model for large masks and resolution generalization; use it with a compatible checkpoint and test texture continuity separately from semantic object restoration.
- [[image-restoration-survey]] - Image restoration survey
- [[RealRestorer]] - RealRestorer is a large image-editing-model restoration workflow for nine documented degradation types; use the repository's patched local runtime and evaluate fidelity separately from benchmark scores.
- [[retouch-patch-harmonization]] - Build color-consistent defect-inpainting training pairs
- [[perspective-calibration-for-compositing]] - Recover camera geometry before inserting or relighting objects
- [[color-checker-and-white-balance]] - Color checker and white balance correction
- [[grayscale-overlay-nn-architectures]] - Neural networks for grayscale overlay prediction

## Specialized Models
- [[Calligrapher]] - Calligrapher customizes text imagery from style references through FLUX.1-Fill-dev, SigLIP, masks, and project weights; treat typography accuracy and licensing as separate acceptance checks.
- [[PixelSmile]] - PixelSmile model
- [[X-Dub]] - X-Dub is a public Wan2.2-TI2V-5B-based visual-dubbing release; validate single-person cropping, identity, temporal stability, audio rights, and model terms on every target video.
- [[FLAIR]] - FLAIR is a training-free flow-based posterior-sampling framework for inverse imaging; use its published configuration and verify fidelity, observed-data consistency, and base-model terms on the target task.
- [[MACRO]] - MACRO is a structured multi-reference dataset, benchmark, and set of model-specific fine-tuning assets; validate the compatible base model and artifact terms before deployment.
- [[MARBLE]] - MARBLE performs material transfer, blending, and parametric material edits through CLIP-space controls over a pretrained image generator; validate object geometry, illumination, and artifact licenses for each workflow.
- [[ATI]] - ATI adds trajectory-conditioned object, local, and camera motion control to its Wan2.1-based image-to-video workflow; preserve the published model, checkpoint, and localhost editor boundaries.
- [[comfyui-sensenova-u1]] - Official SenseNova U1/U1.5 versus third-party ComfyUI wrapper

## Segmentation
- [[in-context-segmentation]] - In-context segmentation

## Additional References

- [[anatomy-correction-diffusion]] - Anatomy correction is a diagnose-mask-condition-inpaint workflow; use geometry-aware research methods and model-matched editing tools, then visually verify every edited hand or limb against the source.
- [[color-correction-by-numbers]] - Deterministic color correction using measurable channel targets rather than perceptual judgment
- [[color-space-and-gamma-reference]] - Practical reference for color management in video/photo processing pipelines
- [[color-theory-for-ml]] - Applied color theory for diffusion model training, color correction, and palette control
- [[comfyui-wan-vace-video-joiner]] - The Wan VACE Video Joiner is a node suite designed for assembling disparate video segments into a
- [[defect-detection-small-objects]] - Reference for detecting defects (scratches, dust, surface anomalies) and small objects in
- [[denoise-architectures-2026]] - 2025-2026 landscape of image denoising architectures: NTIRE 2025 winners, SSM/Mamba-based models
- [[diffusion-distillation-cdm]] - flow-matching distillation to 4 NFE without GAN or reward model
- [[edge-softness-and-compositing]] - Measure the edge instead of choosing it: 10-90 transition width, robust outline fitting
- [[face-beautify-edit-lora]] - Training before/after edit LoRAs on FLUX Klein 9B and Qwen-Image-Edit for facial correction
- [[face-detection-filtering-pipeline]] - Reusable pipeline for filtering image collections by face presence, quality, and type using YOLO
- [[flowinone-unified-multimodal-generation-via-image-flow]] - FlowInOne is a multimodal generation framework that treats all inputs—text, classes, bounding
- [[flux-attention-manipulation]] - Techniques for manipulating, analyzing, and exploiting the joint self-attention mechanism in
- [[flux-klein-9b-architecture]] - Deep reference for the FLUX.2 Klein 9B model internals: transformer structure, text encoding, VAE
- [[flux-klein-capability-map]] - Reference for what FLUX.2 Klein 9B can do natively, via official LoRAs, via fal.ai LoRAs, and via
- [[flux-klein-character-lora]] - Training LoRAs to preserve a specific person's identity with FLUX.2 Klein 9B
- [[flux-klein-jewelry-photography]] - Production pipeline for generating and compositing jewelry product photography using FLUX.2 Klein 9B
- [[flux-klein-style-lora-system]] - Architecture and empirical findings for a user-facing style LoRA system on FLUX.2 Klein Base 9B
- [[fp8-quantization-optimization-for-e4m3]] - FP8 (E4M3) quantization is used to accelerate inference and training on NVIDIA Hopper architecture
- [[frequency-decomposition-editing]] - Methods for separating images into low-frequency (LF) and high-frequency (HF) components, editing
- [[in-context-segmentation-with-insid3-and-dinov3]] - INSID3 is a training-free framework for one-shot in-context segmentation that leverages dense
- [[intrinsic-decomposition]] - Separating an image into intrinsic components (reflectance/albedo vs
- [[lora-auxiliary-losses]] - Additional loss terms beyond standard diffusion denoising loss
- [[lora-identity-disentanglement-in-flux2-klein-9b]] - Identity LoRA training often suffers from concept bleeding, where environmental factors (lighting
- [[megastyle-flux-style-transfer]] - MegaStyle is a single-reference style transfer framework developed by Tencent for FLUX.1-dev
- [[object-removal-inpainting]] - Comparative reference for object removal/erasure models (2024-2026)
- [[pixel-art-generation]] - Algorithms and models for converting raster images to pixel art, generating pixel art via diffusion
- [[plugin-inference-ux]] - Patterns for making slow ML inference (10-30s per operation) feel fast inside desktop creative
- [[recurrent-depth-transformer]] - Looped transformer architecture that reuses a single block T times to simulate multi-step reasoning
- [[segmentation-dataset-preparation]] - Reference for binary semantic segmentation datasets with 0.1-5% positive-pixel coverage (small
- [[skin-retouch-pipeline]] - Automated blemish detection and removal pipeline for photos
- [[spatialedit-16b-geometric-control-for-diffusion-based-image-editing]] - SpatialEdit-16B is a multimodal diffusion transformer (MM-DiT) framework designed for precise
- [[style-reference-ux]] - Comparative analysis of style reference workflows across major AI image generation products
- [[synthetic-dataset-pipeline]] - Pipeline for building high-quality annotated datasets for YOLO + SAM fine-tuning from raw image
- [[tile-position-encoding]] - Methods for injecting spatial position information into patch/tile-based image models, with
- [[upscaler-evaluation]] - Practical comparison of image upscalers for LoRA training data preparation and production pipelines
- [[videomama-diffusion-based-video-matting]] - VideoMaMa is a video matting framework that converts coarse segmentation masks into pixel-perfect
- [[watermark-removal]] - Removing visible logos, text overlays, and branding from images
