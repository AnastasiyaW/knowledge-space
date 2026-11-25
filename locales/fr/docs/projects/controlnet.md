---
title: "ControlNet"
category: projects
date: 2023-04-13
tags: [controlnet, controlnet-development, controlnet_face_landmarks, controlnet_v1_1, open_source_release, project]
aliases: ["ControlNet"]
level: 3
source_sha256: 406dfbe74332beb300a643e28dc1f98b9b4451628e6d807ec4639bc76ae61f3a
translation: machine
translated_at: '2026-10-24'
---
# ControlNet {#controlnet}

**Ligne de développement :** `project:controlnet` · fil `controlnet-development`  
**Dernier événement :** 2023-04-13 · 3 événements datés depuis 2023-02-12 · **Consulté le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

ControlNet est un adaptateur de conditionnement spatial pour les modèles de diffusion. Nous l'utilisons lorsqu'un prompt doit suivre une image de référence et non seulement du texte.

- Les cartes de contours et de lignes, la profondeur, la segmentation, les poses et les croquis guident la génération.
- Les poids du modèle de base gelés restent inchangés, tandis que les branches adaptatrices ajoutent une structure visuelle.

## Ligne de développement {#development-line}

- **2023-02-12 — Le code source de ControlNet et les points d'entrée exécutables sont devenus publics.** Le 2023-02-12, le dépôt GitHub, l'espace Hugging Face et le notebook Colab associés ont ouvert un accès public au code et aux démonstrations exécutables. Les liens ne donnent ni étiquette de version précise ni liste de fonctionnalités.
- **2023-03-20 — Un modèle ControlNet de repères faciaux a été présenté à la communauté.** Le 2023-03-20, une ressource communautaire a publié un modèle ControlNet pour les repères faciaux. Il a ajouté à l'écosystème un conditionnement de la structure faciale. Nous ne disposons d'aucune donnée sur sa diffusion, ses performances ou son adoption.
- **2023-04-13 — ControlNet v1.1 est entré dans une ligne de développement nightly.** Le 2023-04-13, un dépôt GitHub a marqué le début de la ligne nightly de la v1.1. Il a accompagné un développement actif du projet. Le dépôt n'indiquait aucune date de version stable et ne détaillait pas les changements.

## Évolution {#what-changed}

ControlNet est passé d'une implémentation de recherche pour SD 1.x à des workflows de contrôle propres à chaque modèle. 2023-02-12 - Le projet d'origine documentait le transfert de ControlNet vers des modèles communautaires SD 1.x. 2023-03-20 - Un point de contrôle communautaire Face-Landmark a ajouté un type de contrôle sans modifier l'architecture de base. 2023-04-13 - ControlNet 1.1 a conservé l'architecture de la 1.0, normalisé les noms et étendu le catalogue SD 1.5 à 14 modèles : 11 prêts pour la production et 3 expérimentaux. 2023-05-31 - L'extension A1111 a ajouté, dans la 1.1.202, un workflow d'inpainting haute résolution en cascade sans modifier ControlNet lui-même. 2026-09-04 - Les guides actuels documentent les workflows ControlNet pour Flux, Hunyuan-DiT, Stable Diffusion 3 et SDXL, via les nœuds ComfyUI et les pipelines Diffusers.

## Mode d'emploi {#how-to-use-this}

Le travail a commencé le 2023-02-12 avec le code source et les points d'entrée exécutables. À partir du 2023-04-13, identifiez directement la ligne nightly de la v1.1 au lieu de considérer toutes les ressources comme une seule version.

1. Choisissez une contrainte structurelle et prétraitez l'image de référence correspondante ; différents types de ControlNet attendent différentes images de référence.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
2. Dans ComfyUI, placez le point de contrôle dans `ComfyUI/models/controlnet`, chargez le checkpoint de base et ControlNet, puis importez l'image de référence.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
3. Connectez ControlNet aux conditionnements positif et négatif, réglez la force et, si besoin, les pourcentages de début et de fin, puis lancez la génération.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
4. Dans le code, chargez un modèle de contrôle dans le pipeline Diffusers, transmettez le prompt et `control_image`, puis ajustez `controlnet_conditioning_scale`.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
5. Dans AUTOMATIC1111, installez ou mettez à jour `sd-webui-controlnet`, ajoutez les fichiers de modèle, actualisez la liste et sélectionnez le préprocesseur dans l'interface.
  — <https://github.com/Mikubill/sd-webui-controlnet>

## Bonnes pratiques {#best-practices}

- Faites correspondre le préprocesseur et la carte de référence au point de contrôle ; différents types de ControlNet exigent différentes images de référence.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
- Gardez les points de contrôle et les pipelines au sein d'une même famille de modèles, au lieu de considérer SD 1.5, SDXL, Flux et d'autres comme interchangeables.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- Ajustez directement Control Strength ou `controlnet_conditioning_scale` pour que la référence ne domine pas la sortie ni ne la contraigne insuffisamment.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- Pour Multi-ControlNet, redimensionnez les entrées aux dimensions attendues, masquez les conditionnements pour éviter les chevauchements et réglez chaque échelle de conditionnement séparément.
  — <https://huggingface.co/docs/diffusers/using-diffusers/controlnet>
- Dans ComfyUI, utilisez `Apply ControlNet` ; `Apply ControlNet (Old)` est déprécié.
  — <https://docs.comfy.org/tutorials/controlnet/controlnet>
- Pour AUTOMATIC1111, utilisez `sd-webui-controlnet` ; n'installez pas le dépôt de recherche `ControlNet-v1-1-nightly` comme extension A1111.
  — <https://github.com/lllyasviel/ControlNet-v1-1-nightly>

## Éléments remplacés {#superseded-by-this}

- 2023-04-13 - Installer `ControlNet-v1-1-nightly` dans AUTOMATIC1111 est une voie héritée incorrecte ; ses propres instructions orientent les utilisateurs d'A1111 vers `sd-webui-controlnet`.
- 2023-05-31 - Considérer la version 1.1.202 d'A1111 comme l'intégration actuelle est obsolète ; l'extension documente des travaux ultérieurs, la 1.1.454, datée du 2024-07-09.
- 2023 (période) - Les graphes ComfyUI utilisant `Apply ControlNet (Old)` sont dépréciés ; utilisez `Apply ControlNet`.

## Points non vérifiés {#still-unknown}

- L'élément Face-Landmark repose sur une seule publication et une seule démonstration communautaires ; nous n'avons pas vérifié sa fiche de modèle, sa licence, sa compatibilité de point de contrôle ni son hébergement actuel.
- Les événements datés combinent l'architecture de base, un point de contrôle communautaire et une extension AUTOMATIC1111 en un écosystème, et non en une distribution unique et maintenue.
- Nous ne pouvons pas consulter l'espace Hugging Face ni le notebook Colab historiques ; les instructions d'origine et leur disponibilité restent donc non confirmées.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/lllyasviel/ControlNet | GitHub - lllyasviel/ControlNet : Let us control diffusion models! | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/11v3dgj/new_controlnet_model_trained_on_face_landmarks/ | Nouveau modèle ControlNet entraîné sur des repères faciaux | 2026-09-04 |
| https://github.com/lllyasviel/ControlNet-v1-1-nightly | GitHub - lllyasviel/ControlNet-v1-1-nightly : Nightly release of ControlNet 1.1 | 2026-09-04 |
| https://github.com/Mikubill/sd-webui-controlnet/discussions/1464 | [1.1.202 Inpaint] Improvement : Everything Related to Adobe Firefly Generative Fill | 2026-09-04 |
| https://huggingface.co/docs/diffusers/using-diffusers/controlnet | ControlNet - Hugging Face Diffusers | 2026-09-04 |
| https://docs.comfy.org/tutorials/controlnet/controlnet | ComfyUI ControlNet Usage Example | 2026-09-04 |
| https://github.com/Mikubill/sd-webui-controlnet | GitHub - Mikubill/sd-webui-controlnet : WebUI extension for ControlNet | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:controlnet`, fil `controlnet-development`, 3 événements datés du 2023-02-12 au 2023-04-13.
- **Note pratique :** À partir du 2023-02-12, les praticiens pouvaient obtenir ControlNet via les points d'entrée source et exécutables liés ; à partir du 2023-04-13, ils doivent identifier explicitement la ligne nightly de la v1.1 au lieu de traiter toutes les ressources ControlNet comme une version statique unique.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
