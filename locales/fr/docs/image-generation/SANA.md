---
title: "SANA"
category: models
tags: [text-to-image, dit, flow-matching, efficient, 1.6b, 600m, 4.8b, linear-attention, dc-ae, litela, mix-ffn, gemma, nvlabs, jewelry-retouching]
aliases: ["SANA 1.5", "SANA 1.6B", "SANA-Sprint", "SANA-Video"]
level: 4
source_sha256: 37c4e864f5e1877975afe4e579cbb97e287f7bd5a274acf785d4ecfa64157b08
translation: machine
translated_at: '2026-10-24'
---
# SANA (Synthèse d'images haute résolution efficace) {#sana-efficient-high-resolution-image-synthesis}

DiT efficace issu de NVlabs/MIT Han Lab. De 600M à 4,8B de paramètres, avec une qualité compétitive de 1024 à 4096 px. Utilise l'**attention linéaire O(n)**, une compression **DC-AE 32×** et l'encodeur de texte **Gemma-2-2B**. ICLR 2025 Oral.

## État actuel (vérifié le 2026-08-27) {#current-status-verified-2026-08-27}

Le nom SANA couvre désormais plusieurs branches apparentées mais non interchangeables. Identifiez l'artefact concerné avant d'appliquer des affirmations sur les performances, la mémoire ou la licence.

| Branche | État actuel de l'artefact | Usage prévu |
|---|---|---|
| SANA / SANA 1.5 / Sprint | Code de génération d'images et checkpoints publiés | Génération texte-vers-image et raffinement d'images |
| SANA-Video (2025) | Implémentation de recherche publiée ; intégration Diffusers ensuite | Génération vidéo causale antérieure |
| SANA-WM (2026) | Branche de modèle du monde de 2,6B publiée | Simulation interactive/monde en 720p, jusqu'à une minute, contrôle 6-DoF |
| SANA-Video2 (2026) | Code d'entraînement et d'inférence, et checkpoint **5B 720p publié le 2026-08-19** | Génération vidéo 720p actuelle |
| SANA-Video2 14B | Architecture/configuration évoquées, mais aucun checkpoint 14B dans le dépôt officiel | Référence de recherche uniquement ; ne pas choisir pour une recette exécutable |

Le rapport du 4 août 2026 indiquant que Video2 n'avait pas de poids publics était exact à l'époque ; il est désormais **remplacé** pour le modèle 5B. Il reste exact pour le checkpoint 14B à la date de cette vérification.

La page officielle de Video2 rapporte un benchmark de 5 secondes, 720p, 40 étapes avec le modèle 5B sur un seul H100, incluant un résultat de 13,06 secondes avec Sol Engine. Considérez-le comme un contexte de benchmark figé, et non comme une estimation de temps d'exécution sur GPU grand public.

## Architecture — détail complet {#architecture-full-detail}

### Variantes du modèle {#model-variants}

| Variante | Paramètres | Profondeur | Dimension cachée | Têtes | FFN (MLP 2,5×) |
|---------|--------|-------|--------|-------|----------------|
| Sana-0.6B | 590M | 28 blocs | 1152 | 16 | 2880 |
| Sana-1.6B | 1604M | 20 blocs | 2240 | 20 | 5600 |
| Sana-1.5 4.8B | 4800M | 60 blocs | 2240 | 20 | 5600 |

0,6B = plus profond mais plus étroit. 1,6B = moins profond mais plus large. 4,8B ne met à l'échelle que la profondeur (20→60), la largeur reste identique à celle de 1,6B.

### Structure de SanaBlock (AdaLN-Zero) {#sanablock-structure-adaln-zero}

```bash
Input x → LayerNorm → modulate(shift1, scale1) → Linear Self-Attention (LiteLA)
        → LayerNorm → modulate(shift2, scale2) → Cross-Attention (standard, with text)
        → LayerNorm → modulate(shift3, scale3) → Mix-FFN (GLUMBConv)
Output x (residual at each stage, 6 modulation params per block via scale_shift_table)
```

### Attention linéaire (LiteLA avec noyau ReLU) {#linear-attention-litela-with-relu-kernel}

```python
# Standard quadratic: O(N^2)
# Attention = softmax(QK^T / sqrt(d)) * V

# SANA linear: O(N * d^2)
# phi(x) = ReLU(x)
# Shared terms: S = sum_j phi(K_j)^T * V_j   (shape d×d, computed ONCE)
#               Z = sum_j phi(K_j)^T          (shape d×1, computed ONCE)
# Output_i = phi(Q_i) * S / (phi(Q_i) * Z + eps)
```

**Compromis :** l'attention linéaire seule dégrade la qualité. Ce défaut est compensé par Mix-FFN, qui utilise une convolution depthwise 3×3 pour capturer l'information spatiale locale perdue avec le noyau ReLU (absence de biais de localité lié au softmax).

**Fusion de noyaux Triton :** l'activation ReLU, les conversions de précision, le padding et la division sont fusionnés dans la multiplication matricielle → environ 10 % d'accélération.

**Encodage de position :** « NoPE » (No Positional Embeddings) — la convolution depthwise 3×3 de Mix-FFN encode implicitement la position. Il est aussi possible d'utiliser RoPE avec `theta=10000, axes_dim=[0,16,16]`.

### Mix-FFN (GLUMBConv) {#mix-ffn-glumbconv}

Remplace le MLP standard :
```text
Linear(d → d×2.5) → DW-Conv3×3 → SiLU → Gate (GLU) → Linear(d×1.25 → d)
```
La convolution depthwise 3×3 est la clé du bon fonctionnement de l'attention linéaire. Elle fournit un champ réceptif local qui fait défaut à l'attention linéaire avec ReLU.

### DC-AE (Deep Compression Autoencoder) — F32C32P1 {#dc-ae-deep-compression-autoencoder-f32c32p1}

**Compression spatiale de 32×, 32 canaux latents, taille de patch 1.**

| Résolution | Tokens SD/FLUX (F8, P2) | Tokens SANA (F32, P1) | Réduction |
|-----------|-------------------------|------------------------|-----------|
| 512×512 | 1024 | **256** (16×16) | 4× |
| 1024×1024 | 4096 | **1024** (32×32) | 4× |
| 2048×2048 | 16384 | **4096** (64×64) | 4× |
| 4096×4096 | 65536 | **16384** (128×128) | 4× |

4× moins de tokens + attention linéaire O(n) = une accélération de **plusieurs ordres de grandeur** à haute résolution.

Qualité de reconstruction (ImageNet) : rFID 0,34, PSNR 29,29, SSIM 0,84, LPIPS 0,05.

**Tiling pris en charge :** `pipe.vae.enable_tiling(tile_sample_min_height=1024, tile_sample_min_width=1024)` — permet la 4K avec 22 Go de VRAM.

Deux versions : `dc-ae-f32c32-sana-1.0`, `dc-ae-f32c32-sana-1.1` (améliorée) et `dc-ae-lite-f32c32` (plus rapide et plus petite).

### Encodeur de texte : Gemma-2-2B-IT {#text-encoder-gemma-2-2b-it}

LLM decoder-only (et non T5). 6× plus rapide que T5-XXL. Maximum de 300 tokens.

**Point critique :** les sorties d'un LLM decoder-only ont une variance supérieure de plusieurs ordres de grandeur à celle de T5. Solution : une **RMSNorm** après l'encodeur, avec une échelle apprenable de 0,01 (`y_norm: true, y_norm_scale: 0.01`).

**Complex Human Instruction (CHI) :** exploite l'apprentissage en contexte de Gemma → +2,2 points GenEval.

## Entraînement {#training}

### Perte et planificateur {#loss-scheduler}

Prédiction de vitesse en [[flow-matching]] : `v_theta(x_t, t) = epsilon - x_0`. Échantillonnage des pas de temps : logit-normal (moyenne=0,0, écart-type=1,0). Décalage de flux (flow shift) : 3,0.

### Optimiseur : CAME {#optimizer-came}

```yaml
optimizer: CAMEWrapper
lr: 1e-4
betas: [0.9, 0.999, 0.9999]
epsilon: [1e-30, 1e-16]
weight_decay: 0.0
grad_clip: 0.1
warmup: 2000 steps, constant after
```

SANA 1.5 utilise **CAME-8bit** : moments du premier ordre en 8 bits par bloc, moments du second ordre en 32 bits. Réduction de mémoire de 25 % par rapport à AdamW.

### Calendrier de résolution {#resolution-schedule}

On saute entièrement les 256 px. On démarre à 512 px, puis on affine à 1024, 2K et 4K.

### Étiquetage multi-légendes {#multi-caption-labeling}

4 VLM génèrent des légendes (VILA-3B, VILA-13B, InternVL2-8B, InternVL2-26B). Un échantillonneur basé sur le score CLIP sélectionne la légende à chaque itération.

### SFT : 3M d'échantillons filtrés avec CLIP > 25 parmi 50M de données de pré-entraînement. {#sft-3m-samples-filtered-by-clip-25-from-50m-pre-training-set}

## Principales améliorations de SANA 1.5 {#sana-15-key-improvements}

1. **Paradigme de croissance en profondeur (1.6B → 4.8B) :** suppression des 2 derniers blocs du modèle 1.6B entraîné → ajout de 40 nouveaux blocs avec une initialisation à préservation partielle (applications identité) → 60 % d'étapes d'entraînement en moins
2. **Normalisation QK :** RMSNorm sur Q et K pour un entraînement stable des grands modèles
3. **Élagage en profondeur :** métrique d'importance des blocs → élagage des blocs intermédiaires, conservation de la tête et de la queue → récupération rapide avec environ 100 étapes de fine-tuning
4. **Mise à l'échelle au moment de l'inférence :** génération de N candidats, sélection du meilleur via VILA-Judge (NVILA-2B affiné). GenEval : 0,81 → **0,96** avec 2048 candidats. 1,6B avec mise à l'échelle **surpasse** 4,8B sans celle-ci

## Benchmarks {#benchmarks}

| Modèle | Paramètres | FID↓ | CLIP↑ | GenEval↑ | Vitesse (A100) |
|-------|--------|------|-------|----------|-------------|
| FLUX-dev | 12.0B | 10.15 | 27.47 | 0.67 | 0.04 img/s |
| SD3-medium | 2.0B | 11.92 | 27.83 | 0.62 | 0.28 img/s |
| **Sana-0.6B** | 0.6B | **5.81** | 28.36 | 0.64 | **1.7 img/s** |
| **Sana-1.6B** | 1.6B | **5.76** | 28.67 | 0.66 | **1.0 img/s** |
| **Sana-1.5 1.6B** | 1.6B | 5.70 | 29.12 | **0.82** | 1.0 img/s |
| **Sana-1.5 4.8B** | 4.8B | 5.99 | 29.23 | 0.81 | 0.26 img/s |

Sana-1.6B est **23× plus rapide** que FLUX-dev. En 4K : **106× plus rapide** (9,6 s contre 469 s).

## SANA-Sprint (distillé, 1 à 4 étapes) {#sana-sprint-distilled-1-4-steps}

Distillation hybride : sCM (cohérence continue) + LADD (adversarial latent).

| Étapes | FID | GenEval | Latence (H100) |
|-------|-----|---------|-----------------|
| 1 | 7.04 | 0.72 | **0.1s** |
| 2 | 6.76 | — | 0.24s |
| 4 | 6.48 | 0.76 | 0.32s |

Surpasse FLUX-schnell (FID 7,94) tout en étant 10× plus rapide. ICCV 2025 Highlight.

## Branches vidéo et modèle du monde de SANA {#sana-video-and-world-model-branches}

### SANA-Video (génération 2025) {#sana-video-2025-generation}

La branche vidéo originale a introduit Block Causal Linear Attention et Causal Mix-FFN. Ses résultats rapportés 2B/720p/16 FPS appartiennent à cette version et ne doivent pas être reportés sur Video2 ou SANA-WM.

Point clé pour le [[temporal-tiling]] : l'attention causale est structurellement pertinente pour un tiling par images, mais il s'agit d'une analogie architecturale et non d'un workflow SANA pris en charge.

### SANA-WM (modèle du monde 2026) {#sana-wm-2026-world-model}

SANA-WM est un modèle du monde interactif de 2,6B, et non un renommage de SANA-Video. Le projet officiel décrit une génération en 720p, des séquences allant jusqu'à une minute et un contrôle de caméra 6-DoF. Validez le format du contrôleur et la licence du checkpoint sur la version exacte avant toute intégration.

### SANA-Video2 (génération 2026) {#sana-video2-2026-generation}

Video2 est la branche actuelle. Le dépôt officiel a ajouté le code d'entraînement, le code d'inférence, les détails d'architecture et un checkpoint 5B 720p le 2026-08-19. Une variante 14B est décrite mais n'est pas un checkpoint public exécutable dans le dépôt.

Le benchmark de l'article de la page projet et le guide du checkpoint publié utilisent des configurations d'exécution différentes :

| Contexte | Images/durée | FPS | Étapes | Objectif |
|---|---|---:|---:|---|
| Benchmark H100 de la page projet | Clip de 5 secondes | Non défini par la recette publiée | 40 | Comparaison article/moteur uniquement |
| Guide du checkpoint 5B public | 193 images / environ 8,04 secondes | 24 | 50 | Exemple actuel du checkpoint publié |

Pour une évaluation reproductible du checkpoint publié, partez du guide public et consignez :

```yaml
artifact: SANA-Video2-5B
revision: <immutable-checkpoint-or-repository-revision>
resolution: 720p
frames: 193
fps: 24
duration_seconds: 8.04
steps: 50
gpu: <exact-model>
engine: <official-or-baseline-runtime>
seed: <integer>
refiner_enabled: <true-or-false>
```

N'appliquez pas le libellé 14B à cette recette. Utilisez 5 secondes/40 étapes uniquement pour reproduire le benchmark de l'article, et non comme valeur par défaut du checkpoint public. Ne comparez pas les temps mesurés sur H100 à un GPU local sans mesurer les mêmes images/durée, résolution, étapes, environnement d'exécution et état du raffineur.

## VRAM {#vram}

| Configuration | VRAM |
|--------|------|
| 0,6B 1024 px bf16 | ~16 Go |
| 1,6B 1024 px bf16 | ~16-24 Go |
| 4K avec tiling VAE | ~22 Go |
| 4K + quantification 4 bits + offload | **< 8 Go** |
| Génération 1024 px quantifiée W8A8 | Très faible, 0,37 s sur 4090 |

## Fine-tuning / LoRA {#fine-tuning-lora}

Prise en charge officielle via diffusers `train_dreambooth_lora_sana.py`. Voir [[diffusion-lora-training]] pour le détail complet du pipeline d'entraînement.

**Cibles LoRA :** `attn.to_k, attn.to_q, attn.to_v, attn.to_out.0` + éventuellement FFN/MLP.

**Paramètres :** LR 1e-4, 500 étapes, batch 1, accumulation de gradient 4, bf16. Nécessite peft >= 0.14.0.

**Exigences du jeu de données :**
- DreamBooth (sujet) : 3 à 5 images minimum
- LoRA de style/domaine : 20 à 30 images recommandées
- Format : résolution 1024x1024 ou plus, légendes détaillées avec un jeton déclencheur rare (« sks »)

**Options d'optimisation mémoire :** `--offload` (déport CPU de l'encodeur de texte et du VAE), `--cache_latents` (précalcul des latents du VAE), `--use_8bit_adam`.

**ControlNet** également pris en charge : architecture ControlNet-Transformer pour le backbone SANA.

### Auto-raffinement (img2img) {#self-refinement-img2img}

SANA-Sprint prend en charge l'img2img via `SanaSprintImg2ImgPipeline` :

```python
from diffusers import SanaSprintImg2ImgPipeline
import torch

pipe = SanaSprintImg2ImgPipeline.from_pretrained(
    "Efficient-Large-Model/Sana_Sprint_1.6B_1024px_diffusers",
    torch_dtype=torch.bfloat16
)
pipe.to("cuda")

# Multi-pass refinement (replaces SDXL refiner pattern)
refined = pipe(
    prompt="a high quality detailed photo",
    image=initial_image,
    strength=0.3,            # 0.3 = mild refinement, 0.7 = heavy change
    num_inference_steps=4    # Sprint is 1-4 steps
).images[0]
```

**Mécanique de l'img2img en flow matching :** SANA utilise le flow matching, et non DDPM. Le paramètre `strength` interpole entre la latente de l'image d'entrée encodée et le bruit pur : `x_t = (1-strength)*image_latent + strength*noise`. Cela diffère de la planification de bruit de DDPM : il n'y a pas d'étape « ajouter du bruit puis débruiter », mais une interpolation directe.

**Recette multi-passes :**
```text
txt2img 1024px (strength=1.0) → img2img strength=0.3-0.4 → img2img strength=0.2
```

**Le raffineur SDXL n'a pas d'équivalent en flow matching :** le raffineur SDXL utilise un échantillonnage à pas de temps élevés, spécifique à DDPM. L'img2img de SANA en est le remplaçant fonctionnel, mais il fonctionne différemment en interne.

**DemoFusion est incompatible avec SANA :** DemoFusion repose sur les connexions résiduelles (skip connections) de UNet pour le contexte global multi-échelle. L'architecture transformer de SANA ne les possède pas. Utilisez plutôt FreeScale ou APT pour le tiling haute résolution.

Voir [[flow-matching]] pour tous les détails sur l'img2img en flow matching.

## Historique du développement {#development-history}

| Date | Branche | Événement | Statut temporel |
|---|---|---|---|
| 2024-10-22 | SANA image | Dépôt/projet rendu public | Découverte historique |
| 2024-11-21 | SANA image | Code d'entraînement, d'inférence et de métriques, et modèles 1.6B disponibles | Fondation actuelle |
| 2025-10-01 | SANA-Video | Préversion annoncée | Remplacée par l'implémentation publiée |
| 2025-10-27 | SANA-Video | Publication officielle | Historique/actuel pour cette branche |
| 2025-11-06 | SANA-Video | Intégration Diffusers annoncée par le projet | Historique d'intégration actuel |
| 2025-12-24 | SANA-Video | Disponibilité du code/checkpoint annoncée | Remplacée par des branches ultérieures, conservée |
| 2026-03 | Outils SANA image/video | Chemin VAE LTX en 720p et mise à jour raffineur LTX2 vers 2K | Actuel uniquement pour ce pipeline |
| 2026-05 | SANA-WM | Branche de modèle du monde de 2,6B publiée | Branche actuelle |
| 2026-08-04 | SANA-Video2 | Annonce constatée sans poids | Remplacée pour le 5B le 2026-08-19 |
| 2026-08-19 | SANA-Video2 | Code et checkpoint 5B 720p publiés | Actuel |

## Choix pratique {#practical-selection}

- Utilisez SANA/SANA 1.5 pour la génération d'images efficace et les workflows LoRA d'images documentés.
- Utilisez Sprint uniquement lorsque son comportement distillé en une à quatre étapes est explicitement souhaité ; ne réutilisez pas les nombres d'étapes standard.
- Utilisez SANA-Video2 5B pour le chemin Video2 officiel exécutable actuel.
- Utilisez SANA-WM uniquement pour des expériences interactives/modèle du monde, avec son propre contrat de contrôleur.
- Ne planifiez pas de déploiement Video2 14B tant qu'un checkpoint officiel et sa licence ne sont pas disponibles.

## Couverture de la recherche et lacunes ouvertes {#research-coverage-and-open-gaps}

- Preuves primaires en anglais : dépôt officiel, page projet officielle de Video2 et articles.
- Piste de requête en chinois : recherchée, mais aucune source chinoise de première partie qualifiée n'a été retenue lors de la passe bornée.
- Lacune de preuve ouverte : une matrice entièrement reproductible sur GPU grand public, figée par les empreintes des checkpoints, les versions d'exécution et l'état du raffineur.
- Les rapports de performance de la communauté restent secondaires tant qu'ils ne sont pas reproduits avec les mêmes paramètres.

### Rapports de la communauté {#community-reports}

- [Issue #156](https://github.com/NVlabs/Sana/issues/156) signale une piste d'entraînement 1.6B communautaire sur 24 Go avec offload. Le contributeur a explicitement qualifié le correctif de bricolé ; un contributeur officiel a indiqué la configuration CAME-8bit du projet comme une meilleure piste d'économie de mémoire. Considérez ce ticket comme une piste technique, et non comme une recette directement utilisable.
- [Issue #297](https://github.com/NVlabs/Sana/issues/297) décrit un cas non résolu sur MacBook Pro M3/MPS où `Sana_600M_512px_diffusers` avec `float16` produisait une image grise uniforme sans exception. Testez `float32` comme diagnostic, mais aucune correction confirmée par les mainteneurs n'était disponible.
- Aucun de ces tickets ne concerne le checkpoint publié Video2 5B. Ne transférez pas leurs paramètres de modèle d'image vers Video2.

## Pièges courants {#gotchas}

- **Problème :** considérer « SANA-Video » comme un checkpoint unique à versionnage continu → **Correctif :** consignez la branche (`Video`, `WM` ou `Video2`), la taille du modèle, la révision du checkpoint et la date de publication.
- **Problème :** choisir Video2 14B parce qu'il apparaît dans les tableaux d'architecture → **Correctif :** utilisez le checkpoint 5B publié ; le 14B n'est pas un artefact public exécutable au 2026-08-27.
- **Problème :** répéter l'affirmation du 4 août « sans poids » comme information actuelle → **Correctif :** marquez-la comme remplacée par la publication 5B du 19 août, tout en la conservant comme contexte historique.
- **Problème :** généraliser une latence H100 ou d'anciens benchmarks vidéo 2B → **Correctif :** précisez dans chaque comparaison le matériel, le moteur, la durée, la résolution, les étapes et la branche.
- **Problème :** utiliser le benchmark de l'article (5 secondes/40 étapes) comme recette du checkpoint publié → **Correctif :** partez des 193 images, 24 FPS et 50 étapes du guide public, sauf si vous reproduisez volontairement le benchmark.
- **Problème :** appliquer à Video2 un contournement offload/MPS conçu pour les modèles d'images → **Correctif :** exigez la branche, le checkpoint, l'URL du ticket et l'environnement d'exécution exacts avant toute réutilisation.

## Consigne pour l'agent {#agent-brief}

Lorsque vous répondez à une question sur SANA, identifiez d'abord `image`, `Sprint`, `Video`, `WM` ou `Video2`. Privilégiez le dépôt officiel et la page projet officielle aux résumés d'actualité. Accompagnez les affirmations historiques d'une étiquette temporelle (`current`, `superseded` ou `unknown`). Ne recommandez jamais Video2 14B comme téléchargeable, sauf si un checkpoint plus récent et de première partie a été vérifié. Pour les conseils de déploiement, demandez ou signalez la révision exacte de l'artefact, le GPU, l'environnement d'exécution, la résolution, la durée, les étapes et l'état du raffineur.

## Licence {#license}

**Code : Apache 2.0. Poids : NSCL v2-custom** (vérifiez les conditions spécifiques pour un usage commercial).

## Liens clés {#key-links}

- GitHub : https://github.com/NVlabs/Sana
- SANA-Video2 : https://nvlabs.github.io/Sana/Video2/
- Guide du checkpoint Video2 publié : https://github.com/NVlabs/Sana/blob/main/docs/sana_video2.md
- Rapport communautaire sur l'offload : https://github.com/NVlabs/Sana/issues/156
- Rapport ouvert sur la sortie grise MPS : https://github.com/NVlabs/Sana/issues/297
- HF : https://huggingface.co/Efficient-Large-Model/
- Articles : https://arxiv.org/abs/2410.10629 (SANA), https://arxiv.org/abs/2501.18427 (1.5), https://arxiv.org/abs/2503.09641 (Sprint)
- SANA-Video : https://arxiv.org/abs/2509.24695
- DC-AE : https://github.com/mit-han-lab/efficientvit
- Framework d'entraînement : happyin-research/sana-fm/ (local)
