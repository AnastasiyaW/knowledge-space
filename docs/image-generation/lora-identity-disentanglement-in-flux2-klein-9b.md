# LoRA Identity Disentanglement in FLUX.2 Klein 9B

Identity LoRA training often suffers from concept bleeding, where environmental factors (lighting, background, clothing) are baked into the character subspace. Disentanglement strategies isolate identity-specific weights through block-selective training, loss-based regularization, or post-hoc weight surgery.

## Model Architecture and Target Modules
FLUX.2 Klein 9B utilizes a Rectified Flow Transformer (MMDiT) architecture with 57 total transformer blocks (19 double blocks, 39 single blocks).

- **Double Blocks:** Handle joint text and image attention.
- **Single Blocks:** Process image-only features.
- **Target Modules:** Most implementations target `to_q`, `to_k`, `to_v`, and `to_out.0` within both block types. For editing-specific tasks, projection layers for image input (`img_in`) are also tuned.
- **Text Encoder:** Typically uses a frozen 8B Qwen3 embedder.

## Training-Time Disentanglement

### B-LoRA Block Selection
Implicit style-content separation is achieved by restricting training to specific blocks. In SDXL, blocks 4 and 5 are identified as content and style specialized. In Klein 9B, empirical evidence suggests single block 7 is a high-leverage target for identity, though a full sweep of the 57 blocks is required to identify the exact "identity blocks" equivalent.

### Disentanglement Loss (Concept Sliders)
Training with a disentangled loss [2311.12092] forces the model to modify noise prediction in a specific direction (identity) while explicitly subtracting unwanted entangled attributes. 
- **Method:** Define a positive prompt (the person) and a negative prompt ("different background, different lighting, different outfit").
- **Effect:** Prevents the LoRA from memorizing the specific environment of the training set.

### Orthogonal Adaptation
Forces orthogonality between subspaces during training [2403.14572]. This prevents "crosstalk" when merging multiple LoRAs, ensuring that the identity subspace does not overlap with style or background subspaces.

## Post-Training Surgery

### SVD Rank Reduction
Applying Singular Value Decomposition (SVD) to a trained LoRA and truncating the tail singular values acts as a denoiser. Identity signal typically concentrates in the top-k singular values, while environmental noise and overfitting artifacts reside in lower-energy components.

```bash
python resize_lora.py \
    --model_path "path/to/identity_lora.safetensors" \
    --new_rank 8 \
    --dynamic_method sv_ratio \
    --dynamic_param 0.8 \
    --save_to "path/to/disentangled_lora.safetensors"
```

### DARE and TIES Merging
Drop And Rescale (DARE) randomly zeros 80-90% of delta-parameters and rescales the remaining weights. This reduces redundancy and memorization of background pixels while preserving the core identity concept.

### LoRA Subtraction
Arithmetic subtraction can isolate identity if a "background-only" LoRA is available.
- **Formula:** `W_identity = W_full_person - (alpha * W_background_only)`
- **Implementation:** Train a LoRA on the same dataset with faces masked out, then subtract it from the original person LoRA.

## Hierarchy of Implementation
1. **Inference Ablation:** Sweep block weights (0.0 to 1.0) per-block to identify which of the 57 Klein 9B blocks destroy identity when disabled.
2. **SVD Truncation:** Resize existing LoRAs to rank 4 or 8 using `sv_ratio` to drop overfitting noise.
3. **Selective Training:** Train only on suspected "identity blocks" (e.g., middle double blocks 8-12) to minimize environment capture.

## Gotchas
- **Issue:** DiT vs U-Net Symmetry → **Fix:** Unlike SDXL, Klein 9B uses a DiT architecture without IN/OUT pairing; block-weight extensions designed for SD1.5/SDXL (like `sd-webui-lora-block-weight`) require DiT-aware logic mapping to the 19 double and 39 single blocks.
- **Issue:** Rank Reduction Over-Pruning → **Fix:** Truncating LoRA rank too aggressively (e.g., below rank 4) often preserves the face shape but loses skin texture and iris detail. Use `sv_ratio` rather than fixed rank.
- **Issue:** Background Subtraction Color Shifts → **Fix:** Simple arithmetic subtraction of background LoRAs often causes global gamma or color temperature shifts. Use Concept Sliders' disentanglement loss during training for more stable results.

## See Also
- [[flux-klein-9b-architecture]]
- [[flux-klein-character-lora]]
- [[diffusion-lora-training]]
- [[flux-attention-manipulation]]
- [[frequency-decomposition-editing]]

