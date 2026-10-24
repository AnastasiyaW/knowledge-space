---
title: "OmniAvatar — Publication publique et disponibilité de la démo"
category: projects
date: 2025-08-05
tags: [omniavatar, project, public-release-and-demo]
aliases: ["OmniAvatar"]
level: 2
source_sha256: d44698bbbdc966603d4d735b2a645655759ff7a53cf07f17151f2f40eb75fc17
translation: machine
translated_at: '2026-10-24'
---
# OmniAvatar — Publication publique et disponibilité de la démo {#omniavatar-public-release-and-demo-availability}

**Ligne de développement :** `project:omniavatar` · fil `public-release-and-demo`  
**Dernier événement :** 2025-08-05 · 2 événements datés depuis 2025-07-04 · **Vérifié le :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

OmniAvatar est un système de recherche ouvert de génération de vidéos d'avatars parlants à partir d'une image, d'un audio et d'une invite textuelle.

- Synchronisation labiale sur l'audio de la parole.
- Expressions faciales et mouvements du corps synchronisés sur l'audio.
- Contrôle textuel de l'action du personnage, de l'arrière-plan et de l'émotion.

Les modèles sont des points de contrôle LoRA et de conditionnement audio appliqués à Wan2.1 T2V, en variantes 14B et 1.3B. La résolution de sortie est limitée à 480p. Pour des expérimentations en local, il s'agit d'une pile Wan2.1 fonctionnelle. La Space publique est tierce : nous ne la considérons pas comme la seule voie de lancement.

## Ligne de développement {#development-line}

- **2025-07-04 — Le projet public OmniAvatar et son dépôt source ont été liés.** Le dépôt officiel date la publication de ces poids au 2025-07-02.
- **2025-08-05 — La Space Hugging Face OmniAvatar a été liée.** Le 2025-08-05, une Space Hugging Face nommée OmniAvatar est apparue et renvoie à l'annonce du projet de juillet. Elle ajoute une surface de démonstration hébergée, mais les liens seuls ne permettent pas d'établir ses fonctionnalités exactes, sa disponibilité ni son lien avec une révision précise du dépôt.

## Ce qui a changé {#what-changed}

2025-07-04 — le projet public comprenait le code, les poids et la variante 1.3B pour Wan2.1. Le dépôt officiel date la publication de ces poids au 2025-07-02. 2025-08-05 — la Space Hugging Face tierce alexnasa/OmniAvatar est apparue. Le 2025-08-06, l'équipe d'auteurs d'OmniAvatar a publiquement confirmé que la démo fonctionnait, mais elle n'est pas devenue une API d'inférence officielle. 2025-06-23 — l'article d'OmniAvatar a été publié (arXiv:2506.18866). 2025-06-24 — les auteurs ont publié le code d'inférence et les poids initiaux.

## Comment l'utiliser {#how-to-use-this}

Au 2025-08-05, les praticiens pouvaient trouver OmniAvatar via son dépôt public et la Space Hugging Face liée ; ils doivent vérifier la révision actuelle du dépôt, le comportement de la Space et les instructions d'utilisation avant de s'appuyer sur l'un ou l'autre.

1. Clonez le dépôt et installez les dépendances épinglées : PyTorch 2.4.0 avec CUDA 12.4 et requirements.txt.
  — <https://github.com/Omni-Avatar/OmniAvatar>
2. Téléchargez le Wan2.1 T2V compatible, le point de contrôle officiel LoRA/conditionnement audio d'OmniAvatar et wav2vec2-base-960h dans la structure pretrained_models.
  — <https://huggingface.co/OmniAvatar/OmniAvatar-14B>
3. Préparez la chaîne d'entrée au format [prompt]@@[img_path]@@[audio_path] puis exécutez scripts/inference.py avec la configuration 14B ou 1.3B.
  — <https://github.com/Omni-Avatar/OmniAvatar>
4. Ouvrez la Space pour une brève vérification préliminaire, mais attendez-vous à une disponibilité intermittente et reproduisez localement tout résultat critique.
  — <https://huggingface.co/spaces/alexnasa/OmniAvatar>

## Bonnes pratiques {#best-practices}

- Commencez en 480p avec un CFG prompt/audio compris entre 4 et 6 ; augmentez le CFG audio si la synchronisation labiale n'est pas assez stable.
  — <https://github.com/Omni-Avatar/OmniAvatar>
- Composez l'invite à partir de la description de la première image, du comportement de la personne et, si nécessaire, de l'arrière-plan.
  — <https://github.com/Omni-Avatar/OmniAvatar>
- Anticipez la VRAM pour le 14B : les auteurs indiquent 36 Go sans gestion de la mémoire, 21 Go avec 7B de paramètres persistants et 8 Go sans paramètre persistant, sur un seul GPU.
  — <https://github.com/Omni-Avatar/OmniAvatar>
- N'utilisez pas la Space comme point de terminaison de production : les discussions des utilisateurs signalent des écrans blancs et des problèmes lors du clonage en local ; exécutez le code officiel lorsque la reproductibilité est requise.
  — <https://huggingface.co/spaces/alexnasa/OmniAvatar/discussions/1>

## Remplacé par ceci {#superseded-by-this}

- 2025-06-24 — le statut « article seul » ou « exemples seuls » est obsolète : les auteurs ont publié le code d'inférence et les poids.
- 2025-07-02 — le statut « 14B seul » est obsolète : les auteurs ont publié les poids d'OmniAvatar pour Wan2.1 T2V-1.3B.

## Toujours inconnu {#still-unknown}

- Le schéma de réponse ne contient pas les champs event_findings et new_events ; leurs faits confirmés figurent dans what_changed plutôt que dans des objets structurés distincts.
- Le SLA de la Space et la disponibilité interactive stable restent non confirmés : la page affiche Running on Zero, et des messages d'utilisateurs ultérieurs signalent un écran blanc.
- Le dépôt officiel ne prévoit ni API de production, ni support commercial, ni ensemble complet de configurations GPU vérifiées.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://omni-avatar.github.io/ | OmniAvatar : génération de vidéos d'avatars pilotées par l'audio, efficace et à animation corporelle adaptative | 2026-09-05 |
| https://github.com/Omni-Avatar/OmniAvatar | Omni-Avatar/OmniAvatar | 2026-09-05 |
| https://huggingface.co/OmniAvatar/OmniAvatar-14B | OmniAvatar/OmniAvatar-14B | 2026-09-05 |
| https://huggingface.co/spaces/alexnasa/OmniAvatar | alexnasa/OmniAvatar | 2026-09-05 |
| https://huggingface.co/spaces/alexnasa/OmniAvatar/discussions/1 | Discussion alexnasa/OmniAvatar : Ça marche ? | 2026-09-05 |
| https://huggingface.co/spaces/alexnasa/OmniAvatar/discussions/2 | Discussion alexnasa/OmniAvatar : Ça fonctionne. Démo Space très réussie. | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:omniavatar`, fil `public-release-and-demo`, 2 événements datés du 2025-07-04 au 2025-08-05.
- **Note pratique :** Au 2025-08-05, les praticiens pouvaient trouver OmniAvatar via son dépôt public et la Space Hugging Face liée ; ils doivent vérifier la révision actuelle du dépôt, le comportement de la Space et les instructions d'utilisation avant de s'appuyer sur l'un ou l'autre.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
