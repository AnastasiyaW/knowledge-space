---
title: "Glob3R"
category: projects

tags: [glob3r, project]
aliases: ["Glob3R"]
level: 2
source_sha256: a1c970581b1f6f87b84b8720921633457bcffa4f9aced7058c589e9a2be220c1
translation: machine
translated_at: '2026-10-24'
---
# Glob3R {#glob3r}

**Ligne de développement :** `project:glob3r` · fil `glob3r`  
**Dernier événement :** - · 0 daté depuis - · **Consulté :** 2026-09-05 · confiance : élevée

## Qu'est-ce que c'est {#what-it-is}

Glob3R est un pipeline global de Structure-from-Motion hors ligne qui relie les prédictions de modèles 3D Pi3X figés à une mise en correspondance dense, aux pistes (tracks), à la moyenne de mouvements (motion averaging) et à l'ajustement de faisceaux (bundle adjustment).

- Ensembles d'images ordonnés et non ordonnés : traite à la fois les séquences et les collections d'images non ordonnées.
- Raffinement de la géométrie : affine conjointement les poses de caméras et la géométrie dense.
- Rôle dans le pipeline : conçu pour la reconstruction hors ligne plutôt que comme produit destiné à l'utilisateur final.

Le dépôt officiel ne contient qu'un README ; le code d'inférence et le script d'évaluation sont signalés comme TODO. Nous pouvons évaluer la méthode à partir de l'article, mais nous ne pouvons pas la déployer de manière reproductible à partir du dépôt officiel à ce jour.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; ce qui est connu figure dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

2026-07-16 — Glob3R est apparu comme pipeline de SfM global : les prédictions locales de Pi3X se transforment en pistes multi-vues et sont optimisées globalement.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-16, utilisez la page projet Glob3R liée uniquement comme point de départ pour une vérification auprès des sources primaires ; le seul lien daté ne justifie aucun changement d'implémentation ou de flux de travail.

1. Ne planifiez pas une exécution de production ou de recherche à partir du dépôt officiel : il ne contient ni code d'inférence, ni script d'évaluation, ni poids, ni instructions de lancement.
  — <https://github.com/aigc3d/Glob3R>
2. Utilisez l'article pour évaluer l'approche : fournissez une séquence d'images ou construisez un pseudo-séquence basé sur la recherche d'images pour un ensemble non ordonné ; la méthode utilise ensuite des fenêtres qui se chevauchent, des images clés, des pistes et une optimisation globale.
  — <https://arxiv.org/html/2607.09225>

## Bonnes pratiques {#best-practices}

- Construisez d'abord un pseudo-séquence par recherche d'images pour les images non ordonnées ; conservez l'ordre des images pour une séquence existante.
  — <https://arxiv.org/html/2607.09225>
- Ne remplacez pas l'optimisation globale par un simple assemblage de fenêtres : les images clés et le chevauchement des fenêtres sont nécessaires pour relier les poses et les pistes d'une fenêtre à l'autre.
  — <https://arxiv.org/html/2607.09225>
- Considérez les résultats de l'article comme une référence de recherche tant que le code et le script d'évaluation ne sont pas publiés.
  — <https://github.com/aigc3d/Glob3R>

## Remplacé par ceci {#superseded-by-this}

- Rien de marqué obsolète pour l'instant.

## Toujours inconnu {#still-unknown}

- Les dates du projet officiel et du dépôt n'apparaissent pas sur les pages elles-mêmes ; pour l'événement du 2026-07-16, seule la disponibilité de la page projet à cette date est confirmée.
- Le code d'inférence officiel, les poids, la licence, la configuration matérielle requise et les commandes de lancement reproductibles ne sont pas publiés au 2026-09-05.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://junyuandeng.github.io/Glob3r/ | Glob3R | Global Structure-from-Motion with 3D Foundation Models | 2026-09-05 |
| https://arxiv.org/abs/2607.09225 | Glob3R: Global Structure-from-Motion with 3D Foundation Models | 2026-09-05 |
| https://arxiv.org/html/2607.09225 | Glob3R: Global Structure-from-Motion with 3D Foundation Models | 2026-09-05 |
| https://github.com/aigc3d/Glob3R | aigc3d/Glob3R | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:glob3r`, fil `glob3r`, 0 événement daté - → -.
- **Note pratique :** Au 2026-07-16, utilisez la page projet Glob3R liée uniquement comme point de départ pour une vérification auprès des sources primaires ; le seul lien daté ne justifie aucun changement d'implémentation ou de flux de travail.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
