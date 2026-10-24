---
title: "James Webb Space Telescope — Publication des premières images"
category: projects
tags: [first-images-release, james-webb-space-telescope, james_webb_space_telescope, project]
aliases: ["James Webb Space Telescope"]
level: 2
source_sha256: a6de2d602316d55dcb81c40d52d9406c0f6adb2f63e4ab380ff45755aeda1b8c
translation: machine
translated_at: '2026-10-24'
---
# James Webb Space Telescope — Publication des premières images {#james-webb-space-telescope-first-images-release}

**Ligne de développement :** `project:james-webb-space-telescope` · fil `first-images-release`  
**Événements :** 1 daté, 2022-07-12 → 2022-07-12 · **Recherche effectuée le :** 2026-09-04 · confiance : moyenne

## Description {#what-it-is}

James Webb Space Telescope est un observatoire infrarouge actif de la NASA, de l'ESA et de l'ASC, destiné aux astronomes qui analysent des données publiques d'observatoires spatiaux.

- MAST fournit des produits bruts, calibrés et de haut niveau.
- Le pipeline JWST, en open source, traite tous les instruments et modes d'observation à l'aide des fichiers de référence CRDS.

## Ligne de développement {#development-line}

- **2022-07-12 — Publication des premières images publiques de James Webb Space Telescope.** Webb est passé de la phase de mise en service à la diffusion scientifique publique le 2022-07-12. Cette publication a offert au public et à la communauté scientifique une première vue d'ensemble des capacités d'observation du télescope.

## Changements {#what-changed}

- **2022-07-12.** La comparaison SMACS 0723 entre Hubble et Webb a fait de la première image de champ profond un test direct des capacités du télescope. Il s'agissait d'une étape de diffusion scientifique publique, et non d'une modification matérielle.
- **2022-07-13.** Un élément multimédia a ajouté le spectre de transmission NIRISS de WASP-96 b, élargissant la publication initiale, qui ne comprenait que des images, à la spectroscopie des exoplanètes. Le document source est apparu le 2022-07-12 ; la date du 2022-07-13 correspond donc à la diffusion et non à un nouveau mode d'observation.
- **2026-09-04.** Webb reste en activité. MAST retraite les produits de données après chaque version trimestrielle des opérations ; les téléchargements antérieurs ne correspondent donc pas nécessairement aux produits calibrés actuels.

## Mode d'emploi {#how-to-use-this}

À partir du 2022-07-12, considérez les publications des premières images de JWST comme la frontière historique entre la mise en service et la diffusion des observations scientifiques publiques lorsque vous décrivez la maturité opérationnelle du projet.

1. Vérifiez que les observations requises sont publiques. Récupérez les données publiques de MAST de manière anonyme, ou authentifiez-vous avec vos identifiants MyST et une autorisation de programme pour les données à accès exclusif.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data>
2. Recherchez dans MAST Portal par programme, instrument, mode, coordonnées ou cible. Utilisez JWST Mission Search pour les filtres propres à JWST.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access>
3. Téléchargez d'abord le minimum de produits recommandé. Ne sélectionnez les fichiers bruts, intermédiaires, d'étoile-guide ou de référence que lorsque l'analyse en a besoin.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access>
4. Pour un retraitement, installez une version publiée du paquet jwst sous Linux ou macOS. Configurez CRDS avant d'importer le paquet, puis exécutez les étapes adaptées au mode d'observation.
  — <https://jwst-docs.stsci.edu/jwst-science-calibration-pipeline>
5. Pour une publication, consignez la version du pipeline et le contexte CRDS, citez les données et incluez la mention de remerciement requise pour la mission.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/citing-jwst-data>

## Bonnes pratiques {#best-practices}

- Commencez par les produits minimaux recommandés par MAST plutôt que de télécharger par défaut les données brutes. Ne récupérez les produits de plus bas niveau que pour un besoin de réduction défini.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access>
- Utilisez la version Operations du pipeline et son contexte CRDS par défaut compatible pour l'analyse générale. Les versions de développement ne sont pas la recommandation par défaut.
  — <https://jwst-docs.stsci.edu/jwst-science-calibration-pipeline>
- Consignez à la fois la version du logiciel jwst et le contexte CRDS chaque fois que les résultats dépendent d'un retraitement ou d'une substitution de contexte.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data/citing-jwst-data>
- Vérifiez l'état actuel de l'étalonnage et les problèmes connus avant d'interpréter un produit téléchargé comme définitif, car les produits d'archive et les versions d'étalonnage changent chaque trimestre.
  — <https://jwst-docs.stsci.edu/accessing-jwst-data>

## Remplacé par ce document {#superseded-by-this}

- La comparaison des premières images du 2022-07-12 comme base d'analyse est remplacée par la version actuelle de l'archive MAST, car les produits sont retraités après chaque version trimestrielle des opérations.
- La pratique antérieure à octobre 2024, consistant à associer un logiciel jwst publié à un contexte CRDS mobile, est obsolète. Chaque version du pipeline sélectionne désormais un contexte par défaut figé et compatible, et toute substitution doit être documentée.

## Points non élucidés {#still-unknown}

- La page ImgSli ne s'est pas affichée pendant la recherche : sa légende exacte, les versions des images sources et les paramètres de traitement n'ont pas pu être vérifiés.
- L'élément WASP-96 b est lui-même daté du 2022-07-12 ; la date d'événement du 2022-07-13 ne permet donc pas d'établir un changement distinct d'instrument ou de mission.
- Les deux enregistrements datés concernent un même télescope, mais deux résultats de premières images différents : une comparaison d'imagerie SMACS 0723 et un spectre de transmission de WASP-96 b.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://imgsli.com/MTE2Mjc3 | ImgSli item MTE2Mjc3 — Comparaison Hubble/JWST de SMACS 0723 ; la page ne s'est pas affichée pendant la recherche | 2026-09-04 |
| https://webbtelescope.org/contents/media/images/2022/032/01G72VSFW756JW5SXWV1HYMQK4?Collection=First+Images&news=true | Exoplanet WASP-96 b (NIRISS Transmission Spectrum) | 2026-09-04 |
| https://commons.wikimedia.org/wiki/File%3AExoplanet_WASP-96_b_%28NIRISS_Transmission_Spectrum%29_%282022-032-01G72VSFW756JW5SXWV1HYMQK4%29.png | File: Exoplanet WASP-96 b (NIRISS Transmission Spectrum) | 2026-09-04 |
| https://science.nasa.gov/mission/webb/webb-mission-timeline/ | Webb Mission Timeline | 2026-09-04 |
| https://science.nasa.gov/missions/webb/nasas-webb-delivers-deepest-infrared-image-of-universe-yet/ | NASA’s Webb Delivers Deepest Infrared Image of Universe Yet | 2026-09-04 |
| https://science.nasa.gov/mission/webb/ | James Webb Space Telescope | 2026-09-04 |
| https://jwst-docs.stsci.edu/accessing-jwst-data | Accessing JWST Data | 2026-09-04 |
| https://jwst-docs.stsci.edu/accessing-jwst-data/mast-web-access | MAST Web Access | 2026-09-04 |
| https://jwst-docs.stsci.edu/jwst-science-calibration-pipeline | JWST Science Calibration Pipeline | 2026-09-04 |
| https://jwst-docs.stsci.edu/accessing-jwst-data/citing-jwst-data | Citing JWST Data | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:james-webb-space-telescope`, fil `first-images-release`, 1 événement daté, 2022-07-12 → 2022-07-12.
- **Note pratique :** À partir du 2022-07-12, considérez les publications des premières images de JWST comme la frontière historique entre la mise en service et la diffusion des observations scientifiques publiques lorsque vous décrivez la maturité opérationnelle du projet.
- **Confiance :** moyenne. Les remplacements datés font foi pour déterminer ce qui est obsolète.
