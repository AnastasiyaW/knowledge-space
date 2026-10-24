---
title: "DiffIR2VR-Zero"
category: projects
date: 2024-07-14
tags: [diffir2vr-zero, diffir2vr-zero-development, diffir2vr_zero, project]
aliases: ["DiffIR2VR-Zero"]
level: 2
source_sha256: 9898f04564ea07a3478fb68400b8d6f445eb317ba40f1c5dc63146be7c791dbf
translation: machine
translated_at: '2026-10-24'
---
# DiffIR2VR-Zero {#diffir2vr-zero}

**Ligne de développement :** `project:diffir2vr-zero` · fil `diffir2vr-zero-development`  
**Dernier événement :** 2024-07-14 · 2 datés depuis 2024-07-01 · **Recherché le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

DiffIR2VR-Zero — code de recherche qui adapte des modèles de diffusion de restauration d'images pré-entraînés à la restauration vidéo temporellement cohérente. — Débruitage aveugle (`dn`) et super-résolution (`sr`). — Jusqu'à 8× de super-résolution revendiqués, sans ré-entraînement spécifique à la tâche. — Déformation (warping) latente hiérarchique, plus fusion de tokens basée sur le flux et sur la similarité. Limite : le lanceur utilise CUDA par défaut, n'a aucune version GitHub étiquetée, et la démo hébergée signale une erreur de build. utilisez le dépôt pour des expériences contrôlées, et non la démo comme point d'accès en production.

## Ligne de développement {#development-line}

- **2024-07-01 — La page projet et la démo interactive de DiffIR2VR-Zero entrent dans le registre public.** Le 2024-07-01, la ligne de développement de DiffIR2VR-Zero a été reliée à un site web de projet et à un Hugging Face Space. Il s'agit d'une présence publique substantielle du projet et de sa démo dans l'historique. Les preuves scellées n'établissent pas la version du modèle, ses capacités ni le statut de publication derrière ces liens.
- **2024-07-14 — Le dépôt GitHub de DiffIR2VR-Zero a été relié dans la ligne de développement.** Le 2024-07-14, la ligne de développement de DiffIR2VR-Zero a relié un élément antérieur au dépôt GitHub du projet. Cela est considéré comme une étape importante d'accès au source dans l'historique public. Les liens scellés seuls ne montrent pas s'il s'agissait d'une nouvelle publication de code ou d'une référence à du code déjà disponible plus tôt.

## Ce qui a changé {#what-changed}

DiffIR2VR-Zero — la méthode et le source sont arrivés en juillet 2024 ; les preuves ultérieures montrent des révisions de l'article, une réparation d'un lien de checkpoint et une démo hébergée indisponible, plutôt qu'une nouvelle génération de produit. — 2024-07-01 : arXiv v1 et le premier commit du dépôt ont établi la méthode de restauration vidéo sans entraînement, la page projet et le chemin de code local. — 2024-07-14 : la voie GitHub a rendu explicite le checkout du source. L'historique du dépôt, vérifié aujourd'hui, place le commit initial au 2024-07-01, donc ceci n'est pas attesté comme une seconde publication algorithmique. — 2025-12-31 (trouvé aujourd'hui) : arXiv v5 a été publiée. Ses métadonnées ne décrivent aucune modification correspondante du code exécutable. — 2026-01-22 (trouvé aujourd'hui) : le commit `2cf4737` a remplacé l'URL indisponible du checkpoint officiel SD 2.1 par un miroir ; la méthode d'inférence est restée inchangée. — 2026-09-04 (trouvé aujourd'hui) : le Hugging Face Space public signale une erreur de build, faisant du dépôt local le point d'entrée pratique. Limite : aucune installation de bout en bout fraîche n'a été exécutée lors de cette revue. considérez-le comme du code de recherche faiblement maintenu, avec un chemin source fonctionnel mais une chaîne de dépendances fragile.

## Comment l'utiliser {#how-to-use-this}

À partir du 2024-07-01, les praticiens pouvaient examiner DiffIR2VR-Zero via ses liens publics de projet et de démo ; à partir du 2024-07-14, ils pouvaient aussi consulter le dépôt GitHub relié pour accéder à l'implémentation, tout en vérifiant indépendamment la révision exacte et les conditions d'utilisation.

1. Clonez le dépôt, créez un environnement Conda Python 3.10 et installez `requirements.txt`.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
2. Créez `weights/` et ajoutez manuellement `gmflow_sintel-0c07dcb3.pth` ; le chemin d'inférence documenté récupère les autres poids DiffBIR v2 et SD 2.1 à la demande.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
3. Commencez par la base de débruitage documentée : `--version v2 --task dn --upscale 1 --cfg_scale 4.0 --batch_size 10`, avec la configuration fournie, les chemins d'entrée et de sortie, `final_size` et le ratio de fusion.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
4. Pour la super-résolution, passez à `--task sr` et commencez par la commande 4× documentée avant de tenter la plage 8× revendiquée par le projet.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
5. Définissez un `--seed` explicite pour des exécutions comparables et vérifiez que CUDA est réellement disponible ; sinon le lanceur bascule sur le CPU.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero/blob/main/inference.py>

## Bonnes pratiques {#best-practices}

- Utilisez le dépôt local plutôt que le Space hébergé tant que son échec de build n'est pas résolu.
  — <https://huggingface.co/spaces/Koi953215/DiffIR2VR>
- Épinglez et vérifiez indépendamment les checkpoints téléchargés : le mainteneur a remplacé le téléchargement officiel SD 2.1 par un miroir après que l'URL officielle est devenue indisponible.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero/commit/2cf4737bfc8319abd8ca399d70cc49a3aaf097a6>
- Partez de la base documentée 480×854, CFG 4.0, taille de lot 10 et ratio de fusion ; ne modifiez qu'un groupe de paramètres à la fois en vérifiant le détail par rapport à la stabilité temporelle.
  — <https://github.com/jimmycv07/DiffIR2VR-Zero>
- Traitez les affirmations « jusqu'à 8× » et « sans ré-entraînement » comme des résultats de recherche, puis inspectez les extraits restaurés pour la cohérence temporelle et les détails inventés sur les images cibles.
  — <https://jimmycv07.github.io/DiffIR2VR_web/>

## Remplacé par ceci {#superseded-by-this}

- 2024-07-01–2024-07-14 : utiliser la démo Hugging Face comme point d'entrée opérationnel — obsolète comme conseil pratique ; le Space accessible signale désormais une erreur de build.
- Avant 2026-01-22 : se fier au téléchargement automatique depuis l'URL officielle du checkpoint Stable Diffusion 2.1 — obsolète ; le mainteneur a changé la source parce que cette URL officielle était indisponible.
- 2024-07-14 : interpréter le lien GitHub comme une seconde publication de code — non étayé par l'historique du dépôt, qui enregistre le premier commit au 2024-07-01.

## Toujours inconnu {#still-unknown}

- Aucune installation actuelle de CUDA/PyTorch ni aucune exécution complète d'inférence n'ont été vérifiées indépendamment ; les instructions du dépôt sont une preuve de source, non un reçu d'exécution.
- Le Hugging Face Space accessible signale une erreur de build, mais son instantané de page a été exploré deux semaines avant cette revue ; son exécution réelle en direct n'a pas été testée dans un navigateur.
- Le Space source renvoie vers `arXiv:2406.06523`, qui est l'article distinct NaRCan sur l'édition vidéo. Il peut s'agir de métadonnées périmées ou d'une confusion historique. La page projet, le dépôt et `arXiv:2407.01519` identifient de façon cohérente DiffIR2VR-Zero, donc l'existence de deux sujets distincts DiffIR2VR-Zero n'est pas attestée.
- Aucune documentation chinoise de première main n'a été trouvée dans une recherche séparée en chinois simplifié ; aucune consigne opérationnelle spécifique au chinois n'a donc été ajoutée.
- Les métadonnées arXiv v2–v5 n'expliquent pas leurs modifications de fond ; ces dates de révision ne doivent pas être lues comme des publications d'implémentation.

## Sources {#sources}

| source | title | read |
|---|---|---|
| https://arxiv.org/abs/2407.01519 | DiffIR2VR-Zero: Zero-Shot Video Restoration with Diffusion-based Image Restoration Models | 2026-09-04 |
| https://jimmycv07.github.io/DiffIR2VR_web/ | DiffIR2VR-Zero project page | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero | GitHub — jimmycv07/DiffIR2VR-Zero | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero/commits/main | Commit history — jimmycv07/DiffIR2VR-Zero | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero/blob/main/inference.py | DiffIR2VR-Zero inference.py | 2026-09-04 |
| https://github.com/jimmycv07/DiffIR2VR-Zero/commit/2cf4737bfc8319abd8ca399d70cc49a3aaf097a6 | Change sd_v21 model checkpoint URL | 2026-09-04 |
| https://huggingface.co/spaces/Koi953215/DiffIR2VR | DiffIR2VR — Hugging Face Space | 2026-09-04 |
| https://arxiv.org/abs/2406.06523 | NaRCan: Natural Refined Canonical Image with Integration of Diffusion Prior for Video Editing | 2026-09-04 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:diffir2vr-zero`, fil `diffir2vr-zero-development`, 2 événements datés 2024-07-01 → 2024-07-14.
- **Note pratique :** À partir du 2024-07-01, les praticiens pouvaient examiner DiffIR2VR-Zero via ses liens publics de projet et de démo ; à partir du 2024-07-14, ils pouvaient aussi consulter le dépôt GitHub relié pour accéder à l'implémentation, tout en vérifiant indépendamment la révision exacte et les conditions d'utilisation.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité sur ce qui est obsolète.
