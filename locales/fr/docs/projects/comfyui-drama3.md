---
title: "ComfyUI"
category: "projects"
date: 2026-10-17
tags: ["comfy-cloud-pricing", "comfyui", "comfyui-development", "comfyui-drama3", "comfyui_core_updates", "comfyui_desktop", "ecosystem_grants", "product_updates", "project"]
aliases: ["Comfy Cloud", "ComfyUI"]
level: 3
source_sha256: aa2db946caa6556f70f30ed68983e247ea0ddcda403f4dde9eda6f2dc2a91cf3
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI {#comfyui}

**Ligne de développement :** project:comfyui-drama3 · fil comfyui-development  
**Dernier événement :** 2026-10-17 · 20 événements datés depuis le 2023-11-24 · **Recherche effectuée le :** 2026-10-19 · confiance : élevée

## Ce que c'est {#what-it-is}

ComfyUI-Drama3 est une extension de nœuds personnalisés pour ComfyUI. Elle exécute Drama 3 de Fish Audio, un modèle de synthèse vocale et de clonage de voix de 35 milliards de paramètres, localement sur des GPU grand public.

- Clonage de voix en zero-shot à partir d'un enregistrement de parole propre.
- Dialogues à plusieurs locuteurs, avec jusqu'à 16 voix distinctes dans un même scénario.
- Interprétations émotionnelles pilotées par des balises entre crochets.
- Reconnaissance vocale via des nœuds d'alignement auxiliaires locaux.

Les experts MoE inactifs du routage sont déportés dans la RAM système, tandis que les experts actifs restent en cache sur le GPU. Il faut au minimum 8 Go de VRAM.

## Ligne de développement {#development-line}

- **2023-11-24 — Workflows Stable Video Diffusion.** ComfyUI a publié des workflows d'exemple Stable Video Diffusion de première partie pour la génération image-vers-vidéo. Ils documentaient le placement des modèles ainsi que les contrôles du nombre d'images, du mouvement, de la fréquence d'images et du classifier-free guidance.
- **2024-06-12 — SD3 dans le cœur.** Le commit 8c4a9be a ajouté la prise en charge de SD3 au moteur principal. Les workflows SD3 pouvaient désormais être construits nativement.
- **2024-09-16 — ControlNet d'inpainting SD3 et Flux.** Le commit f48e390 a ajouté la prise en charge des modèles ControlNet d'AliMama pour l'inpainting SD3 et Flux. Cela a élargi l'inpainting à conditionnement structurel pour les deux familles de modèles.
- **2024-10-21 — Interface V1 et bêta Desktop.** ComfyUI a introduit l'interface V1 et ouvert la distribution Desktop en bêta fermée. La V1 intégrait un Manager, des onglets, des paramètres, des navigateurs de modèles et de workflows, ainsi qu'une aide au téléchargement de modèles. L'interface d'origine a été basculée vers une voie de maintenance.
- **2024-12-06 — Compromission du paquet Ultralytics.** Les paquets Ultralytics 8.3.41 et 8.3.42, malveillants, sont apparus dans certaines chaînes de dépendances de nœuds personnalisés. ComfyUI a documenté sa réponse et séparé la dépendance compromise du cœur de ComfyUI. Le Manager a reçu des avertissements et un épinglage de versions.
- **2025-07-28 — Wan 2.2 dès le jour J.** La prise en charge native est arrivée dès le jour J. Elle s'accompagnait de workflows officiels de génération texte-vers-vidéo et image-vers-vidéo en mélange d'experts, ainsi que des fichiers de modèles empaquetés.
- **2025-08-13 — Wan 2.2 Fun InP, Control et LightX2V.** Les workflows ont permis la génération à partir de la première et de la dernière image, des contrôles structurels, ainsi qu'une génération accélérée en quatre étapes grâce à l'accélération par LoRA.
- **2025-08-26 — ControlNet DiffSynth pour Qwen-Image.** La prise en charge native a élargi la génération d'images contrôlable. Une accélération optionnelle des workflows par cache a été documentée.
- **2025-08-27 — Gemini hébergé et contrôle local de Qwen-Image.** Deux voies distinctes ont été ajoutées. Google Gemini 2.5 Flash Image passe par des Partner Nodes facturés en crédits. Les workflows InstantX Qwen-Image Unified ControlNet fonctionnent localement, avec des contrôles canny, profondeur, pose et bords doux.
- **2025-08-28 — Deuxième Comfy Challenge.** Le programme communautaire de présentation et d'apprentissage des workflows a pris de l'ampleur avec le deuxième Comfy Challenge. C'était une étape pour l'écosystème et la formation, et non une version du moteur d'exécution.
- **2025-09-24 — Wan 2.2 Animate et édition d'images Qwen.** Des workflows natifs pour Wan 2.2 Animate et Qwen-Image-Edit-2509 ont été ajoutés. Ils couvrent l'animation de personnages pilotée par une performance, le remplacement, ainsi que l'édition multi-images.
- **2025-10-07 — ComfyUI 0.3.63 : sous-graphes publiables.** Les sous-graphes peuvent être publiés comme nœuds blueprint réutilisables. Les outils de sélection pour l'édition de graphes ont été repensés.
- **2025-10-09 — Partner Nodes Sora 2.** Sora 2 et Sora 2 Pro sont devenus disponibles via des Partner Nodes payants. Ils prennent en charge la génération texte-vers-vidéo et image-vers-vidéo avec son.
- **2025-10-22 — ComfyUI 0.3.66 : outils de sous-graphes et de modèles.** Les sous-graphes disposent désormais d'un panneau de paramètres. La découverte et le filtrage des modèles de workflows ont été repensés.
- **2025-11-26 — Infrastructure et quotas de Comfy Cloud.** Comfy Cloud a annoncé son passage à une infrastructure RTX 6000 Pro et la prise en charge des LoRA personnels. Il a également décrit des sessions Pro plus longues et des crédits unifiés couvrant l'exécution sur GPU cloud et les Partner Nodes.
- **2025-12-30 — Migration du dépôt vers Comfy-Org.** Le dépôt GitHub canonique a commencé à migrer de comfyanonymous/ComfyUI vers Comfy-Org/ComfyUI. Les redirections GitHub ont été conservées, et les utilisateurs ont été invités à mettre à jour leurs remotes Git.
- **2026-01-27 — Z-Image dès le jour J.** ComfyUI a ajouté la prise en charge du modèle Z-Image non distillé. Il est livré avec un workflow officiel et des recommandations d'échantillonnage propres au modèle.
- **2026-02-05 — Initiative de subventions pour les modèles ouverts.** Parallèlement au lancement d'Anima, l'écosystème ComfyUI a annoncé une initiative de subventions présentée comme un programme d'un million de dollars. Elle était présentée comme un financement du développement de modèles ouverts.
- **2026-03-26 — Dynamic VRAM stable.** ComfyUI a documenté Dynamic VRAM comme stable. Il réduit la pression sur la mémoire et les échecs de mémoire insuffisante sur les systèmes Nvidia pris en charge. Les recommandations indiquent de mesurer le temps total du workflow, et non la vitesse d'itération isolée.
- **2026-10-17 — Nœuds ComfyUI-Drama3 plus de 3 fois plus rapides.** Un retour d'utilisateur indiquait que les nœuds ComfyUI-Drama3 mis à jour fonctionnent au moins 3 fois plus vite et tournent avec 8 Go de VRAM. Le retour renvoie vers le dépôt GitHub du projet.
  - La mise à jour optimise la gestion du cache d'experts entre la RAM hôte et le GPU pour l'architecture MoE de Drama 3 de Fish Audio, à 35 milliards de paramètres. La génération est 3 à 4 fois plus rapide, et les GPU grand public de 8 Go de VRAM fonctionnent toujours. (2026-10-17) — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## Ce qui a changé {#what-changed}

Le projet est parti d'une adaptation de l'architecture Drama 3 pour devenir un paquet de nœuds personnalisés ComfyUI optimisé. Il conserve les experts en RAM afin que le modèle mixture-of-experts de 35 milliards de paramètres tourne sur du matériel grand public. Des optimisations ultérieures des noyaux de calcul et des améliorations du cache ont réduit la latence d'inférence de plus de trois fois sur les systèmes à 8 Go.

## Comment l'utiliser {#how-to-use-this}

1. Clonez le dépôt dans le répertoire `custom_nodes` de ComfyUI.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
2. Placez les poids du modèle Drama 3 dans `models/diffusion_models` et les poids du codec dans `models/vae`.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
3. Chargez le workflow d'exemple de clonage de voix ou de synthèse vocale. Attachez un audio de référence pour le clonage de locuteur, ajoutez des balises d'émotion, puis lancez la file d'attente.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## Bonnes pratiques {#best-practices}

- Sur les cartes de 8 Go, déportez les experts routés vers la RAM système et réservez la VRAM du GPU au cache des experts actifs.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
- Utilisez une parole de référence courte et propre, sans bruit de fond, afin que la voix clonée reste fidèle.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>
- Ajoutez des indications entre crochets, comme `[whispers]` ou `[laughs]`, pour façonner le ton dans les scénarios de dialogues à plusieurs locuteurs.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## Ce qu'en disent les praticiens {#what-practitioners-say}

- Les praticiens rapportent un gain notable, de 3 à 4 fois, après la mise à jour des nœuds. Cela rend l'inférence locale d'un modèle de 35 milliards de paramètres praticable sur des cartes de 8 Go. (2026-10-17)
  — <https://www.reddit.com/r/StableDiffusion/comments/1x8dj76/comfyuidrama3_is_34x_faster_now/>

## Remplacé par cette version {#superseded-by-this}

- Les versions précédentes des nœuds mettaient beaucoup plus de temps à s'exécuter sur les GPU à 8 Go de VRAM, car les transferts d'experts de la RAM vers la VRAM n'étaient pas optimisés.
  — <https://github.com/PedroMarinhoDev/ComfyUI-Drama3>

## Points toujours inconnus {#still-unknown}

- Les dates des commits antérieurs à la version d'optimisation du 2026-10-17 n'ont pas été datées de manière indépendante dans les résumés de recherche publics.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/PedroMarinhoDev/ComfyUI-Drama3 | PedroMarinhoDev/ComfyUI-Drama3: ComfyUI custom nodes for Drama 3 | 2026-10-19 |
| https://www.reddit.com/r/StableDiffusion/comments/1x8dj76/comfyuidrama3_is_34x_faster_now/ | ComfyUI-Drama3 is 3-4x faster now : r/StableDiffusion | 2026-10-19 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** project:comfyui-drama3, fil comfyui-development, 20 événements datés du 2023-11-24 au 2026-10-17.
- **Remarque pratique :** voir les sections d'usage et de pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés font autorité quant à ce qui est obsolète.
