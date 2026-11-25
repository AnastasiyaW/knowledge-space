---
title: "Stable Audio"
category: projects
date: 2025-09-12
tags: [model_release, project, stable-audio, stable-audio-releases]
aliases: ["Stable Audio"]
level: 2
source_sha256: e6f9da3e17b141e85cb22cfe685ab1b125a24d919d1b535d5754b50ceb137206
translation: machine
translated_at: '2026-10-24'
---
# Stable Audio {#stable-audio}

**Ligne de développement :** `project:stable-audio` · fil `stable-audio-releases`  
**Dernier événement :** 2025-09-12 · 2 événements datés depuis 2023-09-13 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

Stable Audio est une application web, une API et une famille de modèles pour la génération de l'audio à partir de texte, la transformation audio vers audio, l'inpainting et l'édition audio.

- Musique : génère des pistes et des mixages complets.
- SFX : crée des effets sonores et des extraits audio.
- Échantillons et variations : crée des versions alternatives.
- Pistes séparées : isole des stems individuels.
- Exécution locale : exécute certains modèles à poids ouverts.

Les limites dépendent du modèle : Stable Audio 3.0 Medium et Large sont évalués pour plus de six minutes. Pour tout nouveau travail, privilégiez Stable Audio 3.0 et ses modes de déploiement plutôt que les limites des versions 1.0 ou 2.5.

## Ligne de développement {#development-line}

- **2023-09-13 — Stable Audio a été lancé.** La génération de texte vers audio dans le navigateur crée de l'audio à partir de prompts textuels et de durées cibles.
- **2025-09-12 — Stable Audio 2.5 a été lancé pour la production sonore en entreprise.** Pistes de trois minutes, texte vers audio, audio vers audio et inpainting audio.

## Évolutions {#what-changed}

- 2023-09-13 — Stable Audio est sorti comme produit commercial, avec la génération de texte vers audio dans le navigateur à partir de descriptions et de durées définies.
- 2025-09-12 — Stable Audio 2.5 est arrivé pour la production audio en entreprise, avec des pistes de trois minutes, la génération de texte vers audio, la transformation audio vers audio et l'inpainting audio.
- 2026-05-20 — Stable Audio 3.0 a été lancé avec les modèles à poids ouverts Small SFX, Small et Medium, ainsi que le modèle Large accessible via l'API et en auto-hébergement. La durée de génération dépasse six minutes pour Medium et Large.

## Mode d'emploi {#how-to-use-this}

À partir du 2023-09-13, les praticiens pouvaient considérer Stable Audio comme un produit dédié à la génération audio ; à partir du 2025-09-12, ils devraient évaluer Stable Audio 2.5 et sa disponibilité dans ComfyUI lorsqu'un flux de production sonore orienté entreprise est nécessaire.

1. Choisissez une voie : Studio dans le navigateur pour la création et les modifications, Small SFX, Small ou Medium à poids ouverts pour une infrastructure locale, ou l'API et Large en auto-hébergement pour des produits à fort volume.
  — <https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models>
2. Créez une session et commencez par Full Mix, en indiquant dans le prompt le genre, les instruments, le tempo, l'ambiance et la durée cible.
  — <https://stableaudio.com/docs>
3. Utilisez Multi-Track pour une arrangement structuré, et ne joignez des références que pour guider le tempo et la tonalité.
  — <https://stableaudio.com/docs>
4. Corrigez une piste individuelle ou une plage temporelle avec regenerate, replace section ou extend, puis exportez le mixage finalisé.
  — <https://stableaudio.com/docs>

## Bonnes pratiques {#best-practices}

- Rédigez des prompts précis : le genre, les instruments, le BPM, l'ambiance et l'époque contrôlent mieux le résultat qu'une simple étiquette de genre générale.
  — <https://stableaudio.com/docs>
- Commencez par Full Mix lorsque l'interprétation littérale du prompt compte ; Multi-Track facilite le mixage par stems, mais son agent d'arrangement peut s'écarter du prompt.
  — <https://stableaudio.com/docs>
- Choisissez Small SFX ou Open Small pour les effets sonores courts, le foley et les éléments de production ; choisissez Small, Medium ou Large pour la musique complète selon la durée et l'infrastructure d'hébergement.
  — <https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models>
- Ne téléversez pas d'audio protégé par le droit d'auteur dans les outils de transformation audio vers audio ou d'inpainting : les conditions exigent que les contenus téléversés ne portent pas atteinte aux droits d'auteur.
  — <https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale>

## Remplacé par ce qui suit {#superseded-by-this}

- 2023-09-13 — Les limites du premier produit web : jusqu'à 45 secondes dans l'offre gratuite et 90 secondes dans l'offre Pro ne décrivent plus la gamme active ; 3.0 Medium et Large génèrent pour plus de six minutes.
- 2025-09-10 — La présentation de Stable Audio 2.5 comme dernier modèle est devenue obsolète dès le lancement de Stable Audio 3.0 le 2026-05-20.

## Points encore inconnus {#still-unknown}

- Les grilles tarifaires actuelles, les quotas de crédits et les intégrations avec des partenaires évoluent indépendamment des sorties de modèles ; vérifiez la disponibilité directement sur le canal d'accès choisi avant tout achat ou déploiement en production.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://stableaudio.com/ | Stable Audio — IA générative pour la musique et les effets sonores | 2026-09-05 |
| https://stableaudio.com/docs | Comment utiliser Stable Audio | 2026-09-05 |
| https://stability.ai/news-updates/stable-audio-using-ai-to-generate-music | Présentation de Stable Audio, un produit de génération musicale et sonore | 2026-09-05 |
| https://stability.ai/news-updates/stability-ai-introduces-stable-audio-25-the-first-audio-model-built-for-enterprise-sound-production-at-scale | Stability AI présente Stable Audio 2.5, le premier modèle audio conçu pour la production sonore à grande échelle en entreprise | 2026-09-05 |
| https://stability.ai/news-updates/stable-audio-2-0 | Présentation de Stable Audio 2.0 | 2026-09-05 |
| https://stability.ai/news-updates/introducing-stable-audio-open | Présentation de Stable Audio Open — un modèle open source pour les échantillons audio et le sound design | 2026-09-05 |
| https://stability.ai/news-updates/stability-ai-and-arm-release-stable-audio-open-small-enabling-real-world-deployment-for-on-device-audio-control | Stability AI et Arm collaborent pour publier Stable Audio Open Small, permettant un déploiement concret de la génération audio sur appareil | 2026-09-05 |
| https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models | Découvrez Stable Audio 3.0, la famille de modèles conçue pour l'expérimentation artistique avec des modèles à poids ouverts | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:stable-audio`, fil `stable-audio-releases`, 2 événements datés du 2023-09-13 au 2025-09-12.
- **Remarque pratique :** À partir du 2023-09-13, les praticiens pouvaient considérer Stable Audio comme un produit dédié à la génération audio ; à partir du 2025-09-12, ils devraient évaluer Stable Audio 2.5 et sa disponibilité dans ComfyUI lorsqu'un flux de production sonore orienté entreprise est nécessaire.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
