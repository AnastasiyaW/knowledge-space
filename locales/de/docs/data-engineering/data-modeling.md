---
title: "Datenmodellierung und Normalisierung"
category: concepts
tags: [data-engineering, data-modeling, normalization, er-diagrams, database-design]
level: 3
source_sha256: 55bdbef0054455a51335da394b93e9fc7fe2cfec73ee5d7a9c2fbf0980e89ec5
translation: machine
translated_at: '2026-10-24'
---
# Datenmodellierung und Normalisierung {#data-modeling-and-normalization}

Datenmodellierung ist der Prozess, Anforderungen zu analysieren und Datenstrukturen zu entwerfen. Sie umfasst drei Stufen: konzeptionell (Geschäftsentitäten), logisch (ER-Diagramme mit Attributen und Schlüsseln) und physisch (DDL-Skripte mit Indizes und Partitionen). Normalisierung eliminiert Redundanz anhand funktionaler Abhängigkeiten.

## Normalformen {#normal-forms}

**Merkhilfe:** „Daten hängen vom Schlüssel ab [1NF], vom ganzen Schlüssel [2NF] und von nichts außer dem Schlüssel [3NF].“

### Erste Normalform (1NF) {#first-normal-form-1nf}
- Alle Werte sind **atomar** (keine Arrays, keine zusammengesetzten Werte)
- Keine doppelten Zeilen
- Besitzt einen Primärschlüssel

### Zweite Normalform (2NF) {#second-normal-form-2nf}
- Erfüllt 1NF
- Jedes Nicht-Schlüssel-Attribut hängt vom **gesamten** Primärschlüssel ab
- Nur relevant bei zusammengesetzten Schlüsseln. Ist der PK einfach, ist 2NF automatisch erfüllt

### Dritte Normalform (3NF) {#third-normal-form-3nf}
- Erfüllt 2NF
- Keine **transitiven Abhängigkeiten**: Nicht-Schlüssel-Attribut A hängt von Nicht-Schlüssel-Attribut B ab, und B hängt vom PK ab
- **Lösung:** Die transitiv abhängige Gruppe in eine eigene Tabelle auslagern

### Jenseits der 3NF {#beyond-3nf}
- **BCNF, 4NF, 5NF** – in der Praxis selten benötigt
- **6NF** – extreme Zerlegung, ein Attribut pro Tabelle. Wird in der [[data-vault#anchor-modeling|Ankermodellierung]] verwendet

## Funktionale Abhängigkeiten {#functional-dependencies}

`{X} -> {Y}` bedeutet: Stimmen zwei Tupel in X überein, müssen sie auch in Y übereinstimmen. Jeder X-Wert bestimmt genau einen Y-Wert.

### Anomalien (wenn Normalisierung nicht ausreicht) {#anomalies-when-normalization-is-insufficient}

| Anomalie | Problem |
|----------|---------|
| **Aktualisierung** | Das Ändern einer Information erfordert das Aktualisieren ALLER Zeilen, die diese Entität enthalten |
| **Löschung** | Das Löschen der letzten zugehörigen Zeile führt zum vollständigen Verlust der Entitätsdaten |
| **Einfügung** | Eine Entität ohne zugehörige Datensätze kann nicht eingefügt werden |

## Schlüssel {#keys}

| Schlüsseltyp | Definition |
|--------------|-----------|
| **Kandidatenschlüssel** | Eindeutige, nicht weiter reduzierbare Attributmenge |
| **Primärschlüssel** | Ausgewählter Kandidatenschlüssel |
| **Alternativschlüssel** | Nicht gewählte Kandidatenschlüssel |
| **Surrogatschlüssel** | Systemgenerierte ID (Auto-Increment, UUID) |
| **Natürlicher Schlüssel** | Geschäftsattribut (E-Mail, Sozialversicherungsnummer) |
| **Zusammengesetzter Schlüssel** | Mehrere Attribute, die gemeinsam einen Kandidatenschlüssel bilden |

**Surrogatschlüssel bevorzugen**, wenn mehrere Kandidaten existieren oder sich der natürliche Schlüssel ändern kann.

## ER-Diagramme {#er-diagrams}

### Kardinalitätstypen {#cardinality-types}

| Typ | Umsetzung |
|-----|-----------|
| **1:1** | FK mit UNIQUE-Constraint |
| **1:M** | FK in der „Viele“-Tabelle |
| **M:M** | Verbindungstabelle mit FKs auf beide Seiten |

### Notationen {#notations}

**Martin (Krähenfuß / Crow's Foot)** – am praktischsten, in Interviews erwartet:
- Rechtecke = Entitäten mit darin aufgelisteten Attributen
- Krähenfuß (Gabelung) = „viele“, einzelne Linie = „eins“
- Kreis = „null“ (optional), Strich = „eins“ (verpflichtend)

**Chen-Notation** – akademisch: Rechtecke (Entitäten), Rauten (Beziehungen), Ovale (Attribute)

## Normalisierung vs. Denormalisierung {#normalization-vs-denormalization}

| Kriterium | Normalisiert (3NF) | Denormalisiert |
|-----------|--------------------|----------------|
| Datenintegrität | Besser (keine Anomalien) | Schlechter |
| INSERT/UPDATE/DELETE | Schneller (kleinere Tabellen) | Langsamer |
| SELECT (Lesezugriffe) | Langsamer (viele JOINs) | Schneller (breite Tabellen) |
| Geeignet für | OLTP (Schreibintegrität) | OLAP (Lesegeschwindigkeit, Data Marts) |

## Deduplizierungsmuster {#deduplication-patterns}

```sql
-- Method 1: CTE + ROW_NUMBER (most common)
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY key_col1, key_col2
        ORDER BY load_date DESC
    ) AS rn
    FROM source_table
)
SELECT * FROM ranked WHERE rn = 1;

-- Method 2: QUALIFY (Snowflake, BigQuery, DuckDB)
SELECT * FROM source_table
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY key_col1, key_col2
    ORDER BY load_date DESC
) = 1;

-- Method 3: DISTINCT ON (PostgreSQL only)
SELECT DISTINCT ON (key_col1, key_col2) *
FROM source_table
ORDER BY key_col1, key_col2, load_date DESC;
```

## Fallstricke {#gotchas}
- Relationen (mathematisch) enthalten keine doppelten Tupel und keine Ordnung. Tabellen (physisch) können beides verletzen
- Eine Relation ist per Definition (Mengenlehre) automatisch in 1NF. Bei Tabellen muss dies explizit geprüft werden
- Im DWH werden Constraints (PK, FK) oft deaktiviert, um Bulk-Loads zu beschleunigen
- Die meisten produktiven DWHs sind Hybride: Data Vault oder 3NF im Kern, dimensional in den Data Marts

## Siehe auch {#see-also}
- [[dimensional-modeling]] – Stern- und Schneeflockenschemata
- [[data-vault]] – Hub/Link/Satellite-Methodik
- [[dwh-architecture]] – wo Modelle angewendet werden
- [[sql-for-de]] – SQL-Umsetzung von Modellen
