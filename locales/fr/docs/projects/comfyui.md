---
title: "ComfyUI"
category: projects
date: 2026-09-03
tags: [comfy-cloud-pricing, comfyui, comfyui-development, comfyui_core_updates, comfyui_desktop, ecosystem_grants, product_updates, project]
aliases: ["Comfy Cloud", "ComfyUI"]
level: 2
source_sha256: b489a482ac639686aadbd2921c05392c6f891742de39856722272b02691e88db
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI {#comfyui}

**Ligne de développement :** `project:comfyui` · fil `comfyui-development`  
**Dernier événement :** 2026-09-03 · 21 événements datés depuis 2023-11-24 · **Recherche :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

ComfyUI-H3VAE_TRT est une extension tierce pour ComfyUI développée par lihaoyun6. Elle compile les modèles ONNX de VAE MiniMax-H3 en moteurs TensorRT et les charge comme VAE. Il s'agit d'une intégration de nœud personnalisé, et non d'une publication du modèle MiniMax-H3 ni d'une mise à jour du cœur de ComfyUI.

## Ligne de développement {#development-line}

- **2023-11-24 — ComfyUI publie des workflows Stable Video Diffusion.** Le 2023-11-24, ComfyUI a publié des exemples de workflows Stable Video Diffusion officiels pour la génération d'image vers vidéo. Les exemples documentaient le placement des modèles ainsi que les contrôles du nombre d'images, du mouvement, de la fréquence d'images et du guidage sans classifieur.
- **2024-06-12 — Le cœur de ComfyUI ajoute la prise en charge de SD3.** Le 2024-06-12, ComfyUI a ajouté la prise en charge de SD3 à son moteur central dans le commit 8c4a9be. Cette modification a établi la prise en charge native de SD3 dans le moteur pour la construction de workflows SD3.
- **2024-09-16 — ComfyUI ajoute la prise en charge de ControlNet d'inpainting SD3 et Flux.** Le 2024-09-16, ComfyUI a ajouté la prise en charge des modèles ControlNet d'AliMama pour l'inpainting SD3 et Flux dans le commit f48e390. Cette modification a élargi les workflows d'inpainting conditionnés structurellement pour ces familles de modèles.
- **2024-10-21 — ComfyUI V1 introduit une nouvelle interface et une bêta Desktop.** Le 2024-10-21, ComfyUI a présenté son interface V1 et ouvert un empaquetage Desktop en bêta fermée. La version ajoutait un Manager intégré, des onglets, des paramètres, des navigateurs de modèles et de workflows, ainsi qu'une aide au téléchargement de modèles. L'interface d'origine a été basculée vers une voie de maintenance.
- **2024-12-06 — ComfyUI répond à la compromission du paquet Ultralytics.** Le 2024-12-06, ComfyUI a documenté sa réponse aux paquets malveillants Ultralytics 8.3.41 et 8.3.42, rencontrés via certaines chaînes de dépendances de nœuds personnalisés. Le projet a distingué la dépendance compromise du cœur de ComfyUI et ajouté des avertissements dans le Manager ainsi qu'un épinglage des versions.
- **2025-07-28 — ComfyUI ajoute la prise en charge de Wan 2.2 dès le jour zéro.** Le 2025-07-28, ComfyUI a ajouté la prise en charge native de Wan 2.2 dès le jour zéro. La version fournissait des workflows officiels de texte vers vidéo et d'image vers vidéo à mélange d'experts, ainsi que les fichiers de modèles empaquetés.
- **2025-08-13 — ComfyUI élargit les workflows Wan 2.2 Fun InP et Control.** Le 2025-08-13, ComfyUI a ajouté la prise en charge de Wan 2.2 Fun InP, Control et LightX2V. Les workflows permettaient la génération de la première et de la dernière image, des contrôles structurels, ainsi qu'une génération plus rapide en quatre étapes grâce à l'accélération par LoRA.
- **2025-08-26 — ComfyUI ajoute la prise en charge native de ControlNet DiffSynth pour Qwen-Image.** Le 2025-08-26, ComfyUI a ajouté la prise en charge native de ControlNet DiffSynth pour Qwen-Image. La mise à jour a élargi la génération d'images contrôlables et documenté une accélération optionnelle des workflows par cache.
- **2025-08-27 — ComfyUI ajoute des chemins d'exécution Gemini hébergé et Qwen-Image local avec contrôle.** Le 2025-08-27, ComfyUI a ajouté deux chemins d'exécution distincts : Google Gemini 2.5 Flash Image via des Partner Nodes facturés en crédits, et des workflows locaux InstantX Qwen-Image Unified ControlNet. Les workflows locaux prenaient en charge les contrôles canny, profondeur, pose et bords doux.
- **2025-08-28 — Le deuxième Comfy Challenge élargit le programme de workflows communautaires.** Le 2025-08-28, ComfyUI a élargi son programme de vitrine communautaire et d'apprentissage des workflows grâce au deuxième Comfy Challenge. Il s'agissait d'une étape écosystème et pédagogique plutôt que d'une version du moteur d'exécution central.
- **2025-09-24 — ComfyUI ajoute les workflows Wan 2.2 Animate et d'édition d'images Qwen.** Le 2025-09-24, ComfyUI a ajouté des workflows natifs pour Wan 2.2 Animate et Qwen-Image-Edit-2509. Ils prenaient en charge l'animation de personnages pilotée par une performance, ainsi que le remplacement, et l'édition multi-images.
- **2025-10-07 — ComfyUI 0.3.63 rend les sous-graphes publiables.** Le 2025-10-07, ComfyUI 0.3.63 a rendu les sous-graphes publiables en tant que nœuds de blueprint réutilisables. La version a également repensé les outils de sélection pour l'édition de graphes.
- **2025-10-09 — ComfyUI ajoute les Partner Nodes Sora 2.** Le 2025-10-09, ComfyUI a rendu Sora 2 et Sora 2 Pro disponibles via des Partner Nodes payants. L'intégration prenait en charge la génération de texte vers vidéo et d'image vers vidéo avec son.
- **2025-10-22 — ComfyUI 0.3.66 améliore les outils de sous-graphes et de modèles.** Le 2025-10-22, ComfyUI 0.3.66 a ajouté un panneau de paramètres pour les sous-graphes. La version a également repensé la découverte et le filtrage des modèles de workflows.
- **2025-11-26 — Comfy Cloud élargit son infrastructure et ses quotas de fonctionnalités.** Le 2025-11-26, Comfy Cloud a annoncé le passage à une infrastructure RTX 6000 Pro et la prise en charge de l'utilisation de LoRA personnels. Il a aussi décrit des exécutions Pro plus longues et des crédits unifiés couvrant l'exécution GPU Cloud et les Partner Nodes.
- **2025-12-30 — ComfyUI commence à migrer son dépôt canonique vers Comfy-Org.** Le 2025-12-30, ComfyUI a commencé à migrer son dépôt GitHub canonique de comfyanonymous/ComfyUI vers Comfy-Org/ComfyUI. Les redirections GitHub ont été conservées, et les utilisateurs ont été invités à mettre à jour leurs remotes Git.
- **2026-01-27 — ComfyUI ajoute la prise en charge de Z-Image dès le jour zéro.** Le 2026-01-27, ComfyUI a ajouté la prise en charge dès le jour zéro du modèle Z-Image non distillé. La version comprenait un workflow officiel et des recommandations d'échantillonnage propres au modèle.
- **2026-02-05 — L'écosystème ComfyUI annonce une initiative de subventions pour les modèles ouverts.** Le 2026-02-05, l'écosystème ComfyUI a annoncé une initiative de subventions pour les modèles ouverts, présentée comme un programme de 1 million de dollars lancé en parallèle de Anima. L'initiative était présentée comme un financement du développement de modèles ouverts.
- **2026-03-26 — ComfyUI introduit la gestion dynamique stable de la VRAM.** Le 2026-03-26, ComfyUI a documenté Dynamic VRAM comme mécanisme stable de réduction de la pression mémoire et des échecs de mémoire insuffisante sur les systèmes Nvidia pris en charge. Ses recommandations insistaient sur la mesure du temps total du workflow plutôt que de la vitesse d'itération isolée.
- **2026-09-02 — Lancement de l'intégration TensorRT ComfyUI H3VAE.** Le mainteneur a annoncé une version TensorRT du VAE MiniMax-H3 pour ComfyUI, pouvant accroître la vitesse jusqu'à 1,7 fois.
  - L'extension fournit des nœuds Compiler et Loader distincts. La révision source vérifiée est 1b72e7439e1fc306b9dfbfd3d485866553b5960e, validée plus tard le 2 septembre ; l'annonce d'origine n'identifiait pas de tag de version. (2026-09-02) — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>
- **2026-09-03 — Mise à jour de ComfyUI.** Un testeur indépendant a relevé 48,8 s contre 36,6 s pour le même décodage VAE de 2,0 MP et six secondes sur une RTX 4090 de 24 Go, avec ComfyUI 0.34.2 et TensorRT 10.12. À 768p, le résultat était de 19,6 s contre 18,0 s. Il s'agit d'un test de décodage spécifique à une charge de travail, et non d'une affirmation sur la vitesse globale de génération.

## Ce qui a changé {#what-changed}

Le mainteneur indique un traitement VAE MiniMax-H3 jusqu'à 1,7 fois plus rapide dans une intégration tierce pour ComfyUI. Cette affirmation porte sur l'encodage et le décodage VAE, et non sur la génération vidéo de bout en bout. La date d'annonce de la source est conservée séparément des recherches ultérieures.

## Mode d'emploi {#how-to-use-this}

1. Clonez l'extension dans ComfyUI/custom_nodes et installez ses dépendances à l'aide de l'environnement Python qui exécute ComfyUI.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>
2. Téléchargez les fichiers ONNX de l'encodeur et du décodeur depuis le dépôt de modèles lié par le mainteneur, y compris les fichiers .data associés lorsqu'ils sont fournis. Placez-les dans ComfyUI/models/vae.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>
3. Construisez les moteurs avec MiniMax-H3 TRT VAE Compiler, puis chargez-les avec MiniMax-H3 TRT VAE Loader.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md>

## Bonnes pratiques {#best-practices}

- Avec moins de 12 Go de VRAM, le mainteneur suggère le décodeur w4a16_awq. Considérez-le comme une recommandation de l'auteur, et non comme une garantie que le workflow vidéo complet tiendra sur votre GPU.
  — <https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README_zh.md>
- Comparez le même latent à la résolution cible et mesurez le décodage VAE séparément du temps de génération total. Le test indépendant a révélé un gain bien plus faible à 768p qu'à 2,0 MP.
  — <https://note.com/seal309midorin/n/nb75b14bbab4e>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Inconnues {#still-unknown}

- L'annonce d'origine n'identifie ni tag de version immuable ni la version installée.
- L'affirmation maximale de 1,7 fois du mainteneur n'est pas un benchmark indépendant de la génération vidéo complète.
- Un guide communautaire en chinois a été repéré, mais sa page n'a pas pu être récupérée lors de la vérification initiale. La couverture en chinois ici repose sur la documentation de première main ; aucun benchmark indépendant en chinois n'est revendiqué.
- Aucun workflow n'a été exécuté sur notre GPU pour cet article. Les mesures matérielles sont attribuées à leurs auteurs.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README.md | README du mainteneur, en anglais, révision source épinglée | 2026-09-05 |
| https://github.com/lihaoyun6/ComfyUI-H3VAE_TRT/blob/1b72e7439e1fc306b9dfbfd3d485866553b5960e/README_zh.md | README du mainteneur, en chinois simplifié, synthèse traduite en anglais | 2026-09-05 |
| https://note.com/seal309midorin/n/nb75b14bbab4e | Test indépendant japonais de décodage VAE sur RTX 4090, extrait public | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:comfyui`, fil `comfyui-development`, 21 événements datés du 2023-11-24 au 2026-09-03.
- **Remarque pratique :** Voir les sections d'usage et de pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
