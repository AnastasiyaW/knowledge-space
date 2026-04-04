---
title: Generative Models
category: models
tags: [data-science, deep-learning, gan, vae, diffusion, generative]
---

# Generative Models

Models that learn to generate new data samples from a learned distribution. From GANs to diffusion models - the technology behind image generation, style transfer, and data augmentation.

## GANs (Generative Adversarial Networks)

Two networks competing:
- **Generator** G: creates fake samples from random noise
- **Discriminator** D: distinguishes real from fake

Training: D tries to correctly classify, G tries to fool D. Adversarial game drives both to improve.

### GAN Variants

| Variant | Key Idea |
|---------|----------|
| **Conditional GAN** | Generator and discriminator conditioned on class label |
| **CycleGAN** | Unpaired image-to-image translation (A->B and B->A) |
| **StyleGAN** | Style-based generator for high-quality face synthesis |
| **Pix2Pix** | Paired image-to-image translation |

### CycleGAN
Learns bidirectional mapping without paired data. Applications: age progression, style transfer, domain adaptation.

### GAN Challenges
- **Mode collapse**: generator produces limited variety
- **Training instability**: oscillations, failure to converge
- **Catastrophic forgetting**: learning new categories erases old ones
  - **Fix**: Generative Replay (replay old generated samples during training)
  - **Fix**: EWC (Elastic Weight Consolidation) - penalize changes to important weights

## VAE (Variational Autoencoder)

Encoder maps input to latent distribution (mean + variance), sample from it, decoder reconstructs.

**Loss** = reconstruction loss + KL divergence (keeps latent space close to N(0,1))

**Advantages over GAN**: stable training, smooth latent space interpolation, explicit density model.
**Disadvantage**: outputs tend to be blurrier than GANs.

## Diffusion Models

Iteratively denoise from pure Gaussian noise to generate samples. Current state-of-the-art for image quality.

**Forward process**: gradually add noise to data over T steps.
**Reverse process**: learn to denoise at each step. Neural network predicts noise to subtract.

**Key models**: DDPM, Stable Diffusion, DALL-E, Midjourney.

**Advantages**: superior sample quality, stable training, flexible conditioning.
**Disadvantage**: slow generation (many denoising steps), though distillation methods help.

## 3D Generative

- **NeRF** (Neural Radiance Fields): learn 3D scene from 2D images, render novel views
- **Point cloud generation**: PointNet-based generative models
- **3D-aware GANs**: generate 3D-consistent images

## Neural Style Transfer

Combines content from one image with artistic style from another. Uses pre-trained CNN feature representations at different layers.

**Three components:**
- **Content image (C)**: the photo to transform
- **Style image (S)**: the artistic reference (e.g., Van Gogh's Starry Night)
- **Generated image (G)**: output combining C's structure with S's style

**How it works:**
1. Extract features from a pre-trained CNN (VGG-19) at multiple layers
2. **Content loss**: difference between C and G features at deeper layers (captures structure/objects)
3. **Style loss**: difference between Gram matrices of S and G features at multiple layers (captures textures/patterns/colors)
4. **Total loss**: weighted sum of content and style loss
5. Optimize G by gradient descent on the pixel values

Shallow CNN layers capture edges, textures, colors. Deeper layers capture objects, faces, composition. Style transfer exploits this hierarchy: match shallow-layer statistics (style) while preserving deep-layer activations (content).

## Applications

- **Image generation**: faces, art, product images
- **Data augmentation**: generate training samples for rare classes
- **Neural style transfer**: apply artistic style to photos using CNN features
- **Super-resolution**: upscale low-resolution images
- **Inpainting**: fill missing regions in images
- **Text-to-image**: generate images from text descriptions

## Gotchas
- GAN training requires careful hyperparameter tuning and monitoring
- Generated images can contain artifacts (extra fingers, text distortion)
- Evaluation is hard - FID score is standard but imperfect
- Copyright and ethical concerns with training data
- Diffusion models need significant GPU memory and time for generation

## See Also
- [[cnn-computer-vision]] - CNN architectures used in generators
- [[neural-networks]] - training fundamentals
- [[transfer-learning]] - fine-tuning generative models
