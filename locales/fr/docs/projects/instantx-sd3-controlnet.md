---
title: "InstantX SD3 ControlNet — Publications de points de contrôle SD3 ControlNet"
category: projects
date: 2024-06-17
tags: [instantx-sd3-controlnet, project, sd3-controlnet-checkpoint-releases]
aliases: ["InstantX SD3 ControlNet"]
level: 3
source_sha256: ffeeda56aab1973756571ad11fad481fc0997b57677386332bf02ed7bc22607b
translation: machine
translated_at: '2026-10-24'
---
# InstantX SD3 ControlNet — Publications de points de contrôle SD3 ControlNet {#instantx-sd3-controlnet-sd3-controlnet-checkpoint-releases}

**Ligne de développement :** `project:instantx-sd3-controlnet` · fil `sd3-controlnet-checkpoint-releases`  
**Dernier événement :** 2024-06-17 · 2 événements datés depuis 2024-06-15 · **Recherche effectuée :** 2026-09-04 · niveau de confiance : moyen

## Description {#what-it-is}

InstantX SD3 ControlNet fournit des adaptateurs d'image de contrôle destinés aux praticiens qui ont besoin que Stable Diffusion 3 suive des entrées structurelles :
- Canny : suit les contours des bords.
- Pose : suit les poses humaines.
- Tile : suit les tuiles et le guidage par image.
- Depth : suit les cartes de profondeur.

Canny et Pose sont des points de contrôle 0.6B F16 dont les fiches indiquent que l'entraînement n'a utilisé que du 1024×1024. Nous les utilisons lorsque SD3 Medium, soumis à un accès restreint, et un flux de travail en carré 1024 conviennent. La compatibilité avec les versions ultérieures de la famille SD3 n'est pas établie ici.

## Ligne de développement {#development-line}

- **2024-06-15 — Les dépôts InstantX SD3 ControlNet Canny sont apparus sur Hugging Face.** Le 2024-06-15, des liens Hugging Face associés à InstantX SD3 ControlNet pointaient vers un dépôt Canny_alpha_512 et un dépôt Canny. Des artefacts SD3 ControlNet conditionnés par Canny sont ainsi devenus disponibles dans cette ligne de projet.
- **2024-06-17 — Le dépôt InstantX SD3 ControlNet Pose est apparu sur Hugging Face.** Le 2024-06-17, un lien Hugging Face associé à InstantX SD3 ControlNet pointait vers le dépôt SD3-Controlnet-Pose. Cela ajoute à la ligne de projet enregistrée un artefact conditionné par la pose.

## Modifications {#what-changed}

- 2024-06-15 — Canny a été initialisé et a reçu sa configuration et son point de contrôle ; le point d'accès distinct `Canny_alpha_512` reste non vérifié à ce jour.
- 2024-06-17 — La documentation et les ressources de Pose ont changé, tandis que Tile a reçu son point de contrôle ; le point de contrôle initial de Pose était arrivé le 15 juin.
- 2024-06-19 — L'installation de Canny est passée du fork `sd3_control` d'InstantX à `diffusers >= 0.30.0.dev0`.
- 2024-06-23 — SD3-Controlnet-Depth a été créé et a reçu son point de contrôle.
- 2025-04-24 — Le nom de classe de configuration de Canny a été corrigé afin que le chargement direct via `AutoModel.from_pretrained` fonctionne.

## Mode d'emploi {#how-to-use-this}

À partir du 2024-06-15, les praticiens pouvaient étudier les artefacts InstantX SD3 ControlNet Canny pour des flux de travail guidés par les contours. À partir du 2024-06-17, ils pouvaient aussi étudier son artefact conditionné par la pose pour des flux de travail guidés par la pose. Vérifiez la compatibilité, la licence, la révision et les exigences du flux de travail avant utilisation.

1. Acceptez la condition d'accès à Stable Diffusion 3 Medium et authentifiez-vous auprès de Hugging Face avant de télécharger le modèle de base.
  — <https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3>
2. Chargez `InstantX/SD3-Controlnet-Canny` en tant que `SD3ControlNetModel`, associez-le à `StableDiffusion3ControlNetPipeline` avec `stabilityai/stable-diffusion-3-medium-diffusers`, puis exécutez-le sur CUDA en FP16.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Canny>
3. Pour le contrôle de la pose, remplacez par `InstantX/SD3-Controlnet-Pose` et fournissez une image de contrôle de pose. Canny et Pose utilisent des entrées de contrôle correspondantes distinctes.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Pose>
4. Transmettez un prompt et un `control_image`. Pour plusieurs contrôles, chargez une liste de SD3 ControlNet et transmettez une image correspondante par contrôle.
  — <https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sd3>
5. Sur les GPU aux ressources limitées, utilisez FP16 et le déchargement du modèle vers le CPU avant de réduire les paramètres de qualité. Les trois encodeurs de texte de SD3 sont exigeants en dessous de 24 Go de VRAM, même en FP16.
  — <https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3>

## Bonnes pratiques {#best-practices}

- Commencez Canny ou Pose en 1024×1024. Leurs fiches indiquent que d'autres résolutions peuvent être sous-optimales, car l'entraînement n'a utilisé que du 1024×1024.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Canny>
- Commencez avec `controlnet_conditioning_scale=0.5` de la démo de l'auteur. Ajustez délibérément pour chaque image de contrôle plutôt que de le considérer comme universel.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Pose>
- Utilisez la base SD3 Medium documentée pour une recette dont la compatibilité est connue. Ne supposez pas que ces points de contrôle fonctionnent sans modification avec une autre base de la famille SD3.
  — <https://huggingface.co/InstantX/SD3-Controlnet-Canny>
- Un retour d'expérience en chinois sur ComfyUI, publié en juin 2024, recommandait des poids faibles, une fin de contrôle précoce et de traiter les résultats comme une image de départ. Conservez-le comme observation historique d'un flux de travail, et non comme plage universelle actuelle.
  — <https://www.youtube.com/watch?v=5SdRiZ53WPM>

## Remplacé par {#superseded-by-this}

- 2024-06-19 — L'ancien chemin d'installation qui clonait `instantX-research/diffusers_sd3_control` à la branche `sd3_control` a été remplacé par l'exigence Diffusers. Source : https://huggingface.co/InstantX/SD3-Controlnet-Canny/commit/a59221661ea027c11d813cbc595133ca8e56adb5
- 2025-04-24 — Les configurations Canny antérieures à la correction du nom de classe ne prennent pas en charge le chargement direct via `AutoModel.from_pretrained`. Source : https://huggingface.co/InstantX/SD3-Controlnet-Canny/discussions/12

## Points toujours inconnus {#still-unknown}

- https://huggingface.co/InstantX/SD3-Controlnet-Canny_alpha_512 n'a pas pu être récupéré lors de cette session de recherche. Ses poids exacts, sa résolution et son lien avec Canny ne sont pas vérifiés.
- La mise à jour Depth du 2024-07-03 récupérée n'est décrite que comme le téléversement de deux fichiers, et non comme une publication nommée ; son périmètre fonctionnel est donc inconnu.
- Aucune matrice de compatibilité actuelle, émise par l'éditeur, n'a été trouvée pour ces points de contrôle Canny, Pose, Tile et Depth avec SD3.5, les versions actuelles de ComfyUI ou la VRAM des GPU grand public récents.
- Aucune licence explicite n'a été vérifiée à partir des fiches récupérées de Canny, Pose ou Tile. Ne déduisez pas leurs conditions de l'étiquette Apache-2.0 visible sur Depth.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/InstantX/SD3-Controlnet-Canny | InstantX/SD3-Controlnet-Canny | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Pose | InstantX/SD3-Controlnet-Pose | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Pose/tree/main | Fichiers InstantX/SD3-Controlnet-Pose | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Canny/commits/e42ecba9741dee3de8c54039eba8a879c0070ced | Historique des commits — InstantX/SD3-Controlnet-Canny | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Pose/commits/main | Historique des commits — InstantX/SD3-Controlnet-Pose | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Tile/commits/main | Historique des commits — InstantX/SD3-Controlnet-Tile | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Depth/commits/main | Historique des commits — InstantX/SD3-Controlnet-Depth | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Canny/commit/a59221661ea027c11d813cbc595133ca8e56adb5 | Mise à jour du README de Canny, 19 juin 2024 | 2026-09-04 |
| https://huggingface.co/InstantX/SD3-Controlnet-Canny/discussions/12 | Correction du nom de classe de configuration de Canny | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/controlnet_sd3 | ControlNet with Stable Diffusion 3 — Diffusers | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion_3 | Stable Diffusion 3 — Diffusers | 2026-09-04 |
| https://www.youtube.com/watch?v=5SdRiZ53WPM | 在ComfyUI中使用新发布的SD3 ControlNet模型，对比SD1.5及SDXL同款，能控制但不够稳定 | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:instantx-sd3-controlnet`, fil `sd3-controlnet-checkpoint-releases`, 2 événements datés du 2024-06-15 au 2024-06-17.
- **Note pratique :** À partir du 2024-06-15, les praticiens pouvaient étudier les artefacts InstantX SD3 ControlNet Canny pour des flux de travail guidés par les contours. À partir du 2024-06-17, ils pouvaient aussi étudier son artefact conditionné par la pose pour des flux de travail guidés par la pose. Vérifiez la compatibilité, la licence, la révision et les exigences du flux de travail avant utilisation.
- **Niveau de confiance :** moyen. Les mentions datées de remplacement ci-dessus font foi pour ce qui est obsolète.
