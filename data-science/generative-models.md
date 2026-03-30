---
title: Generative Models
category: deep-learning
tags: [gan, vae, autoencoder, diffusion, generative, pytorch, deep-learning]
---

# Generative Models

Learn to generate new data samples that resemble the training distribution. GANs use adversarial training (generator vs. discriminator); VAEs use variational inference with encoder-decoder; diffusion models iteratively denoise random noise. Foundation of modern image generation, data augmentation, and anomaly detection.

## Key Facts

- **Autoencoder**: encoder compresses input to latent vector, decoder reconstructs; learns compressed representation; not truly generative (latent space not continuous)
- **VAE** (Variational Autoencoder): encoder outputs distribution parameters (mu, sigma), sample from it; regularized latent space enables generation; loss = reconstruction + KL divergence
- **GAN** (Generative Adversarial Network): generator creates fake data, discriminator tries to distinguish real from fake; zero-sum game; when equilibrium reached, generator creates realistic data
- **GAN training instability**: mode collapse (generator produces limited variety), vanishing gradients, oscillating loss; mitigations: WGAN-GP, spectral normalization, progressive growing
- **Conditional GAN (cGAN)**: condition generation on class label or other input; enables controlled generation (pix2pix for image-to-image)
- **Latent space**: compressed representation where each dimension captures a meaningful factor of variation; interpolation in latent space produces smooth transitions
- **Diffusion models**: forward process adds noise step by step; reverse process learns to denoise; currently state-of-the-art for image generation (Stable Diffusion, DALL-E)
- **FID** (Frechet Inception Distance): metric for generated image quality; lower is better; compares feature statistics of real vs generated images
- **Reconstruction loss**: MSE (blurry) or perceptual loss (VGG features, sharper); choice affects output quality
- VAE generates blurrier images than GAN but has stable training and meaningful latent space
- Diffusion models produce highest quality but are slow (many denoising steps); speed improvements: DDIM, distillation, latent diffusion

## Patterns

```python
import torch
import torch.nn as nn

# Simple Autoencoder
class Autoencoder(nn.Module):
    def __init__(self, input_dim=784, latent_dim=32):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.ReLU(),
            nn.Linear(256, input_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)

# VAE
class VAE(nn.Module):
    def __init__(self, input_dim=784, latent_dim=32):
        super().__init__()
        self.encoder = nn.Sequential(nn.Linear(input_dim, 256), nn.ReLU())
        self.fc_mu = nn.Linear(256, latent_dim)
        self.fc_logvar = nn.Linear(256, latent_dim)
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 256), nn.ReLU(),
            nn.Linear(256, input_dim), nn.Sigmoid()
        )

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(self, x):
        h = self.encoder(x)
        mu, logvar = self.fc_mu(h), self.fc_logvar(h)
        z = self.reparameterize(mu, logvar)
        recon = self.decoder(z)
        return recon, mu, logvar

def vae_loss(recon_x, x, mu, logvar):
    recon_loss = nn.functional.binary_cross_entropy(recon_x, x, reduction='sum')
    kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon_loss + kl_loss

# Simple GAN
class Generator(nn.Module):
    def __init__(self, noise_dim=100, output_dim=784):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(noise_dim, 256), nn.ReLU(),
            nn.Linear(256, 512), nn.ReLU(),
            nn.Linear(512, output_dim), nn.Tanh()
        )
    def forward(self, z):
        return self.net(z)

class Discriminator(nn.Module):
    def __init__(self, input_dim=784):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 512), nn.LeakyReLU(0.2),
            nn.Linear(512, 256), nn.LeakyReLU(0.2),
            nn.Linear(256, 1), nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(x)

# GAN training loop (simplified)
G = Generator()
D = Discriminator()
opt_G = torch.optim.Adam(G.parameters(), lr=2e-4, betas=(0.5, 0.999))
opt_D = torch.optim.Adam(D.parameters(), lr=2e-4, betas=(0.5, 0.999))
criterion = nn.BCELoss()

for epoch in range(epochs):
    for real_data in dataloader:
        batch_size = real_data.size(0)
        # Train Discriminator
        z = torch.randn(batch_size, 100)
        fake = G(z).detach()
        d_loss = criterion(D(real_data), torch.ones(batch_size, 1)) + \
                 criterion(D(fake), torch.zeros(batch_size, 1))
        opt_D.zero_grad(); d_loss.backward(); opt_D.step()

        # Train Generator
        z = torch.randn(batch_size, 100)
        g_loss = criterion(D(G(z)), torch.ones(batch_size, 1))
        opt_G.zero_grad(); g_loss.backward(); opt_G.step()
```

## Gotchas

- GAN discriminator loss should stay around 0.5 (roughly even game); if D loss drops to 0, generator gets no useful gradients
- VAE `reparameterize` trick is necessary for backpropagation through sampling; sampling is not differentiable, but reparameterization is
- GAN training: use Adam with betas=(0.5, 0.999), NOT default (0.9, 0.999); train D more often than G (1:1 or 2:1)
- Autoencoder != generative model; interpolating in autoencoder latent space produces artifacts (gaps between training points)
- KL divergence weight in VAE can be annealed: start with beta=0 (reconstruction focus), gradually increase to 1 (regularize latent space)
- FID computation requires at minimum ~10K generated samples for reliable estimate

## See Also

- [[neural-network-fundamentals]] - generator and discriminator are neural networks
- [[convolutional-neural-networks]] - convolutional generators (DCGAN) for image generation
- [[loss-functions-and-regularization]] - adversarial loss, reconstruction loss, KL divergence
- [[probability-distributions]] - VAEs explicitly model data distributions
- PyTorch tutorials (DCGAN): https://pytorch.org/tutorials/beginner/dcgan_faces_tutorial.html
