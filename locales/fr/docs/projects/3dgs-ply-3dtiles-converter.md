---
title: "3DGS-PLY-3DTiles-Converter"
category: projects
date: 2026-08-06
tags: [3dgs-ply-3dtiles-converter, 3dgs_ply_3dtiles_converter, project]
aliases: ["3DGS-PLY-3DTiles-Converter"]
level: 3
source_sha256: 6185a5ceb4c747a0c1d6eb34c90b5c2f5b57152167758f6942ceead9a3f56f14
translation: machine
translated_at: '2026-10-24'
---
# 3DGS-PLY-3DTiles-Converter {#3dgs-ply-3dtiles-converter}

**Ligne de développement :** `project:3dgs-ply-3dtiles-converter` · fil `3dgs-ply-3dtiles-converter`  
**Dernier événement :** 2026-08-06 · 1 daté depuis le 2026-08-06 · **Recherche effectuée :** 2026-09-06 · confiance : moyenne

## Présentation {#what-it-is}

3DGS-PLY-3DTiles-Converter est un outil en ligne de commande Node.js, une bibliothèque et une API navigateur ESM permettant de convertir des fichiers PLY de Gaussian Splatting au format GraphDECO ou KHR-natif en un tileset 3D Tiles explicite.

- Tuiles LOD adaptatives avec fichiers GLB compressés en SPZ.
- Réduction autonome de fichiers PLY sans génération de tileset.
- Positionnement WGS84 et matrice de transformation racine.

L'outil en ligne de commande Node.js nécessite Node.js 18+ ; l'API navigateur s'exécute dans un Web Worker et renvoie MEMORY_EXHAUSTED lorsque la mémoire est épuisée.

Le convertisseur convient à la diffusion de grandes scènes 3DGS via 3D Tiles, mais EXT_splat_opacity n'est pas un format universellement pris en charge par les visualiseurs.

## Ligne de développement {#development-line}

- **2026-08-06 — Dépôt source de 3DGS-PLY-3DTiles-Converter et site public enregistrés.** Le 2026-08-06, 3DGS-PLY-3DTiles-Converter a été enregistré avec un dépôt source GitHub et un site public Vercel. Cela établit un point de référence public daté pour le projet, sans affirmer de version, de fonctionnalité ou d'événement de lancement particulier.

## Modifications {#what-changed}

- 2026-08-04 — La GitHub Release v0.6.0 a ajouté la commande autonome simplify pour la réduction directe de fichiers PLY avec --ratio ou --target-count ; l'en-tête du changelog date cette version du 2026-08-05.
- 2026-08-05 — La v0.6.1 a ajouté l'API navigateur ESM avec traitement local dans un Web Worker et porté le memoryBudget par défaut de 3 à 4 Go ; l'en-tête du changelog date la version du 2026-08-06.
- 2026-08-06 — La v0.6.2 a activé EXT_splat_opacity v2 par défaut pour la conversion en CLI, Node.js et navigateur, en conservant une option de désactivation explicite.
- 2026-08-28 — La v0.6.3 a ajouté la traçabilité package/version aux sorties GLB et tileset et corrigé les métadonnées obligatoires des Gaussian splats.
- 2026-08-30 — L'index des paquets enregistre la v0.6.4, mais les notes de version primaires sur son contenu ne sont pas disponibles.
- 2026-08-31 — L'index des paquets enregistre la v0.6.5, mais les notes de version primaires sur son contenu ne sont pas disponibles.

## Mode d'emploi {#how-to-use-this}

1. Installez le paquet dans un projet Node.js 18+ : npm install 3dgs-ply-3dtiles-converter.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
2. Convertissez un fichier PLY : 3dgs-ply-3dtiles-converter scene.ply out_tiles ; pour la CI, ajoutez --no-open-inspector.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
3. Pour le géoréférencement, passez soit --coordinate [lat,long,height], soit --transform avec une matrice 4×4, puis vérifiez source_coordinate_system dans build_summary.json.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
4. Si nous n'avons besoin que d'un fichier PLY réduit, utilisez simplify --ratio 0.5 ou simplify --target-count 250000.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/blob/main/Splat-Simplify.md>

## Bonnes pratiques {#best-practices}

- Ne pointez pas vers output_dir un répertoire existant contenant des données précieuses : la conversion standard le vide avant de le reconstruire ; utilisez --continue pour les exécutions interrompues.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
- N'activez EXT_splat_opacity que pour un chemin vérifié avec 3D-Tiles-RendererJS-3DGS-Plugin ; les autres visualiseurs peuvent ignorer cette extension et revenir au SPZ standard.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter>
- Épinglez la version du convertisseur et conservez build_summary.json : la v0.6.3 écrit la traçabilité package/version et corrige les métadonnées obligatoires pour le contenu de splats.
  — <https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/releases>
- Pour l'intégration avec three.js, générez d'abord les 3D Tiles : le plugin de rendu associé charge les fichiers tileset/GLB, et non le PLY d'origine.
  — <https://github.com/WilliamLiu-1997/3D-Tiles-RendererJS-3DGS-Plugin>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-05 — Déployer un site ou un worker séparé pour la conversion navigateur est obsolète : la v0.6.1 a ajouté l'API navigateur ESM avec un Web Worker intégré.
- 2026-08-06 — Les intégrations lisant l'ancien opacityAccessor Float32 doivent passer à sourceOpacityAccessor et coverageBoostRatioAccessor v2, ou utiliser le repli SPZ standard.
- 2026-08-28 — Privilégiez la v0.6.3+ pour les nouvelles sorties : elle enregistre systématiquement colorSpace, les accesseurs SH VEC3 et les métadonnées obligatoires opacity/SH0.

## Points inconnus {#still-unknown}

- Les GitHub Releases et le CHANGELOG primaires s'arrêtent à la v0.6.3, alors que l'index des paquets liste les v0.6.4 et v0.6.5 les 2026-08-30 et 2026-08-31. Les notes de version primaires de ces deux versions étant indisponibles, nous excluons leurs fonctionnalités des recommandations.
- Les GitHub Releases et le CHANGELOG diffèrent d'un jour calendaire pour les v0.6.0 et v0.6.1 ; les horodatages de version n'indiquent pas de fuseau horaire. La chronologie ci-dessus utilise la date de la GitHub Release et conserve cet écart.
- Nous n'avons pas pu consulter de manière indépendante https://3dgs-ply-3dtiles-converter.vercel.app/ ; ses fonctionnalités actuelles et leur cohérence avec le paquet et l'API navigateur restent non confirmées.
- La recherche sur la voie chinoise n'a donné aucune source primaire en chinois ni aucun rapport d'exploitation reproductible.
- La compatibilité des visualiseurs ne dispose pas d'une matrice confirmée ; seul le plugin de rendu associé a prouvé la prise en charge de EXT_splat_opacity.
- event_findings omis du schéma de base ?

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter | GitHub — WilliamLiu-1997/3DGS-PLY-3DTiles-Converter | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/blob/main/CHANGELOG.md | GitHub — 3DGS-PLY-3DTiles-Converter CHANGELOG.md | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/releases | GitHub — 3DGS-PLY-3DTiles-Converter Releases | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3DGS-PLY-3DTiles-Converter/blob/main/Splat-Simplify.md | GitHub — Voxel-Based Gaussian Splat Simplification | 2026-09-07 |
| https://github.com/WilliamLiu-1997/3D-Tiles-RendererJS-3DGS-Plugin | GitHub — 3D-Tiles-RendererJS-3DGS-Plugin | 2026-09-07 |
| https://greenflagged.dev/packages/3dgs-ply-3dtiles-converter | Greenflagged — 3dgs-ply-3dtiles-converter package history | 2026-09-07 |

## Consigne pour l'agent {#agent-brief}

- **Sujet :** `project:3dgs-ply-3dtiles-converter`, fil `3dgs-ply-3dtiles-converter`, 1 événement daté du 2026-08-06 au 2026-08-06.
- **Note pratique :** Voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
