# MegaStyle FLUX Style Transfer

MegaStyle is a single-reference style transfer framework developed by Tencent for FLUX.1-dev. It utilizes a dedicated style encoder and a LoRA-based adapter to transfer artistic styles from a single reference image to text-to-image generations while maintaining content fidelity.

## Core Architecture
The system consists of three primary components integrated with the BFL FLUX.1-dev base model:

- **MegaStyle-FLUX LoRA:** A 1.2 GB adapter (`safetensors`) trained on top of the base model to inject styling capabilities without full fine-tuning.
- **MegaStyle-Encoder:** A contrastive style encoder (857 MB, `.pth`) trained using style-supervised contrastive learning to extract representative style vectors from reference images.
- **I/O Contract:** Input requires a text prompt and exactly one reference image. Output is a stylized image corresponding to the prompt's content and the reference's aesthetics.

## MegaStyle-1.4M Dataset
The model was trained on a large-scale synthetic dataset designed for high-quality style extraction:

- **Scale:** 1.4 million image pairs.
- **Content:** Diverse content-style combinations with high intra-style consistency and inter-style diversity.
- **Annotation:** Prompts generated via Qwen3-VL and Qwen-Image for precise alignment.

## Implementation and Inference

### Python CLI Usage
Basic inference requires the base FLUX.1-dev model weights, the MegaStyle LoRA, and the encoder.

```bash
python inference.py --ckpt_path models/megastyle_flux.safetensors --ref_path ./ref_styles
```

Style similarity between images can be calculated using the encoder:
```bash
python style_score.py --ckpt_path models/megastyle_encoder.pth --real <path> --fake <path>
```

### Hardware Requirements
- **VRAM:** ~24 GB VRAM for standard BF16 inference on FLUX.1-dev. 
- **Optimization:** For 24 GB consumer GPUs (e.g., RTX 3090/4090), quantization (FP8/4-bit) of the base model is necessary to accommodate the overhead of the style encoder and LoRA.

### ComfyUI Integration
The repository includes a ready-to-use integration in the `/comfyui/` directory:
- `nodes.py`: Custom nodes for style encoding and LoRA application.
- `workflow_megastyle.json`: Pre-configured graph for single-reference transfer.

## Licensing
The project follows a multi-license structure depending on the asset:

| Component | License |
|---|---|
| Model Weights (LoRA/Encoder) | MIT |
| Dataset / Paper | CC-BY-SA-4.0 |
| Code | MIT / Project License |

Pre-trained weights are commercially viable under MIT, but fine-tuning new models on the MegaStyle-1.4M dataset requires adhering to CC-BY-SA-4.0 (ShareAlike) terms.

## Gotchas
- **Issue:** Single-Reference Limitation → **Fix:** MegaStyle is optimized for one reference image only. For multi-reference style blending, use [[flux-klein-style-lora-system]] or official FLUX.1 Redux.
- **Issue:** VRAM Overhead → **Fix:** The style encoder adds approximately 1 GB of additional memory pressure on top of the already heavy FLUX.1-dev. Use 4-bit or 8-bit quantization for the transformer to fit on 24 GB cards.
- **Issue:** Style-Content Bleeding → **Fix:** If the reference image contains very strong semantic objects, they may bleed into the prompt's content. Adjust LoRA strength or refine the text prompt to reinforce desired subjects.

## See Also
- [[flux-klein-9b-inference]]
- [[flux-klein-style-lora-system]]
- [[diffusion-lora-training]]
- [[flux-attention-manipulation]]
- [[flow-matching]]

