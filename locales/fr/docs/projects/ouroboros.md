---
title: "Ouroboros — Mises à jour publiques du projet"
category: projects
date: 2026-08-02
tags: [ouroboros, project, public-project-updates]
aliases: ["Ouroboros"]
level: 3
source_sha256: 11373893bf57967f6988e649cfe94f817a17b910fb87bcd08cfa26c6cc13587e
translation: machine
translated_at: '2026-10-24'
---
# Ouroboros — Mises à jour publiques du projet {#ouroboros-public-project-updates}

**Ligne de développement :** `project:ouroboros` · fil `public-project-updates`  
**Dernier événement :** 2026-08-02 · 1 événement daté depuis le 2026-08-02 · **Recherche :** 2026-09-07 · confiance : moyenne

## Ce que c'est {#what-it-is}

Ouroboros est un runtime d'agents IA pour ordinateur de bureau et sans interface (headless), et non un modèle.

- Mémoire locale : conserve l'historique des projets et la mémoire durable sur le disque.
- Exécuteur de modèles : fait tourner des modèles distants configurés ou un modèle GGUF local.
- Coordinateur : gère des agents spécialisés à travers les tâches.
- Auto-modification : modifie sa propre implémentation via des portes de revue.

Il nécessite un fournisseur de modèles configuré ou un modèle local, et l'auto-modification en fait un environnement local à haut niveau de confiance.

Utilisez-le pour des travaux de programmation et de recherche isolés et relisibles ; ne le traitez pas comme un service réseau sans surveillance.

## Ligne de développement {#development-line}

- **2026-08-02 — Code source public d'Ouroboros et référence de version.** Le 2026-08-02, une entrée sur Ouroboros pointait vers le dépôt GitHub et sa page releases/latest, aux côtés de références techniques et communautaires externes. Ce lot de liens marque un point de référence public, sans vérifier la version exacte, l'ensemble des modifications ni la paternité.

## Ce qui a changé {#what-changed}

- 2026-07-31 — Un rapport public sur l'architecture et les benchmarks est paru ; la v6.87.5 a livré des paquets de plateforme avec une limite de preuve d'artefact historiquement restreinte.
- 2026-08-02 — Des liens source mentionnent Ouroboros, mais l'absence du corps du message ne permet aucune affirmation sur une version, un modèle ou un benchmark.
- 2026-08-07 — La v6.90.0 a renforcé les routes des fournisseurs, les quotas, la délégation et les arrêts d'urgence.
- 2026-08-08 — Un rapport technique a formalisé l'évolution du noyau relu et séparé les instantanés de benchmarks figés de la lignée Hope en direct.
- 2026-08-21 — La v6.109.0 a ajouté un statut de coût des tâches en direct et des comptes d'agents prêts à l'ouverture.
- 2026-09-01 — La v6.114.0 est devenue la version stable, en ajoutant des contrôles de préservation des capacités et un basculement vers OpenRouter fondé sur la forme des requêtes.
- 2026-09-05 — La v7.0.0-rc.15 a été publiée en préversion avec un correctif de course sur le registre au démarrage concurrent, sans remplacer le canal stable.

## Comment l'utiliser {#how-to-use-this}

1. Téléchargez le paquet stable actuel pour la plateforme cible plutôt que de cloner le code source pour un usage courant.
  — <https://github.com/razzant/ouroboros/releases/latest>
2. Au premier lancement, configurez un fournisseur distant pris en charge ou un modèle GGUF local, puis définissez la politique de revue et le budget.
  — <https://github.com/razzant/ouroboros>
3. Lancez une tâche bornée via l'application de bureau ou `ouroboros run --start` ; gardez le travail externe dans un worktree Git séparé et exportez un patch si nécessaire.
  — <https://github.com/razzant/ouroboros>
4. Utilisez le mode source uniquement pour le développement, la modification ou les tests de vérification de verrouillage : synchronisez l'environnement verrouillé, démarrez le serveur, puis utilisez l'interface locale ou la CLI.
  — <https://github.com/razzant/ouroboros>

## Bonnes pratiques {#best-practices}

- Restez par défaut sur la dernière version stable ; traitez les versions candidates v7 (release candidates) comme des builds de test tant qu'une version n'est pas marquée stable.
  — <https://github.com/razzant/ouroboros/releases>
- Gardez le serveur sur la boucle locale (loopback). Une liaison non locale exige `OUROBOROS_NETWORK_PASSWORD` ou une entrée privée déjà authentifiée ; n'exposez jamais le contournement par mot de passe sur un LAN ouvert ou un port public.
  — <https://github.com/razzant/ouroboros/blob/main/docs/DEPLOYMENT.md>
- Utilisez le budget configuré et les contrôles de revue avant d'autoriser des modifications du noyau, car le runtime peut modifier son propre code, ses prompts, ses outils et ses dépendances.
  — <https://github.com/razzant/ouroboros>
- Pour les contributions au noyau, gardez un seul changement ciblé, testez un diff committé et obtenez une revue dans un contexte séparé, avec des preuves consignées.
  — <https://github.com/razzant/ouroboros/blob/main/CONTRIBUTING.md>

## Remplacé par ceci {#superseded-by-this}

- 2026-08-02 — Considérer le lien mutable `/releases/latest` comme preuve d'une version d'août est obsolète ; utilisez un tag épinglé à une date pour les affirmations historiques sur les versions.
- 2026-08-02 — « Bat Codex et Claude Code » est une formulation trop large comme guide opérationnel : les comparaisons rapportées dépendent du modèle et du harnais, et le rapport de juillet décrivait une parité sur GAIA et SWE-bench Pro.
- 2026-09-01 — Les conseils d'installation fondés sur la v6.87.5 ou la v6.90.0 sont remplacés par la version stable v6.114.0 ; la v7.0.0-rc.15 reste une préversion.

## Points restant inconnus {#still-unknown}

- Le texte original du message du 2026-08-02 n'est pas disponible ; aucune affirmation sur une version, un modèle ou un benchmark ne peut donc être rattachée en toute sécurité à cette date, au-delà d'une simple mention du projet avec source.
- Le rapport public lié est daté du 2026-07-31, et l'URL mutable de la dernière version renvoie désormais à une version du 2026-09-01 ; aucun des deux ne peut être rétrodaté à l'événement.
- Les résultats de benchmarks restent rapportés par les auteurs et n'ont pas été reproduits indépendamment ici. Le rapport de juillet donne 86,97 % pour la configuration Terminal-Bench citée, tandis que l'article d'août rapporte 86,74 %.
- Aucune recommandation officielle vérifiée en chinois simplifié pour ce dépôt précis n'a été trouvée. Le nom Ouroboros est aussi utilisé par des projets sans rapport ; la résolution d'identité future doit donc conserver l'ancrage du dépôt `razzant/ouroboros`.

## Sources {#sources}

| source | titre | consulté |
|---|---|---|
| https://github.com/razzant/ouroboros | GitHub - razzant/ouroboros : Ouroboros — agent IA auto-créateur. Né le 16 février 2026. | 2026-09-07 |
| https://habr.com/ru/companies/airi/articles/1065428/ | Mon agent Ouroboros a battu Codex avec Claude Code sur Terminal-Bench, OSWorld et CL-Bench. Il s'est écrit lui-même / Habr | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/latest | Release v6.114.0 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/tag/v6.87.5 | Release v6.87.5 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/ANative-Lab/Awesome-Self-Evolving-Agents/issues/74 | Vérification du périmètre : Ouroboros, runtime d'agent auto-modifiable et relu · Issue #74 | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/tag/v6.90.0 | Release v6.90.0 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://arxiv.org/abs/2608.08311 | Ouroboros : A Self-Developing Frontier Coding Agent with Reviewed Core Evolution | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases | Releases · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/releases/tag/v6.114.0 | Release v6.114.0 · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/blob/main/docs/DEPLOYMENT.md | ouroboros/docs/DEPLOYMENT.md at main · razzant/ouroboros · GitHub | 2026-09-07 |
| https://github.com/razzant/ouroboros/blob/main/CONTRIBUTING.md | ouroboros/CONTRIBUTING.md at main · razzant/ouroboros · GitHub | 2026-09-07 |

## Brief agent {#agent-brief}

- **Sujet :** `project:ouroboros`, fil `public-project-updates`, 1 événement daté du 2026-08-02 au 2026-08-02.
- **Note pratique :** voir les sections d'usage et de bonnes pratiques sourcées ci-dessus, y compris leurs limites.
- **Confiance :** moyenne. Les remplacements datés ci-dessus font autorité pour ce qui est obsolète.
