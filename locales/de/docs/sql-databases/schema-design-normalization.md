---
title: "Schemadesign und Normalisierung"
category: concepts
tags: [sql-databases, schema-design, normalization, 1nf, 2nf, 3nf, denormalization, primary-key, foreign-key]
level: 4
source_sha256: 633a650d278ff3066116bb4c01ae224d344c1bd8afde61d6b288ea58a2df1195
translation: machine
translated_at: '2026-10-24'
---
# Schemadesign und Normalisierung {#schema-design-and-normalization}

Gutes Schemadesign balanciert Datenintegrität (Normalisierung) mit Lesleistung (Denormalisierung). Die Wahl beeinflusst jede Abfrage, jeden Join und jeden Index im System.

## Normalformen {#normal-forms}

**1NF (Erste Normalform):** Jede Spalte enthält atomare Werte (keine Arrays/Listen). Jede Zeile ist eindeutig (besitzt einen Primärschlüssel). Keine wiederholten Gruppen.

**2NF:** 1NF + jede Nicht-Schlüsselspalte hängt vom gesamten Primärschlüssel ab (nicht nur von einem Teil). Beseitigt partielle Abhängigkeiten bei zusammengesetzten Schlüsseln.

**3NF:** 2NF + keine transitiven Abhängigkeiten (eine Nicht-Schlüsselspalte hängt von einer anderen Nicht-Schlüsselspalte ab). Beispiel: Wenn city den country_code enthält, sollte nicht zusätzlich country_name gespeichert werden.

**Praktische Richtlinie:** Normalisieren, bis Abfragen zu komplex oder zu langsam werden, und dann gezielt denormalisieren. OLTP-Systeme profitieren von Normalisierung; OLAP/Reporting toleriert mehr Denormalisierung.

## Wichtige Fakten {#key-facts}

- Normalisierung reduziert Redundanz und erzwingt Integrität über Fremdschlüssel
- Denormalisierung tauscht Integrität gegen Lesleistung (vorberechnete Joins, materialisierte Sichten)
- Eins-zu-Eins: PK als FK oder eindeutiger FK
- Eins-zu-Viele: FK auf der „Viele“-Seite
- Viele-zu-Viele: erfordert eine Zwischentabelle mit zusammengesetztem PK
- Wähle die kleinsten ausreichenden Datentypen – das beeinflusst Indexgröße, Cache-Effizienz und I/O

## Strategien für Primärschlüssel {#primary-key-strategies}

| Strategie | Vorteile | Nachteile |
|----------|------|------|
| Auto-Increment (SERIAL) | Geordnet, kompakt, ideal für clustered Index | Gibt Anzahl preis, nicht für verteilte Systeme geeignet |
| UUID v4 | Global eindeutig, keine Koordination nötig | Zufällig = schlecht für Indizes (Page Splits) |
| UUID v7 / ULID | Zeitlich geordnet + eindeutig, geeignet für verteilte Systeme | Breiter als Integer (16 Bytes) |

## Muster {#patterns}

### Typisches Anwendungsschema (Telegram-Klon) {#typical-application-schema-telegram-clone}
```sql
-- Users with settings (1:1)
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    phone BIGINT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE user_settings (
    user_id BIGINT PRIMARY KEY REFERENCES users(id),
    theme VARCHAR(20) DEFAULT 'light',
    language VARCHAR(10) DEFAULT 'en'
);

-- Messages with self-referencing reply chain
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    sender_id BIGINT NOT NULL REFERENCES users(id),
    receiver_id BIGINT NOT NULL REFERENCES users(id),
    reply_to_id BIGINT REFERENCES messages(id),
    body TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Groups with members (M:M)
CREATE TABLE groups (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    owner_id BIGINT REFERENCES users(id)
);

CREATE TABLE group_members (
    group_id BIGINT REFERENCES groups(id),
    user_id BIGINT REFERENCES users(id),
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (group_id, user_id)
);
```

### Denormalisierungsmuster {#denormalization-patterns}
```sql
-- Materialized count: avoid COUNT(*) on large tables
ALTER TABLE users ADD COLUMN order_count INTEGER DEFAULT 0;
-- Update via trigger or application logic

-- Pre-computed join: store derived data
ALTER TABLE orders ADD COLUMN user_name VARCHAR(100);
-- Trade-off: faster reads, complex update logic
```

### Entwurfs-Antimuster: Einbetten von Listen {#design-anti-pattern-embedding-lists}
```sql
-- BAD: storing comma-separated values
CREATE TABLE users (id INT, hobbies TEXT);  -- hobbies = 'chess,reading,hiking'

-- GOOD: separate table for many-to-many
CREATE TABLE hobbies (id SERIAL PRIMARY KEY, name VARCHAR(50));
CREATE TABLE user_hobbies (user_id INT REFERENCES users(id), hobby_id INT REFERENCES hobbies(id));
```

## Stolperfallen {#gotchas}

- Übermäßige Normalisierung führt zu zu vielen JOINs – heiße Pfade gezielt denormalisieren
- ENUM-Werte sind später schwer zu ändern; stattdessen eine Lookup-/Referenztabelle erwägen
- Die Spaltenreihenfolge in PostgreSQL beeinflusst die Byte-Ausrichtung – Typen gleicher Größe gruppieren
- Auto-Increment-PKs geben Geschäftsinformationen preis (Bestellanzahl, Wachstumsrate)
- Fehlende Indizes auf FK-Spalten sind ein häufiger Performance-Killer

## Siehe auch {#see-also}

- [[ddl-schema-management]] - CREATE-TABLE-Syntax und Constraints
- [[data-types-and-nulls]] - Auswahl geeigneter Datentypen
- [[partitioning-and-sharding]] - Skalierung großer Tabellen
- [[btree-and-index-internals]] - Auswirkung von UUIDs auf die Indexleistung
