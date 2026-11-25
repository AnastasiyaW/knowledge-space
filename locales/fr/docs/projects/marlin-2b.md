---
title: "Marlin-2B"
category: projects
date: 2026-05-21
tags: [marlin-2b, project]
aliases: ["Marlin-2B"]
level: 3
source_sha256: ff1b59db696832ae4132c7f5382909830a48f7d665a5087697bb72879d6c5ea8
translation: machine
translated_at: '2026-10-24'
---
# Marlin-2B {#marlin-2b}

**Ligne de développement :** `project:marlin-2b` · fil `marlin-2b`  
**Dernier événement :** 2026-05-21 · 1 événement daté depuis le 2026-05-21 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

Marlin-2B est un VLM vidéo de 2B paramètres destiné aux développeurs qui ont besoin d'une indexation visuelle horodatée.

- Légender : une description de scène ainsi que des événements bornés dans le temps.
- Rechercher : une requête d'événement en langage naturel renvoie un intervalle début/fin.

Au 2026-09-05, le modèle de base est protégé par une demande d'accès, charge du code personnalisé et ne dispose d'aucun déploiement via Hugging Face Inference Provider. Commencez par des tâches de légendage borné ou de localisation d'événements, puis testez la précision des horodatages sur vos propres séquences vidéo.

## Ligne de développement {#development-line}

- **2026-05-21 — La page du modèle Marlin-2B et le site compagnon du VLM ont été partagés.** Le 2026-05-21, la ligne de développement de Marlin-2B a partagé une page de modèle sur Hugging Face ainsi qu'un site web compagnon du VLM. Nous suivons cette étape parce qu'elle relie le projet à des ressources publiques de modèle et d'utilisation. Les seuls liens datés n'établissent pas la version exacte de publication, les capacités, la licence, ni si l'une de ces ressources est apparue pour la première fois à cette date.

## Ce qui a changé {#what-changed}

- 2026-05-20 — Le projet a annoncé avoir remplacé sa licence BSL 1.1 par Apache-2.0.
- 2026-05-21 — Une demande de prise en charge auprès du fournisseur a confirmé l'identifiant public du modèle, et non un point d'accès hébergé.
- 2026-05-26 — Un billet technique a décrit le modèle et son approche d'évaluation, tandis que les artefacts d'audit restaient non publiés.
- 2026-05-29 — Une réponse du compte de l'organisation a indiqué que MLX/MPS n'était pas encore officiellement pris en charge, et a désigné NVIDIA distant plus Hugging Face Transformers comme configuration de référence.
- 2026-06-24 — La liste de l'organisation a fait apparaître une distribution MLX 8 bits distincte.

## Comment l'utiliser {#how-to-use-this}

Nous pouvons commencer l'évaluation à partir de la page du modèle Hugging Face et du site compagnon du VLM liés, à compter du 2026-05-21, tout en vérifiant la fiche du modèle, les tâches prises en charge, la licence et la version exacte avant de s'y fier.

1. Demandez l'accès au dépôt de base protégé et authentifiez-vous ; les visiteurs anonymes peuvent lister les fichiers mais ne peuvent pas télécharger son contenu protégé.
  — <https://huggingface.co/NemoStation/Marlin-2B/tree/main>
2. Installez la pile documentée : Transformers 5.7 ou ultérieur, PyTorch 2.11 ou ultérieur, TorchCodec, qwen-vl-utils, av et Pillow.
  — <https://huggingface.co/NemoStation/Marlin-2B>
3. Chargez AutoProcessor et AutoModelForCausalLM avec trust_remote_code activé, en BF16 et avec un mapping de périphérique CUDA.
  — <https://huggingface.co/NemoStation/Marlin-2B>
4. Appelez caption(video) pour obtenir une chronologie analysée de scènes et d'événements, ou find(video, event=...) pour obtenir un intervalle temporel analysé.
  — <https://huggingface.co/NemoStation/Marlin-2B>
5. Sur Apple Silicon, utilisez la voie MLX-8bit séparée ; pour le repérage temporel, utilisez un chemin de service sensible aux horodatages plutôt qu'une voie de légendage en une seule passe.
  — <https://huggingface.co/NemoStation/Marlin-2B-MLX-8bit>

## Bonnes pratiques {#best-practices}

- Ne définissez pas le prompt d'aide sauf en cas de raison mesurée de le remplacer. La fiche du modèle indique que le prompt d'entraînement canonique doit presque toujours être conservé.
  — <https://huggingface.co/NemoStation/Marlin-2B>
- Conservez d'abord les paramètres de prétraitement d'entraînement : TorchCodec, 2 FPS, 4 à 240 images et environ 200K pixels par image. La limite par défaut couvre environ deux minutes.
  — <https://huggingface.co/NemoStation/Marlin-2B>
- Considérez span=null ou format_ok=false renvoyés par find() comme un résultat non analysable, et non comme une preuve de l'absence de l'événement.
  — <https://huggingface.co/NemoStation/Marlin-2B>
- Examinez le code personnalisé distant et épinglez un hash de commit examiné avant d'activer trust_remote_code dans un flux de travail de production.
  — <https://huggingface.co/docs/transformers/v4.43.3/custom_models>
- Traitez les résultats de benchmark de légendage dense publiés comme une évaluation du fournisseur. Les auteurs ont indiqué que leur code d'audit, leurs prompts, leurs annotations et le benchmark GRACE restaient des éléments à venir dans le billet du 26 mai.
  — <https://nemostation.com/blog/marlin-2b-the-map-was-wrong>
- Pour le repérage temporel MLX, préservez le temps par image grâce à un chemin de service sensible aux horodatages. La fiche MLX limite la voie en une seule passe au légendage dense.
  — <https://huggingface.co/NemoStation/Marlin-2B-MLX-8bit>

## Remplacé par ceci {#superseded-by-this}

- 2026-05-20 — L'état précédent de la licence BSL 1.1 aurait été remplacé par Apache-2.0.
- 2026-06-24 — La déclaration du 2026-05-29 selon laquelle MLX/MPS manquait de prise en charge officielle est obsolète pour la distribution MLX-8bit listée séparément ; elle ne remplace pas la voie CUDA/Transformers d'origine.

## Toujours inconnu {#still-unknown}

- Aucun instantané immuable de la fiche du modèle, aucun SHA de commit ni aucune trace de publication n'ont été retrouvés pour le 2026-05-21 ; nous ne rattachons donc pas les affirmations actuelles de la fiche du modèle à cette date.
- La date de publication initiale du point de contrôle original reste inconnue. Les preuves primaires établissent une réponse concernant la licence le 20 mai et une demande de prise en charge auprès du fournisseur le 21 mai, mais pas le premier téléversement.
- La disponibilité de la démonstration hébergée reste non vérifiée. L'URL de la démo a répondu, mais n'exposait aucun contrat d'API inspectable ni de reçu d'inférence réussie.
- La distribution MLX est un changement de format de déploiement. Les sources consultées n'établissent pas l'existence d'un nouveau point de contrôle ou d'une nouvelle capacité du cœur Marlin-2B.
- Aucune exigence officielle minimale en VRAM NVIDIA n'a été trouvée.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://huggingface.co/NemoStation/Marlin-2B | NemoStation/Marlin-2B · Hugging Face | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B/tree/main | NemoStation/Marlin-2B at main | 2026-09-05 |
| https://huggingface.co/spaces/huggingface/InferenceSupport/discussions/10010 | huggingface/InferenceSupport · NemoStation/Marlin-2B | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B/discussions/1 | NemoStation/Marlin-2B · 👉 Marlin-2B model? "Open Source" -- my ass! | 2026-09-05 |
| https://nemostation.com/blog/marlin-2b-the-map-was-wrong | Part 1: The Map Was Wrong — Nemostation | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B/discussions/9 | NemoStation/Marlin-2B · use marlin on a remote GPU machine ? third party providers ? | 2026-09-05 |
| https://huggingface.co/NemoStation/models | NemoStation (Nemo Station) | 2026-09-05 |
| https://huggingface.co/NemoStation/Marlin-2B-MLX-8bit | NemoStation/Marlin-2B-MLX-8bit · Hugging Face | 2026-09-05 |
| https://huggingface.co/docs/transformers/v4.43.3/custom_models | Building custom models · Hugging Face | 2026-09-05 |
| https://vlm.nemostation.com | vlm.nemostation.com | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:marlin-2b`, fil `marlin-2b`, 1 événement daté du 2026-05-21 au 2026-05-21.
- **Note pratique :** Nous pouvons commencer l'évaluation à partir de la page du modèle Hugging Face et du site compagnon du VLM liés, à compter du 2026-05-21, tout en vérifiant la fiche du modèle, les tâches prises en charge, la licence et la version exacte avant de s'y fier.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
