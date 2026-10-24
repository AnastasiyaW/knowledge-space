---
title: "OmniStream"
category: projects
date: 2026-03-13
tags: [omnistream, omnistream-development, project]
aliases: ["OmniStream"]
level: 2
source_sha256: e0a25cffb8d3c956624cf3149b589f06f4b01dca603b9174b3150717d7dfd162
translation: machine
translated_at: '2026-10-24'
---
# OmniStream {#omnistream}

**Ligne de développement :** `project:omnistream` · fil `omnistream-development`  
**Dernier événement :** 2026-03-13 · 1 événement daté depuis le 2026-03-13 · **Recherche :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

OmniStream est un backbone visuel de 0,3 milliard de paramètres dérivé de DINOv3 ViT-L, destiné à l'extraction continue de caractéristiques vidéo. Il utilise une attention spatio-temporelle causale, du 3D-RoPE et un cache KV persistant.

- traite les images en ligne sans recalculer l'attention sur les images précédentes ;
- transfère un backbone gelé vers des tâches de perception, de reconstruction, de VLM et de VLA ;
- est distribué sous forme de checkpoint Hugging Face F32 de 1,21 Go et d'un dépôt officiel d'inférence.

Le checkpoint public est un extracteur de caractéristiques d'image. Le dépôt indique toujours que le code de pré-entraînement et celui des VLM/VLA ne sont pas publiés. Il est utilisable dès maintenant pour des expériences d'extraction de caractéristiques sur CUDA, mais pas encore comme pile clé en main pour VLM ou pour le contrôle de robots.

## Ligne de développement {#development-line}

- **2026-03-13 — OmniStream a été publiquement relié à ses ressources de projet, de code et de modèle.** Le 2026-03-13, des liens sont apparus vers la page du projet OmniStream, le dépôt source GitHub et la ressource Hugging Face. Cela fournit un point de référence daté pour la présence web, le code et le modèle, sans fixer de version, de capacité ou de statut de publication précis.

## Ce qui a changé {#what-changed}

2026-03-12 — le rapport technique (arXiv:2603.12265) a été soumis. Il décrit le backbone causal en flux unifié, l'entraînement sur 29 jeux de données et le périmètre d'évaluation.

2026-03-13 — les supports du projet, le code et le checkpoint StreamFormer/OmniStream ont été publiés ou mis à jour. La version a rendu disponible l'extracteur de caractéristiques 0,3B en F32. Les commits de ce jour ont mis à jour le README du dépôt et la référence arXiv.

2026-03-15 — le dépôt a supprimé les chemins DINOv3 propres à un environnement et le code DINO-text intégré. Un espace réservé configurable a remplacé le chemin local codé en dur. Cela remplace les consignes qui supposent l'arborescence de fichiers d'origine des auteurs.

L'étape du 13 mars ajoute deux limites pratiques absentes des seuls liens d'événements : le checkpoint publié compte 0,3 milliard de paramètres, et le dépôt n'a pas publié son code de pré-entraînement ni celui des VLM/VLA.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-03-13, utilisez la page du projet OmniStream, le dépôt source et la ressource Hugging Face citée comme point de départ pour l'évaluation. Vérifiez indépendamment la version exacte du modèle, la licence et les instructions d'utilisation.

1. Clonez le dépôt officiel, créez un environnement Conda Python 3.10, puis installez la pile épinglée PyTorch 2.6.0 CUDA 12.4 et Transformers 4.56.1.
  — <https://github.com/Go2Heart/OmniStream>
2. Chargez `AutoImageProcessor` et `OmnistreamMultiFrameTransformer` depuis `StreamFormer/OmniStream`, placez les tenseurs et le modèle sur CUDA, appelez `eval()` et exécutez l'inférence sous `torch.no_grad()`.
  — <https://huggingface.co/StreamFormer/OmniStream>
3. Traitez la sortie comme des caractéristiques visuelles (`last_hidden_state`, `hidden_states`, `pooler_output` et les indices de patchs) ; fournissez vous-même une couche d'intégration pour une tâche en aval.
  — <https://github.com/Go2Heart/OmniStream>

## Bonnes pratiques {#best-practices}

- Utilisez les versions CUDA/PyTorch et Transformers épinglées par le dépôt pour le chemin d'inférence documenté. Le checkpoint n'est pas servi par un Hugging Face Inference Provider.
  — <https://github.com/Go2Heart/OmniStream>
- Conservez le `model.py` officiel dans l'environnement. La fiche du modèle indique qu'il est requis pour le workflow d'extraction de caractéristiques d'exemple.
  — <https://huggingface.co/StreamFormer/OmniStream>
- Ne vous fiez pas aux anciens chemins DINOv3 propres à la machine des auteurs. Configurez l'emplacement des poids DINOv3 pour votre propre environnement.
  — <https://github.com/Go2Heart/OmniStream/commit/780e5d7d60ea7788e9ee62395dc0d465d02dc873>

## Remplacé par ceci {#superseded-by-this}

- 2026-03-15 — les chemins DINOv3 propres à un environnement et la source DINO-text intégrée ont été supprimés. Ne reproduisez pas l'ancienne configuration à chemins locaux.
- 2026-03-15 — ne décrivez pas l'implémentation disponible comme une pile VLM/VLA de bout en bout publiée. Ces publications de code figurent toujours comme éléments TODO.

## Points encore inconnus {#still-unknown}

- Les sources primaires n'exposent pas d'horodatage daté de publication du checkpoint sur Hugging Face. Le moment exact où les poids sont devenus téléchargeables ne peut pas être distingué de la mise à jour du projet et du code du 2026-03-13.
- La page du projet présente des résultats de transfert vers les VLM et les VLA, mais le code public d'implémentation VLM et VLA n'est pas publié. La maturité en production de ces chemins n'est pas vérifiée.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://arxiv.org/abs/2603.12265 | OmniStream: Mastering Perception, Reconstruction and Action in Continuous Streams | 2026-09-05 |
| https://go2heart.github.io/omnistream/ | Page du projet OmniStream | 2026-09-05 |
| https://github.com/Go2Heart/OmniStream | Go2Heart/OmniStream | 2026-09-05 |
| https://github.com/Go2Heart/OmniStream/commits/main | Historique des commits d'OmniStream | 2026-09-05 |
| https://github.com/Go2Heart/OmniStream/commit/780e5d7d60ea7788e9ee62395dc0d465d02dc873 | fix: hard code and dino.txt | 2026-09-05 |
| https://huggingface.co/StreamFormer/OmniStream | Fiche du modèle StreamFormer/OmniStream | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:omnistream`, fil `omnistream-development`, 1 événement daté du 2026-03-13 au 2026-03-13.
- **Note pratique :** À partir du 2026-03-13, utilisez la page du projet OmniStream, le dépôt source et la ressource Hugging Face citée comme point de départ pour l'évaluation. Vérifiez indépendamment la version exacte du modèle, la licence et les instructions d'utilisation.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
