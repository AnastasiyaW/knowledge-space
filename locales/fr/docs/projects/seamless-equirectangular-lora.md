---
title: "LoRA LTX-2.3 Seamless-Equirectangular — publication de la LoRA Seamless-Equirectangular"
category: projects
date: 2026-07-07
tags: [project, seamless-equirectangular-lora, seamless-equirectangular-lora-release]
aliases: ["Seamless-Equirectangular LTX-2.3 LoRA"]
level: 2
source_sha256: 644814fd98da6afc7dc664c3d06d991abe915e2c327509fbb80100339ae86610
translation: machine
translated_at: '2026-10-24'
---
# LoRA LTX-2.3 Seamless-Equirectangular — publication de la LoRA Seamless-Equirectangular {#seamless-equirectangular-ltx-23-lora-seamless-equirectangular-lora-release}

**Ligne de développement :** `project:seamless-equirectangular-lora` · fil `seamless-equirectangular-lora-release`  
**Dernier événement :** 2026-07-07 · 1 événement daté depuis le 2026-07-07 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

Seamless-Equirectangular LTX-2.3 LoRA : un adaptateur de rang 128 permettant de générer des vidéos equirectangulaires à 360° dans LTX-2.3 via ComfyUI.

Fonctionnalités :

- text-to-video avec le mot déclencheur `Equirectangular` ;
- suppression de la couture grâce au circular VAE et au décalage latent par étape (per-step latent roll) ;
- traitement des pôles via EquiRoPE et CFG géométrique ;
- outpainting d'une vidéo classique vers 360° via un workflow VR-Outpaint dédié.

Limite : la LoRA a été entraînée sur 15 000 étapes ; selon l'auteur, LTX-2.3 de base sans cette LoRA ne produit pas de sortie equirectangulaire, et aucun fournisseur d'inférence hébergée n'est disponible.

Verdict : il s'agit d'un pipeline ComfyUI local et pratique, et non d'un modèle cloud autonome.

## Ligne de développement {#development-line}

- **2026-07-07 — Ressources publiques associées à la LoRA Seamless-Equirectangular LTX-2.3.** LoRA Seamless-Equirectangular LTX-2.3 et pack de nœuds ComfyUI. La fiche du modèle précise les paramètres de l'adaptateur : rang 128, 15 000 étapes, mot déclencheur `Equirectangular`. Le dépôt précise que la LoRA gère la représentation equirectangulaire, tandis que le circular VAE et le décalage par étape traitent la couture. Les README actuels ajoutent la prise en charge de Krea2 et de MiniMax H3, mais les pages primaires ne fournissent pas de date fiable pour ces extensions ; elles ne sont donc pas rattachées à un événement daté distinct.

## Modifications {#what-changed}

2026-07-07 — publication d'un ensemble lié : LoRA Seamless-Equirectangular LTX-2.3 et pack de nœuds ComfyUI. La fiche du modèle précise les paramètres de l'adaptateur : rang 128, 15 000 étapes, mot déclencheur `Equirectangular`. Le dépôt précise que la LoRA gère la représentation equirectangulaire, tandis que le circular VAE et le décalage par étape traitent la couture. Les README actuels ajoutent la prise en charge de Krea2 et de MiniMax H3, mais les pages primaires ne fournissent pas de date fiable pour ces extensions ; elles ne sont donc pas rattachées à un événement daté distinct.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-07-07, les praticiens devraient considérer la LoRA Hugging Face et l'extension ComfyUI liées comme un point de départ couplé pour évaluer les workflows equirectangulaires sans couture avec LTX-2.3.

1. Installez ComfyUI-Seamless-Equirectangular dans le répertoire custom nodes de ComfyUI, puis redémarrez ComfyUI.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular>
2. Chargez l'adaptateur comme une LoRA LTX-2.3 classique et ajoutez le mot `Equirectangular` au prompt.
  — <https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA>
3. Ouvrez le workflow T2V joint et utilisez le pack de nœuds : il ajoute EquiRoPE, CFG géométrique, per-step roll, circular VAE et wrapped noise.
  — <https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA>
4. Pour transformer une vidéo en perspective en 360°, utilisez le workflow VR-Outpaint dédié et ComfyUI-VR-Outpaint-Tools ; cette LoRA s'applique conjointement à la VR-Outpaint IC-LoRA.
  — <https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA>

## Bonnes pratiques {#best-practices}

- Pour LTX, commencez par LoRA + per-step roll + circular VAE : les correctifs de position améliorent la géométrie, mais ne remplacent pas la LoRA.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>
- En présence d'objets répétitifs ou symétriques, n'utilisez pas `dual_average` ; passez à `random_per_step` ou désactivez le roll.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>
- Pour les panoramiques rapides, réglez `start_percent` entre 0.2 et 0.3 afin de fixer d'abord la structure de la scène, puis de traiter la couture.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>
- Ne considérez pas le seam blend latent ou image comme une correction des objets non alignés : c'est uniquement un repli cosmétique étroit pour une couture chromatique résiduelle.
  — <https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points inconnus {#still-unknown}

- Les pages primaires ne fournissent pas de dates fiables pour les extensions ultérieures Krea2 et MiniMax H3 ; elles ne sont donc pas documentées comme de nouveaux événements datés.
- Les affirmations sur la qualité, l'usage en production et la comparaison des composants viennent de l'auteur du projet ; les sources consultées ne contiennent aucune évaluation indépendante et reproductible.
- Le lien enregistré n'a pas été utilisé : la page ne s'est pas ouverte avec l'accès web disponible.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://huggingface.co/TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA | TheBurgstall/Seamless-Equirectangular-LTX2.3-LoRA — fiche du modèle | 2026-09-05 |
| https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular | Burgstall-labs/ComfyUI-Seamless-Equirectangular | 2026-09-05 |
| https://github.com/Burgstall-labs/ComfyUI-Seamless-Equirectangular/blob/main/README.md | README de ComfyUI-Seamless-Equirectangular | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:seamless-equirectangular-lora`, fil `seamless-equirectangular-lora-release`, 1 événement daté du 2026-07-07 au 2026-07-07.
- **Note pratique :** à partir du 2026-07-07, les praticiens devraient considérer la LoRA Hugging Face et l'extension ComfyUI liées comme un point de départ couplé pour évaluer les workflows equirectangulaires sans couture avec LTX-2.3.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
