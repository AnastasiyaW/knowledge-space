---
title: "Cosmos 3 Edge"
category: projects
date: 2026-07-21
tags: [cosmos-3-edge, nvidia-cosmos-3-edge, project]
aliases: ["Cosmos 3 Edge"]
level: 2
source_sha256: 9833a5dbf4c67e324b9f220dd9bcbfb2f1589b189b07dae8d3799252f67f429f
translation: machine
translated_at: '2026-10-24'
---
# Cosmos 3 Edge {#cosmos-3-edge}

**Ligne de développement :** `project:nvidia-cosmos-3-edge` · fil `cosmos-3-edge`  
**Dernier événement :** 2026-07-21 · 1 événement daté depuis le 2026-07-21 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

Cosmos 3 Edge est un modèle de monde multimodal à poids ouverts de 4B paramètres, destiné aux équipes de robotique, de conduite autonome et d'espaces intelligents.

- Entrées : accepte du texte, des images, de la vidéo et des trajectoires d'actions.
- Sorties : produit du texte, des images, de la vidéo et des actions.
- Politique : fournit une variante de manipulation DROID.

La version actuelle du générateur est centrée sur l'image-vers-vidéo, à une résolution de 832×480, 121 images et 20 étapes de débruitage. Utilisez-la prototypage local d'IA physique lorsque les chemins de générateur et de raisonneur pris en charge correspondent à la cible de déploiement.

## Ligne de développement {#development-line}

- **2026-07-21 — NVIDIA a publié Cosmos3-Edge sur Hugging Face.** Le 2026-07-21, le billet de blog de NVIDIA sur Hugging Face et les liens vers le dépôt de modèles de Cosmos3-Edge ont été consignés. Ensemble, ils indiquent une étape officielle de mise à disposition publique du projet, ce qui la rend significative dans son historique de développement. Les liens fournis n'établissent ni les capacités, ni la licence, ni les détails de déploiement.

## Modifications {#what-changed}

- **2026-07-21** — Cosmos3-Edge et Cosmos3-Edge-Policy-DROID, publiés le 2026-07-20 sous forme de modèles de 4B sous licence OpenMDW 1.1 ; cette version ajoute un modèle multimodal de base compact et une variante de politique de manipulation DROID.
- **2026-08-25** — NVIDIA a mis à jour les poids, les valeurs par défaut, les exemples et les benchmarks du générateur Edge ; la recette de générateur maintenue ne supporte désormais que l'image-vers-vidéo, en remplacement des anciens exemples Edge texte-vers-image et texte-vers-vidéo.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-07-21, les praticiens qui suivent Cosmos 3 Edge devraient considérer le dépôt de modèles Hugging Face de NVIDIA comme un point de référence officiel pour l'évaluation, tout en vérifiant les capacités, la licence et les exigences de déploiement dans les documents sous-jacents avant utilisation.

1. Téléchargez un instantané local récent du modèle avant d'utiliser la recette de générateur mise à jour.
  — <https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62>
2. Pour le raisonnement sur un seul GPU, servez Cosmos3-Edge avec vLLM et son API compatible OpenAI ; utilisez vLLM 0.23.0 ou une version ultérieure.
  — <https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md>
3. Pour l'inférence du générateur, utilisez les paramètres actuels d'image-vers-vidéo : 832×480, 121 images, 20 étapes, guidance 6.0 et flow shift 12.0.
  — <https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62>

## Bonnes pratiques {#best-practices}

- Actualisez les instantanés locaux lorsque vous suivez la branche principale ; la mise à jour d'août a modifié les poids, les valeurs par défaut, les exemples et les benchmarks.
  — <https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62>
- Ne chargez pas Edge via Cosmos3OmniForConditionalGeneration ; son intégration Transformers distincte utilise AutoModelForImageTextToText et Cosmos3EdgeForConditionalGeneration.
  — <https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md>
- Gardez les garde-fous activés, sauf si une décision de déploiement explicite accepte la responsabilité de conformité ; leur désactivation s'applique à l'ensemble du serveur.
  — <https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md>
- Intégrez la tour de vision dans les exports locaux pour le raisonnement hors ligne sur image ou vidéo ; sinon, elle peut devoir récupérer ses composants depuis le Hub.
  — <https://github.com/NVIDIA/cosmos-framework/blob/main/docs/inference.md>

## Remplacé par {#superseded-by-this}

- 2026-08-25 — Les exemples de générateur Edge texte-vers-image et texte-vers-vidéo sont obsolètes ; les exemples de générateur Edge maintenus ne supportent que l'image-vers-vidéo.
- 2026-08-25 — Les valeurs par défaut antérieures du générateur Edge sont obsolètes ; utilisez le point de contrôle actualisé et la recette image-vers-vidéo en 480p.

## Points non élucidés {#still-unknown}

- Le guide d'inférence actuel de Cosmos Framework qualifie Edge de modèle de 2B, alors que la fiche modèle NVIDIA et l'annonce de publication le présentent comme un modèle de 4B. Le chiffre de 4B est retenu ici, car il figure dans la section architecture de la fiche modèle et dans les documents de publication ; NVIDIA devrait harmoniser la documentation.
- Le schéma de réponse n'expose pas de champs distincts event_findings ou new_events. La constatation du 2026-07-21 et la mise à jour distincte du 2026-08-25 sont conservées dans what_changed.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/blog/nvidia/cosmos3edge | Introducing Cosmos 3 Edge | 2026-09-05 |
| https://huggingface.co/nvidia/Cosmos3-Edge | Fiche modèle nvidia/Cosmos3-Edge | 2026-09-05 |
| https://huggingface.co/nvidia/Cosmos3-Edge/discussions/62 | Mise à jour du point de contrôle et de la recette d'inférence de Cosmos3-Edge — août 2026 | 2026-09-05 |
| https://github.com/NVIDIA/cosmos/blob/main/cookbooks/cosmos3/README.md | Cosmos 3 cookbooks | 2026-09-05 |
| https://github.com/NVIDIA/cosmos-framework/blob/main/docs/inference.md | Guide d'inférence de Cosmos Framework | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:nvidia-cosmos-3-edge`, fil `cosmos-3-edge`, 1 événement daté du 2026-07-21 au 2026-07-21.
- **Note pratique :** À partir du 2026-07-21, les praticiens qui suivent Cosmos 3 Edge devraient considérer le dépôt de modèles Hugging Face de NVIDIA comme un point de référence officiel pour l'évaluation, tout en vérifiant les capacités, la licence et les exigences de déploiement dans les documents sous-jacents avant utilisation.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
