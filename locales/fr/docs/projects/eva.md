---
title: "EVA"
category: projects
date: 2026-03-26
tags: [eva, eva-public-resources, project]
aliases: ["EVA"]
level: 2
source_sha256: 4147ba2ea46c52ef80d86b8bad838b772f7c7c701d76bf4c7ea04f7c2a53563e
translation: machine
translated_at: '2026-10-24'
---
# EVA {#eva}

**Ligne de développement :** `project:eva` · fil `eva-public-resources`  
**Dernier événement :** 2026-03-26 · 1 événement daté depuis le 2026-03-26 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

EVA (Efficient Video Agent) est un agent vidéo construit sur Qwen2.5-VL, destiné aux chercheurs et aux ingénieurs.

- Cycle de l'agent : exécute une boucle résumé → planification → action → réflexion.
- Sélection de trames : choisit et extrait des images de la vidéo, puis met à jour l'étape suivante en fonction du résultat.
- Poids du modèle : hébergés sous `WRHC/EfficientVideoAgent` pour l'évaluation sur six jeux de données vidéo.

Le dépôt publié couvre l'évaluation multi-GPU via vLLM plutôt qu'une interface interactive. La configuration convient à une évaluation vidéo reproductible pilotée par requêtes, mais un service en production nécessite un pipeline d'inférence distinct.

## Ligne de développement {#development-line}

- **2026-03-26 — Les ressources source et modèle de EVA ont été enregistrées.** Le 2026-03-26, EVA est apparu avec un dépôt source sur GitHub et une page de modèle sur Hugging Face. Ces deux liens indiquent un accès public au projet. Les seules dates des liens ne permettent pas de confirmer une version, des capacités, des résultats d'évaluation, ni que l'une de ces ressources ait été publiée pour la première fois ce jour-là.

## Changements {#what-changed}

2026-03-26 — Le code d'évaluation officiel et les poids de EVA sont publics. Le modèle remplace l'échantillonnage uniforme et passif des trames par une boucle d'agent qui choisit quoi inspecter et quand.

## Mode d'emploi {#how-to-use-this}

Au 2026-03-26, les praticiens devraient considérer que EVA dispose à la fois d'une référence de code source et d'une référence d'hébergement de modèle, puis vérifier directement dans ces ressources la configuration et les détails du modèle avant toute utilisation.

1. Téléchargez les poids de `WRHC/EfficientVideoAgent` et installez les dépendances du dépôt avec FFmpeg.
  — <https://github.com/wangruohui/EfficientVideoAgent>
2. Préparez l'un des six jeux de données vidéo pris en charge pour l'évaluation, puis définissez le `video_root` local dans `DATASET_CONFIG`.
  — <https://github.com/wangruohui/EfficientVideoAgent>
3. Servez les poids avec un point de terminaison compatible OpenAI de vLLM, puis renseignez son URL, le chemin du tokenizer et les chemins de médias autorisés dans `eval-eva.py`.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
4. Lancez le jeu de données choisi avec `eval-eva.py`. Relancez la même commande pour reprendre une exécution interrompue à partir du fichier de cache.
  — <https://github.com/wangruohui/EfficientVideoAgent>

## Bonnes pratiques {#best-practices}

- Gardez `ffprobe` dans `PATH` et les bibliothèques FFmpeg dans `LD_LIBRARY_PATH`, car l'extraction des trames a lieu pendant l'évaluation.
  — <https://github.com/wangruohui/EfficientVideoAgent>
- Donnez à vLLM l'accès aux fichiers vidéo locaux avec `--allowed-local-media-path`, afin que l'agent puisse transmettre les trames extraites au modèle.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
- Fixez `--max-visual-tokens` d'une exécution à l'autre, car dépasser le budget de tokens réduit la résolution et supprime des trames.
  — <https://huggingface.co/WRHC/EfficientVideoAgent>
- Ne considérez pas une exécution unique comme une reproduction exacte, car la précision varie de quelques fractions de pour cent même avec `temperature=0`.
  — <https://github.com/wangruohui/EfficientVideoAgent>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points inconnus {#still-unknown}

- Il n'existe aucun journal des modifications daté, publié par les auteurs, après la version initiale. Nous ne pouvons pas confirmer si des commits ou des mises à jour du modèle ultérieurs ont modifié les capacités de EVA.
- La documentation publique ne couvre que le flux d'évaluation par benchmark. Nous ne trouvons aucune configuration d'inférence en production confirmée, ni d'API autonome, ni d'interface utilisateur.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/wangruohui/EfficientVideoAgent | EVA: Efficient Reinforcement Learning for End-to-End Video Agent — code d'évaluation officiel | 2026-09-05 |
| https://huggingface.co/WRHC/EfficientVideoAgent | WRHC/EfficientVideoAgent — fiche du modèle et poids | 2026-09-05 |
| https://arxiv.org/abs/2603.22918 | EVA: Efficient Reinforcement Learning for End-to-End Video Agent | 2026-09-05 |
| https://huggingface.co/papers/2603.22918 | Page de l'article — EVA: Efficient Reinforcement Learning for End-to-End Video Agent | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:eva`, fil `eva-public-resources`, 1 événement daté du 2026-03-26 au 2026-03-26.
- **Note pratique :** Au 2026-03-26, les praticiens devraient considérer que EVA dispose à la fois d'une référence de code source et d'une référence d'hébergement de modèle, puis vérifier directement dans ces ressources la configuration et les détails du modèle avant toute utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
