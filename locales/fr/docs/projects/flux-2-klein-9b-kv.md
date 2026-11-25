---
title: "FLUX.2 [Klein] KV - 9B — Sortie du modèle et inférence locale"
category: projects
date: 2026-03-13
tags: [flux-2-klein-9b-kv, image_generation, model-release-and-local-inference, project]
aliases: ["FLUX.2 [Klein] KV - 9B"]
level: 2
source_sha256: 4db475c685d746015e7f0c3e93dec0dc9380b137476fcf1b8cd6d542eccc8eae
translation: machine
translated_at: '2026-10-24'
---
# FLUX.2 [Klein] KV - 9B — Sortie du modèle et inférence locale {#flux2-klein-kv-9b-model-release-and-local-inference}

**Ligne de développement :** `project:flux-2-klein-9b-kv` · fil `model-release-and-local-inference`  
**Dernier événement :** 2026-03-13 · 1 événement daté depuis le 2026-03-13 · **Recherche :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

FLUX.2 [klein] 9B-KV est un modèle de type flow de 9B destiné à l'édition locale ou via API, lorsque le FLUX.2 [klein] 9B standard consacre du temps à retraiter les mêmes références. — text-to-image ; — édition d'une seule image ; — édition multi-références avec cache KV ; — BF16 et variante officielle FP8, ainsi que des quantifications GGUF tierces. Repères : modèle flow de 9B, encodeur de texte Qwen3 de 8B, 4 étapes ; la variante officielle BF16 nécessite environ 29 Go de VRAM et est prévue pour une RTX 5090 ou plus. Conclusion : choisissez-le pour l'édition itérative multi-références, et non pour accélérer le text-to-image pur.

## Ligne de développement {#development-line}

- **2026-03-13 — Disponibilité du modèle FLUX.2 Klein 9B KV et ressources pour un usage local.** L'étape zéro calcule les K/V des références, les étapes 1 à 3 réutilisent le cache. La fiche officielle annonce jusqu'à 2,5× pour l'édition multi-références ; un tableau plus détaillé montre une dépendance au nombre de références et à la résolution, de 1,21× à 2,66×.

## Évolutions {#what-changed}

Le 2026-01-15, Black Forest Labs a publié la famille FLUX.2 [klein] : le modèle 9B combinait déjà text-to-image, édition à référence unique et édition multi-références dans un modèle distillé à 4 étapes. Le 2026-03-12, le dépôt officiel d'inférence a reçu le commit « FLUX.2 [klein] KV » : un chemin distinct de mise en cache des références, le choix `flux.2-klein-9b-kv` dans la CLI et un tableau d'accélérations. Le 2026-03-13, FLUX.2 [klein] 9B-KV est sorti comme variante 9B exacte avec cache K/V : l'étape zéro calcule les K/V des références, les étapes 1 à 3 réutilisent le cache. La fiche officielle annonce jusqu'à 2,5× pour l'édition multi-références ; un tableau plus détaillé montre une dépendance au nombre de références et à la résolution, de 1,21× à 2,66×.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-13, les praticiens doivent évaluer cette ligne via le checkpoint ou la démo Hugging Face liés, et utiliser les ressources GGUF et workflows ComfyUI liées pour choisir une voie d'inférence locale.

1. Acceptez les conditions du modèle protégé et de la FLUX Non-Commercial License, puis téléchargez le checkpoint officiel BF16 ou la variante FP8.
  — <https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv>
2. Pour une voie Python locale, mettez à jour Diffusers depuis GitHub, chargez `Flux2KleinKVPipeline`, placez-le sur CUDA en bfloat16 et commencez avec 1024×1024 et 4 inference steps.
  — <https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv>
3. Pour la CLI officielle, définissez `KLEIN_9B_KV_MODEL_PATH`, lancez `scripts/cli.py --model_name flux.2-klein-9b-kv`, indiquez une ou plusieurs `input_images`, puis l'instruction textuelle.
  — <https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md>
4. Pour ComfyUI, avec un budget disque et VRAM plus réduit, vous pouvez prendre un GGUF tiers, le placer dans `ComfyUI/models/unet`, installer ComfyUI-GGUF et importer un workflow compatible ; il s'agit d'une voie communautaire, et non du runtime officiel de BFL.
  — <https://huggingface.co/QuantStack/FLUX.2-Klein-9B-KV-GGUF>
5. Pour un lancement cloud, utilisez le `flux-2-klein-9b-preview` actuel pour les dernières améliorations KV, ou le `flux-2-klein-9b` figé lorsque la reproductibilité compte ; interrogez l'`polling_url` renvoyée.
  — <https://docs.bfl.ai/quick_start/generating_images>

## Bonnes pratiques {#best-practices}

- Ne comptez sur l'accélération que pour les tâches conditionnées par image : le cache conserve les K/V des images de référence uniquement.
  — <https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md>
- Vérifiez le gain pour votre nombre de références et votre résolution : le tableau officiel donne 2,66× pour quatre références en 512×512, mais 1,85× en 1440×1440.
  — <https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md>
- Rédigez une instruction descriptive détaillée : FLUX.2 [klein] ne dispose pas de prompt upsampling, donc les objets importants, les modifications et les propriétés à préserver doivent être nommés explicitement.
  — <https://docs.bfl.ai/flux_2/flux2_overview>
- Ne reportez pas l'exigence de 13 Go de VRAM de Klein 4B sur le 9B-KV : pour le 9B-KV officiel, le repère indiqué est d'environ 29 Go de VRAM.
  — <https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv>
- Pour des résultats de production stables, choisissez un endpoint API non preview ; la preview est destinée aux dernières modifications des poids.
  — <https://docs.bfl.ai/flux_2/flux2_overview>

## Ce qui est remplacé {#superseded-by-this}

- 2026-03-12 — l'activation manuelle du cache KV dans la CLI officielle n'est pas nécessaire : le choix de `flux.2-klein-9b-kv` active automatiquement le chemin KV.
- 2026-03-13 — pour l'édition multi-références, le FLUX.2 [klein] 9B standard n'est plus le choix de faible latence privilégié ; le 9B-KV conserve ses capacités et supprime le retraitement des références.
- 2026-09-05 — il n'est pas possible de considérer la variante preview de l'API comme reproductible : la documentation actuelle distingue le `flux-2-klein-9b-preview`, mutable, du `flux-2-klein-9b`, figé.

## Points non vérifiés {#still-unknown}

- Aucune exécution indépendante n'a été réalisée : les accélérations annoncées sont des mesures officielles, mais la fiche ne détaille pas le banc d'essai complet et ne remplace pas une mesure sur vos propres références et votre propre résolution.
- BF16, FP8 et GGUF ne sont pas des voies runtime interchangeables : la conversion GGUF, ComfyUI-GGUF et le workflow YarvixPA relèvent d'une intégration tierce et n'ont ici aucune validation E2E indépendante.
- La recherche en chinois a donné un guide ComfyUI secondaire, mais pas de source primaire ; ses recommandations n'ont pas été considérées comme une compatibilité officielle.
- Rien n'indique que les liens concernent des modèles différents : BF16 et FP8 sont les variantes officielles d'un même 9B-KV, et le GGUF est une quantification tierce directe de cette même base.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv | black-forest-labs/FLUX.2-klein-9b-kv · Hugging Face | 2026-09-05 |
| https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-kv-fp8 | black-forest-labs/FLUX.2-klein-9b-kv-fp8 · Hugging Face | 2026-09-05 |
| https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md | FLUX.2 [klein] 9B KV Cache — documentation officielle d'inférence | 2026-09-05 |
| https://github.com/black-forest-labs/flux2/commits/main/docs/flux2_klein_kv_cache.md | Historique de flux2_klein_kv_cache.md — commit « FLUX.2 [klein] KV », 2026-03-12 | 2026-09-05 |
| https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence | FLUX.2 [klein]: Towards Interactive Visual Intelligence — Black Forest Labs, 2026-01-15 | 2026-09-05 |
| https://docs.bfl.ai/flux_2/flux2_overview | FLUX.2 Overview — documentation Black Forest Labs | 2026-09-05 |
| https://docs.bfl.ai/quick_start/generating_images | Image Generation with Text Prompts — documentation Black Forest Labs | 2026-09-05 |
| https://huggingface.co/QuantStack/FLUX.2-Klein-9B-KV-GGUF | QuantStack/FLUX.2-Klein-9B-KV-GGUF · Hugging Face | 2026-09-05 |
| https://github.com/YarvixPA/ComfyUI-YarvixPA/blob/main/example_workflows/YarvixPA%20-%20Flux2%209B%20KV%20-%20GGUF.json | YarvixPA — workflow Flux2 9B KV GGUF | 2026-09-05 |
| https://www.stablediffusiontutorials.com/2026/03/flux2-klein-9b-kv.html | Flux2 Klein 9B KV (BF16/FP8/GGUF) : Improved Multi-Editing, 2026-03-13 | 2026-09-05 |
| https://www.runcomfy.com/zh-CN/comfyui-workflows/flux-2-klein-9b-kv-image-edit-in-comfyui-precision-prompt-editing | Guide ComfyUI d'édition d'image FLUX.2 Klein 9B KV, chinois simplifié | 2026-09-05 |

## Briefing agent {#agent-brief}

- **Sujet :** `project:flux-2-klein-9b-kv`, fil `model-release-and-local-inference`, 1 événement daté du 2026-03-13 au 2026-03-13.
- **Note pratique :** À partir du 2026-03-13, les praticiens doivent évaluer cette ligne via le checkpoint ou la démo Hugging Face liés, et utiliser les ressources GGUF et workflows ComfyUI liées pour choisir une voie d'inférence locale.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
