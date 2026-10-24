---
title: "OpenMontage"
category: projects
date: 2026-06-28
tags: [openmontage, openmontage-development, project]
aliases: ["OpenMontage"]
level: 2
source_sha256: c95ae5bdc6172b57ddae2508380ed4fa81dc1eb95fe9d643dd5ab0fa5031c844
translation: machine
translated_at: '2026-10-24'
---
# OpenMontage {#openmontage}

**Ligne de développement :** `project:openmontage` · fil `openmontage-development`  
**Dernier événement :** 2026-06-28 · 1 événement daté depuis le 2026-06-28 · **Recherche effectuée le :** 2026-09-05 · confiance : moyenne

## Ce que c'est {#what-it-is}

OpenMontage est un pipeline vidéo automatisé dans lequel un assistant de programmation IA prend en charge la recherche, l'écriture du script, les ressources, le montage et le rendu.

- 11 types de pipelines documentés, du montage documentaire à la localisation.
- Des points de validation humaine et un journal de sélection des fournisseurs pour contrôler chaque étape.

Nécessite Python 3.10+, FFmpeg, Node.js 18+ et un assistant de programmation.

Il s'agit d'un environnement local pour une production maîtrisée, et non d'un éditeur vidéo cloud en un clic.

## Ligne de développement {#development-line}

- **2026-06-28 — Référence au dépôt GitHub d'OpenMontage.** Le 2026-06-28, un lien public renvoyait vers le dépôt GitHub d'OpenMontage. Les sources ne contiennent ni instantané du dépôt, ni notes de version, ni diff de code : il s'agit donc d'une simple référence à un dépôt public, et non d'une publication de version.

## Ce qui a changé {#what-changed}

- 2026-06-28 — OpenMontage suivi comme projet distinct via son dépôt officiel ; aucune description datée d'une modification précise n'existe pour ce jour.
- 2026-06-29 — Ajout d'un fournisseur natif ComfyUI pour générer des images et des vidéos via un serveur local.
- 2026-07-15 — Publication d'un exemple reproductible d'un reportage complet réalisé avec OpenMontage.

## Comment l'utiliser {#how-to-use-this}

Au 2026-06-28, nous utilisons le dépôt GitHub d'OpenMontage comme référence de départ pour le contexte des sources et du développement ; aucune installation ni modification de flux de travail n'est documentée pour cette date.

1. Installer Python 3.10+, FFmpeg, Node.js 18+ et un assistant de programmation IA ; cloner le dépôt officiel et exécuter `make setup` ou l'équivalent manuel.
  — <https://github.com/calesthio/OpenMontage>
2. Ouvrir le projet dans un assistant de programmation et fournir un brief avec la durée, le sujet, le format ainsi que les limites de ressources ou d'API.
  — <https://github.com/calesthio/OpenMontage>
3. Choisir d'abord un pipeline, puis suivre son manifeste et ses compétences par étape au lieu d'exécuter des scripts arbitraires.
  — <https://github.com/calesthio/OpenMontage>
4. Examiner le brouillon du projet, le script, le plan de scènes et les ressources aux points de validation avant le rendu ; ouvrir le Backlot local si nécessaire.
  — <https://github.com/calesthio/OpenMontage>

## Bonnes pratiques {#best-practices}

- Ne cloner que `calesthio/OpenMontage` : un signalement de juin a identifié un dépôt à l'apparence similaire, appartenant à un autre propriétaire, comme un logiciel malveillant potentiel.
  — <https://github.com/calesthio/OpenMontage/issues/200>
- Choisir tôt le pipeline et l'environnement d'exécution du rendu : les décisions de montage consignent l'environnement d'exécution, et les changements silencieux d'environnement vont à l'encontre du processus.
  — <https://github.com/calesthio/OpenMontage>
- Utiliser un flux de travail personnalisé avec un `output_node` explicite pour les configurations ComfyUI locales : la disponibilité du serveur détermine l'état de préparation sur les chemins personnalisés, et non les modèles intégrés.
  — <https://github.com/calesthio/OpenMontage/pull/230>

## Remplacé par ceci {#superseded-by-this}

- 2026-06-29 — La PR #230 a remplacé la PR #29 par un rebasage sur main et la résolution d'un conflit dans .gitignore.

## Toujours inconnu {#still-unknown}

- Aucune source primaire datée ne décrit une modification fonctionnelle le 2026-06-28 ; event_findings reste vide.
- Le signalement d'un dépôt malveillant d'apparence similaire provient d'une issue GitHub, et non d'un audit indépendant par un antivirus.

## Sources {#sources}

| source | titre | consulté le |
|---|---|---|
| https://github.com/calesthio/OpenMontage | Dépôt calesthio/OpenMontage et README | 2026-09-05 |
| https://github.com/calesthio/OpenMontage/pull/230 | PR #230 : Add native ComfyUI provider | 2026-09-05 |
| https://github.com/calesthio/OpenMontage/discussions/231 | OpenMontage now supports ComfyUI | 2026-09-05 |
| https://github.com/calesthio/OpenMontage/discussions/385 | A 7-Minute Trending-News Show for $0.24 | 2026-09-05 |
| https://github.com/calesthio/OpenMontage/issues/200 | Security warning: lookalike Open-Montage/OpenMontage release behaves like malware | 2026-09-05 |

## Brief pour agent {#agent-brief}

- **Sujet :** `project:openmontage`, fil `openmontage-development`, 1 événement daté du 2026-06-28 au 2026-06-28.
- **Note pratique :** Au 2026-06-28, les praticiens peuvent utiliser le dépôt GitHub d'OpenMontage comme référence de départ pour le contexte des sources et du développement du projet ; aucune modification spécifique d'installation ou de flux de travail ne peut être déduite.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
