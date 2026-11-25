---
title: "Verbatim-Speicherung vs. LLM-Extraktion"
category: concepts
tags: [llm-memory, verbatim, extraction, memory-quality, retrieval-accuracy]
level: 3
source_sha256: 061608cb33b78edd799f527b817cc641a4ed28a92928eda3db2c5829e043c354
translation: machine
translated_at: '2026-10-24'
---
# Verbatim-Speicherung vs. LLM-Extraktion {#verbatim-storage-vs-llm-extraction}

Die Frage, ob rohe Texte oder per LLM extrahierte Fakten im Speicher abgelegt werden sollen. Empirisch erreicht rohes Verbatim-Material mit Standard-Embeddings auf Langzeitgedächtnis-Benchmarks einen Recall@5 von 96,6 %, während extraktionsbasierte Systeme bei etwa 85 % stagnieren. Das ist kontraintuitiv, aber Extraktion ist verlustbehaftet.

## Kernfakten {#key-facts}

- Verbatim + Standard-Embeddings = 96,6 % R@5 auf LongMemEval, ohne LLM-Aufrufe zur Retrieval-Zeit
- Extraktionsbasierte Systeme (Mem0, Zep) = ~85 % R@5, deutlich schlechter, obwohl sie beim Schreiben und Lesen ein LLM verwenden
- Ein leichtgewichtiges LLM-Reranking (~0,001 $ pro Anfrage) hebt das Verbatim-Retrieval auf ~100 % (500/500)
- Die Lücke entsteht, weil Extraktion Kontext, Nuancen und Begründungen verwirft
- Kostenunterschied: ~10 $ pro Jahr für Verbatim-Speicherung vs. ~500 $ pro Jahr für Systeme, die bei jedem Schreibvorgang zusammenfassen

## Warum Extraktion Informationen verliert {#why-extraction-loses-information}

Wenn das LLM aus einer Konversation „Nutzer bevorzugt PostgreSQL“ extrahiert, gehen folgende Informationen verloren:

1. **Die Begründung**: „...weil pgvector Ähnlichkeitssuche ohne separate Vektordatenbank ermöglicht und wir Postgres bereits im Produktivbetrieb haben“
2. **Der Kontext**: Diese Präferenz wurde geäußert, während Datenbanken für ein bestimmtes ML-Pipeline-Projekt evaluiert wurden
3. **Die Einschränkungen**: „...aber nur für Datensätze unter 10 Mio. Zeilen; darüber hinaus würden wir ClickHouse in Betracht ziehen“
4. **Der zeitliche Kontext**: Wann diese Entscheidung getroffen wurde und welche Alternativen betrachtet wurden
5. **Das emotionale Gewicht**: „Wir haben MySQL drei Monate lang ausprobiert, und es war qualvoll“ – ein Signal für eine starke Präferenz

Der extrahierte Fakt ist technisch korrekt, reicht aber nicht aus, damit der Agent künftige Datenbankentscheidungen gut begründen kann.

## Vergleich der Retrieval-Qualität {#retrieval-quality-comparison}

| Ansatz | R@5 | LLM-Aufrufe (Schreiben) | LLM-Aufrufe (Lesen) | Kosten/Jahr |
|--------|-----|-------------------------|---------------------|-------------|
| Verbatim + Embeddings | 96,6 % | 0 | 0 | ~10 $ |
| Verbatim + LLM-Reranking | ~100 % | 0 | 1 (günstig) | ~15 $ |
| Extraktion (Mem0-artig) | ~85 % | 1 pro Schreibvorgang | 1 pro Lesevorgang | ~500 $ |
| Zusammenfassung | ~80 % | 1 pro Schreibvorgang | 0–1 | ~300 $ |

## Wann Verbatim gewinnt {#when-verbatim-wins}

- **Konversationelles Gedächtnis**: Nutzerpräferenzen, Entscheidungen, Feedback – das *Warum* ist genauso wichtig wie das *Was*
- **Episodisches Erinnern**: „Was ist in jenem Meeting passiert?“ – benötigt die originale Formulierung, keine Zusammenfassung
- **Mehrstufiges Schlussfolgern**: Der Agent muss die Gedankenkette rekonstruieren, die zu einer Entscheidung geführt hat
- **Geringes Volumen, hoher Wert**: <100K Einträge, bei denen die Speicherkosten vernachlässigbar sind

## Wann Extraktion gewinnt {#when-extraction-wins}

- **Strukturierte Abfragen**: „Welche Zeitzone hat der Nutzer?“ – ein Schlüssel-Wert-Fakt, keine Nuancen nötig
- **Sitzungsübergreifende Aggregation**: Zusammenführen von Informationen aus 50 Konversationen zu einem Nutzerprofil
- **Speicherbeschränkte Umgebungen**: Eingebettete Geräte, Edge-Deployments mit begrenztem Speicher
- **Hohes Volumen, geringer Wert**: Millionen von Einträgen, von denen die meisten nie abgerufen werden

## Muster {#patterns}

### Hybrid: Verbatim + extrahierter Index {#hybrid-verbatim-extracted-index}

Beides speichern – Verbatim für die Retrieval-Qualität, Extraktion für strukturierten Zugriff:

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

### Verbatim mit Metadaten-Anreicherung {#verbatim-with-metadata-enrichment}

LLM-Extraktion überspringen, aber strukturierte Metadaten für das Filtern hinzufügen:

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

### Graphbasierte Kompression (MemPalace-Muster) {#graph-based-compression-mempalace-pattern}

Anstatt zwischen Verbatim und Extraktion zu wählen, werden beide in einem Wissensgraphen gespeichert: Rohtext als „Räume“ und extrahierte Entitäten bzw. Beziehungen als Kanten. Das Retrieval durchläuft den Graphen und lädt Verbatim-Text nur für relevante Knoten. Dabei wird eine etwa 30-fach verlustfreie Kompression gegenüber flacher Verbatim-Speicherung erreicht, indem Entitätsreferenzen über Erinnerungen hinweg dedupliziert werden.

Zentrale Architektur:
1. **Ingest**: Verbatim-Text mit positionsbewusstem Chunking speichern
2. **Extrahieren**: Entitätsgraph (Personen, Projekte, Entscheidungen) aus den Chunks aufbauen
3. **Verknüpfen**: Bidirektionale Kanten zwischen Entitäten und Quell-Chunks
4. **Abrufen**: Graph-Traversierung von den Abfrage-Entitäten aus → nur relevante Verbatim-Chunks laden

Dies umgeht den Informationsengpass reiner Extraktionssysteme (der Graph bewahrt den vollständigen Quelltext) und erreicht Kompressionsraten, die mit flacher Verbatim-Speicherung unmöglich wären (gemeinsame Entitäten werden einmal gespeichert und vielfach referenziert).

### Kompressionsverfahren, die die Qualität erhalten {#compression-approaches-that-preserve-quality}

Verlustbehaftete Abkürzungsschemata (eigene Dialekte, Akronymkompression) verschlechtern nachweislich das Retrieval. In Benchmarks sank die Baseline von 96,6 % bei aggressiver Kompression auf 84,2 %. Fehler bei der Token-Zählung in Kompressionsimplementierungen sind häufig – immer mit einem geeigneten Tokenizer validieren, nicht mit `len(text) // 3`.

Standardmäßige Textkompression (gzip) wirkt auf der Speicherebene, senkt aber die Embedding-Kosten nicht, da vor dem Embedding dekomprimiert werden muss.

## Fallstricke {#gotchas}

- **LLM-Extraktion hat einen grundlegenden Informationsengpass.** Das LLM muss zur Schreibzeit entscheiden, was „wichtig“ ist, die Wichtigkeit hängt aber von künftigen Abfragen ab, die noch nicht stattgefunden haben. Verbatim-Speicherung verlagert diese Entscheidung auf die Retrieval-Zeit, wo der Abfragekontext vorliegt
- **Die Schätzung der Token-Anzahl ist fehleranfällig.** Niemals `len(text) // 3` oder `len(text) // 4` zur Token-Schätzung verwenden. Einen geeigneten Tokenizer verwenden (tiktoken für OpenAI, tokenizers für HuggingFace). Falsche Schätzungen führen zu fehlerhaften Kostenvergleichen und Budgetüberschreitungen
- **Verbatim bedeutet nicht unverarbeitet.** Den Text vor dem Speichern bereinigen: UI-Artefakte entfernen, Leerzeichen normalisieren, irrelevante Metadaten entfernen. Der Inhalt sollte wörtlich erhalten bleiben, die Formatierung aber sauber sein

## Siehe auch {#see-also}

- [[memory-architectures]]
- [[memory-retrieval-patterns]]
- [[embeddings]]
- [[chunking-strategies]]
- [[forgetting-strategies]]
