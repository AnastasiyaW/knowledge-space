---
title: Style Reference UX Patterns
category: product
tags: [ux, style-reference, midjourney, ideogram, firefly, product-design, style-transfer, lora]
---

# Style Reference UX Patterns

Comparative analysis of style reference workflows across major AI image generation products. Reference for product design decisions around style input, strength control, browsing, and persistence.

## Style Input Methods

Ranked by user effort required:

| Method | Product | Effort | Reusability |
|--------|---------|--------|-------------|
| Preset library pick | All products | One click | Infinite |
| Single image upload | All products | Drag-drop | Per session |
| Numeric code paste | Midjourney | Copy-paste | Infinite |
| Multi-image upload (1-3) | Ideogram, Krea, Firefly | 2-3 uploads | Per session or saved |
| Binary image rating | Midjourney Personalization | 15-20 min, 200 pairs | Infinite (profile) |
| Grid selection from generated options | Midjourney Style Creator | 5-10 min | Infinite (code) |
| LoRA training (5-35 images) | Freepik | 15-30 min training | Infinite |
| Real-time canvas drawing | Krea.ai | Continuous | Per session |

## Midjourney --sref Deep Dive

**Five creation methods:**
1. Image URL: `--sref <url>` in Discord, paperclip icon in web app
2. Numeric code: `--sref 2213253170` (billions of internal styles)
3. `--sref random`: discover style, reveals code post-generation
4. Style Creator: grid selection → generates unique code
5. Moodboard: `--profile <id>` named image collections

**Style strength:** `--sw 0-1000`, default 100. Community-found optimal: 65-175.

**Multi-style blending:** `--sref code1::2 code2::1` - proportional weighting (only ratios matter).

**Benchmark grids:** 16 creative domains shown with same sref code. Reveals style's range across character, fashion, portraiture, technical drawing, etc.

Community ecosystem spawned: Midlibrary.io, SrefHunt.com (50K+ codes), sref-midjourney.com, PromptsRef.com. All follow: grid cards + one-click copy + category filters + personal bookmarks.

## Strength/Influence Control Patterns

| Pattern | Products | Notes |
|---------|---------|-------|
| Numeric parameter in text (`--sw 0-1000`) | Midjourney | Power users, precise |
| Named levels (Low/Mid/High/Ultra/Max) | Leonardo.ai | Approachable, limited precision |
| Continuous slider | Adobe Firefly, Freepik | Standard UI pattern |
| Named flavors (Faithful/Bold/Dreamy) | Freepik Mystic | Qualitative, intuitive |
| Drag gesture on image | Krea.ai | Direct manipulation |
| Proportional weights (`::2 ::1`) | Midjourney blending | Proportional, power users |

## Style vs Structure Separation

**Adobe Firefly**: two distinct sliders:
- **Style Strength**: how closely output follows the style reference
- **Visual Intensity**: detail/drama of base image before style application

**Structure Reference** (Firefly) is separate from Style Reference: controls outline and depth matching. Can use both independently.

**Leonardo.ai**: same image can be Content Reference OR Style Reference. Clear mental model:
- Content Reference = WHAT is in the image (subjects, composition)
- Style Reference = HOW it looks (colors, artistic style, texture)

## Persistence and Sharing

| Mechanism | Product | Notes |
|-----------|---------|-------|
| Numeric code (portable, shareable) | Midjourney | Single number = entire aesthetic. Most viral. |
| Named saved style (account-bound) | Ideogram, Freepik | Personal library |
| Moodboard with ID | Midjourney | Curated collection, shareable |
| Trained LoRA (account-bound) | Freepik | Highest commitment, highest quality |
| Profile from ratings | Midjourney | Implicit style from preference history |

## Key UX Insights

**1. Numeric codes are the most viral mechanism.** Midjourney's single-number encoding spawned an entire third-party ecosystem. A portable, copy-pasteable aesthetic identifier creates sharing loops that no gallery can match.

**2. Two-tier commitment works.** Ideogram's "Quick Reference" (temporary) vs "My Styles" (permanent named) pattern serves exploration and production simultaneously. Key: frictionless experimentation, clear path to commitment.

**3. `--sref random` as discovery mechanic.** Generate → discover → save code → build collection. Turns randomness into curation. Creates addictive collecting behavior without explicit gamification.

**4. Named qualitative modes beat numeric sliders for non-power-users.** Freepik's "Faithful/Bold/Dreamy" flavors and Leonardo's "Low/Mid/High/Ultra/Max" are more actionable than 0-1000 scales for users who think in qualities.

**5. Benchmark grids show style versatility.** 16 variations of one style across different subjects is more informative than 4 variations of the same subject. Reveals style's range and limitations.

**6. LoRA training exposed to end users is a UX barrier AND moat.** Freepik's 15-30 min wait creates investment/commitment. Users who trained a custom style don't switch platforms.

**7. Real-time feedback (Krea, <50ms) changes the paradigm.** From "configure then generate" to "continuously sculpt." Fundamentally different interaction model.

**8. Style + Character as independent axes.** Freepik's separate trainable entities that combine freely is powerful for brand content (same character, multiple styles or vice versa).

## Ideogram Pattern: Immutable Custom Styles

Reference images in Ideogram's custom styles cannot be changed after creation. Forces intentional curation - you commit to a style before training it. UX trade-off: more friction upfront, cleaner library management.

**Quick Reference** tab: temporary style for experimenting (no naming, no saving required). Permanent "My Styles" for production use.

## Runway Aleph: Post-Generation Style

Post-generation style transfer via text prompts without regenerating from scratch. Apply style AFTER generation → non-destructive workflow. Currently only for video.

Implication for product design: style can be a post-processing step, not just a generation parameter.

## Implementation Notes for Custom LoRA Systems

For a LoRA-based style system (like Freepik's):

```
Recommended: rank32, 1000 steps, cosine scheduler
Dataset: 5-50 images, trigger_word + content captions (no style descriptors)
Caption dropout: 0.1 (forces style into LoRA weights)
Inference: Gemini-based prompt reformulation to weave style into scene description
```

**Dataset size → quality:**
| Refs | Quality | Steps |
|------|---------|-------|
| 1-3 | Poor | N/A |
| 5-7 | Marginal | 1500 |
| 10-15 | Good | 1000 |
| 30+ | Excellent | 500 |

**Gemini two-level approach for style injection:**
- L1 (Style Extraction): analyze reference images → style profile with MUST/ENRICH elements
- L2 (Prompt Reformulation): weave style profile + user prompt naturally, resolve conflicts (style wins on visuals, user wins on subject/action)

## Gotchas

- **Building style browsing into the product is critical**: the explosion of third-party sref sites shows unmet demand. Users want to discover styles they haven't seen, not just apply ones they already know.
- **LoRA at rank128 on small datasets (<10 images) overfit after ~500 steps**: rank32 is more robust for small datasets. Use rank128 only with 30+ reference images.
- **Cosine scheduler causes "jumps" at midpoint in LoRA training**: if LR is still high when scheduler reaches midpoint, model can overshoot and produce inconsistent checkpoints. Use linear warm-down or check-at-500-steps pattern.
- **Content leakage with small/homogeneous datasets**: a 2-image style dataset that both contain the same person → LoRA learns the person, not the style. Need content diversity within style consistency.

## See Also

- [[Diffusion LoRA Training]] - training style LoRAs
- [[flux-klein-style-lora-system]] - full style system architecture
- [[FLUX Klein 9B Inference]] - LoRA stacking at inference
