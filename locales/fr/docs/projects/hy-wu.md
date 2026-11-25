---
title: "HY-WU — Tencent Hunyuan"
category: projects
date: 2026-03-06
tags: [hy-wu, project, tencent-hunyuan]
aliases: ["HY-WU"]
level: 3
source_sha256: 53799f20cc1190f7fefc0711385bd252aaeb9f82f07c5d4510155e9cf183d021
translation: machine
translated_at: '2026-10-24'
---
# HY-WU — Tencent Hunyuan {#hy-wu-tencent-hunyuan}

**Ligne de développement :** `project:hy-wu` · fil `tencent-hunyuan`  
**Dernier événement :** 2026-03-06 · 1 événement daté depuis le 2026-03-06 · **Recherche effectuée le :** 2026-09-06 · confiance : élevée

## Ce que c'est {#what-it-is}

HY-WU est une pile de recherche locale destinée aux équipes disposant de matériel multi-GPU et qui ont besoin de modifications image-à-image sans entraîner de LoRA spécifique à l'édition.

- Générateur de LoRA : crée des mises à jour LoRA conditionnées par l'instance et les injecte dans un backbone gelé.
- Modèle associé : fonctionne avec `tencent/HY-WU` aux côtés de `tencent/HunyuanImage-3.0-Instruct`.
- Tâches d'édition : démontre la fusion de vêtements, le transfert de tenue, le transfert d'identité faciale, l'essayage virtuel et la synthèse de textures.

## Ligne de développement {#development-line}

- **2026-03-06 — Les ressources officielles du projet HY-WU sont devenues disponibles.** Le 2026-03-06, les ressources officielles de HY-WU ont été mises en ligne via un site de projet, un dépôt GitHub et une page Hugging Face. Nous ne disposons d'aucun détail confirmé sur la version publiée, l'annonce ou les capacités complètes.

## Ce qui a changé {#what-changed}

2026-03-06 — HY-WU a publié le code d'inférence et les poids du modèle pour l'inférence avec HunyuanImage-3.0-Instruct. 2026-03-07 — le rapport technique de HY-WU est paru sur arXiv en version v1, sous forme d'article de recherche et non de point de contrôle distinct. 2026-03-18 — l'historique GitHub enregistre le commit `a9f4206`, intitulé « add configurable image size » ; l'inférence actuelle accepte `image_size`. 2026-06-18 — arXiv v2 a révisé le rapport technique ; nous n'avons trouvé aucune publication plus récente de code ou de poids.

## Comment l'utiliser {#how-to-use-this}

Nous pouvons évaluer HY-WU à partir du 2026-03-06 en utilisant son site de projet, son dépôt source et sa page Hugging Face. Nous ne disposons pas de preuves suffisantes pour le recommander dans des tâches de production.

1. Lisez d'abord la licence communautaire et vérifiez que le territoire visé et l'usage en aval prévu sont couverts.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/LICENSE>
2. Provisionnez, avant l'installation, la capacité multi-GPU documentée : au minimum 8×40 Go ou 4×80 Go de VRAM.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
3. Clonez `Tencent-Hunyuan/HY-WU`, placez-vous dans le répertoire et installez `requirements.txt`.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
4. Exécutez `python infer.py`, ou créez `WUPipeline` avec `tencent/HunyuanImage-3.0-Instruct` comme modèle de base et `tencent/HY-WU` comme générateur de paramètres.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py>
5. Fournissez une image de base, une ou plusieurs images de référence et une instruction qui précise à la fois le transfert souhaité et ce qui doit rester inchangé ; enregistrez l'image générée.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py>
6. Pour l'interface utilisateur locale facultative, installez Gradio et exécutez `python gradio/app.py`.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>

## Bonnes pratiques {#best-practices}

- Commencez par la paire de modèles correspondante en amont plutôt que de remplacer le backbone par un modèle non listé ; les points de contrôle distillés et ceux d'autres backbones restent non vérifiés dans le plan du projet.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
- Reproduisez la recette fournie à deux images, avec son instruction explicite de préservation, 50 étapes de diffusion et une graine fixe, avant de modifier les paramètres de génération.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py>
- Traitez la capacité GPU comme une condition préalable : la documentation en amont exige explicitement une inférence multi-GPU pour le modèle de base.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md>
- Ne codez pas en dur le port Gradio indiqué dans le README : l'application actuelle écoute sur le port 7860 alors que le README mentionne 7680 ; inspectez le point d'accès en cours d'exécution.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/gradio/app.py>
- N'utilisez pas les travaux ni leurs sorties pour améliorer un modèle non Hunyuan, et n'exploitez pas le modèle dans les territoires exclus par la licence.
  — <https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/LICENSE>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-03-07 — arXiv v1 a été remplacée par arXiv v2, révisée le 2026-06-18 ; cela n'établit pas la publication d'un modèle ou de poids plus récents.

## Toujours inconnu {#still-unknown}

- La fiche modèle officielle sur Hugging Face indique actuellement « March 6, 2025 », ce qui contredit la date de licence du 6 mars 2026 et l'historique du dépôt ; il semble s'agir d'une erreur de documentation plutôt que d'un lancement distinct en 2025.
- Aucune exécution locale réussie et vérifiée indépendamment, aucune mesure de débit, aucun contournement pour GPU grand public ni aucun point de contrôle distillé n'ont été trouvés.
- Aucune publication ultérieure de poids de modèle par l'éditeur n'a été établie ; arXiv v2 est une révision du rapport et ne prouve pas une mise à jour de l'implémentation.
- Aucune annonce d'entreprise datée de Tencent en chinois simplifié accessible concernant la publication du projet n'a été trouvée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://tencent-hy-wu.github.io/ | HY-WU (Partie I) : un cadre extensible de mémoire neuronale fonctionnelle et une instanciation en édition d'image guidée par texte | 2026-09-06 |
| https://github.com/Tencent-Hunyuan/HY-WU | Tencent-Hunyuan/HY-WU | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/README.md | README de HY-WU | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/LICENSE | Contrat de licence communautaire Tencent Hunyuan pour HY-WU | 2026-09-06 |
| https://huggingface.co/tencent/HY-WU | Fiche modèle tencent/HY-WU | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/infer.py | Exemple d'inférence HY-WU | 2026-09-06 |
| https://raw.githubusercontent.com/Tencent-Hunyuan/HY-WU/main/gradio/app.py | Application Gradio HY-WU | 2026-09-06 |
| https://github.com/Tencent-Hunyuan/HY-WU/commits/main | Historique des commits de HY-WU | 2026-09-06 |
| https://arxiv.org/abs/2603.07236v2 | HY-WU (Partie I), arXiv v2 | 2026-09-06 |
| https://github.com/Tencent-Hunyuan/HY-WU/releases | Versions publiées de HY-WU sur GitHub | 2026-09-06 |

## Note pour l'agent {#agent-brief}

- **Sujet :** `project:hy-wu`, fil `tencent-hunyuan`, 1 événement daté du 2026-03-06 au 2026-03-06.
- **Note pratique :** Nous pouvons évaluer HY-WU à partir du 2026-03-06 via son site de projet officiel, son dépôt source et sa page Hugging Face ; les preuves fournies ne justifient pas de recommandations d'adoption propres à une capacité donnée.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
