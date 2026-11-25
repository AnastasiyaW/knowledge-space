---
title: "Muster für den Speicherabruf"
category: patterns
tags: [llm-memory, retrieval, semantic-search, bm25, hybrid-search, reranking, index-navigation]
level: 3
source_sha256: 2da298bbd2a94de2267c603841c71b79c8727a871f8bd1a05c0b9d76c6bc1a2d
translation: machine
translated_at: '2026-10-24'
---
# Muster für den Speicherabruf {#memory-retrieval-patterns}

So finden Agenten relevante Informationen in ihrem Speicher. Die Abrufmethode bestimmt die Trefferqualität (Recall), die Latenz und die Kosten. Unterschiedliche Ansätze funktionieren bei unterschiedlichen Datenmengen.

## Wichtigste Fakten {#key-facts}

- Indexbasierte Navigation funktioniert bis etwa 500 Artikel ohne Abrufkosten
- BM25 (Schlüsselwort) findet exakte Treffer, die semantische Suche übersieht
- Vektorähnlichkeit findet semantische Treffer, die Schlüsselwortsuche übersieht
- Hybrid (BM25 + Vektor) mit Reranking ist der zuverlässigste Ansatz für den Produktivbetrieb
- Leichtgewichtiges LLM-Reranking (~$0,001 pro Anfrage) kann den Recall von 96,6 % auf ~100 % anheben
- Die Abruflatenz summiert sich in Agentenschleifen. Daher vorab laden beim Start des Plans, nicht bei jedem Schritt

## Vergleich der Abrufmethoden {#retrieval-methods-comparison}

| Methode | Skalierung | Kosten/Anfrage | Recall | Latenz | Ideal für |
|--------|-----------|-----------|--------|---------|----------|
| **Indexnavigation** | <500 Artikel | ~0 | Abhängig von der Qualität des Index | <100ms | Kleine Wissensbasen |
| **Schlüsselwort/BM25** | Beliebig | ~0 | Hoch bei exakten Treffern | <10ms | Bekannte Terminologie |
| **Vektorähnlichkeit** | Beliebig | Embedding-Kosten | Hoch bei semantischen Treffern | 10-100ms | Unscharfe/konzeptuelle Anfragen |
| **Hybrid (BM25+Vektor)** | Beliebig | Embedding-Kosten | Am höchsten | 20-150ms | Produktivsysteme |
| **LLM-Reranking** | Beliebig | ~$0,001 | Nahezu perfekt | +200-500ms | Kritische Genauigkeitsanforderungen |

## Indexbasierte Navigation {#index-based-navigation}

Der einfachste Abruf: Der Agent liest einen Index, wählt relevante Dateien aus und liest diese.

```markdown
# Memory Index (agent reads this first)

## User Preferences
- db-preference - PostgreSQL, pgvector, reasons
- editor - Neovim, plugins, keybindings

## Current Projects
- api-rewrite - GraphQL migration, Q2 deadline
```

**So funktioniert es:** Der Index passt in den Kontext (~500 Token für 100 Einträge). Der Agent gleicht die Anfrage des Nutzers mit den Indexeinträgen ab und liest die passenden Dateien. Keine Embeddings, keine Suchinfrastruktur.

**Skalierung:** Ab etwa 500 Einträgen überschreitet der Index selbst eine handhabbare Kontextgröße. Dann in domänenspezifische Indizes aufteilen oder eine Suche ergänzen.

## Schlüsselwortsuche (BM25) {#keyword-search-bm25}

Abruf auf Basis der Termhäufigkeit. Findet Dokumente, die die exakten Wörter der Anfrage enthalten.

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

**Stärken:** Schnell, kostenlos, deterministisch, findet exakte Terminologie.
**Schwächen:** Übersieht semantisch ähnliche, aber lexikalisch verschiedene Inhalte („car“ findet kein „automobile“).

## Vektorähnlichkeitssuche {#vector-similarity-search}

Anfrage und Dokumente werden eingebettet, anschließend werden die nächsten Vektoren gesucht. Details finden sich unter [[embeddings]] und [[vector-databases]].

```python
import chromadb

collection = client.get_collection("memory")

results = collection.query(
    query_texts=["What database does the user prefer?"],
    n_results=5,
    where={"valid_to": None}  # only current facts
)
```

**Stärken:** Semantisches Verständnis, behandelt Paraphrasen, funktioniert sprachübergreifend.
**Schwächen:** Übersieht manchmal exakte Schlüsselwort-Treffer, nicht deterministisch, benötigt Embedding-Infrastruktur.

## Hybridsuche {#hybrid-search}

BM25- und Vektorsuche werden kombiniert. Es gibt zwei Strategien zum Zusammenführen:

### Gewichtete Summe {#weighted-sum}

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

**Problem:** `alpha` muss je Domäne abgestimmt werden. 0,5 ist selten optimal.

### Reciprocal Rank Fusion (RRF) {#reciprocal-rank-fusion-rrf}

Zusammenführung anhand der Rangposition, keine Abstimmung von `alpha` nötig:

```python
def rrf_merge(ranked_lists: list[list], k: int = 60) -> list:
    """Merge multiple ranked lists using Reciprocal Rank Fusion."""
    scores = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list):
            scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (rank + k)
    return sorted(scores.items(), key=lambda x: -x[1])
```

**RRF wird bevorzugt**, weil keine Normalisierung der Scores und keine Abstimmung von `alpha` nötig ist. Es funktioniert mit beliebig vielen Abrufmethoden.

## LLM-Reranking {#llm-reranking}

Nach dem initialen Abruf rangiert ein LLM die Kandidaten nach Relevanz neu:

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

**Kosten:** ~$0,001 pro Anfrage mit einem kleinen Modell. Hebt den Recall in Benchmarks von 96,6 % auf ~100 %.

**Alternative:** Cross-Encoder-Reranking (ohne LLM):

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
pairs = [(query, doc) for doc in candidates]
scores = reranker.predict(pairs)
```

Cross-Encoder sind schneller und günstiger als LLM-Reranking, aber weniger flexibel.

## Muster {#patterns}

### Vorab laden beim Start des Plans {#pre-fetch-at-plan-start}

Nicht bei jedem Agentenschritt abrufen. Stattdessen den Abruf gebündelt am Anfang jeder Planphase ausführen:

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

Dadurch entfällt die Abruflatenz bei jedem LLM-Aufruf, und der Ablauf des Agenten bleibt ungestört.

### Metadatengefilterter Abruf {#metadata-filtered-retrieval}

Den Suchraum vor der Ähnlichkeitsberechnung einschränken:

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

Metadatenfilter werden in den meisten Datenbanken vor der Vektorsuche angewendet. Das Metadatenschema sollte daher sorgfältig entworfen werden.

## Kostenvergleich {#cost-comparison}

Für 1.000 Anfragen pro Monat gegen 10.000 Dokumente:

| Methode | Infrastruktur | Pro Anfrage | Monatlich gesamt |
|--------|---------------|-----------|---------------|
| Indexnavigation | ~$0 (Dateien) | ~$0 | ~$0 |
| Nur BM25 | ~$5 (Rechenleistung) | ~$0 | ~$5 |
| Nur Vektor | ~$20 (Vektor-DB) | ~$0,0005 | ~$20,50 |
| Hybrid + Reranking | ~$20 (Vektor-DB) | ~$0,001 | ~$21 |

Der Kostenunterschied zwischen den Ansätzen ist gering. Die Wahl sollte sich nach der Trefferqualität richten, nicht nach dem Preis.

## Fallstricke {#gotchas}

- **Vektorsuche kann offensichtlich vorhandenen Text übersehen.** Die Kosinusähnlichkeit versagt manchmal dort, wo die Schlüsselwortsuche trivial erfolgreich ist. Bei kritischen Anwendungen immer mit BM25 kombinieren. Bekannte Ähnlichkeitsfehler sind unter [[embeddings]] beschrieben
- **Die Abruflatenz summiert sich in Agentenschleifen.** Ein Agent, der 20 Schritte mit jeweils einer Vektorsuche ausführt, addiert 2-4 Sekunden Abruflatenz. Beim Start des Plans vorab laden oder Ergebnisse innerhalb einer Aufgabe zwischenspeichern. Abrufanfragen wo möglich bündeln
- **Der Entwurf der Metadatenfilter ist dauerhaft.** Eine Änderung des Metadatenschemas erfordert das Neuindizieren aller Dokumente. Die Metadatenfelder (wing, room, type, valid_from, valid_to) vor der ersten Indizierung planen. Später hinzugefügte Felder bedeuten, dass alles erneut verarbeitet werden muss

## Siehe auch {#see-also}

- [[memory-architectures]]
- [[verbatim-vs-extraction]]
- [[knowledge-base-as-memory]]
- [[vector-databases]]
- [[embeddings]]
- [[rag-pipeline]]
