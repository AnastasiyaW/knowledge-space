---
title: "Disney Research — Édition générative interactive de mouvement"
category: organizations
tags: [disney-research, disney_research, interactive-generative-motion-editing, organization]
aliases: ["Disney Research"]
level: 2
source_sha256: 30f6ca9c687d9a5dafc4bb6310fc4806fb4d2ade079ef0c9331e1138e2fb5bf5
translation: machine
translated_at: '2026-10-24'
---
# Disney Research — Édition générative interactive de mouvement {#disney-research-interactive-generative-motion-editing}

**Ligne de développement :** `organization:disney-research` · fil `interactive-generative-motion-editing`  
**Événements :** 1 daté, 2026-08-01 → 2026-08-01 · **Recherché le :** 2026-09-03 · confiance : moyenne

## Présentation {#what-it-is}

Disney Research — DisneyResearch|Studios publie des travaux de recherche en apprentissage automatique et en informatique visuelle destinés aux équipes d'animation, d'effets visuels (VFX) et de recherche. — articles publics et démonstrations techniques ; — travaux de 2022 sur le rajeunissement et le vieillissement de visages dans la vidéo ; — travaux de 2026 sur l'édition de mouvement squelettique. Limite : les pages officielles examinées décrivent des articles et des vidéos, et non un installateur public, une API ni une publication du code source. Verdict : à utiliser comme référence de R&D ou cible de reproduction, et non comme outil prêt à l'emploi.

## Ligne de développement {#development-line}

- **2026-08-01 — Disney Research a documenté l'édition générative interactive de mouvement par inpainting planifié.** Le 2026-08-01, cette ligne a enregistré le travail de Disney Research intitulé « Interactive Generative Motion Editing via Scheduled Inpainting », publié sur son site Studios. Le lien vidéo associé indique que ce travail comprenait une démonstration visuelle de l'approche d'édition de mouvement.

## Ce qui a changé {#what-changed}

Disney Research — les éléments datés sont des publications de recherche, et non des versions d'un même produit. — 2022-12-02 : la vidéo liée documente FRAN, publié par Disney Research le 2022-11-30 : une approche U-Net de rajeunissement de visages dans la vidéo, avec contrôle localisé par les artistes, visant à réduire la peinture 2D image par image tout en préservant l'identité et la stabilité temporelle. — 2026-08-01 : la publication liée, datée du 2026-07-30 par Disney et du 2026-07-31 sur arXiv, présente l'inpainting planifié : une méthode d'inférence permettant d'éditer des modèles génératifs pré-entraînés de mouvement squelettique au moyen d'un calendrier de préservation et d'un masque spatio-temporel ; elle permet l'extension, l'assemblage (stitching) et la composition (compositing) sans entraînement supplémentaire. — Constaté aujourd'hui (2026-09-04) : DisneyResearch|Studios se présente toujours comme une organisation de recherche en apprentissage automatique et en informatique visuelle, avec des publications en cours. Limite : les travaux récents portent sur le mouvement du corps, et non sur le rajeunissement facial. Verdict : l'inpainting planifié ne remplace pas FRAN ; il s'agit de deux axes de recherche distincts.

## Mode d'emploi {#how-to-use-this}

Au 2026-08-01, les praticiens qui évaluent des flux de travail d'édition générative de mouvement devraient considérer l'approche d'inpainting planifié de Disney Research comme une orientation de recherche documentée, et examiner la démonstration liée avant de choisir une implémentation.

1. Choisir un résultat de recherche précis dans le catalogue actuel ; Disney Research est un éditeur de travaux en apprentissage automatique et en informatique visuelle, et non un point d'accès logiciel.
  — <https://studios.disneyresearch.com/research/>
2. Considérer l'inpainting planifié comme une cible de reproduction ou de prototype interne : la page officielle fournit un article et une démonstration, et non une installation publique nommée, une API ou un dépôt de code.
  — <https://studios.disneyresearch.com/2026/07/30/interactive-generative-motion-editing-via-scheduled-inpainting/>
3. Fournir un extrait de mouvement squelettique de base et des contraintes articulaires spatiales à un modèle génératif de mouvement pré-entraîné qui prend en charge la manipulation directe.
  — <https://arxiv.org/html/2607.29133>
4. Définir un calendrier de préservation temporelle et un masque par articulation et par image : conserver le mouvement inchangé et permettre la synthèse autour de la modification visée ; utiliser le même mécanisme pour l'extension, l'assemblage ou la composition.
  — <https://arxiv.org/html/2607.29133>
5. Examiner les sorties quant au respect des contraintes, à la continuité, au glissement des pieds et au comportement en dehors de la distribution de mouvements apprise par le modèle, avant de les intégrer à un pipeline d'animation.
  — <https://arxiv.org/html/2607.29133>

## Bonnes pratiques {#best-practices}

- Effectuer d'abord la modification structurelle globale avec des contraintes sur tout le corps, puis affiner les courbes de mouvement avec des contraintes individuelles de position et d'orientation.
  — <https://arxiv.org/html/2607.29133>
- Aligner l'origine et la direction de l'extrait et normaliser l'échelle avant de mélanger des mouvements ; l'article associe l'absence d'alignement à des déformations, des discontinuités et des artefacts de glissement.
  — <https://arxiv.org/html/2607.29133>
- Utiliser une zone d'influence gaussienne à décroissance régulière autour d'une modification, afin que les images voisines restent en partie ancrées au mouvement de base au lieu de changer brusquement de cadence.
  — <https://arxiv.org/html/2607.29133>
- Ne pas attendre une reconstruction fiable loin de la distribution de mouvements apprise par le modèle ; un mouvement exagéré ou périodique peut nécessiter des contraintes d'extrema supplémentaires, ce qui crée davantage de contraintes à gérer ultérieurement.
  — <https://arxiv.org/html/2607.29133>

## Remplacé par {#superseded-by-this}

- Rien de marqué comme obsolète pour l'instant.

## Points encore inconnus {#still-unknown}

- Les travaux de 2022 sur le rajeunissement facial et ceux de 2026 sur le mouvement squelettique partagent une organisation, mais aucune source examinée n'établit de relation de prédécesseur ou de successeur entre eux.
- Les pages officielles de projet examinées ne mentionnent ni dépôt de code public, ni poids, ni API, ni installateur, ni licence ; la disponibilité publique d'une implémentation n'est pas vérifiée.
- Aucune source de première main en chinois n'a été trouvée lors de la recherche limitée d'aujourd'hui.
- Les sources examinées ne précisent pas si l'une ou l'autre méthode a été déployée dans une production Disney après leur publication.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://studios.disneyresearch.com/research/ | Research | Disney Research Studios | 2026-09-04 |
| https://www.youtube.com/watch?v=ZP1ApcdyAjk | Production Ready Face Re Aging for Visual Effects - YouTube | 2026-09-04 |
| https://studios.disneyresearch.com/2022/11/30/production-ready-face-re-aging-for-visual-effects/ | Production-Ready Face Re-Aging for Visual Effects | Disney Research Studios | 2026-09-04 |
| https://studios.disneyresearch.com/2026/07/30/interactive-generative-motion-editing-via-scheduled-inpainting/ | Interactive Generative Motion Editing via Scheduled Inpainting | Disney Research Studios | 2026-09-04 |
| https://arxiv.org/html/2607.29133 | Interactive Generative Motion Editing via Scheduled Inpainting | 2026-09-04 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `organization:disney-research`, fil `interactive-generative-motion-editing`, 1 événement daté du 2026-08-01 au 2026-08-01.
- **Note pratique :** Au 2026-08-01, les praticiens qui évaluent des flux de travail d'édition générative de mouvement devraient considérer l'approche d'inpainting planifié de Disney Research comme une orientation de recherche documentée, et examiner la démonstration liée avant de choisir une implémentation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
