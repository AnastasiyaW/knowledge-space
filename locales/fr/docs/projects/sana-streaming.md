---
title: "SANA-Streaming — Streaming SANA"
category: projects
date: 2026-06-03
tags: [project, sana-streaming, sana_streaming]
aliases: ["SANA-Streaming"]
level: 2
source_sha256: 8d016585234049934f1d8225ea863394892e038bf4104c5b7dfaf81838dbcfb4
translation: machine
translated_at: '2026-10-24'
---
# SANA-Streaming — Streaming SANA {#sana-streaming-sana-streaming}

**Ligne de développement :** `project:sana-streaming` · fil `sana-streaming`  
**Dernier événement :** 2026-06-03 · 1 daté depuis le 2026-06-03 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

SANA-Streaming est un éditeur vidéo-vers-vidéo de 2B paramètres destiné aux créateurs qui ont besoin de modifications guidées par texte tout en conservant le mouvement source et les zones non modifiées.

- Édition en streaming longue : modifie des flux vidéo continus image par image.
- Édition bidirectionnelle courte : modifie des clips en exploitant à la fois le contexte avant et arrière.

La configuration temps réel annoncée fonctionne en 1280×704 à 24 FPS de bout en bout sur une seule RTX 5090. Le chemin d'inférence public utilise des points de contrôle en BF16, et non la recette de déploiement MPQ décrite dans l'article. Nous l'utilisons pour les travaux locaux de V2V long format lorsque son environnement d'exécution orienté NVIDIA et son flux de travail fixe en 720p correspondent à la tâche.

## Ligne de développement {#development-line}

- **2026-06-03 — Page projet SANA Streaming référencée.** Nous avons relié la ligne de développement de SANA Streaming à la page projet de NVIDIA consacrée à SANA Streaming, le 2026-06-03. Il s'agit d'un point de repère important pour l'historique public du projet. Les éléments disponibles n'établissent pas de version, de capacité ou d'affirmation de performance précise.

## Ce qui a changé {#what-changed}

- **2026-06-03** — NVIDIA a présenté SANA-Streaming comme un éditeur vidéo-vers-vidéo en streaming de 2B paramètres, en 720p, à l'échelle de la minute. L'article associé, daté du 2026-05-28, annonçait 24 FPS de bout en bout et 58 FPS DiT en 1280×704 sur une RTX 5090.
- **2026-07** — NVIDIA a publié la prise en charge de l'entraînement pour les chemins bidirectionnel et de distillation. Cela a étendu la publication initiale centrée sur l'inférence et les points de contrôle.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-03, partez de la page projet SANA Streaming pour consulter les documents officiels avant de vous fier à des synthèses secondaires.

1. Installez l'environnement du dépôt, activez l'environnement Conda `sana` et conservez les versions d'exécution épinglées documentées pour une inférence bidirectionnelle reproductible.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>
2. Lancez `long_streaming` avec le point de contrôle publié `sana_streaming_ar.pth` pour une vidéo source, une instruction textuelle et jusqu'à 969 images décodées. Les valeurs par défaut documentées utilisent quatre étapes de débruitage, un CFG de 1.0, deux blocs en cache et la mise en cache de jetons « sink ».
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>
3. Utilisez `bidirectional_short` avec `sana_bidirectional_short.pth` lorsqu'une modification de cinq secondes, soit 81 images, suffit. Les valeurs par défaut documentées utilisent 50 étapes et un CFG de 6.0.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>

## Bonnes pratiques {#best-practices}

- Conservez la configuration du dépôt propre à chaque mode et les versions épinglées des paquets. Les noyaux GDN fusionnés et le chemin VAE LTX-2 sont sensibles à la version.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>
- Considérez le chiffre de 24 FPS sur RTX 5090 comme un résultat MPQ co-conçu au niveau du système. Il ne garantit pas la commande d'inférence BF16 publiée.
  — <https://arxiv.org/abs/2605.30409>
- Utilisez le streaming long pour la longueur de séquence et le mode bidirectionnel pour les modifications courtes. Les points de contrôle publiés, les nombres d'images, les réglages d'échantillonnage et les hypothèses temporelles diffèrent entre les deux.
  — <https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md>

## Remplacé par ceci {#superseded-by-this}

- **2026-07** — La compréhension de juin, limitée à l'inférence, est incomplète. NVIDIA a ensuite publié les chemins d'entraînement bidirectionnel et de distillation.

## Toujours inconnu {#still-unknown}

- L'événement daté de juin ne mentionne ni commit de publication ni annonce spécifique à un jour donné. Nous ne pouvons pas établir indépendamment le périmètre exact de la publication du 2026-06-03 au-delà de l'avis de publication de juin et de la date de l'article, 2026-05-28.
- Le schéma de réponse fourni ne contient pas les champs `event_findings` et `new_events`. Nous reprenons leur contenu vérifié dans `what_changed` et `supersedes`.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://nvlabs.github.io/Sana/Streaming/ | SANA-Streaming | Real-time Streaming Video Editing | 2026-09-05 |
| https://github.com/NVlabs/Sana/blob/main/docs/sana_streaming.md | SANA-Streaming: Real-time Streaming Video Editing with Hybrid Diffusion Transformer | 2026-09-05 |
| https://github.com/NVlabs/Sana | NVlabs/Sana | 2026-09-05 |
| https://arxiv.org/abs/2605.30409 | SANA-Streaming: Real-time Streaming Video Editing with Hybrid Diffusion Transformer | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:sana-streaming`, fil `sana-streaming`, 1 événement daté du 2026-06-03 au 2026-06-03.
- **Note pratique :** Au 2026-06-03, les praticiens doivent utiliser la page projet SANA Streaming comme point de départ principal pour identifier les documents publics du projet, avant de se fier à des synthèses secondaires.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
