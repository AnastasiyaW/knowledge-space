---
title: "Ultra Real - Klein 9b — Klein 9b"
category: projects
date: 2026-03-23
tags: [klein-9b, project, ultra-real-klein-9b]
aliases: ["Ultra Real - Klein 9b"]
level: 2
source_sha256: 1b404e90ad930bd14749904192cc4f94a56fb6cb0c8f6785f153d42485b99527
translation: machine
translated_at: '2026-10-24'
---
# Ultra Real - Klein 9b — Klein 9b {#ultra-real-klein-9b-klein-9b}

**Ligne de développement :** `project:ultra-real-klein-9b` · fil `klein-9b`  
**Dernier événement :** 2026-03-23 · 1 événement daté depuis le 2026-03-23 · **Recherche :** 2026-09-05 · confiance : moyenne

## Présentation {#what-it-is}

Ultra Real - Klein 9b est un LoRA destiné aux utilisateurs de FLUX.2 Klein 9B dans ComfyUI.

- Génération de portraits : crée des portraits.
- Édition d'image : modifie des images existantes.
- Upscale : restaure d'anciennes images.

Les versions vont de V1 à V4 : V3 produit une texture plus délicate, tandis que V4 gère le détaillage.
Le LoRA n'est pas un modèle de base et nécessite un workflow Klein 9B compatible.
Pour une peau naturelle, commencez par V3 et n'ajoutez V4 que pour une passe de détaillage.

## Ligne de développement {#development-line}

- **2026-03-23 — Ultra Real - Klein 9b relié à une page de modèle Civitai et à des workflows ComfyUI.** V2 revendique une texture de peau plus naturelle, avec une meilleure préservation des tons et de l'éclairage.

## Ce qui a changé {#what-changed}

- 2026-03-23 — Ultra Real - Klein 9b était disponible sous forme de LoRA V1/V2 pour FLUX.2 Klein 9B ; V2 revendiquait une texture de peau plus naturelle et une meilleure préservation des tons et de l'éclairage.
- 2026-04-10 — La fiche du modèle a été mise à jour pour présenter la ligne V1–V4 ; V3 était décrit comme une texture plus délicate sans taches de rousseur supplémentaires, et V4 comme un mode de détaillage distinct.
- 2026-04-13 — La fiche actuelle indique FLUX.2 Klein 9B comme modèle de base et V1–V4 comme variantes d'une même ligne de LoRA.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-23, utilisez la page de modèle Civitai et le dépôt de workflows ComfyUI liés comme points de référence datés pour évaluer Ultra Real - Klein 9b. Les liens seuls ne permettent pas de vérifier une version spécifique, la compatibilité d'un workflow ou une affirmation de performance.

1. Installez les composants compatibles FLUX.2 Klein 9B dans les dossiers ComfyUI correspondants : le modèle de diffusion, l'encodeur de texte Qwen 3 8B et le VAE flux2.
  — <https://github.com/Comfy-Org/docs/blob/main/ja/tutorials/flux/flux-2-klein.mdx>
2. Chargez Ultra Real - Klein 9b dans l'emplacement LoRA du workflow Klein 9B ; pour l'édition d'image avec V3, commencez à un poids de 0,6, et pour V4 à 0,55.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
3. Pour l'édition, utilisez une instruction qui préserve le visage, l'expression, la morphologie, la pose et la composition ; pour V2, le poids cible publié est de 0,5.
  — <https://tensor.art/models/981017447823890853>
4. Pour la génération à partir de texte, commencez à un poids de 0,7–0,8 et décrivez la scène comme une photographie ; le poids cible publié pour V2 est de 0,7.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>

## Bonnes pratiques {#best-practices}

- N'utilisez pas V4 comme LoRA de style universel : la description le limite au détaillage ; pour une génération standard, utilisez un prompt textuel ou un autre LoRA.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
- Ne reprenez pas les réglages de V1 sans les tester : V1 peut exagérer les pores et les taches de rousseur, ou modifier l'éclairage et le ton de peau ; V3 revendique un résultat plus délicat.
  — <https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09>
- Pour l'édition d'image, demandez explicitement au modèle de conserver les traits, l'expression, la pose et la composition, afin que le LoRA ne modifie pas davantage que la texture de la peau.
  — <https://tensor.art/models/981017447823890853>

## Éléments remplacés {#superseded-by-this}

- 2026-04-10 — V1 n'est plus le mode recommandé pour une peau naturelle : la fiche actuelle décrit V3 comme une texture plus délicate et V4 comme une passe de détaillage dédiée.
- 2026-04-10 — La recommandation d'utiliser le même LoRA pour la génération et le détaillage est obsolète : V4 est désormais explicitement réservé au détaillage.

## Points non résolus {#still-unknown}

- La page Civitai directe et le dépôt de workflows n'étaient pas accessibles en téléchargement exploitable lors de la revue ; les réglages sont confirmés par des miroirs et des pages de publication, et non par les fichiers de workflow source.
- La fiche SeaArt actuelle indique une date d'annonce du 2026-03-13, une date de mise à jour du 2026-04-10 et une date de publication du 2026-04-13, mais ne donne aucune date de sortie distincte pour V3 et V4 ; nous ne pouvons pas les dater plus précisément.
- L'identifiant Civitai 2462105 apparaît plus tard sur certains miroirs pour UltraReal - Krea2, Klein9b également ; rien ne prouve qu'il s'agit d'une continuation du même LoRA Klein 9B plutôt que d'une réutilisation de la fiche.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://civitai.com/models/2462105/ultra-real-klein-9b | Ultra Real - Klein 9b — page de modèle Civitai | 2026-09-05 |
| https://github.com/vizsumit/comfyui-workflows | vizsumit/comfyui-workflows | 2026-09-05 |
| https://civarchive.com/seaart/models/0b4b3278ab4fd5b6471cd029ef88fc09/versions/4eaaed353d71f3ae09efa4411c954877 | Ultra Real - Klein 9b V2 — CivArchive | 2026-09-05 |
| https://www.seaart.ai/indo/models/detail/0b4b3278ab4fd5b6471cd029ef88fc09 | Ultra Real - Klein 9b — page de modèle SeaArt | 2026-09-05 |
| https://tensor.art/models/981017447823890853 | Ultra Real - Klein 9b V1 — Tensor.Art | 2026-09-05 |
| https://github.com/Comfy-Org/docs/blob/main/ja/tutorials/flux/flux-2-klein.mdx | Tutoriel ComfyUI FLUX.2 Klein | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:ultra-real-klein-9b`, fil `klein-9b`, 1 événement daté du 2026-03-23 au 2026-03-23.
- **Note pratique :** À partir du 2026-03-23, les praticiens doivent utiliser la page de modèle Civitai et le dépôt de workflows ComfyUI liés comme points de référence datés pour évaluer Ultra Real - Klein 9b ; les liens seuls ne permettent pas de vérifier une version spécifique, la compatibilité d'un workflow ou une affirmation de performance.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
