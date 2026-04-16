---
title: Textual Latent Interpolation
category: techniques
tags: [interpolation, text-embeddings, continuous-control, expression-editing, latent-arithmetic, zero-shot]
---

# Textual Latent Interpolation

Technique for continuous attribute control in diffusion models by interpolating between text embeddings. Enables smooth transitions between states (e.g., neutral → happy) with an intensity parameter alpha. Core mechanism behind [[PixelSmile]]'s expression control.

## Principle

Same idea as word2vec arithmetic ("king - man + woman = queen") but in the text embedding space of a diffusion model's text encoder.

```python
# Direction vector in embedding space
e_neutral = text_encoder("neutral expression")
e_target  = text_encoder("happy expression")
delta = e_target - e_neutral

# Controlled generation at any intensity
e_conditioned = e_neutral + alpha * delta
# alpha=0 → neutral, alpha=1 → full expression, alpha>1 → exaggerated
```

## Implementation Strategies

### Strategy 1: All-token interpolation (PixelSmile default)

Interpolate across ALL token positions in the embedding sequence. Simplest, works when prompts differ only in the attribute word.

```python
# score_one_all method
e_cond = (1 - alpha) * e_neutral + alpha * e_target
# Equivalent to: e_neutral + alpha * (e_target - e_neutral)
```

### Strategy 2: Tail-token interpolation

Only interpolate the last N tokens (where the attribute-specific words are). Preserves the shared context tokens exactly.

```python
# Interpolate only last 6-7 tokens
e_cond = e_neutral.clone()
e_cond[:, -7:, :] = (1 - alpha) * e_neutral[:, -7:, :] + alpha * e_target[:, -7:, :]
```

### Strategy 3: Direction projection

Compute the delta, project it to a subspace, apply scaled:

```python
delta = e_target - e_neutral
delta_norm = delta / delta.norm()  # unit direction
e_cond = e_neutral + alpha * magnitude * delta_norm
```

## Multi-Attribute Blending

Extend to pairwise combinations (PixelSmile's expression blending):

```python
e_angry = text_encoder("angry expression")
e_sad   = text_encoder("sad expression")
e_neutral = text_encoder("neutral expression")

delta_angry = e_angry - e_neutral
delta_sad   = e_sad - e_neutral

# Blend two emotions at different intensities
e_cond = e_neutral + 0.7 * delta_angry + 0.5 * delta_sad
```

9 of 15 basic-expression pairs produce plausible results. Failures when attributes are physiologically contradictory (conflicting muscle states).

## Requirements

1. **Aligned embedding space**: the text encoder must produce embeddings where linear interpolation is semantically meaningful. VLM-based encoders (**Qwen 2.5 VL**) work better than CLIP for this.

2. **LoRA training with the technique**: the model must be trained to respond to interpolated embeddings. PixelSmile explicitly trains with varied alpha values — the model learns that intermediate embeddings mean intermediate expressions.

3. **Prompt structure**: neutral and target prompts should be identical except for the controlled attribute. Keeps the delta clean.

## Applications Beyond Expressions

The technique generalizes to any attribute controllable via text:

| Application | Neutral Prompt | Target Prompt | Alpha Controls |
|-------------|---------------|---------------|----------------|
| Expression | "neutral expression" | "happy expression" | Smile intensity |
| Age | "young person" | "elderly person" | Apparent age |
| Lighting | "normal lighting" | "dramatic lighting" | Light intensity |
| Style | "photograph" | "oil painting" | Stylization degree |
| Weather | "clear sky" | "heavy rain" | Rain intensity |

## Relation to Other Techniques

| Technique | Mechanism | Granularity | Training Required |
|-----------|-----------|-------------|-------------------|
| Textual Latent Interpolation | Embedding arithmetic | Continuous | Yes (for best results) |
| Prompt weighting | Token-level scale factors | Discrete steps | No |
| ControlNet | Spatial conditioning | Pixel-level | Yes (dedicated model) |
| IP-Adapter | Image embedding injection | Per-reference | Yes (adapter) |

Key advantage: zero additional parameters at inference (just different conditioning), continuous control, and composable.
