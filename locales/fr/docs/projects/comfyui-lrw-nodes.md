---
title: "comfyui-lrw-nodes — ComfyUI LRW Nodes"
category: projects
date: 2026-06-09
tags: [comfyui-lrw-nodes, comfyui_lrw_nodes, project]
aliases: ["comfyui-lrw-nodes"]
level: 2
source_sha256: 92d7e27ab96261eaa8fc0aa8d4a6e93b2c0ce52330443feb3aafb26b55daf2e2
translation: machine
translated_at: '2026-10-24'
---
# comfyui-lrw-nodes — ComfyUI LRW Nodes {#comfyui-lrw-nodes-comfyui-lrw-nodes}

**Ligne de développement :** `project:comfyui-lrw-nodes` · fil `comfyui-lrw-nodes`  
**Dernier événement :** 2026-06-09 · 1 événement daté depuis le 2026-06-09 · **Recherche :** 2026-09-05 · confiance : moyenne

## Description {#what-it-is}

ComfyUI-LRW-Nodes fournit des nœuds personnalisés pour ComfyUI afin de guider le mouvement intermédiaire de WAN2.2 First–Last Frame sans remplacer le conditionnement des images d'extrémité.

- Interpolation latente géodésique et SLERP.
- Expériences sur la distance latente, la courbure et le transport parallèle.
- Mélange de keyframes géodésiques WAN2.2 dans les latents vidéo avant KSampler.

Nécessite `latent-riemannian-world >= 0.3.0`, `torch >= 2.4`, ainsi que des nœuds WAN et vidéo supplémentaires pour le workflow fourni.
Utilisez-le comme guide souple expérimental et comparez-le à une référence direct-FLF à graine fixe ; il ne remplace pas la continuité des extrémités de WAN2.2.

## Ligne de développement {#development-line}

- **2026-06-09 — Le dépôt ComfyUI LRW Nodes et les exemples de workflows ont été documentés.** Un message daté du 2026-06-09 renvoyait ComfyUI LRW Nodes vers son dépôt GitHub et le répertoire des workflows d'exemple. Cela confirme que des personnes ont référencé le projet et les workflows à cette date. Cela n'indique aucune version, modification de fonctionnalité ou état particulier du dépôt.

## Modifications {#what-changed}

- 2026-06-07 — Le déploiement public initial visait WAN2.2 First–Last Frame. Les latents d'extrémité LRW ont produit un guide géodésique mélangé avant KSampler. Une correction de l'enregistrement et du chemin d'importation a suivi le même jour.
- 2026-06-09 — Le dépôt et son répertoire de workflows sont devenus publics. Nous ne disposons ni de numéro de version ni d'un journal des modifications daté pour cette étape.

## Mode d'emploi {#how-to-use-this}

À la date du 2026-06-09, évaluez ComfyUI LRW Nodes à partir du dépôt et des workflows d'exemple.

1. Installez via ComfyUI Manager en recherchant `comfyui-lrw-nodes`, ou clonez le dépôt dans `ComfyUI/custom_nodes`, exécutez `pip install -r requirements.txt`, puis redémarrez ComfyUI.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
2. Pour WAN2.2, installez les dépendances du workflow : ComfyUI-GGUF, le support WAN First–Last Frame et ComfyUI-VideoHelperSuite ; KJNodes est facultatif.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
3. Chargez le workflow pratique. Transmettez les première et dernière images à `WanFirstLastFrameToVideo` directement, puis encodez par VAE les deux images d'extrémité pour LRW.
  — <https://github.com/lajjadred/comfyui-lrw-nodes/tree/main/examples/workflows>
4. Créez des keyframes géodésiques, faites passer l'une d'elles par `LRW_WanLatentGuideBlend`, échantillonnez avec KSampler, puis décodez et assemblez la vidéo.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>

## Bonnes pratiques {#best-practices}

- Conservez WAN2.2 FLF direct comme voie de continuité. Mélangez le guide LRW dans son latent vidéo au lieu de remplacer le conditionnement de la dernière image cible.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
- Commencez avec `blend_strength=0.15`, `time_schedule=middle_focus` et `normalize_guide=true` ; la plage documentée est de 0,10 à 0,20.
  — <https://github.com/lajjadred/comfyui-lrw-nodes>
- Si des nœuds apparaissent comme inconnus ou échouent à l'importation, ne conservez qu'une seule installation, mettez-la à jour ou clonez-la à nouveau, redémarrez complètement ComfyUI et examinez le journal de démarrage autour de ce pack de nœuds.
  — <https://www.reddit.com/r/comfyui/comments/1tz4qnu/i_built_comfyui_nodes_that_use_riemannian/>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-07 — L'enregistrement obsolète dans `__init__.py` qui importe `LRW_LatentKeyframePicker` depuis `wan_nodes.py` est caduc. Mettez à jour le pack de nœuds et redémarrez ComfyUI.
- 2026-06-07 — Les recommandations qui présentent LRW comme une amélioration directe de la qualité ou comme un remplacement du conditionnement de l'image de fin de WAN2.2 FLF sont caduques. Son rôle documenté est celui d'un guide latent souple avant KSampler.

## Points toujours inconnus {#still-unknown}

- Aucune version, étiquette ou journal des modifications daté et émis par l'éditeur n'établit la révision exacte du dépôt au 2026-06-09.
- Le README mentionne quatre workflows d'exemple, alors que le répertoire de workflows lié ne montre que `wan22_practical_direct_flf_plus_lrw_guided_blend.json`. Les fichiers JSON de référence, d'interpolation d'images et de transfert de style ne sont pas vérifiés.
- GitHub indique dix commits, mais leur historique daté n'a pas pu être récupéré lors de cette vérification.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/lajjadred/comfyui-lrw-nodes | README de lajjadred/comfyui-lrw-nodes | 2026-09-05 |
| https://github.com/lajjadred/comfyui-lrw-nodes/tree/main/examples/workflows | Workflows d'exemple de comfyui-lrw-nodes | 2026-09-05 |
| https://www.reddit.com/r/comfyui/comments/1tz4qnu/i_built_comfyui_nodes_that_use_riemannian/ | I built ComfyUI nodes that use Riemannian geometry to guide WAN2.2 latent interpolation | 2026-09-05 |

## Synthèse pour l'agent {#agent-brief}

- **Sujet :** `project:comfyui-lrw-nodes`, fil `comfyui-lrw-nodes`, 1 événement daté du 2026-06-09 au 2026-06-09.
- **Note pratique :** à la date du 2026-06-09, les praticiens peuvent utiliser le dépôt du projet et les workflows d'exemple liés comme point de départ pour évaluer ou adopter ComfyUI LRW Nodes.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
