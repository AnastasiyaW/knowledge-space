---
title: "MagicMakeup Transfer"
category: projects
date: 2026-07-28
tags: [magicmakeup, magicmakeup-transfer, project]
aliases: ["MagicMakeup Transfer"]
level: 2
source_sha256: 5abe2ac4b1d843ac8bbc1d6d3d0a33fb1d9398fa466f6de43af7b337dee3a233
translation: machine
translated_at: '2026-10-24'
---
# MagicMakeup Transfer {#magicmakeup-transfer}

**Ligne de développement :** `project:magicmakeup` · fil `magicmakeup-transfer`  
**Dernier événement :** 2026-07-28 · 1 événement daté depuis le 2026-07-28 · **Consulté le :** 2026-09-05 · fiabilité : élevée

## Présentation {#what-it-is}

MagicMakeup Transfer est un système de transfert de maquillage image à image, doté d'un contrôle par région, destiné aux utilisateurs de recherche qui préparent des recadrages de visages et des masques.

- Transfert de référence : transfère l'apparence complète du visage, des yeux et des lèvres à partir d'un portrait de référence.
- Point de contrôle du modèle : utilise un point de contrôle MagicMakeup sur FLUX.1-Kontext-dev.
- Résolution de sortie : produit des recadrages de 1024 × 1024 et prend en charge l'inférence sur une paire unique ou en mode lot tous-contre-tous.

## Ligne de développement {#development-line}

- **2026-07-28 — Publication des ressources publiques du projet MagicMakeup Transfer.** Un pipeline de transformeur de diffusion à contrôle par région, avec transfert du visage, des yeux et des lèvres, construit sur FLUX.1-Kontext-dev.

## Ce qui a changé {#what-changed}

2026-07-28 — La publication officielle du code et du point de contrôle est intervenue. MagicMakeup est devenu utilisable comme pipeline de transformeur de diffusion à contrôle par région, avec transfert du visage, des yeux et des lèvres, construit sur FLUX.1-Kontext-dev.

## Mode d'emploi {#how-to-use-this}

Commencez par la page du projet, le dépôt et la ressource de modèle hébergée, telles qu'elles existaient au 2026-07-28. Vérifiez ces documents primaires afin de confirmer les versions exactes et les détails d'utilisation.

1. Clonez le dépôt officiel et créez l'environnement Python 3.10 recommandé avec PyTorch 2.6.0/CUDA 12.4 et les dépendances listées.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
2. Acceptez la licence FLUX.1-Kontext-dev, téléchargez ce modèle de base, puis téléchargez le point de contrôle Anyou/MagicMakeup.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
3. Placez les portraits source et les portraits de référence de maquillage dans des répertoires distincts. Recadrez les visages principaux en images centrées de 1024 × 1024 et conservez le journal de prétraitement.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
4. Générez des masques de visage, d'yeux ou de lèvres correspondants pour les deux images. Exécutez test_single.py avec la valeur --label souhaitée : eyes, lip ou eyes,lip,face.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
5. Vérifiez que les radicaux de noms de fichiers correspondent pour chaque image et chaque masque avant d'exécuter test_dir.py. Le script associe chaque source à chaque référence et ignore les masques non appariés.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>

## Bonnes pratiques {#best-practices}

- Commencez par une paire unique et inspectez le panneau de comparaison avant de lancer un lot tous-contre-tous. Le mode lot ignore les paires en cas de non-correspondance entre recadrages et masques.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
- Utilisez d'abord le mode de déchargement de modèle par défaut. Ne choisissez le déchargement CPU séquentiel que si la mémoire GPU est limitée, car il ralentit l'inférence.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>
- Restez dans le périmètre indiqué, à savoir la recherche académique non commerciale sur les cosmétiques. Ne le détournez pas pour l'échange de visages, la reconnaissance d'identité, l'usurpation d'identité ou les retouches trompeuses.
  — <https://github.com/vivoCameraResearch/Magic-Makeup>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points non élucidés {#still-unknown}

- Nous n'avons trouvé ni version GitHub versionnée ni publication datée du point de contrôle. La date exacte de publication du code et du point de contrôle ne peut donc pas être distinguée de l'événement de publication du 2026-07-28.
- La page Hugging Face expose un exemple Diffusers générique qui omet le pipeline de MagicMakeup conditionné par les masques. Le dépôt officiel reste la voie d'inférence qui fait autorité.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://vivocameraresearch.github.io/magicmakeup/ | MagicMakeup: A Region-Controllable Diffusion Transformer for High-Fidelity Makeup-Transfer | 2026-09-05 |
| https://github.com/vivoCameraResearch/Magic-Makeup | vivoCameraResearch/Magic-Makeup | 2026-09-05 |
| https://huggingface.co/Anyou/MagicMakeup | Fiche modèle Anyou/MagicMakeup | 2026-09-05 |
| https://arxiv.org/abs/2607.20924 | MagicMakeup: A Region-Controllable Diffusion Transformer for High-Fidelity Makeup-Transfer | 2026-09-05 |

## Briefing agent {#agent-brief}

- **Sujet :** `project:magicmakeup`, fil `magicmakeup-transfer`, 1 événement daté, du 2026-07-28 au 2026-07-28.
- **Note pratique :** Commencez par la page du projet, le dépôt et la ressource de modèle hébergée, telles qu'elles existaient au 2026-07-28. Vérifiez les versions exactes et les détails d'utilisation à partir de ces documents primaires.
- **Fiabilité :** élevée. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
