---
title: "NAVA"
category: projects
date: 2026-06-03
tags: [nava, nava-development, project]
aliases: ["NAVA"]
level: 3
source_sha256: e5c145d7400bd1fc03b2eb4689a3d60ca4fb21710c94665cfa83435c84311ca9
translation: machine
translated_at: '2026-10-24'
---
# NAVA {#nava}

**Ligne de développement :** `project:nava` · fil `nava-development`  
**Dernier événement :** 2026-06-03 · 1 daté depuis le 2026-06-03 · **Consulté le :** 2026-09-06 · confiance : moyenne

## Ce que c'est {#what-it-is}

NAVA est un modèle local conjoint audio-vidéo pour la génération texte-vers-audio-vidéo, la continuation d'image à partir de la première frame, la génération audio seule et la parole à timbre de référence.

- Génère ensemble la vidéo et l'audio stéréo de la scène et de la parole, au lieu d'ajouter l'audio après la génération vidéo.
- Utilise un MMDiT Align-then-Fuse ; les fichiers WAV de référence sont associés à des segments de parole `<S>…<E>` ordonnés.
- 1280×704 à 37 frames/24 fps tourne en environ six secondes ; l'inférence entièrement résidente est documentée à 80 Go de VRAM, tandis que la voie FP8 requiert environ 18 Go.
- Utilisez le code local maintenu ou la voie ComfyUI ; l'espace Hugging Face officiel était suspendu lors de la vérification.

## Ligne de développement {#development-line}

- **2026-06-03 — Les ressources publiques du projet NAVA ont été liées.** Le 2026-06-03, NAVA a lié sa page de projet, son dépôt GitHub et sa page Hugging Face afin de diriger les lecteurs vers la documentation, le code source et les ressources de modèle.

## Ce qui a changé {#what-changed}

- 2026-05-28 — L'article NAVA v1 décrivait un MMDiT Align-then-Fuse de 6,3 B paramètres pour la génération conjointe audio-vidéo.
- 2026-05-29 — NAVA a atteint sa première publication officielle du modèle.
- 2026-05-30 — NAVA a envoyé `NAVA.safetensors` et supprimé de Hub la copie de l'ancien `NAVA.ckpt`.
- 2026-06-01 — NAVA a ajouté le point de contrôle `NAVA_fp8.safetensors`, à moindre VRAM.
- 2026-06-03 — NAVA a envoyé la documentation de fiche modèle en anglais et en chinois simplifié ; GitHub a également mis à jour le README et optimisé l'inférence.
- 2026-06-05 — NAVA a ajouté la prise en charge FP8 pour ComfyUI.
- 2026-06-08 — NAVA a optimisé et nettoyé son implémentation ComfyUI.
- 2026-06-15 — NAVA a corrigé la désynchronisation du réécrivain de prompts FP8 et ajouté un flux de réécriture vision-langage.
- 2026-06-23 — NAVA a mis à jour son Space Hugging Face et son implémentation Gradio.
- 2026-06-30 — NAVA a mis à jour les scripts d'inférence VerseBench.

## Comment l'utiliser {#how-to-use-this}

1. Considérez la démo hébergée officielle comme indisponible pour le moment : son Space était suspendu lors de la vérification ; utilisez plutôt un flux de travail local.
  — <https://huggingface.co/spaces/baidu/NAVA>
2. Clonez le code officiel, installez d'abord PyTorch compatible avec CUDA, puis installez NAVA et FlashAttention dans l'ordre documenté.
  — <https://github.com/ernie-research/NAVA>
3. Téléchargez les poids maintenus depuis la page actuelle du modèle `baidu/NAVA` ; utilisez `NAVA.safetensors` pour le bf16 ou `NAVA_fp8.safetensors` pour la voie à moindre VRAM.
  — <https://huggingface.co/baidu/NAVA>
4. Placez chaque tâche dans un fichier JSONL : utilisez `prompt` pour la génération texte-vers-audio-vidéo, ajoutez `image_path` pour le conditionnement par la première frame, et ajoutez jusqu'à deux `spk_wavs` pour la parole à timbre contrôlé ; choisissez ensuite le script d'inférence correspondant.
  — <https://github.com/ernie-research/NAVA>
5. Pour un flux de travail par nœuds, installez les nœuds ComfyUI officiels, sélectionnez `NAVA_fp8.safetensors` et chargez l'un des graphes d'exemple fournis.
  — <https://github.com/ernie-research/NAVA/blob/main/comfyui_nava/README.md>

## Bonnes pratiques {#best-practices}

- Conservez l'installation de PyTorch compatible avec CUDA, l'installation NAVA en mode éditable et `flash-attn --no-build-isolation` comme étapes distinctes ; ne forcez pas la réinstallation du fichier de dépendances.
  — <https://github.com/ernie-research/NAVA>
- Réécrivez les prompts courts ou en anglais avant l'inférence, et conservez chaque segment de parole `<S>…<E>` sans modification.
  — <https://github.com/ernie-research/NAVA>
- Gardez l'ordre des fichiers WAV de référence aligné sur l'ordre des segments de parole ; pour ComfyUI, activez d'abord le déchargement de T5 et le déchargement par groupes en dessous de 48 Go de VRAM.
  — <https://github.com/ernie-research/NAVA/blob/main/comfyui_nava/README.md>
- Utilisez FP8 pour réduire la VRAM, et non pour espérer des calculs matriciels plus rapides ; il est déquantifié en bf16 au moment du calcul.
  — <https://github.com/ernie-research/NAVA>
- Utilisez uniquement des références de visage et de voix approuvées par leurs titulaires, étiquetez le contenu généré comme synthétique, et appliquez une traçabilité ou un filigrane avant toute redistribution.
  — <https://huggingface.co/baidu/NAVA>
- Privilégiez les points de contrôle safetensors actuels ; Hub a supprimé `NAVA.ckpt`, même si le code local conserve la compatibilité avec ce format.
  — <https://huggingface.co/baidu/NAVA/commits/main>

## Remplacé par ceci {#superseded-by-this}

- 2026-05-30 — La consigne de téléchargement depuis Hub exigeant `NAVA.ckpt` est obsolète : le Hub officiel a supprimé cet artefact et fournit des points de contrôle safetensors ; la compatibilité locale avec `.ckpt` demeure.
- 2026-06-05 — Traiter NAVA comme un flux de travail en script seul sur 8 GPU est dépassé : le projet officiel a ajouté une voie FP8 pour ComfyUI.
- 2026-06-15 — Les consignes de réécriture FP8 antérieures à la correction sont obsolètes pour les travaux conditionnés par image : le code officiel a corrigé la désynchronisation du réécrivain et ajouté la réécriture VL.

## Toujours inconnu {#still-unknown}

- Le texte exact accompagnant l'entrée du 2026-06-03 n'est pas disponible ; nous considérons donc cette date comme une étape de mise à jour de la documentation et de l'inférence le même jour, et non comme une annonce de lancement déduite.
- Aucune étiquette de version sémantique ni aucune GitHub Release ne fait correspondre les modifications au niveau des commits à des versions NAVA numérotées.
- L'espace officiel était suspendu lors de la vérification ; une exécution réussie actuelle de l'inférence hébergée n'a donc pas été vérifiée.
- La documentation officielle est incohérente en interne : le code actuel utilise safetensors par défaut, alors que certaines parties de la fiche modèle mentionnent encore les chemins supprimés de `NAVA.ckpt`.
- Aucune entrée ultérieure de code ou d'historique de modèle émanant de l'éditeur n'a été trouvée après le 2026-06-30 ; cela ne prouve pas qu'aucune mise à jour n'existe en dehors des historiques officiels consultés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/abs/2605.30073 | Native Audio-Visual Alignment for Generation — arXiv:2605.30073 | 2026-09-06 |
| https://ernie-research.github.io/NAVA/ | NAVA · Native Audio-Visual Alignment for Generation | 2026-09-06 |
| https://github.com/ernie-research/NAVA | ernie-research/NAVA — Official Code of NAVA | 2026-09-06 |
| https://github.com/ernie-research/NAVA/commits/main | Commits · ernie-research/NAVA | 2026-09-06 |
| https://huggingface.co/ernie-research/NAVA | ernie-research/NAVA redirect to baidu/NAVA | 2026-09-06 |
| https://huggingface.co/baidu/NAVA | baidu/NAVA · Hugging Face | 2026-09-06 |
| https://huggingface.co/baidu/NAVA/commits/main | Commits · baidu/NAVA | 2026-09-06 |
| https://huggingface.co/baidu/NAVA/blob/main/README_zh.md | README_zh.md · baidu/NAVA | 2026-09-06 |
| https://github.com/ernie-research/NAVA/blob/main/comfyui_nava/README.md | NAVA ComfyUI Nodes | 2026-09-06 |
| https://huggingface.co/spaces/baidu/NAVA | NAVA Audio-Video Generator — Hugging Face Space | 2026-09-06 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:nava`, fil `nava-development`, 1 événement daté du 2026-06-03 au 2026-06-03.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
