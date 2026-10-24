---
title: "ID-V2V — Ressources publiques du projet"
category: projects
date: 2026-07-30
tags: [id-v2v, project, public-project-resources]
aliases: ["ID-V2V"]
level: 2
source_sha256: 741e2bfe3394c68138389baed6891dc5cde4acaed5eed4649a49bea704c54cb0
translation: machine
translated_at: '2026-10-24'
---
# ID-V2V — Ressources publiques du projet {#id-v2v-public-project-resources}

**Ligne de développement :** `project:id-v2v` · fil `public-project-resources`  
**Dernier événement :** 2026-07-30 · 1 événement daté depuis le 2026-07-30 · **Recherche effectuée le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

ID-V2V est un pipeline de recherche open source, construit sur Wan2.1 I2V-14B-720P et VACE, destiné aux monteurs vidéo. Il transforme une vidéo source, une première image stylisée, des images-clés optionnelles et un prompt textuel en une nouvelle vidéo, tout en préservant l'apparence humaine, l'expression, le regard et le mouvement.

- Le restylage transfère une nouvelle apparence visuelle aux séquences filmées.
- Le relighting ajuste l'éclairage de la scène tout en préservant l'identité.
- La gestion multi-personnages traite plusieurs personnes dans une même scène.
- Les images-clés supplémentaires guident la génération des personnages intermédiaires.
- Le traitement des vidéos longues répartit les séquences longues en plusieurs clips.

La génération s'effectue en 720p, les poids de base et les dépendances occupent environ 96 Go, et le banc d'essai des auteurs utilise 8× A100 80 Go. Il s'agit d'un artefact de recherche lourd, destiné à une inférence locale reproductible, et non d'un service de production.

## Ligne de développement {#development-line}

- **2026-07-30 — Les ressources publiques du projet ID-V2V ont été liées.** Le code officiel définit le répertoire d'entrée, le flux de travail prétraitement-puis-génération et la génération en 720p. Il traite les clips de plus de 81 images à l'aide de fenêtres qui se chevauchent. Il fournit des recettes pour le restylage, le relighting et les images-clés. Une mise à jour de la fiche modèle datée du 2026-07-29 indique que l'architecture de base est Wan 2.1 image-to-video avec contrôle VACE. Les poids ne sont destinés qu'à la démonstration et à l'inspiration.

## Ce qui a changé {#what-changed}

2026-07-24 — L'article arXiv « ID-V2V: Identity-Preserving Video Restylization » a été publié ; il décrit la séparation entre la synthèse guidée par images-clés et la préservation de l'identité ancrée dans la source, via le relighting. 2026-07-29 — Hugging Face a publié deux points de contrôle affinés et incompatibles : le `idv2v.pth` recommandé, avec une condition SAM3 de premier plan sur fond gris, et `idv2v_with_normal_depth.pth`, avec des contrôles supplémentaires de normales et de profondeur. 2026-07-30 — La publication est devenue reproductible en pratique : le code officiel définit un répertoire d'entrée, un flux de travail prétraitement-puis-génération, une génération en 720p, le traitement des clips de plus de 81 images via des clips qui se chevauchent, ainsi que des recettes pour le restylage, le relighting et les images-clés. Une mise à jour de la fiche modèle datée du 2026-07-29 indique que l'architecture de base est Wan 2.1 image-to-video avec contrôle VACE, les poids étant destinés uniquement à la démonstration et à l'inspiration.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-30, les praticiens doivent commencer l'évaluation ou la reproduction d'ID-V2V à partir de la page officielle du projet, du dépôt source et de la page Hugging Face liés, en vérifiant sur ces pages les capacités exactes et l'état de publication avant toute utilisation.

1. Clonez le dépôt, créez un environnement unifié avec `uv sync`, activez-le, puis connectez-vous à Hugging Face dès le départ, car SAM3 nécessite un accès restreint.
  — <https://github.com/Eyeline-Labs/ID-V2V>
2. Téléchargez les points de contrôle standards et les dépendances avec `bash scripts/download_checkpoints.sh` ; ajoutez `--with-depth` pour la variante normales et profondeur.
  — <https://github.com/Eyeline-Labs/ID-V2V>
3. Préparez un répertoire contenant `source.mp4`, `stylized_first_frame.png` et `prompt.txt` ; ajoutez `keyframes/<numéro_d'image>.png` si nécessaire.
  — <https://github.com/Eyeline-Labs/ID-V2V>
4. Pour le modèle standard, lancez le prétraitement avec le prompt textuel SAM3, puis l'inférence ; le relighting emprunte un chemin distinct, sans prétraitement.
  — <https://github.com/Eyeline-Labs/ID-V2V>
5. Pour les séquences source longues, ajoutez des images-clés et utilisez la recette pour vidéos longues : le système raccorde les clips à l'aide d'images de frontière qui se chevauchent.
  — <https://github.com/Eyeline-Labs/ID-V2V>

## Bonnes pratiques {#best-practices}

- Associez chaque point de contrôle au script de sa variante : une architecture correspondante ne déclenche aucune erreur en cas de couple invalide, mais la sortie se dégrade silencieusement.
  — <https://huggingface.co/Eyeline-Labs/ID-V2V>
- Utilisez davantage d'images-clés sur les vidéos longues afin de limiter la dérive entre les clips.
  — <https://github.com/Eyeline-Labs/ID-V2V>
- Considérez les résultats comme expérimentaux, et vérifiez la préservation de l'identité, les expressions faciales et la synchronisation labiale sur vos propres séquences avant toute utilisation en production.
  — <https://huggingface.co/Eyeline-Labs/ID-V2V>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- Le schéma fourni omet `event_findings` et `new_events` ; leurs détails vérifiables figurent dans `what_changed`.
- Les documents officiels décrivent une inférence reproductible, mais ne confirment ni prise en charge en production, ni API publique hébergée, ni exigences minimales en GPU.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://eyeline-labs.github.io/ID-V2V/ | ID-V2V: Identity-preserving Video Restylization | 2026-09-05 |
| https://github.com/Eyeline-Labs/ID-V2V | Eyeline-Labs/ID-V2V | 2026-09-05 |
| https://huggingface.co/Eyeline-Labs/ID-V2V | Eyeline-Labs/ID-V2V | 2026-09-05 |
| https://arxiv.org/abs/2607.22830 | ID-V2V: Identity-Preserving Video Restylization | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:id-v2v`, fil `public-project-resources`, 1 événement daté, du 2026-07-30 au 2026-07-30.
- **Note pratique :** Au 2026-07-30, les praticiens doivent commencer l'évaluation ou la reproduction d'ID-V2V à partir de la page officielle du projet, du dépôt source et de la page Hugging Face liés, en vérifiant sur ces pages les capacités exactes et l'état de publication avant toute utilisation.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
