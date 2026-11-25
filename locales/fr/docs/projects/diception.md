---
title: "DICEPTION"
category: projects
date: 2025-10-02
tags: [diception, diception-development, project]
aliases: ["DICEPTION"]
level: 3
source_sha256: 43b39dda46990491999158dc1ef1b0f854c88a862f1e66186592a09480903152
translation: machine
translated_at: '2026-10-24'
---
# DICEPTION {#diception}

**Ligne de développement :** `project:diception` · fil `diception-development`  
**Dernier événement :** 2025-10-02 · 2 entrées datées depuis 2025-04-21 · **Recherche effectuée le :** 2026-09-04 · confiance : moyenne

## Ce que c'est {#what-it-is}

DICEPTION est un modèle de diffusion basé sur SD3, destiné aux praticiens qui souhaitent disposer d'un seul modèle local pour des sorties de perception visuelle.

- Profondeur monoculaire et normales de surface.
- Estimation de pose.
- Segmentation par entité, sémantique et par points d'invite.

## Ligne de développement {#development-line}

- **2025-04-21 — Les ressources du projet DICEPTION ont été rendues publiques.** Le 2025-04-21, des liens sont apparus pour le site web du projet, son dépôt GitHub et une démo sur Hugging Face Spaces. Ils ont établi un point d'entrée public daté pour le projet, son code source et une démonstration interactive.
- **2025-10-02 — Le dépôt Hugging Face de DICEPTION a été ajouté.** Le 2025-10-02, des liens ont ajouté le dépôt Hugging Face de DICEPTION à la publication initiale du projet. Cela a ajouté un point d'accès distinct au dépôt de modèles à la trace publique datée, sans préciser quels fichiers ont changé ni s'il s'agissait d'une première version.

## Ce qui a changé {#what-changed}

Développement de DICEPTION :

- 2025-02-24/25 — les versions v1/v2 sur arXiv ont établi la méthode généraliste de perception fondée sur la diffusion.
- 2025-04-21 — les points d'entrée publics étaient la page du projet, le dépôt et la démo web. Le code d'inférence utilisable et les poids ne sont arrivés que plus tard, en septembre ; l'installation locale n'était donc pas encore possible.
- 2025-09-19 — accepté comme Spotlight à NeurIPS 2025.
- 2025-09-21 — les mainteneurs ont publié le code d'inférence et le modèle v1.
- 2025-10-02 — des fichiers ont ajouté l'arborescence du modèle Hugging Face avec le point de contrôle DICEPTION_v1.pth.
- 2026-09-04 — la démo hébergée signale RUNTIME_ERROR ; la voie utilisable est donc le code local accompagné des poids.

## Mode d'emploi {#how-to-use-this}

À partir du 2025-10-02, consultez ensemble le site du projet DICEPTION, le dépôt, la démo et le dépôt Hugging Face lorsque vous évaluez le projet.

1. Clonez le dépôt, créez son environnement Conda Python 3.10 et installez les dépendances.
  — <https://github.com/aim-uofa/Diception>
2. Téléchargez Stable Diffusion 3 Medium au format Diffusers ainsi que DICEPTION_v1.pth, puis définissez --pretrained_model_path et --diception_path vers ces répertoires locaux.
  — <https://huggingface.co/Canyu/DICEPTION/tree/main>
3. Exécutez inference.py avec une image d'entrée et un jeton de tâche exact, tel que `[[image2depth]]`, `[[image2normal]]`, `[[image2pose]]`, `[[image2entity]]` ou `[[image2segmentation]]`.
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
4. Pour la segmentation sémantique, ajoutez la catégorie COCO à `[[image2semantic]]` ; pour la segmentation interactive, passez des points y,x normalisés, à raison de cinq points au maximum.
  — <https://github.com/aim-uofa/Diception>
5. Pour les jeux de données, utilisez batch_inference.py avec la structure JSON fournie ; utilisez --save_npy lorsque les valeurs de profondeur ou de normales sont nécessaires plutôt qu'une simple visualisation.
  — <https://github.com/aim-uofa/Diception>

## Bonnes pratiques {#best-practices}

- Préparez un environnement bfloat16 compatible CUDA avant d'exécuter le script publié : celui-ci déplace explicitement le modèle sur CUDA/bfloat16 et charge le point de contrôle sur CUDA.
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
- Commencez avec les 28 étapes d'inférence et l'échelle de guidage 2.0 recommandées par les mainteneurs pour une qualité générale ; n'utilisez 1 étape et un guidage de 1.0 que lorsque la vitesse prime, en particulier pour la profondeur ou les normales.
  — <https://github.com/aim-uofa/Diception>
- Validez au format d'évaluation natif de la tâche : l'inférence sur image unique fonctionne toujours en 768×768 et enregistre une image côte à côte entrée/sortie, et non une prédiction non modifiée à la résolution native.
  — <https://github.com/aim-uofa/Diception/blob/main/inference.py>
- Ne téléchargez le fichier .pth v1 que depuis le dépôt de modèles indiqué et traitez-le comme un artefact pickle PyTorch : le Hub signale les imports pickle et le code utilise torch.load.
  — <https://huggingface.co/Canyu/DICEPTION/tree/main>
- Ne faites pas dépendre un workflow du Space hébergé tant qu'il n'est pas réparé ; utilisez plutôt le code local publié et les poids.
  — <https://huggingface.co/spaces/Canyu/Diception-Demo>
- Pour un usage commercial, suivez l'instruction du projet de contacter le mainteneur indiqué, plutôt que de supposer que la mention d'usage académique couvre le déploiement.
  — <https://github.com/aim-uofa/Diception>

## Remplacé par ceci {#superseded-by-this}

- Accès à la recherche et à la démo uniquement, en date du 2025-04-21 : remplacé le 2025-09-21 par le code d'inférence local publié et les poids v1.
- Accès centré sur la démo, en date du 2025-04-21 : obsolète comme workflow courant depuis le 2026-09-04, car le Space Hugging Face hébergé signale RUNTIME_ERROR.

## Toujours inconnu {#still-unknown}

- Nous ne disposons pas du texte original des publications du 2025-04-21 et du 2025-10-02 ; leur formulation ne peut être reconstituée qu'à partir des liens datés.
- Nous avons trouvé des résumés traduits de sources secondaires, mais aucune documentation opérationnelle chinoise de première main ni de rapport indépendant d'exécution en chinois ; aucun n'a été utilisé comme preuve pratique.
- Nous n'avons trouvé ni exécution locale complète récente, ni mesure de VRAM, ni matrice de matériel supporté. Le code CUDA/bfloat16 constitue une preuve d'implémentation, non un justificatif d'exécution réussie.
- Le README actuel indique encore que le code d'entraînement et de fine-tuning en peu d'exemples est prévu ; le résultat de l'article avec 50 images et une adaptation de 1 % des paramètres ne constitue donc pas un workflow public exécutable.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://aim-uofa.github.io/Diception/ | Page du projet DICEPTION | 2026-09-04 |
| https://github.com/aim-uofa/Diception | README et notes de version de aim-uofa/Diception | 2026-09-04 |
| https://github.com/aim-uofa/Diception/blob/main/inference.py | Script d'inférence sur image unique DICEPTION | 2026-09-04 |
| https://github.com/aim-uofa/Diception/blob/main/models/Renderer.py | Renderer DICEPTION et chemin d'exécution de la diffusion | 2026-09-04 |
| https://huggingface.co/Canyu/DICEPTION/tree/main | Fichiers du modèle Canyu/DICEPTION | 2026-09-04 |
| https://huggingface.co/spaces/Canyu/Diception-Demo | Diception Demo | 2026-09-04 |
| https://arxiv.org/abs/2502.17157 | DICEPTION: A Generalist Diffusion Model for Visual Perceptual Tasks | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:diception`, fil `diception-development`, 2 événements datés du 2025-04-21 au 2025-10-02.
- **Note pratique :** À partir du 2025-10-02, les praticiens doivent consulter ensemble le site du projet DICEPTION, le dépôt source, la démo et le dépôt Hugging Face associé lorsqu'ils évaluent le projet ou recherchent ses artefacts publics.
- **Confiance :** moyenne. Les mentions datées de remplacement ci-dessus font foi pour déterminer ce qui est obsolète.
