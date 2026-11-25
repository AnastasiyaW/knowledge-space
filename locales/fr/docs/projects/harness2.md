---
title: "Harness^2: harness2-open-source-release — Version open source de Harness2"
category: "projects"
date: 2026-10-18
tags: ["harness2", "harness2-open-source-release", "project"]
aliases: ["Harness^2: harness2-open-source-release"]
level: 2
source_sha256: c78fda51470e0ac0f7e3829ba44f8dcade711c64c9074437357da30d45aabfaa
translation: machine
translated_at: '2026-10-24'
---
# Harness^2: harness2-open-source-release — Version open source de Harness2 {#harness2-harness2-open-source-release-harness2-open-source-release}

**Ligne de développement :** project:harness2 · fil harness2-open-source-release  
**Dernier événement :** 2026-10-18 · 3 événements datés depuis le 2026-10-18 · **Recherche :** 2026-10-19 · confiance : élevée

## Ce que c'est {#what-it-is}

Harness² est un cadre de recherche destiné aux ingénieurs qui testent si le système qui entoure un agent peut s'améliorer sans modifier les poids du modèle. Il édite et évalue les prompts, les garde-fous, la mémoire, les consignes d'utilisation des outils, les sous-agents, les compétences, les scripts et les plugins. Il prend en charge la récursion parallèle et séquentielle, les exécuteurs OpenCode et Codex, ainsi que trois intégrations de benchmarks.

Les exécutions reposant sur un modèle nécessitent une configuration locale et peuvent entraîner des coûts d'API. L'accès web des exécuteurs n'est pas restreint par défaut. Utilisez Harness² pour des expériences contrôlées d'amélioration de harnais, et non comme preuve qu'un harnais révisé est sûr pour une utilisation en production sans relecture.

## Ligne de développement {#development-line}

- **2026-10-18 — Harness^2 introduit l'optimisation récursive de harnais d'agents pour des modèles de langage figés.** Des auteurs de Google ont présenté Harness^2, un cadre qui optimise le harnais d'un modèle de langage figé (prompts, garde-fous, compétences, scripts, code intermédiaire) sans vérificateurs de référence. Il utilise une récursion au niveau des tâches et au niveau de la configuration, avec une bibliothèque d'améliorations réutilisable. Les scores moyens rapportés sur WorkBuddy-Bench sont passés de 64,2 à 75,7 pour GLM-5 avec k=1, et à 80,8 avec k=5. JobBench est passé de 31,5/32,9 à 39,0. Le billet précise que la vérification de plusieurs candidats augmente le coût en jetons d'inférence.
- **2026-10-18 — Google publie en open source le harnais d'agents Harness².** Le 2026-10-18, le lien enregistré indique que Google a publié Harness² en open source. Il est décrit comme un harnais prêt à l'emploi pour la gestion récursive d'agents d'IA dans des environnements ouverts. Les agents peuvent apprendre de leur expérience sur des tâches qui sortent du champ initial du harnais. Le harnais comporte huit composants : prompt système, garde-fous, mémoire, consignes d'utilisation des outils, sous-agents, compétences, scripts et plugins. Le dépôt GitHub associé est google-research/harness2.
- **2026-10-18 — Google publie en open source le harnais d'agents Harness².** Google a publié Harness² en open source. Il est décrit comme un harnais prêt à l'emploi pour la gestion récursive d'agents d'IA dans un environnement ouvert. Ses huit composants sont le prompt système, les contraintes de protection, la mémoire, les consignes d'utilisation des outils, les sous-agents, les compétences, les scripts et les plugins.
- **2026-10-18 — autres informations publiées à cette date.**
  - L'article associé indique que le harnais du modèle figé comporte huit composants modifiables, montés sous forme de fichiers. L'affinement au niveau des tâches utilise Propose–Probe–Compose sans retour de vérité terrain. Une boucle distincte au niveau du harnachement conserve, pour les tâches suivantes, les enseignements étayés par des preuves. (2026-10-09) — <https://arxiv.org/abs/2610.14224>
  - La publication consiste en un code source sous licence Apache-2.0, avec une procédure d'installation Linux/Python 3.12/uv et une démonstration locale déterministe qui ne nécessite aucun identifiant de modèle. Les exécutions de benchmarks reposant sur un modèle ajoutent Node.js, la Google Cloud CLI, les dépendances propres à chaque benchmark et la configuration de modèle de l'utilisateur. (date non précisée) — <https://github.com/google-research/harness2>
  - L'implémentation publique prend en charge les exécuteurs OpenCode et Codex, la récursion parallèle ou séquentielle, ainsi que JobBench, LAB et WorkBuddy-Bench. Son README avertit que l'accès réseau des exécuteurs n'est pas restreint et que Codex s'exécute avec son bac à sable désactivé, sauf si l'opérateur configure des restrictions réseau. (date non précisée) — <https://github.com/google-research/harness2>

## Ce qui a changé {#what-changed}

Publication publique (2026-10-18) : Harness² a rendu sa méthode de harnachement récursif disponible sous forme de dépôt de code sous licence Apache-2.0. L'article décrit un affinement au niveau des tâches selon Propose–Probe–Compose, ainsi que des mises à jour persistantes de la bibliothèque d'améliorations entre les tâches.

## Comment l'utiliser {#how-to-use-this}

1. Sous Linux avec Python 3.12 et uv, créez l'environnement virtuel documenté, installez le paquet en mode éditable et lancez la démonstration sans identifiants avant de connecter un modèle.
  — <https://github.com/google-research/harness2>
2. Pour une exécution reposant sur un modèle, installez l'environnement d'exécution et les dépendances de benchmarks listés, configurez les paramètres du modèle et l'authentification, puis commencez avec une seule tâche de benchmark et une sélection réduite.
  — <https://github.com/google-research/harness2>
3. Lancez la vérification, l'affinement, l'évaluation et la production de rapports avec le même benchmark, le même exécuteur, le même sous-ensemble, le même budget de récursion, le même mode et la même graine. Utilisez le mode simulation (dry-run) pour inspecter la sélection des tâches sans appels au modèle.
  — <https://github.com/google-research/harness2>
4. Choisissez la récursion parallèle pour explorer plus largement les harnais candidats, ou la récursion séquentielle pour enchaîner les affinements à travers des étapes successives. Ne conservez les harnais adoptés qu'avec les preuves d'exécution qui les étayent.
  — <https://github.com/google-research/harness2>

## Bonnes pratiques {#best-practices}

- Configurez des restrictions réseau avant l'évaluation, afin que les grilles d'évaluation, les réponses ou les critères de notation publics des benchmarks ne puissent pas fuiter vers un exécuteur disposant d'un accès web non restreint.
  — <https://github.com/google-research/harness2>
- Conservez une configuration d'évaluation identique à celle de l'exécution d'affinement lors de l'évaluation et de la production de rapports. Modifier le benchmark, l'exécuteur, le sous-ensemble, le mode de récursion, le budget ou la graine invalide la comparabilité du résultat.
  — <https://github.com/google-research/harness2>
- Considérez les budgets de récursion plus élevés comme un compromis explicite entre calcul et performance. L'article comptabilise à la fois les jetons d'exécution et ceux d'amélioration, et ses gains n'ont été mesurés que dans les configurations de benchmark évaluées.
  — <https://arxiv.org/abs/2610.14224>

## Remplacé par ceci {#superseded-by-this}

- Aucun élément marqué comme obsolète pour le moment.

## Toujours inconnu {#still-unknown}

- La page du dépôt ne fournit pas d'horodatage public stable de publication. Ses éléments d'événement sont donc marqués comme non datés, plutôt que de se voir attribuer une date de dépôt déduite.
- Aucun retour indépendant de praticiens sur une utilisation durable ou une reproduction des benchmarks n'a été trouvé dans les sources qualifiées.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://arxiv.org/abs/2610.14224 | Harness²: Recursive Agent Harnessing for an Open World | 2026-10-19 |
| https://github.com/google-research/harness2 | google-research/harness2: Recursive Agent Harnessing for an Open World | 2026-10-19 |

## Fiche pour agents {#agent-brief}

- **Sujet :** project:harness2, fil harness2-open-source-release, 3 événements datés du 2026-10-18 au 2026-10-18.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** élevée. Les remplacements datés ci-dessus font foi pour ce qui est obsolète.
