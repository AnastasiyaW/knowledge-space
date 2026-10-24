---
title: "Patrons de récupération de la mémoire"
category: patterns
tags: [llm-memory, retrieval, semantic-search, bm25, hybrid-search, reranking, index-navigation]
level: 3
source_sha256: 2da298bbd2a94de2267c603841c71b79c8727a871f8bd1a05c0b9d76c6bc1a2d
translation: machine
translated_at: '2026-10-24'
---
# Patrons de récupération de la mémoire {#memory-retrieval-patterns}

Comment les agents retrouvent les informations pertinentes dans leur mémoire. La méthode de récupération détermine la qualité du rappel, la latence et le coût. Les différentes approches s'adaptent à différentes échelles.

## Points clés {#key-facts}

- La navigation par index fonctionne jusqu'à ~500 articles, sans coût de récupération
- BM25 (par mots-clés) retrouve les correspondances exactes que la recherche sémantique manque
- La similarité vectorielle retrouve les correspondances sémantiques que la recherche par mots-clés manque
- L'approche hybride (BM25 + vecteurs) avec reranking est la plus fiable en production
- Un reranking léger par LLM (~0,001 $/requête) peut faire passer le rappel de 96,6 % à ~100 %
- La latence de récupération s'accumule dans les boucles d'agents : effectuez un pré-chargement au début du plan, et non à chaque étape

## Comparaison des méthodes de récupération {#retrieval-methods-comparison}

| Méthode | Échelle | Coût/requête | Rappel | Latence | Idéal pour |
|--------|-------|-----------|--------|---------|----------|
| **Navigation par index** | <500 articles | ~0 | Dépend de la qualité de l'index | <100 ms | Petites bases de connaissances |
| **Mots-clés/BM25** | Quelconque | ~0 | Élevé pour les correspondances exactes | <10 ms | Terminologie connue |
| **Similarité vectorielle** | Quelconque | Coût d'embedding | Élevé pour le sémantique | 10-100 ms | Requêtes floues ou conceptuelles |
| **Hybride (BM25+vecteurs)** | Quelconque | Coût d'embedding | Le plus élevé | 20-150 ms | Systèmes de production |
| **Reranking par LLM** | Quelconque | ~0,001 $ | Presque parfait | +200-500 ms | Besoins de précision critiques |

## Navigation par index {#index-based-navigation}

La récupération la plus simple : l'agent lit un index, choisit les fichiers pertinents et les lit.

```markdown
# Memory Index (agent reads this first)

## User Preferences
- db-preference - PostgreSQL, pgvector, reasons
- editor - Neovim, plugins, keybindings

## Current Projects
- api-rewrite - GraphQL migration, Q2 deadline
```

**Fonctionnement :** l'index tient dans le contexte (~500 tokens pour 100 entrées). L'agent compare la requête de l'utilisateur aux entrées de l'index et lit les fichiers pertinents. Pas d'embeddings, pas d'infrastructure de recherche.

**Passage à l'échelle :** à ~500 entrées, l'index lui-même dépasse une taille de contexte confortable. Découpez-le en index par domaine ou ajoutez une recherche.

## Recherche par mots-clés (BM25) {#keyword-search-bm25}

Récupération fondée sur la fréquence des termes. Trouve les documents contenant les mots exacts de la requête.

```python
from rank_bm25 import BM25Okapi

class KeywordMemory:
    def __init__(self, documents: list[str]):
        tokenized = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)
        self.documents = documents

    def search(self, query: str, top_k: int = 5) -> list[str]:
        tokens = query.lower().split()
        scores = self.bm25.get_scores(tokens)
        top_indices = scores.argsort()[-top_k:][::-1]
        return [self.documents[i] for i in top_indices if scores[i] > 0]
```

**Points forts :** rapide, gratuite, déterministe, retrouve la terminologie exacte.
**Points faibles :** manque les contenus sémantiquement proches mais lexicalement différents (« voiture » ne trouvera pas « automobile »).

## Recherche par similarité vectorielle {#vector-similarity-search}

Calculez l'embedding de la requête et des documents, puis recherchez les vecteurs les plus proches. Voir [[embeddings]] et [[vector-databases]] pour plus de détails.

```python
import chromadb

collection = client.get_collection("memory")

results = collection.query(
    query_texts=["What database does the user prefer?"],
    n_results=5,
    where={"valid_to": None}  # only current facts
)
```

**Points forts :** compréhension sémantique, gère les paraphrases, fonctionne entre les langues.
**Points faibles :** manque parfois les correspondances exactes de mots-clés, non déterministe, nécessite une infrastructure d'embeddings.

## Recherche hybride {#hybrid-search}

Combinez la recherche BM25 et la recherche vectorielle. Deux stratégies de fusion existent :

### Somme pondérée {#weighted-sum}

```python
def hybrid_search(query: str, alpha: float = 0.5, top_k: int = 5):
    bm25_scores = get_bm25_scores(query)      # normalized 0-1
    vector_scores = get_vector_scores(query)    # normalized 0-1

    combined = {}
    for doc_id in set(bm25_scores) | set(vector_scores):
        combined[doc_id] = (
            alpha * vector_scores.get(doc_id, 0) +
            (1 - alpha) * bm25_scores.get(doc_id, 0)
        )

    return sorted(combined.items(), key=lambda x: -x[1])[:top_k]
```

**Problème :** `alpha` doit être ajusté pour chaque domaine. 0,5 est rarement optimal.

### Fusion par rang réciproque (RRF) {#reciprocal-rank-fusion-rrf}

Fusion selon la position de rang, sans réglage d'alpha :

```python
def rrf_merge(ranked_lists: list[list], k: int = 60) -> list:
    """Merge multiple ranked lists using Reciprocal Rank Fusion."""
    scores = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list):
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (rank + k)
    return sorted(scores.items(), key=lambda x: -x[1])
```

**La RRF est préférée** car elle ne nécessite ni normalisation des scores ni réglage d'alpha. Elle fonctionne avec un nombre quelconque de méthodes de récupération.

## Reranking par LLM {#llm-reranking}

Après la récupération initiale, utilisez un LLM pour reclasser les candidats selon leur pertinence :

```python
def llm_rerank(query: str, candidates: list[str], top_k: int = 3) -> list[str]:
    prompt = f"""Rate each candidate's relevance to the query (0-10).
Query: {query}

Candidates:
{chr(10).join(f'{i+1}. {c[:200]}' for i, c in enumerate(candidates))}

Return JSON: [{{"index": 1, "score": 8}}, ...]"""

    scores = llm.complete(prompt, model="haiku")  # cheap model suffices
    ranked = sorted(scores, key=lambda x: -x["score"])
    return [candidates[s["index"]-1] for s in ranked[:top_k]]
```

**Coût :** ~0,001 $/requête avec un petit modèle. Fait passer le rappel de 96,6 % à ~100 % sur les benchmarks.

**Alternative :** reranking par cross-encoder (sans LLM) :

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
pairs = [(query, doc) for doc in candidates]
scores = reranker.predict(pairs)
```

Les cross-encoders sont plus rapides et moins coûteux que le reranking par LLM, mais moins flexibles.

## Patrons {#patterns}

### Pré-chargement au début du plan {#pre-fetch-at-plan-start}

Ne récupérez pas à chaque étape de l'agent. Regroupez la récupération au début de chaque phase du plan :

```python
def start_plan_phase(phase: str, subtasks: list[str]):
    # Pre-fetch all likely-needed context
    queries = [phase] + subtasks
    context = {}
    for q in queries:
        context[q] = memory.search(q, top_k=3)

    # Inject aggregated context once
    return format_context(context)
```

Cela évite la latence de récupération à chaque appel au LLM et préserve le déroulement ininterrompu de l'agent.

### Récupération filtrée par métadonnées {#metadata-filtered-retrieval}

Réduisez l'espace de recherche avant le calcul de similarité :

```python
results = collection.query(
    query_texts=["deployment configuration"],
    n_results=5,
    where={
        "$and": [
            {"wing": "project-api"},
            {"valid_to": None},
            {"room": {"$in": ["infrastructure", "deployment"]}}
        ]
    }
)
```

Dans la plupart des bases de données, le filtrage par métadonnées s'effectue avant la recherche vectorielle. Concevez donc soigneusement votre schéma de métadonnées.

## Comparaison des coûts {#cost-comparison}

Pour 1000 requêtes/mois sur 10 000 documents :

| Méthode | Infrastructure | Par requête | Total mensuel |
|--------|---------------|-----------|---------------|
| Navigation par index | ~0 $ (fichiers) | ~0 $ | ~0 $ |
| BM25 seul | ~5 $ (calcul) | ~0 $ | ~5 $ |
| Vecteurs seuls | ~20 $ (base vectorielle) | ~0,0005 $ | ~20,50 $ |
| Hybride + reranking | ~20 $ (base vectorielle) | ~0,001 $ | ~21 $ |

L'écart de coût entre les approches est faible. Choisissez en fonction de la qualité du rappel, et non du prix.

## Pièges courants {#gotchas}

- **La recherche vectorielle peut manquer un texte pourtant bien présent.** La similarité cosinus échoue parfois là où la recherche par mots-clés réussit trivialement. Combinez-la toujours avec BM25 pour les applications critiques. Voir [[embeddings]] pour les échecs de similarité connus
- **La latence de récupération s'accumule dans les boucles d'agents.** Un agent qui exécute 20 étapes avec une recherche vectorielle à chaque étape ajoute 2 à 4 secondes de latence. Effectuez un pré-chargement au début du plan ou mettez les résultats en cache pendant une tâche. Regroupez les requêtes de récupération lorsque c'est possible
- **La conception du filtrage par métadonnées est définitive.** Modifier le schéma de métadonnées impose de réindexer tous les documents. Planifiez vos champs de métadonnées (wing, room, type, valid_from, valid_to) avant l'indexation initiale. Ajouter de nouveaux champs plus tard implique de tout retraiter

## Voir aussi {#see-also}

- [[memory-architectures]]
- [[verbatim-vs-extraction]]
- [[knowledge-base-as-memory]]
- [[vector-databases]]
- [[embeddings]]
- [[rag-pipeline]]
