# SpatialEdit-16B: Geometric Control for Diffusion-Based Image Editing

SpatialEdit-16B is a multimodal diffusion transformer (MM-DiT) framework designed for precise geometric manipulation of objects and camera perspectives in 2D images. It addresses the "spatial gap" in semantic editors by focusing on metric transformations like rotation, translation, and scaling.

## System Architecture
The model utilizes a 16-billion parameter Multi-Modal Diffusion Transformer (MM-DiT) backbone, derived from the Wan2.1 video model architecture but optimized for high-fidelity image-to-image spatial edits.

- **Vision-Language Encoder:** Qwen3-VL-8B-Instruct serves as the primary multimodal encoder, processing the source image and text instruction to generate conditioning tokens.
- **Backbone:** MM-DiT with 40 double blocks, a hidden size of 4096, and 32 attention heads.
- **Inference Pipeline:**
  - **Scheduler:** FlowMatchDiscreteScheduler (1000 timesteps).
  - **VAE:** WanxVAE in `bf16` precision.
  - **Sampling:** Typically 30 steps with a guidance scale of 5.0.
- **Training Stages:** Initial pre-training on general image editing datasets followed by LoRA post-training (rank 16, alpha 16) on the SpatialEdit-500K synthetic dataset for geometric specialization.

## Geometric Control Capabilities
SpatialEdit treats spatial manipulation through two primary lenses: object-centric and camera-centric transformations.

### Object-Centric Edits
- **Rotation:** Supports 8 discrete canonical viewpoints (Front, Rear, Left, Right, and diagonal variants).
- **Translation:** Repositions objects within the frame using text-based instructions or red-box bounding box prompts.
- **Scaling:** Resizes specific objects while attempting to maintain scene consistency.

### Camera-Centric Edits
- **Perspective Shifts:** Controlled yaw rotation at 45° increments and pitch rotation at 15° intervals.
- **Framing:** Focal length variation for zoom-in and zoom-out operations.
- **Logic:** "Move the camera. Camera rotation: Yaw 45.0°, Pitch 0.0°. Keep the 3D scene static."

## Hardware and VRAM Requirements
The model's parameter count and architectural complexity necessitate significant GPU resources.

- **VRAM Floor:** Approximately 60-70 GB VRAM is required to load the full pipeline in `bf16`.
  - **DiT Checkpoint:** ~33 GB.
  - **Qwen3-VL-8B:** ~18 GB.
  - **VAE + Activations:** ~5-10 GB overhead.
- **GPU Compatibility:** Runs optimally on H100/H200 (140 GB) or A100 (80 GB). Standard consumer hardware (RTX 4090, 24 GB) is currently insufficient for the full-precision weights without aggressive quantization or offloading.

## Technical Comparison
SpatialEdit-16B is specialized for geometry and complements semantic-heavy models like Qwen-Image-Edit.

| Feature | Qwen-Image-Edit | SpatialEdit-16B |
| :--- | :--- | :--- |
| **Primary Strength** | Appearance/Semantic changes | Geometric/Spatial transforms |
| **Rotation** | Poor/Hallucinated | Precise (8 Canonical views) |
| **Background** | Often modified | High preservation |
| **Training Data** | Web-scale natural images | Synthetic 3D-generated spatial pairs |

## Gotchas
- **Issue:** The official repository contains hardcoded absolute paths in `wanvae.py` (e.g., `/pfs/yichengxiao/...`) → **Fix:** Manually edit the VAE loading logic to point to local HuggingFace cache directories.
- **Issue:** Dependency mismatch for `diffusers==0.36.2` and `transformers==4.54.0` (unreleased versions on PyPI as of mid-2026) → **Fix:** Install directly from the development branches on GitHub or use the provided environment containers.
- **Issue:** Discrete Rotation Limit → **Fix:** SpatialEdit is limited to 8 specific viewpoints; it cannot perform free-form arbitrary 3D rotation beyond the canonical angles it was trained on.
- **Issue:** OOM on 24GB GPUs → **Fix:** The model currently lacks a native 4-bit or 8-bit quantized version; use `JD-opensource/JoyAI-Image` as a lower-parameter alternative if VRAM is constrained.

## See Also
- [[diffusion-inference-acceleration]]
- [[in-context-segmentation]]
- [[DC-AE]]
- [[flux-klein-9b-inference]]
- [[MMDiT]]

