---
title: "WAN"
category: projects
date: 2026-07-31
tags: [project, wan, wan-video-generation]
aliases: ["WAN", "Wan", "Wan2.2 dyno"]
level: 2
source_sha256: 163affe162b36def00c920958f44219a2721b201bf53e3863d1cb126bc0de624
translation: machine
translated_at: '2026-10-24'
---
# WAN {#wan}

**Ligne de développement :** `project:wan` · fil `wan-video-generation`  
**Dernier événement :** 2026-07-31 · 3 événements datés depuis 2025-09-23 · **Recherche effectuée :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

WAN est une famille de modèles de génération vidéo destinée aux créateurs et aux développeurs : texte vers vidéo, image vers vidéo, vidéo pilotée par la parole ou par une référence, animation et remplacement de personnages. Wan2.2 reste une lignée de modèles locaux sous licence Apache-2.0 ; les API hébergées actuelles exposent des modèles plus récents, en versions 2.6 et 2.7. L'inférence locale du modèle A14B nécessite au moins 80 Go de VRAM dans l'exemple officiel. Verdict : utiliser WAN hébergé actuel pour la génération en production ; utiliser Wan2.2 lorsque des poids locaux et inspectables, ainsi que les accélérations développées par la communauté, sont importants.

## Ligne de développement {#development-line}

- **2025-09-23 — Alibaba Wan 2.5 apparaît comme modèle texte vers vidéo sur WaveSpeed.** Le 2025-09-23, une route de modèle WaveSpeed a identifié Alibaba Wan 2.5 comme offre texte vers vidéo. Il s'agit d'une étape importante de disponibilité dans l'écosystème, car elle a donné aux praticiens une route hébergée nommée pour utiliser cette version de WAN pour la génération vidéo.
- **2025-10-01 — Des ressources Wan 2.2 Lightning apparaissent pour des workflows texte vers vidéo en quatre étapes.** Le 2025-10-01, les ressources liées ont identifié une variante Dyno Wan 2.2 Lightning en quatre étapes, un artefact ComfyUI FP8 correspondant et une page de workflow. Il s'agit d'une étape pratique importante, car elle indique une voie d'inférence plus rapide et prête à l'emploi pour la génération texte vers vidéo avec Wan 2.2.
- **2026-07-31 — WAN expose une route de terrain de jeu temps réel.** Le 2026-07-31, le site WAN Create comprenait une route de terrain de jeu de laboratoire intitulée realtime. Il s'agit d'une étape importante de développement d'interface, car elle indique un point d'entrée interactif et temps réel pour WAN, distinct d'un lien de téléchargement de modèle ou de workflow par lots.

## Ce qui a changé {#what-changed}

2025-09-23 — Wan 2.5 apparaît comme API hébergée de génération vidéo à partir de texte ou d'image, avec audio synchronisé, sortie en 480p à 1080p et tâches de 5 ou 10 secondes. 2025-10-01 — le chemin communautaire Wan2.2-Lightning ajoute un répertoire de point de contrôle Dyno en quatre étapes pour le modèle de base Wan2.2 T2V-A14B ; son dépôt indique une taille de 28,6 Go pour ce répertoire, et l'artefact ComfyUI FP8 associé identifie la famille exacte de modèles T2V. 2026-07-31 — une route de terrain de jeu WAN Realtime était disponible, mais la page accessible n'expose ni nom de modèle, ni latence, ni tarification, ni contrat public d'utilisation. 2026-08-04 — une version canari de la même route Realtime était disponible ; sa page accessible n'expose pas non plus de détails de publication, elle ne constitue donc pas une preuve d'un modèle public distinct. 2025-07-28 — étape antérieure omise : Wan2.2 a publié son code et ses poids, et a intégré ComfyUI et Diffusers. 2025-09-19 — étape antérieure omise : Wan2.2-Animate-14B a ajouté l'animation et le remplacement de personnages. 2026-09-02 — la documentation hébergée actuelle répertorie les API vidéo Wan 2.6/2.7 ; Wan2.7 prend en charge des variantes texte vers vidéo et image vers vidéo en 720p/1080p, de 2 à 15 secondes, à 30 ips.

## Comment l'utiliser {#how-to-use-this}

À partir du 2025-10-01, les praticiens pouvaient évaluer Wan 2.2 via le workflow Lightning/ComfyUI en quatre étapes lorsque l'inférence vidéo à faible nombre d'étapes importait ; à partir du 2026-07-31, ils doivent aussi évaluer séparément le terrain de jeu temps réel public de WAN, distinct des workflows par lots. Considérer le point de terminaison canari du 2026-08-04 comme une infrastructure de déploiement non vérifiée, et non comme une modification publique des capacités.

1. Pour une tâche actuelle de texte vers vidéo hébergée, soumettre un prompt à l'API Wan, choisir une taille et une durée prises en charge, conserver l'identifiant de tâche renvoyé, puis interroger le statut plutôt que de renvoyer un travail en double.
  — <https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference>
2. Pour Wan2.2 en local, cloner le dépôt officiel, installer ses dépendances, télécharger le point de contrôle correspondant, puis exécuter generate.py avec la tâche et la résolution voulues.
  — <https://github.com/Wan-Video/Wan2.2>
3. Pour une expérimentation T2V accélérée de Wan2.2 en local, télécharger à la fois le point de contrôle de base A14B et les ressources LightX2V, puis transmettre le répertoire LoRA Lightning à la commande de génération officielle.
  — <https://huggingface.co/lightx2v/Wan2.2-Lightning>

## Bonnes pratiques {#best-practices}

- Fixer une graine pour la reproductibilité, mais ne pas considérer une graine fixe comme une garantie de sortie vidéo identique.
  — <https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference>
- Traiter la version du modèle, la résolution, la durée, l'audio et la région comme des paramètres de tâche explicites ; ils influent sur la disponibilité, le coût et les limites de sortie.
  — <https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference>
- Utiliser un workflow Wan2.2 local uniquement avec un matériel dimensionné pour celui-ci ; l'exemple officiel A14B mono-GPU en 720p indique un minimum de 80 Go de VRAM.
  — <https://github.com/Wan-Video/Wan2.2>
- Utiliser l'accélération de type Lightning comme complément communautaire du modèle de base correspondant, et non comme remplacement du point de contrôle de base.
  — <https://huggingface.co/lightx2v/Wan2.2-Lightning>

## Remplacé par ceci {#superseded-by-this}

- 2025-09-23 : considérer Wan 2.5 comme le point de terminaison WAN actuel est obsolète ; la documentation actuelle d'Alibaba répertorie les familles de modèles vidéo Wan 2.6 et Wan 2.7.
- 2025-10-01 : considérer l'actif Dyno Wan2.2 en quatre étapes comme le chemin WAN par défaut est obsolète pour la production hébergée ; il reste une option communautaire d'inférence locale.
- 2026-07-31 et 2026-08-04 : considérer l'une ou l'autre URL du terrain de jeu Realtime comme une spécification de produit documentée n'est pas étayé ; aucune des routes accessibles n'expose de contrat public.

## Encore inconnu {#still-unknown}

- Les pages Realtime accessibles et Realtime canari étaient des pages d'habillage sans modèle, date de publication, latence, quota ni information de tarification extractibles ; leurs événements du 2026-07-31 et du 2026-08-04 ne peuvent être caractérisés au-delà de la disponibilité de la route.
- L'événement daté WAN 2.5 est ici étayé par un fournisseur d'API tiers plutôt que par une annonce officielle accessible ; l'étendue exacte de sa publication initiale reste non vérifiée.
- WAN recouvre deux sujets opérationnellement différents : les poids locaux ouverts de Wan2.2 et les API hébergées Wan 2.5–2.7 ultérieures. Ils partagent un nom, mais ne doivent pas être traités comme des cibles de déploiement interchangeables.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference | Wan - référence de l'API texte vers vidéo | 2026-09-05 |
| https://www.alibabacloud.com/help/tc/model-studio/video-generate-edit-model/ | Liste des modèles de génération et d'édition vidéo | 2026-09-05 |
| https://github.com/Wan-Video/Wan2.2 | Wan2.2 — dépôt officiel | 2026-09-05 |
| https://huggingface.co/lightx2v/Wan2.2-Lightning | lightx2v/Wan2.2-Lightning | 2026-09-05 |
| https://huggingface.co/lightx2v/Wan2.2-Lightning/tree/main/Wan2.2-T2V-A14B-4steps-250928-dyno | Répertoire Wan2.2 Lightning Dyno en quatre étapes | 2026-09-05 |
| https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/blob/main/T2V/Wan2_2-T2V-A14B-HIGH_4_steps-250928-dyno-lightx2v_fp8_e4m3fn_scaled_KJ.safetensors | Artefact FP8 Kijai Wan2.2 T2V-A14B Dyno en quatre étapes | 2026-09-05 |
| https://wavespeed.ai/models/alibaba/wan-2.5/text-to-video | API Wan 2.5 texte vers vidéo sur WaveSpeed | 2026-09-05 |
| https://create.wan.video/lab/playground/realtime | Terrain de jeu Wan Realtime | 2026-09-05 |
| https://canary-create.wan.video/lab/playground/realtime | Route canari du terrain de jeu Wan Realtime | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:wan`, fil `wan-video-generation`, 3 événements datés du 2025-09-23 au 2026-07-31.
- **Note pratique :** À partir du 2025-10-01, les praticiens pouvaient évaluer Wan 2.2 via le workflow Lightning/ComfyUI en quatre étapes lorsque l'inférence vidéo à faible nombre d'étapes importait ; à partir du 2026-07-31, ils doivent aussi évaluer séparément le terrain de jeu temps réel public de WAN, distinct des workflows par lots. Considérer le point de terminaison canari du 2026-08-04 comme une infrastructure de déploiement non vérifiée, et non comme une modification publique des capacités.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
