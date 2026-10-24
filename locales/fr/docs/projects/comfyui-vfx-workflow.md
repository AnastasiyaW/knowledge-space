---
title: "heydoughogan ComfyUI VFX Workflow — passes VFX ComfyUI"
category: projects
date: 2026-06-12
tags: [comfyui-vfx-passes, comfyui-vfx-workflow, project]
aliases: ["heydoughogan ComfyUI VFX Workflow"]
level: 2
source_sha256: f2619a3c10cd3836bac86198d670c0137c36b6a93afeec8d3557329749b1f577
translation: machine
translated_at: '2026-10-24'
---
# heydoughogan ComfyUI VFX Workflow — passes VFX ComfyUI {#heydoughogan-comfyui-vfx-workflow-comfyui-vfx-passes}

**Ligne de développement :** `project:comfyui-vfx-workflow` · fil `comfyui-vfx-passes`  
**Dernier événement :** 2026-06-12 · 1 événement daté depuis le 2026-06-12 · **Recherche :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

VFX Utilities est un workflow ComfyUI créé par Doug Hogan à l'intention des compositeurs et des artistes VFX. Il génère des passes pour le relighting, la composition et le look development, sans rendu CG séparé.

- Extraction d'alpha et de matte avec RMBG et SAM3
- Segmentation par prompt texte et par points
- Segmentation des visages
- Génération de passes de profondeur et de normales

La fiche fournit actuellement 1 graphe JSON téléchargeable.

## Ligne de développement {#development-line}

- **2026-06-12 — Référence Comfy datée pour les passes VFX.** Le graphe combine l'ingestion de vidéo source, RMBG, les prompts et points SAM3, la segmentation des visages, la profondeur et les normales dans un seul graphe ComfyUI. La fiche actuelle liste les cartes d'alpha, de profondeur et de normales comme sorties. Nous n'avons pas de confirmation de l'état du graphe à la date de publication.

## Modifications {#what-changed}

2026-06-12 — Publication du workflow VFX Utilities. Il combine l'ingestion de vidéo source, RMBG, les prompts et points SAM3, la segmentation des visages, la profondeur et les normales dans un seul graphe ComfyUI. La fiche actuelle liste les cartes d'alpha, de profondeur et de normales comme sorties. La version historique du graphe à la date de publication reste non confirmée.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-12, considérez le workflow Comfy lié comme une référence à inspecter manuellement pour les travaux de passes VFX, plutôt que comme une recette vérifiée ou entièrement documentée.

1. Ouvrez la fiche et téléchargez le JSON du workflow.
  — <https://comfy.org/workflows/be0889296f65-be0889296f65/>
2. Chargez le JSON dans ComfyUI, fournissez une image ou un plan vidéo, puis définissez le texte du prompt ou les points de segmentation.
  — <https://comfy.org/workflows/download/be0889296f65.json?filename=be0889296f65>
3. Exécutez les chemins nécessaires et utilisez les sorties alpha, profondeur et normales comme passes pour la composition, le relighting ou le look development.
  — <https://comfy.org/workflows/be0889296f65-be0889296f65/>

## Remplacé par {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Inconnues restantes {#still-unknown}

- L'événement indiquait une URL de compte pour heydoughogan, mais nous n'avons pas pu la vérifier. L'auteur confirmé de la fiche est Doug Hogan (@doughogan).
- La fiche affiche le JSON actuel avec une date de création relative ; la configuration exacte des nœuds et des modèles au 2026-06-12 n'est donc pas confirmée.
- Nous n'avons trouvé aucune source primaire datée confirmant des modifications ultérieures de ce workflow ; aucun nouvel événement daté n'est donc ajouté.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://comfy.org/workflows/be0889296f65-be0889296f65/ | VFX Utilities - ComfyUI Workflow | 2026-09-05 |
| https://comfy.org/workflows/download/be0889296f65.json?filename=be0889296f65 | be0889296f65 workflow JSON | 2026-09-05 |
| https://comfy.org/workflows/doughogan/ | Doug Hogan - ComfyUI Workflow Templates | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:comfyui-vfx-workflow`, fil `comfyui-vfx-passes`, 1 événement daté du 2026-06-12 au 2026-06-12.
- **Note pratique :** Au 2026-06-12, les praticiens doivent considérer le workflow Comfy lié comme une référence à inspecter manuellement pour les travaux de passes VFX, plutôt que comme une recette vérifiée ou entièrement documentée.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
