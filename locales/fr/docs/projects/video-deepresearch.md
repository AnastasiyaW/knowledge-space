---
title: "Video-DeepResearch"
category: projects
date: 2026-08-10
tags: [project, video-deepresearch]
aliases: ["Video-DeepResearch"]
level: 2
source_sha256: 0e6390d3b276f1634066f7f76499c75c1481632c4138020726a5f21b8883fb41
translation: machine
translated_at: '2026-10-24'
---
# Video-DeepResearch {#video-deepresearch}

**Ligne de développement :** `project:video-deepresearch` · fil `video-deepresearch`  
**Dernier événement :** 2026-08-10 · 1 événement daté depuis le 2026-08-10 · **Recherché le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Video-DeepResearch est un écosystème de recherche ouvert et deux modèles destinés aux questions ancrées dans des objets et des événements vidéo, avant la vérification de sources externes.

- Sélection des images clés : sélectionne les images de la vidéo.
- Recherche par recadrage : examine des sous-régions visuelles.
- Recherche textuelle : interroge des sources externes.
- Extraction de preuves : extrait des preuves structurées à partir de pages web.

L'exécution de la configuration documentée nécessite des services distincts pour l'inférence, le juge et l'extraction ; les points de contrôle bruts et les clés d'API ne les remplacent pas. Cet ensemble convient à l'évaluation reproductible et au réglage fin d'agents ancrés dans la vidéo, et non à un service de chat autonome.

## Ligne de développement {#development-line}

- **2026-08-10 — Publication du projet public Video-DeepResearch et enregistrement des références sources.** La tâche vidéo se détache de Vision-DeepResearch, antérieur et centré sur l'image, et impose un ancrage visuel avant toute recherche web.

## Ce qui a changé {#what-changed}

2026-08-10 — Video-DeepResearch est apparu sous la forme d'une page de projet et d'une section dans le dépôt Vision-DeepResearch : la tâche vidéo se détache de Vision-DeepResearch, antérieur et centré sur l'image, et impose un ancrage visuel avant toute recherche web.

## Comment l'utiliser {#how-to-use-this}

À la date du 2026-08-10, évaluez Video-DeepResearch à partir de la page de projet et du dépôt source liés, et vérifiez directement les capacités et l'état de publication.

1. Clonez le dépôt et travaillez dans le sous-dossier Video-DeepResearch ; il contient des modules distincts de prétraitement, d'évaluation, de SFT et de RL.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
2. Extrayez les images clés de la vidéo ; la documentation recommande un filtrage par similarité CLIP, la différence de pixels ne servant que de solution de repli approximative.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
3. Lancez un VLM pour l'inférence, un juge séparé compatible OpenAI et le serveur d'extraction requis pour Visit ; l'exemple utilise Qwen3-VL-30B-A3B-Instruct pour le juge et l'extraction.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
4. Lancez un script d'évaluation pour SGLang, vLLM ou MaaS compatible OpenAI, puis choisissez le mode tool, direct ou both.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>

## Bonnes pratiques {#best-practices}

- Recueillez des preuves à partir des images et des recadrages avant d'ouvrir la recherche textuelle : cet ordre empêche l'agent de répondre de mémoire ou à partir d'une seule requête textuelle.
  — <https://costaliya.github.io/Video-DeepResearch/>
- Utilisez la similarité cosinus CLIP pour les images clés ; n'utilisez la différence de pixels que lorsque CLIP est indisponible, en tenant compte d'une sélection moins fine.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
- Gardez le serveur d'extraction en fonctionnement : sans lui, Visit renvoie du HTML brut au lieu de preuves structurées, et la documentation avertit que la précision agentique chute fortement.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>
- Comparez les modes tool et direct à l'aide d'un juge indépendant, afin de distinguer les gains de la recherche des réponses fondées uniquement sur les images clés.
  — <https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Toujours inconnu {#still-unknown}

- Les documents publics confirment les annonces de code, d'article et de points de contrôle, mais nous n'avons pas exécuté d'inférence et n'avons pas vérifié la disponibilité actuelle, la licence et les besoins matériels de chaque point de contrôle.
- VideoDR-Bench500 est annoncé comme « bientôt disponible » ; nous ne pouvons ni le considérer comme publié ni l'utiliser pour une comparaison.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://costaliya.github.io/Video-DeepResearch/ | Video-DeepResearch: Towards the Next-Generation Multimodal Deepresearch Agent | 2026-09-05 |
| https://github.com/Osilly/Vision-DeepResearch | Osilly/Vision-DeepResearch | 2026-09-05 |
| https://github.com/Osilly/Vision-DeepResearch/blob/main/Video-DeepResearch/README.md | Video-DeepResearch README | 2026-09-05 |
| https://arxiv.org/abs/2608.03979 | Video-DeepResearch: Towards the Next-Generation Multimodal Deepresearch Agent | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:video-deepresearch`, fil `video-deepresearch`, 1 événement daté du 2026-08-10 au 2026-08-10.
- **Note pratique :** À la date du 2026-08-10, les praticiens doivent utiliser la page de projet et le dépôt source liés comme points de départ pour évaluer Video-DeepResearch, tout en vérifiant indépendamment ses capacités et son état de publication.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
