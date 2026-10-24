---
title: "Wissensdatenbank als Gedächtnis"
category: patterns
tags: [llm-memory, knowledge-base, wiki, markdown, ingest, lint, persistent-knowledge]
level: 3
source_sha256: bfcc86470238e81454d7793cf51556b323dfdbe10318dffac57bbf6dcb5145e8
translation: machine
translated_at: '2026-10-24'
---
# Wissensdatenbank als Gedächtnis {#knowledge-base-as-memory}

Eine strukturierte Markdown-Wissensdatenbank als Langzeitgedächtnis des Agenten nutzen. Der Agent liest, schreibt und pflegt eine Sammlung von Artikeln, die sich mit der Zeit anreichern. Wissen wird einmal geschrieben und gepflegt, statt bei jeder Anfrage neu hergeleitet zu werden.

## Wichtige Fakten {#key-facts}

- Einfache Markdown-Sammlungen mit Querverweisen funktionieren bis etwa 100 Artikel bzw. etwa 400.000 Wörter ohne Vektorsuche
- Das LLM navigiert über Zusammenfassungen und Indexdateien. Bei moderatem Wissensumfang braucht es keine Embeddings
- Ein eingespeister Quellablauf aktualisiert bzw. erstellt etwa 10–15 Wiki-Seiten
- Wissensdatenbanken sind „persistente, sich anreichernde Artefakte“. Anders als bei RAG werden Antworten nicht bei jedem Mal aus den Rohquellen neu hergeleitet
- LLMs erledigen Pflegearbeiten gut: Sie werden nicht lustlos, vergessen keine Querverweise und können in einem Durchgang 15 Dateien bearbeiten
- Ab etwa 500 Artikeln optional BM25- oder Vektorsuche mit LLM-Reranking ergänzen

## Architektur: Raw -> Wiki -> Schema {#architecture-raw-wiki-schema}

Drei Schichten, jede mit klarer Aufgabe:

### raw/ - Unveränderliche Quellen {#raw-immutable-sources}

```text
raw/
  paper-attention-is-all-you-need.md
  meeting-notes-2026-03-15.md
  api-docs-stripe-v3.md
```

- PDFs in Markdown konvertiert, gespeicherte Webartikel, Datensätze, Besprechungsnotizen
- Das LLM liest diese Dateien, verändert sie aber NIEMALS
- Maßgebliche Quelle für Verifikation und Deduplizierung

### wiki/ - Vom LLM erzeugtes Wissen {#wiki-llm-generated-knowledge}

```text
wiki/
  index.md              # catalog with summaries - agent reads first
  log.md                # append-only chronological operation log
  transformer-architecture.md
  stripe-integration.md
  attention-mechanisms.md
```

- Enzyklopädisch gehaltene Artikel zu Konzepten und Entitäten
- Zusammenfassungen, Vergleiche, Querverweise über `[[wiki-links]]`
- `index.md` - Einstiegspunkt des Agenten, wird bei jedem Ingest aktualisiert
- `log.md` - nur anhängbares Protokoll aller Operationen (dient als Audit-Trail)

### schema - Konfiguration {#schema-configuration}

Die Betriebsanweisungen des Agenten: Struktur der Wissensdatenbank, Namenskonventionen, Workflows, Qualitätsstandards. Entspricht einer CLAUDE.md oder dem Contributing-Leitfaden eines Projekts.

## Drei Operationen {#three-operations}

### 1. Ingest {#1-ingest}

Eine neue Quelle trifft ein. Der Agent:

```bash
1. Read source from raw/
2. Discuss key takeaways (optionally with user)
3. Create/update wiki pages for new concepts and entities
4. Update index.md with new entries and summaries
5. Revisit related pages - add cross-references
6. Append to log.md: what changed and why
```

**Qualitätssignal:** Ein gutes Ingest berührt 10–15 Seiten. Erstellt es nur eine Seite, verweist der Agent zu wenig quer.

### 2. Query {#2-query}

Der Nutzer stellt eine Frage. Der Agent:

```sql
1. Read index.md to locate relevant articles
2. Read specific wiki pages
3. Synthesize answer with citations to wiki pages
4. If the answer is valuable, create a new wiki page from it
```

In diesem Umfang ist keine Vektorsuche nötig. Der Index ist der Abrufmechanismus.

### 3. Lint / Health-Check {#3-lint-health-check}

Periodischer Wartungsdurchlauf:

```python
# Automated checks (scriptable, deterministic)
checks = [
    "orphan_pages",        # pages not referenced from index or other pages
    "dead_links",          # [[wiki-links]] pointing to non-existent pages
    "missing_cross_refs",  # related pages that don't reference each other
    "stale_claims",        # facts with valid_to in the past
    "empty_sections",      # placeholder sections never filled
    "duplicate_topics",    # multiple pages covering the same concept
]

# LLM-assisted checks (need judgment)
llm_checks = [
    "contradictions",      # page A says X, page B says not-X
    "outdated_info",       # claims that may have changed
    "missing_context",     # pages that assume knowledge not in the KB
]
```

**Lint regelmäßig ausführen:** wöchentlich für aktive Wissensdatenbanken, monatlich für stabile. Ohne Pflege sammeln sich Widersprüche und veraltete Informationen an.

## Muster {#patterns}

### Indexgesteuerte Navigation {#index-driven-navigation}

```markdown
# Knowledge Base Index

## Architecture (12 articles)
- microservices-patterns - saga, CQRS, event sourcing
- api-design - REST vs GraphQL, versioning, pagination

## Infrastructure (8 articles)
- kubernetes-ops - deployment strategies, HPA, resource limits
- observability - metrics, tracing, alerting stack

Last updated: 2026-04-08 | Total: 87 articles
```

Der Agent liest diese Datei zuerst. Etwa 500 Token genügen für 100 Artikel mit einzeiligen Zusammenfassungen. Das ist der günstigste mögliche Abrufmechanismus.

### Nur anhängbares Operationsprotokoll {#append-only-operation-log}

```markdown
# Operations Log

## 2026-04-08 14:30
- **Ingested:** Stripe API v3 migration guide
- **Created:** wiki/stripe-v3-migration.md
- **Updated:** wiki/stripe-integration.md (added v3 breaking changes)
- **Updated:** wiki/payment-processing.md (cross-ref to v3 migration)
- **Updated:** index.md (new entry under Payments)

## 2026-04-07 09:15
- **Query:** "How does our auth flow handle token refresh?"
- **Created:** wiki/auth-token-refresh.md (valuable answer, persisted)
```

Das Protokoll dient als Audit-Trail und hilft dem Agenten, die Entwicklung der Wissensdatenbank nachzuvollziehen.

### Skalierung über Markdown hinaus {#scaling-beyond-markdown}

Wenn die Wissensdatenbank die reine Navigation übersteigt:

| Skalierung | Strategie |
|-------|----------|
| <100 Artikel | Nur Index-Navigation |
| 100-500 | Domänenspezifische Indizes + Stichwortsuche |
| 500-5000 | BM25-Suche mit LLM-Reranking ergänzen |
| 5000+ | Vollständige [[rag-pipeline]] mit [[vector-databases]] |

## Tooling {#tooling}

- **Obsidian** - Graphansicht zur Visualisierung von Verbindungen, Dataview-Plugin für Abfragen auf YAML-Frontmatter
- **MkDocs Material** - statische Site-Generierung aus Markdown, Suche integriert
- **Obsidian Web Clipper** - Webquellen direkt in raw/ speichern

## Stolperfallen {#gotchas}

- **Der Index ist der Engpass.** Wird index.md nicht gepflegt, findet der Agent nichts. Index-Aktualisierungen bei jedem Ingest als verpflichtend behandeln, nicht als optional. Nach Möglichkeit automatisieren
- **„Eine Seite pro Thema“ scheitert bei komplexen Themen.** Eine einzelne Seite zu „Kubernetes“ wächst unkontrolliert. Früh aufteilen: k8s-networking, k8s-storage, k8s-rbac. Zehn fokussierte Seiten sind besser als eine ausufernde
- **LLMs erstellen beim Ingest zu viele Seiten.** Ohne Vorgaben legt der Agent für jedes Substantiv, das er antrifft, eine neue Seite an. Eine Qualitätshürde setzen: Eine Seite muss mindestens 3 inhaltlich substanzielle Fakten enthalten, um zu existieren

## Siehe auch {#see-also}

- [[memory-architectures]]
- [[memory-retrieval-patterns]]
- [[session-persistence]]
- [[context-window-management]]
- [[rag-pipeline]]
