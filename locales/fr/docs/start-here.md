---
title: Commencer ici
description: "Un parcours orienté tâches à travers Happyin Knowledge Space pour les personnes qui ont besoin d'une prochaine étape technique fiable."
---
# Commencer ici {#start-here}

Utilisez cette page lorsque vous avez une tâche technique concrète et souhaitez le chemin le plus court et le plus fiable vers la base de connaissances. Vous n'avez besoin ni de compte ni d'une installation locale : effectuez une recherche, ouvrez une référence, puis vérifiez son contexte de version et ses pièges avant de l'appliquer.

## Avant de commencer {#before-you-start}

Partez d'un résultat concret, et non d'une vaste étiquette technologique. De bonnes questions de départ sont :

- « Comment déployer un service Python avec un chemin de déploiement sûr ? »
- « Quelle approche de génération d'images convient à une retouche contrôlée ? »
- « Pourquoi ce rééquilibrage de consommateur Kafka provoque-t-il des doublons ? »
- « Comment fournir à mon agent de code un contexte fiable ? »

Si vous connaissez déjà un outil, un modèle, une erreur ou une commande, utilisez d'abord la zone de recherche. Si vous ne connaissez que le résultat recherché, choisissez un parcours ci-dessous.

## 1. Choisir la tâche la plus proche {#1-choose-the-closest-task}

| Je dois… | Commencer ici | Puis aller à |
|---|---|---|
| Construire ou étendre un workflow IA/image | [Image Generation](image-generation/index.md) | les pages sur les modèles, l'édition, LoRA, les workflows ou l'infrastructure |
| Construire un service ou un produit web | [Architecture](architecture/index.md) | [Python](python/index.md), [Web Frontend](web-frontend/index.md) et [DevOps](devops/index.md) |
| Déplacer, analyser ou interroger des données | [Data Engineering](data-engineering/index.md) | [BI & Analytics](bi-analytics/index.md), [SQL & Databases](sql-databases/index.md) ou [Data Science](data-science/index.md) |
| Travailler avec des modèles de langage ou des workflows autonomes | [LLM & Agents](llm-agents/index.md) | [LLM Memory](llm-memory/index.md) et [Security](security/index.md) |
| Travailler avec la parole, la transcription ou la voix synthétique | [Audio & Voice](audio-voice/index.md) | la comparaison de modèles, la latence et les notes sur le déploiement multilingue |
| Déboguer, tester ou améliorer du code existant | [Testing & QA](testing-qa/index.md) | la section sur le langage ou le framework de votre base de code |

## 2. Lire une page comme une aide à la décision {#2-read-a-page-as-a-decision-aid}

Chaque référence est volontairement dense. Lisez-la dans cet ordre :

1. Vérifiez la version, la date et le périmètre. Une recommandation de modèle ou de framework de 2024 peut ne pas convenir à une installation de 2026.
2. Repérez le motif d'implémentation ou le bloc de configuration qui correspond à votre environnement.
3. Lisez **Gotchas** avant de copier des commandes. Ils décrivent les modes de défaillance que l'exemple du cas nominal ne peut pas montrer.
4. Suivez **See also** uniquement lorsque vous avez besoin de la décision voisine ; n'ouvrez pas tout un domaine par défaut.

La base de connaissances est un point de départ pour une décision, et non une autorité qui remplace les tests dans votre propre environnement.

## 3. L'utiliser avec un assistant IA {#3-use-it-with-an-ai-assistant}

Pour un agent, donnez-lui la page pertinente ou demandez-lui de chercher dans le dépôt avant de proposer une solution. Le [guide pour agents](for-llm-agents.md) contient un prompt court, des index lisibles par machine et le contrat de retour d'information.

Lorsque vous demandez à un agent d'agir, indiquez le résultat attendu, votre environnement et la page source. Par exemple :

```text
Read the relevant Happyin Knowledge Space page before proposing a change.
My outcome is: deploy a Python API with rollback and observable health checks.
Use the version context and Gotchas from the source; tell me what must be verified locally.
```

## 4. Garder la réponse utile pour le lecteur suivant {#4-keep-the-answer-useful-for-the-next-person}

Si un article est manquant, obsolète ou erroné, utilisez la voie de retour d'information de la page ou le [guide de contribution](contributing/index.md). Un signalement utile indique l'article ou le sujet, le problème observé, la version ou l'environnement, et une source publique qui étaie la correction. N'incluez pas de code privé, d'identifiants ni de données utilisateur.

## La suite {#what-comes-next}

- Parcourez la [carte complète des domaines](index.md#domains) lorsque la tâche traverse plusieurs domaines.
- Lisez le [blog](blog/index.md) pour les contenus récemment ajoutés et les mises à jour du projet.
- Utilisez [Pour les agents IA](for-llm-agents.md) lorsque le prochain lecteur est un assistant de code plutôt qu'une personne.
