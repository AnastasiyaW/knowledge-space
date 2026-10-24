---
title: "CameraCtrl"
category: projects
date: 2024-05-29
tags: [cameractrl, cameractrl-development, project]
aliases: ["CameraCtrl"]
level: 3
source_sha256: 9cddf8b85147979fffdcbfd74ca06f4babee9fb9d546c30da84c3cf51b8b6649
translation: machine
translated_at: '2026-10-24'
---
# CameraCtrl {#cameractrl}

**Ligne de développement :** `project:cameractrl` · fil `cameractrl-development`  
**Dernier événement :** 2024-05-29 · 2 événements datés depuis 2024-04-10 · **Recherche :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

CameraCtrl est une base de code de recherche pour la génération de vidéos avec un mouvement de caméra prescrit dans AnimateDiffV3 et Stable Video Diffusion.

- Conditionnement par pose de caméra : guide la génération vidéo le long d'une trajectoire de caméra exacte.
- Conception modulaire : sépare le modèle de diffusion de base des poids de contrôle de caméra.
- Implémentations pour différents backends : fournit AnimateDiffV3 sur `main` et l'image-vers-vidéo SVD sur `svd`.

## Ligne de développement {#development-line}

- **2024-04-10 — La page du projet CameraCtrl et le dépôt source ont été liés.** Le 2024-04-10, des liens publics pointaient vers la page du projet CameraCtrl et le dépôt GitHub. Ces liens indiquent une disponibilité publique, mais ne précisent ni version de publication ni contenu des publications.
- **2024-05-29 — Un Space Hugging Face CameraCtrl-svd a été lié.** Le 2024-05-29, un suivi public a relié le Space Hugging Face CameraCtrl-svd et référencé la publication CameraCtrl antérieure. Cela montre une étape de démonstration, mais les liens seuls ne confirment ni le fonctionnement, ni la version du modèle, ni l'état en ligne à cette date.

## Évolutions {#what-changed}

2024-04-10 — CameraCtrl est apparu sur sa page de projet et sur le dépôt public. Les notes de version datent la publication du code et des points de contrôle AnimateDiffV3 au 2024-04-03.
2024-05-29 — Le chemin Stable Video Diffusion est apparu via la démo SVD-xt. Les notes du mainteneur datent le code, les modèles pré-entraînés et la démo Gradio au 2024-05-24. Cela a ajouté une implémentation SVD image-vers-vidéo distincte.
2025-03-13 [trouvé aujourd'hui] — CameraCtrl II a été soumis pour étendre la recherche vers l'exploration itérative de scènes dynamiques.
2026-09-04 [trouvé aujourd'hui] — Le dépôt d'origine assigne toujours AnimateDiffV3 à `main` et SVD à `svd`. Le Space public CameraCtrl-svd affiche un échec d'import de dépendance.

## Comment l'utiliser {#how-to-use-this}

Nous disposions de liens publics vers le projet et le code source le 2024-04-10. Le Space Hugging Face CameraCtrl-svd a suivi le 2024-05-29 pour les tests. Les seules preuves par liens ne justifient aucune affirmation opérationnelle au-delà de ces emplacements.

1. Choisissez d'abord le backend : utilisez `main` pour AnimateDiffV3, et récupérez `svd` uniquement pour l'image-vers-vidéo Stable Video Diffusion.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
2. Pour le chemin AnimateDiffV3, créez l'environnement Python 3.10/CUDA 11.7 documenté et activez `cameractrl`.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
3. Téléchargez SD1.5, l'adaptateur AnimateDiffV3, les points de contrôle du module de mouvement et le point de contrôle CameraCtrl. Fusionnez l'adaptateur ADV3 dans l'UNet de SD1.5 avant l'inférence.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
4. Préparez un fichier texte de trajectoire et un JSON de prompts à partir des ressources fournies, puis visualisez la trajectoire avant l'échantillonnage.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
5. Exécutez la recette `inference.py` documentée en fournissant les chemins du modèle de base, du module de mouvement, du point de contrôle CameraCtrl, des prompts, de la trajectoire et de la sortie. Le lancement de référence utilise huit processus.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
6. Pour SVD, utilisez l'environnement `svd`, un point de contrôle SVD ou SVD-xt compatible, les images de conditionnement, le JSON de prompts et la trajectoire. Les nombres d'images documentés sont 14 pour SVD et 25 pour SVD-xt.
  — <https://github.com/hehao13/CameraCtrl/blob/svd/README.md>

## Bonnes pratiques {#best-practices}

- Gardez `main` et `svd` séparés : ils ciblent des backends, des environnements et des modes d'entrée différents, n'mélangez donc pas leurs instructions d'installation ni leurs points de contrôle.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
- Traitez la trajectoire de caméra comme une entrée de premier plan : commencez par les fichiers de pose fournis, visualisez le chemin, et gardez les prompts et les graines fixes lorsque vous comparez des trajectoires.
  — <https://github.com/hehao13/CameraCtrl/blob/main/README.md>
- Utilisez le jeu de ressources correspondant : main nécessite SD1.5 plus les poids ADV3 fusionnés et CameraCtrl, tandis que `svd` nécessite SVD/SVD-xt plus son point de contrôle CameraCtrl correspondant.
  — <https://github.com/hehao13/CameraCtrl/blob/svd/README.md>
- Reproduisez avec l'environnement épinglé par le projet avant de mettre à jour les bibliothèques. L'environnement main épingle Python 3.10, PyTorch 1.13.1, CUDA 11.7, diffusers 0.24.0 et xformers 0.0.16.
  — <https://github.com/hehao13/CameraCtrl/blob/main/environment.yaml>
- Exécutez SVD en local plutôt que de dépendre du Space public tant qu'il n'est pas réparé : l'erreur du Space est un échec d'import de `cached_download`.
  — <https://huggingface.co/spaces/hehao13/CameraCtrl-svd>

## Remplacé par ce qui suit {#superseded-by-this}

- Consignes d'installation main uniquement du 2024-04-10 — remplacées pour les utilisateurs de SVD par la version `svd` du 2024-05-24. Il s'agit d'une implémentation image-vers-vidéo distincte, et non d'une mise à niveau de `main`.
- Flux de démonstration hébergée du 2024-05-29 — remplacé depuis le 2026-09-04 par l'échec d'exécution observé de CameraCtrl-svd. Exécutez le chemin `svd` local pour reproduire les résultats.

## Inconnues {#still-unknown}

- La page d'erreur de CameraCtrl-svd provient d'un crawl daté de deux semaines. Une vérification interactive récente n'était pas disponible ; vérifiez donc l'état d'exécution avant de vous y fier.
- CameraCtrl II est un projet de recherche ultérieur sans guide de migration officiel, sans version compatible ni affirmation de remplacement direct. Nous ne le considérons pas comme un remplaçant du dépôt 2024.
- La page de l'auteur mentionne CameraCtrl II++, mais les tests n'ont pas permis de vérifier une version utilisable ni la compatibilité avec le flux de travail CameraCtrl d'origine.
- Aucune recette de référence officielle pour un seul GPU n'existe. Les deux exemples d'inférence documentés utilisent huit processus.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://hehao13.github.io/projects-CameraCtrl/ | CameraCtrl: Enabling Camera Control for Video Diffusion Models | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl | hehao13/CameraCtrl | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl/blob/main/README.md | CameraCtrl README — branche main | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl/blob/main/environment.yaml | CameraCtrl environment.yaml — branche main | 2026-09-04 |
| https://github.com/hehao13/CameraCtrl/blob/svd/README.md | CameraCtrl README — branche svd | 2026-09-04 |
| https://huggingface.co/spaces/hehao13/CameraCtrl-svd | CameraCtrl Svd Xt — Space Hugging Face | 2026-09-04 |
| https://arxiv.org/abs/2404.02101 | CameraCtrl: Enabling Camera Control for Text-to-Video Generation | 2026-09-04 |
| https://arxiv.org/abs/2503.10592 | CameraCtrl II: Dynamic Scene Exploration via Camera-controlled Video Diffusion Models | 2026-09-04 |
| https://hehao13.github.io/ | Hao He — projects | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:cameractrl`, fil `cameractrl-development`, 2 événements datés du 2024-04-10 au 2024-05-29.
- **Note pratique :** Les liens publics vers le projet et le code source étaient accessibles au 2024-04-10. Le Space Hugging Face CameraCtrl-svd était disponible au 2024-05-29 pour évaluation. Les seules preuves par liens ne justifient aucune affirmation opérationnelle au-delà de ces emplacements.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
