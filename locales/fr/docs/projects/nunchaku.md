---
title: "Nunchaku — Extension de l'intégration de modèles"
category: projects
date: 2026-01-23
tags: [model-integration-expansion, nunchaku, project]
aliases: ["Nunchaku"]
level: 3
source_sha256: 318b3f1f35208adc5ddc1eed09bf5a8121bd04e80cb1a16013c770b250f9c593
translation: machine
translated_at: '2026-10-24'
---
# Nunchaku — Extension de l'intégration de modèles {#nunchaku-model-integration-expansion}

**Ligne de développement :** `project:nunchaku` · fil `model-integration-expansion`  
**Dernier événement :** 2026-01-23 · 3 événements datés depuis 2025-08-03 · **Consulté le :** 2026-09-04 · confiance : élevée

## Présentation {#what-it-is}

Nunchaku est un moteur d'inférence 4 bits SVDQuant destiné aux utilisateurs de Diffusers et ComfyUI qui ont besoin de transformeurs FLUX ou Qwen Image en précision réduite, plutôt que d'un autre modèle de base.

- Poids des transformeurs : charge des poids SVDQuant INT4 ou FP4 via des classes compatibles Diffusers.
- Prise en charge des frameworks : fournit des chemins Python et ComfyUI pour FLUX, Qwen Image/Edit, les ControlNets et Z-Image.

Nous devons faire correspondre la roue (wheel) à PyTorch, CUDA, Python et au GPU ; la documentation est étiquetée 1.3.0, alors que GitHub marque la v1.2.1 comme dernière version officielle.
Nous utilisons un espace de noms officiel de modèles Nunchaku et un workflow aligné sur la version, et nous traitons l'artefact QuantFunc 2511 comme une implémentation distincte.

## Ligne de développement {#development-line}

- **2025-08-03 — Nunchaku a publié des ressources d'intégration pour FLUX.1-Krea-dev.** Le 2025-08-03, Nunchaku a ajouté un dépôt Hugging Face et un exemple GitHub pour FLUX.1-Krea-dev. L'exemple documentait une voie d'implémentation pour ce modèle.
- **2025-09-24 — Nunchaku a documenté l'intégration de Qwen Image Edit 2509.** Le 2025-09-24, Nunchaku a documenté l'utilisation de Qwen Image Edit 2509 et a référencé un dépôt de modèle ainsi qu'un workflow ComfyUI. Ces fichiers fournissent une voie d'intégration opérationnelle pour cette variante d'édition d'images.
- **2026-01-23 — Un dépôt de modèle Qwen Image Edit 2511 portant le nom Nunchaku est apparu.** Le 2026-01-23, QuantFunc a publié le dépôt Nunchaku-Qwen-Image-EDIT-2511 sur Hugging Face. Ce fichier introduisait un artefact de modèle Qwen Image Edit postérieur à l'intégration 2509.

## Changements {#what-changed}

- 2025-08-03 — Nunchaku a ajouté la prise en charge 4 bits de FLUX.1-Krea-dev, en utilisant des poids de transformeur SVDQuant pour le point de contrôle compatible FLUX.
- 2025-09-24 — Nunchaku a publié les poids 4 bits de Qwen-Image-Edit-2509 ainsi que l'intégration Diffusers/ComfyUI, avec des choix INT4/NVFP4 et de rang.
- 2026-01-23 — QuantFunc a publié le point de contrôle Qwen-Image-Edit-2511 portant le nom Nunchaku, comme une re-quantification indépendante et non comme une version officielle de Nunchaku.

## Mode d'emploi {#how-to-use-this}

Au 2026-01-23, sélectionnez les ressources Nunchaku en fonction de la variante de modèle exacte prise en charge, et utilisez la documentation ou le workflow spécifique au modèle fourni, afin de ne pas supposer qu'une même configuration couvre les variantes FLUX.1-Krea-dev et Qwen Image Edit.

1. Installez une roue précompilée uniquement après l'avoir fait correspondre à PyTorch 2.5 ou version ultérieure, à CUDA, à Python et à l'architecture GPU ; ne compilez depuis les sources que lorsqu'aucune roue compatible n'existe.
  — <https://nunchaku.tech/docs/nunchaku/installation/installation.html>
2. Pour ComfyUI, installez le plugin ComfyUI-nunchaku, puis installez le backend Nunchaku dans le même environnement Python que celui dans lequel ComfyUI s'exécute.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/installation.html>
3. Téléchargez les ressources correspondantes du modèle quantifié Nunchaku et du modèle de base, importez un workflow d'exemple officiel, démarrez ComfyUI, puis sélectionnez ce workflow.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/usage.html>
4. Pour Qwen-Image-Edit-2509 en Python, chargez le transformeur Nunchaku via NunchakuQwenImageTransformer2DModel, utilisez QwenImageEditPlusPipeline avec le modèle de base en amont, et passez la liste d'images RGB utilisée par l'exemple officiel.
  — <https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509>
5. Dans le Wheel Installer de ComfyUI, actualisez la liste des versions, sélectionnez une version officielle, installez-la, puis redémarrez complètement ComfyUI ; n'utilisez la commande distincte de version de développement que pour les builds de développement.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/workflows/tools.html>

## Bonnes pratiques {#best-practices}

- Utilisez FP4 avec les GPU Blackwell de la série RTX 50 et INT4 avec les autres architectures GPU listées ; Blackwell requiert également PyTorch 2.7 ou version ultérieure avec CUDA 12.8 ou version ultérieure.
  — <https://nunchaku.tech/docs/nunchaku/installation/installation.html>
- Pour Qwen-Image-Edit-2509, choisissez r32 lorsque la vitesse compte et r128 lorsque la qualité de sortie compte davantage ; ne comparez pas leurs débits comme s'il s'agissait de configurations équivalentes.
  — <https://huggingface.co/nunchaku-tech/nunchaku-qwen-image-edit-2509>
- En cas de VRAM limitée, utilisez le déchargement asynchrone de Nunchaku ; si vous ajoutez le déchargement séquentiel CPU de Diffusers, excluez le transformeur Nunchaku, car son chemin de déchargement est différent. La configuration documentée peut réduire la consommation à environ 3 Go.
  — <https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509>
- Figez Qwen-Image-Edit-2509 sur diffusers 0.36.0 ou version ultérieure, et ne prévoyez pas de prise en charge officielle des LoRA personnalisées pour ce modèle tant que la documentation n'a pas changé.
  — <https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509>
- Privilégiez le sélecteur de version officielle du Wheel Installer plutôt que le sélecteur de version de développement pour les travaux en production, et redémarrez ComfyUI après toute modification de paquet.
  — <https://nunchaku.tech/docs/ComfyUI-nunchaku/workflows/tools.html>
- Conservez les poids Qwen-Image-Edit-2511 de QuantFunc en dehors du chemin de compatibilité officiel de Nunchaku ; ils ciblent le moteur propre à QuantFunc et sont explicitement indépendants de Nunchaku.
  — <https://www.modelscope.cn/models/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511>

## Remplacé par ceci {#superseded-by-this}

- L'état du 2025-09-24 selon lequel les modèles Lightning de Qwen-Image-Edit-2509 arriveraient plus tard — obsolète depuis le 2025-09-25.
- L'hypothèse selon laquelle tout point de contrôle portant le mot Nunchaku serait une version officielle du projet Nunchaku — obsolète depuis la clarification ultérieure de QuantFunc en 2026-07.

## Points encore inconnus {#still-unknown}

- La documentation actuelle est étiquetée 1.3.0, mais GitHub marque la v1.2.1 comme dernière version officielle et ne liste que des préversions v1.3.0dev ; nous n'avons trouvé aucune note de version stable v1.3.0.
- Nous n'avons trouvé aucune page officielle actuelle de prise en charge de Qwen-Image-Edit-2511 par Nunchaku. Le point de contrôle QuantFunc du 2026-01-23 est une re-quantification indépendante ; il ne constitue donc pas une preuve de compatibilité officielle avec Nunchaku.
- Les liens d'origine nunchaku-tech redirigent vers nunchux-ai sur GitHub et vers nunchaku-ai sur Hugging Face. Nous n'avons trouvé aucune annonce de renommage officielle distincte ; reproduisez donc les workflows à partir de la cible résolue, et figez la version exacte ou le fichier de modèle.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://github.com/nunchaku-tech/nunchaku | README du dépôt Nunchaku | 2026-09-04 |
| https://github.com/nunchux-ai/nunchaku/releases | Versions GitHub de Nunchaku | 2026-09-04 |
| https://www.krea.ai/blog/flux-krea-open-source-release | Publication des poids ouverts de FLUX.1 Krea | 2026-09-04 |
| https://huggingface.co/nunchaku-tech/nunchaku-flux.1-krea-dev/tree/main | Fichiers du modèle nunchaku-flux.1-krea-dev | 2026-09-04 |
| https://huggingface.co/nunchaku-tech/nunchaku-qwen-image-edit-2509 | Fiche du modèle Nunchaku Qwen-Image-Edit-2509 | 2026-09-04 |
| https://huggingface.co/Qwen/Qwen-Image-Edit-2509 | Fiche du modèle Qwen-Image-Edit-2509 | 2026-09-04 |
| https://huggingface.co/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511 | Fiche du modèle QuantFunc Nunchaku-Qwen-Image-EDIT-2511 | 2026-09-04 |
| https://www.modelscope.cn/models/QuantFunc/Nunchaku-Qwen-Image-EDIT-2511 | QuantFunc Nunchaku-Qwen-Image-EDIT-2511 sur ModelScope | 2026-09-04 |
| https://nunchaku.tech/docs/nunchaku/ | Documentation Nunchaku 1.3.0 | 2026-09-04 |
| https://nunchaku.tech/docs/nunchaku/installation/installation.html | Guide d'installation de Nunchaku | 2026-09-04 |
| https://nunchaku.tech/docs/nunchaku/usage/qwen-image-edit.html#qwen-image-edit-2509 | Guide d'utilisation de Nunchaku Qwen-Image-Edit | 2026-09-04 |
| https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/installation.html | Guide d'installation de ComfyUI-nunchaku | 2026-09-04 |
| https://nunchaku.tech/docs/ComfyUI-nunchaku/get_started/usage.html | Guide d'utilisation de ComfyUI-nunchaku | 2026-09-04 |
| https://nunchaku.tech/docs/ComfyUI-nunchaku/workflows/tools.html | Workflow Wheel Installer de ComfyUI-nunchaku | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:nunchaku`, fil `model-integration-expansion`, 3 événements datés du 2025-08-03 au 2026-01-23.
- **Note pratique :** Au 2026-01-23, sélectionnez les ressources Nunchaku en fonction de la variante de modèle exacte prise en charge, et utilisez la documentation ou le workflow spécifique au modèle fourni, afin de ne pas supposer qu'une même configuration couvre les variantes FLUX.1-Krea-dev et Qwen Image Edit.
- **Confiance :** élevée. Les mentions de remplacement datées font foi pour ce qui est obsolète.
