---
title: "Speicherarchitekturen für LLM-Agenten"
category: concepts
tags: [llm-memory, memory-systems, hierarchical-memory, graph-memory, vector-stores]
level: 3
source_sha256: 2b3ee9ed507294c95d3653734a7c147def42563d63906b96899d998926a0f82d
translation: machine
translated_at: '2026-10-24'
---
# Speicherarchitekturen für LLM-Agenten {#memory-architectures-for-llm-agents}

Strukturelle Ansätze zur Organisation von persistentem Wissen für LLM-Agenten. Die Architektur bestimmt die Abrufqualität, die Speicherkosten und die Fähigkeit des Agenten, über gespeicherte Informationen hinweg zu schlussfolgern.

## Wichtige Fakten {#key-facts}

- LLMs sind zustandslos – das gesamte Gedächtnis ist externe Infrastruktur, aus der der Agent liest und in die er schreibt
- Die Speicherarchitektur bestimmt unmittelbar, was der Agent abrufen kann und wie genau
- Einfache Flat-Files übertreffen komplexe Systeme bis zu ~100 Artikeln / ~400K Wörtern
- Darüber hinaus wird strukturierter Abruf (indexbasiert oder vektorbasiert) notwendig
- Rohe, wörtliche Speicherung mit Standard-Embeddings erreicht 96,6 % R@5 auf Long-Memory-Benchmarks – und schlägt damit extraktionsbasierte Systeme (~85 %)
- Ein leichtgewichtiges LLM-Reranking hebt den Abruf auf ~100 % bei vernachlässigbaren Kosten (~0,001 $/Anfrage)

## Vergleich der Architekturen {#architecture-comparison}

| Architektur | Umfang | Kosten | Abruf | Wartung |
|-------------|--------|--------|-------|---------|
| **Flat Files** (Markdown) | <100 Artikel | Minimal | LLM navigiert über den Index | Manuell oder LLM-gestützt |
| **Hierarchischer Graph** | 100–10K Einträge | Gering bis mittel | Metadatengestützte Traversierung | Automatisch nach Taxonomie organisiert |
| **Vektorspeicher** (wörtlich) | 1K–1M Einträge | Mittel | Embedding-Ähnlichkeit | Automatisch indiziert beim Einlesen |
| **Wissensgraph** (Tripel) | Beliebig | Hoch | Strukturierte Abfragen + Traversierung | Komplex, erfordert Entity Resolution |
| **Hybrid** | Beliebig | Variabel | Mehrere Abrufpfade | Am komplexesten, beste Ergebnisse |

## Flat-File-Architektur {#flat-file-architecture}

Einfache Markdown-Dateien mit Querverweisen und einem gepflegten Index. Das LLM navigiert, indem es zunächst den Index liest und anschließend gezielt in einzelne Dateien eintaucht.

```bash
knowledge/
  index.md          # catalog with summaries (LLM reads first)
  log.md            # append-only operation log
  raw/              # immutable source materials
  wiki/             # LLM-generated structured articles
    concept-a.md
    entity-b.md
```

**Drei Operationen:**
1. **Ingest** – Eine neue Quelle trifft ein, das LLM liest sie, erstellt bzw. aktualisiert ~10–15 Wiki-Seiten und aktualisiert den Index
2. **Query** – Das LLM liest den Index, navigiert zu den relevanten Seiten und formuliert daraus eine Antwort mit Quellenangaben
3. **Lint** – Periodische Zustandsprüfung: Widersprüche, veraltete Aussagen, verwaiste Seiten und fehlende Querverweise aufspüren

**Wann es funktioniert:** Das LLM ist die Abrufinstanz. Mit guten Zusammenfassungen im Index navigiert es ~100 Artikel ohne Vektorsuche. Wissen akkumuliert sich – einmal geschrieben, schrittweise gepflegt, nicht bei jeder Anfrage neu hergeleitet.

**Wann es bricht:** Jenseits von ~500 Artikeln wird der Index zu groß für das Kontextfenster. Dann muss in Domänen-Indizes aufgeteilt oder eine Suche ergänzt werden.

## Hierarchische Graph-Architektur {#hierarchical-graph-architecture}

Organisiert den Speicher in eine navigierbare Taxonomie mit räumlichen Metaphern:

```text
Wing (person/project)
  └── Room (topic)
       └── Hall (type: facts/events/discoveries/preferences/advice)
            └── Closet (summary)
                 └── Drawer (verbatim text)
```

- **Querverbindungen** („Tunnel“) verknüpfen Räume über verschiedene Flügel hinweg
- Metadaten in [[vector-databases]] kodieren die Hierarchie – keine separate Graph-DB nötig
- [[embeddings]] auf wörtlichem Text in den Schubladen (Drawers) übernehmen die Ähnlichkeitssuche
- Ein zeitlicher Wissensgraph in SQLite speichert Entitäts-Beziehungs-Tripel mit Gültigkeitszeiträumen

**Zentraler Vorteil:** Die Navigation ist strukturiert. Der Agent durchsucht nicht den gesamten Speicher – er grenzt zunächst nach Flügel, dann nach Raum, dann nach Halle ein. Das reduziert Fehltreffer und macht den Abruf nachvollziehbar.

## Vektorspeicher-Architektur {#vector-store-architecture}

Textabschnitte mit [[embeddings]] speichern und über semantische Ähnlichkeit abrufen.

```python
# Simplest viable memory
import chromadb

client = chromadb.Client()
collection = client.create_collection("memory")

# Store verbatim
collection.add(
    documents=["User prefers Postgres because of jsonb support and pgvector"],
    ids=["mem_001"],
    metadatas=[{"wing": "user", "room": "preferences", "valid_from": "2026-01-15"}]
)

# Retrieve
results = collection.query(query_texts=["database preference"], n_results=5)
```

**Entscheidender Befund:** Roher, wörtlicher Text mit Standard-Embeddings übertrifft von LLMs extrahierte Zusammenfassungen deutlich. Systeme, die Fakten wie „Nutzer bevorzugt Postgres“ extrahieren, verlieren das *Warum* – und genau das Warum macht den Abruf nützlich. Siehe [[verbatim-vs-extraction]].

## Wissensgraph-Architektur {#knowledge-graph-architecture}

Entitäts-Beziehungs-Tripel mit zeitlicher Gültigkeit:

```text
(User, prefers, PostgreSQL, valid_from=2026-01, valid_to=null)
(PostgreSQL, supports, pgvector, valid_from=2024-06, valid_to=null)
(User, evaluated, MySQL, valid_from=2025-11, valid_to=2025-12)
```

- Am besten geeignet für schlussfolgernde Abfragen über Beziehungen hinweg („Welche Werkzeuge bevorzugt der Nutzer, die Vektorsuche unterstützen?“)
- Aufwendig in der Pflege – Entity Resolution, Deduplizierung, Verfolgung der Gültigkeit
- Häufig mit einem Vektorspeicher kombiniert, um hybriden Abruf zu ermöglichen

## Hybrid-Architektur {#hybrid-architecture}

Produktivsysteme kombinieren mehrere Ansätze:

```text
L0: Identity core (flat file, ~50 tokens, always loaded)
L1: Critical facts (flat file, ~120 tokens, always loaded)
L2: Topic-specific memory (vector store, loaded on demand)
L3: Full history (vector store, loaded on explicit request)
```

Siehe [[context-window-management]] für das geschichtete Ladeverfahren.

## Muster {#patterns}

### Index-First-Navigation {#index-first-navigation}

```markdown
# Memory Index

## User Preferences
- database-choice - PostgreSQL, reasons, migration history
- editor-setup - Neovim config, plugins, keybindings

## Project: API Rewrite
- architecture-decisions - REST vs GraphQL, chosen GraphQL
- deployment - K8s on GCP, Terraform managed
```

Der Agent liest zuerst diesen Index und öffnet dann nur die Dateien, die er benötigt. Dies ist JIT-Kontextladen – minimale Token, bis spezifisches Wissen tatsächlich gebraucht wird.

### Ingest-Workflow {#ingest-workflow}

```bash
Source material arrives
  → LLM reads source (raw/ - immutable)
  → LLM creates/updates wiki pages
  → LLM updates index.md with new entries
  → LLM appends to log.md
  → LLM revisits related pages for cross-references
```

Eine Quelle berührt typischerweise 10–15 Wiki-Seiten. Das LLM erledigt die Verwaltungsarbeit zuverlässig – es langweilt sich nicht und vergisst nicht, Querverweise zu aktualisieren.

## Stolpersteine {#gotchas}

- **Flat Files stoßen bei etwa 400K Wörtern an eine Grenze.** Der Index selbst wird zu groß für das Kontextfenster. Lösung: in domänenspezifische Indizes aufteilen, optionale BM25-/Vektorsuche mit LLM-Reranking ergänzen
- **Graph-DBs bringen für die meisten Anwendungsfälle Komplexität ohne entsprechenden Nutzen.** Metadatenfelder in einem Vektorspeicher (Flügel, Raum, Typ, valid_from) liefern ~80 % der Graph-Navigation bei ~20 % des Aufwands. Eine dedizierte Graph-DB lohnt sich nur, wenn mehrstufige Beziehungsabfragen nötig sind
- **Speicher ohne Wartung verschlechtert sich.** Fakten veralten, Widersprüche häufen sich, verwaiste Seiten entstehen. Periodische Lint-/Health-Check-Durchläufe einplanen – Widersprüche finden, zeitliche Gültigkeit prüfen, tote Links entfernen

## Siehe auch {#see-also}

- [[verbatim-vs-extraction]]
- [[context-window-management]]
- [[knowledge-base-as-memory]]
- [[memory-retrieval-patterns]]
- [[agent-memory]]
- [[vector-databases]]
