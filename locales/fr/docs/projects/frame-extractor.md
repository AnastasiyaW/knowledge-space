---
title: "Frame Extractor"
category: projects
date: 2026-08-21
tags: [frame-extractor, project]
aliases: ["Frame Extractor"]
level: 2
source_sha256: 592d77c92e7cc396c41288dc9ed3f8fa398f7c5a42fe12b31be03935d4a9cd47
translation: machine
translated_at: '2026-10-24'
---
# Frame Extractor {#frame-extractor}

**Ligne de développement :** `project:frame-extractor` · fil `frame-extractor`  
**Dernier événement :** 2026-08-21 · 1 événement daté depuis le 2026-08-21 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Frame Extractor — GUI et CLI locaux pour transformer une vidéo en séquence d'images destinée à SfM et Gaussian Splatting. — adapte la densité des images au mouvement de la caméra ; — prend en charge un intervalle fixe, des zones sélectionnées de la timeline et l'export manuel ; — enregistre les JPEG/PNG, le manifeste CSV, les paramètres et le summary à côté des images. La version de test actuelle est v0.2.0-rc.2 ; macOS Apple Silicon reste la plateforme principale testée manuellement. Verdict : pour préparer une prise de vue vidéo à la reconstruction 3D, utilisez le nouveau projet GUI en C++ plutôt que le CLI Python d'origine.

## Ligne de développement {#development-line}

- **2026-08-21 — Dépôt Frame Extractor lié comme référence de développement du projet.** Le 2026-08-21, la ligne de développement de Frame Extractor incluait un lien vers son dépôt GitHub. Cela établit une référence publique datée pour le projet, mais les éléments disponibles n'identifient ni version, ni fonctionnalité, ni modification, ni capacité opérationnelle précise.

## Modifications {#what-changed}

2026-08-15 — le Frame Extractor Python d'origine a bénéficié d'une refonte du pipeline de temporisation, de tests plus stricts, de manifestes d'images horodatés et d'une extraction obligatoire de la dernière image traitée avec succès. 2026-08-21 — Frame Extractor était disponible comme outil Python qui suit une grille régulière de points via le dense optical flow DIS d'OpenCV et sélectionne les keyframes en fonction du décalage cumulé et de la perte de points. 2026-09-05 — le dépôt d'origine a été marqué comme projet dont le développement se poursuit dans Adaptive Frame Extractor : une application multiplateforme en C++20 dotée d'une GUI, d'un CLI, de zones de timeline et de paquets prêts à l'emploi.

## Mode d'emploi {#how-to-use-this}

Depuis le 2026-08-21, les praticiens doivent considérer le dépôt Frame Extractor lié comme la référence datée du projet à examiner avant de s'appuyer sur son workflow ; ses capacités et son statut de version restent non vérifiés.

1. Ouvrez Adaptive Frame Extractor, glissez-déposez la vidéo et sélectionnez le répertoire de résultats.
  — <https://github.com/morishuz/adaptive-frame-extractor>
2. Sélectionnez Low, Medium ou High pour la sélection adaptative, ou fixed interval ; si nécessaire, cochez les zones voulues sur la timeline.
  — <https://github.com/morishuz/adaptive-frame-extractor>
3. Sélectionnez JPEG ou PNG et lancez l'extraction ; utilisez keyframes.csv et summary.txt comme manifeste d'entrée pour COLMAP ou Gaussian Splatting.
  — <https://github.com/morishuz/adaptive-frame-extractor>
4. Pour l'automatisation, lancez le CLI : ./build/release/frame-extractor input.mp4 --output-dir output.
  — <https://github.com/morishuz/adaptive-frame-extractor>

## Bonnes pratiques {#best-practices}

- Pour un mouvement de caméra irrégulier, commencez par le preset adaptive : un intervalle fixe crée des doublons lors des arrêts et peut laisser un recouvrement insuffisant lors d'un mouvement rapide.
  — <https://github.com/morishuz/adaptive-frame-extractor>
- Limitez l'extraction aux zones utiles de la timeline et conservez le manifeste CSV avec les images, afin que la reconstruction puisse être reproduite.
  — <https://github.com/morishuz/adaptive-frame-extractor>
- Dans le CLI legacy, passez explicitement configs/default.yaml pour une exécution reproductible ; les paramètres de DIS, de la grille, de l'estimation du mouvement et des seuils sont regroupés dans un seul YAML.
  — <https://github.com/morishuz/frame-extractor>

## Éléments rendus obsolètes {#superseded-by-this}

- 2026-09-05 — la recommandation d'installer et de faire évoluer le projet Python via uv est obsolète pour les nouveaux utilisateurs : le dépôt lui-même oriente le développement futur vers Adaptive Frame Extractor.
- 2026-09-05 — le lancement exclusivement Python avec configuration de l'environnement a été remplacé par une application GUI multiplateforme prête à l'emploi ; le CLI legacy reste applicable aux scripts existants.

## Points inconnus {#still-unknown}

- Pour la date du 2026-08-21, il n'existe aucune source primaire datée distincte en dehors du lien vers le dépôt d'origine ; c'est pourquoi event_findings est volontairement vide. Les dates de lancement d'Adaptive Frame Extractor et de v0.2.0-rc.2 n'ont pas pu être confirmées via la page GitHub Releases disponible.
- event_findings=[]
- new_events=[{"date":"2026-08-15","source_date":"2026-08-15","summary":"Le projet Python d'origine a bénéficié d'une refonte du timing pipeline, d'une couverture de tests étendue, de manifestes de keyframes horodatés et d'une extraction de la dernière image.","source_url":"https://github.com/morishuz/frame-extractor/commits/main/"},{"date":"2026-09-05","source_date":"2026-09-05","summary":"La documentation actuelle du projet d'origine oriente les nouveaux utilisateurs vers Adaptive Frame Extractor, une GUI et un CLI multiplateformes en C++20 avec traitement local.","source_url":"https://github.com/morishuz/frame-extractor"}]} еицassistant to=developer ? Non. Nous avons donné un JSON invalide ! J'ai involontairement des champs `

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/morishuz/frame-extractor | GitHub — morishuz/frame-extractor | 2026-09-05 |
| https://github.com/morishuz/frame-extractor/commits/main/ | GitHub — historique des commits pour morishuz/frame-extractor | 2026-09-05 |
| https://github.com/morishuz/adaptive-frame-extractor | GitHub — morishuz/adaptive-frame-extractor | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:frame-extractor`, fil `frame-extractor`, 1 événement daté du 2026-08-21 au 2026-08-21.
- **Note pratique :** Depuis le 2026-08-21, les praticiens doivent considérer le dépôt Frame Extractor lié comme la référence datée du projet à examiner avant de s'appuyer sur son workflow ; ses capacités et son statut de version restent non vérifiés.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
