---
title: "FLUX Video Upscale — Black Forest Labs"
category: projects
date: 2026-08-21
tags: [black-forest-labs, flux-video-upscale, project]
aliases: ["FLUX Video Upscale"]
level: 2
source_sha256: 1d7cf6ba7163e65ec8d2649189ce2027fa402c8ce9c87c197f63062ad925d17c
translation: machine
translated_at: '2026-10-24'
---
# FLUX Video Upscale — Black Forest Labs {#flux-video-upscale-black-forest-labs}

**Ligne de développement :** `project:flux-video-upscale` · fil `black-forest-labs`  
**Dernier événement :** 2026-08-21 · 1 événement daté depuis le 2026-08-21 · **Recherche effectuée :** 2026-09-05 · confiance : élevée

## Présentation {#what-it-is}

FLUX Video Upscale est un point d'accès de super-résolution vidéo FLUX 3 destiné aux utilisateurs de l'API.

- Agrandissement vidéo de 1,5× à 3×, jusqu'à la 4K.
- Mode Precise pour les séquences sensibles à l'identité et mode Creative pour les détails générés.
- Préservation de la piste audio source.

Les entrées sont limitées à 20 secondes, 50 Mo et 2560×1440 ; les images de sortie sont plafonnées à environ 14,4 MP.

Utilisez Precise pour les visages, les produits et les éléments de marque ; utilisez Creative pour les paysages et textures générés, lorsque le détail importe davantage que l'identité exacte.

## Ligne de développement {#development-line}

- **2026-08-21 — Black Forest Labs a présenté FLUX Video Upscale.** Le 2026-08-21, Black Forest Labs a publié un lien vers une annonce officielle sur son blog, la documentation produit et un modèle accessible dans le playground pour FLUX Video Upscale. Ces liens officiels établissent la présentation publique, mais ne détaillent ni les capacités, ni la disponibilité, ni la tarification, ni les performances.

## Changements {#what-changed}

2026-08-21 — FLUX Video Upscale est devenu disponible en tant qu'outil autonome `POST /v1/flux-tools/video-upscale-v1`, à la suite de la version publiée par BFL le 20 août. Le lancement a ajouté la super-résolution vidéo de 1,5× à 3×, deux modes `creativity`, la préservation de l'audio et une facturation limitée à la sortie.

2026-08-26 — Le catalogue actuel des outils de BFL répertorie Video Upscale aux côtés de ses autres points d'accès d'édition, confirmant son rôle d'outil FLUX (FLUX Tool) avec le même flux asynchrone de soumission puis d'interrogation.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-08-21, nous évaluons FLUX Video Upscale à travers le flux de travail documenté de Black Forest Labs et le playground associé, plutôt que de le traiter comme une capacité non annoncée ou non documentée.

1. Préparez un fichier MP4 d'au plus 20 secondes, puis hébergez-le à une URL HTTPS accessible ou encodez-le en base64.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
2. Envoyez en POST `input_video`, un `upscale_factor` compris entre 1,5 et 3, et `creativity` vers `/v1/flux-tools/video-upscale-v1`.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
3. Interrogez le `polling_url` renvoyé jusqu'à ce que le statut soit `Ready`, puis téléchargez `result.sample` avant l'expiration de son URL signée.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>

## Bonnes pratiques {#best-practices}

- Utilisez `creativity: 0` pour les visages, les produits, les logos et tout autre élément dont l'identité doit rester stable.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
- Utilisez `creativity: 1` pour les séquences générées, les textures, les foules et les paysages ; ajoutez un court prompt de contenu uniquement lorsqu'orienter les détails inventés s'avère utile.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>
- Agrandissez la source la moins compressée après montage et découpage, afin que les artefacts ne soient pas amplifiés et que la facturation limitée à la sortie ne porte que sur les séquences conservées.
  — <https://docs.bfl.ai/flux_tools/flux_video_upscale>

## Remplacé par ceci {#superseded-by-this}

- Aucun élément marqué comme obsolète pour l'instant.

## Points restant inconnus {#still-unknown}

- Notre entrée date l'événement du 2026-08-21, alors que la note de version officielle de BFL et le blog datent le lancement du 2026-08-20 ; la diffusion a probablement été consignée un jour plus tard.
- Nous n'avons pas obtenu de réponse du playground accessible de manière indépendante pendant la recherche ; les commandes actuelles de l'interface navigateur et la disponibilité selon les formules de compte n'ont donc pas été vérifiées.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://bfl.ai/blog/flux-video-upscale | FLUX Upscale: 2K and 4K for Video | 2026-09-05 |
| https://docs.bfl.ai/flux_tools/flux_video_upscale | FLUX Video Upscale | 2026-09-05 |
| https://docs.bfl.ai/release-notes | Release Notes | 2026-09-05 |
| https://help.bfl.ai/articles/5950329591-what-are-the-flux-tools | What are the FLUX Tools? | 2026-09-05 |
| https://bfl.ai/video-upscaler | FLUX Video Upscale: AI Video Upscaler to 1080p, 2K and 4K | 2026-09-05 |

## Synthèse pour agent {#agent-brief}

- **Sujet :** `project:flux-video-upscale`, fil `black-forest-labs`, 1 événement daté du 2026-08-21 au 2026-08-21.
- **Note pratique :** À partir du 2026-08-21, évaluer FLUX Video Upscale à travers le flux de travail documenté de Black Forest Labs et le playground associé, plutôt que de le traiter comme une capacité non annoncée ou non documentée.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
