---
title: "Vergessensstrategien"
category: patterns
tags: [llm-memory, forgetting, compaction, archival, ttl, memory-management, pruning]
level: 3
source_sha256: a8b654f22aacbabbd6e6e11d8138edf4cd5ebb316c005fa1acdeee6df801a0c3
translation: machine
translated_at: '2026-10-24'
---
# Vergessensstrategien {#forgetting-strategies}

Wann und wie Informationen aus dem Speicher eines LLM-Agenten entfernt werden sollten. Ungebremstes Wachstum des Speichers verschlechtert die Abrufqualität – irrelevante Treffer verwässern relevante. Strategisches Vergessen ist genauso wichtig wie strategisches Erinnern.

## Kernfakten {#key-facts}

- Speicher ohne Bereinigung verschlechtert die Abrufpräzision mit der Zeit – mehr Einträge bedeuten mehr falsch positive Treffer
- „Vergessen“ bedeutet meist Archivierung (Verschieben in kalten Speicher), nicht Löschung
- Die Token-Kosten skalieren mit der Größe des Speichers – selbst wenn der Abruf schnell ist, ist es teuer, zu viel Kontext einzufügen
- Compaction (Zusammenfassung) ist eine Form des verlustbehafteten Vergessens – Details gehen dauerhaft verloren
- Die optimale Speichergröße hängt von der Abrufmethode ab: Die Indexnavigation verschlechtert sich ab etwa 500 Einträgen, die Vektorsuche verschlechtert sich allmählicher
- Daten niemals löschen, bevor sie archiviert wurden

## Vergessensmechanismen {#forgetting-mechanisms}

| Mechanismus | Was er tut | Reversibel | Am besten geeignet für |
|-------------|------------|------------|------------------------|
| **TTL (Time-to-Live)** | Läuft nach einem festen Zeitraum automatisch ab | Nein (sofern nicht archiviert) | Temporären Zustand, Sitzungsdaten |
| **Relevanzbewertung** | Einträge bewerten, die niedrigsten entfernen | Ja (sofern archiviert) | Großer Speicher mit gemischter Qualität |
| **Compaction** | Zusammenfassen, Details ersetzen | Nein | Gesprächsverlauf |
| **Archivierung** | In kalten Speicher verschieben | Ja | Alte, aber potenziell nützliche Daten |
| **Deduplizierung** | Redundante Einträge zusammenführen | Teilweise | Überlappende Informationen |
| **Explizite Löschung** | Auf Wunsch des Nutzers entfernen | Nein | Datenschutz, Korrekturen |

## TTL-basiertes Ablaufen {#ttl-based-expiry}

Weisen Sie eine Time-to-Live abhängig von der Art der Information zu:

```python
TTL_CONFIG = {
    "session_state": timedelta(hours=24),       # task-specific, short-lived
    "project_status": timedelta(days=30),        # changes monthly
    "tool_output": timedelta(days=7),            # raw outputs are transient
    "decision": timedelta(days=365),             # decisions have long relevance
    "preference": timedelta(days=730),           # preferences are stable
    "identity": None,                            # never expires
}

def should_expire(entry: MemoryEntry, now: datetime) -> bool:
    ttl = TTL_CONFIG.get(entry.type)
    if ttl is None:
        return False
    return (now - entry.created_at) > ttl
```

**Nicht beim Ablauf löschen – archivieren.** Verschieben Sie abgelaufene Einträge in einen separaten Speicher. Werden sie später benötigt, können sie aus dem Archiv abgerufen werden.

## Relevanzbewertung {#relevance-scoring}

Bewerten Sie jeden Speichereintrag nach seinem Nutzen. Faktoren:

```python
def relevance_score(entry: MemoryEntry, now: datetime) -> float:
    # Recency: newer is more relevant
    age_days = (now - entry.created_at).days
    recency = 1.0 / (1 + age_days / 30)  # 30-day half-life

    # Access frequency: more-retrieved is more relevant
    access_freq = min(entry.access_count / 10, 1.0)

    # Freshness: recently accessed is more relevant
    last_access_days = (now - entry.last_accessed).days
    freshness = 1.0 / (1 + last_access_days / 7)

    # Type weight: some types are inherently more valuable
    type_weights = {
        "decision": 1.0,
        "gotcha": 0.9,
        "preference": 0.8,
        "finding": 0.7,
        "observation": 0.5,
        "tool_output": 0.3,
    }
    type_weight = type_weights.get(entry.type, 0.5)

    return (0.3 * recency + 0.3 * access_freq + 0.2 * freshness + 0.2 * type_weight)
```

Bereinigen Sie Einträge unterhalb eines Schwellenwerts. Empfohlen: Einträge mit einer Bewertung < 0,2 archivieren.

## Compaction {#compaction}

Verlustbehaftete Zusammenfassung detaillierter Historie in eine komprimierte Form. Siehe [[context-window-management]] für Besonderheiten der Gesprächs-Compaction.

```python
def compact_memory_topic(topic: str, entries: list[MemoryEntry]) -> MemoryEntry:
    """Replace multiple entries with one summary."""
    full_text = "\n".join(e.text for e in entries)

    summary = llm.complete(f"""Summarize these {len(entries)} memory entries about '{topic}'.
Preserve: key decisions, current state, gotchas, preferences.
Discard: intermediate steps, superseded information, raw outputs.

{full_text}""")

    return MemoryEntry(
        text=summary,
        type="compacted_summary",
        created_at=max(e.created_at for e in entries),
        metadata={"compacted_from": len(entries), "topic": topic}
    )
```

**Warnung:** Compaction ist nicht umkehrbar. Archivieren Sie die ursprünglichen Einträge, bevor Sie compacten.

## Archivierung {#archival}

Verschieben Sie alte Einträge aus dem aktiven Speicher in den kalten Speicher:

```python
def archive_old_entries(active_store, archive_store, max_age_days: int = 90):
    now = datetime.utcnow()
    to_archive = []

    for entry in active_store.all():
        if should_archive(entry, now, max_age_days):
            to_archive.append(entry)

    for entry in to_archive:
        archive_store.add(entry)
        active_store.remove(entry.id)

    return len(to_archive)

def should_archive(entry: MemoryEntry, now: datetime, max_age: int) -> bool:
    # Don't archive: identity, active decisions, high-relevance entries
    if entry.type in ("identity", "active_decision"):
        return False
    if relevance_score(entry, now) > 0.5:
        return False
    return (now - entry.last_accessed).days > max_age
```

Der aktive Speicher bleibt schnell und fokussiert. Das Archiv ist durchsuchbar, hat aber höhere Latenzzeiten.

## Deduplizierung {#deduplication}

Mehrere Gespräche erzeugen häufig überlappende Erinnerungen:

```python
def deduplicate(entries: list[MemoryEntry], similarity_threshold: float = 0.92):
    """Merge near-duplicate entries, keeping the most recent."""
    unique = []
    for entry in sorted(entries, key=lambda e: e.created_at, reverse=True):
        is_dup = False
        for existing in unique:
            sim = cosine_similarity(
                embed(entry.text), embed(existing.text)
            )
            if sim > similarity_threshold:
                # Keep existing (more recent), update metadata
                existing.metadata["also_from"] = entry.id
                is_dup = True
                break
        if not is_dup:
            unique.append(entry)
    return unique
```

## Zielgrößen für den Speicher {#memory-size-targets}

| Speichertyp | Zielgröße | Auslöser für Bereinigung |
|-------------|-----------|--------------------------|
| Identität (L0) | <50 Token | Niemals bereinigen |
| Kritische Fakten (L1) | <200 Token | Nur manuelle Prüfung |
| Aktiver Projektspeicher | <5K Token | Wenn das Projekt abgeschlossen ist |
| Historischer Speicher | <50K Token | Monatliche Archivierung |
| Archiv | Unbegrenzt | Jährliche Prüfung |

## Muster {#patterns}

### Gestaffelte Aufbewahrung {#graduated-retention}

```text
0-7 days:   Keep everything (verbatim)
7-30 days:  Keep decisions, gotchas, preferences. Archive raw outputs
30-90 days: Compact findings into summaries. Archive details
90+ days:   Archive to cold storage. Keep only identity + decisions
```

### Zugriffsgesteuerte Erhaltung {#access-triggered-preservation}

```python
def on_memory_access(entry_id: str):
    """Every time an entry is retrieved, extend its life."""
    entry = store.get(entry_id)
    entry.last_accessed = datetime.utcnow()
    entry.access_count += 1
    store.update(entry)
    # Frequently accessed entries never get archived
```

## Stolperfallen {#gotchas}

- **Vergessen ohne Archivierung ist Datenvernichtung.** Archivieren Sie immer, bevor Sie bereinigen. Die Kosten für die Speicherung alter Daten im kalten Speicher sind vernachlässigbar im Vergleich zu den Kosten, wenn sich später herausstellt, dass Informationen gebraucht werden
- **Compaction häuft Informationsverlust an.** Wenn Sie eine bereits compactete Zusammenfassung erneut compacten, verschlechtert sich die Qualität exponentiell. Verfolgen Sie die Compaction-Tiefe und compacten Sie niemals öfter als zweimal. Ist der Speicher nach zwei Compactions immer noch zu groß, archivieren Sie stattdessen
- **Der Schwellenwert für die Deduplizierung ist schwer abzustimmen.** Zu aggressiv (>0,85 Ähnlichkeit = Duplikat) führt zum Zusammenführen tatsächlich verschiedener Einträge. Zu konservativ (<0,95) lässt Redundanz bestehen. Beginnen Sie bei 0,92 und passen Sie den Wert anhand der Rate falsch positiver Treffer an. Protokollieren Sie stets, was zusammengeführt wurde, damit es überprüft werden kann

## Siehe auch {#see-also}

- [[context-window-management]]
- [[temporal-memory]]
- [[memory-architectures]]
- [[verbatim-vs-extraction]]
- [[session-persistence]]
