---
title: "LTX-2.3 IC-LoRA Ingredients — LTX-2.3"
category: projects
date: 2026-06-19
tags: [ltx-2-3, ltx-2-3-ic-lora-ingredients, ltx_2_3, project]
aliases: ["LTX-2.3 IC-LoRA Ingredients"]
level: 2
source_sha256: ecffa62cd24e01f93b402c8a894f3c6db7b5d3a19e40ad5fba95cc54c0632c07
translation: machine
translated_at: '2026-10-24'
---
# LTX-2.3 IC-LoRA Ingredients — LTX-2.3 {#ltx-23-ic-lora-ingredients-ltx-23}

**Ligne de développement :** `project:ltx-2-3-ic-lora-ingredients` · fil `ltx-2-3`  
**Dernier événement :** 2026-06-19 · 1 événement daté depuis le 2026-06-19 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

LTX-2.3 IC-LoRA Ingredients est un IC-LoRA destiné aux praticiens de LTX-2.3-22B : il prend en entrée une reference sheet composite sous forme de vidéo statique et génère un nouveau clip à partir d'une description textuelle de l'action. Fonctionnalités : cohérence des personnages, des costumes, des accessoires et du lieu ; séparation entre la description de la feuille et celle de l'action ; utilisation via un workflow IC-LoRA dédié. Bucket d'entraînement de référence : 768×448, 121 images, 24 fps. Verdict : ce n'est pas un module T2V généraliste, ni un outil d'édition de vidéo existante, mais un moyen ciblé de maintenir cohérents les éléments récurrents d'une scène.

## Ligne de développement {#development-line}

- **2026-06-19 — Lightricks a publié une page de modèle LTX-2.3 IC-LoRA Ingredients.** Le 2026-06-19, une page de modèle Hugging Face pour le LTX-2.3-22B IC-LoRA Ingredients de Lightricks a été consignée dans cette ligne de développement. Le lien daté établit l'existence d'un artefact de modèle LTX-2.3 distinct, mais les éléments fournis n'établissent ni ses notes de version, ni ses capacités, ni le workflow recommandé.

## Ce qui a changé {#what-changed}

2026-06-19 — le modèle est apparu dans la branche sous le nom LTX-2.3-22b-IC-LoRA-Ingredients ; la fiche précise qu'il s'agit d'un contrôle par reference sheet pour la version dev de LTX-2.3-22B, avec le fichier `ltx-2.3-22b-ic-lora-ingredients-0.9.safetensors`, un rang de 128 et un checkpoint recommandé à l'étape 12 000.

2026-06-17 — un index tiers date la sortie officielle au 17 juin, et non au 19 juin ; le 19 juin reste la date de l'événement enregistré, et non une date de sortie confirmée.

## Mode d'emploi {#how-to-use-this}

Au 2026-06-19, les praticiens doivent considérer LTX-2.3-22B IC-LoRA Ingredients comme un artefact de modèle LTX-2.3 suivi séparément, et consulter sa page Hugging Face avant de le sélectionner pour un workflow lié aux ingredients.

1. Obtenez l'accès au dépôt gated, téléchargez le LoRA Ingredients ainsi que la base LTX-2.3-22B compatible.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
2. Préparez une reference sheet unique sur fond noir : des panneaux distincts et propres pour les personnages, les accessoires et le lieu ; convertissez la feuille en vidéo statique dont la résolution et les fps correspondent à la sortie, et dont la longueur est d'au moins 121 images.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
3. Dans ComfyUI, chargez le modèle de base LTX-2.3-22B et le LoRA Ingredients via le workflow IC-LoRA/reference, puis envoyez la vidéo statique de la feuille à l'entrée control/reference.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
4. Rédigez le prompt en deux sections : `Reference sheet:` pour le contenu des panneaux et `Generated video:` pour l'action ou le plan.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
5. Pour un démarrage reproductible, utilisez le workflow ComfyUI officiel qui fixe `ltx-2.3-22b-dev.safetensors` et le LoRA Ingredients.
  — <https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/2.3/LTX-2.3_ICLoRA_Ingredients_Single_Stage_Distilled.json>

## Bonnes pratiques {#best-practices}

- Commencez avec une force de LoRA de 1.0 pour valider le pipeline ; la fiche recommande 1.4 comme valeur de travail.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
- Restez dans le bucket d'entraînement 768×448, 121 images, 24 fps ; les autres résolutions, les clips nettement plus longs et l'exécution sans reference sheet sortent de la distribution d'entraînement.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
- Pour les personnages et objets critiques, donnez des panneaux grands et propres ; pour le visage, ajoutez un gros plan frontal et une vue complète de profil, sans placer de texte sur le panneau.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>
- N'utilisez pas un chargeur de LoRA classique s'il ne transmet pas le chemin de la vidéo de référence : il chargera les poids, mais n'appliquera pas le conditionnement par référence.
  — <https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients>

## Remplacé par ce qui suit {#superseded-by-this}

- 2026-06-17 — l'hypothèse selon laquelle Ingredients serait un text-to-video universel ou un éditeur de vidéo existante est fausse : il requiert un conditionnement par reference sheet et génère un nouveau clip.
- 2026-06-17 — la recommandation de fournir un court clip de référence est obsolète : la vidéo statique de référence doit comporter au moins 121 images.

## Points encore inconnus {#still-unknown}

- La fiche officielle, consultée le 2026-09-05, n'affiche pas sa propre date de publication ; la date du 2026-06-17 pour la sortie n'est confirmée que par un index secondaire.
- Aucune source primaire datée n'a été trouvée pour expliquer l'écart entre la date d'événement du 2026-06-19 et la date du 2026-06-17 dans l'index.
- La compatibilité actuelle avec LTX-2.5 n'est pas confirmée : la documentation officielle de LTX avertit que chaque LoRA ne fonctionne qu'avec le modèle sur lequel il a été entraîné.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients | Fiche du modèle Lightricks/LTX-2.3-22b-IC-LoRA-Ingredients | 2026-09-05 |
| https://github.com/Lightricks/ComfyUI-LTXVideo/blob/master/example_workflows/2.3/LTX-2.3_ICLoRA_Ingredients_Single_Stage_Distilled.json | Workflow LTX-2.3 IC-LoRA Ingredients Single Stage Distilled | 2026-09-05 |
| https://github.com/NitishMamadgi/awesome-ltx2.3-ic_lora | Index awesome-ltx2.3-ic_lora | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:ltx-2-3-ic-lora-ingredients`, fil `ltx-2-3`, 1 événement daté du 2026-06-19 au 2026-06-19.
- **Note pratique :** Au 2026-06-19, les praticiens doivent considérer LTX-2.3-22B IC-LoRA Ingredients comme un artefact de modèle LTX-2.3 suivi séparément, et consulter sa page Hugging Face avant de le sélectionner pour un workflow lié aux ingredients.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
