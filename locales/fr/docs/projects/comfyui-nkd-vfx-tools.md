---
title: "ComfyUI-NKD-VFX-Tools"
category: projects

tags: [comfyui-nkd-vfx-tools, comfyui-nkd-vfx-tools-development, comfyui_nkd_vfx_tools, project]
aliases: ["ComfyUI-NKD-VFX-Tools"]
level: 2
source_sha256: 1a6d8b7968fb51bd60d2abdef3dda72a4d8ce039f463a7e0bf067e54b0222d6b
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI-NKD-VFX-Tools {#comfyui-nkd-vfx-tools}

**Ligne de développement :** `project:comfyui-nkd-vfx-tools` · fil `comfyui-nkd-vfx-tools-development`  
**Dernier événement :** - · 0 daté depuis - · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

ComfyUI-NKD-VFX-Tools fournit des nœuds interactifs orientés VFX plutôt qu'un modèle : Relight, Lens Blur, Preview 3D, fSpy Camera, Camera Delta Prompt, Perspective Unwarp/Rewarp, Lens Distort et Mask Scheduler. Les métadonnées actuelles du paquet indiquent la version 1.7.4 ; il nécessite une version récente du frontend ComfyUI et numpy, tandis que les bords sans raccord (Seamless Edges) du nœud Perspective Rewarp utilisent en plus OpenCV. Verdict : utilisez-le pour construire des conditions d'image contrôlables et les transmettre à un workflow de génération ComfyUI existant, et non comme un remplacement d'un modèle de diffusion.

## Ligne de développement {#development-line}

- La ligne datée n'est pas encore rédigée ; les éléments connus figurent dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

2026-07-24 — Le paquet en était à sa première ligne de publication publique : l'historique first-party place la première version publique au 21 juillet et ajoute des instructions d'utilisation le 23 juillet ; l'élément du 24 juillet représente donc une première étape de mise à disposition publique, mais aucun commit first-party n'est enregistré spécifiquement pour le 24 juillet. 2026-07-27 — Lens Distort a été documenté en version 1.4.0, et Preview 3D a reçu une entrée MESH directe ainsi que des contrôles de FOV, de roulis et de couleur d'arrière-plan. 2026-07-30 — Preview 3D a ajouté la prise en charge des entrées Hunyuan3D/modèles de sortie, une sortie de profondeur contrôlée par la fenêtre d'affichage, des normales lissées automatiquement et une visionneuse détachable avec raccourcis clavier pour le gizmo. 2026-07-31 — Le calcul de l'ombre de contact a été corrigé pour marquer le contact réel avec le sol ; le paquet a été porté en version 1.7.2. État observé actuel — les métadonnées du paquet indiquent la version 1.7.4.

## Mode d'emploi {#how-to-use-this}

Au 2026-07-24, aucune modification destinée aux praticiens ne peut être proposée, car la publication source, les liens et les éléments de recherche étaient indisponibles.

1. Installez depuis ComfyUI Manager en recherchant NKD VFX Tools, ou clonez le dépôt dans ComfyUI/custom_nodes ; redémarrez ensuite ComfyUI.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
2. Ouvrez les nœuds dans le menu NKD Nodes et construisez d'abord l'image de contrôle : résolvez la caméra ou la perspective, positionnez le contenu 3D, et créez les conditions de profondeur ou d'éclairage avant de transmettre les sorties au graphe de génération.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
3. Pour le calage de caméra, tracez deux paires de lignes de fuite dans NKD fSpy Camera ; pour une modification de perspective, dépliez la surface (unwarp), modifiez-la, puis replions-la (rewarp).
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
4. Utilisez Preview 3D avec des entrées GLB/GLTF, des splats gaussiens ou des maillages pris en charge pour produire un composite, une couche d'objet, un masque, une carte de profondeur et les informations de caméra pour les nœuds en aval.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>

## Bonnes pratiques {#best-practices}

- Traitez les nœuds comme une direction artistique en amont de la génération : rendez explicites la lumière, la caméra, la profondeur, le placement et la perspective dans l'image de contrôle, plutôt que de vous fier au seul texte du prompt.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
- Gardez le frontend de ComfyUI à jour et installez numpy ; n'installez OpenCV que si Perspective Rewarp nécessite Seamless Edges, car le reste de ce nœud reste utilisable sans lui.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>
- Utilisez les fenêtres d'affichage interactives pour vérifier visuellement les contrôles avant de lancer une passe de génération coûteuse.
  — <https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools>

## Remplacé par ceci {#superseded-by-this}

- 2026-07-23 : le README initial décrivait son guide d'utilisation comme provisoire en attendant que les workflows d'exemple soient prêts ; la documentation first-party actuelle ne fournit toujours pas de collection datée de workflows de remplacement, donc aucune recommandation de remplacement précise n'est vérifiée.

## Toujours inconnu {#still-unknown}

- L'événement du 24 juillet n'a ni URL extraite ni texte source public. Les éléments first-party établissent des dates de publication et de documentation voisines, mais n'identifient pas de commit, de version ou de contenu d'annonce exact pour le 24 juillet.
- Aucune fiche de publication first-party datée n'a été trouvée pour la version 1.7.4 actuelle des métadonnées ; sa date de publication exacte n'est donc pas vérifiée.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools | Dépôt Nekodificador / ComfyUI-NKD-VFX-Tools et README | 2026-09-05 |
| https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools/commits/master/ | Historique des commits de ComfyUI-NKD-VFX-Tools | 2026-09-05 |
| https://github.com/Nekodificador/ComfyUI-NKD-VFX-Tools/blob/master/pyproject.toml | Métadonnées du paquet ComfyUI-NKD-VFX-Tools | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:comfyui-nkd-vfx-tools`, fil `comfyui-nkd-vfx-tools-development`, 0 événement daté - → -.
- **Note pratique :** Au 2026-07-24, aucune modification destinée aux praticiens ne peut être proposée, car la publication source, les liens et les éléments de recherche étaient indisponibles.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
