---
title: "Capybara"
category: projects
date: 2026-02-24
tags: [capybara, capybara-development, project]
aliases: ["CAPYBARA", "Capybara"]
level: 4
source_sha256: 9f63befab217238f6ea0b0323ec6fd4b508c2223b5ec34121c22c9f37b67fd05
translation: machine
translated_at: '2026-10-24'
---
# Capybara {#capybara}

**Ligne de développement :** `project:capybara` · fil `capybara-development`  
**Dernier événement :** 2026-02-24 · 2 événements datés depuis 2026-02-17 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Qu'est-ce que c'est {#what-it-is}

Capybara est un pipeline d'inférence open source destiné aux utilisateurs qui ont besoin de génération et d'édition pilotée par instructions dans une seule interface.

- Génération texte-vers-image (T2I) et texte-vers-vidéo (T2V).
- Édition image-vers-image (TI2I) et vidéo-vers-vidéo (TV2V) pilotée par instructions.
- Exécutions unitaires, traitements par lots à partir de fichiers CSV, inférence distribuée via Accelerate, et nœuds ComfyUI.

La documentation recommande Python 3.11 et CUDA 12.6. Le format FP8 nécessite des GPU NVIDIA Ada/Hopper avec une capacité de calcul d'au moins 8.9 ainsi que torchao. C'est une intégration exploitable pour l'inférence en local, mais ce n'est pas une plateforme de production ou d'entraînement documentée.

## Ligne de développement {#development-line}

- **2026-02-17 — Les ressources source, modèle et démo de Capybara ont été reliées.** Le 2026-02-17, l'ensemble de ressources datées reliait le dépôt source de Capybara et la page du modèle à un modèle Qwen3-VL ainsi qu'à un point d'accès hébergé. Cela marque une première étape de développement publique pour Capybara, bien que les liens seuls n'établissent pas les capacités exactes, le statut de publication ni leur relation.
- **2026-02-24 — La documentation de Capybara a fait apparaître les workflows ComfyUI et FP8.** La documentation décrivait des nœuds personnalisés ComfyUI, le FP8 et un workflow d'exemple. Le README officiel date ces ajouts au 2026-02-20 pour les modifications de code, tandis que le 2026-02-24 est la date d'événement enregistrée.

## Ce qui a changé {#what-changed}

Capybara — le 2026-02-17, le framework d'inférence v0.1 a été publié avec T2I, T2V, TI2I et TV2V. Le 2026-02-24, la documentation a enregistré les nœuds personnalisés ComfyUI, le FP8 et un workflow d'exemple. Le README officiel date ces fonctionnalités au 2026-02-20 pour les modifications de code, ce qui fait du 2026-02-24 la date d'événement enregistrée. Au 2026-09-04, le README officiel actuel ne contient toujours que ces deux lignes datées, marque ComfyUI comme terminé, et laisse en TODO la publication du modèle de création unifié et du code d'entraînement.

## Comment l'utiliser {#how-to-use-this}

Après le 2026-02-24, évaluez Capybara à partir de sa documentation ComfyUI, de son workflow d'exemple et des recommandations FP8, plutôt que du seul dépôt de base ou de la seule page du modèle.

1. Créez un environnement Python 3.11 isolé, installez PyTorch pour CUDA 12.6 et installez les dépendances du projet.
  — <https://github.com/xgen-universe/Capybara>
2. Téléchargez tous les composants de points de contrôle requis dans `ckpts/`. Qwen3-VL-8B-Instruct n'est nécessaire que si la réécriture par instructions est activée.
  — <https://github.com/xgen-universe/Capybara>
3. Pour un premier essai, appelez `inference.py` avec `task_type` égal à `t2i` ou `t2v`. Pour `ti2i` et `tv2v`, passez `media_path` ainsi qu'une instruction textuelle.
  — <https://github.com/xgen-universe/Capybara>
4. Pour les traitements par lots, préparez un CSV avec `img_path` ou `video_path` et `instruction`, puis passez `csv_path` et `data_root_path`.
  — <https://github.com/xgen-universe/Capybara>
5. Pour ComfyUI, créez un lien symbolique de la racine de Capybara vers `custom_nodes` et lancez ComfyUI dans le même environnement `capybara`.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
6. Chargez `sample_workflow.json` dans le canevas ComfyUI, puis ajustez `task_type` et l'entrée `reference` pour T2I, T2V, TI2I ou TV2V.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/examples/sample_workflow.json>

## Bonnes pratiques {#best-practices}

- Commencez par le mode de référence officiel : 480p et 50 étapes pour la vidéo, 720p et 50 étapes pour les images. N'augmentez la résolution qu'après avoir établi une référence fonctionnelle.
  — <https://github.com/xgen-universe/Capybara>
- Dans ComfyUI pour TI2I et TV2V, fournissez l'image ou la vidéo via `reference`. Le nœud déduit le rapport d'aspect de `reference` et fixe `guidance_scale` à 1.0.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Activez FP8 uniquement sur Ada/Hopper avec `torchao`. Cela réduit d'environ moitié la mémoire des poids du transformeur, mais ne promet aucun gain de vitesse et maintient le transformeur épinglé en mémoire GPU.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Ne mélangez pas les environnements Python entre Capybara et ComfyUI. La documentation exige d'exécuter ComfyUI depuis le même environnement afin que les nœuds personnalisés trouvent leurs dépendances.
  — <https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md>
- Épinglez le dépôt de modèle résolu et la révision avant le téléchargement. Le lien officiel `xgen-universe` redirige actuellement vers `Glanty/Capybara`.
  — <https://huggingface.co/xgen-universe/Capybara>

## Remplacé par ceci {#superseded-by-this}

- 2026-02-20 : le TODO précédent « Add support for ComfyUI » est obsolète, car Capybara fournit des nœuds personnalisés et un workflow d'exemple. L'interface en ligne de commande native reste prise en charge et n'est pas remplacée.

## Points encore inconnus {#still-unknown}

- Les sources officielles n'expliquent pas si la redirection Hugging Face de `xgen-universe/Capybara` vers `Glanty/Capybara` correspond à un transfert de propriété, à un miroir ou à une erreur. Vérifiez les fichiers spécifiques et la révision avant utilisation.
- La documentation officielle ne fournit ni tableaux de consommation de VRAM, ni benchmarks indépendants, ni preuve de maturité pour la production. Le code d'entraînement reste également non publié.
- L'URL de démo ngrok temporaire de l'événement du 2026-02-17 n'a pas pu être ouverte en toute sécurité ; sa disponibilité actuelle n'est donc pas confirmée.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/xgen-universe/Capybara | xgen-universe/Capybara — README du dépôt | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/README.md | Capybara — README principal, source brute | 2026-09-04 |
| https://huggingface.co/xgen-universe/Capybara | xgen-universe/Capybara — page du modèle Hugging Face, redirigée vers Glanty/Capybara | 2026-09-04 |
| https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct | Qwen3-VL-8B-Instruct — fiche du modèle Hugging Face | 2026-09-04 |
| https://github.com/xgen-universe/Capybara/blob/main/comfyui/README.md | Capybara ComfyUI Custom Nodes | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/comfyui/README.md | Capybara ComfyUI Custom Nodes — source brute | 2026-09-04 |
| https://github.com/xgen-universe/Capybara/blob/main/comfyui/examples/sample_workflow.json | Workflow d'exemple ComfyUI de Capybara | 2026-09-04 |
| https://raw.githubusercontent.com/xgen-universe/Capybara/main/comfyui/examples/sample_workflow.json | Workflow d'exemple ComfyUI de Capybara — source brute | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:capybara`, fil `capybara-development`, 2 événements datés du 2026-02-17 au 2026-02-24.
- **Note pratique :** Après le 2026-02-24, les praticiens qui évaluent Capybara doivent consulter sa documentation ComfyUI, son workflow d'exemple et ses recommandations FP8, plutôt que de se fier uniquement au dépôt de base ou à la page du modèle.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
