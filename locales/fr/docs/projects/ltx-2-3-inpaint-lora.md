---
title: "LTX-2.3 inpaint LoRA"
category: projects
date: 2026-03-24
tags: [ltx-2-3-inpaint-lora, ltx_2_3_inpaint_lora, project]
aliases: ["LTX-2.3 inpaint LoRA"]
level: 2
source_sha256: cdfde29e8951086bdf99b48118bcb3ceb9998a2e40dfcf5bd23772aa400a7e8a
translation: machine
translated_at: '2026-10-24'
---
# LTX-2.3 inpaint LoRA {#ltx-23-inpaint-lora}

**Ligne de développement :** `project:ltx-2-3-inpaint-lora` · fil `ltx-2-3-inpaint-lora`  
**Dernier événement :** 2026-03-24 · 1 événement daté depuis le 2026-03-24 · **Consulté le :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

LTX-2.3 inpaint LoRA est un ensemble de LoRA communautaires pour le masquage vidéo dans Lightricks/LTX-2.3 : inpainting text-only, inpainting avec référence, et choix du checkpoint selon le respect du prompt ou l'utilisation du masque. — remplace ou ajoute des objets uniquement à l'intérieur de la zone préparée ; — la variante MR2V accepte une référence visuelle ou une référence vide pour le mode text-only ; — il ne s'agit pas de l'IC-LoRA officiel LTX In-Outpainting et pas d'une solution revendiquée pour le face/body swap. Limite : pour MR2V, la taille et la préparation du masque sont critiques ; l'auteur indique que sous FP8 la qualité baisse nettement. Verdict : adapté aux retouches d'objets sur de courtes vidéos, si le workflow reproduit son marquage de couleurs ; pour les visages et l'in/outpainting officiel LTX-2.5, il faut un autre adaptateur.

## Ligne de développement {#development-line}

- **2026-03-24 — Liens de distribution des LoRA LTX enregistrés.** Le 24 mars 2026, cette ligne de développement a enregistré des liens vers un dépôt LTX-LoRAs sur Hugging Face et une page LTX LoRAs sur Civitai. Ces liens indiquent une étape de distribution ou de découverte publique liée au projet, mais l'enregistrement n'établit ni la variante exacte du modèle, ni le comportement d'inpainting, ni la compatibilité, ni la provenance, ni les détails de publication.

## Ce qui a changé {#what-changed}

2026-03-24 — Le LTX-2.3 inpaint LoRA a été présenté comme un workflow prêt à l'emploi pour remplacer des objets, retoucher localement des images et corriger une zone donnée sans regénérer tout le clip. 2026-04-06 — publication de la variante expérimentale MR2V `ltx23_inpaint_masked_r2v_rank32_v1_3000steps.safetensors` : inpainting guidé par référence à l'intérieur du masque, orienté objets, et non face/body swap. 2026-04-08 — le README a corrigé les noms de deux checkpoints text-to-video : les anciens `ltx23_inpaint_rank128...` ont été remplacés par `ltx23_inpaint_masked_t2v_rank128...`.

## Mode d'emploi {#how-to-use-this}

Au 2026-03-24, il convient de traiter les emplacements Hugging Face et Civitai liés comme des sources à examiner et à vérifier avant utilisation, plutôt que de supposer qu'ils fournissent un LoRA d'inpainting LTX-2.3 confirmé ou une revendication de compatibilité particulière.

1. Installer le pipeline LTX-2 via `uv sync --frozen`, télécharger l'ensemble de LoRA et l'encodeur de texte Gemma.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/tree/main>
2. Pour le pipeline natif, charger le fichier voulu via `--lora` et commencer avec un poids de 1.0 ; pour image-to-video, ajouter `--image`.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/tree/main>
3. Pour l'inpainting, ne pas transmettre le masque sur un canal séparé : l'intégrer dans la vidéo de guidage et l'injecter via `LTXVAddGuideMulti` ; le masque est magenta `(255,0,255)`, la zone de référence est chroma-key vert `(0,255,0)`.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md>
4. Pour remplacer un objet avec référence, choisir `ltx23_inpaint_masked_r2v_rank32_v1_3000steps.safetensors` ; pour le mode text-only, utiliser une référence vide et un prompt détaillé.
  — <https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/>

## Bonnes pratiques {#best-practices}

- Comparer d'abord les variantes 2500 steps et 10000 steps : la première privilégie le respect du prompt, la seconde le remplissage du masque ; ne pas considérer un seul checkpoint comme universellement meilleur.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md>
- Pour MR2V, commencer avec Blockify Mask size 8 et élargir le masque si nécessaire : la distribution d'entraînement utilisait un marquage par blocs, et un masque trop serré dégrade le remplacement d'objet.
  — <https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md>
- Ne pas utiliser MR2V comme modèle de face/body swap ; il a été entraîné principalement sur des objets. Vérifier le résultat au minimum en FP8, car la précision plus basse a entraîné, selon l'auteur, une baisse de qualité notable.
  — <https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/>

## Ce qui est remplacé {#superseded-by-this}

- 2026-04-08 : les noms `ltx23_inpaint_rank128_v1_02500steps.safetensors` et `ltx23_inpaint_rank128_v1_10000steps.safetensors` figurant dans les exemples ont été remplacés par `ltx23_inpaint_masked_t2v_rank128_v1_02500steps.safetensors` et `ltx23_inpaint_masked_t2v_rank128_v1_10000steps.safetensors`.
- L'IC-LoRA officiel LTX-2.5 In-Outpainting ne remplace pas automatiquement cet ensemble communautaire : il s'agit d'un checkpoint et d'un workflow distincts.

## Points non établis {#still-unknown}

- Civitai n'a renvoyé aucun contenu lisible de page pendant la recherche ; sa présence n'est donc confirmée que par le lien figurant dans l'événement, sans vérification indépendante des fichiers ou de la version actuels.
- La date de première mise en ligne de chaque fichier Hugging Face n'a pas été obtenue ; le 24.03.2026 confirme la présentation publique du workflow, et non l'horodatage Git d'un poids particulier.
- Le fichier officiel `ltx-2.3-22b-ic-lora-in-outpainting-0.9.safetensors`, utilisé par LTX dans LTX-2.5, n'est pas démontré comme compatible ou interchangeable avec les fichiers communautaires d'Alissonerdx.
- event_findings:[{"event_date":"2026-03-24","finding":"Ce jour-là, l'ensemble a été décrit comme un workflow permettant de supprimer ou remplacer des objets, de retoucher ponctuellement des images et de corriger une seule zone sans regénérer tout le clip.","source_date":"2026-03-24","source_url":"https://www.youtube.com/watch?v=PX3-OqOz6rE"}]
- new_events:[{"date":"2026-04-06","finding":"L'auteur a nommé le fichier MR2V expérimental exact `ltx23_inpaint_masked_r2v_rank32_v1_3000steps.safetensors` ; il effectue un inpainting basé sur une référence à l'intérieur du masque, est orienté objets et n'est pas destiné au face/body swap.","source_date":"2026-04-06","source_url":"https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/"},{"date":"2026-04-08","finding":"Le README a renommé deux checkpoints d'inpainting T2V en variantes `masked_t2v`, corrigeant les noms de fichiers présentés précédemment.","source_date":"2026-04-08","source_url":"https://huggingface.co/Alissonerdx/LTX-LoRAs/commit/345088ffcbda7ea9680bd73e145371e527450ff6"}]

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://huggingface.co/Alissonerdx/LTX-LoRAs/tree/main | Alissonerdx/LTX-LoRAs | 2026-09-05 |
| https://huggingface.co/Alissonerdx/LTX-LoRAs/blob/main/README.md | README.md · Alissonerdx/LTX-LoRAs | 2026-09-05 |
| https://civitai.com/models/2484952/ltx-loras | LTX LoRAs - LTX-2.3 Inpainting | Civitai | 2026-09-05 |
| https://www.youtube.com/watch?v=PX3-OqOz6rE | LTX23 Inpainting Is Here: Alissonerdx Inpaint LoRA + Ready Workflows | 2026-09-05 |
| https://www.reddit.com/r/StableDiffusion/comments/1secygl/inpainting_with_reference_to_ltx23_mr2v/ | Inpainting with reference to LTX-2.3 (MR2V) | 2026-09-05 |
| https://huggingface.co/Alissonerdx/LTX-LoRAs/commit/345088ffcbda7ea9680bd73e145371e527450ff6 | Update README.md · Alissonerdx/LTX-LoRAs | 2026-09-05 |
| https://docs.ltx.io/open-source-model/feature-guides/editing-effects/in-outpainting | Inpainting and Outpainting | LTX Documentation | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:ltx-2-3-inpaint-lora`, fil `ltx-2-3-inpaint-lora`, 1 événement daté du 2026-03-24 au 2026-03-24.
- **Note pratique :** Au 2026-03-24, il convient de traiter les emplacements Hugging Face et Civitai liés comme des sources à examiner et à vérifier avant utilisation, plutôt que de supposer qu'ils fournissent un LoRA d'inpainting LTX-2.3 confirmé ou une revendication de compatibilité particulière.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
