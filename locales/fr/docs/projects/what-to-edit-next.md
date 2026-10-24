---
title: "Que modifier ensuite — Référence du site public"
category: projects
date: 2026-08-17
tags: [alibaba/what-to-edit-next, project, public-site-reference, what-to-edit-next]
aliases: ["What to Edit Next"]
level: 2
source_sha256: ff3092ba99717b66d4bad1fc645e9e2c015c9d5403103929f3660fdfe43f5f0f
translation: machine
translated_at: '2026-10-24'
---
# Que modifier ensuite — Référence du site public {#what-to-edit-next-public-site-reference}

**Ligne de développement :** `project:what-to-edit-next` · fil `public-site-reference`  
**Dernier événement :** 2026-08-17 · 1 événement daté depuis le 2026-08-17 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

What to Edit Next est une méthode de l'application Qwen qui suggère la prochaine modification à partir de la dernière image, de la requête courante et de l'intention d'édition.

- Politique Qwen3-VL-8B affinée avec des intentions sélectionnées et des retours de clics.
- Vérificateur image-first Qwen3-VL-30B-A3B qui rejette, pendant l'entraînement, les modifications non étayées ou redondantes.

## Ligne de développement {#development-line}

- **2026-08-17 — Le site public de What to Edit Next a été référencé.** La page du projet What to Edit Next a été liée afin d'établir une référence de site. Elle n'atteste que cette référence, et non un lancement, une sortie de fonctionnalité, une publication de code ni un changement d'accès public.

## Ce qui a changé {#what-changed}

- 2026-08-03 : What to Edit Next v1 a été soumis sur arXiv, documentant la méthode Qwen App en trois étapes.
- 2026-08-17 : la page du projet What to Edit Next a été liée ; cela n'établit qu'une référence de site, et non un lancement documenté, une sortie de fonctionnalité, une publication de code ni un changement d'accès public.
- 2026-08-18 : What to Edit Next arXiv v2 a été soumis ; son historique de versions ne fournit aucun journal des révisions.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-17, commencez par le site public du projet lié pour évaluer What to Edit Next. Vérifiez directement les documents sources avant de supposer des fonctionnalités ou l'état de publication.

1. Commencez par la page du projet pour évaluer la méthode, et non pour l'installer. Sa navigation visible expose des éléments sur l'article, arXiv et la méthode, et non un point d'entrée public d'intégration.
  — <https://what-to-edit-next.github.io/>
2. Pour une implémentation comparable, construisez chaque entrée à partir de la dernière image, de la requête courante reformulée et de l'intention d'édition. Générez cinq à sept suggestions et sélectionnez-en trois au hasard pour l'affichage.
  — <https://arxiv.org/html/2608.07565v1>
3. Validez les modifications en partant de l'image. Inventoriez l'image, décomposez chaque candidat en sources requises et cibles souhaitées, puis rejetez les sources absentes et les cibles déjà satisfaites. Un objet ajouté est une cible et n'a pas besoin d'être déjà visible.
  — <https://arxiv.org/html/2608.07565v1>

## Bonnes pratiques {#best-practices}

- N'optimisez pas uniquement les clics. Les auteurs signalent que l'incohérence visuelle passe de 3,0 % après SFT à 3,7 % après RL sur les clics, puis tombe à 0,9 % avec la récompense d'ancrage.
  — <https://arxiv.org/html/2608.07565v1>
- Observez l'image avant d'interpréter les instructions candidates. Gardez séparées les vérifications d'existence de la source et les vérifications de l'état cible.
  — <https://arxiv.org/html/2608.07565v1>
- Considérez l'article comme un contrat de décision plutôt que comme un paquet de production reproductible. Il omet les prompts de production textuels, les lexiques propres au produit et les déclencheurs exacts de post-traitement.
  — <https://arxiv.org/html/2608.07565v1>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-18 : arXiv v1 (2026-08-03) a cessé d'être la dernière version de l'article lorsque v2 a été soumis. N'attribuez pas à la date du 2026-08-17 les éléments propres à v2.

## Toujours inconnu {#still-unknown}

- La page du projet ne comporte aucun horodatage de publication. Son contenu et sa disponibilité au 2026-08-17 ne peuvent pas être établis à partir de la page actuelle.
- Les liens visibles ne prouvent pas que du code, des poids, une API ou une démo n'existent pas ailleurs.
- arXiv v2 ne comporte aucune note de révision ; ses différences substantielles avec v1 sont donc inconnues.
- Aucune annonce chinoise datée et de première main, ni guide public d'implémentation, n'a été trouvée dans les sources consultées.
- L'unique enregistrement daté et la prépublication correspondante désignent un seul sujet ; aucun second projet portant le même nom n'a été trouvé.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://what-to-edit-next.github.io/ | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems | 2026-09-05 |
| https://arxiv.org/abs/2608.07565v1 | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems, arXiv v1 | 2026-09-05 |
| https://arxiv.org/html/2608.07565v1 | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems, arXiv HTML v1 | 2026-09-05 |
| https://arxiv.org/abs/2608.07565 | What to Edit Next: Visually Aligned Image-Editing Follow-Up Suggestions in Conversational Systems, historique des versions arXiv | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:what-to-edit-next`, fil `public-site-reference`, 1 événement daté du 2026-08-17 au 2026-08-17.
- **Note pratique :** Au 2026-08-17, commencez l'évaluation par le site public du projet lié. Vérifiez directement les documents sources avant de supposer des fonctionnalités ou l'état de publication.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
