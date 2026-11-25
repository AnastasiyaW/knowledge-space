---
title: "Auto1111SDK"
category: projects
date: 2024-03-05
tags: [auto1111sdk, auto1111sdk-development, project]
aliases: ["Auto1111SDK"]
level: 2
source_sha256: 0e20f3f6ea5b1e109eecf120ee1313705d78f164c87a8c1b598648ab417efc3d
translation: machine
translated_at: '2026-10-24'
---
# Auto1111SDK {#auto1111sdk}

**Ligne de développement :** `project:auto1111sdk` · fil `auto1111sdk-development`  
**Dernier événement :** 2024-03-05 · 2 événements datés depuis 2024-02-06 · **Consulté le :** 2026-09-04 · confiance : moyenne

## Description {#what-it-is}

Auto1111SDK est une bibliothèque Python destinée aux développeurs qui pilotent des workflows Stable Diffusion locaux depuis du code, plutôt que depuis l'interface WebUI d'Automatic1111.

- Text-to-image, image-to-image, inpainting, outpainting et upscale Stable Diffusion.
- Upscaling ESRGAN/Real-ESRGAN, téléchargements CivitAI, prise en charge de VAE personnalisés et de SDXL, et une interface ControlNet.

## Ligne de développement {#development-line}

- **2024-02-06 — Apparition du dépôt du projet Auto1111SDK et du notebook Colab.** Le projet utilisait le chemin de dépôt personnel `saketh12/Auto1111SDK` ainsi qu'une démo Colab.
- **2024-03-05 — Apparition du dépôt de l'organisation Auto1111SDK avec le notebook Colab.** Le 2024-03-05, le dépôt a été déplacé sous l'organisation GitHub Auto1111SDK, avec le notebook Colab associé. Ce changement marque un point d'entrée public, mais les liens ne permettent pas de savoir s'il s'agissait d'une migration de dépôt, d'une publication ou d'une republication.

## Évolutions {#what-changed}

Le développement d'Auto1111SDK s'est arrêté au début de 2024, sans version ultérieure sur PyPI. Le 2024-02-06, le projet a démarré sous le dépôt personnel `saketh12/Auto1111SDK` avec une démo Colab. Le 2024-02-16, PyPI a publié la version 0.0.95, qui reste la dernière version de son historique. Le 2024-03-05, le chemin du dépôt est devenu `Auto1111SDK/Auto1111SDK` tout en conservant le même fichier Colab ; cela traduit un changement de chemin de publication et non l'arrivée de nouveau code. Le 2026-09-04, le README GitHub documente toujours une installation uniquement via virtualenv, l'ancien chemin d'installation Git personnel, et ControlNet en FP32 uniquement. Le paquet est désormais une dépendance héritée dont la compatibilité avec les environnements d'exécution actuels n'est pas vérifiée.

## Mode d'emploi {#how-to-use-this}

À partir du 2024-03-05, considérez le dépôt de l'organisation Auto1111SDK comme le point d'entrée historique du projet, et vérifiez séparément la configuration actuelle.

1. Créez un environnement virtuel Python propre ; le projet recommande explicitement un virtualenv et indique que Conda n'est pas pris en charge.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
2. Installez la dernière version reproductible du paquet avec `pip install auto1111sdk==0.0.95`, puis vérifiez la version et les fichiers sur PyPI.
  — <https://pypi.org/project/auto1111sdk/>
3. Placez un checkpoint local compatible ou un fichier `.safetensors` sur le disque, instanciez `StableDiffusionPipeline(path)`, et appelez `generate_txt2img` avec un prompt, des dimensions et un nombre d'étapes.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
4. Enregistrez la première image générée avec `output[0].save(...)` ; utilisez ce flux minimal comme test de fumée de l'environnement avant d'ajouter un workflow plus complexe.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
5. Pour ControlNet, créez un `ControlNetModel` avec le nom du modèle sans son extension et une image d'entrée, transmettez-le au pipeline, et prévoyez de la VRAM en FP32.
  — <https://github.com/Auto1111SDK/Auto1111SDK>

## Bonnes pratiques {#best-practices}

- Utilisez un environnement virtuel isolé plutôt que Conda ; c'est la seule limite de prise en charge d'environnement indiquée en amont.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
- Figez les versions d'Auto1111SDK, de Python, de PyTorch, de CUDA et des poids de modèles dans un lockfile ou une image : le dernier paquet publié est la version pré-alpha 0.0.95 du 2024-02-16.
  — <https://pypi.org/project/auto1111sdk/>
- N'utilisez pas la commande du README `pip install git+https://github.com/saketh12/Auto1111SDK.git`, non figée, pour un workflow reproductible ; si une installation depuis les sources est nécessaire, utilisez une révision source immuable et validée.
  — <https://github.com/Auto1111SDK/Auto1111SDK>
- Considérez ControlNet comme FP32 uniquement et mesurez la mémoire GPU avant de vous y engager ; ne supposez pas que la prise en charge FP16 prévue dans le README ait été livrée.
  — <https://github.com/Auto1111SDK/Auto1111SDK>

## Remplacé par ceci {#superseded-by-this}

- 2024-02-06 — le lien personnel `saketh12/Auto1111SDK` est remplacé comme référence canonique par le chemin d'organisation enregistré le 2024-03-05 ; les deux pointent aujourd'hui vers le même projet nommé.
- 2024-02-16 — « installer la dernière version » ne doit pas être interprété comme un support de diffusion de génération actuelle : cela correspond à la version pré-alpha 0.0.95, publiée le 2024-02-16.
- 2024-03-05 — considérer l'installation depuis les sources Git comme une preuve d'un support ControlNet plus récent est obsolète ; le README actuel documente toujours ControlNet en FP32 uniquement.

## Points restant inconnus {#still-unknown}

- Le notebook Colab à l'adresse `https://colab.research.google.com/drive/1SekiJ-mdB2V8ogWbyRyF_yDnoMuDGWTl` n'a pas pu être consulté sans session Google valide ; son environnement d'exécution actuel, ses versions de paquets figées, son matériel et son état d'exécution ne sont donc pas vérifiés.
- Les liens datés établissent un changement de chemin GitHub, du personnel vers l'organisation, le 2024-03-05, mais ne permettent pas de savoir s'il s'agissait d'un transfert de dépôt, d'un miroir ou d'une publication de code ; aucune note de version ni aucun diff de commit du 2024-03-05 n'était disponible.
- La compatibilité actuelle avec Python, PyTorch, CUDA et les formats de modèles de 2026 n'est pas établie par les sources consultées.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/Auto1111SDK/Auto1111SDK | README du dépôt Auto1111SDK/Auto1111SDK | 2026-09-04 |
| https://pypi.org/project/auto1111sdk/ | Projet PyPI auto1111sdk et historique des versions | 2026-09-04 |
| https://github.com/saketh12/Auto1111SDK | Dépôt Auto1111SDK à son chemin personnel d'origine | 2026-09-04 |

## Brief agent {#agent-brief}

- **Sujet :** `project:auto1111sdk`, fil `auto1111sdk-development`, 2 événements datés du 2024-02-06 au 2024-03-05.
- **Note pratique :** à partir du 2024-03-05, considérez le dépôt de l'organisation Auto1111SDK comme le point d'entrée historique enregistré du projet, et validez séparément les instructions de configuration actuelles.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
