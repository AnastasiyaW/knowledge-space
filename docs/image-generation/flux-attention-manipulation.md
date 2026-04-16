---
title: FLUX MMDiT Attention Manipulation
category: techniques
tags: [flux, mmdit, attention, regional-prompting, compositional-generation, visualization, anatomy]
---

# FLUX MMDiT Attention Manipulation

Techniques for manipulating, analyzing, and exploiting the joint self-attention mechanism in FLUX/MMDiT for regional prompting, compositional generation, and semantic control.

## MMDiT Joint Attention Structure

FLUX uses a joint self-attention over concatenated image and text tokens. The attention matrix has 4 quadrants:

| Quadrant | Role |
|----------|------|
| I2I (image→image) | Spatial coherence, structure |
| I2T (image→text) | Text conditions image regions |
| T2I (text→image) | Image regions affect text interpretation |
| T2T (text→text) | Text self-coherence |

**Key for manipulation:** I2I quadrant dominates spatial layout. Masking or biasing specific quadrants lets you decouple style from content, isolate regions, or inject custom guidance.

FreeFlux block analysis (23 of 38 blocks): early blocks handle low-level texture/style, late blocks govern high-level layout and semantics. Layer 19 onward = layout-critical.

## Regional Prompting (instantX)

Regional-Prompting-FLUX: assigns different text prompts to spatial regions by masking the I2T attention quadrant.

```python
# ComfyUI node: Regional Conditioning
# Each region gets its own prompt
# Attention mask prevents cross-region contamination

regions = [
    {"mask": top_half_mask, "prompt": "blue sky with clouds"},
    {"mask": bottom_half_mask, "prompt": "green meadow with flowers"}
]
```

Use `base_ratio` to blend regional and global conditioning. Higher base_ratio = more global coherence, lower = sharper region boundaries. Typical range: 0.3-0.7.

## Stitch: Two-Phase Compositional Generation

Stitch (Feb 2025) generates complex scenes by splitting into individual subjects then compositing via attention.

**Pipeline:**
1. Generate each subject independently with clean background
2. Extract attention maps for each subject
3. Composite via attention injection into joint generation

**Results**: >200% improvement on GenEval compositional benchmarks. Outperforms most FLUX-based methods on attribute binding (assigning correct attributes to correct subjects).

**Why it works**: FLUX's I2T attention is used to "plant" subject features at target positions in the joint attention space.

## Attention Temperature Scaling (TACA)

Temperature Aware Concept Alignment: scale the softmax temperature in cross-attention to control concept-token binding strength.

```python
# Higher temperature = softer attention = more distributed concept binding
# Lower temperature = sharper = more precise localization
# TACA learns per-concept temperature via a small MLP

scaled_attn = torch.softmax(attn_weights / temperature_scale, dim=-1)
```

Useful for: attribute binding (red apple + blue car), object counting, spatial layout compliance.

## ConceptAttention (ICML 2025)

Extracts semantic saliency maps from FLUX attention for interpretability and control.

```python
# Hook onto attention layers
from concept_attention import ConceptAttentionPipeline

pipe = ConceptAttentionPipeline.from_pretrained("black-forest-labs/FLUX.1-dev")
output = pipe(
    prompt="a red apple on a wooden table",
    concepts=["apple", "table", "background"],
    return_attention_maps=True
)
# output.attention_maps: {concept: spatial_heatmap}
```

**Applications:**
- Semantic segmentation without training
- Region-specific editing masks from text
- Understanding why FLUX placed elements where it did
- Input for downstream inpainting/editing

Aperture (2025): related visualization tool for FLUX layer-by-layer attention inspection. Interactive UI shows which prompt tokens activate which image regions at each layer.

## FluxSpace: Feature-Space Editing

Edit images via intermediate feature injection. Extract features from a source image at specific layers, then inject modified features during generation of a target image.

```python
# 1. Forward pass source through FLUX, save intermediate activations
# 2. Apply editing operation in feature space (interpolation, direction shift)
# 3. Generate target with injected features at same layers
# Layer range 15-25 = good balance of content/style preservation
```

Differs from LoRA: no training, pure inference-time manipulation. Suitable for style transfer, structure-preserving edits, attribute manipulation.

## NUMINA: Object Counting Accuracy (CVPR 2026)

Additive attention bias injection for accurate object counting in Wan2.1 and adaptable to FLUX/MMDiT.

**Architecture (two-phase):**

**Phase 1 - Layout Construction:**
```python
# MeanShift + DBSCAN clustering on text tokens
# Builds spatial layout: where should N copies of object be placed?
layout = construct_layout(prompt, target_count=N)  
# Returns: list of (center_x, center_y, radius) tuples
```

**Phase 2 - Attention Bias Injection:**
```python
# Additive pre-softmax bias (not multiplicative)
# Delta(t) modulation: bias stronger at early timesteps, fade to zero
delta_t = 1.0 - (t / T_max)  # decreases over denoising
bias = delta_t * spatial_layout_bias  # [H, W] -> added to attn_weights

attn_weights = attn_weights + bias  # pre-softmax addition
attn = softmax(attn_weights)
```

**FLUX adaptation feasibility (HIGH):** FLUX's cross-attention handles text→image injection. Replace Wan's temporal attention with FLUX's image-text cross-attention. Same MeanShift+DBSCAN layout works. Main challenge: FLUX's MMDiT is natively joint, Wan treats them separately.

## HandCraft / RHanDS: Attention-Based Anatomy Correction

Post-generation approaches that use attention manipulation for correct hand anatomy.

**HandCraft (WACV 2025):** uses MANO parametric hand model to generate conditioning depth maps, then ControlNet-conditions an inpainting pass.

**RHanDS (AAAI 2025):** decoupled structure + style guidance in attention space:
- Structure path: hand mesh depth → structure conditioning branch
- Style path: malformed hand itself → style preservation branch
- Merge: attention-level fusion, not image-level

Result: preserves original skin tone and lighting better than HandRefiner because it operates in attention space, not pixel space.

## Practical Implementations

### ComfyUI Nodes

| Node | Purpose | GitHub |
|------|---------|--------|
| Regional-Prompting-FLUX | Region-specific prompts via attention masks | instantX-research |
| ComfyUI-NAG | Normalized Attention Guidance (negative guidance) | ChenDarYen/ComfyUI-NAG |
| ComfyUI_Flux2Klein-Enhancer | Boost prompt adherence via embedding scaling | capitan01R |
| ComfyUI-Impact-Pack | FaceDetailer/DetailerForEach for anatomy post-processing | ltdrdata |

### Layer Targeting for Editing

```python
# FLUX block analysis for targeted LoRA training
# Skip content blocks (20-29) → train ONLY style blocks (30-57)
# SplitFlux approach: 30% faster training, better style/content separation

split_flux_target_blocks = list(range(30, 57))  # style layers only
```

## Gotchas

- **Regional prompting quality depends on region mask precision**: soft/blurred masks cause concept bleed. Binary masks with hard edges work better for FLUX's attention structure.
- **ConceptAttention returns layer-averaged maps**: individual layer maps vary significantly. Inspect layer 20-30 for semantic content, layers 1-10 for low-level texture.
- **TACA temperature too low causes oversaturation**: temperature < 0.5 makes cross-attention too sharp, object outlines become cartoonish. Start at 1.0 and tune down.
- **Stitch's two-phase approach doubles generation time**: each subject requires a full forward pass. For >3 subjects, generation time scales linearly.
- **NUMINA layout construction fails on abstract counting** ("a dozen roses", "many birds"): MeanShift+DBSCAN needs a specific integer target count for reliable layout.

## See Also

- [[MMDiT]] - transformer architecture details
- [[flux-klein-9b-inference]] - inference settings
- [[anatomy-correction-diffusion]] - full anatomy fix pipeline
- [[diffusion-lora-training]] - layer targeting for LoRA
- [[object-removal-inpainting]] - region-aware inpainting approaches
