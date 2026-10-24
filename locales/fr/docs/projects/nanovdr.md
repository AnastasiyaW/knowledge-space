---
title: "NanoVDR"
category: projects
date: 2026-03-17
tags: [nanovdr, nanovdr-public-release, project]
aliases: ["NanoVDR"]
level: 2
source_sha256: e70f2d040d188f53e961f507741934d70a8d5fcccaf24ac406596d36573e2174
translation: machine
translated_at: '2026-10-24'
---
# NanoVDR {#nanovdr}

**Ligne de développement :** `project:nanovdr` · fil `nanovdr-public-release`  
**Dernier événement :** 2026-03-17 · 1 événement daté depuis le 2026-03-17 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

NanoVDR est un système de recherche de documents visuels destiné aux équipes qui recherchent dans des pages PDF, des rapports et des images de pages. Il se présente comme un remplacement côté requête, et non comme un indexeur de documents autonome.

- Indexeur de documents : indexe les pages hors ligne avec Qwen3-VL-Embedding-2B.
- Encodeur de requêtes : encode les requêtes textuelles avec des modèles élèves de 69 à 151 millions de paramètres.
- Scoreur : classe les vecteurs compatibles à l'aide d'un produit scalaire.

Le modèle de requêtes multilingue de 69 M s'exécute à 51 ms par requête sur CPU et nécessite des documents indexés par le modèle enseignant.

## Ligne de développement {#development-line}

- **2026-03-17 — NanoVDR a publié des ressources publiques Hugging Face et une démo.** Le 2026-03-17, la ligne a publié un article de blog Hugging Face, une page de projet et un espace de démonstration. Cela a permis de rendre le projet et sa démonstration découvrables pour la diffusion publique, bien que nous n'ayons pas examiné leur contenu pour cette revue.

## Ce qui a changé {#what-changed}

- **2026-03-17** — NanoVDR a été présenté comme un encodeur de requêtes texte seul de 69 M, distillé à partir de Qwen3-VL-Embedding-2B pour la recherche de documents visuels. L'article de première main est daté du 2026-03-16 et indique une conservation de 95,1 % des performances du modèle enseignant pour NanoVDR-S-Multi.
- **2026-08-11** — Les noms des points de contrôle ont été modifiés pour indiquer la tour d'encodage, le modèle enseignant et la largeur des embeddings. Les anciens liens redirigent.
- **2026-08-29** — L'équipe a publié la version 3 sur arXiv. Le dépôt du projet distingue les travaux ultérieurs sur la tour documentaire DistilVDR de la ligne d'origine, consacrée à la tour de requêtes NanoVDR.

## Comment l'utiliser {#how-to-use-this}

Consultez les ressources Hugging Face liées et la démo publique avant toute évaluation, telles qu'elles étaient au 2026-03-17 ; les capacités, les prérequis et les résultats précis n'ont pas été vérifiés.

1. Chargez un point de contrôle de requêtes compatible avec SentenceTransformers, puis encodez la requête textuelle.
  — <https://github.com/Ryenhails/NanoVDR>
2. Pour la ligne d'origine de NanoVDR, indexez les pages hors ligne avec Qwen3-VL-Embedding-2B, puis classez leurs vecteurs de pages par rapport au vecteur de requête à l'aide d'un produit scalaire.
  — <https://huggingface.co/nanovdr>
3. N'utilisez la démo hébergée que pour des requêtes exploratoires ; elle peut être en veille jusqu'à son redémarrage.
  — <https://huggingface.co/spaces/nanovdr/NanoVDR-Demo>

## Bonnes pratiques {#best-practices}

- Faites correspondre les tours de requêtes et de documents à la fois par modèle enseignant et par largeur d'embedding ; les vecteurs issus d'espaces enseignants différents ne sont pas interchangeables.
  — <https://github.com/Ryenhails/NanoVDR>
- Privilégiez le point de contrôle de requêtes multilingue `-ML`, sauf si un modèle exclusivement anglophone est explicitement requis.
  — <https://github.com/Ryenhails/NanoVDR>
- Utilisez la ligne d'origine pour le service de requêtes sur CPU avec des index construits par le modèle enseignant ; n'utilisez la paire DistilVDR que lorsqu'une indexation sans modèle enseignant est nécessaire.
  — <https://github.com/Ryenhails/NanoVDR>

## Remplacé par ceci {#superseded-by-this}

- **2026-08-11** — Les noms de points de contrôle indiquant la tour, le modèle enseignant et la largeur du vecteur remplacent les noms antérieurs ; les anciens liens de modèles redirigent.

## Toujours inconnu {#still-unknown}

- Les champs event_findings et new_events sont absents du schéma de réponse ; les ajouts datés figurent donc dans what_changed.
- Un article de première main daté du 2026-03-16 corrobore l'événement du 2026-03-17.
- La renommation du 2026-08-11 et la version 3 sur arXiv du 2026-08-29 relèvent de mises à jour ultérieures, et non de l'événement du 2026-03-17.
- La démo publique était en veille lors de la vérification ; une exécution interactive n'est donc pas vérifiée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/blog/Ryenhails/nanovdr | NanoVDR : un modèle de 70 M, texte seul, qui retrouve des documents visuels aussi bien qu'un VLM de 2 B | 2026-09-05 |
| https://huggingface.co/nanovdr | Page de l'organisation nanovdr (NanoVDR) | 2026-09-05 |
| https://huggingface.co/spaces/nanovdr/NanoVDR-Demo | NanoVDR Demo | 2026-09-05 |
| https://github.com/Ryenhails/NanoVDR | Ryenhails/NanoVDR | 2026-09-05 |
| https://arxiv.org/abs/2603.12824 | NanoVDR : distillation d'un retriever vision-langage de 2 B en un encodeur texte seul de 70 M pour la recherche de documents visuels | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:nanovdr`, fil `nanovdr-public-release`, 1 événement daté, du 2026-03-17 au 2026-03-17.
- **Remarque pratique :** au 2026-03-17, les praticiens doivent consulter les ressources de projet Hugging Face liées à NanoVDR et la démo publique avant de l'évaluer ; les capacités, les prérequis et les résultats précis n'ont pas été vérifiés.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
