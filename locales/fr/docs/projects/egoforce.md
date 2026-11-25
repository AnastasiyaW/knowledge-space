---
title: "EgoForce"
category: projects
date: 2026-07-14
tags: [egoforce, egoforce-development, project]
aliases: ["EgoForce"]
level: 2
source_sha256: 9c9c0b83bb8195bd78cff838c25c2e07c7b29b799ffffc774cf81c4e86be5e49
translation: machine
translated_at: '2026-10-24'
---
# EgoForce {#egoforce}

**Ligne de développement :** `project:egoforce` · fil `egoforce-development`  
**Dernier événement :** 2026-07-14 · 1 événement daté depuis le 2026-07-14 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

EgoForce estime la pose 3D absolue de la main et le maillage dans l'espace caméra à partir d'une seule caméra RGB égocentrique.

- Prise en charge des caméras : fonctionne avec les caméras fisheye, à perspective et à grand champ de vision déformé.
- Ressources incluses : poids, jeux de données et une démo Gradio/Project Aria.
- Benchmark : rapporte jusqu'à 28 % de MPJPE dans l'espace caméra en moins sur HOT3D.

Il s'agit de code de recherche destiné à la capture égocentrique calibrée, et non d'un SDK commercial général de suivi de la main.

## Ligne de développement {#development-line}

- **2026-07-14 — Les ressources publiques du projet EgoForce ont été liées.** Le 2026-07-14, la ligne de développement d'EgoForce a relié une page de projet, un dépôt source, une page de modèle Hugging Face et un Space Hugging Face. Ensemble, ces liens datés établissent un point d'entrée public vers les informations du projet, le code, les artefacts de modèle et une interface interactive. Ils ne font aucune affirmation sur une version, des capacités, des benchmarks ou un statut de publication particuliers.

## Ce qui a changé {#what-changed}

- **2026-05-12** — L'article DFKI/MPII a introduit l'approche par espace de rayons guidée par l'avant-bras.
- **2026-07-14** — Le code du projet, les ressources de modèle, le jeu de données et la démo navigateur étaient disponibles simultanément.
- **2026-08-09** — Un rapport ouvert a documenté une défaillance du suivi de la main gauche sur une séquence HOT3D nommée ; aucune correction vérifiée n'a été trouvée.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-14, utilisez la page de projet, le dépôt, la page de modèle et le Space liés comme points de départ pour évaluer ou reproduire EgoForce, tout en vérifiant leur contenu et leurs conditions actuels avant de vous y fier.

1. Créez l'environnement Conda Python 3.10 documenté et exécutez l'installateur du dépôt.
  — <https://github.com/dfki-av/EgoForce/tree/main>
2. Téléchargez les poids du modèle et les ressources requises, puis définissez la racine du jeu de données dans settings.py.
  — <https://github.com/dfki-av/EgoForce/tree/main>
3. Exécutez experiments/save_predictions.py pour un jeu de données pris en charge, puis évaluez le fichier de prédictions enregistré avec les options correspondantes.
  — <https://github.com/dfki-av/EgoForce/tree/main>
4. Pour un test visuel rapide, importez une vidéo dans la démo hébergée ou exécutez localement l'application Gradio du dépôt.
  — <https://huggingface.co/spaces/chris10/EgoForce>

## Bonnes pratiques {#best-practices}

- Considérez-le comme un logiciel de recherche à usage non commercial : le code et les poids sont sous licence CC-BY-NC 4.0, tandis que les ressources WiLoR et MANO incluses ont leurs propres licences.
  — <https://huggingface.co/chris10/EgoForce>
- Validez les paramètres intrinsèques de la caméra et utilisez les options de prédiction/évaluation correspondantes ; les auteurs documentent un balayage du bruit sur les paramètres intrinsèques et des suffixes de sortie propres à chaque variante.
  — <https://github.com/dfki-av/EgoForce/tree/main>
- Testez les deux mains sur les séquences cibles avant de vous fier au système : une défaillance de la main gauche sur HOT3D reste ouverte dans le gestionnaire de tickets public.
  — <https://github.com/dfki-av/EgoForce/issues>

## Remplacé par ceci {#superseded-by-this}

- Aucun élément marqué comme obsolète pour l'instant.

## Toujours inconnu {#still-unknown}

- Un autre article de mai 2026 porte également le nom EgoForce, mais il s'agit d'un projet distinct de reconstruction du mouvement du corps entier fondé sur la diffusion, réalisé par d'autres auteurs ; les URL fournies renvoient au projet DFKI de pose de la main.
- Aucune note de version datée n'a été trouvée pour confirmer de manière indépendante la raison pour laquelle les liens vers le code, le modèle, les données et la démo ont été regroupés le 2026-07-14.
- Le ticket ouvert sur la main gauche dans HOT3D établit une défaillance signalée, et non sa fréquence ni une correction confirmée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://dfki-av.github.io/EgoForce/ | Page du projet EgoForce | 2026-09-05 |
| https://github.com/dfki-av/EgoForce/tree/main | dfki-av/EgoForce, implémentation officielle | 2026-09-05 |
| https://huggingface.co/chris10/EgoForce | Dépôt de modèle chris10/EgoForce | 2026-09-05 |
| https://huggingface.co/spaces/chris10/EgoForce | Démo chris10/EgoForce | 2026-09-05 |
| https://arxiv.org/abs/2605.12498 | EgoForce: Forearm-Guided Camera-Space 3D Hand Pose from a Monocular Egocentric Camera | 2026-09-05 |
| https://github.com/dfki-av/EgoForce/issues | Gestionnaire de tickets d'EgoForce | 2026-09-05 |
| https://arxiv.org/abs/2605.13041 | EgoForce: Robust Online Egocentric Motion Reconstruction via Diffusion Forcing | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:egoforce`, fil `egoforce-development`, 1 événement daté du 2026-07-14 au 2026-07-14.
- **Note pratique :** Au 2026-07-14, les praticiens doivent utiliser la page de projet, le dépôt, la page de modèle et le Space liés comme points de départ pour évaluer ou reproduire EgoForce, tout en vérifiant leur contenu et leurs conditions actuels avant de s'y fier.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
