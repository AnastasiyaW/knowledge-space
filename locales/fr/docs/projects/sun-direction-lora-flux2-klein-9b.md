---
title: "Sun Direction LoRA Flux 2 Klein 9B — LoRA Flux 2 Klein"
category: projects
date: 2026-07-03
tags: [flux2-klein-loras, project, sun-direction-lora-flux2-klein-9b]
aliases: ["Sun Direction LoRA Flux 2 Klein 9B"]
level: 2
source_sha256: 8c420eb60d9d31d8d379c84b6f4f1b4c755df0b838587955d776ae08338c0bce
translation: machine
translated_at: '2026-10-24'
---
# Sun Direction LoRA Flux 2 Klein 9B — LoRA Flux 2 Klein {#sun-direction-lora-flux-2-klein-9b-flux-2-klein-loras}

**Ligne de développement :** `project:sun-direction-lora-flux2-klein-9b` · fil `flux2-klein-loras`  
**Dernier événement :** 2026-07-03 · 1 daté depuis le 2026-07-03 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Sun Direction LoRA Flux 2 Klein 9B est un LoRA image-à-image de 331 Mo destiné aux utilisateurs de FLUX.2 [klein] 9B. Il modifie la position apparente du soleil dans les photographies d'extérieur.

- Élévation et rotation du soleil : règle l'angle par rapport à la caméra.
- Sphère d'éclairage de référence : conditionne la modification à partir d'une sphère rendue.
- Passe préparatoire de ciel couvert : supprime les ombres existantes avant le rééclairage.

## Ligne de développement {#development-line}

- **2026-07-03 — Référence de la ressource Sun Direction LoRA Flux 2 Klein 9B enregistrée.** Le 2026-07-03, le fil Flux 2 Klein LoRAs a renvoyé vers son dépôt Hugging Face. Nous ne disposons pas encore du corps de message ni de la fiche du modèle ; nous ne formulons donc aucune affirmation sur la version publiée, la configuration d'entraînement, la licence ou les performances.

## Ce qui a changé {#what-changed}

2026-07-03 — une démonstration exécutable de FLUX.2 [klein] 9B a documenté le flux de travail de rééclairage en deux passes utilisant le conditionnement par sphère pour l'adaptateur v1.

## Mode d'emploi {#how-to-use-this}

Consultez le dépôt Hugging Face daté du 2026-07-03 avant utilisation. Nous ne disposons d'aucune affirmation confirmée concernant la compatibilité, les déclencheurs, la licence ou la qualité.

1. Mettez à jour ComfyUI, puis installez le modèle de diffusion FLUX.2 [klein] 9B, l'encodeur de texte 9B et le VAE FLUX.2 requis pour un flux de travail de modification d'image.
  — <https://docs.comfy.org/tutorials/flux/flux-2-klein>
2. Téléchargez le LoRA v1 et utilisez le flux de travail fourni ; utilisez le nœud Sphere Light Render ou la scène Blender incluse pour créer la référence de sphère éclairée.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
3. Si l'entrée présente déjà une lumière directionnelle marquée, créez d'abord une version en ciel couvert avec moins d'ombres ; utilisez cette image et l'image de sphère comme références latentes pour la passe de rééclairage.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
4. Incluez `match the sun direction from the reference` dans le prompt, puis ajoutez après celui-ci les instructions de scène, par exemple les conditions de ciel.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>

## Bonnes pratiques {#best-practices}

- Utilisez des photos d'extérieur et considérez qu'un résultat en intérieur n'est pas pris en charge plutôt que comme une configuration défectueuse.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
- Ne sautez la préparation en ciel couvert que si l'entrée ne présente déjà pas de direction d'ombre claire.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
- Gardez la graine fixe lors du rendu d'une vidéo accélérée de rééclairage afin de réduire le scintillement.
  — <https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B>
- Mettez à jour ComfyUI si le flux de travail fourni comporte des nœuds principaux manquants.
  — <https://docs.comfy.org/tutorials/flux/flux-2-klein>

## Remplacé par ceci {#superseded-by-this}

- Aucun élément marqué obsolète pour le moment.

## Points encore inconnus {#still-unknown}

- Aucun poids v2 public, note de version, benchmark ni jeu de données d'entraînement n'a été publié. La fiche de la v1 indique seulement que la v2 est en cours de développement.
- L'auteur ne publie ni plage validée d'intensité du LoRA ni configuration matérielle requise pour cet adaptateur.
- L'entrée de développement du 2026-07-03 correspond à une démonstration exécutable du même jour ; les poids v1 et les flux de travail du dépôt ont été versionnés le 2026-06-29.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B | Sun Direction LoRA Flux 2 Klein 9B v1 | 2026-09-05 |
| https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B/tree/main | Fichiers du dépôt Sun-Direction-Lora-Flux2Klein9B | 2026-09-05 |
| https://huggingface.co/eric-venti-seeds/Sun-Direction-Lora-Flux2Klein9B/commits/main | Historique des commits de Sun-Direction-Lora-Flux2Klein9B | 2026-09-05 |
| https://huggingface.co/spaces/linoyts/sun-direction-flux2-klein/commit/36259bd5c170a583fac16461a64b6ebc05f2ab84 | Démonstration Sun Direction LoRA (FLUX.2 klein 9B) | 2026-09-05 |
| https://docs.comfy.org/tutorials/flux/flux-2-klein | Guide ComfyUI Flux.2 Klein | 2026-09-05 |

## Fiche de synthèse pour agent {#agent-brief}

- **Sujet :** `project:sun-direction-lora-flux2-klein-9b`, fil `flux2-klein-loras`, 1 événement daté du 2026-07-03 → 2026-07-03.
- **Remarque pratique :** à partir du 2026-07-03, inspectez la ressource Hugging Face liée avant toute utilisation ; nous n'établissons aucune affirmation de compatibilité, de déclencheurs, de licence ou de qualité.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
