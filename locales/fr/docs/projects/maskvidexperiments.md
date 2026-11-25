---
title: "MaskVidExperiments"
category: projects
date: 2026-08-23
tags: [maskvid-experiments, maskvidexperiments, project]
aliases: ["MaskVidExperiments"]
level: 2
source_sha256: 90af374ab2b5a258acf9af83234c1d538798068b8b2e736365350a1e14dc3ac9
translation: machine
translated_at: '2026-10-24'
---
# MaskVidExperiments {#maskvidexperiments}

**Ligne de développement :** `project:maskvidexperiments` · fil `maskvid-experiments`  
**Dernier événement :** 2026-08-23 · 1 événement daté depuis le 2026-08-23 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

MaskVidExperiments est un ensemble de nœuds ComfyUI destiné à ceux qui disposent déjà d'un masque image par image d'un objet et qui veulent le inpainter ou le stylistiser dans une vidéo sans recadrage qui tremble. — Subject Crop/Uncrop construit un recadrage stable pour l'ensemble du clip, puis réinsère l'objet traité avec un fondu sur les bords. — Mask Cleanup nettoie les zones courtes et bruitées du masque ; Mask To Latent Space convertit le masque vidéo dans la géométrie du VAE ; des nœuds distincts existent pour le latent audio et pour le Differential Diffusion doux. Limites : ComfyUI >=0.15.0 et GPLv3 sont annoncés ; ce n'est ni un segmenteur ni un modèle vidéo. Verdict : à utiliser pour l'édition locale par masque d'une vidéo déjà annotée, et non comme remplacement des masques, d'un modèle ou d'un workflow de production éprouvé.

## Ligne de développement {#development-line}

- **2026-08-23 — Le dépôt GitHub de MaskVidExperiments a été publiquement référencé.** Le lien daté renvoie à un projet v0.2.0 déjà existant ; dans l'historique de main consulté, aucun commit n'existe à cette date.

## Ce qui a changé {#what-changed}

2026-07-28 : le commit initial est marqué comme Initial release. 2026-07-29 : ajout de MVEx Differential Diffusion (Soft) pour des bords de masque doux selon les étapes de débruitage. 2026-08-04 : les masques commencent à être regroupés selon les frontières exactes des latents VAE ; ajout d'un nœud qui reporte le masque latent sur les images en pixels. 2026-08-08 : la mise en correspondance avec le cycle des chunks VAE et la réduction GPU avec repli CPU rapprochent la conversion du masque de la géométrie du modèle vidéo. 2026-08-10 : ajout de Frame Range Mask et des nœuds Audio Mask To Latent/Debug. 2026-08-13 : crop_scale=0 devient un mode de passage plein cadre pour comparer avec le pipeline de recadrage. 2026-08-14 : le minimum ComfyUI 0.15.0 est fixé et la publication automatique vers le Registry est ajoutée lors d'un bump de version. 2026-08-15 : les masques latents sont alignés sur la grille de tokens 2x2 de MiniMax H3. 2026-08-17 : les métadonnées du projet passent de 0.1.0 à 0.2.0 ; un upscale_megapixels négatif permet désormais le downscale. 2026-08-23 : le lien daté renvoie à un projet v0.2.0 déjà existant ; dans l'historique de main consulté, aucun commit n'existe à cette date.

## Comment l'utiliser {#how-to-use-this}

Au 2026-08-23, les praticiens peuvent utiliser le dépôt GitHub de MaskVidExperiments référencé comme source projet datée, tout en considérant son contenu et l'état de sa version comme non vérifiés tant qu'ils ne sont pas contrôlés séparément.

1. Clonez le dépôt dans ComfyUI/custom_nodes et redémarrez ComfyUI ; la documentation annonce un minimum v0.15.0 et aucune dépendance séparée au-delà de ComfyUI.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
2. Passez les images et le masque prêt dans Mask Cleanup en cas de bruit court, puis dans Subject Crop ; faites passer le recadrage dans votre sampler ou votre workflow d'inpainting, puis rétablissez-le via Subject Uncrop avec les images d'origine, les bboxes et les masques de recadrage.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
3. Pour un masque vidéo, connectez Mask To Latent Space au VAE, laissez compression=auto si le VAE est connecté, et transmettez le résultat à Set Latent Noise Mask ; n'utilisez manual que lorsque la géométrie du VAE est connue.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>

## Bonnes pratiques {#best-practices}

- Pour un mouvement de recadrage minimal, choisissez tracked ; combined convient à une fenêtre fixe unique, zoomed lorsque la proportion constante de l'objet compte. Consultez le debug : l'insertion exacte au pixel n'est conservée que sans redimensionnement du recadrage.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
- N'envoyez pas directement un masque vidéo en pixels dans Set Latent Noise Mask : utilisez Mask To Latent Space pour éviter de flouter le masque par un redimensionnement trilinéaire entre les images.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>
- Réglez crop_scale=0 pour comparer, à l'aide de deux bypass, le pipeline de recadrage avec le plein cadre avant de trancher pour un clip donné.
  — <https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md>

## Remplacé par cette version {#superseded-by-this}

- 2026-08-17 : les métadonnées du projet 0.1.0 sont remplacées par 0.2.0 (commit d98cc89).

## Toujours inconnu {#still-unknown}

- Une recherche distincte en chinois simplifié n'a fourni aucune source primaire ou d'implémentation accessible ; la piste de preuves en chinois reste non couverte.
- L'amont ne publie aucun benchmark de VRAM, de vitesse, de clips longs ou de qualité de stabilité temporelle ; le graphe n'a pas été exécuté dans un environnement propre.
- Le minimum ComfyUI 0.15.0 et la prise en charge de la géométrie des VAE nommés sont confirmés par la documentation, mais il n'existe pas de matrice complète des versions de ComfyUI, des modèles vidéo et du matériel testés.
- Avant toute application en production, il faut un commit figé et une vérification distincte de la compatibilité de licence GPLv3.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/drozbay/MaskVidExperiments | MaskVidExperiments — dépôt GitHub | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/README.md | README de MaskVidExperiments au commit d98cc89 | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/commits/main | Historique des commits de main de MaskVidExperiments | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/commit/d98cc899c1fac718acf81cde1735bf57281097cf | Bump version to 0.2.0 — commit d98cc89 | 2026-09-06 |
| https://github.com/drozbay/MaskVidExperiments/blob/d98cc899c1fac718acf81cde1735bf57281097cf/pyproject.toml | Métadonnées du projet au commit d98cc89 | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:maskvidexperiments`, fil `maskvid-experiments`, 1 événement daté du 2026-08-23 au 2026-08-23.
- **Note pratique :** Au 2026-08-23, les praticiens peuvent utiliser le dépôt GitHub de MaskVidExperiments référencé comme source projet datée, tout en considérant son contenu et l'état de sa version comme non vérifiés tant qu'ils ne sont pas contrôlés séparément.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
