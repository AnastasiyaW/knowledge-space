---
title: "GLM-5.2-NVFP4"
category: projects
date: 2026-06-26
tags: [glm-5-2-nvfp4, project]
aliases: ["GLM-5.2-NVFP4"]
level: 3
source_sha256: 05ff2666d99ea4e4c023a0f6612605a9776405713ac9538780ac18aa3ea3c9ed
translation: machine
translated_at: '2026-10-24'
---
# GLM-5.2-NVFP4 {#glm-52-nvfp4}

**Ligne de développement :** `project:glm-5-2-nvfp4` · fil `glm-5-2-nvfp4`  
**Dernier événement :** 2026-06-26 · 1 événement daté depuis le 2026-06-26 · **Recherche effectuée le :** 2026-09-06 · confiance : élevée

## Présentation {#what-it-is}

GLM-5.2-NVFP4 est le point de contrôle (checkpoint) NVFP4 de NVIDIA Model Optimizer pour GLM-5.2 de Z.AI, destiné à l'auto-hébergement d'agents, de chatbots, de RAG, de génération de code et de raisonnement.

- Génération de texte et raisonnement avec architecture Sparse-MoE.
- Requêtes de code et à long contexte.
- Appel d'outils via les paramètres de parseur SGLang et vLLM fournis.

753 Md de paramètres au total, 40 Md actifs, et jusqu'à 1M de contexte sur Blackwell et Linux.
Déployez-le sur Blackwell après validation de la charge de travail ; ces éléments ne permettent pas d'établir une voie générale en local, hors NVIDIA, ou via inférence managée.

## Ligne de développement {#development-line}

- **2026-06-26 — GLM-5.2-NVFP4 relié à la page de modèle Hugging Face de NVIDIA.** Le 2026-06-26, la ligne de développement de GLM-5.2-NVFP4 a été reliée à une page de modèle Hugging Face sous le compte NVIDIA. Il s'agit d'un point de repère important pour la piste de distribution publique du projet, bien que ce lien daté n'établisse à lui seul ni une date de publication, ni une révision du modèle, ni des spécifications techniques.

## Évolutions {#what-changed}

- 2026-06-26 — GLM-5.2-NVFP4 a été documenté comme point de contrôle NVFP4 1.0 Model Optimizer de GLM-5.2 de Z.AI ; la fiche liée est datée du 2026-06-25.
- 2026-07-09 — NVIDIA NGC a ajouté `nim-aec724e-nvfp4`, un artefact de préparation NIM de 432,95 Go ; sa description FP8 crée une réserve sur l'identité du paquet.
- 2026-07-20 — NVIDIA Dynamo a enregistré un runtime SGLang de développement pour GLM-5.2, comportant des correctifs de stabilité, d'analyse de configuration et de prise en charge du modèle non remontés en amont.
- 2026-08-14 — NVIDIA Dynamo v1.4.0 a ajouté des recettes SGLang GLM-5.2 agrégées et désagrégées pour les déploiements B200 NVFP4 et H200 FP8.

## Mode d'emploi {#how-to-use-this}

1. Confirmez une cible de déploiement Blackwell/Linux. Le point de contrôle publié est testé sur B200/B300 et liste SGLang et vLLM comme moteurs pris en charge.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
2. Pour un service direct, partez de la configuration officielle SGLang ou vLLM : SGLang nécessite `transformers>=5.3.0` et `modelopt_fp4` ; l'exemple vLLM utilise `vllm/vllm-openai:v0.23.0`, un parallélisme de tenseurs de 8, un parallélisme d'experts, les parseurs GLM et un cache KV en FP8.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
3. Pour un cluster Dynamo, sélectionnez la cible B200 NVFP4 pour ce point de contrôle, provisionnez le cache de modèles partagé et le jeton Hugging Face, déployez la recette agrégée ou désagrégée correspondante, puis lancez son test de fumée compatible OpenAI.
  — <https://docs.nvidia.com/dynamo/dev/recipes/glm-5-2>
4. Validez la précision, la sûreté et le comportement système sur des données propres au cas d'usage avant la mise en production.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>

## Bonnes pratiques {#best-practices}

- Considérez les versions de runtime et les options de parseur fournies comme point de départ contractuel, et non comme une commande de lancement générique de GLM-5.2.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
- Avec NVIDIA Dynamo, ne remplacez pas l'image SGLang standard par l'image de développement GLM-5.2 documentée tant que ses correctifs requis ne figurent pas dans une version stable.
  — <https://docs.nvidia.com/dynamo/v1.4.2/reference/model-early-access-builds>
- Dimensionnez la capacité d'après la recette de déploiement, et non d'après la limite de 1M du point de contrôle : le chemin B200 NVFP4 documenté prend en charge jusqu'à 500K de contexte avec déchargement CPU HiCache ; le chemin H200 FP8 prend en charge jusqu'à 250K.
  — <https://docs.nvidia.com/dynamo/dev/recipes/glm-5-2>
- Ne déduisez pas une quantification de l'ensemble du modèle : NVIDIA indique que seuls les opérateurs linéaires des blocs de transformeur experts MoE sont quantifiés en NVFP4, tandis que l'expert partagé reste non quantifié.
  — <https://huggingface.co/nvidia/GLM-5.2-NVFP4>
- Avant d'utiliser l'artefact NIM, vérifiez son manifeste et sa précision plutôt que de vous fier au seul libellé du catalogue.
  — <https://catalog.ngc.nvidia.com/orgs/nim/zai-org/models/glm-52/nim-aec724e-nvfp4>

## Remplacé par {#superseded-by-this}

- 2026-07-20 — Pour la voie SGLang de NVIDIA Dynamo, les recommandations génériques sur les runtimes stables sont remplacées par l'image de développement GLM-5.2 documentée, tant que ses correctifs requis ne sont pas disponibles dans une version stable de SGLang.

## Points inconnus {#still-unknown}

- NVIDIA NGC étiquette `nim-aec724e-nvfp4` comme NVFP4 mais décrit le modèle de préparation comme FP8 ; sa page publique ne permet pas de lever le doute sur la précision exacte de l'artefact.
- L'interface Hugging Face affiche 381 Md de paramètres, alors que la fiche du modèle indique 753 Md au total et 40 Md actifs ; la page n'explique pas l'écart, il ne faut donc pas utiliser le chiffre de l'interface pour déduire les besoins en mémoire.
- La déclaration de contexte de 1M dans la fiche ne constitue pas une garantie de déploiement de bout en bout : les recettes Dynamo actuelles documentent 500K sur B200 et 250K sur H200.
- Aucune source primaire en chinois simplifié spécifique à NVIDIA GLM-5.2-NVFP4 n'a été retrouvée ; les recommandations de maintenance ou de déploiement en chinois restent non vérifiées.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/nvidia/GLM-5.2-NVFP4 | nvidia/GLM-5.2-NVFP4 · Hugging Face | 2026-09-06 |
| https://catalog.ngc.nvidia.com/orgs/nim/zai-org/models/glm-52/nim-aec724e-nvfp4 | zai-org GLM-5.2 | NVIDIA NGC | 2026-09-06 |
| https://docs.nvidia.com/dynamo/v1.4.2/reference/model-early-access-builds | Model Early Access Builds | NVIDIA Dynamo Documentation | 2026-09-06 |
| https://docs.nvidia.com/dynamo/dev/reference/releases/v1-4-0 | Dynamo v1.4.0 | NVIDIA Dynamo Documentation | 2026-09-06 |
| https://docs.nvidia.com/dynamo/dev/recipes/glm-5-2 | GLM-5.3/5.2 | NVIDIA Dynamo Documentation | 2026-09-06 |
