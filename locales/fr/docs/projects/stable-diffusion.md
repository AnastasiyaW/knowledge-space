---
title: "Stable Diffusion"
category: projects
date: 2022-07-26
tags: [dataset, project, stable-diffusion, stable-diffusion-development, stable_diffusion, stable_diffusion_v2_2_2_xl_beta]
aliases: ["Stable Diffusion", "Stable Diffusion 3"]
level: 3
source_sha256: 7b48d1917ab34df24f8db0096fcde9547314281d2418410f69c90bf42f011089
translation: machine
translated_at: '2026-10-24'
---
# Stable Diffusion {#stable-diffusion}

**Ligne de développement :** `project:stable-diffusion` · fil `stable-diffusion-development`  
**Dernier événement :** 2022-07-26 · 1 événement daté depuis le 2022-07-26 · **Vérifié le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Stable Diffusion est une famille de modèles génératifs d'images destinée aux artistes et aux développeurs qui doivent choisir entre l'auto-hébergement et une API, plutôt qu'un service fermé comme Midjourney.

- génération d'image à partir de texte et image-à-image
- ControlNet pour le contrôle par Canny, profondeur ou flou
- variantes Large, Turbo, Medium et Flash

L'API SD 3.5 produit des images de 1 MP, par défaut 1024×1024 ; l'entrée image-à-image accepte jusqu'à 10 MiB.

Pour les nouvelles intégrations, utilisez SD 3.5 plutôt que les identifiants antérieurs de SD3 ou de la bêta SDXL.

## Ligne de développement {#development-line}

- **2022-07-26 — jalon d'inscription à l'accès bêta de Stable Diffusion.** Le 2022-07-26, l'enregistrement Stable Diffusion renvoyait au formulaire d'inscription bêta de Stability AI. Cela étaye la conservation de ce jalon d'accès bêta, mais n'établit ni une version de modèle publiée, ni l'éligibilité, ni un ensemble de fonctionnalités.

## Changements {#what-changed}

2022-07-26 — l'inscription bêta impliquait des tests limités plutôt qu'une publication publique des poids ; l'accès à la recherche a ouvert le 2022-08-10, et la publication publique a suivi le 2022-08-22.

2023-03-09 — le lien NeuralPic ne précise aucun jeu de données, modèle ou version de Stable Diffusion ; le changement de produit n'est pas confirmé.

2023-03-25 — l'entrée `stable_diffusion_v2_2_2_xl_beta` n'a pas d'URL, la date et le changement ne peuvent donc pas être vérifiés. Le 2023-04-13, l'API officielle a ajouté le moteur `stable-diffusion-xl-beta-v2-2-2` pour la bêta SDXL et DreamStudio.

2024-03-07 — le lien ne pointe que vers un profil X, ce qui rend le message précis invérifiable. Le statut officiel de SD3 à cette période était un aperçu anticipé sur liste d'attente, avec des variantes allant de 800M à 8B paramètres.

2024-03-13 — le message X précis est indisponible à la vérification ; aucun changement confirmé de modèle ou d'API n'en découle.

Le 2024-06-12, SD3 Medium a été publié pour l'API REST et le téléchargement des poids ; le 2024-10-22, SD 3.5 Large et Large Turbo sont apparus, puis SD 3.5 Medium le 2024-10-29.

À partir du 2025-04-17, les identifiants de l'API SD3 sont redirigés automatiquement vers leurs équivalents SD 3.5. Dans la liste active des Core Models au 2026-05-20, SD 3.5 Medium, Large et Large Turbo sont toujours présents.

## Mode d'emploi {#how-to-use-this}

Pour l'enregistrement historique du 2022-07-26, considérez l'inscription bêta, et non une publication publique confirmée, comme voie d'accès opérationnelle ; vérifiez séparément la disponibilité actuelle et les conditions.

1. Choisissez une voie : API pour une intégration gérée, ou hébergement local pour un contrôle de l'infrastructure. Pour une qualité 1 MP, prenez Large ; pour la vitesse, choisissez Large Turbo ou Flash ; pour un coût de ressources réduit, choisissez Medium.  
  — <https://platform.stability.ai/docs/api-reference>
2. Pour l'API, créez un compte et une clé, puis transmettez la clé uniquement dans l'en-tête Authorization.  
  — <https://platform.stability.ai/docs>
3. Envoyez une requête POST multipart vers `/v2beta/stable-image/generate/sd3` avec `prompt`, `model` et `output_format` ; pour l'image-à-image, transmettez l'image source, `strength` et `mode=image-to-image`.  
  — <https://platform.stability.ai/docs/api-reference>
4. Pour les exécutions locales, acceptez la licence des poids, installez `diffusers`, `transformers` et `accelerate`, chargez `StableDiffusion3Pipeline` et enregistrez les images produites.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
5. Pour ancrer la composition à des images de référence, attachez le ControlNet SD3.5 Large avec une image de conditionnement Canny, profondeur ou flou.  
  — <https://github.com/Stability-AI/sd3.5>

## Bonnes pratiques {#best-practices}

- Ne stockez pas et ne committez pas les clés API : transmettez la clé dans l'en-tête Authorization et révoquez-la en cas de fuite.  
  — <https://platform.stability.ai/docs>
- Définissez une graine (seed) explicite pour des comparaisons reproductibles : elle contrôle l'aléa de la génération.  
  — <https://platform.stability.ai/docs/api-reference>
- Pour SD 3.5 Medium, limitez les prompts à 256 tokens T5 : des requêtes plus longues risquent des artefacts en bordure. Utilisez Skip Layer Guidance pour la structure et l'anatomie.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- Lorsque la VRAM est insuffisante, utilisez la quantification officielle en 4 bits et le déchargement sur CPU plutôt que des échanges arbitraires de poids.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- Vérifiez la licence avant un auto-hébergement commercial : la Community License couvre les entités dont le chiffre d'affaires annuel est inférieur à 1 M$ ; au-delà, une Enterprise License est requise.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>
- Ajoutez en production des garde-fous de sécurité de contenu personnalisés : les filtres d'entraînement n'empêchent pas les sorties nuisibles.  
  — <https://huggingface.co/stabilityai/stable-diffusion-3.5-medium>

## Remplacé par {#superseded-by-this}

- 2022-07-26 : l'inscription à la liste d'attente bêta a été remplacée par la publication publique de Stable Diffusion du 2022-08-22.
- 2023-04-13 : les limites du moteur et le nom `stable-diffusion-xl-beta-v2-2-2` s'appliquent à l'ancienne bêta SDXL, et non aux routes API actuelles.
- 2024-02 à 03 : l'attente de l'aperçu anticipé de SD3 a été remplacée par les publications de SD3 et SD 3.5.
- 2025-04-17 : les instructions d'API visant `sd3-large`, `sd3-large-turbo` et `sd3-medium` sont obsolètes, car les requêtes sont redirigées vers SD 3.5.

## Points restant inconnus {#still-unknown}

- Le contenu du formulaire d'inscription bêta du 2022-07-26 est indisponible ; son rôle d'accès préliminaire repose sur des annonces officielles ultérieures.
- Le lien NeuralPic du 2023-03-09 ne relie pas l'événement à un jeu de données, un point de contrôle ou une version précise de Stable Diffusion.
- L'enregistrement du 2023-03-25 ne comporte pas d'URL : le nom ressemble au moteur API bêta SDXL ultérieur, mais rien ne prouve qu'il soit apparu à cette date.
- Les liens X du 2024-03-07 et du 2024-03-13 n'ont renvoyé aucun contenu, ce qui laisse les changements de modèle, de licence ou de gestion non vérifiés.
- Les étiquettes `dataset`, `stable_diffusion` et `stable_diffusion_v2_2_2_xl_beta` peuvent confondre un lien de jeu de données non confirmé, une piste bêta non officielle et des publications officielles de modèles.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://stability.ai/beta-signup-form | Formulaire d'inscription bêta de Stability AI — indisponible à la lecture | 2026-09-04 |
| https://twitter.com/EMostaque | Emad Mostaque sur X — indisponible à la lecture | 2026-09-04 |
| https://twitter.com/EMostaque/status/1767662732797411433 | Emad Mostaque, message 1767662732797411433 — indisponible à la lecture | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-launch-announcement | Annonce de lancement de Stable Diffusion | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-public-release | Publication publique de Stable Diffusion | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-xl-beta-available-for-api-customers-and-dreamstudio-users | Stable Diffusion XL Beta disponible pour les clients API et les utilisateurs de DreamStudio | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-3 | Stable Diffusion 3 | 2026-09-04 |
| https://platform.stability.ai/docs/release-notes | Notes de version de la plateforme développeur Stability AI | 2026-09-04 |
| https://stability.ai/core-models | Core Models de Stability AI | 2026-09-04 |
| https://platform.stability.ai/docs | Stability AI API : démarrage | 2026-09-04 |
| https://platform.stability.ai/docs/api-reference | API REST StabilityAI (v2beta) | 2026-09-04 |
| https://huggingface.co/stabilityai/stable-diffusion-3.5-medium | Fiche modèle stabilityai/stable-diffusion-3.5-medium | 2026-09-04 |
| https://github.com/Stability-AI/sd3.5 | Stability-AI/sd3.5 | 2026-09-04 |

## Consigne pour l'agent {#agent-brief}

- **Sujet :** `project:stable-diffusion`, fil `stable-diffusion-development`, 1 événement daté du 2022-07-26 au 2022-07-26.
- **Note pratique :** Pour l'enregistrement historique du 2022-07-26, considérez l'inscription bêta, et non une publication publique confirmée, comme voie d'accès opérationnelle ; vérifiez séparément la disponibilité actuelle et les conditions.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
