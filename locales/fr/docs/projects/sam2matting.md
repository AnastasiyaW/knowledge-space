---
title: "SAM2Matting"
category: projects
date: 2026-07-15
tags: [project, sam2matting, sam2matting-public-release]
aliases: ["SAM2Matting"]
level: 3
source_sha256: 68ab791325f52efeb45f14a0a0884361b19e97c825c8983001f4ae38d217bf03
translation: machine
translated_at: '2026-10-24'
---
# SAM2Matting {#sam2matting}

**Ligne de développement :** `project:sam2matting` · fil `sam2matting-public-release`  
**Dernier événement :** 2026-07-15 · 1 événement daté depuis le 2026-07-15 · **Recherche effectuée le :** 2026-09-08 · confiance : moyenne

## Qu'est-ce que c'est {#what-it-is}

SAM2Matting est un framework d'inférence qui transforme des prompts de premier plan en mattes alpha pour la composition d'images et de vidéos.

- Affinage de matte : transforme des masques, des points, des boîtes et des prompts texte SAM3 en mattes aux bords fins.
- Matting vidéo : combine le suivi temporel avec des têtes de matting dédiées.

Les poids publiés font 216 Mo (Tiny), 383 Mo (Base+) et 3,51 Go (SAM3). Le code d'entraînement n'a pas été publié, et la licence CC BY-NC-SA 4.0 est non commerciale. Utilisez donc ce projet pour évaluer l'inférence, et non comme pile d'entraînement publiée ni comme solution de déploiement commercial.

## Ligne de développement {#development-line}

- **2026-07-15 — Les ressources publiques du projet SAM2Matting sont devenues disponibles.** Le 2026-07-15, SAM2Matting a été présenté à travers des ressources officielles liées : page du projet, code source, hébergement des modèles et démo interactive. Il s'agit d'une étape significative vers l'accès public, car les lecteurs peuvent désormais localiser l'implémentation et l'évaluer via les ressources liées.

## Ce qui a changé {#what-changed}

- 2026-06-22 — Le dépôt source de SAM2Matting a été initialisé.
- 2026-06-25 — La version v1 de SAM2Matting a été soumise sur arXiv et ses trois points de contrôle d'inférence ont été envoyés.
- 2026-06-30 — SAM2Matting a supprimé `pip install -e .` et corrigé les dépendances ; c'est toujours le dernier changement en amont sur GitHub.
- 2026-07-09 — SAM2Matting a reçu une fiche de modèle Hugging Face et le tag `image-segmentation` ; cela a modifié la documentation, et non les poids ni le code.
- 2026-07-15 — SAM2Matting était disponible sous forme de lot projet-code-point de contrôle-démo ; les historiques principaux n'établissent pas de nouvelle version en amont à cette date.

## Mode d'emploi {#how-to-use-this}

1. Clonez le dépôt en amont, créez son environnement Conda Python 3.10, puis exécutez `pip install -r requirements.txt`.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/README.md>
2. Téléchargez un point de contrôle officiel dans `checkpoints/` et associez-le à la famille de scripts SAM2 ou SAM3.
  — <https://huggingface.co/FudanCVL/SAM2Matting>
3. Pour la vidéo, fournissez un masque de premier plan sur la première image, puis modifiez les chemins codés en dur du script de démo (variante, entrée, masque et sortie), ou encapsulez-le, avant d'utiliser vos propres médias.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/inference_video_sam2.py>
4. Pour les prompts interactifs, utilisez `interactive_sam2.py` pour les points ou les boîtes, et `interactive_sam3.py` pour le texte.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/README.md>
5. Pour un essai dans le navigateur, utilisez le Space officiel avec une image et un masque de premier plan approximatif ; il renvoie un matte alpha, un aperçu de composition et un PNG transparent.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>

## Bonnes pratiques {#best-practices}

- Utilisez un masque qui couvre approximativement le premier plan, en blanc pour le premier plan ; les masques en niveaux de gris doux sont recommandés.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>
- Utilisez SAM2.1-Tiny lorsque la vitesse compte ; réservez SAM3 aux cas où son support des prompts justifie davantage de VRAM et de temps.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>
- Pour une vidéo hébergée sur le Space, initialisez la première image et gardez un nombre d'images modeste ; cette limite est propre à la démo ZeroGPU.
  — <https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py>
- N'automatisez pas la commande `--save_mp4` du README telle quelle : le code actuel la définit avec `store_false` alors que la sauvegarde est activée par défaut.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/inference_video_sam2.py>
- Restez dans un usage non commercial, ou obtenez une autorisation pour un autre cas d'usage selon la licence indiquée.
  — <https://github.com/FudanCVL/SAM2Matting/blob/main/README.md>

## Remplacé par {#superseded-by-this}

- 2026-06-30 — l'ancienne instruction d'installation consistant à ajouter `pip install -e .` est obsolète ; l'amont l'a supprimée au profit de l'installation des dépendances listées.

## Points encore inconnus {#still-unknown}

- Aucune page en chinois émanant des auteurs ni aucun retour d'expérience indépendant et reproductible en chinois n'a été trouvé dans la recherche en chinois ; aucune recette pratique en chinois n'est donc avancée.
- Aucune exécution locale en propre ni aucun benchmark indépendant et actuel de qualité ou de débit n'a été trouvé ; les résultats de l'article ne sont pas utilisés comme attentes de production.
- Le Space officiel n'expose pas d'horodatage absolu stable pour son déploiement actuel ; son état applicatif actuel n'est donc pas consigné comme événement daté.
- Le README et le code actuel divergent au sujet de `--save_mp4` ; un wrapper ou une correction du code doit être testé avant toute automatisation reproductible.
- Le code d'entraînement officiel, une procédure de finetuning, une matrice de GPU supportés et une exigence minimale de VRAM n'ont pas été trouvés.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://henghuiding.com/SAM2Matting/ | Page du projet SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting | Dépôt FudanCVL/SAM2Matting | 2026-09-08 |
| https://huggingface.co/FudanCVL/SAM2Matting | Dépôt de modèle FudanCVL/SAM2Matting | 2026-09-08 |
| https://huggingface.co/spaces/FudanCVL/sam2matting | Space FudanCVL/sam2matting | 2026-09-08 |
| https://arxiv.org/abs/2606.27339 | SAM2Matting: Generalized Image and Video Matting — arXiv | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/commits/main | Commits — FudanCVL/SAM2Matting | 2026-09-08 |
| https://huggingface.co/FudanCVL/SAM2Matting/commit/6f92789a2a16ae899e81470a1b4dc47e08f40db3 | Upload checkpoints — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/commit/73dd721d77b56749248aefe5e8824d7f61b9d13c | update install and requirements — FudanCVL/SAM2Matting | 2026-09-08 |
| https://huggingface.co/FudanCVL/SAM2Matting/discussions/1 | Model-card and pipeline-tag pull request — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/releases | Releases — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/blob/main/README.md | README de SAM2Matting — FudanCVL/SAM2Matting | 2026-09-08 |
| https://github.com/FudanCVL/SAM2Matting/blob/main/inference_video_sam2.py | inference_video_sam2.py — FudanCVL/SAM2Matting | 2026-09-08 |
| https://huggingface.co/spaces/FudanCVL/sam2matting/blob/main/app.py | app.py — Space FudanCVL/sam2matting | 2026-09-08 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:sam2matting`, fil `sam2matting-public-release`, 1 événement daté du 2026-07-15 au 2026-07-15.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
