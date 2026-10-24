---
title: "Distillation par correspondance de contexte"
category: projects
date: 2026-08-21
tags: [context-matched-distillation, nvidia-cmd, nvidia-cosmos, project]
aliases: ["Context-Matched Distillation"]
level: 3
source_sha256: 46b3df60cce689ec9190e316927f45ccd2f36058f4fce02058c5b554b5330e7c
translation: machine
translated_at: '2026-10-24'
---
# Distillation par correspondance de contexte {#context-matched-distillation}

**Ligne de développement :** `project:nvidia-cmd` · fil `context-matched-distillation`  
**Dernier événement :** 2026-08-21 · 1 daté depuis le 2026-08-21 · **Recherché le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

La Context-Matched Distillation (CMD) est une méthode de distillation par correspondance de distribution causale développée par NVIDIA, accompagnée d'une publication de points de contrôle (checkpoints) pour la génération autoregressive d'image vers vidéo.

- Génération en chunk-1 ou chunk-4.
- Rollouts longs.
- Variantes conditionnées par la caméra.

Le code CMD publié et ses dérivés ne sont autorisés qu'à des fins de recherche non commerciale et d'enseignement. Le modèle de base Cosmos sous-jacent nécessite également une demande d'accès approuvée. Utilisez-le pour évaluer la recherche interactive sur l'image vers vidéo causale, et non comme une pile vidéo commerciale prête à l'emploi.

## Ligne de développement {#development-line}

- **2026-08-21 — Publication des ressources Context-Matched Distillation.** Le 2026-08-21, NVIDIA a publié la page de projet, le dépôt de code, la page du modèle et la démonstration image vers vidéo de la Context-Matched Distillation (CMD). Ces liens ont ouvert le projet à un examen public.

## Changements {#what-changed}

- 2026-08-13 — L'article CMD a introduit le scoring causal du teacher, le Prefix Scoring et la Prefix Corruption pour la distillation vidéo autoregressive en peu d'étapes.
- 2026-08-19 — Le dépôt Hugging Face de CMD a été créé.
- 2026-08-21 — CMD a été documenté avec sa page de projet, son dépôt de code, son dépôt de modèle et un lien vers une démonstration image vers vidéo.
- 2026-08-23 — NVIDIA a ajouté la fiche de modèle CMD et les checkpoints, couvrant les variantes chunk-1/chunk-4 courtes, longues et conditionnées par la caméra.
- 2026-08-24 — NVIDIA a mis à jour la fiche de modèle avec la citation arXiv.
- 2026-08-30 — Le dépôt de modèle a ajouté config.json.

## Mode d'emploi {#how-to-use-this}

Au 2026-08-21, évaluez CMD en examinant conjointement le code lié, la page du modèle, la documentation et la démonstration.

1. Demandez l'accès au modèle de base Cosmos-Predict2.5 2B avant d'exécuter CMD.
  — <https://huggingface.co/nvidia/Cosmos-Predict2.5-2B>
2. Clonez CMD, créez l'environnement conda Python 3.10, installez les dépendances et FlashAttention, puis installez le paquet en mode développement.
  — <https://github.com/nv-tlabs/cmd>
3. Téléchargez tous les checkpoints CMD, ou seulement le checkpoint nécessaire pour une variante choisie.
  — <https://huggingface.co/nvidia/cmd>
4. Associez le checkpoint à sa configuration fournie, à l'image, au prompt, à la taille de bloc, à la fenêtre d'attention locale et au nombre de frames de sortie demandé ; le dépôt donne un exemple d'invocation chunk-4 pour une vidéo courte.
  — <https://github.com/nv-tlabs/cmd>
5. Exécutez le script d'exemple fourni pour l'une des variantes courte, longue ou conditionnée par la caméra avant de remplacer les entrées d'exemple.
  — <https://github.com/nv-tlabs/cmd>

## Bonnes pratiques {#best-practices}

- Considérez l'appariement checkpoint/configuration comme un invariant : t désigne la durée d'une frame et l désigne la longueur de l'attention locale, tandis que chunk-1 et chunk-4 utilisent des granularités de génération différentes.
  — <https://huggingface.co/nvidia/cmd>
- Évaluez les rollouts longs sur des entrées représentatives : les erreurs autoregressives s'accumulent et dégradent la cohérence temporelle, les détails fins, les visages, les mains, le texte et les mouvements rapides.
  — <https://huggingface.co/nvidia/cmd>
- Ne vous attendez pas à ce que la configuration publique DL3DV reproduise la qualité rapportée ; elle ne sert qu'à vérifier le pipeline de bout en bout, tandis que les données d'entraînement rapportées ne sont pas publiées.
  — <https://github.com/nv-tlabs/cmd>
- Gardez l'usage et les dérivés de CMD non commerciaux, sauf si la licence évolue ; toute redistribution doit conserver la licence et les mentions légales.
  — <https://github.com/nv-tlabs/cmd/blob/main/LICENSE>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Inconnues restantes {#still-unknown}

- L'historique des commits Hugging Face date le dépôt initial de CMD au 2026-08-19 et le téléversement du checkpoint et de la fiche de modèle au 2026-08-23, alors que l'événement du 2026-08-21 comportait déjà l'URL du modèle. La liste de liens a peut-être été enrichie après l'événement daté ; cela ne peut pas être tranché à partir de l'historique de première main disponible.
- La page de démonstration publique était accessible en tant que Space Hugging Face, mais n'exposait ni paramètres d'exécution reproductibles ni garantie de disponibilité.
- Aucune donnée de première main sur les benchmarks post-publication ni sur un déploiement en production n'a été trouvée ; les résultats de l'article restent des éléments de recherche et non un SLA de production.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://arxiv.org/abs/2608.13391 | Context-Matched Distillation: Teacher Causality for Autoregressive Video Distillation | 2026-09-05 |
| https://hmrishavbandy.github.io/cmd-site/ | Page de projet Context-Matched Distillation | 2026-09-05 |
| https://github.com/nv-tlabs/cmd | nv-tlabs/cmd | 2026-09-05 |
| https://huggingface.co/nvidia/cmd | Fiche de modèle nvidia/cmd | 2026-09-05 |
| https://huggingface.co/nvidia/cmd/commits/main | Historique des commits nvidia/cmd | 2026-09-05 |
| https://huggingface.co/spaces/hugging-apps/cmd-i2v-demo | Démonstration NVIDIA CMD Image to Video | 2026-09-05 |
| https://huggingface.co/nvidia/Cosmos-Predict2.5-2B | Fiche de modèle Cosmos-Predict2.5-2B | 2026-09-05 |
| https://github.com/nv-tlabs/cmd/blob/main/LICENSE | NVIDIA OneWay Noncommercial License | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:nvidia-cmd`, fil `context-matched-distillation`, 1 événement daté du 2026-08-21 au 2026-08-21.
- **Note pratique :** Au 2026-08-21, les praticiens évaluant CMD doivent consulter ensemble le dépôt de code lié, la page du modèle, la documentation du projet et la démonstration image vers vidéo, plutôt que de traiter l'annonce comme une référence de recherche non étayée.
- **Confiance :** élevée. Les remplacements datés ci-dessus font autorité pour déterminer ce qui est obsolète.
