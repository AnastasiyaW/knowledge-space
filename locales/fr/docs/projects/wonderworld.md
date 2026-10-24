---
title: "WonderWorld"
category: projects
date: 2024-12-30
tags: [project, wonderworld, wonderworld-development]
aliases: ["WonderWorld"]
level: 2
source_sha256: c9a4973fe00eb61c34dec8db3bec23974cf0ee07bf3b581a70290645abc4f0fd
translation: machine
translated_at: '2026-10-24'
---
# WonderWorld {#wonderworld}

**Ligne de développement :** `project:wonderworld` · fil `wonderworld-development`  
**Dernier événement :** 2024-12-30 · 2 datés depuis 2024-07-11 · **Consulté le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

WonderWorld est le code d'une méthode de recherche destinée aux développeurs de génération 3D : à partir d'une seule image de départ, il construit et complète de manière interactive des scènes 3D liées, en fonction des mouvements de caméra et de descriptions textuelles. Fonctionnalités : représentation FLAGS, génération couche par couche, guided depth diffusion ; repère de performance : 9,5 secondes par scène sur A6000. Verdict : pile de recherche reproductible, nécessitant un GPU CUDA doté de 48 Go de mémoire, et non un produit cloud prêt à l'emploi.

## Ligne de développement {#development-line}

- **2024-07-11 — Site du projet WonderWorld référencé.** Le 2024-07-11, la fiche renvoyait vers un site public du projet WonderWorld. Ce lien daté établit une référence publique au projet, mais ne montre pas s'il marquait un lancement, une mise à jour ou une republication.
- **2024-12-30 — Dépôt GitHub de WonderWorld référencé.** Le 2024-12-30, la fiche renvoyait vers le dépôt GitHub de WonderWorld. Cela ajoute une référence d'hébergement de code à la ligne de développement, mais les seuls liens datés ne permettent pas de savoir si le dépôt venait d'être publié ou s'il était simplement mentionné.

## Ce qui a changé {#what-changed}

2024-07-11 — la page du projet présentait la génération interactive de scènes 3D liées à partir d'une seule image ; le préprint du 2024-06-13 précise FLAGS et guided depth diffusion, et annonce un temps inférieur à 10 secondes sur A6000. 2024-12-30 — du code public est apparu, transformant la méthode en pipeline local reproductible, avec des configurations, une visualisation interactive et la sauvegarde de la scène générée. 2025-06-11 — le travail a été publié à CVPR 2025 en tant que Highlight ; il s'agit d'un statut de publication, et non d'une nouvelle version du code public.

## Mode d'emploi {#how-to-use-this}

À partir du 2024-12-30, les praticiens qui évaluent WonderWorld devraient consulter ensemble la page du projet et le dépôt GitHub liés ; les seuls liens datés ne permettent pas d'établir des consignes d'installation, de reproduction ou de disponibilité pour une publication.

1. Cloner le dépôt, créer un environnement Python 3.10 et installer les dépendances selon le README sur une machine compatible CUDA disposant de 48 Go de mémoire GPU.
  — <https://github.com/KovenYu/WonderWorld>
2. Télécharger le checkpoint RepViT-SAM à la racine du dépôt et, si nécessaire, définir une clé OpenAI uniquement pour la création automatique des descriptions de scènes.
  — <https://github.com/KovenYu/WonderWorld>
3. Configurer l'exemple YAML, lancer run.py sur le serveur, ouvrir le viewer local via un tunnel SSH et choisir un nouveau point de vue avec la touche R ; X enregistre le résultat.
  — <https://github.com/KovenYu/WonderWorld>

## Bonnes pratiques {#best-practices}

- Partir de example.yaml tel quel et ne modifier les paramètres qu'un à la fois ; le README couvre depth_conditioning et les paramètres de caméra, et la page actuelle du projet avertit que les objets complexes peuvent produire des holes et des floaters lors d'un changement de point de vue.
  — <https://github.com/KovenYu/WonderWorld>
- Utiliser une description textuelle manuelle de la scène si un LLM externe n'est pas nécessaire ; use_gpt=False laisse la description sous le contrôle de l'opérateur.
  — <https://github.com/KovenYu/WonderWorld>
- Sauvegarder les mondes réussis et les charger via load_gen plutôt que de les régénérer.
  — <https://github.com/KovenYu/WonderWorld>

## Remplacé par ceci {#superseded-by-this}

- 2024-06-13 — l'affirmation du préprint « le code sera publié » est obsolète : le dépôt public contient désormais les instructions d'installation et de lancement.
- 2024-06-13 — le statut de simple préprint est obsolète : la page du projet indique CVPR 2025 (Highlight).

## Toujours inconnu {#still-unknown}

- La date initiale et le contenu exact du premier commit public du dépôt ne sont pas confirmés par une réponse datée et indépendante de l'API GitHub ; l'événement du 2024-12-30 confirme l'existence d'un lien vers le dépôt, mais pas la date d'un commit précis.
- Le README public ne précise pas le statut de maintenance au-delà des cinq commits affichés ; il est donc impossible d'affirmer que le projet est activement maintenu.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://wonderworld-2024.github.io/ | WonderWorld 2024 project page | 2026-09-05 |
| https://github.com/KovenYu/WonderWorld | KovenYu/WonderWorld repository and README | 2026-09-05 |
| https://arxiv.org/abs/2406.09394 | WonderWorld: Interactive 3D Scene Generation from a Single Image | 2026-09-05 |
| https://kovenyu.com/wonderworld/ | WonderWorld project page | 2026-09-05 |
| https://openaccess.thecvf.com/content/CVPR2025/papers/Yu_WonderWorld_Interactive_3D_Scene_Generation_from_a_Single_Image_CVPR_2025_paper.pdf | WonderWorld CVPR 2025 paper | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:wonderworld`, fil `wonderworld-development`, 2 événements datés du 2024-07-11 au 2024-12-30.
- **Remarque pratique :** À partir du 2024-12-30, les praticiens qui évaluent WonderWorld devraient consulter ensemble la page du projet et le dépôt GitHub liés ; les seuls liens datés ne permettent pas d'établir des consignes d'installation, de reproduction ou de disponibilité pour une publication.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
