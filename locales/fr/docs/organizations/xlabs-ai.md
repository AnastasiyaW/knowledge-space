---
title: "XLabs AI — Conditionnement FLUX et intégrations ComfyUI"
category: organizations
date: 2024-08-21
tags: [flux-conditioning-and-comfyui-integrations, organization, xlabs-ai, xlabs_flux_controlnet, xlabs_flux_ip_adapter]
aliases: ["XLabs AI"]
level: 3
source_sha256: 3998dee9731d8ffbe4018d96e9059fb85240bba983396d73467827175ce04c96
translation: machine
translated_at: '2026-10-24'
---
# XLabs AI — Conditionnement FLUX et intégrations ComfyUI {#xlabs-ai-flux-conditioning-and-comfyui-integrations}

**Ligne de développement :** `organization:xlabs-ai` · fil `flux-conditioning-and-comfyui-integrations`  
**Dernier événement :** 2024-08-21 · 3 événements datés depuis le 2024-08-14 · **Recherche effectuée :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

XLabs AI publie des extensions FLUX.1-dev pour ComfyUI. Elles apportent un contrôle structurel et un conditionnement par image de référence lorsque le prompt seul ne suffit pas.

- ControlNet : contours Canny, profondeur Midas et cartes de lignes HED.
- IP-Adapter v2 : conditionnement par image de référence.
- x-flux-comfyui : nœuds et workflows d'exemple.

## Ligne de développement {#development-line}

- **2024-08-14 — XLabs AI a relié une collection ControlNet FLUX à ComfyUI.** Le 2024-08-14, XLabs AI a associé une collection ControlNet FLUX sur Hugging Face à sa base de code x-flux-comfyui. Cela a ouvert une voie d'intégration ControlNet pour FLUX dans ComfyUI. Les liens ne détaillent ni les modèles individuels ni les notes de version.
- **2024-08-19 — XLabs AI a documenté trois variantes ControlNet FLUX v3.** Le 2024-08-19, XLabs AI a publié les pages de modèles FLUX ControlNet HED v3, Depth v3 et Canny v3. La collection compte ainsi trois variantes de conditionnement nommées. Les pages ne fournissent ni benchmarks, ni généalogie des versions, ni précisions sur les workflows.
- **2024-08-21 — XLabs AI a ajouté une voie d'intégration IP-Adapter FLUX.** Le 2024-08-21, XLabs AI a combiné une page de modèle FLUX IP-Adapter, le dépôt x-flux-comfyui et un workflow OpenArt. Cela ajoute un conditionnement par image de référence à côté de ControlNet. Les éléments disponibles ne confirment ni les paramètres d'exécution ni les résultats opérationnels.

## Ce qui a changé {#what-changed}

Le 2024-08-14, XLabs AI a ajouté une collection ControlNet FLUX.1-dev et des nœuds personnalisés pour ComfyUI.
Le 2024-08-19, la ligne s'est scindée en points de contrôle dédiés Canny v3, Depth v3 et HED v3 pour ComfyUI, en 1024×1024.
Le 2024-08-21, XLabs AI a ajouté FLUX IP-Adapter v1 pour le conditionnement par image de référence dans la même pile.
Nous avons vérifié les dépôts le 2026-09-04. La fiche v1 indique flux-ip-adapter-v2 comme version plus récente. Ce modèle v2 comporte davantage d'étapes d'entraînement, conserve le rapport d'aspect et constitue le point de départ actuel de XLabs. Le dépôt des nœuds personnalisés ne montre aucune modification de la branche principale après le 2024-10-30.

## Mode d'emploi {#how-to-use-this}

Considérez les variantes ControlNet et le conditionnement IP-Adapter par image de référence comme deux voies distinctes à partir du 2024-08-21. Partez de l'intégration ComfyUI plutôt que d'attendre un workflow unique et commun.

1. Installez x-flux-comfyui via ComfyUI Manager, ou clonez-le dans ComfyUI/custom_nodes, exécutez python setup.py, puis redémarrez ComfyUI.
  — <https://github.com/XLabs-AI/x-flux-comfyui/blob/main/Guide.md>
2. Pour le conditionnement structurel, installez la dépendance du préprocesseur ControlNet. Placez les poids Canny, Depth ou HED v3 choisis dans ComfyUI/models/xlabs/controlnets, puis actualisez la liste des modèles.
  — <https://github.com/XLabs-AI/x-flux-comfyui>
3. Commencez par canny_workflow.json, depth_workflow.json ou hed_workflow.json, en 1024×1024.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-collections>
4. Pour les images de référence, utilisez flux-ip-adapter-v2. Placez Clip-L dans ComfyUI/models/clip_vision et l'adaptateur dans ComfyUI/models/xlabs/ipadapters, puis utilisez Load Flux IPAdapter et Apply Flux IPAdapter.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter-v2>
5. Ajustez la force IP si le respect de la référence est faible. Utilisez CUDA pour le chargeur CLIP-ViT uniquement si la VRAM le permet.
  — <https://github.com/XLabs-AI/x-flux-comfyui/blob/main/Guide.md>

## Bonnes pratiques {#best-practices}

- Adaptez la condition à la tâche : Canny pour les contours, Depth pour la géométrie et HED pour la structure en lignes. Ne les traitez pas comme des ControlNet génériques interchangeables.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-collections>
- Testez d'abord ControlNet en 1024×1024, résolution d'entraînement et de fonctionnement documentée pour les modèles v3.
  — <https://huggingface.co/XLabs-AI/flux-controlnet-depth-v3>
- Construisez les nouveaux workflows à image de référence sur IP-Adapter v2 plutôt que v1. La fiche v1 signale v2 comme modèle plus récent.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter>
- Considérez IP-Adapter comme un workflow de réglage plutôt que comme un transfert figé. La fiche v2 le qualifie toujours de bêta et suggère d'ajuster la force IP en cas de mauvais résultats.
  — <https://huggingface.co/XLabs-AI/flux-ip-adapter-v2>
- Figez et testez les nœuds personnalisés avant toute utilisation en production. L'historique de la branche principale s'arrête au 2024-10-30, donc les guides d'installation ne garantissent pas la compatibilité actuelle.
  — <https://github.com/XLabs-AI/x-flux-comfyui/commits/main>

## Remplacé par {#superseded-by-this}

- 2024-08-14 — pour tout nouveau travail ComfyUI avec ControlNet, la collection initiale est remplacée par les points de contrôle et workflows Canny v3, Depth v3 et HED v3 du 2024-08-19.
- 2024-08-21 — ne commencez pas de nouveaux travaux à partir de flux-ip-adapter v1. Sa fiche indique flux-ip-adapter-v2 comme version plus récente.
- Les consignes d'installation de l'époque 2024 ne garantissent pas la compatibilité actuelle. L'historique de la branche principale de x-flux-comfyui s'arrête au 2024-10-30 ; testez donc l'installation avec la version de ComfyUI que vous utilisez.

## Points non élucidés {#still-unknown}

- ControlNet et IP-Adapter sont deux lignes distinctes chez XLabs AI. L'une conditionne FLUX par des cartes structurelles, l'autre par des images de référence ; aucune ne remplace l'autre.
- Nous n'avons trouvé aucune documentation ni aucune note de version en chinois simplifié émanant de XLabs dans le volet de recherche en chinois.
- Aucune source consultée aujourd'hui ne prouve la compatibilité entre x-flux-comfyui et la version actuelle de ComfyUI ou un successeur de FLUX.
- Les conditions commerciales restent non confirmées. La page v2 affiche des métadonnées Apache-2.0, mais le texte de licence restreint les poids à la licence FLUX.1-dev Non-Commercial.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://huggingface.co/XLabs-AI/flux-controlnet-collections | XLabs-AI/flux-controlnet-collections · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-controlnet-hed-v3 | XLabs-AI/flux-controlnet-hed-v3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-controlnet-depth-v3 | XLabs-AI/flux-controlnet-depth-v3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-controlnet-canny-v3 | XLabs-AI/flux-controlnet-canny-v3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-ip-adapter | XLabs-AI/flux-ip-adapter · Hugging Face | 2026-09-04 |
| https://huggingface.co/XLabs-AI/flux-ip-adapter-v2 | XLabs-AI/flux-ip-adapter-v2 · Hugging Face | 2026-09-04 |
| https://github.com/XLabs-AI/x-flux-comfyui | GitHub - XLabs-AI/x-flux-comfyui | 2026-09-04 |
| https://github.com/XLabs-AI/x-flux-comfyui/blob/main/Guide.md | x-flux-comfyui Guide.md · GitHub | 2026-09-04 |
| https://github.com/XLabs-AI/x-flux-comfyui/commits/main | Commits · XLabs-AI/x-flux-comfyui · GitHub | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `organization:xlabs-ai`, fil `flux-conditioning-and-comfyui-integrations`, 3 événements datés du 2024-08-14 au 2024-08-21.
- **Note pratique :** Considérez le conditionnement ControlNet et le conditionnement IP-Adapter par image de référence comme deux voies distinctes à partir du 2024-08-21. Partez de l'intégration ComfyUI liée plutôt que de supposer un workflow unique et commun.
- **Confiance :** moyenne. La liste datée des remplacements ci-dessus indique ce qui est obsolète.
