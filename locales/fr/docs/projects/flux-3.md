---
title: "FLUX 3"
category: projects
date: 2026-08-05
tags: [flux-3, flux-3-development, flux_3, project]
aliases: ["FLUX 3"]
level: 2
source_sha256: bfbeac1ecf848db22f2a80bbbdaa68e416c9028bc8020e43daab24f145eee645
translation: machine
translated_at: '2026-10-24'
---
# FLUX 3 {#flux-3}

**Ligne de développement :** `project:flux-3` · fil `flux-3-development`  
**Dernier événement :** 2026-08-05 · 2 datés depuis le 2026-07-24 · **Recherché le :** 2026-09-04 · confiance : moyenne

## Présentation {#what-it-is}

FLUX 3 est un modèle vidéo en préversion de BFL destiné aux créateurs et aux équipes API qui réalisent de courts plans audiovisuels.

- Génération vidéo : texte vers vidéo, image ou images clés vers vidéo, et prolongation de vidéo, exécutées via l'endpoint flux-3-video.
- Spécification de sortie : vidéo à 24 ips avec parole synchronisée, effets sonores et ambiance.

## Ligne de développement {#development-line}

- **2026-07-24 — Black Forest Labs a publié une mise à jour de blog sur FLUX 3.** FLUX 3 est entré en accès anticipé en tant que modèle multimodal unifié. Black Forest Labs a échelonné séparément l'accès à Video, Image, Action et Dev.
- **2026-08-05 — FLUX 3 était relié à travers les surfaces produit de Black Forest Labs.** Les pages du modèle et du Quick Start ne comportent aucune date. La route Playground liée renvoie une erreur.

## Ce qui a changé {#what-changed}

2026-07-24 — Le matériel de lancement cité est daté du 2026-07-23 : FLUX 3 est entré en accès anticipé en tant que modèle multimodal unifié, tandis que l'accès à Video, Image, Action et Dev était échelonné séparément. 2026-08-04 — BFL a rendu disponible au public une première version de FLUX 3 Video via son API et à certains partenaires sélectionnés. 2026-08-05 — Nous ne pouvons vérifier aucune version distincte des capacités : les pages du modèle et du Quick Start ne sont pas datées, et la route Playground associée renvoie désormais une erreur. 2026-08-20 — FLUX Upscale a été lancé comme endpoint distinct, capable de régénérer une vidéo jusqu'à la résolution native 4K.

## Mode d'emploi {#how-to-use-this}

Consultez la page du modèle FLUX 3, la documentation de démarrage rapide et le playground prompt-to-image datés du 2026-08-05 avant de tester FLUX 3, afin de vérifier les fonctionnalités et l'accès auprès des sources primaires.

1. Créez un compte BFL, ajoutez des crédits, puis utilisez le Playground ou l'API.
  — <https://docs.bfl.ai/flux_3>
2. Pour un nouveau clip, envoyez en POST `mode=t2v`, un prompt et une durée facultative à l'endpoint `/v1/flux-3-video` avec votre clé API BFL.
  — <https://docs.bfl.ai/flux_3>
3. Pour une vidéo guidée par l'image, utilisez `mode=i2v` avec des images clés ; pour une extension, utilisez `mode=v2v` avec `start_video`.
  — <https://docs.bfl.ai/flux_3>
4. Interrogez le `polling_url` renvoyé jusqu'à ce que la tâche soit Ready, puis téléchargez le résultat avant l'expiration de son URL signée.
  — <https://docs.bfl.ai/flux_3>
5. Prototypez avec `draft=true` ; envoyez le `draft_cache` du résultat sélectionné dans `mode=draft_enhance` pour rendre ce même plan en qualité maximale.
  — <https://docs.bfl.ai/flux_3>

## Bonnes pratiques {#best-practices}

- Utilisez draft et draft_enhance après avoir validé un aperçu, car un rendu complet neuf peut réinterpréter le plan.
  — <https://docs.bfl.ai/flux_3>
- Épinglez les images clés à des horodatages précis lorsqu'une transition doit être contrôlée ; i2v accepte de une à dix images, y compris les épingles de début et de fin.
  — <https://docs.bfl.ai/flux_3>
- Téléchargez rapidement un résultat Ready, car son URL signée expire après environ deux heures.
  — <https://docs.bfl.ai/flux_3>
- Utilisez le mode Upscale Precise lorsque l'identité ou le détail de référence doivent rester cohérents, car le mode Creative peut modifier ou remplacer l'identité.
  — <https://bfl.ai/blog/flux-video-upscale>

## Remplacé par cette information {#superseded-by-this}

- 2026-08-04 : « FLUX 3 Video n'est disponible que via l'accès anticipé » est obsolète ; BFL a rendu disponible au public une version initiale via son API et à certains partenaires sélectionnés.

## Points encore inconnus {#still-unknown}

- L'URL Playground du 2026-08-05 renvoie actuellement une erreur interne ; nous ne pouvons donc pas vérifier le modèle, le prompt et la sortie d'origine.
- Le lot de sources du 2026-08-05 mélange une route Playground prompt-to-image avec la documentation actuelle de BFL, qui présente FLUX 3 comme un modèle vidéo ; sans le texte source d'origine, nous ignorons s'il s'agit du même produit FLUX 3 ou d'un simple lien générique vers un tableau de bord.
- Les sources publiques de première partie consultées n'établissent ni date de sortie ni endpoint public pour FLUX 3 Image, FLUX 3 Dev ou FLUX 3 Action au-delà de leurs plans de lancement échelonnés.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://bfl.ai/blog/flux-3 | FLUX 3 - Real World Models: Towards Multimodal Flow Models as the Backbone of Visual Intelligence. | 2026-09-04 |
| https://bfl.ai/blog/flux-3-video | FLUX 3 Video, Part 1: Generation | 2026-09-04 |
| https://bfl.ai/blog/flux-video-upscale | FLUX Upscale: 2K and 4K for Video | 2026-09-04 |
| https://docs.bfl.ai/flux_3 | FLUX 3 - Black Forest Labs | 2026-09-04 |
| https://docs.bfl.ai/quick_start/introduction | The frontier of visual intelligence - Black Forest Labs | 2026-09-04 |
| https://help.bfl.ai/articles/7655484417-what-flux-models-are-available | Quels modèles FLUX sont disponibles ? | Black Forest Labs Knowledge Base | 2026-09-04 |
| https://bfl.ai/models/flux-3 | FLUX 3: One Multimodal Model | Black Forest Labs | 2026-09-04 |

## Résumé pour agent {#agent-brief}

- **Sujet :** `project:flux-3`, fil `flux-3-development`, 2 événements datés du 2026-07-24 au 2026-08-05.
- **Note pratique :** Consultez la page du modèle FLUX 3, la documentation de démarrage rapide et le playground prompt-to-image datés du 2026-08-05 avant de tester FLUX 3, afin de confirmer les capacités et l'éligibilité auprès des sources primaires.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est devenu obsolète.
