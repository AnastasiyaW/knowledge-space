---
title: "Temporales Gedächtnis"
category: patterns
tags: [llm-memory, temporal-validity, staleness, contradiction-resolution, time-decay, knowledge-graph]
level: 3
source_sha256: 0bd32ac2d68c282890ac27c145fc2b490e1b7812158af31d42217d96b6768d39
translation: machine
translated_at: '2026-10-24'
---
# Temporales Gedächtnis {#temporal-memory}

Verwaltung der Zeitdimension gespeicherten Wissens. Fakten ändern sich: Das bevorzugte Framework eines Nutzers im Jahr 2024 muss im Jahr 2026 nicht mehr seine Präferenz sein. Ohne zeitliches Bewusstsein liefern Speichersysteme veraltete Informationen mit voller Überzeugung.

## Wichtige Fakten {#key-facts}

- Jeder Fakt hat einen impliziten oder expliziten Gültigkeitszeitraum (valid_from / valid_to)
- Die meisten Speichersysteme ignorieren die Zeitlichkeit: Alle gespeicherten Fakten gelten als gleichermaßen aktuell
- Temporale Wissensgraphen speichern Entitäts-Beziehungs-Tripel mit Gültigkeitszeitstempeln in SQLite oder ähnlichen Systemen
- Die Erkennung veralteter Fakten erfordert entweder explizite Ablaufdaten oder heuristische, altersbasierte Bewertung
- Widersprüche zwischen Fakten aus verschiedenen Zeiträumen sollten zugunsten des neueren Fakts aufgelöst werden
- Die domänenspezifischen Verfallsraten variieren: Präferenzen beim Tech-Stack ändern sich jährlich, persönliche Eigenschaften selten

## Temporales Wissensmodell {#temporal-knowledge-model}

```python
@dataclass
class TemporalFact:
    subject: str          # "user"
    predicate: str        # "prefers_framework"
    object: str           # "FastAPI"
    valid_from: datetime  # when this became true
    valid_to: datetime | None  # null = still valid
    confidence: float     # 0.0-1.0
    source: str           # which conversation/document

# Storage: SQLite table
"""
CREATE TABLE facts (
    id INTEGER PRIMARY KEY,
    subject TEXT NOT NULL,
    predicate TEXT NOT NULL,
    object TEXT NOT NULL,
    valid_from TEXT NOT NULL,
    valid_to TEXT,
    confidence REAL DEFAULT 1.0,
    source TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_facts_subject ON facts(subject, predicate);
CREATE INDEX idx_facts_valid ON facts(valid_from, valid_to);
"""
```

## Erkennung veralteter Fakten {#staleness-detection}

### Explizites Ablaufdatum {#explicit-expiry}

Setzen Sie `valid_to`, wenn bekannt ist, dass der Fakt abläuft:

```python
def store_fact(subject, predicate, obj, valid_from, valid_to=None):
    # If a conflicting fact exists, close it
    existing = db.query(
        "SELECT id FROM facts WHERE subject=? AND predicate=? AND valid_to IS NULL",
        (subject, predicate)
    )
    if existing:
        db.execute(
            "UPDATE facts SET valid_to=? WHERE id=?",
            (valid_from, existing[0]["id"])
        )

    db.execute(
        "INSERT INTO facts (subject, predicate, object, valid_from, valid_to) VALUES (?,?,?,?,?)",
        (subject, predicate, obj, valid_from, valid_to)
    )
```

### Heuristischer, altersbasierter Verfall {#heuristic-age-based-decay}

Wenn kein explizites Ablaufdatum verfügbar ist, bewerten Sie nach Alter und Domäne:

```python
DECAY_RATES = {
    "tech_preference": 365,    # days until 50% confidence
    "project_status": 30,      # projects change monthly
    "personal_trait": 3650,    # personality rarely changes
    "api_version": 180,        # APIs update ~twice/year
    "team_member": 730,        # team composition changes over years
    "server_config": 90,       # infra changes quarterly
}

def confidence_at(fact: TemporalFact, now: datetime) -> float:
    age_days = (now - fact.valid_from).days
    half_life = DECAY_RATES.get(fact.predicate, 365)
    return fact.confidence * (0.5 ** (age_days / half_life))
```

### Signale für Veraltung {#staleness-signals}

Erkennen Sie, wann der Speicher aufgefrischt werden muss:

| Signal | Erkennung | Aktion |
|--------|-----------|--------|
| Alter überschreitet die Halbwertszeit | `confidence_at() < 0.5` | Zur Verifikation markieren |
| Direkter Widerspruch | Neuer Fakt steht im Konflikt mit gespeichertem | Alten Fakt schließen, neuen speichern |
| Kontextabweichung | Fakt verweist auf gelöschte Datei/Projekt | Als möglicherweise veraltet markieren |
| Nutzerkorrektur | Nutzer korrigiert einen Fakt explizit | Sofort aktualisieren |
| Externe Änderung | Versionsveröffentlichung, Teamwechsel | Verwandte Fakten prüfen |

## Auflösung von Widersprüchen {#contradiction-resolution}

Wenn zwei Fakten einander widersprechen, hängt die Auflösung vom Kontext ab:

```python
def resolve_contradiction(fact_a: TemporalFact, fact_b: TemporalFact) -> TemporalFact:
    # Rule 1: Newer wins for same subject+predicate
    if fact_a.subject == fact_b.subject and fact_a.predicate == fact_b.predicate:
        return fact_b if fact_b.valid_from > fact_a.valid_from else fact_a

    # Rule 2: Higher confidence wins for same time period
    if overlaps(fact_a, fact_b):
        return fact_a if fact_a.confidence > fact_b.confidence else fact_b

    # Rule 3: More specific wins (user preference > general default)
    if is_more_specific(fact_a, fact_b):
        return fact_a

    # Rule 4: Flag for human resolution
    return flag_for_review(fact_a, fact_b)
```

**Auflösungshierarchie:**
1. Die explizite Korrektur des Nutzers gewinnt immer
2. Neuere Beobachtung > ältere Beobachtung
3. Spezifisch > allgemein ("Nutzer sagte X" > "Die meisten Nutzer bevorzugen Y")
4. Bei weiterhin unklarer Lage den Nutzer fragen

## Muster {#patterns}

### Zeitliche Abfrage {#temporal-query}

```python
def query_current(subject: str, predicate: str, now: datetime = None) -> list:
    """Get currently valid facts."""
    now = now or datetime.utcnow()
    return db.query("""
        SELECT * FROM facts
        WHERE subject = ? AND predicate = ?
          AND valid_from <= ?
          AND (valid_to IS NULL OR valid_to > ?)
        ORDER BY valid_from DESC
    """, (subject, predicate, now, now))

def query_history(subject: str, predicate: str) -> list:
    """Get full history of a fact, including expired values."""
    return db.query("""
        SELECT * FROM facts
        WHERE subject = ? AND predicate = ?
        ORDER BY valid_from ASC
    """, (subject, predicate))
```

### Zeitliche Metadaten im Vektorspeicher {#temporal-metadata-in-vector-store}

Wenn ein [[vector-databases]]-Ansatz verwendet wird, kodieren Sie zeitliche Daten als Metadaten für die Filterung:

```python
vector_store.add(
    documents=[conversation_text],
    metadatas=[{
        "valid_from": "2026-04-08",
        "valid_to": None,
        "domain": "tech_preference",
        "confidence": 0.95
    }]
)

# Query with temporal filter
results = vector_store.query(
    query_texts=["database preference"],
    where={"valid_to": None},  # only current facts
    n_results=5
)
```

### Periodische Gültigkeitsprüfung {#periodic-validity-scan}

```python
def scan_stale_facts(threshold: float = 0.5):
    """Find facts that may be outdated."""
    now = datetime.utcnow()
    all_facts = db.query("SELECT * FROM facts WHERE valid_to IS NULL")
    stale = []
    for fact in all_facts:
        conf = confidence_at(fact, now)
        if conf < threshold:
            stale.append({"fact": fact, "confidence": conf})
    return sorted(stale, key=lambda x: x["confidence"])
```

## Fallstricke {#gotchas}

- **Die meisten Speichersysteme behandeln alle Fakten als zeitlos.** Eine Präferenz von vor zwei Jahren hat dasselbe Gewicht wie eine von gestern. Ohne zeitlichen Verfall oder Gültigkeitsverfolgung verwendet der Agent veraltete Informationen mit voller Überzeugung. Speichern Sie daher immer Zeitstempel zusammen mit den Fakten
- **Das Schließen alter Fakten bei Widersprüchen erfordert sorgfältiges Schlüssel-Matching.** "Nutzer bevorzugt Python" und "Nutzer mag Python für Skripting" sind verschiedene Fakten mit unterschiedlichen Prädikaten. Naive Deduplizierung übersieht Widersprüche (zu streng) oder schließt gültige Fakten fälschlicherweise (zu lose). Verwenden Sie Subjekt+Prädikat als Konfliktschlüssel statt eines Volltextvergleichs
- **Zeitzonen sind für Gültigkeitszeiträume wichtig.** Wenn valid_from in UTC gespeichert, aber mit der lokalen Zeit verglichen wird, können Fakten fälschlicherweise als gültig oder abgelaufen erscheinen. Verwenden Sie durchgängig UTC

## Siehe auch {#see-also}

- [[memory-architectures]]
- [[forgetting-strategies]]
- [[knowledge-base-as-memory]]
- [[session-persistence]]
- [[verbatim-vs-extraction]]
