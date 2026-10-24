---
title: "LTX-2.3-Foley-LoRA — LTX Video"
category: projects
date: 2026-07-01
tags: [ltx-foley-lora, ltx-video, ltx_video, project]
aliases: ["LTX-2.3-Foley-LoRA"]
level: 2
source_sha256: 4e3d5aea59ce758a576954ce94e5c9cf11a7478eef944dff5068292c58c1285e
translation: machine
translated_at: '2026-10-24'
---
# LTX-2.3-Foley-LoRA — LTX Video {#ltx-23-foley-lora-ltx-video}

**Ligne de développement :** `project:ltx-foley-lora` · fil `ltx-video`  
**Dernier événement :** 2026-07-01 · 1 événement daté depuis le 2026-07-01 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

LTX-2.3-Foley-LoRA est un LoRA vidéo-vers-audio de 400 étapes destiné aux modèles de base ou distillés LTX-2.3. Il prend en entrée une vidéo muette et une consigne d'action pour générer des bruitages (Foley) synchronisés et non verbaux. Ce n'est pas un modèle généraliste de musique ou de dialogue. Utilisez un multiplicateur LoRA compris entre 1 et 3. Il corrige les générations LTX-2.3 qui ajoutent une musique de fond, mais le comportement sur la parole reste insuffisamment documenté.

## Ligne de développement {#development-line}

- **2026-07-01 — Enregistrement de la page du modèle LTX-2.3-Foley-LoRA.** Le 2026-07-01, FuzzPuppy a publié la page de modèle Hugging Face de LTX-2.3-Foley-LoRA. La page fournit l'artefact LoRA Foley, mais ne détaille ni ses capacités, ni sa provenance, ni sa compatibilité, ni les informations de publication.

## Modifications {#what-changed}

- 2026-07-01 — LTX-2.3-Foley-LoRA a été publié sous la forme d'un adaptateur de 400 étapes destiné à supprimer les accompagnements musicaux et à générer des effets sonores correspondant visuellement à la scène. Son auteur l'a entraîné sans exemples de parole et n'a pas testé la parole.
- 2026-07-04 — Le dépôt ComfyUI associé a ajouté un workflow de fenêtre glissante pour les vidéos longues, avec chevauchement et raccord audio, étendant le workflow initial conçu pour les clips courts.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-07-01, évaluez et vérifiez LTX-2.3-Foley-LoRA sur Hugging Face avant de vous en servir en production ; cette seule ligne de développement ne permet pas d'étayer des affirmations opérationnelles.

1. Téléchargez `ltx-2.3-foley-400-steps.safetensors`, chargez-le avec un modèle vidéo-vers-audio LTX-2.3 de base ou distillé, et commencez avec une intensité LoRA de 1.0.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA>
2. Pour ComfyUI, installez les nœuds officiels LTXVideo et les nœuds auxiliaires `ltx_foley_v2a` du dépôt de workflows ; placez le LoRA dans `ComfyUI/models/loras`.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow>
3. Utilisez le workflow court pour un clip rapide ; utilisez `foley-sliding-window.json` pour les vidéos plus longues, afin que les fenêtres soient chevauchées puis raccordées.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow>

## Bonnes pratiques {#best-practices}

- Décrivez uniquement l'action visible, puis ajoutez « No speech is present. No music is present » ; utilisez un prompt négatif anti-musique.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA>
- Augmentez l'intensité du LoRA de 1 vers 2 ou 3 uniquement si la musique subsiste dans la sortie.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA>
- Lancez ComfyUI avec `--cache-classic` pour le workflow à fenêtre glissante, afin d'éviter que les volumineuses sorties des nœuds LTX soient purgées puis recalculées entre les fenêtres.
  — <https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow>

## Remplacé par {#superseded-by-this}

- 2026-07-04 — Considérer le workflow initial pour clips courts comme la seule voie prise en charge est obsolète pour les vidéos longues ; utilisez plutôt le workflow à fenêtre glissante.

## Points encore inconnus {#still-unknown}

- La fiche du modèle ne documente ni les données d'entraînement, ni les métriques d'évaluation, ni les besoins exacts en VRAM, ni la préservation fiable des dialogues.
- La mise à jour du workflow du 2026-07-04 apparaît dans l'historique du dépôt et la documentation sur les vidéos longues, mais ne dispose pas de note de version immuable.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-LoRA | FuzzPuppy/LTX-2.3-Foley-LoRA | 2026-09-05 |
| https://huggingface.co/FuzzPuppy/LTX-2.3-Foley-Workflow | FuzzPuppy/LTX-2.3-Foley-Workflow | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1uk60hg/ltx23_foley_lora_for_synced_sound_effects_without/ | LTX-2.3 Foley LoRA for synced sound effects without unwanted music | 2026-09-05 |

## Fiche pour agents {#agent-brief}

- **Sujet :** `project:ltx-foley-lora`, fil `ltx-video`, 1 événement daté du 2026-07-01 au 2026-07-01.
- **Note pratique :** À partir du 2026-07-01, les praticiens doivent considérer LTX-2.3-Foley-LoRA comme un artefact Foley-LoRA Hugging Face distinct, à évaluer et vérifier avant de s'y fier ; cette seule ligne de développement ne permet pas d'étayer des affirmations opérationnelles.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi quant à ce qui est obsolète.
