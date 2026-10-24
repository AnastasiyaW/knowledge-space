---
title: "OrbitSheets"
category: projects
date: 2026-08-17
tags: [comfyui-orbitsheets, lumosai8/comfyui-orbitsheets, project]
aliases: ["OrbitSheets"]
level: 2
source_sha256: 3649fa7ee73590bc60ce8d8e6442c9b4b5d2e5d42030c3cb4cd7092c7e671e6b
translation: machine
translated_at: '2026-10-24'
---
# OrbitSheets {#orbitsheets}

**Ligne de développement :** `project:comfyui-orbitsheets` · fil `comfyui-orbitsheets`  
**Dernier événement :** 2026-08-17 · 1 événement daté depuis le 2026-08-17 · **Recherche :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

OrbitSheets est un pack de nœuds ComfyUI pour les turnarounds de personnages et les planches de lieux. Il les construit à partir d'une seule prise vidéo MiniMax-H3, au lieu de prompts d'image séparés.

- Prompts de plans coupés : écrit des séquences de prompts pour les vues de personnages et de lieux.
- Sélection de frames : choisit des frames nettes et distinctes et construit une planche de contact.
- Évaluation des frames : note les frames via CLIP intégré au graphe, un endpoint de vision compatible OpenAI, ou un repli basé sur la netteté et la diversité.
- Référence audio : extrait une piste vocale du personnage à partir de la prise.

La version 0.1.0 requiert Python >=3.10 et `requests`. Elle nécessite les assets MiniMax H3 et ne constitue pas une implémentation de H3. Utilisez-la comme outil de workflow lorsque H3 fonctionne déjà, et non comme modèle autonome ou plugin publié.

## Ligne de développement {#development-line}

- **2026-08-17 — Dépôt GitHub d'OrbitSheets relié dans le fil de développement.** La séquence de développement visible se termine au commit du 2026-08-14, et GitHub ne présente aucune release.

## Ce qui a changé {#what-changed}

2026-08-13 — Quatre commits ont ajouté le pack MiniMax-H3 pour personnages et lieux, mis à jour les workflows d'exemple et ajouté un nœud d'attention dans le graphe.  
2026-08-14 — Le commit 8952eae a fait passer le workflow de lieu par défaut aux vues coupées et ajouté un garde-fou sur la vitesse de rotation. Le mouvement continu est devenu optionnel.  
2026-08-17 — Aucune nouvelle version n'est apparue à cette date. Les commits visibles se terminent le 2026-08-14, et GitHub ne présente aucune release.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-17, le dépôt GitHub relié est la source datée d'OrbitSheets. Vérifiez directement les fichiers avant de vous fier à une affirmation sur une fonctionnalité.

1. Clonez le dépôt dans `ComfyUI/custom_nodes`, puis redémarrez ComfyUI. Les nœuds apparaissent sous la catégorie `OrbitSheets`.
2. Placez le modèle de diffusion MiniMax H3, l'encodeur de texte Qwen3-VL 32B H3 et le VAE vidéo H3 dans les dossiers de modèles de ComfyUI. Ajoutez le VAE audio H3 uniquement si vous avez besoin de la piste vocale. Choisissez n'importe quel modèle d'ancrage ; les exemples utilisent Krea2.
3. Glissez un graphe depuis `example_workflows/` pour des exécutions manuelles, ou soumettez le graphe correspondant dans `api_workflows/`. Le chemin va de l'image d'ancrage → `MiniMaxH3ImageToVideo` → frames/audio décodés → Frame Select → Contact Sheet.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>
4. Vérifiez la sortie `info` de Frame Select après chaque exécution. Elle indique si la sélection a utilisé le CLIP intégré au graphe, un modèle de vision HTTP ou le repli déterministe.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>

## Bonnes pratiques {#best-practices}

- Conservez `coverage=cut views` pour les planches de lieux. Passez à `continuous move` uniquement lorsque les coupures inventeraient des parties non vues, et gardez la rotation sous la limite de 40°/s.
- Réglez `shots` sur le nombre de vues visé. Réglez `count` sur la même valeur lorsque vous voulez un élément retenu par vue. Privilégiez `shot_split=views (by content)`. Relancez la prise H3 ou réduisez `shots` si `info` signale moins de vues distinctes.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>
- Utilisez `full body, generous margin` pour les ailes, les queues et les accessoires. Donnez à l'ancrage la même marge afin que les limites de recadrage ne cassent pas le turnaround.
- Gardez `free_vram_first` activé avant l'évaluation par vision. Testez les rendus avant d'utiliser le backend d'attention avec pertes `comfy kitchen (int8)`.
  — <https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py>
- Épinglez le commit dans les workflows partagés, car la page des releases GitHub ne contient aucune release.
  — <https://github.com/lumosai8/ComfyUI-OrbitSheets/releases>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-14 — Le guidage d'orbite continue pour les planches de lieux est obsolète. `coverage=cut views` est désormais la valeur par défaut. Le mouvement continu ne reste utilisé que lorsque les coupures inventeraient des faces non vues.
- 2026-08-14 — Les rotations non bornées dans les prises courtes sont obsolètes. Le projet limite les rotations au-delà de 40°/s et documente environ neuf secondes pour une rotation de 360 degrés.

## Toujours inconnu {#still-unknown}

- Le README ne correspond pas au code pour les plans de personnages. Certaines sections annoncent cinq plans ou huit frames. Le code actuel du nœud et le graphe de personnage retiennent six vues, dont le visage effrayé optionnel, à partir d'une prise de 124 frames.
- Le README et les métadonnées du paquet ne mentionnent aucune version testée de ComfyUI-core, aucune révision du paquet H3 ni aucune matrice de compatibilité.
- Les tests en amont vérifient le code de sélection et de prompts sans GPU. Nous n'avons vérifié aucun rendu MiniMax H3 en conditions réelles ici.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/lumosai8/ComfyUI-OrbitSheets | GitHub — lumosai8/ComfyUI-OrbitSheets | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/commits/main | Commits — lumosai8/ComfyUI-OrbitSheets | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/commit/8952eae1d3298f241c538c029a6e929509c4813f | Découper la planche de lieu au lieu de faire tourner la caméra autour — commit 8952eae | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/blob/main/pyproject.toml | ComfyUI-OrbitSheets pyproject.toml | 2026-09-05 |
| https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/nodes.py | ComfyUI-OrbitSheets nodes.py | 2026-09-05 |
| https://raw.githubusercontent.com/lumosai8/ComfyUI-OrbitSheets/main/example_workflows/CharacterTurnaroundSheetH3.json | Workflow canvas CharacterTurnaroundSheetH3 fourni | 2026-09-05 |
| https://github.com/lumosai8/ComfyUI-OrbitSheets/releases | Releases — lumosai8/ComfyUI-OrbitSheets | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:comfyui-orbitsheets`, fil `comfyui-orbitsheets`, 1 événement daté du 2026-08-17 au 2026-08-17.
- **Note pratique :** Au 2026-08-17, les praticiens peuvent utiliser le dépôt GitHub relié comme emplacement source daté d'OrbitSheets, tout en vérifiant son contenu avant de se fier à une affirmation sur l'installation ou une fonctionnalité.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
