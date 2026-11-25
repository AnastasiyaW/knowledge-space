---
title: "Moebius — Disponibilité publique"
category: projects
date: 2026-06-20
tags: [moebius, project, public-availability]
aliases: ["Moebius"]
level: 2
source_sha256: 89dfa8260f92c0d93775e5579ec444d6cfca943fd653b19f2c44943a7e72298d
translation: machine
translated_at: '2026-10-24'
---
# Moebius — Disponibilité publique {#moebius-public-availability}

**Ligne de développement :** `project:moebius` · fil `public-availability`  
**Dernier événement :** 2026-06-20 · 1 événement daté depuis le 2026-06-20 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Moebius est un framework open source de complétion d'image (inpainting) destiné aux développeurs qui fournissent une image et un masque correspondant.
- Points de contrôle pré-entraînés, Places2, CelebA-HQ et FFHQ pour des complétions spécifiques à un domaine.
- Chemin d'inférence via le dépôt pour les exécutions locales scriptées.
- Chemin de chargement via Hugging Face Diffusers pour l'intégration dans des pipelines.

Il fonctionne avec 226 M de paramètres, à raison de 26,01 ms par étape sur le GPU de test des auteurs. C'est un spécialiste des complétions masquées et de la suppression d'objets, et non un service de génération généraliste hébergé.

## Ligne de développement {#development-line}

- **2026-06-20 — Les ressources du projet Moebius ont été partagées publiquement.** Le 2026-06-20, un message concernant Moebius renvoyait vers le site du projet, son dépôt GitHub et sa page Hugging Face. Nous considérons ceci comme une étape importante de disponibilité publique, car elle oriente les lecteurs vers les ressources publiques du projet, alors que la version exacte publiée ou les capacités précises ne peuvent pas être établies à partir des seuls liens fournis.

## Ce qui a changé {#what-changed}

2026-06-20 — Moebius était disponible sous forme de page de projet, de dépôt public et de modèle Hugging Face ; les documents de première main le présentent comme un spécialiste de complétion d'image de 0,22 B de paramètres.

Constat d'événement pour le 2026-06-20 — l'annonce du dépôt du 18 juin 2026 indique que le périmètre comprenait le code d'entraînement, le code d'inférence et les poids publics, avec des points de contrôle pour les variantes pré-entraînée, Places2, CelebA-HQ et FFHQ ; il ne s'agissait pas d'une version GitHub empaquetée.

Nouveaux événements : 2026-06-16 — le dépôt a été publié pour la première fois, selon ses actualités datées du projet. 2026-06-17 — la version v1 sur arXiv (2606.19195) a été soumise, documentant le backbone LλMI et la distillation multi-granularité dans l'espace latent. 2026-06-18 — les auteurs ont annoncé l'acceptation à ECCV 2026 et publié la prépublication, le code et les poids. 2026-06-19 — le projet a signalé l'atteinte de la première place du classement quotidien de Hugging Face ; il s'agit d'un indice de visibilité, et non d'une révision du modèle. 2026-06-25 — le projet a signalé un classement hebdomadaire de 4/105 sur Hugging Face ; il s'agit d'un indice de visibilité, et non d'une révision du modèle.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-20, les praticiens doivent consulter les pages du projet, du code et de Hugging Face de Moebius comme point de départ pour l'évaluation ; ces seuls éléments ne permettent pas d'établir une version, une capacité, une licence ou une recommandation de déploiement précises.

1. Clonez le dépôt, créez l'environnement documenté et installez ses dépendances épinglées avant d'utiliser le flux de travail du dépôt.
  — <https://github.com/hustvl/Moebius>
2. Téléchargez le VAE ainsi que le point de contrôle pré-entraîné ou spécifique à la tâche, en conservant l'arborescence de répertoires de poids documentée.
  — <https://github.com/hustvl/Moebius>
3. Placez chaque image source et son masque dans des répertoires distincts avec des noms de fichiers correspondants, puis exécutez infer.infer_moebius avec la configuration de modèle choisie, le point de contrôle, les répertoires d'entrée, le répertoire de sortie, la valeur CFG, la taille de lot et le nombre de workers.
  — <https://github.com/hustvl/Moebius>
4. Pour le chemin via le Hub, installez diffusers, transformers et accelerate, puis chargez hustvl/Moebius via DiffusionPipeline ; validez ses sorties par rapport au chemin du dépôt avant de l'adopter pour l'édition masquée.
  — <https://huggingface.co/hustvl/Moebius>

## Bonnes pratiques {#best-practices}

- Utilisez le chemin d'inférence image-et-masque du dépôt pour la complétion d'image ; son arborescence de fichiers et sa commande encodent explicitement le flux de travail fondé sur le masque.
  — <https://github.com/hustvl/Moebius>
- Choisissez un point de contrôle aligné sur le domaine de l'image — Places2 pour les scènes naturelles, CelebA-HQ ou FFHQ pour les portraits — et ne considérez pas les résultats de benchmark comme une preuve pour un domaine sans rapport.
  — <https://hustvl.github.io/Moebius/>
- Épinglez les versions de Torch, Diffusers, Transformers et flash-linear-attention listées par le dépôt lorsque vous reproduisez son flux de travail ; la page Hub présente un exemple Diffusers générique distinct.
  — <https://github.com/hustvl/Moebius>
- Considérez les 26,01 ms par étape et l'accélération supérieure à 15x annoncées comme des résultats de benchmark des auteurs, et non comme une garantie de latence en déploiement.
  — <https://arxiv.org/abs/2606.19195>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-18 — la consigne selon laquelle Moebius n'était qu'un article ou une page de projet est obsolète : les documents de première main indiquent que le code et les poids ont été publiés.
- 2026-09-05 — la consigne d'installer un artefact de version GitHub n'est pas étayée : la page des versions du dépôt n'affiche aucune version. Utilisez plutôt un clone des sources et les points de contrôle du Hub.

## Points encore inconnus {#still-unknown}

- La page Hugging Face indique une licence MIT pour le modèle, tandis que le README du dépôt indique Apache-2.0 pour le code et les poids pré-entraînés. Confirmez la licence prévue auprès des mainteneurs avant tout déploiement commercial.
- Le schéma fourni ne comporte pas de champs event_findings ni new_events ; leur contenu requis est conservé dans what_changed.
- Aucune reproduction matérielle indépendante n'a été trouvée pour l'affirmation de 26,01 ms par étape ou d'accélération supérieure à 15x.
- L'exemple Diffusers générique de Hugging Face semble ne prendre qu'un prompt, alors que le dépôt documente la complétion image-et-masque ; l'interface exacte de masquage du pipeline du Hub n'a pas été vérifiée indépendamment.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://hustvl.github.io/Moebius/ | Moebius Project Page | 2026-09-05 |
| https://github.com/hustvl/Moebius | hustvl/Moebius repository | 2026-09-05 |
| https://huggingface.co/hustvl/Moebius | hustvl/Moebius model card | 2026-09-05 |
| https://arxiv.org/abs/2606.19195 | Moebius: 0.2B Lightweight Image Inpainting Framework with 10B-Level Performance | 2026-09-05 |
| https://github.com/hustvl/Moebius/releases | Moebius GitHub releases | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:moebius`, fil `public-availability`, 1 événement daté du 2026-06-20 au 2026-06-20.
- **Note pratique :** Au 2026-06-20, les praticiens doivent consulter les pages du projet, du code et de Hugging Face de Moebius comme point de départ pour l'évaluation ; ces seuls éléments ne permettent pas d'établir une version, une capacité, une licence ou une recommandation de déploiement précises.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
