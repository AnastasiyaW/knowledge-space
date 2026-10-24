---
title: "Mémoire des LLM et persistance des connaissances"
type: MOC
level: 2
source_sha256: 71474d6e69cb1bff2d843d384162e84d85f59ebb1f7c776c939ada4f3422499c
translation: machine
translated_at: '2026-10-24'
---
# Mémoire des LLM et persistance des connaissances {#llm-memory-knowledge-persistence}

Patterns et architectures pour organiser les connaissances persistantes lorsqu'on travaille avec des agents LLM. Il ne s'agit pas de construire des systèmes RAG (voir [[agent-fundamentals]]), mais de la manière dont les agents mémorisent, oublient et gèrent les connaissances d'une session à l'autre.

## Architecture de la mémoire {#memory-architecture}
- [[memory-architectures]] - Fichiers plats, graphes hiérarchiques, magasins vectoriels, graphes de connaissances, approches hybrides
- [[verbatim-vs-extraction]] - Pourquoi le texte brut l'emporte sur l'extraction par LLM (96,6 % contre 85 %), et quand utiliser chacune des deux approches

## Gestion du contexte et de la fenêtre {#context-window-management}
- [[context-window-management]] - Chargement par couches (L0 à L3), budgets de tokens, compaction, patterns de réinjection

## Organisation des connaissances {#knowledge-organization}
- [[knowledge-base-as-memory]] - Pipeline brut -> wiki -> schéma, markdown brut contre RAG, opérations d'ingestion, de requête et de lint
- [[session-persistence]] - Fichiers de passation, fichiers de mémoire, fichiers d'état, patterns de journal

## Temporalité et récupération {#temporal-retrieval}
- [[temporal-memory]] - Périodes de validité, détection de l'obsolescence, décroissance temporelle, résolution des contradictions
- [[memory-retrieval-patterns]] - Navigation dans les index, BM25, recherche vectorielle, recherche hybride, reranking, comparaison des coûts

## Cycle de vie de la mémoire {#memory-lifecycle}
- [[forgetting-strategies]] - Compaction, archivage, TTL, scoring de pertinence, gestion de la taille de la mémoire

## Références complémentaires {#additional-references}

- [[knowledge-graph-memory]] - Patterns de graphes de connaissances persistants pour agents IA : résolution d'entités, étapes du pipeline, notes d'agent
- [[memory-priority-enforcement]] - Pattern de structuration de la mémoire d'un agent en deux niveaux : chargement permanent (critique) et chargement à la demande (référence)
- [[memory-transfer-learning]] - Transfert de mémoire entre domaines pour les agents de programmation
- [[shared-knowledge-layers]] - Lorsque plusieurs agents travaillent en parallèle, ils ont besoin d'un moyen structuré de partager leurs découvertes sans
- [[verbatim-retrieval-vs-extraction]] - Pourquoi le stockage verbatim brut l'emporte sur l'extraction par LLM pour la récupération de mémoire d'agent : benchmarks, MemPalace
