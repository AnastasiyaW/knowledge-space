---
title: "AuraFlow"
category: projects
date: 2024-08-15
tags: [auraflow, auraflow-model-releases, auraflow_release, project]
aliases: ["AuraFlow"]
level: 3
source_sha256: 6718fd27805d917914803d8496c28ed4ef426d2ce88b5be844d6a070dcd46640
translation: machine
translated_at: '2026-10-24'
---
# AuraFlow {#auraflow}

**Ligne de développement :** `project:auraflow` · fil `auraflow-model-releases`  
**Dernier événement :** 2024-08-15 · 3 entrées datées depuis le 2024-07-12 · **Recherche effectuée :** 2026-09-04 · confiance : medium

## Présentation {#what-it-is}

Un modèle de génération d'images à partir de texte basé sur les flux (flow-based), utilisable en local avec Diffusers et ComfyUI ou en inférence hébergée via fal.

- Génère des images à partir de texte via AuraFlowPipeline.
- Expose un point de terminaison hébergé `fal-ai/aura-flow`.
- La v0.3 prend en charge des rapports d'aspect variés, jusqu'à 1536 pixels par dimension.

## Ligne de développement {#development-line}

- **2024-07-12 — Les premières références publiques du projet AuraFlow ont été enregistrées.** La v0.1 a été publiée en tant que modèle de génération d'images à partir de texte basé sur les flux, entièrement ouvert ; fal a documenté la prise en charge native de Diffusers et de ComfyUI ainsi qu'une architecture de 6,8 B de paramètres.
- **2024-07-29 — La version AuraFlow v0.2 a été enregistrée comme nouvelle version du modèle.** La v0.2 était documentée comme successeur de la v0.1, entraîné avec davantage de calcul. La collection officielle indique sa mise à jour de modèle au 2024-07-27, ce qui pourrait distinguer la publication du modèle de son annonce.
- **2024-08-15 — La version AuraFlow v0.3 a été enregistrée comme version ultérieure du modèle.** La v0.3 ajoute davantage de calcul, un affinage sur des données esthétiques et la prise en charge de rapports d'aspect allant jusqu'à 1536 pixels par dimension.

## Changements {#what-changed}

AuraFlow — ligne de développement :

- 2024-07-12 : la v0.1 a été publiée en tant que modèle de génération d'images à partir de texte basé sur les flux, entièrement ouvert ; fal a documenté la prise en charge native de Diffusers et de ComfyUI ainsi qu'une architecture de 6,8 B.
- 2024-07-29 : la v0.2 a été documentée comme successeur de la v0.1, entraîné avec davantage de calcul. La collection officielle indique sa mise à jour de modèle au 2024-07-27, ce qui pourrait distinguer la publication du modèle de son annonce.
- 2024-08-15 : la v0.3 ajoute davantage de calcul, un affinage sur des données esthétiques et la prise en charge de rapports d'aspect allant jusqu'à 1536 pixels par dimension.
- Constaté aujourd'hui : la collection officielle de fal ne liste que le modèle sans numéro de version, la v0.2 et la v0.3 ; le point de terminaison fal en production identifie AuraFlow comme v0.3 et l'étiquette toujours comme bêta.

## Mode d'emploi {#how-to-use-this}

Au 2024-08-15, considérez AuraFlow comme une lignée de modèles versionnée. Sélectionnez la référence officielle précise — AuraFlow, AuraFlow-v0.2 ou AuraFlow-v0.3 — requise par chaque flux de travail, plutôt que de supposer que les versions sont interchangeables.

1. Épinglez `fal/AuraFlow-v0.3` pour toute nouvelle installation locale ; c'est le point de contrôle actuel documenté dans la collection officielle.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
2. Installez les versions actuelles de `diffusers`, `transformers` et `accelerate`, puis chargez `AuraFlowPipeline.from_pretrained("fal/AuraFlow-v0.3", torch_dtype=torch.float16, variant="fp16").to("cuda")`.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
3. Générez avec des dimensions explicites, 50 étapes d'inférence, un CFG de 3,5 et une graine de générateur fixe ; enregistrez l'image obtenue.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
4. Pour l'inférence hébergée, installez `@fal-ai/client`, définissez `FAL_KEY` dans l'environnement serveur, appelez `fal.subscribe("fal-ai/aura-flow", { input: { prompt } })` et conservez l'identifiant de requête renvoyé.
  — <https://fal.ai/models/fal-ai/aura-flow/api>

## Bonnes pratiques {#best-practices}

- Définissez explicitement les étapes et le CFG. Partez de la recette v0.3 (50 étapes, CFG 3,5) plutôt que de vous fier à une valeur par défaut de la bibliothèque.
  — <https://huggingface.co/fal/AuraFlow-v0.3>
- Lorsque la VRAM locale est limitée, utilisez la quantification 8 bits documentée et le mappage d'appareils équilibré, puis comparez les sorties avant d'adopter la voie à plus faible précision.
  — <https://huggingface.co/docs/diffusers/api/pipelines/aura_flow>
- Conservez `FAL_KEY` côté serveur ; utilisez l'état de la file d'attente et les webhooks plutôt que d'attendre de manière bloquante les requêtes lentes, et conservez la graine et le prompt enrichi renvoyés pour la reproductibilité.
  — <https://fal.ai/models/fal-ai/aura-flow/api>
- N'importez pas tel quel le workflow ComfyUI v0.3 publié : il référence actuellement `aura_flow_0.2.safetensors`. Remplacez délibérément le checkpoint et validez par une génération de test.
  — <https://huggingface.co/fal/AuraFlow-v0.3/blob/main/comfy_workflow.json>
- Pour le fine-tuning avec SimpleTuner, considérez la voie LoKr Lycoris spécifique à AuraFlow comme point de départ plutôt qu'un entraînement de rang plein sans précaution ; son guide prévoit une VRAM importante ou DeepSpeed pour un entraînement complet, et démarre la validation à 1024², 30–50 étapes et un CFG de 3,5–4,0.
  — <https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/AURAFLOW.md>

## Versions remplacées {#superseded-by-this}

- 2024-07-29 : AuraFlow v0.2 remplace le checkpoint v0.1 pour la branche principale officielle, car il a été entraîné avec davantage de calcul ; ne conservez la v0.1 que pour la reproductibilité héritée.
- 2024-08-15 : AuraFlow v0.3 remplace la v0.2 comme point de contrôle de départ documenté, en ajoutant un affinage esthétique et des rapports d'aspect variables allant jusqu'à 1536 pixels par dimension.
- Actuel : les extraits de chargement de `fal/AuraFlow` sans numéro de version et de la v0.2 sont obsolètes pour une nouvelle installation ; épinglez plutôt `fal/AuraFlow-v0.3`. Il s'agit d'une recommandation d'usage, et non d'un avis de dépréciation formel.

## Points non vérifiés {#still-unknown}

- La collection de fal liste trois points de contrôle v0.x, mais cette absence ne permet pas de prouver qu'aucun successeur non publié ou portant un autre nom n'existe.
- Les pages publiques du modèle et de l'API qualifient toujours la v0.3 de bêta ; aucune matrice actuelle de GPU pris en charge ni mesure propre de la v0.3 n'a été trouvée, si bien que la VRAM et la latence ne sont pas généralisées.
- La référence Diffusers actuelle est incohérente : la signature d'appel indique un CFG de 3,5, tandis que le texte des paramètres indique 5,0. Définissez le CFG explicitement à partir de la fiche ou de la recette API v0.3.
- Le fichier `comfy_workflow.json` publié dans le dépôt v0.3 référence un checkpoint v0.2 ; il n'est donc pas vérifié comme workflow v0.3 sans remplacement local et exécution de test.
- La piste en chinois simplifié a trouvé une traduction du guide SimpleTuner et un workflow ComfyUI communautaire, mais aucune mesure opérationnelle indépendante et verrouillée sur la v0.3 ; elle ne modifie pas la recette de départ documentée.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://blog.fal.ai/auraflow/ | Introducing AuraFlow v0.1, an Open Exploration of Large Rectified Flow Models | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow | fal/AuraFlow · Hugging Face | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow-v0.2 | fal/AuraFlow-v0.2 · Hugging Face | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow-v0.3 | fal/AuraFlow-v0.3 · Hugging Face | 2026-09-04 |
| https://huggingface.co/collections/fal/auraflow | AuraFlow — a fal Collection | 2026-09-04 |
| https://fal.ai/models/fal-ai/aura-flow/api | AuraFlow Text to Image API Docs | fal | 2026-09-04 |
| https://huggingface.co/docs/diffusers/api/pipelines/aura_flow | AuraFlow — Hugging Face Diffusers | 2026-09-04 |
| https://huggingface.co/fal/AuraFlow-v0.3/blob/main/comfy_workflow.json | comfy_workflow.json · fal/AuraFlow-v0.3 | 2026-09-04 |
| https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/AURAFLOW.md | Auraflow Quickstart — SimpleTuner | 2026-09-04 |
| https://github.com/bghira/SimpleTuner/blob/main/documentation/quickstart/AURAFLOW.zh.md | Auraflow Quickstart, Simplified Chinese — SimpleTuner | 2026-09-04 |
| https://comfyui.nomadoor.net/zh/basic-workflows/auraflow/ | AuraFlow | Comfy with ComfyUI, Simplified Chinese | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:auraflow`, fil `auraflow-model-releases`, 3 événements datés du 2024-07-12 au 2024-08-15.
- **Note pratique :** Au 2024-08-15, les praticiens doivent considérer AuraFlow comme une lignée de modèles versionnée et sélectionner la référence officielle précise — AuraFlow, AuraFlow-v0.2 ou AuraFlow-v0.3 — requise par leur flux de travail, plutôt que de supposer que les versions sont interchangeables.
- **Confiance :** medium. Les remplacements datés ci-dessus font foi pour déterminer ce qui est obsolète.
