---
title: "ResearchStudio"
category: projects
date: 2026-07-07
tags: [project, researchstudio]
aliases: ["ResearchStudio"]
level: 3
source_sha256: 5c3dba54d1c92fd0ba761bac2f9d96e9a39d0955b378ed191d9089a48e5a1896
translation: machine
translated_at: '2026-10-24'
---
# ResearchStudio {#researchstudio}

**Ligne de développement :** `project:researchstudio` · fil `researchstudio`  
**Dernier événement :** 2026-07-07 · 1 événement daté depuis le 2026-07-07 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

ResearchStudio est une suite de skills pour Claude Code et Codex, sous licence MIT, couvrant deux étapes de la recherche.

- Idea : recherche dans la littérature, explore des pistes et vérifie les collisions avec l'art antérieur pour produire une fiche d'idée.
- Reel : transforme un article au format PDF en affiche, vidéo commentée, blog bilingue et reel interactif.

## Ligne de développement {#development-line}

- **2026-07-07 — Références publiques du projet ResearchStudio enregistrées.** Le 2026-07-07, des références publiques sont apparues pour le site du projet ResearchStudio de Microsoft et pour son dépôt GitHub. Elles montrent que le projet existe publiquement, mais ne confirment ni version publiée, ni ensemble de fonctionnalités, ni statut de lancement.

## Modifications {#what-changed}

- 2026-07-03 — ResearchStudio-Idea a publié le flux de travail précédant la rédaction de l'article : IdeaSpark, Paper-Search et Scoop-Check.
- 2026-07-05 — Les articles associés Idea et Reel ont documenté les conceptions d'idéation fondée sur des preuves et de diffusion à extraction partagée.
- 2026-07-08 — ResearchStudio-Reel a publié le pipeline post-article de cinq skills pour les sorties affiche, vidéo, blog bilingue et reel interactif.
- 2026-08-13 — IdeaSpark a commencé à conserver la requête complète, à résoudre les articles nommés et à enregistrer si la sélection suivait ou non une direction de solution énoncée.
- 2026-08-25 — Trending Paper a été publié comme point d'entrée basé sur les Reels pour parcourir la recherche.
- 2026-09-03 — IdeaSpark a ajouté un validateur de l'ordre des mots en chinois au niveau d'avertissement.

## Mode d'emploi {#how-to-use-this}

Consultez le site officiel de ResearchStudio et le dépôt source avant d'adopter le projet, tel qu'il était au 2026-07-07. Cette seule référence ne confirme aucun flux de travail, aucune capacité ni aucune version publiée en particulier.

1. Créez un environnement Python isolé avec conda (Python 3.10+) ou uv, puis installez à partir d'un clone avec install.sh ou via l'installateur interactif npx.
  — <https://github.com/microsoft/ResearchStudio/blob/main/README.md>
2. Pour une piste de recherche en amont, invoquez IdeaSpark avec le problème ainsi que les contraintes, les articles de départ et le budget de calcul ; utilisez Paper-Search et Scoop-Check lorsque ces parties sont nécessaires séparément.
  — <https://github.com/microsoft/ResearchStudio/tree/main/ResearchStudio-Idea>
3. Pour un article achevé, exécutez Paper2Assets une fois, puis utilisez son bundle partagé pour Paper2Poster, Paper2Video, Paper2Blog et Paper2Reel.
  — <https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md>
4. Consultez un reel interactif via le serveur HTTP fourni plutôt qu'en ouvrant directement son fichier HTML, car la recherche temporelle dans la vidéo nécessite la prise en charge des requêtes HTTP Range.
  — <https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md>

## Bonnes pratiques {#best-practices}

- Utilisez le niveau minimal de modèle capable recommandé et un environnement isolé avant d'installer les skills.
  — <https://github.com/microsoft/ResearchStudio/blob/main/README.md>
- Fournissez à IdeaSpark des contraintes concrètes, des articles de départ et des limites de calcul ; effectuez la vérification de l'art antérieur avant de considérer une affirmation de nouveauté comme exploitable.
  — <https://github.com/microsoft/ResearchStudio/tree/main/ResearchStudio-Idea>
- Réutilisez un même bundle Paper2Assets pour la génération de l'affiche, de la vidéo, du blog et du reel, afin que les livrables partagent les mêmes preuves extraites.
  — <https://microsoft.github.io/ResearchStudio/reel-page/>
- Conservez le HTML intermédiaire pendant les exécutions de Reel et validez la visionneuse finale via serve_reel.py.
  — <https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md>
- Pour les sorties Idea en chinois, passez à la version dotée du validateur de l'ordre des mots et examinez ses avertissements plutôt que de vous fier à une consigne de traduction générique.
  — <https://github.com/microsoft/ResearchStudio/commit/2540dde4be02dc841444f4ef7d81aa73aa6cf86e>

## Remplacé par ceci {#superseded-by-this}

- 2026-07-07 — Décrire ResearchStudio comme une version au cycle de vie complet publiée le même jour n'est pas étayé : l'historique officiel place Idea le 2026-07-03 et Reel le 2026-07-08.
- 2026-08-13 — La consigne qui traite un simple sujet comme l'intégralité du brief d'IdeaSpark est remplacée par la préservation de la requête, la résolution des articles nommés et la gestion explicite de la direction de solution.
- 2026-09-03 — « Un chinois naturel, pas mot à mot » comme seul contrôle est remplacé par un validateur documenté de l'ordre des mots au niveau d'avertissement.

## Points restant inconnus {#still-unknown}

- Aucune entrée de version officielle n'identifie une modification distincte de ResearchStudio le 2026-07-07 ; sans le texte source original, cette date ne peut être traitée que comme un point de découverte entre les versions Idea et Reel.
- Le dépôt n'expose aucune matrice de compatibilité par version étiquetée ; la reproductibilité exacte des dépendances et de l'environnement d'exécution reste donc non vérifiée.
- Nous n'avons pas reproduit de manière indépendante les résultats de référence publiés.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://microsoft.github.io/ResearchStudio/ | ResearchStudio — Votre co-auteur IA, de la problématique de recherche à la publication | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio | GitHub — microsoft/ResearchStudio | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/blob/main/README.md | ResearchStudio README | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/tree/main/ResearchStudio-Idea | ResearchStudio-Idea | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/blob/main/ResearchStudio-Reel/README.md | ResearchStudio-Reel README | 2026-09-05 |
| https://microsoft.github.io/ResearchStudio/reel-page/ | ResearchStudio-Reel Gallery | 2026-09-05 |
| https://arxiv.org/abs/2607.04439 | ResearchStudio-Idea: An Evidence-Grounded Research-Ideation Skill Suite from ML Conference Outcomes | 2026-09-05 |
| https://arxiv.org/abs/2607.04438 | ResearchStudio-Reel: Automate the Last Mile of Research from Paper to Poster, Video, and Blog | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/commits/main | Historique des commits de ResearchStudio | 2026-09-05 |
| https://github.com/microsoft/ResearchStudio/commit/2540dde4be02dc841444f4ef7d81aa73aa6cf86e | feat(idea-spark): l'ordre des mots chinois est une règle, pas une requête | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:researchstudio`, fil `researchstudio`, 1 événement daté du 2026-07-07 au 2026-07-07.
- **Remarque pratique :** Au 2026-07-07, les praticiens peuvent consulter le site officiel de ResearchStudio et le dépôt source avant d'évaluer ou d'adopter le projet ; cette seule ligne n'établit aucun flux de travail, aucune capacité ni aucune version publiée en particulier.
- **Confiance :** moyenne. Les mises à jour datées « Remplacé par ceci » font foi pour ce qui est devenu obsolète.
