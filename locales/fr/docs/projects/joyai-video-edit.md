---
title: "JoyAI-Video-Edit"
category: projects
date: 2026-08-06
tags: [joyai-video-edit, joyai-video-edit-public-reference, joyai_video_edit, project]
aliases: ["JoyAI-Video-Edit"]
level: 2
source_sha256: 6181d24f08bad7193eb9b7174ba2d4fcb382ff4e3f9b26f5e301794a410f5269
translation: machine
translated_at: '2026-10-24'
---
# JoyAI-Video-Edit {#joyai-video-edit}

**Ligne de développement :** `project:joyai-video-edit` · fil `joyai-video-edit-public-reference`  
**Dernier événement :** 2026-08-06 · 1 événement daté depuis le 2026-08-06 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

JoyAI-Video-Edit : un éditeur vidéo autorégressif-diffusion de 16B sous licence Apache-2.0, destiné aux montages vidéo-vers-vidéo causaux et en direct.

- Modifications par texte, locales, d'arrière-plan, de style, de mouvement et guidées par image de référence.
- Entrée depuis une caméra en direct ou une vidéo téléversée, via WebSocket.
- Performance annoncée : 720p à environ 30 FPS sur un Nvidia B200 ; la configuration pour GPU grand public est de 840×480 à 24 FPS sur RTX 5090.

## Ligne de développement {#development-line}

- **2026-08-06 — Références publiques du projet JoyAI-Video-Edit enregistrées.** Le 2026-08-06, des liens publics sont apparus pour un dépôt GitHub, une page Hugging Face et un site de JoyAI Labs. Ces références attestent d'un travail en cours, mais ne précisent ni version de publication, ni capacité, ni état de lancement.

## Évolutions {#what-changed}

- 2026-08-06 — Code de déploiement, points de contrôle et rapport technique publiés ; le point de contrôle DiT initial était `joyai_video_edit_dit_0804.pth`.
- 2026-08-14 — Le point de contrôle DiT `joyai_video_edit_dit_0811.pth` a remplacé le point de contrôle initial pour le service et a amélioré l'édition guidée par image de référence.
- 2026-08-15 — Une démo Hugging Face en direct est devenue disponible sur du matériel RTX PRO 6000.
- 2026-08-24 — Le support officiel pour GPU grand public a ajouté une configuration RTX 5090 à 840×480 et 24 FPS.

## Mode d'emploi {#how-to-use-this}

Au 2026-08-06, consultez les références publiques du code, de la distribution des modèles et du site officiel afin de vérifier l'état exact de la publication et les consignes d'utilisation avant d'adopter JoyAI-Video-Edit.

1. Clonez le dépôt, créez un environnement Conda Python 3.10, puis installez `deploy/requirements.txt`.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit>
2. Compilez l'extension CUDA `joyomni_ops` incluse dans le dépôt ; pour le matériel Blackwell, utilisez CUDA nvcc 12.8 ou une version ultérieure.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>
3. Téléchargez `joyai_video_edit_dit_0811.pth`, les fichiers VAE et l'encodeur MiMo-VL requis dans l'arborescence de points de contrôle documentée.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>
4. Définissez les variables d'environnement propres à chaque GPU, puis exécutez `bash deploy/run_server.sh` ; ouvrez le port 8080 ou redirigez-le via SSH.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>

## Bonnes pratiques {#best-practices}

- Utilisez le point de contrôle DiT actuel `0811` ; `0804` n'est conservé que pour la reproductibilité et n'est pas la valeur par défaut du serveur.
  — <https://huggingface.co/jdopensource/JoyAI-Video-Edit>
- Attribuez une valeur `JOYOMNI_CACHE_ROOT` distincte à chaque modèle de GPU lorsqu'une même copie de travail est partagée, et utilisez les réglages de résolution et de FPS par GPU documentés.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>
- Utilisez SageAttention uniquement sur RTX 5090 ; laissez-le désactivé sur RTX PRO 6000 et B200. Activez le mode faible VRAM sur les cartes de 48 Go ou moins.
  — <https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md>

## Remplacé par {#superseded-by-this}

- 2026-08-14 — `joyai_video_edit_dit_0804.pth` est remplacé pour le service par `joyai_video_edit_dit_0811.pth` ; ne conservez le premier que pour la reproductibilité.

## Points non résolus {#still-unknown}

- L'URL de la démo originale de JoyAI Labs n'a pas pu être récupérée dans cet environnement de recherche ; sa disponibilité actuelle n'est donc pas vérifiée.
- Le débit annoncé provient d'un benchmark du fournisseur, et non d'un résultat de performance reproduit de manière indépendante.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/jd-opensource/JoyAI-Video-Edit | Dépôt officiel de JoyAI-Video-Edit | 2026-09-05 |
| https://huggingface.co/jdopensource/JoyAI-Video-Edit | Fiche du modèle jdopensource/JoyAI-Video-Edit | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Video-Edit/blob/main/DEPLOYMENT.md | Guide de déploiement de JoyAI-Video-Edit | 2026-09-05 |
| https://arxiv.org/abs/2608.03974 | JoyAI-Video-Edit: Real-Time Open-Ended Video Editing with Autoregressive Diffusion | 2026-09-05 |

## Brief pour agents {#agent-brief}

- **Sujet :** `project:joyai-video-edit`, fil `joyai-video-edit-public-reference`, 1 événement daté du 2026-08-06 au 2026-08-06.
- **Note pratique :** Au 2026-08-06, les praticiens doivent considérer que JoyAI-Video-Edit dispose de références publiques de code, de distribution de modèles et de site officiel, puis vérifier l'état exact de la publication et les consignes d'utilisation auprès de ces sources avant de l'adopter.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
