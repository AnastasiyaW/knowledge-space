---
title: "hf-mount"
category: projects
date: 2026-03-25
tags: [hf-mount, hf-mount-development, hf_mount, project]
aliases: ["hf-mount"]
level: 3
source_sha256: 26492c9516cf5a813229c05a16c0d0f5b15ed900a61881d3e3a6d6be2efeab95
translation: machine
translated_at: '2026-10-24'
---
# hf-mount {#hf-mount}

**Ligne de développement :** `project:hf-mount` · fil `hf-mount-development`  
**Dernier événement :** 2026-03-25 · 1 daté depuis le 2026-03-25 · **Recherche :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

hf-mount est un CLI Rust destiné aux développeurs et à l'infrastructure ML pour monter le stockage de Hugging Face sur des systèmes de fichiers locaux.

- Hugging Face Buckets, montés avec accès en écriture via NFS ou FUSE.
- Dépôts de modèles et de jeux de données, montés en lecture seule avec chargement des fichiers au premier accès.

Les dépôts restent en lecture seule, et les modifications distantes se stabilisent en 10 secondes sous FUSE et en 30 secondes sous NFS. Nous l'utilisons pour des tâches ML à forte intensité de lecture sur des disques contraints, mais pas pour des écritures multi-utilisateurs, des verrouillages inter-machines ni des accès aléatoires sensibles à la latence.

## Ligne de développement {#development-line}

- **2026-03-25 — Le dépôt hf-mount de Hugging Face a été référencé publiquement.** Le 2026-03-25, cette ligne de développement a enregistré un lien vers le dépôt GitHub hf-mount de Hugging Face. À partir du seul lien daté, on peut uniquement établir que le projet a été référencé publiquement à cette date ; aucune affirmation de publication, de fonctionnalité ou d'usage n'est étayée.

## Ce qui a changé {#what-changed}

2026-03-25 — hf-mount est devenu capable de monter sur un chemin local les modèles, jeux de données et Storage Buckets du Hub ; les Buckets prennent en charge l'écriture, tandis que les dépôts restent en lecture seule.

Une annonce officielle datée du 2026-03-24 précise l'échelle pour le lancement du 2026-03-25 : les utilisateurs peuvent connecter un stockage distant censé atteindre jusqu'à 100 fois la taille du disque local ; il ne s'agit pas d'une nouvelle version le 25 mars, mais d'une clarification du lancement initial.

Événements récents :
- 2026-06-10 — la v0.7.0 a ajouté le formatage des journaux en JSON et corrigé l'arrêt FUSE/NFS qui bloquait les pods.
- 2026-07-08 — la v0.9.0 a plafonné la durée de lecture des blocs distants, réduit le délai d'expiration de lecture CAS à 30 secondes et transformé link() FUSE en copie côté serveur.
- 2026-08-14 — la v0.9.2 a corrigé les répertoires fantômes lors des correspondances d'arborescence de préfixes bruts, l'encodage URL des chemins et la prise en charge de l'écriture object_store.

## Mode d'emploi {#how-to-use-this}

Au 2026-03-25, les praticiens peuvent utiliser le dépôt GitHub hf-mount comme point de départ pour évaluer le projet, tout en vérifiant ses capacités et sa maturité à partir de la documentation primaire.

1. Installer via Homebrew sur macOS/Linux ou télécharger le binaire pour Linux x86_64/aarch64 ou macOS Apple Silicon.
  — <https://github.com/huggingface/hf-mount>
2. Monter un modèle ou un jeu de données public en chemin lecture seule : `hf-mount start repo openai-community/gpt2 /tmp/gpt2` ; passer `HF_TOKEN` ou `--hf-token` pour une ressource privée.
  — <https://huggingface.co/docs/hub/main/models-downloading>
3. Pour les checkpoints modifiables, journaux et artefacts, monter un Bucket : `hf-mount start --hf-token $HF_TOKEN bucket username/my-bucket /mnt/data`.
  — <https://huggingface.co/docs/hub/storage-buckets-access>
4. Inspecter et arrêter les montages avec `hf-mount status` et `hf-mount stop <mount-path>` ; les journaux se trouvent dans `~/.hf-mount/logs/`.
  — <https://github.com/huggingface/hf-mount>

## Bonnes pratiques {#best-practices}

- Privilégier NFS par défaut : il ne nécessite ni root, ni extension de noyau, ni dépendances FUSE système ; choisir FUSE lorsque l'intégration plus poussée avec le cache noyau et les métadonnées est importante.
  — <https://github.com/huggingface/hf-mount>
- Ne pas utiliser le montage comme système de fichiers distribué : il n'existe pas de verrous inter-clients, les écritures concurrentes ne font l'objet d'aucune détection de conflit, et des vues obsolètes peuvent persister jusqu'à l'intervalle d'interrogation.
  — <https://github.com/huggingface/hf-mount>
- Activer `--advanced-writes` pour l'édition interactive : le mode streaming bloque les sauvegardes typiques des éditeurs (unlink puis création) et perd le tampon en cas de plantage avant `close()`.
  — <https://github.com/huggingface/hf-mount>
- Préférer les montages de volumes gérés pour les HF Jobs et les Spaces, sauf si l'on a besoin d'un montage sur un hôte autonome.
  — <https://huggingface.co/docs/hub/storage-buckets-access>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Inconnues restantes {#still-unknown}

- La balise ou le commit exact correspondant à l'état de hf-mount au 2026-03-25 n'est pas confirmé par les pages primaires disponibles. L'annonce officielle est datée du 2026-03-24 : elle sert donc de source de clarification pour l'événement du 2026-03-25 plutôt que d'événement distinct.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/huggingface/hf-mount | GitHub - huggingface/hf-mount | 2026-09-05 |
| https://huggingface.co/changelog/hf-mount | Introducing hf-mount | 2026-09-05 |
| https://huggingface.co/docs/hub/main/models-downloading | Downloading models | 2026-09-05 |
| https://huggingface.co/docs/hub/storage-buckets-access | Access Patterns | 2026-09-05 |
| https://github.com/huggingface/hf-mount/releases | Releases · huggingface/hf-mount | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:hf-mount`, fil `hf-mount-development`, 1 événement daté du 2026-03-25 au 2026-03-25.
- **Note pratique :** Au 2026-03-25, les praticiens peuvent utiliser le dépôt GitHub hf-mount comme point de départ pour évaluer le projet, tout en vérifiant ses capacités et sa maturité à partir de la documentation primaire.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
