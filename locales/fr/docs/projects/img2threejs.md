---
title: "img2threejs"
category: projects
date: 2026-07-24
tags: [img2threejs, project]
aliases: ["img2threejs"]
level: 2
source_sha256: 39f90ba725a789d2467cea8a24888238187a443d4d9a2bee93b1ebc667a8d092
translation: machine
translated_at: '2026-10-24'
---
# img2threejs {#img2threejs}

**Ligne de développement :** `project:img2threejs` · fil `img2threejs`  
**Dernier événement :** 2026-07-24 · 1 daté depuis le 2026-07-24 · **Recherché :** 2026-09-05 · confiance : élevée

## Qu'est-ce que c'est {#what-it-is}

img2threejs — skill Apache-2.0 pour Claude Code, Codex et OpenCode : à partir d'une seule image, il construit une fabrique TypeScript `THREE.Group`, et non un GLB ni un maillage extrait. — décompose l'objet en composants, matériaux, sockets et colliders ; — génère le modèle par passes et compare le rendu à la référence ; — pour les personnages, sait construire un rig et vérifier l'animation. Limite : une seule vue ne montre pas les faces cachées ; pour une ressemblance précise, le projet signale explicitement les zones incertaines et demande des vues supplémentaires. Verdict : convient lorsqu'il faut du code Three.js lisible et animable ; ne remplace pas la photogrammétrie ni la modélisation manuelle pour la géométrie invisible.

## Ligne de développement {#development-line}

- **2026-07-24 — le dépôt GitHub d'img2threejs a été publiquement lié.** Le 2026-07-24, la ligne de développement d'img2threejs incluait un lien direct vers son dépôt GitHub. Cela consigne un jalon public de référence source pour le projet ; les preuves scellées n'établissent ni ses fonctionnalités, ni son statut de publication, ni aucune modification de code précise.

## Ce qui a changé {#what-changed}

2026-07-15 — la v1.0 a publié le pipeline objet initial : sculpture par étapes, revue côte à côte et hiérarchie runtime ; la v1.1 a ajouté un inventaire obligatoire des petits détails et une porte de qualité stricte. 2026-07-21 — la v1.2 a placé les personnages humanoïdes et les objets hybrides sur un parcours distinct, avec proportions et diagnostic. 2026-07-22 — la v1.3 a ajouté le harnais de revue déterministe Divine Eye, des vérifications géométriques et des matériaux ancrés dans la référence. 2026-07-24 — le projet a été présenté comme un outil Python de reconstruction Three.js procédurale, prête à l'animation, à partir d'une seule référence. 2026-07-25 — la v1.4.0 a ajouté un pipeline spécialisé d'armes CS2 avec provenance, familles de géométrie et portes de revue. 2026-07-26 — la v1.4.1 a durci les vérifications CS2 : couverture des composants, contrat Glock-18 et preuves de géométrie réelle au lieu d'une texture convaincante. 2026-07-30 — la v1.4.3 a consacré la 1.4.x comme ligne de publication acceptée ; la publication d'une release n'est possible qu'à partir d'un tag annoté approuvé. 2026-08-12 — la v1.5.0 a remplacé la ligne bêta : rig validable, skinning, pipeline de cheveux, contrôle gauche/droite et portes de revue par fonctionnalité. 2026-08-22 — la v1.5.1 a ajouté la voie de référence GLB : le GLB sert d'instrument de mesure, et le résultat reste du code TypeScript. 2026-08-25 — la v1.5.2 a ajouté des portes d'animation/rigging mesurables ; une absence de données signifie désormais `unevaluated`, et non PASS.

## Comment l'utiliser {#how-to-use-this}

Au 2026-07-24, les praticiens peuvent utiliser le dépôt GitHub lié comme référence source publique du projet, tout en vérifiant directement ses fonctionnalités et son statut de version actuels avant de s'y fier.

1. Clonez le dépôt dans le répertoire skills ; le noyau nécessite Python 3.10+ et la bibliothèque standard.
  — <https://github.com/img2threejs/img2threejs>
2. Donnez à l'agent une image et appelez `/img2threejs` ; le pipeline classe lui-même le sujet et crée l'assessment/spec.
  — <https://github.com/img2threejs/img2threejs>
3. Lancez la validation de qualité stricte et ne générez la fabrique TypeScript qu'après réussite de la porte.
  — <https://github.com/img2threejs/img2threejs>
4. Pour un travail long et un personnage, créez un index d'état, puis reprenez la passe suivante autorisée via `forge/next.py`.
  — <https://github.com/img2threejs/img2threejs>
5. Si vous disposez d'un GLB du personnage, utilisez la voie de référence GLB dédiée ; sans lui, restez sur le pipeline central piloté par l'image.
  — <https://github.com/img2threejs/img2threejs/releases/tag/v1.5.1>

## Bonnes pratiques {#best-practices}

- Commencez par un objet hard-surface isolé à silhouette lisible ; ne présentez pas les surfaces cachées comme mesurées.
  — <https://github.com/img2threejs/img2threejs>
- D'abord, listez les détails qui définissent l'identité et reliez chacun à un composant ou matériau ; ne contournez pas `--strict-quality`.
  — <https://github.com/img2threejs/img2threejs>
- Vérifiez chaque passe sur une seule feuille de comparaison « référence à côté du rendu » et ne passez pas à la suite sans PASS.
  — <https://github.com/img2threejs/img2threejs>
- Pour les personnages, ne considérez pas un `AnimationClip` existant comme une animation fonctionnelle : exécutez les portes rig/animation et traitez `unevaluated` comme une vérification inachevée.
  — <https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md>

## Remplacé par cette version {#superseded-by-this}

- 2026-07-30 : la publication automatique après merge de PR est obsolète ; une release exige un tag de version annoté approuvé.
- 2026-08-12 : `1.4.4-beta.1`, `1.4.4-beta.2` et `v1.5-beta` ont été remplacés par la version stable v1.5.0 ; 1.4.4 n'a pas été publiée comme stable.
- 2026-08-25 : la règle « un clip sans travel/rise peut être répété » a été remplacée par la mesure du retour de pose et de la position du bassin ; une boucle non vérifiée ne doit plus être implicitement considérée comme `false`.

## Points encore inconnus {#still-unknown}

- Le dépôt visé par le lien source redirige désormais de `hoainho/img2threejs` vers `img2threejs/img2threejs` ; la date et la raison du transfert ne sont pas établies.
- Le changelog actuel contient une section Unreleased après la v1.5.2 ; ce n'est pas une release publiée et elle ne doit pas être considérée comme une version stable disponible.
- event_findings:[{"event_date":"2026-07-24","source_date":"2026-07-24","finding":"À la même date, un catalogue indépendant précise le cadre pratique : il s'agit d'un outil Python qui construit un modèle Three.js procédural, prêt à l'animation, à partir d'une référence ; ce n'est pas un service distinct de mesh/image-to-3D.","source_url":"https://buttondown.com/surfaced/archive/surfaced-friday-july-24-2026/"}]
- new_events:[{"date":"2026-07-15","finding":"v1.0 et v1.1 : pipeline objet par étapes et inventaire obligatoire des petits détails avec porte de qualité stricte.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-21","finding":"v1.2 : parcours distinct pour les personnages humanoïdes et les sujets hybrides.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-22","finding":"v1.3 : Divine Eye et vérifications déterministes de la géométrie, des matériaux et des données d'entrée.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-25","finding":"v1.4.0 : pipeline d'armes CS2 avec provenance et reconstruction propre à chaque famille.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-26","finding":"v1.4.1 : porte de couverture des composants et contrat Glock-18.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-07-30","finding":"v1.4.3 : ligne de release 1.4.x acceptée et publication uniquement à partir d'un tag annoté approuvé.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-08-12","finding":"v1.5.0 : rig validable, skinning, sous-système de cheveux et portes de revue pour les personnages.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"},{"date":"2026-08-22","finding":"v1.5.1 : voie de référence GLB avec mesure des paramètres et résultat en code.","source_url":"https://github.com/img2threejs/img2threejs/releases/tag/v1.5.1"},{"date":"2026-08-25","finding":"v1.5.2 : portes d'animation/rigging exécutables, où une entrée non vérifiée ne peut pas devenir PASS.","source_url":"https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md"}]

## Sources {#sources}

| source | titre | lu |
|---|---|---|
| https://github.com/hoainho/img2threejs | Redirection du dépôt img2threejs vers le dépôt canonique de l'organisation | 2026-09-05 |
| https://github.com/img2threejs/img2threejs | README d'img2threejs | 2026-09-05 |
| https://github.com/img2threejs/img2threejs/blob/main/CHANGELOG.md | Changelog d'img2threejs | 2026-09-05 |
| https://github.com/img2threejs/img2threejs/releases/tag/v1.5.1 | Release 1.5.1 : ajout de la voie de référence GLB | 2026-09-05 |
| https://buttondown.com/surfaced/archive/surfaced-friday-july-24-2026/ | Surfaced — vendredi 24 juillet 2026 | 2026-09-05 |

## Brief pour l'agent {#agent-brief}

- **Sujet :** `project:img2threejs`, fil `img2threejs`, 1 événement daté du 2026-07-24 au 2026-07-24.
- **Note pratique :** Au 2026-07-24, les praticiens peuvent utiliser le dépôt GitHub lié comme référence source publique du projet, tout en vérifiant directement ses fonctionnalités et son statut de version actuels avant de s'y fier.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
