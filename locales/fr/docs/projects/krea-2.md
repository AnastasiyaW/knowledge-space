---
title: "Krea 2 — Publication open source et écosystème"
category: projects
date: 2026-06-24
tags: [krea-2, open-source-release, project]
aliases: ["Krea 2"]
level: 3
source_sha256: f4b58f925686d0c3609f47f947ec958465f68f6220726e7e71a89bb1da14cfe1
translation: machine
translated_at: '2026-10-24'
---
# Krea 2 — Publication open source et écosystème {#krea-2-open-source-release-and-ecosystem}

**Ligne de développement :** `project:krea-2` · fil `open-source-release`  
**Dernier événement :** 2026-06-24 · 2 événements datés depuis le 2026-06-23 · **Recherche :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

Krea 2 est une famille de modèles de génération d'images destinée aux designers, aux développeurs et aux chercheurs. L'API hébergée propose Medium, Large et Medium Turbo, avec des images de référence de style, des moodboards, LoRA et image-à-image. La publication open source fournit les poids RAW et Turbo, ainsi que le code pour la génération texte-à-image en local et l'entraînement de LoRA.

- Cloud : API, images de référence, moodboards, sliders et tâches.
- Local : RAW pour le fine-tuning et les LoRA, Turbo pour une génération rapide.

RAW en local est recommandé jusqu'à 1K, Turbo fonctionne en 1K–2K avec 8 étapes, et Medium Turbo hébergé n'accepte que 1K. Choisissez Krea 2 hébergé pour les workflows pilotés par des références, et RAW ou Turbo pour une génération locale maîtrisée, car les surfaces de checkpoints sont apparentées sans être prouvées identiques.

## Ligne de développement {#development-line}

- **2026-06-23 — Les premiers outils communautaires et artefacts de modèle de Krea 2 ont fait surface.** RAW est devenu la base pour l'entraînement et les LoRA, et Turbo est devenu le checkpoint à 8 étapes pour le texte-à-image.
- **2026-06-24 — Krea a publié les documents officiels d'open source et de déploiement de Krea 2.** La version à poids ouverts correspond à Medium, tandis que les modules moodboard et de référence de style sont omis de la publication open source.

## Ce qui a changé {#what-changed}

Le 2026-06-23, le rapport technique officiel, le code d'inférence et les poids ouverts RAW et Turbo ont établi le pipeline local : RAW est devenu la base pour l'entraînement et les LoRA, et Turbo est devenu le checkpoint à 8 étapes pour le texte-à-image. Le 2026-06-24, Krea a précisé la frontière de la publication : la version à poids ouverts correspond à Medium, et les modules moodboard et de référence de style ne sont pas inclus dans la publication open source.

## Comment l'utiliser {#how-to-use-this}

À partir du 2026-06-24, les praticiens devraient commencer l'évaluation de Krea 2 par les ressources officielles Raw ou Turbo liées et par le workflow ComfyUI Turbo indiqué, tout en considérant les artefacts communautaires du 2026-06-23 comme des alternatives non vérifiées.

1. Choisissez la surface : utilisez RAW ou Turbo à poids ouverts pour la génération locale et les LoRA personnalisées ; utilisez l'API hébergée pour les images de référence, les moodboards et les tâches gérées.
  — <https://www.krea.ai/krea-2-open-source>
2. Pour une exécution locale, récupérez le dépôt officiel, exécutez `uv sync`, téléchargez les checkpoints et définissez les chemins dans `OSS_RAW` et `OSS_TURBO`.
  — <https://github.com/krea-ai/krea-2>
3. Commencez avec les paramètres officiels : RAW à 52 étapes et CFG 3.5 jusqu'à 1K ; Turbo à 8 étapes, CFG 0, `mu=1.15` et taille 1K–2K.
  — <https://github.com/krea-ai/krea-2>
4. Dans ComfyUI, importez le workflow officiel Turbo texte-à-image ; sa configuration de départ est 1024×1024 et KSampler à 8 étapes.
  — <https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_krea2_turbo_t2i.json>
5. Pour l'API hébergée, envoyez une requête POST authentifiée par Bearer vers `.../krea-2/medium-turbo` avec le prompt, le ratio d'aspect et une résolution 1K ; conservez `job_id` et récupérez le résultat via l'endpoint de la tâche ou via un webhook.
  — <https://www.krea.ai/docs/api-reference/krea/krea-2-turbo>

## Bonnes pratiques {#best-practices}

- Entraînez les LoRA sur RAW et exécutez l'inférence sur Turbo ; n'utilisez pas RAW comme checkpoint de production rapide par défaut.
  — <https://github.com/krea-ai/krea-2>
- Rédigez des prompts naturels et détaillés ; placez entre guillemets les mots destinés à apparaître comme texte dans l'image.
  — <https://github.com/krea-ai/krea-2/blob/main/docs/prompting.md>
- Dans Krea hébergé, gardez le prompt inchangé et ajustez un seul slider à la fois ; 0 est la valeur neutre, et Raw/Low Creativity convient mieux à un contrôle précis.
  — <https://www.krea.ai/blog/generative-sliders>
- Pour les LoRA hébergées, utilisez un jeu de données restreint à partir de trois images, vérifiez manuellement les légendes automatiques et évitez de mélanger personnage, style et produit dans la première LoRA.
  — <https://www.krea.ai/blog/krea-2-lora-training>
- Dans l'API, traitez les réponses comme asynchrones : un 200 peut renvoyer une tâche en attente ; utilisez un webhook ou un polling de statut, et gérez explicitement les états échoué ou annulé.
  — <https://www.krea.ai/docs/api-reference/krea/krea-2-turbo>
- Effectuez des tests de sécurité adaptés à votre scénario avant de déployer des poids ouverts, et respectez la Krea 2 Community License en plus de la licence du code.
  — <https://huggingface.co/krea/Krea-2-Raw>

## Remplacé par ceci {#superseded-by-this}

- Rien n'est encore marqué comme obsolète.

## Points encore inconnus {#still-unknown}

- La correspondance exacte entre Krea 2 Medium ou Medium Turbo hébergés et RAW ou Turbo à poids ouverts n'est pas documentée au niveau des hachages ou des checkpoints ; l'AMA indique seulement que la version open source correspond à Medium.
- La fiche modèle ouverte indique 13 milliards de paramètres, tandis que la page de publication mentionne un DiT dense de 12 milliards ; il peut s'agir de périmètres de comptage différents, mais sans détail du comptage de paramètres, ces chiffres ne peuvent pas être réconciliés en un seul total.
- Les pages officielles ne montrent aucun checkpoint public RAW ou Turbo postérieur au 2026-06-24 ; la documentation actuelle de l'API ne prouve pas de mises à jour des poids ouverts.
- Le contenu du post X de l'événement du 2026-06-23 n'était pas disponible pour vérification et n'a pas été utilisé comme preuve.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.krea.ai/blog/krea-2-image-model | Introducing Krea 2 | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-lora-training | Krea 2 LoRA training is now available | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-api-launch | Krea 2 API | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-turbo | Krea 2 Turbo: Generate Images in 2 Seconds | 2026-09-04 |
| https://www.krea.ai/blog/generative-sliders | Introducing Generative Sliders | 2026-09-04 |
| https://www.krea.ai/blog/krea-2-technical-report | Krea 2 Technical Report | 2026-09-04 |
| https://huggingface.co/krea/Krea-2-Raw | krea/Krea-2-Raw | 2026-09-04 |
| https://github.com/krea-ai/krea-2 | Krea 2 (K2) — official inference code | 2026-09-04 |
| https://www.krea.ai/krea-2-open-source | Krea 2 Open Source | 2026-09-04 |
| https://www.reddit.com/r/StableDiffusion/comments/1udnm0a/we_are_the_team_behind_krea_2_ask_us_anything/ | We are the team behind Krea 2. Ask us anything! | 2026-09-04 |
| https://github.com/Comfy-Org/workflow_templates/blob/main/templates/image_krea2_turbo_t2i.json | image_krea2_turbo_t2i.json | 2026-09-04 |
| https://www.krea.ai/docs/api-reference/introduction | Krea API reference: models, endpoints, and schemas | 2026-09-04 |
| https://www.krea.ai/docs/api-reference/krea/krea-2-turbo | Krea 2 Turbo API | 2026-09-04 |
| https://github.com/krea-ai/krea-2/blob/main/docs/prompting.md | Prompting guidelines | 2026-09-04 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:krea-2`, fil `open-source-release`, 2 événements datés du 2026-06-23 au 2026-06-24.
- **Note pratique :** À partir du 2026-06-24, les praticiens devraient commencer l'évaluation de Krea 2 par les ressources officielles Raw ou Turbo liées et par le workflow ComfyUI Turbo indiqué, tout en considérant les artefacts communautaires du 2026-06-23 comme des alternatives non vérifiées.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.

<!-- authored-live-update:bf52587c12cd0fb788672535d3ae6ab873df031c4d2c724e5db6ec3ff4b3e322 -->
# Krea 2 Turbo SDA Diversity LoRA {#krea-2-turbo-sda-diversity-lora}

L'artefact public est [F16/krea2-turbo-sda](https://huggingface.co/F16/krea2-turbo-sda), intitulé **Krea 2 Turbo — SDA Diversity LoRA (v1.0)**. Il s'agit d'un adaptateur communautaire pour `krea/Krea-2-Turbo`, et non d'un nouveau modèle Krea ni d'un réglage général de Krea 2.

Son auteur, F16, désigne SDA par « Semantic Directional Alignment ». L'objectif annoncé est de faire en sorte que des seeds différentes produisent des images plus variées à partir d'un même prompt. L'auteur rapporte un panel d'évaluation fixe de 10 prompts par 16 seeds : la distance cosinus CLIP par paires est passée de 0,0296 à 0,0548 avec l'adaptateur au gate 2, tandis que HPSv2.1 est passé de 0,2990 à 0,2987. Ce sont des chiffres rapportés par le créateur, non un benchmark indépendant. [Fiche en anglais](https://huggingface.co/F16/krea2-turbo-sda) · [Fiche en chinois simplifié](https://huggingface.co/F16/krea2-turbo-sda/blob/main/README.zh.md)

## Le gate est le workflow {#the-gate-is-the-workflow}

La fiche documente l'usage de ce LoRA pour les deux premières étapes de débruitage du calendrier Turbo de Krea 2 à huit étapes, puis indique de le désactiver. Dans le panel de l'auteur, « gate 2 » est la configuration prévue. Le garder actif pendant les huit étapes provoquerait, selon les rapports, du flou ou un effondrement de la qualité.

Un chargeur de LoRA toujours actif ne convient pas. L'auteur indique que ComfyUI standard applique un LoRA à chaque étape ; le chemin ComfyUI nécessite donc un hook par étape ou un nœud de planification qui retire l'adaptateur après l'étape 2. La fiche ne nomme ni nœud canonique ni JSON de workflow. Ne qualifiez pas un graphe ComfyUI quelconque de workflow SDA officiel.

Le dépôt contient deux fichiers :

- `krea2_turbo_sda_v1.0_comfy.safetensors` pour ComfyUI.
- `krea2_turbo_sda_v1.0_diffusers.safetensors` pour Diffusers.

Pour la voie Diffusers documentée, la fiche demande un build de `Krea2Pipeline` fusionné après `0.39.0.dev0`, en bf16, avec huit étapes, un guidance de 1.0, et un callback qui désactive le LoRA après la deuxième étape. Il s'agit de la recette du créateur, non d'une recette reproduite localement.

## Ce que cela ne prouve pas {#what-it-does-not-prove}

L'auteur rapporte davantage de variation d'une seed à l'autre. Cela ne montre pas que l'adaptateur corrige un défaut de Krea 2. La fiche ne précise pas non plus si cela fonctionne avec Raw ou d'autres variantes de Turbo.

La fiche signale aussi un compromis : une diversité accrue peut réduire la stabilité et rendre les erreurs d'anatomie plus probables. Conservez le checkpoint de base, le fichier de l'adaptateur, la révision du framework, la plage de seeds, la résolution, les étapes, le guidance, le shift et le gate dans chaque comparaison.

Une [démo Hugging Face Space publique](https://huggingface.co/spaces/hugging-apps/krea2-turbo-sda-demo) existe. La fiche indique qu'une démo est disponible, mais cette recherche n'a pas pu obtenir son export de workflow, son lockfile d'exécution, son profil matériel ni un résultat rejoué indépendamment.

## Sources {#sources_1}

- [F16/krea2-turbo-sda](https://huggingface.co/F16/krea2-turbo-sda) — fiche d'artefact en anglais du créateur, évaluation rapportée, installation et limites.
- [README.zh.md](https://huggingface.co/F16/krea2-turbo-sda/blob/main/README.zh.md) — fiche en chinois simplifié du créateur ; la paraphrase anglaise ci-dessus conserve sa provenance.
- [Démo Krea 2 Turbo SDA](https://huggingface.co/spaces/hugging-apps/krea2-turbo-sda-demo) — simple fiche de démo publique.

## Brief pour l'agent {#agent-brief_1}

Identifiez l'artefact comme `F16/krea2-turbo-sda` avant d'en parler. Utilisez-le uniquement avec `krea/Krea-2-Turbo` ; utilisez le fichier correspondant ComfyUI ou Diffusers ; planifiez-le pour les deux premières étapes sur huit et désactivez-le ensuite. Étiquetez chaque chiffre de diversité comme rapporté par le créateur. Ne considérez pas la fiche de démo comme un workflow vérifié, et n'étendez pas la compatibilité au-delà de la base et du calendrier exacts sans un run versionné.
