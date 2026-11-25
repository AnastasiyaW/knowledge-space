---
title: "ExAvatar"
category: projects
date: 2024-09-26
tags: [exavatar, exavatar-development, project]
aliases: ["ExAvatar"]
level: 3
source_sha256: 240e0e756c9d7eee2296d025c679d5cea8769177ba81658b26007e521ee47891
translation: machine
translated_at: '2026-10-24'
---
# ExAvatar {#exavatar}

**Ligne de développement :** `project:exavatar` · fil `exavatar-development`  
**Dernier événement :** 2024-09-26 · 2 entrées datées depuis 2024-08-01 · **Recherche :** 2026-09-04 · confiance : moyenne

## Description {#what-it-is}

ExAvatar est un pipeline de recherche destiné aux praticiens de la synthèse graphique et des avatars qui ont besoin de contrôler le corps, les mains et les expressions faciales à partir d'une seule vidéo monoculaire tournée avec un téléphone, au lieu de l'entrée par scan 3D ou RGB-D utilisée par X-Avatar.

- Ajustement SMPL-X et FLAME : ajustement sur la capture.
- Avatar 3D Gaussian : entraînement à partir de la capture ajustée.
- Synthèse de vues : rendu de nouvelles poses du corps et des mains, d'expressions faciales et de points de vue.

Le projet démontre un scan téléphone d'environ 10 secondes en pose neutre. Les intérieurs de bouche non visibles, les surfaces de paume et les vêtements dynamiques peuvent échouer. Nous l'utilisons pour la recherche contrôlée et hors ligne sur les avatars lorsque la pile d'ajustement SMPL-X est acceptable. Nous ne l'utilisons pas lorsque la déformation des vêtements ou une anatomie non visible doit être fiable.

## Ligne de développement {#development-line}

- **2024-08-01 — Partage du site web du projet ExAvatar.** Le 2024-08-01, ExAvatar a été partagé via son site web de projet comme référence publique.
- **2024-09-26 — Partage du dépôt de publication d'ExAvatar.** Le 2024-09-26, ExAvatar a publié un dépôt GitHub dédié aux publications, afin de fournir une source orientée publication en complément du site web initial du projet.

## Changements {#what-changed}

2024-08-01 — ExAvatar est apparu comme une méthode présentée à ECCV 2024, combinant SMPL-X et le 3D Gaussian Splatting pour créer un avatar contrôlable du corps, des mains et du visage à partir d'un scan téléphone court.

2024-09-26 — ExAvatar_RELEASE a rendu disponible la réimplémentation PyTorch officielle, avec des ressources publiques et des chemins documentés pour l'ajustement, l'entraînement, les tests et l'animation.

2026-09-04 — Le dépôt officiel et la documentation restent publics, mais GitHub ne liste aucune version empaquetée ni aucune note de version. Une utilisation reproductible doit enregistrer le commit retenu.

## Mode d'emploi {#how-to-use-this}

À la date du 2024-09-26, consultez le dépôt de publication d'ExAvatar pour les ressources orientées publication, plutôt que de vous fier uniquement au site web du projet partagé le 2024-08-01.

1. Créez l'environnement Conda dans une copie de ExAvatar_RELEASE : `conda env create -f environment.yml`, puis `conda activate exavatar`.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/README.md>
2. Installez les prérequis d'ajustement : SMPL-X 1.1, FLAME, DECA, Hand4Whole, MMPose, Segment Anything, Depth Anything V2 et COLMAP ; exécutez les personnalisations `copy_code.py` du dépôt.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
3. Placez la vidéo d'une personne à `data/Custom/data/$SUBJECT_ID/video.mp4`, extrayez les images, créez les listes de trames all/train/test, définissez `dataset = 'Custom'`, puis ajustez SMPL-X avec le mode caméra documenté.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
4. Générez les masques de premier plan, créez un nuage de points d'arrière-plan uniquement pour un arrière-plan statique, entraînez avec `main/train.py` et inspectez la sortie de reconstruction avec `test.py`.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>
5. Pour un avatar exporté sous `output/model_dump/$SUBJECT_ID`, fournissez les paramètres SMPL-X de pilotage et exécutez `animation.py` ; utilisez `animate_view_rot.py` pour un rendu avec caméra en rotation.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>

## Bonnes pratiques {#best-practices}

- Capturez en extérieur ou évitez autrement les éclairages forts et les ombres dures ; choisissez en conséquence le chemin de prétraitement à arrière-plan statique ou dynamique.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>
- Utilisez des trames d'ajustement où la majeure partie de la personne est visible et non tronquée ; un échantillonnage d'environ 5 ips à partir de 30 ips constitue le point de départ documenté, orienté vitesse.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
- Utilisez COLMAP pour une caméra en mouvement ; utilisez le chemin de caméra virtuelle pour une capture statique ou l'extraction des paramètres SMPL-X.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
- Si l'ajustement du visage se dégrade, inspectez `flame_init/renders` et vérifiez que les résultats DECA ont été préparés avant de relancer le pipeline.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md>
- Conservez identiques entre l'entraînement et l'évaluation les paramètres d'identité SMPL-X de forme, de décalage articulaire et de décalage facial.
  — <https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md>

## Remplacé par {#superseded-by-this}

- 2024-09-26 — Pour l'implémentation, le dépôt public ExAvatar_RELEASE et ses READMEs d'ajustement et d'avatar remplacent les indications de pré-version ou celles limitées à la page du projet.

## Points inconnus {#still-unknown}

- Le dépôt ne possède aucun paquet de publication GitHub, et les sources examinées ne fournissent ni cible actuelle de VRAM, ni durée d'entraînement attendue, ni matrice CUDA/pilote prise en charge.
- Aucune source de première main examinée ne déclare ExAvatar obsolète ni ne désigne un successeur officiel.
- Aucun rapport d'exploitation reproductible en langue chinoise ni aucune recette matérielle communautaire indépendante n'a été vérifié ; les pratiques listées sont des recommandations des mainteneurs.
- Le permalien de la source du 2024-09-26 n'a pas pu être récupéré et n'a pas été utilisé comme preuve.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://mks0601.github.io/ExAvatar/ | Page du projet ExAvatar | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE | Dépôt officiel ExAvatar_RELEASE | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/blob/main/README.md | README de ExAvatar_RELEASE | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/blob/main/fitting/README.md | Ajustement de SMPL-X à partir d'une vidéo monoculaire | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/blob/main/avatar/README.md | Création d'un avatar à partir d'un scan téléphone | 2026-09-04 |
| https://github.com/mks0601/ExAvatar_RELEASE/releases | Versions GitHub de ExAvatar_RELEASE | 2026-09-04 |
| https://arxiv.org/abs/2407.21686 | Expressive Whole-Body 3D Gaussian Avatar | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:exavatar`, fil `exavatar-development`, 2 événements datés du 2024-08-01 au 2024-09-26.
- **Note pratique :** À la date du 2024-09-26, les praticiens doivent consulter le dépôt de publication d'ExAvatar pour les ressources orientées publication, plutôt que de se fier uniquement au site web du projet partagé le 2024-08-01.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
