---
title: "SketchVideo"
category: projects
date: 2025-04-07
tags: [project, sketchvideo, sketchvideo-development]
aliases: ["SketchVideo"]
level: 2
source_sha256: 749af09511f387c43fac44e37f26d65b42b9378a852adda5330e333e11f171b3
translation: machine
translated_at: '2026-10-24'
---
# SketchVideo {#sketchvideo}

**Ligne de développement :** `project:sketchvideo` · fil `sketchvideo-development`  
**Dernier événement :** 2025-04-07 · 2 entrées datées depuis le 2023-11-28 · **Recherche effectuée :** 2026-09-04 · confiance : élevée

## Ce que c'est {#what-it-is}

SketchVideo ne désigne pas un outil unique aujourd'hui, mais une collision de noms. — Sketch Video Synthesis (2023) : optimise des courbes de Bézier par-dessus une vidéo d'entrée et exporte des SVG vectoriels pour la stylisation, le redessin et le compositing. — Sketch-based Video Generation and Editing (2025) : génère ou modifie une vidéo à partir d'un texte et d'une ou deux esquisses d'images clés. Limite du code 2025 actuel : jusqu'à 49 images en 720×480 ; pour A100, les auteurs indiquent environ 21 GB/95 s pour SketchGen et 23 GB/230 s pour SketchEdit. Conclusion : il faut choisir selon le dépôt officiel des auteurs, et non selon le nom.

## Ligne de développement {#development-line}

- **2023-11-28 — Les ressources du projet SketchVideo ont été rendues disponibles.** Le code publié optimise des courbes de Bézier image par image avec une sémantique CLIP et une cohérence inter-images, en transformant la vidéo source en esquisse SVG.
- **2025-04-07 — Un ensemble de ressources SketchVideo ultérieur a été référencé.** Un autre projet a fourni le code et les poids pour la génération et l'édition locale de vidéos à partir d'une ou deux esquisses d'images clés, sur la base de CogVideo-2b.

## Ce qui a changé {#what-changed}

2023-11-28 — Sketch Video Synthesis : le code publié optimise des courbes de Bézier image par image avec une sémantique CLIP et une cohérence inter-images, en transformant la vidéo source en esquisse SVG. 2025-04-07 — SketchVideo : un autre projet a fourni le code et les poids pour la génération et l'édition locale de vidéos à partir d'une ou deux esquisses d'images clés, sur la base de CogVideo-2b.

Aucune de ces étapes n'est une mise à jour de l'autre : ce sont deux projets distincts portant le même nom.

## Comment l'utiliser {#how-to-use-this}

Au 2025-04-07, les praticiens doivent comparer les ressources ultérieures liées à geometrylearning.com et IGLICT avec les ressources du projet de 2023 avant de choisir une implémentation de SketchVideo.

1. Pour le projet génératif, créez un environnement Python 3.10 et installez les dépendances ; le dépôt requiert diffusers==0.30.1.
  — <https://github.com/IGLICT/SketchVideo>
2. Téléchargez les poids de SketchGen ou SketchEdit ainsi que le modèle de base CogVideo-2b, puis renseignez leurs chemins dans les scripts ou dans config.py.
  — <https://github.com/IGLICT/SketchVideo>
3. Pour la génération, préparez une esquisse en 720×480 sur une ou deux images et lancez test_sketch_gen_single.sh ou test_sketch_gen_two.sh.
  — <https://github.com/IGLICT/SketchVideo>
4. Pour l'édition, préparez une vidéo de 49 images en 720×480, une esquisse d'image clé et des masques des zones à modifier, puis lancez test_sketch_edit.sh.
  — <https://github.com/IGLICT/SketchVideo>
5. Pour la vectorisation d'une vidéo, utilisez le dépôt distinct de 2023 : installez les dépendances, préparez un clip de moins de 70 images avec des masques, construisez l'atlas et exécutez operate_clipavideo.sh.
  — <https://github.com/yudianzheng/SketchVideo>

## Bonnes pratiques {#best-practices}

- Ne mélangez pas les poids, les instructions et les résultats des deux dépôts : leurs auteurs, leurs tâches et leurs pipelines sont différents.
  — <https://github.com/yudianzheng/SketchVideo>
- Pour SketchVideo 2025, commencez avec une ou deux esquisses de clés strictement en 720×480 ; pour l'édition, le clip d'entrée doit contenir 49 images.
  — <https://github.com/IGLICT/SketchVideo>
- Si le résultat du projet génératif est instable, essayez d'autres seeds ; les auteurs ne garantissent pas explicitement le succès à chaque exécution. Réduire le nombre d'étapes DDIM raccourcit le temps d'inférence.
  — <https://github.com/IGLICT/SketchVideo>
- Pour le projet de 2023, limitez le clip d'entrée à moins de 70 images et préparez les masques de l'objet au premier plan avant de construire l'atlas.
  — <https://github.com/yudianzheng/SketchVideo>

## Remplacé par ceci {#superseded-by-this}

- 2025-04-07 : l'hypothèse selon laquelle IGLICT/SketchVideo serait une nouvelle version de yudianzheng/SketchVideo est fausse ; il s'agit d'un projet indépendant, publié à CVPR 2025.
- 2025-04-01 : pour une tâche de génération ou d'édition à partir d'esquisses, IGLICT/SketchVideo avec ses poids s'applique ; il ne remplace pas la vectorisation SVG du projet de 2023.

## Points encore inconnus {#still-unknown}

- La page http://geometrylearning.com/SketchVideo/ était inaccessible lors de la vérification ; son contenu n'a donc pas été utilisé.
- Aucune preuve n'a été trouvée d'une base de code commune, d'une équipe commune ou d'une filiation entre les dépôts de 2023 et de 2025 ; il convient de les suivre comme deux subject_key distincts.
- event_findings : 2023-11-28 — le préprint arXiv du 2023-11-26 précise les auteurs (Yudian Zheng, Xiaodong Cun, Menghan Xia, Chi-Man Pun) et le fait que la méthode optimise des courbes de Bézier avec une perte sémantique CLIP et une perte de cohérence basée sur l'atlas ; source https://arxiv.org/abs/2311.15306.
- event_findings : 2025-04-07 — le dépôt précise les noms des poids SketchGen et SketchEdit, la base CogVideo-2b et la limite de 49 images en 720×480 ; le README date la publication du code et des poids au 2025-04-01 ; source https://github.com/IGLICT/SketchVideo.
- new_events : 2023-11-26 — publication du préprint arXiv Sketch Video Synthesis ; source https://arxiv.org/abs/2311.15306.
- new_events : 2025-03-30 — pour le SketchVideo indépendant, mise en ligne de la page du projet et mise à jour du préprint arXiv ; source https://github.com/IGLICT/SketchVideo.
- new_events : 2025-04-01 — pour le SketchVideo indépendant, publication du code et des poids ; source https://github.com/IGLICT/SketchVideo.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/yudianzheng/SketchVideo | yudianzheng/SketchVideo — Sketch Video Synthesis | 2026-09-05 |
| https://sketchvideo.github.io/ | Sketch Video Synthesis project page | 2026-09-05 |
| https://arxiv.org/abs/2311.15306 | Sketch Video Synthesis | 2026-09-05 |
| https://github.com/IGLICT/SketchVideo | IGLICT/SketchVideo — Sketch-based Video Generation and Editing | 2026-09-05 |
| https://arxiv.org/abs/2503.23284 | SketchVideo: Sketch-based Video Generation and Editing | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:sketchvideo`, fil `sketchvideo-development`, 2 événements datés du 2023-11-28 au 2025-04-07.
- **Note pratique :** Au 2025-04-07, les praticiens doivent comparer les ressources ultérieures liées à geometrylearning.com et IGLICT avec les ressources du projet de 2023 avant de choisir une implémentation de SketchVideo.
- **Confiance :** élevée. Les mentions « remplacé » datées ci-dessus font foi pour ce qui est obsolète.
