---
title: "MTVCrafter"
category: projects
date: 2025-05-22
tags: [mtvcrafter, mtvcrafter-public-development, project]
aliases: ["MTVCrafter"]
level: 3
source_sha256: cd74f7b339d4694cdf699c0a81fdb7ef4ee28386df8ca0ba87cadca58ae72d7a
translation: machine
translated_at: '2026-10-24'
---
# MTVCrafter {#mtvcrafter}

**Ligne de développement :** `project:mtvcrafter` · fil `mtvcrafter-public-development`  
**Dernier événement :** 2025-05-22 · 1 événement daté depuis le 2025-05-22 · **Consulté le :** 2026-09-04 · confiance : moyenne

## Qu'est-ce que c'est {#what-it-is}

MTVCrafter est un pipeline local d'animation d'images humaines destiné aux utilisateurs de GPU, qui fournit une image de référence et une vidéo de pilotage avec un mouvement SMPL récupérable.

- 4DMoT transforme les articulations 3D au fil du temps en jetons de mouvement.
- MV-DiT pilote un backbone image-vers-vidéo CogVideoX ou Wan2.1.
- La voie Wan ajoute un contrôle par texte.

Les scripts fournis génèrent des unités de 49 images et ciblent CUDA. Exécutez le dépôt et les points de contrôle en local, car l'Space officiel ne dispose pas d'un pilote GPU fonctionnel.

## Ligne de développement {#development-line}

- **2025-05-22 — Les ressources publiques de MTVCrafter ont été mises en ligne.** MTVCrafter a établi l'approche 4DMoT couplée à MV-DiT. Il anime directement une image de référence à partir d'un mouvement 3D brut, et non de cartes de pose 2D rendues.

## Modifications {#what-changed}

- 2025-05-22 : MTVCrafter a établi l'approche 4DMoT couplée à MV-DiT. Le pipeline anime directement une image de référence à partir d'un mouvement 3D brut, plutôt que de cartes de pose 2D rendues.
- 2025-08-15 : L'arborescence des points de contrôle MV-DiT associés a séparé la méthode en deux voies d'inférence locale, CogVideoX et Wan-2.1.

## Comment l'utiliser {#how-to-use-this}

À partir du 2025-05-22, commencez par la page de projet datée, le dépôt et la page de modèle Hugging Face pour localiser MTVCrafter. Le lien du 2025-08-15 seul n'établit pas un nouveau composant, une nouvelle version ou un nouveau flux de travail.

1. Clonez l'implémentation actuelle, créez un environnement Python 3.10+ propre et installez requirements.txt.
  — <https://github.com/DINGYANB/MTVCrafter>
2. Téléchargez l'estimateur de pose NLF, un modèle de base correspondant (CogVideoX-5B pour le 7B ou Wan2.1 I2V-14B pour le 17B) et les poids MTVCrafter 4DMoT/MV-DiT.
  — <https://github.com/DINGYANB/MTVCrafter>
3. Commencez avec data/sampled_data.pkl ; pour une vidéo de pilotage, exécutez process_nlf.py afin de créer l'entrée .pkl de vidéo de mouvement SMPL.
  — <https://github.com/DINGYANB/MTVCrafter>
4. Lancez la voie CogVideoX avec infer_7b.py, une image de référence, le chemin des données de mouvement et --output_dir.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_7b.py>
5. Pour un guidage textuel Wan, utilisez infer_17b.py avec les mêmes chemins et l'option --prompt facultative ; il accepte aussi --output_dir.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_17b.py>
6. Pour la voie 17B, fournissez au moins 89 images d'entrée : le script joint deux clips de 49 images avec un recouvrement de neuf images.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_17b.py>

## Bonnes pratiques {#best-practices}

- Installez les dépendances du projet épinglées dans un environnement propre, plutôt que d'assembler une pile Diffusers générique.
  — <https://github.com/DINGYANB/MTVCrafter>
- Utilisez --output_dir, l'option de sortie actuellement documentée et implémentée pour les deux voies d'inférence.
  — <https://github.com/DINGYANB/MTVCrafter>
- Vérifiez la présence d'un GPU CUDA avant l'exécution ; l'Space officiel échoue car son environnement d'exécution ne dispose d'aucun pilote NVIDIA.
  — <https://huggingface.co/spaces/yanboding/MTVCrafter>
- Validez une première exécution avec le fichier sampled_data.pkl fourni avant de déboguer l'extraction NLF à partir de vidéos personnalisées.
  — <https://github.com/DINGYANB/MTVCrafter>
- Utilisez les scripts des auteurs comme chemin de référence : le script 7B construit un MTVCrafterPipeline7B personnalisé et charge séparément les ressources CogVideoX et 4DMoT.
  — <https://github.com/DINGYANB/MTVCrafter/blob/main/infer_7b.py>
- Considérez le LoRA Wan FusionX optionnel comme un compromis : les mainteneurs indiquent qu'il peut améliorer la vitesse et le détail, mais qu'il peut dégrader la précision du mouvement.
  — <https://github.com/DINGYANB/MTVCrafter>

## Remplacé par {#superseded-by-this}

- 2025-08-24 : Les indications de démarrage rapide utilisant --output_path sont obsolètes ; les scripts d'inférence actuels utilisent --output_dir.
- 2026-03-09 : MTVCrafter n'est plus le titre de l'article arXiv ; citez MTVCraft pour l'article révisé et MTVCrafter pour les dépôts.
- 2026-09-04 : L'indication d'utiliser la démo Space officielle est obsolète ; le Space échoue avant l'inférence car son environnement d'exécution ne dispose pas de pilote NVIDIA.
- 2026-09-04 : Considérer DINGYANB/MTVCtafter comme la copie de travail du code est obsolète ; il s'agit du dépôt statique de la page de projet.

## Points encore inconnus {#still-unknown}

- L'arborescence MV-DiT du 2025-08-15 ne comporte pas de date de publication déclarée par l'auteur ; sa date exacte de publication ne peut donc pas être vérifiée de manière indépendante.
- Les mainteneurs lient la page de projet statique MTVCtafter et le dépôt de code exécutable MTVCrafter, sans avoir documenté la raison de la différence entre les noms.
- L'article arXiv révisé est intitulé MTVCraft, tandis que les dépôts de code et de modèles conservent MTVCrafter ; aucune note des mainteneurs n'explique ce changement de nom.
- Aucune documentation officielle en chinois ni aucun retour d'expérience indépendant et reproductible en chinois n'a été trouvé.
- Aucune exigence officielle actuelle en mémoire GPU ni aucun benchmark de qualité reproduit de manière indépendante n'a été trouvé.
- Il n'est pas confirmé que l'extrait Diffusers générique de la page du modèle reproduise les scripts d'inférence maintenus par les auteurs.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://dingyanb.github.io/MTVCtafter/ | Page de projet MTVCrafter | 2026-09-04 |
| https://github.com/dingyanb/MTVCtafter | Dépôt de la page de projet DINGYANB/MTVCtafter | 2026-09-04 |
| https://github.com/DINGYANB/MTVCtafter/blob/main/index.html | Source statique de la page de projet MTVCtafter | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter | Dépôt d'implémentation DINGYANB/MTVCrafter | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter/commits/main | Historique des commits DINGYANB/MTVCrafter | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter/blob/main/infer_7b.py | Script d'inférence MTVCrafter 7B | 2026-09-04 |
| https://github.com/DINGYANB/MTVCrafter/blob/main/infer_17b.py | Script d'inférence MTVCrafter 17B | 2026-09-04 |
| https://huggingface.co/yanboding/MTVCrafter | Dépôt de modèle yanboding/MTVCrafter | 2026-09-04 |
| https://huggingface.co/yanboding/MTVCrafter/tree/main/MV-DiT | Arborescence des points de contrôle MV-DiT de MTVCrafter | 2026-09-04 |
| https://huggingface.co/yanboding/MTVCrafter/blob/main/README.md | README de la fiche modèle MTVCrafter | 2026-09-04 |
| https://huggingface.co/spaces/yanboding/MTVCrafter | Statut d'exécution du Space Hugging Face MTVCrafter | 2026-09-04 |
| https://arxiv.org/abs/2505.10238 | Notice de l'article MTVCraft / MTVCrafter | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:mtvcrafter`, fil `mtvcrafter-public-development`, 1 événement daté du 2025-05-22 au 2025-05-22.
- **Note pratique :** À partir du 2025-05-22, les praticiens doivent commencer par la page de projet datée, le dépôt et la page de modèle Hugging Face pour localiser MTVCrafter. Le lien du 2025-08-15 seul n'établit pas un nouveau composant, une nouvelle version ou un nouveau flux de travail.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
