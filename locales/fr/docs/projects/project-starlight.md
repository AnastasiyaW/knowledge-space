---
title: "Project Starlight"
category: projects
date: 2025-02-11
tags: [project, project-starlight, project-starlight-public-rollout, project_starlight]
aliases: ["Project Starlight"]
level: 3
source_sha256: 946c6d6b71a0022fa6895f7d6e4b0986012f88110282466ef8ff4eb822b51d6f
translation: machine
translated_at: '2026-10-24'
---
# Project Starlight {#project-starlight}

**Ligne de développement :** `project:project-starlight` · fil `project-starlight-public-rollout`  
**Dernier événement :** 2025-02-11 · 2 datés depuis 2025-02-06 · **Recherche :** 2026-09-04 · confiance : élevée

## Ce que c'est {#what-it-is}

Le modèle de diffusion générative original de Topaz destiné à la restauration de vidéos d'archives et de clips GenAI basse résolution.

- Augmentation de la résolution.
- Reconstruction structurelle.
- Restauration de la cohérence temporelle.

Le modèle original fonctionne dans l'API sous le nom Starlight Precise 1 (`sl-1`), sans contrôles manuels, et est limité à 9 000 images d'entrée. Ce n'est pas un produit figé mais le point de départ d'une famille de modèles : il faut donc choisir en fonction de la variante Starlight spécifique et de la cible d'exécution.

## Ligne de développement {#development-line}

- **2025-02-06 — Topaz Labs a publiquement mentionné Project Starlight.** Un modèle de diffusion de recherche dans le cloud pour la restauration vidéo, privilégiant la qualité à la vitesse et à la taille du modèle.
- **2025-02-11 — Project Starlight est apparu dans Topaz Labs Experiments.** Le 2025-02-11, une URL Project Starlight dans l'application web Experiments de Topaz Labs a été relevée. Les éléments disponibles ne conservent pas le contenu des pages ; cette entrée consigne donc le point d'accès daté aux expérimentations, sans affirmer de flux de travail, d'éligibilité ou d'ensemble de fonctionnalités précis.

## Ce qui a changé {#what-changed}

- 2025-02-06 — Topaz a présenté Project Starlight comme un modèle de diffusion de recherche dans le cloud pour la restauration vidéo, privilégiant la qualité à la vitesse et à la taille.
- 2025-02-11 — Le modèle est devenu accessible via une interface web expérimentale. À l'époque, les aperçus gratuits et les rendus payants étaient soumis à des conditions de contenu différentes.
- 2025-03-05 — L'accès anticipé a ajouté les rendus Starlight en 4K.
- 2025-03-25 — Topaz a préparé la première variante de la série exécutable en local.
- 2025-05-13 — Starlight Mini a été lancé pour le rendu local sous Windows avec des GPU NVIDIA.
- 2025-09-17 — Starlight Sharp a élargi la gamme locale et cloud avec une variante plus détaillée.

## Mode d'emploi {#how-to-use-this}

Considérez la voie Topaz Labs Experiments à partir du 2025-02-11 comme un chemin de découverte daté. Vérifiez la page d'expérimentation actuelle avant toute utilisation, car ces liens seuls n'établissent ni les capacités ni les conditions d'accès.

1. Déterminez s'il faut un modèle local dans Topaz Video ou un modèle cloud. La documentation répertorie Mini, Sharp, Fast 2, HQ et Precise 2.5/2.6, et indique que les modèles cloud fonctionnent aussi dans Astra.
  — <https://docs.topazlabs.com/topaz-video/project-starlight-series>
2. Pour le rendu local, installez Topaz Video avec Neuroserver. Tous les modèles de diffusion Starlight l'exigent. Si Neuroserver échoue, Topaz recommande de réinstaller l'application en mode Réparation.
  — <https://docs.topazlabs.com/topaz-video/project-starlight-series>
3. Pour un traitement programmatique, soumettez la vidéo à l'API Video en utilisant le modèle `sl-1`. Définissez les paramètres techniques si nécessaire et ne dépassez pas 9 000 images d'entrée.
  — <https://developer.topazlabs.com/video-models/starlight/starlight-precise-1>

## Bonnes pratiques {#best-practices}

- Planifiez la file d'attente selon la durée réelle, la résolution et la fréquence d'images. Les rendus de diffusion Starlight peuvent durer de quelques minutes à plusieurs jours.
  — <https://docs.topazlabs.com/topaz-video/project-starlight-series>
- Testez un court extrait représentatif avant un rendu complet lorsque l'identité d'origine et les détails fins comptent. Les premiers échantillons d'utilisateurs ont montré des expressions faciales altérées et des artefacts sur des séquences VHS dégradées.
  — <https://community.topazlabs.com/t/project-starlight-video-ai-6-1-beta/87108?page=10>
- N'envoyez pas de séquences sensibles au niveau d'aperçu gratuit. En février 2025, Topaz a séparé les modes : les rendus payants n'étaient pas utilisés pour l'entraînement des modèles sans consentement, tandis que les aperçus gratuits pouvaient être conservés, examinés et utilisés à des fins de recherche.
  — <https://community.topazlabs.com/t/project-starlight-video-ai-6-1-beta/87108?page=10>

## Remplacé par {#superseded-by-this}

- 2025-05-13 — L'ancienne règle selon laquelle Starlight n'existe que dans le cloud ne vaut plus pour l'ensemble de la famille. Starlight Mini a reçu le rendu local sous Windows avec des GPU NVIDIA, bien que cela ne prouve pas la prise en charge locale du modèle `sl-1` original.
- 2025-09-17 — La répartition antérieure en deux modèles, Project Starlight et Starlight Mini, est obsolète. Starlight Sharp a rejoint la gamme de produits.

## Points toujours inconnus {#still-unknown}

- L'URL d'expérimentation originale ne prouve plus l'interface ou le niveau tarifaire actuels. Les points d'entrée actuels de Topaz mènent à Astra, Topaz Video et l'API.
- Nous n'avons pas vérifié directement le texte original du message X du 2025-02-06. Un message daté de la communauté Topaz publié le même jour en confirme le contenu.
- La date à laquelle Topaz a officiellement renommé Project Starlight en Starlight Precise 1 n'est pas consignée. La documentation actuelle confirme la continuité, mais pas la date du changement de nom.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://x.com/topazlabs/status/1887497602398073234 | Annonce de Topaz Labs concernant Project Starlight | 2026-09-05 |
| https://app.topazlabs.com/experiments/starlight | Expérimentation Project Starlight | 2026-09-05 |
| https://community.topazlabs.com/t/the-process-of-improving-video-quality-with-project-starlight/87143 | The process of improving video quality with Project Starlight | 2026-09-05 |
| https://community.topazlabs.com/t/project-starlight-video-ai-6-1-beta/87108?page=10 | Project Starlight - Video AI 6.1 Beta | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-ai-6-0-4/87385 | Topaz Video AI 6.0.4 | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-ai-6-1-2-6-1-3/88231 | Topaz Video AI 6.1.2 + 6.1.3 | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-ai-beta-6-2-0-0-b/89146 | Topaz Video AI Beta 6.2.0.0.b | 2026-09-05 |
| https://community.topazlabs.com/t/video-ai-7-0-new-starlight-mini-local-ai-model/90631 | Video AI 7.0 - NEW Starlight Mini (Local) AI Model | 2026-09-05 |
| https://community.topazlabs.com/t/topaz-video-1-0-0-new-studio-release/95523/1 | Topaz Video 1.0.0 (New Studio Release) | 2026-09-05 |
| https://developer.topazlabs.com/video-models/starlight/starlight-precise-1 | Starlight Precise 1 | Developer Documentation | 2026-09-05 |
| https://docs.topazlabs.com/topaz-video/project-starlight-series | Starlight Series | Topaz Video | 2026-09-05 |
| https://www.topazlabs.com/starlight | Project Starlight | AI Video Enhancement | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:project-starlight`, fil `project-starlight-public-rollout`, 2 événements datés du 2025-02-06 au 2025-02-11.
- **Note pratique :** Considérez la voie Topaz Labs Experiments à partir du 2025-02-11 comme un chemin de découverte daté pour Project Starlight. Vérifiez la page d'expérimentation actuelle avant toute utilisation, car ces liens seuls n'établissent ni les capacités ni les conditions d'accès.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
