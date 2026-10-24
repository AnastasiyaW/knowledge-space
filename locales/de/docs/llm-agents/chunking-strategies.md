---
title: "Chunking-Strategien für Retrieval (September 2026)"
category: techniques
tags: [llm-agents, chunking, retrieval, rag, document-processing]
level: 3
source_sha256: 5f7a98f6bca65a5c1f0da7036ec5cb93987301816aa00d80e4cd91ae2fb9b0d9
translation: machine
translated_at: '2026-10-24'
---
# Chunking-Strategien für Retrieval (September 2026) {#chunking-strategies-for-retrieval-september-2026}

Überprüft am 2026-09-03. Chunking erzeugt die Retrieval-Einheiten für einen Dokumentenkorpus. Es gibt keine universell beste Chunk-Größe: Eine brauchbare Strategie bewahrt Belege und Metadaten und optimiert Retrieval- und Antwortqualität anhand eines realen Evaluationsdatensatzes.

## Vom Retrieval-Vertrag ausgehen {#start-from-the-retrieval-contract}

| Frage | Designimplikation |
|---|---|
| Was muss die Antwort zitieren? | Quelle, Version, Seite/Abschnitt und stabilen Locator erhalten |
| Wonach fragt der Nutzer? | Eine Einheit wählen, die genug Evidenz zur Beantwortung enthält |
| Welche Struktur ist vorhanden? | Überschriften, Datensätze, Tabellen und semantische Grenzen bevorzugen |
| Welches Modell verarbeitet das Ergebnis? | Das Token-Budget mit dem exakten Tokenizer messen |
| Wie werden Dokumente aktualisiert? | Chunk-Identität/Version stabil genug halten, um sie zu löschen und neu zu indexieren |

LangChain beschreibt Retrieval als modulare Pipeline aus Loadern, Text-Splittern, Embeddings, Vektorspeichern und Retrievern. Ein Splitter ist eine Komponente, nicht das gesamte Qualitätssystem. [LangChain retrieval](https://docs.langchain.com/oss/python/langchain/retrieval)

## Strategien {#strategies}

| Strategie | Einsatz, wenn | Hauptrisiko |
|---|---|---|
| Strukturbewusst | Überschriften, Datensätze und Absätze tragen Bedeutung | Beschädigte Eingabestruktur erzeugt schlechte Grenzen |
| Token-begrenzt | Das nachgelagerte Kontextlimit ist strikt | Nichtübereinstimmung von Tokenizer und Version |
| Parent-Child | Kleine Einheiten liefern präzises Retrieval, größere Einheiten ermöglichen gute Antworten | Verknüpfung zu Parents und Speicherkomplexität |
| Tabellen-/datensatzbewusst | Fakten stehen in Zeilen oder Feldern | Flachklopfen verliert Beziehungen |
| Semantische Grenze | Zusammenhängende Abschnitte sind wichtiger als feste Länge | Die Grenzheuristik kann inkonsistent sein |

Overlap nur wählen, wenn damit ein evaluiertes Problem mit Informationsverlust an Grenzen gelöst wird. Overlap erhöht Indexgröße, Retrieval-Duplikate und Prompt-Kosten.

## Strukturbewusster Splitter {#structure-aware-splitter}

Dieses Python-Beispiel verwendet das aktuelle eigenständige Paket LangChain text-splitters. Es erzeugt begrenzte Chunks und bevorzugt dabei Absatz- und Zeilengrenzen.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=80,
    separators=["\n\n", "\n", ". ", " ", ""],
)

chunks = splitter.split_text(
    "Heading\n\nFirst paragraph with evidence.\n\nSecond paragraph with context."
)
print(chunks)
```

Die numerischen Werte sind als Ausgangspunkt für die Evaluation zu verstehen, nicht als Standard, der für jeden Korpus passt.

## Metadatenvertrag {#metadata-contract}

```json
{
  "chunk_id": "policy-2026-09:section-4:chunk-02",
  "document_id": "policy-2026-09",
  "document_version": "sha256:...",
  "source_locator": {"section": "4", "page": 12},
  "parent_id": "policy-2026-09:section-4",
  "text": "..."
}
```

Metadaten müssen das Retrieval überstehen und den Antwortgenerator erreichen. Kann die finale Antwort nicht angeben, welche Version und welcher Abschnitt eine Aussage stützen, kann die Retrieval-Pipeline keine verlässliche Zitierung liefern.

## Evaluation {#evaluation}

Den gesamten Pfad evaluieren, nicht nur die Ähnlichkeit der Embeddings:

1. Repräsentative Fragen mit akzeptierten Quellen und erwarteten Antwortbedingungen erstellen.
2. Messen, ob die abgerufene Menge ausreichend Evidenz enthält.
3. Nach der Generierung Antwortkorrektheit und Genauigkeit der Zitate messen.
4. Fehlschläge untersuchen: Extraktion, Segmentierung, Embedding, Ranking, Kontext-Packing oder Modellnutzung.
5. Nach einer wesentlichen Änderung am Splitter unter einer neuen Dokument-/Versionsidentität neu indexieren.

## Stolperfallen {#gotchas}

- **Problem: Tabellen werden zu unbeschrifteter Prosa geglättet.** Zeilen- und Spaltenbeziehungen gehen vor dem Retrieval verloren. **Lösung:** Strukturierte Felder beibehalten oder eine stabile, beschriftete Darstellung mit Quell-Locator rendern.
- **Problem: Zeichenzahlen für ein token-begrenztes Modell verwenden.** Ein Chunk kann nach Formatierung oder bei mehrsprachiger Tokenisierung überlaufen. **Lösung:** Den finalen gepackten Kontext mit dem Tokenizer des Deployments messen.
- **Problem: Durch Overlap entstandene Duplikate indexieren.** Das Retrieval kann nahezu identische Chunks liefern und verdeckt dabei diverse Evidenz. **Lösung:** Ergebnisse deduplizieren oder diversifizieren und Overlap anhand von Evaluationsdaten begründen.
- **Problem: Neu indexieren ohne Dokumentversion.** Alte Chunks bleiben nach einer Quelländerung abrufbar. **Lösung:** Jeden Chunk an eine unveränderliche Dokumentversion binden und ersetzte Versionen löschen oder filtern.

## Siehe auch {#see-also}

- [[rag-pipeline]]
- [[embeddings]]
- [[tokenization]]
- [[vector-databases]]
- [[production-patterns]]

## Quellen {#sources}

- [LangChain retrieval overview](https://docs.langchain.com/oss/python/langchain/retrieval)
- [LangChain text splitters](https://docs.langchain.com/oss/python/integrations/splitters)
