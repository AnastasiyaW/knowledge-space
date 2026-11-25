---
title: "UnitySplats"
category: projects
date: 2026-07-26
tags: [project, unitysplats]
aliases: ["UnitySplats"]
level: 2
source_sha256: a394280ffc62752502069e286d6f86af62a1fb248768030c3fa7f621101896c3
translation: machine
translated_at: '2026-10-24'
---
# UnitySplats {#unitysplats}

**Ligne de développement :** `project:unitysplats` · fil `unitysplats`  
**Dernier événement :** 2026-07-26 · 1 événement daté depuis le 2026-07-26 · **Recherche effectuée le :** 2026-09-05 · fiabilité : élevée

## Présentation {#what-it-is}

UnitySplats est un package Unity 6 permettant d'importer, de charger et de rendre des 3D Gaussian Splats, sans avoir à développer un moteur de rendu from scratch. Il prend en charge les formats PLY, SOG, SPZ et KHR_gaussian_splatting GLB ; les pipelines Built-in, URP et HDRP ; le chargement à l'exécution depuis un fichier, un tableau d'octets ou un flux ; ainsi que le tri GPU et CPU. La version minimale du moteur est Unity 6000.0 ; WebGL 2 utilise un tri CPU sur le thread principal et n'est pas adapté aux grandes scènes non compressées. Verdict : à utiliser lorsqu'un projet Unity a besoin de lecture de splats multi-formats, mais il convient de benchmarker le GPU cible et le chemin de rendu avant de s'engager pour un déploiement mobile, VR ou web.

## Ligne de développement {#development-line}

- **2026-07-26 — Références publiques du projet UnitySplats.** Le 2026-07-26, UnitySplats a été associé à un dépôt GitHub public et à une page d'expérience Arloopa. Ensemble, ces références datées établissent un point de repère public pour le développement du projet.

## Ce qui a changé {#what-changed}

2026-07-26 — UnitySplats a été présenté comme un package Unity open source ; la version initiale v1.0.0 du dépôt lié, datée du 2026-07-22, a introduit la base d'import multi-formats et de rendu à l'exécution. 2026-08-18 — la v1.2.0 a corrigé les défauts d'ordre de profondeur du tri CPU sous Direct3D 11 et de sélection du viewport.

## Mode d'emploi {#how-to-use-this}

À partir du 2026-07-26, les praticiens peuvent utiliser le dépôt UnitySplats et l'expérience Arloopa associée comme points de départ pour évaluer le projet, tout en vérifiant les détails d'implémentation avant toute adoption.

1. Ajoutez le registre OpenUPM pour le scope com.netpyoung et la dépendance Git UnitySplats dans Packages/manifest.json, ou installez d'abord Unity.WebP puis UnitySplats depuis les URL Git dans le Package Manager.
  — <https://github.com/arloopa/UnitySplats>
2. Pour URP, ajoutez Gsplat URP Feature au renderer actif ; pour HDRP, ajoutez Gsplat HDRP Pass dans un Custom Pass Volume avant le rendu transparent.
  — <https://github.com/arloopa/UnitySplats>
3. Importez un PLY binaire, un SOG, un SPZ ou un GLB compatible dans Assets, choisissez l'importeur GLB d'UnitySplats si nécessaire, puis placez le GsplatAsset généré dans la scène.
  — <https://github.com/arloopa/UnitySplats>
4. Pour un contenu à l'exécution, chargez un chemin local avec GsplatRuntimeLoader.LoadFile ou récupérez des données via une URI avec UnityWebRequest, puis transmettez les octets à GsplatRuntimeLoader.Load ; créez et détruisez les objets Unity sur le thread principal.
  — <https://github.com/arloopa/UnitySplats>

## Bonnes pratiques {#best-practices}

- Privilégiez Vulkan sous Android et Vulkan ou Direct3D 12 sous Windows ; Direct3D 11 et OpenGL utilisent le tri CPU portable.
  — <https://github.com/arloopa/UnitySplats>
- Utilisez des assets Spark-packed pour réduire la mémoire et accélérer l'upload ; réservez Uncompressed aux cas nécessitant des valeurs exactes dans le projet.
  — <https://github.com/arloopa/UnitySplats>
- Gardez le tri inter-renderers activé pour les renderers Spark qui se chevauchent sur les cibles Vulkan, Direct3D 12 et Metal compatibles ; il ne peut pas fournir d'ordre fusionné sur les chemins de tri CPU.
  — <https://github.com/arloopa/UnitySplats>
- Pour WebGL 2, utilisez la compression Spark et des nombres de splats modérés, car le tri est synchrone sur le thread principal d'Unity et la mémoire du navigateur est limitée.
  — <https://github.com/arloopa/UnitySplats>

## Ce qui est remplacé {#superseded-by-this}

- 2026-08-18 — la v1.2.0 remplace l'ordre de profondeur sur 16 bits du fallback CPU Direct3D 11 et le comportement de tri de la vue Scene dérivé de la caméra Main.
- 2026-07-22 — la v1.1.0 modifie la posture antérieure, optionnelle, du tri inter-renderers en activant par défaut le tri des renderers Spark compatibles, tout en migrant une fois les paramètres existants.

## Points non établis {#still-unknown}

- Aucun benchmark de performance primaire pour un nombre de splats donné, une classe d'appareil, une cible de fréquence d'images ou une configuration XR n'a été trouvé dans les sources examinées.
- L'URL de l'expérience ARLOOPA a été fournie avec l'événement mais n'a pas renvoyé de contenu lisible lors de la recherche ; elle n'est donc pas utilisée comme preuve.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://github.com/arloopa/UnitySplats | arloopa/UnitySplats — dépôt GitHub et documentation d'installation | 2026-09-05 |
| https://raw.githubusercontent.com/arloopa/UnitySplats/main/CHANGELOG.md | Journal des modifications d'UnitySplats | 2026-09-05 |

## Fiche agent {#agent-brief}

- **Sujet :** `project:unitysplats`, fil `unitysplats`, 1 événement daté du 2026-07-26 au 2026-07-26.
- **Note pratique :** À partir du 2026-07-26, les praticiens peuvent utiliser le dépôt UnitySplats et l'expérience Arloopa associée comme points de départ pour évaluer le projet, tout en vérifiant les détails d'implémentation avant toute adoption.
- **Fiabilité :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
