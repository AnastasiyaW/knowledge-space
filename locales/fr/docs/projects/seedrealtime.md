---
title: "SeedRealtime"
category: projects
date: 2026-08-06
tags: [project, seedrealtime, seedrealtime-development]
aliases: ["SeedRealtime"]
level: 2
source_sha256: 02c8c2da877ead9c5a2a2200bf0d4d815055cf116a6115c31499dac45a55d8be
translation: machine
translated_at: '2026-10-24'
---
# SeedRealtime {#seedrealtime}

**Ligne de développement :** `project:seedrealtime` · fil `seedrealtime-development`  
**Dernier événement :** 2026-08-06 · 1 daté depuis le 2026-08-06 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

SeedRealtime est un LLM audio-visuel natif en full-duplex, destiné à la conversation en temps réel sur des flux continus d'audio, de vidéo et de texte.

- Liaison parole-image : relie les mots prononcés au contexte visuel.
- Timing conversationnel : décide quand parler.
- Gestion des interférences : gère les interruptions.
- Rappels proactifs : déclenche des alertes via des appels d'outils.

ByteDance indique deux fois moins de problèmes de rythme audio-visuel par rapport à des systèmes en cascade non nommés. Nous n'avons trouvé ni poids publics, ni API, ni tarification, ni rapport technique. Il s'agit d'une capacité produit déployée, et non d'une plateforme développeur documentée.

## Ligne de développement {#development-line}

- **2026-08-06 — Annonce de la sortie de SeedRealtime.** La version officielle est datée du 2026-08-05 et nomme le modèle SeedRealtime. ByteDance indique que le modèle a été déployé en totalité. La sortie fait état d'une réduction de moitié des problèmes de rythme conversationnel audio-visuel par rapport aux modèles en cascade.

## Ce qui a changé {#what-changed}

2026-04-09 — Seeduplex a ajouté la parole native en full-duplex à Doubao. ByteDance présentait l'entrée visuelle comme l'étape suivante.

2026-08-06 — SeedRealtime a livré cette étape audio-visuelle. L'annonce officielle est datée du 2026-08-05, et non du 2026-08-06. Elle nomme le modèle SeedRealtime et confirme un déploiement complet.

L'annonce du 2026-08-05 énumère trois capacités déclarées : compréhension conjointe audio-visuelle, interaction proactive et timing conversationnel. Elle illustre sept scénarios. Dans une évaluation humaine de bout en bout, les problèmes de rythme conversationnel ont été réduits de moitié par rapport aux modèles en cascade. C'est le seul chiffre comparatif que ByteDance a publié.

Le déploiement de Seeduplex dans Doubao, le 2026-04-09, ne portait que sur la parole et présentait l'entrée visuelle comme un travail futur. Il s'agit d'un prédécesseur antérieur, et non d'une version distincte de SeedRealtime.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-08-06, considérez SeedRealtime comme une ligne de modèles audio-visuels full-duplex annoncée. Consultez les documents de sortie officiels avant de vous appuyer sur une affirmation concernant ses capacités ou sa disponibilité.

1. Testez l'interaction continue caméra et voix dans le déploiement grand public. ByteDance ne fournit ni SDK, ni API, ni téléchargement de modèle, ni workflow d'intégration.
  — <https://seed.bytedance.com/en/blog/seedrealtime-audio-visual-full-duplex-llm-released-toward-omni-modal-natural-interaction>

## Bonnes pratiques {#best-practices}

- Ne traitez pas SeedRealtime comme une dépendance pour développeurs tant que ByteDance ne publie pas d'API, de poids ou de documentation d'intégration. Considérez les affirmations publiques comme des comportements de produit, et non comme des résultats de benchmark reproductibles.
  — <https://www.eesel.ai/blog/seedrealtime>
- Définissez des exigences explicites sur l'alternance des tours de parole et la gestion des interférences lorsque vous évaluez des agents temps réel. SeedRealtime identifie le timing, les bruits de fond et les scènes à plusieurs personnes comme des conditions de fonctionnement non résolues.
  — <https://seed.bytedance.com/en/blog/seedrealtime-audio-visual-full-duplex-llm-released-toward-omni-modal-natural-interaction>

## Remplacé par ceci {#superseded-by-this}

- 2026-04-09 — SeedRealtime ajoute la compréhension vidéo et temporelle native à la conception de Seeduplex, limitée à la parole. Cela n'invalide pas les affirmations de déploiement rapportées pour Seeduplex.

## Toujours inconnu {#still-unknown}

- L'annonce publique de ByteDance ne documente ni l'accès API, ni les poids, ni la tarification, ni un article technique, ni le nombre de paramètres, ni la configuration requise, ni un protocole de benchmark reproductible.
- L'événement cité est daté du 2026-08-06, mais l'annonce officielle est datée du 2026-08-05. L'écart d'un jour correspond probablement aux dates de publication et non à une seconde modification du produit.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://seed.bytedance.com/en/blog/seedrealtime-audio-visual-full-duplex-llm-released-toward-omni-modal-natural-interaction | SeedRealtime Audio-Visual Full-Duplex LLM Released: Toward Omni-Modal Natural Interaction | 2026-09-05 |
| https://seed.bytedance.com/en/blog/introducing-seed-full-duplex-speech-llm-attentive-listening-robust-interference-suppression-enabling-more-natural-interaction | Introducing Seed Full-Duplex Speech LLM: Attentive Listening, Robust Interference Suppression, Enabling More Natural Interaction | 2026-09-05 |
| https://www.eesel.ai/blog/seedrealtime | SeedRealtime: what ByteDance’s audio-visual model actually does | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:seedrealtime`, fil `seedrealtime-development`, 1 événement daté du 2026-08-06 au 2026-08-06.
- **Note pratique :** À partir du 2026-08-06, les praticiens qui évaluent SeedRealtime doivent le considérer comme une ligne de modèles audio-visuels full-duplex annoncée publiquement, et consulter les documents de sortie officiels avant de s'appuyer sur une affirmation de capacité ou de disponibilité.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
