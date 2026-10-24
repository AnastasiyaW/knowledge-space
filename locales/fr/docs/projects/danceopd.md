---
title: "DanceOPD"
category: projects
date: 2026-06-26
tags: [danceopd, danceopd-development, project]
aliases: ["DanceOPD"]
level: 3
source_sha256: 4e76ddb15414128a47d49feb175dd5812017d99441a5964e6f481bb4ba024ceb
translation: machine
translated_at: '2026-10-24'
---
# DanceOPD {#danceopd}

**Ligne de développement :** `project:danceopd` · fil `danceopd-development`  
**Dernier événement :** 2026-06-26 · 1 daté depuis le 2026-06-26 · **Recherche :** 2026-09-06 · confiance : élevée

## Présentation {#what-it-is}

DanceOPD est un cadre d'entraînement destiné aux équipes qui disposent déjà de points de contrôle ou de LoRA compatibles en flow matching et qui ont besoin qu'un seul étudiant combine les comportements de génération texte-vers-image et d'édition d'image.

- Achemine chaque échantillon de manière stricte vers un seul champ de capacité gelé.
- Interroge un état à faible bruit à partir du déploiement actuel de l'étudiant et fait correspondre la vélocité par MSE.
- Documente les backends SD3.5/Diffusers et Z-Image/DiffSynth.

## Ligne de développement {#development-line}

- **2026-06-26 — site web du projet DanceOPD relié.** Le 2026-06-26, le site GitHub Pages de DanceOPD a été mis en ligne. Le site a donné au projet une présence publique, mais le texte source sous-jacent n'était pas disponible.

## Ce qui a changé {#what-changed}

- 2026-06-25 — la v1 de l'arXiv a été soumise à 17:59:58 UTC, créant l'enregistrement de préimpression de référence.
- 2026-06-26 — le manuscrit v1 est daté du 26 juin, et le dépôt public a été ouvert avec le commit initial `init`.
- 2026-06-30 — `Sync public release contents` a ajouté 59 fichiers, avec 3 208 ajouts et 76 suppressions, incluant le code, les configurations, la préparation des données, les scripts de test rapide et la documentation.
- 2026-07-07 — la v2 de l'arXiv a été soumise sans note de révision, si bien que la nature de ses modifications reste inconnue.
- 2026-08-15 — la v3 de l'arXiv a été soumise. DanceOPD 0.2.0 a ajouté le routage vers l'enseignant lié à la tâche, trois modes pour SD3.5-M et Z-Image, des configurations publiques exécutables, des modèles d'article, la reprise d'entraînement, la prise en charge de la double LoRA et des options de champ CFG.

## Comment l'utiliser {#how-to-use-this}

1. Clonez `worldbench/DanceOPD`, installez l'ensemble d'extras nécessaire, puis exécutez `pip install -e ".[smoke]"` suivi de `bash scripts/bootstrap_smoke.sh`.
  — <https://github.com/worldbench/DanceOPD>
2. Exécutez une simulation (dry run) de la configuration SD3.5 ou Z-Image avant de charger les poids réels. Installez DiffSynth-Studio avant l'entraînement complet de Z-Image.
  — <https://github.com/worldbench/DanceOPD>
3. Préparez une invite routée ou un CSV OmniEdit. Les routes d'édition exigent `source_image`, et les tâches de style, d'arrière-plan ou d'environnement sont associées à `global_edit`, sauf si elles sont remplacées.
  — <https://github.com/worldbench/DanceOPD>
4. Configurez chaque enseignant gelé comme point de contrôle de base, point de contrôle complet, LoRA PEFT ou point de contrôle plus LoRA. Gardez la LoRA étudiante entraînable séparée.
  — <https://github.com/worldbench/DanceOPD>
5. Utilisez `configs/public` pour tester le code ou les modèles d'article avec des ressources compatibles, puis lancez l'entraînement avec Accelerate et reprenez depuis une étape sauvegardée si nécessaire.
  — <https://github.com/worldbench/DanceOPD>

## Bonnes pratiques {#best-practices}

- Considérez le chemin de test rapide comme une vérification de l'état du code, et non comme une preuve que les métriques de l'article sont reproductibles.
  — <https://github.com/worldbench/DanceOPD>
- Pour DanceOPD lui-même, conservez la valeur par défaut documentée : un seul enseignant routé de manière stricte, une seule requête à faible bruit (`K=1`) et une MSE directe sur la vélocité.
  — <https://github.com/worldbench/DanceOPD>
- N'empilez pas de LoRA enseignantes sur l'adaptateur étudiant entraînable. Fusionnez plutôt chaque enseignant dans un module enseignant gelé et propre.
  — <https://github.com/worldbench/DanceOPD>
- Conservez `student_cfg_scale=1.0` lorsque vous intégrez le CFG, ajustez l'échelle de l'enseignant et réglez le CFG d'inférence séparément, afin que les effets ne se cumulent pas.
  — <https://github.com/worldbench/DanceOPD>
- Gardez distincts les substituts publics téléchargeables et les modèles alignés sur l'article ; les points de contrôle de l'article restent indisponibles.
  — <https://github.com/worldbench/DanceOPD>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-26 — une compréhension fondée uniquement sur la page du projet a été remplacée par la synchronisation du code public du 2026-06-30 et par la boîte à outils 0.2.0 du 2026-08-15.
- 2026-08-15 — un chemin de reproduction non différencié est obsolète : les ressources de substitution publiques et les modèles alignés sur l'article sont distincts, et les points de contrôle de l'article restent non publiés.

## Toujours inconnu {#still-unknown}

- La page du projet elle-même ne comporte pas d'horodatage de publication. L'événement du 26 juin repose sur la date affichée dans le manuscrit et sur l'historique du dépôt, tandis que la v1 de l'arXiv a été soumise le 25 juin en UTC.
- arXiv ne fournit aucune note de modification pour les v2 ou v3, de sorte que les modifications du manuscrit restent non vérifiées.
- Aucune conférence ou revue à comité de lecture n'a été vérifiée ; arXiv qualifie le travail de rapport technique (Technical Report).
- Aucune exigence matérielle officielle, aucune estimation de durée d'entraînement réelle, aucune graine déterministe, aucun point d'accès d'inférence hébergé et aucun rapport de reproduction indépendant n'ont été vérifiés.

## Sources {#sources}

| source | titre | lu le |
|---|---|---|
| https://danceopd.github.io/ | DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://arxiv.org/html/2606.27377v1 | DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://arxiv.org/abs/2606.27377 | [2606.27377] DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://github.com/worldbench/DanceOPD | GitHub - worldbench/DanceOPD: DanceOPD: On-Policy Generative Field Distillation | 2026-09-06 |
| https://github.com/worldbench/DanceOPD/commits/main/ | Commits · worldbench/DanceOPD · GitHub | 2026-09-06 |
| https://github.com/worldbench/DanceOPD/commit/08f1230c013bf8fe21295cc95bd01e36e5c2a45b | Sync public release contents · worldbench/DanceOPD@08f1230 · GitHub | 2026-09-06 |
| https://raw.githubusercontent.com/worldbench/DanceOPD/main/CHANGELOG.md | DanceOPD CHANGELOG.md | 2026-09-06 |

## Brief agent {#agent-brief}

- **Sujet :** `project:danceopd`, fil `danceopd-development`, 1 événement daté du 2026-06-26 au 2026-06-26.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés ci-dessus font autorité pour déterminer ce qui est obsolète.
