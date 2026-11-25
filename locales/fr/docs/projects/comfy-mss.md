---
title: "Comfy-MSS"
category: projects

tags: [comfy-mss, comfy-mss-development, project]
aliases: ["Comfy-MSS"]
level: 2
source_sha256: fe47731b1f8c5c17dd4a88df303f85c2193a4b81471a3fd15da97a40585fe4d6
translation: machine
translated_at: '2026-10-24'
---
# Comfy-MSS {#comfy-mss}

**Ligne de développement :** `project:comfy-mss` · fil `comfy-mss-development`  
**Dernier événement :** - · 0 daté depuis - · **Recherché :** 2026-09-05 · confiance : élevée

## Ce que c'est {#what-it-is}

Comfy-MSS — ensemble de custom nodes ComfyUI basé sur pymss, destiné à séparer l'AUDIO en piste vocale et stems instrumentaux.

Fonctionnalités : séparation MSS et VR/UVR, modèles MSST personnalisés, chargement par lots, ensemble, inversion de phase, normalisation et enregistrement en WAV/FLAC/MP3.

Limitation : le chemin utilisateur ne prend en charge que MSST, et les graphes v1.0.x sont incompatibles avec la v1.1.0+ en raison du renommage des types de nodes.

Verdict : c'est la voie la plus complète pour la séparation de stems dans ComfyUI, mais la mise à niveau vers 1.1 impose de reconstruire les anciens graphes.

## Ligne de développement {#development-line}

- L'événement daté n'a pas encore fait l'objet d'une rédaction ; ce qui est connu figure dans les sections ci-dessous.

## Ce qui a changé {#what-changed}

2026-07-06 — Comfy-MSS a été documenté comme paquet de séparation AUDIO pour ComfyUI en stems vocaux et instrumentaux, via les modèles MSS et VR/UVR, avec ensemble, normalisation et phase-invert.

2026-05-31 — publication du tag 1.0.0. 2026-06-03 — le tag 1.0.1 a figé la version du paquet. 2026-06-13 — la 1.0.2 a mis à jour la dépendance pymss vers 2.0.6. 2026-06-28 — la 1.0.3 a retravaillé les nodes et normalisé la gestion de la largeur de l'interface. 2026-08-03 — la 1.0.4 a aligné les modèles personnalisés sur pymss : il faut un répertoire dédié contenant le fichier de poids et le YAML ; VR/UVR ont été exclus de Custom MSS Separate. 2026-08-11 — la 1.1.0 a renommé les types de nodes et rendu les graphes 1.0.x incompatibles.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-06, ne modifiez pas votre workflow à partir de ces seuls liens ; attendez une publication de version ou des éléments sourcés avant d'adopter ou de documenter l'usage de Comfy-MSS.

1. Installer le dépôt dans `ComfyUI/custom_nodes` et installer `pymss` dans le même environnement Python que celui utilisé par ComfyUI ; redémarrer ensuite ComfyUI.
  — <https://github.com/pymss-project/comfy-mss>
2. Envoyer l'AUDIO dans `MSS Separate` ou `VR Separate`, choisir le modèle de répertoire, le périphérique et la source de téléchargement ; un modèle absent est téléchargé automatiquement par défaut.
  — <https://github.com/pymss-project/comfy-mss>
3. Pour une série de fichiers, utiliser `Load Audio Batch` et la variante list du separator ; les nodes suivants s'exécutent pour chaque élément de la liste.
  — <https://github.com/pymss-project/comfy-mss>
4. Pour votre propre modèle MSST, placer le fichier de poids et le `.yaml` dans un sous-dossier dédié `<pymss_model_dir>/custom`, puis cliquer sur `Refresh Models`.
  — <https://github.com/pymss-project/comfy-mss>
5. Enregistrer les stems obtenus avec `Save Audio` ; les formats WAV, FLAC et MP3 sont disponibles à 32, 44,1 et 48 kHz.
  — <https://github.com/pymss-project/comfy-mss>

## Bonnes pratiques {#best-practices}

- Avant de passer à la 1.1.0, sauvegarder et reconstruire les graphes v1.0.x : le renommage des types de nodes les rend incompatibles.
  — <https://github.com/pymss-project/comfy-mss/blob/main/README.md>
- Laisser `chunk_size` et `overlap_size` sur Default tant qu'un réglage éprouvé n'est pas nécessaire : les valeurs du YAML du modèle choisi s'appliquent alors.
  — <https://github.com/pymss-project/comfy-mss>
- Pour des workflows portables, ne pas figer de chemins machine : utiliser le répertoire standard `ComfyUI/models/pymss`, les variables `COMFY_MSS_MODEL_DIR`/`PYMSS_MODEL_DIR` ou les extra model paths.
  — <https://github.com/pymss-project/comfy-mss>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-03 — l'ancienne pratique d'une disposition personnalisée libre a été remplacée par l'exigence d'un dossier dédié contenant un fichier de poids pris en charge et un YAML ; VR/UVR ne relèvent plus de Custom MSS Separate.
- 2026-08-11 — les workflows v1.0.x sont obsolètes pour la 1.1.0+ et doivent être reconstruits à cause du renommage des node types.

## Points toujours inconnus {#still-unknown}

- Le paquet ne publie pas de GitHub Releases ; les dates et le périmètre de ses versions sont confirmés par les tags, et non par des notes de version distinctes.
- Le point du 2026-07-06 correspond à la date d'une documentation indépendante de Comfy-MSS, et non à une version confirmée du paquet lui-même.

## Sources {#sources}

| Source | Titre | Consulté |
|---|---|---|
| https://github.com/pymss-project/comfy-mss | pymss-project/comfy-mss — ComfyUI custom nodes for music source separation | 2026-09-05 |
| https://github.com/pymss-project/comfy-mss/blob/main/README.md | README de Comfy-MSS | 2026-09-05 |
| https://github.com/pymss-project/comfy-mss/tags | Tags de Comfy-MSS et changements datés | 2026-09-05 |
| https://pypi.org/project/pymss/ | pymss sur PyPI | 2026-09-05 |
| https://github.com/SlavaSexton/ComfyUI-Agent-Kit/blob/master/CHANGELOG.md | Journal des modifications de ComfyUI-Agent-Kit 2.3.0 | 2026-09-05 |

## Brief agent {#agent-brief}

- **Sujet :** `project:comfy-mss`, fil `comfy-mss-development`, 0 événement daté - → -.
- **Note pratique :** Au 2026-07-06, ne modifiez pas votre workflow à partir de ces seuls liens ; attendez une publication de version ou des éléments sourcés avant d'adopter ou de documenter l'usage de Comfy-MSS.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
