---
title: "SDXL"
category: projects
date: 2023-06-22
tags: [project, sdxl, sdxl-development]
aliases: ["SDXL", "SDXL 0.9", "SDXL 1.0"]
level: 2
source_sha256: fdcc92cf54ef02510fc3464644de778f2d49863834ba99fe0bf5b5bdc4b877a0
translation: machine
translated_at: '2026-10-24'
---
# SDXL {#sdxl}

**Ligne de développement :** `project:sdxl` · fil `sdxl-development`  
**Dernier événement :** 2023-06-22 · 2 événements datés depuis le 2023-05-24 · **Vérifié le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

SDXL : un modèle Stable Diffusion destiné aux praticiens qui ont besoin de génération d'images pilotée par prompt.

- Génère des sorties texte-vers-image, image-vers-image et inpainting.
- Fonctionne avec le checkpoint de base officiel 1.0, seul ou avec un refiner optionnel.
- Cible par défaut : 1024×1024 ; les checkpoints par défaut ne sont pas recommandés en dessous de 512 pixels.

## Ligne de développement {#development-line}

- **2023-05-24 — Un jalon d'avancement de l'entraînement de SDXL a été signalé.** Le 2023-05-24, un lien daté de développement SDXL indiquait que l'entraînement du modèle avait atteint un jalon à mi-parcours et renvoyait les lecteurs vers un canal de discussion communautaire. C'est un point de contrôle important, car il situe le projet dans une phase active d'entraînement et de retours avant publication.
- **2023-06-22 — Stability AI a publié une mise à jour SDXL 0.9.** Elle était disponible via Clipdrop, les poids de recherche étaient accessibles, et la version 1.0 était prévue pour mi-juillet.

## Évolutions {#what-changed}

2023-05-24 — SDXL n'était encore entraîné qu'à moitié environ ; un bot Discord recueillait des votes de préférence sur les images pendant le test de paramètres. Il s'agissait donc de retours sur l'entraînement, et non d'une version publiée. 2023-06-22 — SDXL 0.9 est passé de la bêta vers une diffusion limitée à des fins de recherche : il était disponible via Clipdrop, les poids de recherche étaient accessibles, et la version 1.0 était prévue pour mi-juillet. 2023-06-25 — la publication officielle liée ne peut plus être récupérée aujourd'hui ; aucun changement technique supplémentaire ne peut donc être vérifié à partir de celle-ci. 2023-07-26 (constaté le 2026-09-04) — SDXL 1.0 a été publié en tant que modèle ouvert, remplaçant la version 0.9 limitée à la recherche par la ligne 1.0 base avec refiner optionnel. 2026-09-04 (constaté aujourd'hui) — la voie pratique maintenue est le checkpoint officiel `stabilityai/stable-diffusion-xl-base-1.0` via Diffusers ; la base reste utilisable sans le refiner.

## Mode d'emploi {#how-to-use-this}

À partir du 2023-06-22, les praticiens doivent suivre SDXL 0.9 séparément dans leurs notes sur les modèles et les workflows : cette ligne passe d'une mise à jour sur l'état de l'entraînement à une publication nommée SDXL 0.9.

1. Installez Diffusers, Transformers, Accelerate et la dépendance optionnelle invisible-watermark à partir du guide SDXL actuel.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
2. Chargez `stabilityai/stable-diffusion-xl-base-1.0` avec `StableDiffusionXLPipeline` ou `AutoPipelineForText2Image`, de préférence en safetensors fp16 sur un accélérateur compatible.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
3. Commencez le travail texte-vers-image en 1024×1024 ; utilisez 768×768 ou 512×512 uniquement si le workflow l'exige, et évitez les dimensions plus petites avec le checkpoint par défaut.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
4. Pour une retouche, réutilisez le pipeline chargé en image-vers-image avec une image d'entrée, ou en inpainting avec une image d'entrée et un masque.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
5. Ajoutez `stabilityai/stable-diffusion-xl-refiner-1.0` seulement lorsqu'une passe de débruitage finale vaut le coût de calcul supplémentaire ; le passage documenté entre les deux modèles est de 80 % de débruitage par la base et 20 % par le refiner.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
6. Avant de publier ou d'automatiser des sorties, vérifiez la licence de la fiche modèle, les limites d'usage prévu et les échecs connus pour le texte, les visages, la composition et les représentations factuelles.
  — <https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0>

## Bonnes pratiques {#best-practices}

- Utilisez le checkpoint de base officiel 1.0 comme référence et considérez le refiner comme optionnel ; la base est un chemin autonome pris en charge.
  — <https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0>
- Gardez la génération SDXL par défaut proche de sa cible native de 1024×1024 ; utilisez le conditionnement par taille et recadrage pour la composition, plutôt que de vous attendre à de bons résultats du checkpoint par défaut en dessous de 512 pixels.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
- En cas d'erreurs de mémoire insuffisante, utilisez d'abord le déchargement CPU du modèle (model CPU offload) avant de sacrifier la plage de résolution documentée ; n'utilisez `torch.compile` ou xFormers que si l'environnement d'exécution les prend en charge.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
- Conservez la dépendance invisible-watermark lorsque le marquage des images générées est exigé par le workflow ; Diffusers l'active par défaut lorsqu'elle est installée.
  — <https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl>
- N'utilisez pas les sorties SDXL comme représentation factuelle de personnes ou d'événements, et conservez une relecture humaine pour le texte lisible, les visages et les relations spatiales.
  — <https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0>

## Ce qui est remplacé {#superseded-by-this}

- 2023-05-24 — Les votes Discord et les expériences de paramètres relevaient d'un processus de retours sur l'entraînement avant publication, et non d'une voie de déploiement ; les poids ouverts de SDXL 1.0 ont remplacé cet état le 2023-07-26.
- 2023-06-22 — Les consignes relatives aux poids de recherche de SDXL 0.9 et à l'aperçu Clipdrop sont obsolètes pour tout nouveau déploiement ; utilisez plutôt le checkpoint de base SDXL 1.0 nommé.
- 2023-06-22 — Le passage prévu à la version 1.0 en mi-juillet n'est plus une consigne prospective ; la publication ouverte de SDXL 1.0 a eu lieu le 2023-07-26.

## Points non vérifiés {#still-unknown}

- L'URL Twitter datée du 2023-06-25 fournie n'a renvoyé aucune donnée lisible par le lecteur disponible ; son affirmation exacte et son impact technique restent non vérifiés.
- Ce document n'affirme rien sur la disponibilité actuelle, les tarifs ou le statut de support des moteurs de l'ancienne API Stability cités en 2023 ; les éléments disponibles ne concernent que le workflow checkpoint et Diffusers.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.reddit.com/r/StableDiffusion/comments/13ppmtk/sdxl_is_now_50_trained_and_we_need_your_help/ | SDXL est maintenant entraîné à ~50 % — et nous avons besoin de votre aide ! | 2026-09-04 |
| https://stability.ai/blog/sdxl-09-stable-diffusion | Stability AI lance SDXL 0.9 : un bond en avant dans la génération d'images par IA | 2026-09-04 |
| https://twitter.com/emostaque/status/1672700056154275841?s=21&t=RcamOh5xDIh5ilUsd6CSdA | Publication d'Emad Mostaque sur SDXL (contenu non récupérable) | 2026-09-04 |
| https://stability.ai/news-updates/stable-diffusion-sdxl-1-announcement | Annonce de SDXL 1.0 | 2026-09-04 |
| https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0 | stabilityai/stable-diffusion-xl-base-1.0 — Fiche modèle SD-XL 1.0-base | 2026-09-04 |
| https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl | Stable Diffusion XL — documentation Diffusers | 2026-09-04 |

## Note pour l'agent {#agent-brief}

- **Sujet :** `project:sdxl`, fil `sdxl-development`, 2 événements datés du 2023-05-24 au 2023-06-22.
- **Note pratique :** À partir du 2023-06-22, les praticiens doivent suivre SDXL 0.9 séparément dans leurs notes sur les modèles et les workflows : cette ligne passe d'une mise à jour sur l'état de l'entraînement à une publication nommée SDXL 0.9.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
