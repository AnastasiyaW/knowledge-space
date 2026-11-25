---
title: "FLUX.2"
category: projects
date: 2025-12-30
tags: [flux, flux-2-development, project]
aliases: ["1.58-bit FLUX", "FLUX", "FLUX.1", "FLUX.2", "FLUX.2 [dev] Turbo"]
level: 3
source_sha256: bc3cabda9ea9570ad8fa128565ffa8e2068cdf8568ff981b33a32e4939392e28
translation: machine
translated_at: '2026-10-24'
---
# FLUX.2 {#flux2}

**Ligne de développement :** `project:flux` · fil `flux-2-development`  
**Dernier événement :** 2025-12-30 · 5 dates depuis 2024-11-07 · **Recherche effectuée :** 2026-09-07 · confiance : moyenne

## Présentation {#what-it-is}

FLUX.2 est la famille de modèles de Black Forest Labs destinée aux équipes utilisant une API, aux développeurs en local et aux pipelines ComfyUI, qui assurent la génération et l'édition au sein d'un même pipeline.
- Texte vers image, édition guidée par texte et composition à partir de plusieurs références.
- [max], [pro] et [flex] pour l'usage via API, avec [dev] et [klein] pour un déploiement en local.
- Typographie, prompts structurés et contrôle des couleurs pour les mises en page de production.

[pro] plafonne le budget à 9 MP pour les entrées et la sortie combinées ; les poids locaux [dev] et [klein] 9B sont soumis à une licence non commerciale, tandis que [klein] 4B est sous licence Apache 2.0.

Choisissez FLUX.2 lorsqu'un même workflow nécessite à la fois des références et l'édition d'images ; ne remplacez pas automatiquement les points d'accès API autonomes de FLUX.1.1.

## Ligne de développement {#development-line}

- **2024-11-07 — FLUX 1.1 Ultra a été publiquement documenté.** Le 2024-11-07, cette ligne de développement a référencé la page de Black Forest Labs consacrée à FLUX 1.1 Ultra ainsi que la route de modèle correspondante sur fal.ai. Ensemble, ces liens datés marquent une étape de documentation et de disponibilité publique de FLUX 1.1 Ultra, dans la lignée qui précède FLUX.2.
- **2024-12-30 — Un article de recherche sur FLUX a été ajouté à la ligne de développement.** Le 2024-12-30, l'article Hugging Face 2412.18653 a été référencé dans cette lignée. Cela conserve une référence de recherche datée dans la lignée FLUX ; les éléments disponibles ne permettent pas d'établir la contribution précise de cet article à une version donnée.
- **2025-11-25 — Un dépôt de modèle de développement FLUX.2 a été référencé.** BFL a publié FLUX.2 [pro] et [flex], introduisant un pipeline unifié de génération et d'édition, une résolution allant jusqu'à 4 MP, des entrées multi-références, des prompts structurés et la typographie.
- **2025-11-27 — Les recommandations de prompting pour FLUX.2 ont été documentées.** Le 2025-11-27, le guide de prompting FLUX.2 de Black Forest Labs a été référencé avec une source associée. Cela fait des recommandations de prompting un élément daté de la ligne de développement publique de FLUX.2 ; le texte de la source liée n'a pas été fourni.
- **2025-12-30 — FLUX.2-dev-Turbo a été référencé avec une démo hébergée.** fal a référencé une démo hébergée annonçant 8 étapes au lieu des 50 habituelles, prenant en charge la génération texte vers image et l'édition.

## Ce qui a changé {#what-changed}

FLUX.2 distingue les modèles hérités FLUX.1, les versions principales FLUX.2 et les adaptateurs tiers.
- **2024-11-07** : FLUX1.1 [pro] Ultra a ajouté une sortie allant jusqu'à 4 MP et un mode RAW, en tant que version de la ligne FLUX.1 et non comme version FLUX.2.
- **2024-12-30** : 1.58-bit FLUX a démontré la quantification 1.58 bit pour FLUX.1-dev comme méthode de recherche, et non comme format de poids FLUX.2.
- **2025-11-25** : BFL a publié FLUX.2 [pro] et [flex] avec un pipeline unifié de génération et d'édition, jusqu'à 4 MP, plusieurs références, des prompts structurés et la typographie.
- **2025-11-25** : Comfy-Org a empaqueté les composants quantifiés de FLUX.2-dev pour ComfyUI comme distribution communautaire, et non comme version de base de BFL.
- **2025-11-27** : les recommandations de BFL ont établi le prompting pour [pro] et [max] sans prompts négatifs, en utilisant des prompts JSON structurés et l'édition multi-références.
- **2025-12-30** : fal/FLUX.2-dev-Turbo a ajouté un adaptateur LoRA tiers pour FLUX.2-dev, annonçant 8 étapes au lieu des 50 habituelles et la prise en charge de la génération texte vers image ainsi que de l'édition.
- **2026-01-15** : BFL a publié les variantes [klein] 4B et 9B Base pour les exécutions interactives en local, la version 4B sous licence Apache 2.0 et la version 9B sous licence FLUX NCL.
- **2026-02-17** : le statut de réussite du webhook de l'API est passé de SUCCESS à Ready.
- **2026-03-03** : les améliorations de qualité de [pro] sont déployées sur flux-2-pro-preview, tandis que flux-2-pro reste un instantané figé pour la reproductibilité.
- **2026-04-23** : la bêta publique de l'inférence LoRA gérée a été ouverte pour [klein] via les points d'accès -finetuned.
- **2026-07-31** : aucune modification vérifiée n'a été enregistrée, car la publication liée était illisible.

## Mode d'emploi {#how-to-use-this}

1. Associez la variante à la tâche : [max] pour la qualité maximale et la recherche d'ancrage, [pro] pour les pipelines commerciaux, [flex] pour la typographie intégrée à l'image, [klein] pour une faible latence et [dev] pour la personnalisation non commerciale. Vérifiez la licence des poids avant d'exécuter les modèles en local.
  — <https://help.bfl.ai/articles/6122710168-which-flux-2-model-should-i-choose>
2. Envoyez les requêtes au point d'accès API BFL choisi, conservez le polling_url renvoyé et récupérez l'asset généré à partir de celui-ci. Le statut Ready marque la réussite ; Error et Failed sont des erreurs terminales.
  — <https://docs.bfl.ai/quick_start/generating_images>
3. Utilisez le point d'accès preview pour évaluer les améliorations du modèle. Sélectionnez un point d'accès épinglé et non preview pour une sortie de production reproductible, et ne mélangez pas les points d'accès au sein d'une même exécution de génération.
  — <https://docs.bfl.ai/quick_start/generating_images>
4. Acceptez les conditions du dépôt sur Hugging Face pour utiliser FLUX.2-dev en local, chargez les poids via Diffusers en bfloat16 sur CUDA, et passez une image avec le prompt pour l'édition.
  — <https://huggingface.co/black-forest-labs/FLUX.2-dev/tree/main>
5. Mettez à jour ComfyUI pour exécuter [klein] 4B en local, sélectionnez un workflow existant de texte vers image ou d'édition, et placez l'encodeur de texte, le modèle de diffusion et le VAE dans les répertoires de modèles spécifiés.
  — <https://docs.comfy.org/zh/tutorials/flux/flux-2-klein>
6. Associez le LoRA Turbo tiers de fal à FLUX.2-dev si la latence est le principal goulot d'étranglement, en utilisant ses sigmas dédiés à 8 étapes. L'exemple publié spécifie 8 étapes et un guidance_scale de 2.5.
  — <https://huggingface.co/fal/FLUX.2-dev-Turbo>

## Bonnes pratiques {#best-practices}

- Structurez les prompts pour [pro] et [max] selon le schéma Sujet + Action + Style + Contexte. Placez les détails essentiels en premier et gardez les descriptions entre 30 et 80 mots.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Évitez totalement les prompts négatifs. Décrivez directement le résultat visé, par exemple « mise au point nette sur toute la surface » plutôt que « aucun flou ».
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Utilisez des prompts JSON pour l'automatisation structurée, en commençant par des structures de schéma de base. Attribuez des codes couleur HEX à des objets individuels plutôt qu'à l'image entière.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Attribuez un rôle explicite à chaque image d'entrée lors de l'édition multi-références. Restez dans le budget total de 9 MP sur [pro], qui permet au maximum 8 images de référence avec une image de sortie de 1 MP.
  — <https://docs.bfl.ai/guides/prompting_guide_flux2>
- Gardez des points d'accès cohérents pendant les évaluations. Sélectionnez preview pour les modifications actuelles du modèle, et choisissez des points d'accès épinglés lorsqu'une sortie reproductible est requise.
  — <https://docs.bfl.ai/quick_start/generating_images>
- Entraînez les adaptateurs LoRA sur Klein Base non distillé, mais déployez Klein distillé pour la génération d'images interactive. Vérifiez les licences séparément : 4B est sous Apache 2.0, tandis que 9B reste sous FLUX NCL.
  — <https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence>

## Remplacé par ceci {#superseded-by-this}

- 2026-02-17 : la gestion des webhooks utilisant status=SUCCESS est obsolète ; vérifiez status=Ready.
- 2026-03-03 : l'hypothèse selon laquelle flux-2-pro suit automatiquement les mises à jour du modèle est obsolète ; utilisez flux-2-pro-preview pour les nouvelles mises à jour, et conservez flux-2-pro pour une sortie reproductible.
- 2026-04-23 : l'API de finetuning de l'ère FLUX.1 a été dépréciée en octobre 2025 ; BFL oriente l'entraînement LoRA en libre-service vers les points d'accès FLUX.2 [klein] -finetuned avec finetune_id et finetune_strength.
- 2024-12-30 : 1.58-bit FLUX ne peut pas servir de guide d'installation pour FLUX.2 ; l'article quantifie FLUX.1-dev.

## Toujours inconnu {#still-unknown}

- Le contenu de la publication du 2026-07-31 n'a pas pu être lu via le miroir fourni ni via l'URL canonique de X ; aucune modification n'est revendiquée.
- Les jalons du 2024-11-07 et du 2024-12-30 décrivent FLUX.1.1 et FLUX.1-dev plutôt que FLUX.2 ; ils représentent une lignée apparentée plutôt qu'une piste de version unique.
- La qualité et la compatibilité de FLUX.2 [dev] Turbo reposent uniquement sur la fiche du modèle fal ; nous n'avons pas vérifié de benchmarks indépendants.
- Une documentation officielle en chinois existe pour ComfyUI, mais nous n'avons pas vérifié l'exécution locale sur du matériel spécifique.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://blackforestlabs.ai/flux-1-1-ultra/ | Introducing FLUX1.1 [pro] Ultra and Raw Modes | Black Forest Labs | 2026-09-04 |
| https://huggingface.co/papers/2412.18653 | 1.58-bit FLUX | Hugging Face Papers | 2026-09-04 |
| https://huggingface.co/Comfy-Org/flux2-dev | Comfy-Org/flux2-dev | Hugging Face | 2026-09-04 |
| https://bfl.ai/blog/flux-2 | FLUX.2: Frontier Visual Intelligence | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/guides/prompting_guide_flux2 | Prompting Guide - FLUX.2 [pro] & [max] | Black Forest Labs | 2026-09-04 |
| https://huggingface.co/fal/FLUX.2-dev-Turbo | FLUX.2 [dev] Turbo LoRA | fal | 2026-09-04 |
| https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence | FLUX.2 [klein]: Towards Interactive Visual Intelligence | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/release-notes | Release Notes | Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/quick_start/generating_images | Image Generation with Text Prompts | Black Forest Labs | 2026-09-04 |
| https://help.bfl.ai/articles/6122710168-which-flux-2-model-should-i-choose | Which FLUX.2 model should I choose? | Black Forest Labs Knowledge Base | 2026-09-04 |
| https://huggingface.co/black-forest-labs/FLUX.2-dev/tree/main | black-forest-labs/FLUX.2-dev at main | Hugging Face | 2026-09-04 |
| https://docs.comfy.org/zh/tutorials/flux/flux-2-klein | ComfyUI Flux.2 Klein 4B 指南 | ComfyUI | 2026-09-04 |
| https://bfl.ai/models/flux-2 | FLUX.2 - Next Generation Image Generation | Black Forest Labs | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:flux`, fil `flux-2-development`, 5 événements datés du 2024-11-07 au 2025-12-30.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
