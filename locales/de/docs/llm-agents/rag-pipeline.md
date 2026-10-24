---
title: "RAG-Pipeline-Design (September 2026)"
category: techniques
tags: [llm-agents, rag, retrieval, grounding, citations, evaluation]
level: 3
source_sha256: 261b8c6bb7f225b53f0af2bff1031287053e86fa789c3e585f1ee1733eb29234
translation: machine
translated_at: '2026-10-24'
---
# RAG-Pipeline-Design (September 2026) {#rag-pipeline-design-september-2026}

Überprüft am 2026-09-03. Retrieval-Augmented Generation (RAG) stellt einem Generierungsschritt zur Laufzeit ausgewählte externe Evidenz bereit. Damit lässt sich der Zugriff auf sich ändernde oder private Wissensbestände verbessern, doch eine Antwort wird dadurch nicht automatisch faktisch korrekt, aktuell, autorisiert oder korrekt zitiert.

## Als Datenprodukt aufbauen {#build-it-as-a-data-product}

```text
authoritative sources
    -> ingest with provenance and access policy
    -> normalize and split into citation-preserving units
    -> embed/index as an immutable generation
    -> retrieve and filter candidates at query time
    -> generate only from allowed evidence
    -> validate citations, outcome, and feedback
```

Jeder Pfeil ist eine Release-Grenze. Ändert sich ein Dokument, muss das System die betroffenen Chunks, Embeddings, Index-Generationen und veröffentlichten Antworten identifizieren können.

## Quelldatensatz vor dem Chunking {#source-record-before-chunking}

| Feld | Zweck |
|---|---|
| Stabile ID und Locator | Ermöglicht es, dass eine Antwort auf eine für Menschen lesbare Quelle verweist |
| Revision/Zeitpunkt | Unterscheidet aktuelle Evidenz von ersetzten Inhalten |
| Eigentümer und Autorität | Zeigt, ob eine Quelle eine Aussage stützen kann |
| Zugriffsbereich | Verhindert, dass Retrieval zu einer Umgehung von Berechtigungen wird |
| Parser-/Splitter-Version | Erklärt ein verändertes Retrieval-Ergebnis |

Nimm eine URL oder Datei nicht allein deshalb auf, weil sie erreichbar ist. Lege zuerst Autorität, Lizenz und Aktualitätsrichtlinie explizit fest.

## Vertrag zur Abfragezeit {#query-time-contract}

1. Klassifiziere die Anfrage und ihren Zugriffsbereich.
2. Ermittle Kandidaten aus der benannten Index-Generation.
3. Wende deterministische Metadaten- und Autorisierungsfilter an, bevor das Modell Inhalte sieht.
4. Übergib Auszüge zusammen mit stabilen Quell-Locatorn und Revisionsmetadaten.
5. Verlange von der Antwortschicht, Evidenz zu zitieren, oder einen expliziten Zustand für unzureichende Evidenz auszugeben.
6. Speichere den Retrieval-Beleg getrennt vom generierten Fließtext.

```json
{
  "query_id": "q-482",
  "index_generation": "kb-2026-09-03-02",
  "candidates": [
    {"source_id": "policy-14", "revision": "sha256:...", "locator": "policy.md#citations"}
  ],
  "access_policy": "editorial-internal",
  "outcome": "EVIDENCE_SUFFICIENT"
}
```

## Retrieval getrennt evaluieren {#evaluate-retrieval-separately}

Eine Antwort kann hilfreich klingen, obwohl das Retrieval fehlgeschlagen ist. Pflege einen Testsatz von Anfragen mit erwarteten bzw. verbotenen Quellkennungen, erwarteter Zitiergranularität und relevanten Berechtigungsgrenzen. Analysiere Fehler nach Kategorie: keine Evidenz, falsches Dokument, veraltete Revision, fehlender Abschnitt, falsche Sprache, Berechtigungsverletzung oder nicht gestützte Synthese.

Standardwerte öffentlicher Frameworks sind Hypothesen und keine Evaluation deines Korpus. Die sinnvolle Chunk-Größe, Überlappung, Retriever und Reranker hängen von der Dokumentstruktur und den Evidenzanforderungen der Aufgabe ab.

## Aktualisierung und Rollback {#update-and-rollback}

Erzeuge eine neue Index-Generation, wenn sich Korpusinhalte, Embeddings, Chunking oder Retrieval-Richtlinie ändern. Validiere sie parallel zur aktiven Generation; schalte den Reader atomar um; bewahre die vorherige Generation so lange auf, bis du Fehler untersuchen und zurückrollen kannst. Ein partielles Reindexieren an Ort und Stelle ist schwer zu evaluieren und kaum nachvollziehbar zu erklären.

## Stolperfallen {#gotchas}

- **Problem: Abgerufener Text wird automatisch als vertrauenswürdig behandelt.** Eine Quelle kann veraltet, manipuliert oder außerhalb des Zugriffsbereichs der anfragenden Person sein. **Lösung:** Autoritäts-, Revisions- und Zugriffsmetadaten beibehalten und vor dem Prompting deterministisch filtern.
- **Problem: Nur die finalen Antworten werden getestet.** Retrieval-Fehler bleiben unsichtbar, sobald der Text flüssig ist. **Lösung:** Einen Retrieval-Beleg speichern und unabhängig von der Antwortqualität bewerten.
- **Problem: Fehlende Evidenz wird verborgen.** Das Modell kann die Lücke mit plausiblem Text füllen. **Lösung:** Einen Zustand `EVIDENCE_INSUFFICIENT` ausgeben und an Suche, Rückfrage oder einen Menschen weiterleiten.
- **Problem: Reindexierung an Ort und Stelle.** Nutzer können gemischte alte und neue Evidenz erhalten. **Lösung:** Unveränderliche Index-Generationen veröffentlichen und den Reader-Alias atomar umschalten.

## Siehe auch {#see-also}

- [[embeddings]]
- [[chunking-strategies]]
- [[vector-databases]]
- [[production-patterns]]

## Quellen {#sources}

- [Original RAG paper](https://arxiv.org/abs/2005.11401)
- [LangChain retrieval overview](https://docs.langchain.com/oss/python/langchain/retrieval)
- [OpenAI retrieval guide](https://developers.openai.com/api/docs/guides/retrieval)
