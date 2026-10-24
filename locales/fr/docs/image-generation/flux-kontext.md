---
title: "FLUX Kontext"
category: models
tags: [image-editing, flux, bfl, dit, flow-matching, sequence-concatenation, character-consistency, multi-turn, non-commercial-dev]
aliases: ["FLUX.1-Kontext-dev", "Kontext"]
level: 2
source_sha256: fea0e789c9b4e32c721e4938e5d018bbc1e0f1c35924e00292b51b852b10fee4
translation: machine
translated_at: '2026-10-24'
---
# FLUX Kontext {#flux-kontext}

Modèle d'édition d'images de Black Forest Labs (BFL). Il étend l'architecture FLUX.1 avec une **concaténation de séquences** pour le conditionnement par images de contexte. Il est le meilleur de sa catégorie pour l'édition de texte, la cohérence des personnages et l'édition multi-tours.

Article : arXiv:2506.15742 (juin 2025).

## Architecture {#architecture}

Même DiT de 12B que FLUX.1-dev :
- 19 blocs à flux double (poids séparés pour l'image et le texte, attention conjointe)
- 38 blocs à flux unique (FFN fusionné)
- Dimension cachée : 3072, têtes : 24, VAE latent à 16 canaux
- Texte : CLIP (768d) + T5 (4096d)

### Innovation clé : concaténation de séquences {#key-innovation-sequence-concatenation}

Les images de contexte sont encodées par le VAE de FLUX → les tokens latents sont **ajoutés à la suite des tokens de l'image cible** dans le flux visuel :
```text
Target tokens:  position (0, h, w)
Context image:  position (1, h, w)   ← "virtual timestep" via 3D RoPE
Context image 2: position (2, h, w)  ← architecturally supported, not yet released
```

**La concaténation par canaux a été testée et a donné de moins bons résultats.** La concaténation de séquences préserve la résolution et le rapport d'aspect indépendants pour l'entrée et la sortie.

Lorsque le contexte est vide, le modèle revient à la génération pure texte-vers-image.

### vs [[Step1X-Edit]] {#vs-step1x-edit}

| Aspect | FLUX Kontext | Step1X-Edit / Qwen-Edit |
|--------|-------------|------------------------|
| Base | FLUX.1 12B DiT | MMDiT personnalisé |
| Encodeur de texte | CLIP + T5 | Qwen 2.5 VL (vision-langage) |
| Conditionnement | Concaténation de séquences (tokens latents) | Attention conjointe (image + texte) |
| Support des masques | Pas de masque explicite (piloté par le texte) | Le pipeline DiffSynth prend en charge les masques |
| Vitesse | 3-5 s en 1024×1024 | Plus lent (~40 Go de VRAM) |

## Variantes {#variants}

| Variante | Accès | Licence |
|---------|--------|---------|
| Kontext [dev] | Poids ouverts (HF) | **Non commerciale** (licence BFL dev) |
| Kontext [pro] | API uniquement | Commerciale via BFL |
| Kontext [max] | API uniquement | Commerciale via BFL |

**Dev ne fait que de l'I2I** (pas de T2I). Le T2I n'est disponible que dans pro/max.

## Entraînement {#training}

- Part du checkpoint T2I de FLUX.1
- Fine-tuning conjoint sur I2I + T2I avec la fonction de perte rectified flow
- Données : des millions de paires relationnelles (non divulguées)
- FSDP2, Flash Attention 3, activation checkpointing sélectif

## VRAM {#vram}

~24 Go minimum (transformeur en bf16). Pipeline complet : ~32-40 Go. Des quantifications FP8/FP4 sont disponibles pour les GPU de 24 Go.

## Points d'attention {#gotchas}

- **Modifie l'image entière**, et pas seulement la zone éditée. Utilisez le nœud flux-kontext-diff-merge pour une fusion sélective, basée sur la détection dans l'espace colorimétrique LAB et sur le Poisson blending
- L'édition multi-tours se dégrade après environ 6 itérations
- Le modèle dev présente des artefacts de distillation
- Licence non commerciale pour les poids ouverts : un usage commercial nécessite une licence BFL
- Le développement de [ACE++](ACE++.md) sur la base FLUX a été **suspendu** en raison de l'instabilité de l'entraînement

## Liens utiles {#key-links}

- GitHub : github.com/black-forest-labs/flux
- HF : huggingface.co/black-forest-labs/FLUX.1-Kontext-dev
- Diff-merge : github.com/safzanpirani/flux-kontext-diff-merge
