---
title: "ComfyUI-PuLID-Flux2 — Intégration de PuLID-Flux2 dans ComfyUI"
category: projects
date: 2026-03-16
tags: [comfyui-pulid-flux2, project, pulid, pulid-flux2-comfyui-integration]
aliases: ["ComfyUI-PuLID-Flux2"]
level: 2
source_sha256: 612b7404a3d7c1221ef00238edf37e2547cede6dcb877a80196856aee5417d8c
translation: machine
translated_at: '2026-10-24'
---
# ComfyUI-PuLID-Flux2 — Intégration de PuLID-Flux2 dans ComfyUI {#comfyui-pulid-flux2-pulid-flux2-comfyui-integration}

**Ligne de développement :** `project:comfyui-pulid-flux2` · fil `pulid-flux2-comfyui-integration`  
**Dernier événement :** 2026-03-16 · 1 événement daté depuis le 2026-03-16 · **Consulté le :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

ComfyUI-PuLID-Flux2 est une adaptation de PuLID pour ComfyUI et FLUX.2 : il charge les poids InsightFace AntelopeV2, EVA-CLIP et PuLID, puis applique l'identité au modèle avant l'échantillonnage. Fonctionnalités : Klein 4B/9B et Dev, sélection du visage par index, visualisation de débogage, workflow Klein prêt à l'emploi. Limite : EVA-CLIP télécharge automatiquement environ 800 MB, et les training scripts ont été supprimés car jugés instables. Verdict : adapté aux workflows de portrait préservant l'identité, mais utilisez les poids Flux.2 natifs et vérifiez la compatibilité du modèle concerné.

## Ligne de développement {#development-line}

- **2026-03-16 — Les ressources d'installation de ComfyUI-PuLID-Flux2 ont été liées.** Le 2026-03-16, le dépôt ComfyUI-PuLID-Flux2 a été lié avec son répertoire de workflows et les ressources de modèles externes PuLID et antelopev2. Cela constitue un point de référence pratique pour l'intégration du projet, mais les éléments disponibles n'établissent ni une version, ni une publication, ni une modification d'implémentation précise.

## Modifications {#what-changed}

2026-03-16 — la v0.2.1 a corrigé le dimension mismatch lors du passage entre Flux.2 Klein et Dev ; le même jour, la connexion et les noms dans l'example workflow ont été corrigés. 2026-03-17 — conflit de dtype FP16/BF16 corrigé. 2026-03-20 — la v0.3.0 a corrigé les single blocks, half/bfloat16, la plage sigma et EVA-CLIP 3D ; ajout d'un training pipeline pour Vast.ai. 2026-03-21 — la v0.4.0 a ajouté safetensors, des poids sur Hugging Face et des réglages mis à jour. 2026-03-25 — 2026-03-28 — la v0.5.0 a ajouté de nouveaux poids ; la v0.6.0 a ajouté les v1/v2 natifs ; la v0.6.2 a rétabli la prise en charge de Dev32. 2026-03-30 et 2026-04-24 — ont été introduits un contournement de la détection via model_function_wrapper et une protection contre le monkey-patching cumulatif de block.forward.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-03-16, les praticiens doivent utiliser les workflows du projet liés avec les sources de modèles PuLID et antelopev2 référencées lors de la préparation d'une installation ComfyUI-PuLID-Flux2, en vérifiant séparément la version exacte et les exigences d'installation.

1. Clonez le custom node dans ComfyUI/custom_nodes et installez les dépendances indiquées ; n'exécutez pas le requirements.txt complet dans une installation ComfyUI déjà fonctionnelle.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2>
2. Téléchargez le checkpoint PuLID-Flux2 natif et placez-le dans ComfyUI/models/pulid/.
  — <https://huggingface.co/Fayens/Pulid-Flux2>
3. Placez les fichiers AntelopeV2 dans ComfyUI/models/insightface/models/antelopev2/.
  — <https://huggingface.co/MonsterMMORPG/InstantID_Models/tree/main/models/antelopev2>
4. Importez le workflow Klein, connectez la photo de référence, le modèle Flux.2, le modèle PuLID, EVA-CLIP et InsightFace à Apply PuLID Flux.2.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2/tree/main/workflows>

## Bonnes pratiques {#best-practices}

- Commencez avec un strength de 1.0 ; la documentation de l'auteur indique 1.4 comme réglage recommandé, mais n'augmentez la valeur qu'après une vérification visuelle de l'identité et des artefacts.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2>
- Pour Flux.2, utilisez les checkpoints natifs v1/v2 et non les PuLID-FLUX v0.9.x d'origine : ces derniers relèvent d'une ligne FLUX antérieure.
  — <https://huggingface.co/Fayens/Pulid-Flux2>
- N'installez pas eva_clip directement depuis GitHub ; le chargeur du projet récupère EVA-CLIP automatiquement.
  — <https://github.com/iFayens/ComfyUI-PuLID-Flux2>

## Consignes rendues obsolètes {#superseded-by-this}

- 2026-03-16 : les consignes pour les workflows supposant qu'on pouvait basculer entre Klein et Dev sans reconstruire le module PuLID sont obsolètes ; la v0.2.1 a corrigé le dimension mismatch.
- 2026-03-17 : les hypothèses strictes sur un unique chemin FP16/BF16 sont obsolètes ; le conflit de dtype a été corrigé.
- 2026-03-26 : les consignes antérieures aux poids natifs sont remplacées, pour Flux.2, par les poids natifs PuLID-Flux2 v1/v2.

## Points non vérifiés {#still-unknown}

- Les champs requis event_findings et new_events sont absents du schéma de sortie fourni ; leur chronologie vérifiable est incluse dans what_changed. Pour l'événement du 2026-03-16, l'historique GitHub donne sa date propre et la correction exacte : la v0.2.1 a corrigé le dimension mismatch Klein↔Dev, et le workflow a reçu une correction de connexion.
- Le dépôt indique la prise en charge de Klein et Dev, mais ne fournit ni benchmark indépendant d'identité, ni profil de VRAM, ni garantie de stabilité pour toutes les variantes de FLUX.2.
- Le dépôt d'origine guozinan/PuLID publie PuLID-FLUX-v0.9.0/v0.9.1 pour la ligne FLUX antérieure ; ce n'est pas le même checkpoint que les PuLID-Flux2 v1/v2 natifs.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/iFayens/ComfyUI-PuLID-Flux2 | README de iFayens/ComfyUI-PuLID-Flux2 | 2026-09-05 |
| https://github.com/iFayens/ComfyUI-PuLID-Flux2/commits/main | Historique des commits de iFayens/ComfyUI-PuLID-Flux2 | 2026-09-05 |
| https://github.com/iFayens/ComfyUI-PuLID-Flux2/tree/main/workflows | Workflows ComfyUI-PuLID-Flux2 | 2026-09-05 |
| https://huggingface.co/Fayens/Pulid-Flux2 | Dépôt de modèle Fayens/Pulid-Flux2 | 2026-09-05 |
| https://huggingface.co/MonsterMMORPG/InstantID_Models/tree/main/models/antelopev2 | Fichiers AntelopeV2 de MonsterMMORPG/InstantID_Models | 2026-09-05 |
| https://huggingface.co/guozinan/PuLID | Fiche modèle guozinan/PuLID | 2026-09-05 |

## Consigne pour l'agent {#agent-brief}

- **Sujet :** `project:comfyui-pulid-flux2`, fil `pulid-flux2-comfyui-integration`, 1 événement daté, du 2026-03-16 au 2026-03-16.
- **Note pratique :** à partir du 2026-03-16, les praticiens doivent utiliser les workflows du projet liés avec les sources de modèles PuLID et antelopev2 référencées lors de la préparation d'une installation ComfyUI-PuLID-Flux2, en vérifiant séparément la version exacte et les exigences d'installation.
- **Confiance :** élevée. Les remplacements datés ci-dessus font autorité pour déterminer ce qui est obsolète.
