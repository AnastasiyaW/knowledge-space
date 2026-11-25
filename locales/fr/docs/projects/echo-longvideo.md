---
title: "Echo LongVideo"
category: projects
date: 2026-06-05
tags: [echo-longvideo, echo-longvideo-public-release, echo_longvideo, project]
aliases: ["Echo LongVideo"]
level: 2
source_sha256: 013b181b2644d3b426639d2f815de4a669c6c527e3a7c82c4eada7a54e81a871
translation: machine
translated_at: '2026-10-24'
---
# Echo LongVideo {#echo-longvideo}

**Ligne de développement :** `project:echo-longvideo` · fil `echo-longvideo-public-release`  
**Dernier événement :** 2026-06-05 · 1 événement daté depuis le 2026-06-05 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Echo LongVideo est le sous-projet vidéo longue de JoyAI-Echo 1.5, destiné à la génération audio et vidéo multi-plans avec transfert d'identité, de voix et de scène entre des plans modifiables.
- R2V avec texte, première image optionnelle et jusqu'à 7 emplacements mémoire audio-visuels ordonnés.
- Génération conjointe audio et vidéo, inférence en BF16/FP8/FP4 et un Director Agent local.
Les poids FP4 occupent 22,81 Go ; le profil 24 GiB exige un conditionnement précalculé.
Il s'agit d'une pile d'inférence locale destinée aux tests, et non d'un service de production établi.

## Ligne de développement {#development-line}

- **2026-06-05 — Les ressources publiques du projet Echo LongVideo ont été rendues accessibles.** Le 2026-06-05, Echo LongVideo était référencé à partir d'une page de projet publique, d'un dépôt GitHub et d'une page de modèle sur Hugging Face. Cet ensemble de ressources daté identifie les emplacements publics de la documentation, du code source et de la distribution des modèles ; les éléments disponibles n'établissent pas le contenu précis de la publication.

## Changements {#what-changed}

2026-06-05 — Hugging Face a reçu une mise à jour du README ; la page du projet décrivait un rapport technique revendiquant des histoires cohérentes de 5 minutes, une mémoire A/V et une accélération de 7,5×, tandis que le code et les poids étaient présentés comme des publications open source futures. 2026-06-22 — Le README racine date la publication de JoyAI-Echo 1.0 et le maintient dans la branche `echo1.0` ; le pipeline d'origine était T2V/multi-plans sans I2V. 2026-08-24 — La version v1 sur arXiv a introduit JoyAI-Echo 1.5 ; la variante vidéo longue ajoutait une mémoire A/V inter-plans composable pour combiner les conditions textuelles, visuelles et mémorielles. 2026-08-27 — Un commit Git a publié la version vidéo longue de JoyAI-Echo 1.5. 2026-08-28 — La documentation a annoncé JoyAI-Echo 1.5 / Echo-LongVideo : code, poids, inférence R2V, profils pour GPU grand public et Director Agent. 2026-08-31 — La documentation a porté la durée revendiquée pour les vidéos longues à plus de 10 minutes ; il s'agit d'une mise à jour de l'affirmation, et non d'une preuve distincte d'un nouveau point de contrôle ou d'un nouveau benchmark.

## Mode d'emploi {#how-to-use-this}

Au 2026-06-05, les praticiens doivent consulter la page de projet, le dépôt source et la page Hugging Face liés à Echo LongVideo pour évaluer le projet ou tenter de l'utiliser, plutôt que de se fier à une description secondaire non vérifiée.

1. Consultez la [LTX-2 Community License](https://github.com/jd-opensource/JoyAI-Echo/blob/main/LICENSE) avant de télécharger ou de déployer : les organisations dont le chiffre d'affaires annuel atteint 10 millions d'US$ doivent obtenir une licence commerciale distincte ; conservez les restrictions de licence lors de toute redistribution.
2. Clonez le dépôt et travaillez uniquement dans `echo_longvideo` ; l'environnement de référence est Python 3.11, PyTorch 2.8, CUDA 12.8, `ffmpeg` dans le PATH, et `scripts/setup_msst.py`, comme détaillé dans le [README](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md).
3. Téléchargez exactement un point de contrôle 1.5 — BF16, FP8 ou FP4 — ainsi que `gemma-3-12b` ; associez-le à la même configuration d'inférence et vérifiez le manifeste et SHA256SUMS sur [Hugging Face](https://huggingface.co/jdopensource/JoyAI-Echo).
4. Construisez la requête R2V avec un prompt texte, une première image optionnelle et jusqu'à sept emplacements mémoire image/audio ordonnés ; exécutez `inference.py` avec la configuration YAML correspondante, décrite dans le [guide](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md).
5. Pour un GPU cible de 24 GiB, utilisez le profil FP4 grand public et précalculez le conditionnement ; la marge réelle dépend du GPU, du pilote et de la forme de la requête, comme documenté dans le [guide](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md).

## Bonnes pratiques {#best-practices}

- Ne mélangez pas les environnements, les répertoires de points de contrôle ni les points d'entrée d'Echo LongVideo avec ceux d'Echo-WM : en amont, ce sont deux projets distincts sur [GitHub](https://github.com/jd-opensource/JoyAI-Echo).
- Vérifiez `checkpoint.json` dans le répertoire des poids ainsi que le fichier `SHA256SUMS` à la racine avant la première exécution d'inférence, sur [Hugging Face](https://huggingface.co/jdopensource/JoyAI-Echo).
- Épinglez le SHA de commit complet pour des installations reproductibles : GitHub ne publie aucun artefact de version sous [releases](https://github.com/jd-opensource/JoyAI-Echo/releases).
- Commencez par le jeu fourni `examples/the_last_visa/requests/`, que la configuration standard prend en charge, avant de soumettre vos propres requêtes R2V, conformément au [README](https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md).

## Ce qui est rendu obsolète {#superseded-by-this}

- 2026-08-28 — l'état « le code et les poids seront publiés ultérieurement » est obsolète : la documentation 1.5 annonce le code, les poids et l'inférence R2V comme publiés.
- 2026-08-28 — pour les installations récentes, l'instruction de la 1.0 « seulement T2V, I2V non pris en charge » est obsolète : la 1.5 utilise R2V avec une première image optionnelle, et la 1.0 reste disponible dans la branche d'archive `echo1.0`.

## Points inconnus {#still-unknown}

- La date officielle de publication de la 1.0 est ambiguë : l'historique Hugging Face montre un commit initial, la licence et des envois le 2026-06-02, une mise à jour du README le 2026-06-05, tandis que le README racine indique une publication le 2026-06-22.
- Il n'existe aucune version GitHub Release versionnée ; le commit de publication de la 1.5 est daté du 2026-08-27, et l'annonce dans le README du 2026-08-28.
- Aucune preuve primaire n'établit une exécution E2E locale réussie, une VRAM/RAM minimale universelle, une vitesse réelle ou une qualité de sortie ; 24 GiB est un profil cible pour GPU grand public, et non une garantie.
- Les termes de la licence nécessitent une revue manuelle : le README indique un usage académique, de recherche et non commercial, tandis que la LTX-2 Community License fournie autorise un usage restreint et exige une licence payante pour les entités commerciales dont le chiffre d'affaires atteint 10 millions d'US$.
- Le dépôt contient également Echo-WM, mais l'amont l'isole comme projet distinct, avec un environnement et une arborescence de points de contrôle différents ; les événements d'Echo-WM sont exclus de cette ligne.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://echo-team-joy-future-academy-jd.github.io/Echo-LongVideo-Page/ | JoyAI-Echo: Pushing the Frontier of Long Audio-Visual Generation | 2026-09-05 |
| https://huggingface.co/jdopensource/JoyAI-Echo/commits/main | Commits · jdopensource/JoyAI-Echo | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo | Dépôt JoyAI-Echo et actualités datées | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/blob/main/echo_longvideo/README.md | JoyAI-Echo/echo_longvideo/README.md at main · jd-opensource/JoyAI-Echo | 2026-09-05 |
| https://huggingface.co/jdopensource/JoyAI-Echo | jdopensource/JoyAI-Echo · Hugging Face | 2026-09-05 |
| https://arxiv.org/abs/2608.23383 | Long-Horizon Audio-Visual Generation for Persistent Stories and Interactive Worlds | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/commits/main/ | Commits · jd-opensource/JoyAI-Echo · GitHub | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/tree/echo1.0 | GitHub - jd-opensource/JoyAI-Echo at echo1.0 | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/blob/main/LICENSE | LTX-2 Community License Agreement | 2026-09-05 |
| https://github.com/jd-opensource/JoyAI-Echo/releases | Releases · jd-opensource/JoyAI-Echo | 2026-09-05 |

## Brief pour agents {#agent-brief}

- **Sujet :** `project:echo-longvideo`, fil `echo-longvideo-public-release`, 1 événement daté du 2026-06-05 au 2026-06-05.
- **Note pratique :** Au 2026-06-05, les praticiens doivent consulter la page de projet, le dépôt source et la page Hugging Face liés à Echo LongVideo pour évaluer le projet ou tenter de l'utiliser, plutôt que de se fier à une description secondaire non vérifiée.
- **Confiance :** moyenne. Les mentions « Ce qui est rendu obsolète » datées font autorité pour déterminer ce qui est obsolète.
