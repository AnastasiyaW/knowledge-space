# FlowInOne: Unified Multimodal Generation via Image Flow

FlowInOne is a multimodal generation framework that treats all inputs—text, classes, bounding boxes, or doodles—as visual prompts. It operates on an image-in/image-out paradigm using flow matching instead of traditional diffusion denoising. The model contains 1.2B parameters and is built upon the CrossFlow architecture.

## Core Architecture
The system bypasses typical cross-modal alignment issues by encoding all conditional inputs into a unified visual representation.

- **Visual Encoding:** Uses Janus-Pro-1B as the primary visual encoder for all prompts.
- **Image Coding:** Employs a frozen Stable Diffusion VAE for encoding target images into latent space.
- **Dual-Path Spatially-Adaptive Modulation:** A dynamic routing mechanism that adjusts processing based on the specific task type (e.g., editing vs. generation).
- **Flow Matching:** Unlike diffusion-based models, FlowInOne learns a velocity field to transform noise into the target image, which can improve sampling efficiency and path straightness.

## Capabilities and Task Modalities
FlowInOne supports diverse generative and editing tasks within a single weights-set:

- **Generative Tasks:** Standard Text-to-Image (T2I) and Class-to-Image generation.
- **Conditional Editing:** 
    - **Instruction-based:** Text-driven modifications.
    - **Spatial Control:** Bounding box-guided editing and visual marker placement.
    - **Sketch-based:** Doodle-to-image synthesis.
- **Physics and Motion:** 
    - **Force Dynamics:** Physics-aware generation based on "force" inputs.
    - **Trajectory Prediction:** Generating frames or sequences based on motion paths.

### Sampling Configuration
The model typically requires a high guidance scale and significant sampling steps to achieve quality results at its current scale.

```text
Sampling Steps: 50
CFG Guidance: 7.0
Resolution: 256x256
Base Framework: CrossFlow
```

## Performance and Constraints
While architecturally elegant, FlowInOne 1.2B currently serves as a research proof-of-concept (PoC).

- **Spatial Resolution:** Native output is limited to 256x256 pixels, which limits practical utility in production environments without upscaling.
- **Competitive Metrics:** Achieves a human pass rate of 44.9%, outperforming similar small-scale models like Nano Banana (40.6%) in multimodal consistency.
- **Efficiency:** The 1.2B parameter count makes it lightweight enough for local deployment, though its flow-matching inference speed is balanced by the requirement for 50 sampling steps.

## Gotchas
- **Issue: Low Native Resolution** → **Fix:** Output is strictly 256x256; use a separate super-resolution model or latent upscaler for high-resolution requirements.
- **Issue: License Ambiguity** → **Fix:** GitHub lists MIT while HuggingFace specifies Apache-2.0. Both are permissive for commercial use, but verify legal compliance if redistributing modified weights.
- **Issue: Inference Cost** → **Fix:** Despite the small parameter count, the 50-step sampling requirement means it is not inherently faster than larger distilled diffusion models (like FLUX.1 [schnell]) which run in 1-4 steps.

## See Also
- [[flow-matching]]
- [[MMDiT]]
- [[flux-kontext]]
- [[Step1X-Edit]]
- [[DC-AE]]

