---
title: "TimeLens2"
category: projects
date: 2026-07-22
tags: [project, timelens2, timelens2-development]
aliases: ["TimeLens2"]
level: 2
source_sha256: be9c7a1c507f56317676f2bc3862f3b1efcc8c19f2d3915c4924a5ec16d8ddb2
translation: machine
translated_at: '2026-10-24'
---
# TimeLens2 {#timelens2}

**Ligne de développement :** `project:timelens2` · fil `timelens2-development`  
**Dernier événement :** 2026-07-22 · 1 événement daté depuis le 2026-07-22 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

TimeLens2 est une famille de modèles ouverts basée sur Qwen3-VL, destinée aux chercheurs et aux développeurs de moteurs de recherche vidéo, qui convertit une vidéo et une requête textuelle en un ou plusieurs intervalles de preuve. Elle prend en charge l'ancrage temporel de séquences courtes et longues, d'événements répétés, de requêtes formulées sous forme de questions, ainsi que de vidéos en vue subjective (egocentric). Les tailles publiées sont 2B, 4B et 8B. Le modèle 8B affiche un mIoU moyen de 48,0 sur sept benchmarks. L'inférence locale nécessite une pile Transformers et vidéo compatible ; aucun fournisseur d'inférence hébergée n'existe.

## Ligne de développement {#development-line}

- **2026-07-22 — Les ressources publiques du projet TimeLens2 ont été publiées.** Le 2026-07-22, un message de la ligne de développement de TimeLens2 a donné accès à la page publique du projet, au dépôt source GitHub, à la collection Hugging Face et à un Space dédié à l'ancrage temporel. Cette publication donne un accès concret au projet, mais ne précise aucune version, aucune configuration de modèle ni aucune fonctionnalité.

## Changements {#what-changed}

2026-07-22 — TimeLens2 est sorti comme version généraliste d'ancrage temporel, avec une page de projet, du code sous licence Apache-2.0, les données TimeLens2-93K, les points de contrôle 2B/4B/8B et une démonstration 8B. L'article associé, soumis le 2026-07-19, présente la tâche comme une prédiction d'intervalles à valeurs multiples. Sur le backbone Qwen3-VL, il rapporte des gains de 14,2 mIoU pour le 2B, 13,0 pour le 4B et 18,1 pour le 8B. Le 2026-07-27, des points de contrôle SFT 2B/4B/8B correspondants ont été ajoutés pour la génération de rollouts et la reproduction de GRPO.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-07-22, commencez par la page de projet et le dépôt de TimeLens2, puis utilisez la collection Hugging Face et le Space pour les ressources et les démonstrations.

1. Installez les dépendances d'inférence, chargez `MCG-NJU/TimeLens2-8B` avec Transformers et fournissez un URI vidéo local.
  — <https://huggingface.co/MCG-NJU/TimeLens2-8B>
2. Demandez tous les segments pertinents en secondes et exigez un tableau JSON de paires `[start, end]` ; décodez la réponse générée comme l'ensemble des preuves.
  — <https://huggingface.co/MCG-NJU/TimeLens2-8B>
3. Pour la reproduction, téléchargez les vidéos requises, lancez le SFT, régénérez éventuellement les rollouts à partir du point de contrôle `-SFT` correspondant, puis lancez GRPO et l'évaluation.
  — <https://github.com/MCG-NJU/TimeLens2>

## Bonnes pratiques {#best-practices}

- Demandez tous les segments correspondants plutôt qu'un seul moment deviné, et contraignez le format de réponse à des paires d'horodatages.
  — <https://huggingface.co/MCG-NJU/TimeLens2-8B>
- Utilisez une racine de sortie distincte pour chaque combinaison modèle, données et graine afin que les tâches de shards concurrentes n'écrasent pas les sorties.
  — <https://github.com/MCG-NJU/TimeLens2/blob/main/grpo/README.md>
- Ne lancez pas GRPO tant que la fusion des rollouts n'a pas réussi et que chaque ligne d'entraînement ne comporte pas les huit réponses attendues.
  — <https://github.com/MCG-NJU/TimeLens2/blob/main/grpo/README.md>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points non élucidés {#still-unknown}

- L'événement du 2026-07-22 renvoie vers un Space 8B, mais la page consultée n'expose ni limites opérationnelles ni configuration de déploiement. La fiche officielle du modèle 8B indique qu'il n'est déployé par aucun fournisseur d'inférence ; la disponibilité de cette démonstration ne constitue donc pas une preuve d'une API hébergée prise en charge.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://mcg-nju.github.io/TimeLens2/ | TimeLens2 — Generalist Video Temporal Grounding with Multimodal LLMs | 2026-09-05 |
| https://github.com/MCG-NJU/TimeLens2 | Dépôt MCG-NJU/TimeLens2 | 2026-09-05 |
| https://huggingface.co/collections/MCG-NJU/timelens2 | Collection TimeLens2 | 2026-09-05 |
| https://huggingface.co/spaces/hugging-apps/timelens2-8b-temporal-grounding | Space d'ancrage temporel TimeLens2-8B | 2026-09-05 |
| https://arxiv.org/abs/2607.17423 | TimeLens2: Generalist Video Temporal Grounding with Multimodal LLMs | 2026-09-05 |
| https://huggingface.co/MCG-NJU/TimeLens2-8B | Fiche du modèle MCG-NJU/TimeLens2-8B | 2026-09-05 |
| https://github.com/MCG-NJU/TimeLens2/blob/main/grpo/README.md | Guide TimeLens2 sur les rollouts et GRPO | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:timelens2`, fil `timelens2-development`, 1 événement daté du 2026-07-22 au 2026-07-22.
- **Note pratique :** À partir du 2026-07-22, les praticiens doivent utiliser la page de projet et le dépôt comme point de départ pour TimeLens2, la collection Hugging Face liée et le Space servant de points d'entrée publics pour les ressources et les démonstrations ; les capacités exactes restent non vérifiées.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
