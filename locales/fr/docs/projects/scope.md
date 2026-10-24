---
title: "SCoPE"
category: projects
date: 2026-08-14
tags: [project, scope, scope-public-resources]
aliases: ["SCoPE"]
level: 3
source_sha256: 17efd9309dcfb3ec57dc8c708a375ee635e829a8b269eb5803c4f432ec581e6f
translation: machine
translated_at: '2026-10-24'
---
# SCoPE {#scope}

**Ligne de développement :** `project:scope` · fil `scope-public-resources`  
**Dernier événement :** 2026-08-14 · 1 événement daté depuis le 2026-08-14 · **Recherche effectuée le :** 2026-09-07 · confiance : moyenne

## Ce que c'est {#what-it-is}

SCoPE est une version de recherche image-vers-vidéo destinée aux équipes qui ont besoin de contrôler la trajectoire de caméra sur Wan2.2-I2V-A14B.

- Entrées : prend une première image, un prompt texte et une trajectoire de caméra cible.
- Coordonnée positionnelle : ajoute le rayon de caméra de chaque token comme seconde coordonnée, sans branche de contrôle séparée.
- Poids d'inférence : fournit des poids autonomes pour sa base Wan2.2-I2V-A14B.

Le point de contrôle (checkpoint) fait environ 67 Go. L'inférence locale nécessite Python 3.11 et un GPU compatible CUDA. L'exemple par défaut documenté génère 81 images à 480×832. Utilisez-le lorsque vous pouvez fournir des poses de caméra compatibles : une géométrie imprécise, des trajectoires hors distribution, des occlusions et des mouvements rapides peuvent réduire la qualité.

## Ligne de développement {#development-line}

- **2026-08-14 — Les ressources du projet SCoPE ont été reliées.** Le 2026-08-14, des liens publics ont relié le site du projet SCoPE, le dépôt source de TencentARC et la page Hugging Face. Ensemble, ces liens offraient des points d'entrée publics vers les informations du projet, le code source et les documents d'hébergement du modèle. Ils n'établissent ni une date de publication, ni une version, ni une autorité de création, ni des capacités.

## Ce qui a changé {#what-changed}

- 2026-06-25 — La version 1 de l'article SCoPE a établi un encodage positionnel basé sur les rayons pour les transformers de diffusion vidéo.
- 2026-08-12 — arXiv v3 est devenue la dernière révision de l'article avant les liens publics. La première mise en ligne publique du code a ajouté le code d'inférence et d'entraînement, des exemples, la documentation et une licence.
- 2026-08-14 — Les documents liés décrivaient une version SCoPE déjà publique. Aucune nouvelle version ni modification de l'article propre à cette date n'a été trouvée.
- 2026-08-15 — Le README a documenté la démo officielle sur Hugging Face.
- 2026-08-16 — Le dépôt a amélioré la sélection des trajectoires et les flux de démonstration.
- 2026-08-22 — Le dépôt a rétabli les sources de modèles DiffSynth vendorisées qui manquaient. Cette correction a réparé l'organisation des sources et n'établit pas de nouvelles performances du modèle.

## Comment l'utiliser {#how-to-use-this}

1. Utilisez la démo officielle dans le navigateur pour examiner le flux de contrôle de caméra image-vers-vidéo avant toute installation locale.
  — <https://huggingface.co/TencentARC/SCoPE>
2. Pour une inférence locale reproductible, clonez le dépôt et créez son environnement épinglé avec `uv sync`. La version documentée utilise Python 3.11, PyTorch 2.9.1 et CUDA 12.8.
  — <https://github.com/TencentARC/SCoPE>
3. Téléchargez `TencentARC/SCoPE` dans un répertoire local de points de contrôle. Prévoyez de la place pour le point de contrôle d'environ 67 Go et pour le cache.
  — <https://huggingface.co/TencentARC/SCoPE>
4. Exécutez un cas fourni avec une trajectoire explicite, comme `omni-misty-forest` et `truck_right`, pour obtenir une référence reproductible.
  — <https://github.com/TencentARC/SCoPE>
5. Pour une exécution personnalisée, fournissez une première image, un prompt, un tableau de poses caméra-vers-monde au format OpenCV et le champ de vision horizontal.
  — <https://github.com/TencentARC/SCoPE/blob/main/MODEL_CARD.md>

## Bonnes pratiques {#best-practices}

- Respectez l'environnement documenté (Python 3.11, PyTorch 2.9.1, CUDA 12.8) lorsque vous reproduisez des résultats. Le projet avertit que les changements de version de PyTorch peuvent modifier les résultats numériques.
  — <https://github.com/TencentARC/SCoPE>
- Utilisez un `--trajectory` explicite pour les tâches automatisées ou répétables, et ne le combinez pas avec `--camera_path`.
  — <https://github.com/TencentARC/SCoPE>
- Validez les poses personnalisées comme des tableaux finis de poses caméra-vers-monde OpenCV de forme `[81, 3, 4]` ou `[81, 4, 4]`. Fournissez `x_fov` en radians horizontaux et utilisez `xi=0` pour une caméra sténopé (pinhole).
  — <https://github.com/TencentARC/SCoPE/blob/main/MODEL_CARD.md>
- Conservez le point de contrôle et le cache Hugging Face sur un stockage local. Utilisez `--vram_limit_gb` lorsque la gestion de la VRAM ou le déchargement est nécessaire.
  — <https://github.com/TencentARC/SCoPE>
- Utilisez une source à partir du commit `449343d` ou ultérieur pour un travail de copie locale, car ce commit rétablit les sources de modèles DiffSynth vendorisées omises. Ne considérez pas cette correction comme une preuve d'inférence de bout en bout.
  — <https://github.com/TencentARC/SCoPE/commit/449343d217c54b98cb182cbc00f318f892bfecef>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-22 — Les consignes fondées sur une copie antérieure au commit 449343d sont remplacées pour une organisation complète des sources. Le commit ultérieur rétablit les sources de modèles DiffSynth vendorisées omises. Il s'agit d'une réparation du dépôt, et non d'une nouvelle version du modèle.

## Points encore inconnus {#still-unknown}

- Aucune page de première source n'établit une version SCoPE indépendante ni une modification de l'article le 2026-08-14 ; la mise en ligne publique du code et la dernière révision arXiv antérieure à l'événement sont datées du 2026-08-12.
- Les instructions actuelles du README incluent des améliorations postérieures au 2026-08-14 : ce sont donc des consignes d'utilisation actuelles, et non une preuve du flux de travail initial exact.
- Aucun retour indépendant d'opérateur en anglais ou en chinois simplifié n'était suffisant pour élever les conseils d'installation au-delà de la documentation officielle.
- SCoPE présente des collisions de noms sans rapport dans la recherche et la recherche de modèles. Le dépôt TencentARC exact, l'identifiant du modèle et l'identifiant arXiv définissent cette entrée.

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://visual-ai.github.io/scope/ | SCoPE: Sightline-Coordinate Positional Encoding for Video Diffusion Transformers | 2026-09-07 |
| https://github.com/TencentARC/SCoPE | Dépôt TencentARC/SCoPE et README | 2026-09-07 |
| https://huggingface.co/TencentARC/SCoPE | Fiche du modèle TencentARC/SCoPE | 2026-09-07 |
| https://arxiv.org/abs/2606.27345 | SCoPE: Sightline-Coordinate Positional Encoding for Video Diffusion Transformers, arXiv:2606.27345 | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commits/main | Historique des commits de TencentARC/SCoPE | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/30226072dd5314dc7c4d91a25cdf3771b485e13e | Release SCoPE: inference + training code, examples, docs, and license | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/69baf9815e10afcb44cf794f76cb80e1f5c4155b | Update README.md | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/6658d0e | Improve inference trajectory selection and README demos | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/commit/449343d217c54b98cb182cbc00f318f892bfecef | Fix missing vendored DiffSynth model sources | 2026-09-07 |
| https://github.com/TencentARC/SCoPE/blob/main/MODEL_CARD.md | Fiche modèle SCoPE pour Wan2.2-I2V-A14B | 2026-09-07 |

## Résumé pour agent {#agent-brief}

- **Sujet :** `project:scope`, fil `scope-public-resources`, 1 événement daté du 2026-08-14 au 2026-08-14.
- **Note pratique :** voir les sections d'usage et de pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
