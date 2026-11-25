---
title: "Stockage verbatim vs extraction par LLM"
category: concepts
tags: [llm-memory, verbatim, extraction, memory-quality, retrieval-accuracy]
level: 3
source_sha256: 061608cb33b78edd799f527b817cc641a4ed28a92928eda3db2c5829e043c354
translation: machine
translated_at: '2026-10-24'
---
# Stockage verbatim vs extraction par LLM {#verbatim-storage-vs-llm-extraction}

Choisir entre stocker le texte brut ou des faits extraits par un LLM en mémoire. Empiriquement, le texte verbatim brut avec les embeddings par défaut atteint 96,6 % de recall@5 sur les benchmarks de mémoire longue, tandis que les systèmes basés sur l'extraction plafonnent autour de 85 %. C'est contre-intuitif, mais l'extraction est avec perte d'information.

## Points clés {#key-facts}

- Verbatim + embeddings par défaut = 96,6 % de R@5 sur LongMemEval, sans aucun appel LLM au moment de la recherche
- Systèmes basés sur l'extraction (Mem0, Zep) = ~85 % de R@5, nettement moins bon, bien qu'ils utilisent un LLM à la fois à l'écriture et à la lecture
- Ajouter un reranking léger par LLM (~0,001 $/requête) fait passer la recherche verbatim à ~100 % (500/500)
- L'écart existe parce que l'extraction élimine le contexte, les nuances et le raisonnement
- Différence de coût : ~10 $/an pour le stockage verbatim contre ~500 $/an pour les systèmes qui résument à chaque écriture

## Pourquoi l'extraction perd de l'information {#why-extraction-loses-information}

Lorsque le LLM extrait « l'utilisateur préfère PostgreSQL » d'une conversation, il perd :

1. **Le raisonnement** : « ...parce que pgvector permet de faire de la recherche par similarité sans base de vecteurs séparée, et nous avons déjà Postgres en production »
2. **Le contexte** : cette préférence a été exprimée lors de l'évaluation de bases de données pour un projet de pipeline ML spécifique
3. **Les contraintes** : « ...mais seulement pour des jeux de données de moins de 10 M de lignes ; au-delà, nous envisagerions ClickHouse »
4. **Le contexte temporel** : quand cette décision a été prise et quelles alternatives ont été considérées
5. **Le poids émotionnel** : « nous avons essayé MySQL pendant 3 mois et c'était pénible », ce qui signale une forte préférence

Le fait extrait est techniquement correct, mais insuffisant pour que l'agent puisse raisonner correctement sur de futures décisions concernant les bases de données.

## Comparaison de la qualité de recherche {#retrieval-quality-comparison}

| Approche | R@5 | Appels LLM (écriture) | Appels LLM (lecture) | Coût/an |
|----------|-----|-------------------|-------------------|-----------|
| Verbatim + embeddings | 96,6 % | 0 | 0 | ~10 $ |
| Verbatim + reranking LLM | ~100 % | 0 | 1 (peu coûteux) | ~15 $ |
| Extraction (style Mem0) | ~85 % | 1 par écriture | 1 par lecture | ~500 $ |
| Résumé | ~80 % | 1 par écriture | 0-1 | ~300 $ |

## Quand le verbatim l'emporte {#when-verbatim-wins}

- **Mémoire conversationnelle** : préférences, décisions, retours des utilisateurs. Le *pourquoi* compte autant que le *quoi*
- **Rappel épisodique** : « que s'est-il passé lors de cette réunion ? » nécessite la formulation d'origine, pas un résumé
- **Raisonnement en plusieurs étapes** : l'agent doit reconstituer la chaîne de raisonnement qui a mené à une décision
- **Faible volume, forte valeur** : <100 K entrées, où le coût de stockage est négligeable

## Quand l'extraction l'emporte {#when-extraction-wins}

- **Recherches structurées** : « quel est le fuseau horaire de l'utilisateur ? » Il s'agit d'un fait clé-valeur, sans besoin de nuance
- **Agrégation inter-sessions** : combiner les informations de 50 conversations en un profil utilisateur
- **Environnements à stockage contraint** : appareils embarqués, déploiements en périphérie aux capacités de stockage limitées
- **Volume élevé, faible valeur** : des millions d'entrées dont la plupart ne seront jamais récupérées

## Patterns {#patterns}

### Hybride : verbatim + index extrait {#hybrid-verbatim-extracted-index}

Stocker les deux : le verbatim pour la qualité de recherche, l'extrait pour l'accès structuré :

```python
def store_memory(text: str, metadata: dict):
    # Store verbatim for high-quality retrieval
    vector_store.add(
        documents=[text],
        metadatas=[metadata],
        ids=[generate_id()]
    )

    # Extract structured facts for direct lookup
    facts = extract_facts(text)  # LLM call
    for fact in facts:
        structured_store.upsert(
            key=fact["key"],
            value=fact["value"],
            source_id=metadata["id"],
            valid_from=metadata["timestamp"]
        )
```

### Verbatim avec enrichissement de métadonnées {#verbatim-with-metadata-enrichment}

Ignorer l'extraction par LLM, mais ajouter des métadonnées structurées pour le filtrage :

```python
def store_with_metadata(text: str, context: dict):
    metadata = {
        "timestamp": context["timestamp"],
        "wing": context.get("person", "general"),
        "room": context.get("topic", "misc"),
        "hall": classify_type(text),  # simple rule-based, not LLM
        "token_count": count_tokens(text),
    }
    vector_store.add(documents=[text], metadatas=[metadata])
```

### Compression par graphe (pattern MemPalace) {#graph-based-compression-mempalace-pattern}

Plutôt que de choisir entre verbatim et extraction, stocker les deux dans un graphe de connaissances : le texte brut sous forme de « salles », et les entités et relations extraites sous forme d'arêtes. La recherche parcourt le graphe et ne récupère le texte verbatim que pour les nœuds pertinents. Cette approche permet d'atteindre une compression sans perte d'environ 30x par rapport au stockage verbatim à plat, en dédupliquant les références aux entités entre les mémoires.

Architecture clé :
1. **Ingestion** : stocker le texte verbatim avec un découpage conscient des positions
2. **Extraction** : construire un graphe d'entités (personnes, projets, décisions) à partir des fragments
3. **Liaison** : arêtes bidirectionnelles entre les entités et les fragments sources
4. **Recherche** : parcours du graphe depuis les entités de la requête, puis récupération des seuls fragments verbatim pertinents

Cela évite le goulot d'information des systèmes basés uniquement sur l'extraction (le graphe conserve l'intégralité du texte source) tout en atteignant des taux de compression impossibles avec du verbatim à plat (les entités partagées ne sont stockées qu'une fois et référencées plusieurs fois).

### Approches de compression préservant la qualité {#compression-approaches-that-preserve-quality}

Les schémas d'abréviation avec perte (dialectes personnalisés, compression par acronymes) dégradent empiriquement la recherche. Testé sur des benchmarks, le score de référence de 96,6 % chute à 84,2 % avec une compression agressive. Les bugs de comptage de tokens dans les implémentations de compression sont courants : toujours valider avec un tokenizer approprié, et non avec `len(text) // 3`.

La compression de texte standard (gzip) fonctionne au niveau du stockage, mais ne réduit pas les coûts d'embedding, car il faut décompresser avant d'embedder.

## Pièges {#gotchas}

- **L'extraction par LLM a un goulot d'information fondamental.** Le LLM doit décider ce qui est « important » au moment de l'écriture, alors que l'importance dépend de requêtes futures qui n'ont pas encore eu lieu. Le stockage verbatim reporte cette décision au moment de la recherche, qui dispose du contexte de la requête
- **L'estimation du nombre de tokens est sujette à erreur.** N'utilisez jamais `len(text) // 3` ou `len(text) // 4` pour estimer les tokens. Utilisez un tokenizer approprié (tiktoken pour OpenAI, tokenizers pour HuggingFace). Des estimations erronées conduisent à des comparaisons de coûts incorrectes et à des dépassements de budget
- **Verbatim ne signifie pas non traité.** Nettoyer le texte avant de le stocker : supprimer les artefacts d'interface, normaliser les espaces, retirer les métadonnées non pertinentes. Le contenu doit rester verbatim, mais la mise en forme doit être propre

## Voir aussi {#see-also}

- [[memory-architectures]]
- [[memory-retrieval-patterns]]
- [[embeddings]]
- [[chunking-strategies]]
- [[forgetting-strategies]]
