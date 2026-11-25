---
title: "video_to_world"
category: projects
date: 2026-03-23
tags: [project, video-to-world]
aliases: ["video_to_world"]
level: 3
source_sha256: 78a2afcb8f8ea2cb0206d3c9a28dc1cb218d50c88a29be6a12e05d697318056c
translation: machine
translated_at: '2026-10-24'
---
# video_to_world {#video_to_world}

**Ligne de développement :** `project:video-to-world` · fil `video-to-world`  
**Dernier événement :** 2026-03-23 · 1 événement daté depuis 2026-03-23 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

video_to_world est un code de recherche local pour ECCV 2026, destiné aux personnes qui reconstruisent une séquence vidéo générée sous forme de scène 2DGS ou 3DGS explorable ; il ne s'agit ni d'un générateur vidéo, ni d'un service hébergé.

- Depth Anything 3 estime la géométrie et les caméras image par image.
- Un ICP non rigide frame-to-model et une optimisation globale consolident les vues incohérentes.
- Une optimisation de splats gaussiens tenant compte de la déformation inverse produit la scène.

## Ligne de développement {#development-line}

- **2026-03-23 — Les ressources du projet Video-to-World ont été publiées en ligne.** La page du projet et le dépôt ont été recensés ; les sources de première main n'identifient pas cette date comme une date de publication en amont.

## Ce qui a changé {#what-changed}

2026-03-17 : la v1 sur arXiv et le commit initial du dépôt ont rendu public l'article et le premier code. 2026-03-18 : la v2 sur arXiv est devenue la version courante ; les commits du dépôt ont ajouté la référence arXiv/BibTeX, des mises à jour de l'installation et une correction du chemin de l'évaluation automatique. 2026-03-23 : la page du projet et le dépôt ont été recensés ; les sources de première main n'identifient pas cette date comme une date de publication en amont. 2026-03-26 : le mainteneur a ajouté le fichier LICENSE au dépôt. 2026-04-27 : le mainteneur a fait un commit intitulé « Release sample data » ; le README actuel fournit les données de la scène de l'article, mais le détail exact des fichiers ajoutés n'a pas été vérifié de manière indépendante.

## Comment l'utiliser {#how-to-use-this}

Au 2026-03-23, les praticiens peuvent utiliser la page du projet et le dépôt GitHub liés comme point de départ pour évaluer le projet Video-to-World et les ressources d'implémentation disponibles.

1. Cloner la branche main, créer un environnement Conda Python 3.10, conserver numpy<2 et opencv-python<4.12, puis épingler Depth Anything 3 au commit documenté et appliquer le patch d'export de trajectoire fourni.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
2. Fournir une vidéo MP4 déjà générée avec --config.input-video, ou un dossier de images avec --config.frames-dir ; run_reconstruction.py effectue le prétraitement, l'alignement, l'entraînement à la déformation inverse et l'entraînement des splats gaussiens.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
3. Utiliser le préréglage rapide par défaut pour le parcours plus court en 3DGS uniquement, ou extensive lorsque le parcours complet d'optimisation globale, 2DGS et 3DGS est nécessaire ; le choix du moteur de rendu peut être forcé explicitement.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
4. Utiliser eval_gs pour rendre de nouvelles vues à partir du point de contrôle entraîné ; exporter un point de contrôle 3DGS au format PLY ou ouvrir la visionneuse interactive locale une fois la scène prête.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
5. Vérifier le modèle de prétraitement avant une exécution : la valeur par défaut actuelle est depth-anything/DA3NESTED-GIANT-LARGE, et non un modèle fourni par video_to_world lui-même.
  — <https://github.com/lukasHoel/video_to_world/blob/main/run_reconstruction.py>

## Bonnes pratiques {#best-practices}

- Épingler la révision source documentée de Depth Anything 3 et appliquer le patch du dépôt ; le pipeline dépend de son export de trajectoire, donc remplacer par un checkout arbitraire de DA3 n'est pas équivalent.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
- Considérer le nombre de frames et le stride de l'étape 0 comme un budget de mémoire GPU : les valeurs par défaut sont 100 frames et un stride de 8, et les auteurs recommandent explicitement moins de frames sur les GPU plus petits. L'étape 1 a une valeur par défaut distincte de 50 frames pour l'alignement.
  — <https://github.com/lukasHoel/video_to_world/blob/main/README.md>
- Enregistrer le commit exact de main et l'environnement résolu pour chaque exécution. Le dépôt ne dispose d'aucun artefact de release GitHub ; « main actuelle » n'est donc pas une distribution versionnée.
  — <https://github.com/lukasHoel/video_to_world/releases>
- Vérifier les séquences sources pour les zones revisitées où des objets sont ajoutés, supprimés ou modifiés : l'article indique que de telles hallucinations des modèles vidéo peuvent être consolidées dans la géométrie statique finale plutôt que corrigées par l'alignement.
  — <https://arxiv.org/html/2603.16736v2>
- Ne pas déduire une autorisation commerciale du seul dépôt : la fiche du modèle par défaut DA3NESTED-GIANT-LARGE déclare la licence CC BY-NC 4.0 et une utilisation non commerciale uniquement.
  — <https://huggingface.co/depth-anything/DA3NESTED-GIANT-LARGE>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Inconnues restantes {#still-unknown}

- Aucune source de première main n'a été trouvée avec une date de publication, de release ou de commit du 2026-03-23 ; cette date est conservée comme date de référence observée et non considérée comme un lancement en amont.
- Il n'existe ni bundle de release GitHub, ni verrou complet des dépendances, et la révision documentée du code DA3 ne fixe pas une révision immuable des poids du modèle.
- Aucune exécution GPU locale n'a été réalisée. Les temps et les besoins mémoire sur A6000 correspondent à un benchmark fixe de l'article, et non à une garantie de capacité pour un autre clip ou un autre matériel.
- Le périmètre publié concerne les séquences vidéo générées. Les performances sur des vidéos réelles, très dynamiques ou fortement incohérentes n'ont pas été établies ici.
- Les poids par défaut de DA3 sont non commerciaux ; la compatibilité d'un substitut sous licence commerciale et la préservation de la qualité ne sont pas vérifiées.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://lukashoel.github.io/video_to_world/ | World Reconstruction From Inconsistent Views — page officielle du projet | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world | lukasHoel/video_to_world — dépôt officiel | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/blob/main/README.md | README de video_to_world — installation, pipeline, préréglages et publication des données | 2026-09-05 |
| https://arxiv.org/abs/2603.16736 | World Reconstruction From Inconsistent Views — résumé arXiv et historique des versions | 2026-09-05 |
| https://arxiv.org/html/2603.16736v2 | World Reconstruction From Inconsistent Views — arXiv HTML v2 | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/commits/main/ | video_to_world — historique des commits | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/releases | video_to_world — releases GitHub | 2026-09-05 |
| https://github.com/lukasHoel/video_to_world/blob/main/run_reconstruction.py | video_to_world run_reconstruction.py — valeurs par défaut actuelles du pipeline | 2026-09-05 |
| https://huggingface.co/depth-anything/DA3NESTED-GIANT-LARGE | Depth Anything 3 DA3NESTED-GIANT-LARGE — fiche du modèle et licence | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:video-to-world`, fil `video-to-world`, 1 événement daté du 2026-03-23 au 2026-03-23.
- **Note pratique :** Au 2026-03-23, les praticiens peuvent utiliser la page du projet et le dépôt GitHub liés comme point de départ pour évaluer le projet Video-to-World et les ressources d'implémentation disponibles.
- **Confiance :** moyenne. Les mises à jour datées ci-dessus font foi quant à ce qui est obsolète.
