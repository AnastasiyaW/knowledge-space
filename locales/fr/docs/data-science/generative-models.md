---
title: "Modèles génératifs"
category: models
tags: [data-science, deep-learning, gan, vae, diffusion, generative]
level: 3
source_sha256: f109a08824da676068f55792ab405de3cf38a3f4581972e04d6041510fc88f23
translation: machine
translated_at: '2026-10-24'
---
# Modèles génératifs {#generative-models}

Modèles qui apprennent à générer de nouveaux échantillons de données à partir d'une distribution apprise. Des GAN aux modèles de diffusion, ils sous-tendent la génération d'images, le transfert de style et l'augmentation de données.

## GAN (Generative Adversarial Networks) {#gans-generative-adversarial-networks}

Deux réseaux en compétition :
- **Générateur** G : crée de faux échantillons à partir de bruit aléatoire
- **Discriminateur** D : distingue les vrais des faux

Entraînement : D cherche à classer correctement, G cherche à tromper D. Ce jeu adversarial pousse les deux à s'améliorer.

### Variantes de GAN {#gan-variants}

| Variante | Idée clé |
|---------|----------|
| **Conditional GAN** | Générateur et discriminateur conditionnés par une étiquette de classe |
| **CycleGAN** | Traduction d'images non appariées (A->B et B->A) |
| **StyleGAN** | Générateur basé sur le style pour la synthèse de visages de haute qualité |
| **Pix2Pix** | Traduction d'images appariées |

### CycleGAN {#cyclegan}
Apprend une correspondance bidirectionnelle sans données appariées. Applications : vieillissement de visages, transfert de style, adaptation de domaine.

### Défis des GAN {#gan-challenges}
- **Mode collapse** : le générateur produit une variété limitée
- **Instabilité de l'entraînement** : oscillations, échec de convergence
- **Oubli catastrophique** : l'apprentissage de nouvelles catégories efface les anciennes
  - **Solution** : Generative Replay (rejouer d'anciens échantillons générés pendant l'entraînement)
  - **Solution** : EWC (Elastic Weight Consolidation) - pénaliser les modifications des poids importants

## VAE (Variational Autoencoder) {#vae-variational-autoencoder}

L'encodeur associe l'entrée à une distribution latente (moyenne + variance), on échantillonne à partir de celle-ci, puis le décodeur reconstruit l'entrée.

**Perte** = perte de reconstruction + divergence KL (maintient l'espace latent proche de N(0,1))

**Avantages par rapport aux GAN** : entraînement stable, interpolation fluide dans l'espace latent, modèle de densité explicite.
**Inconvénient** : les sorties tendent à être plus floues que celles des GAN.

## Modèles de diffusion {#diffusion-models}

Débruitage itératif à partir d'un bruit gaussien pur pour générer des échantillons. État de l'art actuel en matière de qualité d'image.

**Processus direct** : ajout progressif de bruit aux données sur T étapes.
**Processus inverse** : apprentissage du débruitage à chaque étape. Le réseau de neurones prédit le bruit à soustraire.

**Modèles clés** : DDPM, Stable Diffusion, DALL-E, Midjourney.

**Avantages** : qualité d'échantillon supérieure, entraînement stable, conditionnement flexible.
**Inconvénient** : génération lente (nombreuses étapes de débruitage), bien que les méthodes de distillation aident.

## Génératifs 3D {#3d-generative}

- **NeRF** (Neural Radiance Fields) : apprend une scène 3D à partir d'images 2D et rend de nouvelles vues
- **Génération de nuages de points** : modèles génératifs basés sur PointNet
- **GAN sensibles à la 3D** : génèrent des images cohérentes en 3D

## Transfert de style neuronal {#neural-style-transfer}

Combine le contenu d'une image avec le style artistique d'une autre. Utilise les représentations de caractéristiques d'un CNN pré-entraîné à différentes couches.

**Trois composantes :**
- **Image de contenu (C)** : la photo à transformer
- **Image de style (S)** : la référence artistique (par exemple, *La Nuit étoilée* de Van Gogh)
- **Image générée (G)** : sortie combinant la structure de C avec le style de S

**Fonctionnement :**
1. Extraire les caractéristiques d'un CNN pré-entraîné (VGG-19) à plusieurs couches
2. **Perte de contenu** : différence entre les caractéristiques de C et de G dans les couches profondes (capture la structure et les objets)
3. **Perte de style** : différence entre les matrices de Gram de S et de G à plusieurs couches (capture les textures, motifs et couleurs)
4. **Perte totale** : somme pondérée des pertes de contenu et de style
5. Optimiser G par descente de gradient sur les valeurs des pixels

Les couches CNN peu profondes capturent les contours, textures et couleurs. Les couches plus profondes capturent les objets, les visages et la composition. Le transfert de style exploite cette hiérarchie : il fait correspondre les statistiques des couches superficielles (style) tout en préservant les activations des couches profondes (contenu).

## Applications {#applications}

- **Génération d'images** : visages, art, images de produits
- **Augmentation de données** : génération d'échantillons d'entraînement pour les classes rares
- **Transfert de style neuronal** : appliquer un style artistique à des photos à l'aide de caractéristiques CNN
- **Super-résolution** : agrandissement d'images basse résolution
- **Inpainting** : remplissage des zones manquantes dans les images
- **Text-to-image** : génération d'images à partir de descriptions textuelles

## Pièges à éviter {#gotchas}
- L'entraînement des GAN demande un réglage minutieux des hyperparamètres et un suivi attentif
- Les images générées peuvent contenir des artefacts (doigts superflus, déformation du texte)
- L'évaluation est difficile : le score FID est la référence, mais reste imparfait
- Questions de droit d'auteur et d'éthique concernant les données d'entraînement
- Les modèles de diffusion nécessitent beaucoup de mémoire GPU et de temps pour la génération

## Voir aussi {#see-also}
- [[cnn-computer-vision]] - architectures CNN utilisées dans les générateurs
- [[neural-networks]] - fondamentaux de l'entraînement
- [[transfer-learning]] - affinage des modèles génératifs
