---
title: "Penguin-VL"
category: projects
date: 2026-03-09
tags: [penguin-vl, penguin-vl-public-release, project, tencent-ailab]
aliases: ["Penguin-VL"]
level: 2
source_sha256: 2601042161c6bf18ed0e71d3bd8c71ef9567da2b1d3dcae467f323bd3ab811c7
translation: machine
translated_at: '2026-10-24'
---
# Penguin-VL {#penguin-vl}

**Ligne de développement :** `project:penguin-vl` · fil `penguin-vl-public-release`  
**Dernier événement :** 2026-03-09 · 1 événement daté depuis le 2026-03-09 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Penguin-VL est une famille de VLM basée sur Qwen3, destinée aux praticiens qui ont besoin d'une inférence multimodale en local plutôt que d'une API de vision hébergée.

- Requêtes portant sur des images, des documents, des graphiques, plusieurs images et des vidéos
- Chemins de service Transformers, Gradio et vLLM
- Points de contrôle 2B et 8B, ainsi qu'un encodeur de vision de 0,4B

## Ligne de développement {#development-line}

- **2026-03-09 — Les ressources publiques du projet Penguin-VL ont été partagées.** Le 2026-03-09, Penguin-VL a publié les liens vers le site web du projet, le dépôt source, la collection Hugging Face et l'Space Hugging Face interactif. Cette étape publique permet d'évaluer le projet, de retrouver ses ressources publiées et de tester sa démo. Les seuls liens datés n'établissent pas la version exacte du modèle, les affirmations techniques, la licence ni le périmètre de la publication.

## Évolutions {#what-changed}

2026-03-09 — Tencent a publié Penguin-VL-2B, Penguin-VL-8B, Penguin-Encoder, le code d'inférence, un plugin vLLM et une démo Gradio. 2026-03-17 — le code d'entraînement a été publié. 2026-03-20 — Penguin-Recap-I, les données d'entraînement d'images reconstruites qui l'accompagnent, a été publié. 2026-03-26 — lmms-eval a ajouté la prise en charge des benchmarks Penguin-VL. 2026-03-30 — Penguin-Recap-V, des données vidéo avec des annotations denses au niveau temporel, des paragraphes et de la vidéo entière, a été publié.

## Mode d'emploi {#how-to-use-this}

Au 2026-03-09, évaluez Penguin-VL via son site web, son dépôt source, sa collection Hugging Face et sa démo. Vérifiez les capacités, les versions, les licences et les exigences de déploiement dans ces ressources primaires avant de vous y fier.

1. Créez un environnement propre avec Python 3.11.13, PyTorch 2.5 ou ultérieur, et CUDA 11.8 ou ultérieur. Installez les dépendances du dépôt, puis exécutez l'exemple Transformers fourni avec `tencent/Penguin-VL-2B` ou `tencent/Penguin-VL-8B`.
  — <https://github.com/tencent-ailab/Penguin-VL>
2. Pour une intégration Python directe, chargez `tencent/Penguin-VL-8B` via `AutoModelForCausalLM` et `AutoProcessor` avec `trust_remote_code=True`. Transmettez les entrées image, vidéo ou texte au processeur.
  — <https://huggingface.co/tencent/Penguin-VL-8B>
3. Pour une interface de test visuel interne, lancez `inference/launch_gradio_demo.py --model-path tencent/Penguin-VL-2B` ou le point de contrôle 8B, puis utilisez l'interface locale.
  — <https://github.com/tencent-ailab/Penguin-VL>
4. Pour un point de terminaison de service compatible OpenAI, installez la pile vLLM dont la version est gérée séparément. Démarrez le plugin du projet avec `python -m penguinvl.plugin.vllm serve tencent/Penguin-VL-8B`.
  — <https://github.com/tencent-ailab/Penguin-VL>

## Bonnes pratiques {#best-practices}

- Séparez l'inférence Transformers et l'inférence vLLM dans des environnements distincts : le chemin vLLM 0.11.0 documenté exige PyTorch 2.8, tandis que le chemin standard recommande PyTorch 2.5 ou ultérieur.
  — <https://github.com/tencent-ailab/Penguin-VL>
- Installez vLLM avant Flash Attention lorsque vous utilisez le chemin vLLM, afin d'éviter les conflits de dépendances. C'est l'ordre documenté par le projet.
  — <https://github.com/tencent-ailab/Penguin-VL>
- Utilisez le notebook d'inférence fourni et testez des entrées représentatives d'OCR, de documents, de graphiques et de vidéos avant d'adopter les affirmations de benchmark pour un routage en production.
  — <https://github.com/tencent-ailab/Penguin-VL>

## Remplacé par {#superseded-by-this}

- 2026-03-17 — la version d'inférence seule du 2026-03-09 constitue un guide incomplet pour les praticiens qui doivent reproduire ou adapter l'entraînement ; le code d'entraînement est désormais disponible.
- 2026-03-20 — le guide selon lequel les données d'entraînement de Penguin-VL étaient indisponibles est obsolète pour le volet image ; Penguin-Recap-I est disponible.
- 2026-03-30 — le guide sur les données d'entraînement limitées aux images est incomplet pour les travaux sur la vidéo ; Penguin-Recap-V ajoute des annotations vidéo à plusieurs granularités.

## Points encore inconnus {#still-unknown}

- L'Space Hugging Face hébergé affichait une erreur de configuration à la consultation du 2026-09-05 ; l'instance Gradio locale reste la voie de démo documentée.
- Nous n'avons trouvé aucune mesure indépendante de déploiement ou de coût dans les sources primaires consultées.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/tencent-ailab/Penguin-VL | Dépôt Tencent AI Lab Penguin-VL et historique des publications | 2026-09-05 |
| https://huggingface.co/tencent/Penguin-VL-8B | Fiche modèle tencent/Penguin-VL-8B | 2026-09-05 |
| https://huggingface.co/collections/tencent/penguin-vl | Collection Tencent Penguin-VL | 2026-09-05 |
| https://huggingface.co/spaces/tencent/Penguin-VL | Space Tencent Penguin-VL | 2026-09-05 |
| https://arxiv.org/abs/2603.06569 | Penguin-VL: Exploring the Efficiency Limits of VLM with LLM-based Vision Encoders | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:penguin-vl`, fil `penguin-vl-public-release`, 1 événement daté du 2026-03-09 au 2026-03-09.
- **Note pratique :** Au 2026-03-09, les praticiens peuvent commencer à évaluer Penguin-VL via le site web, le dépôt source, la collection Hugging Face et la démo liés ; vérifiez les capacités, les versions, les licences et les exigences de déploiement dans ces ressources primaires avant de vous y fier.
- **Confiance :** élevée. Les mentions datées de remplacement ci-dessus font foi quant à ce qui est obsolète.
