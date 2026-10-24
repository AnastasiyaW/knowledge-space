---
title: Commencez par la tâche
description: "Le chemin le plus court entre une tâche d'ingénierie et un contenu vérifiable de la base de connaissances."
---
# Commencez par la tâche {#_1}

Cette page vous aide à trouver le chemin le plus court et fiable vers la base. Nul besoin de compte ni d'installation locale, seulement un objectif précis : trouvez la source, vérifiez la version et lisez les limites avant de copier la configuration.

## 1. Formulez le résultat attendu {#1}

Une bonne requête décrit le résultat attendu et l'environnement :

- « Déployer un service Python en toute sécurité avec retour arrière et contrôle de santé » ;
- « Choisir une approche d'édition d'image contrôlée » ;
- « Comprendre pourquoi un consumer Kafka crée des doublons après un rebalance » ;
- « Fournir à un agent de codage un contexte technique vérifiable ».

Si le modèle, la bibliothèque, l'erreur ou la commande sont déjà connus, utilisez la recherche du site ou la [carte de la base](knowledge-base/index.md). Si seul le résultat est connu, commencez par l'itinéraire ci-dessous.

## 2. Choisissez l'itinéraire le plus proche {#2}

| J'ai besoin de | Commencer ici | Puis |
|---|---|---|
| Construire un workflow AI ou image | [Image Generation](image-generation/index.md) | modèle, édition, LoRA, workflow ou infrastructure |
| Déployer un service ou un produit web | [Architecture](architecture/index.md) | [Python](python/index.md), [Web Frontend](web-frontend/index.md) et [DevOps](devops/index.md) |
| Transférer, analyser ou interroger des données | [Data Engineering](data-engineering/index.md) | [BI & Analytics](bi-analytics/index.md), [SQL](sql-databases/index.md) ou [Data Science](data-science/index.md) |
| Travailler avec des LLM ou des workflows autonomes | [LLM & Agents](llm-agents/index.md) | [LLM Memory](llm-memory/index.md) et [Security](security/index.md) |
| Travailler avec la parole, la transcription ou la voix synthétique | [Audio & Voice](audio-voice/index.md) | modèle, latence et déploiement multilingue |
| Déboguer, tester ou améliorer du code existant | [Testing & QA](testing-qa/index.md) | langage ou framework de votre projet |

## 3. Lisez le contenu comme appui à la décision {#3}

1. Vérifiez d'abord la version, la date et le périmètre.
2. Repérez l'approche ou la configuration correspondant à votre environnement.
3. Lisez la section **Gotchas** avant d'exécuter les commandes : elle recense les échecs non évidents du chemin nominal.
4. Ouvrez les articles voisins uniquement s'ils sont nécessaires à la décision suivante.

La page de la base sert de point de départ pour une décision, et ne remplace pas les tests de votre infrastructure.

## 4. Utilisez-la avec un agent IA {#4-ai-}

Donnez à l'agent le lien vers le contenu, le résultat visé et l'environnement. Le contrat complet pour les agents figure dans le [guide dédié](for-llm-agents.md).

```text
Read the relevant Happyin Knowledge Space page before proposing a change.
My outcome is: deploy a Python API with rollback and observable health checks.
Use the version context and Gotchas from the source; tell me what must be verified locally.
```

## Si le contenu est insuffisant {#_2}

La base dispose d'un canal public de retour d'information (décrit dans le [guide pour les agents](for-llm-agents.md)). Le message doit indiquer la page ou le sujet, la version ou l'environnement, ainsi que la source publique. N'y envoyez ni code personnel, ni jetons, ni données utilisateur.
