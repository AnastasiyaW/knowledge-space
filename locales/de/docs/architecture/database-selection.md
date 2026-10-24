---
title: "Datenbankauswahl und -design"
category: reference
tags: [database, postgresql, redis, mongodb, cassandra, nosql, sql, orm]
level: 4
source_sha256: 54234710ca31cc281a41f38b2567d2f06c26e0a0f3ba10b62d2e04523fbf189b
translation: machine
translated_at: '2026-10-24'
---
# Datenbankauswahl und -design {#database-selection-and-design}

Die Wahl der richtigen Datenbank ist eine architektonische Entscheidung mit langfristigen Folgen. Berücksichtigen Sie Datentyp, Konsistenzanforderungen, Performancebedarf, Teamkompetenzen und Budget.

## OLTP vs. OLAP {#oltp-vs-olap}

| Aspekt | OLTP | OLAP |
|--------|------|------|
| Zweck | Echtzeit-Transaktionen | Analytische Abfragen, Reporting |
| Transaktionen | Viele, kurz | Wenige, lang laufend |
| Beispiele | PostgreSQL, MySQL, Oracle | ClickHouse, BigQuery, Greenplum |
| Anwendungsfall | Operative Daten von Services | DWH, Analytics, Reports |

## Auswahl nach Datentyp {#selection-by-data-type}

| Datentyp | DB-Typ | Beispiel | Geeignet für |
|----------|--------|----------|--------------|
| Strukturiert | Relational | PostgreSQL | Bestellungen, Benutzer, Transaktionen |
| Dokumente/JSON | Dokumentenorientiert | MongoDB | Hierarchische, semistrukturierte Daten |
| Hohes Volumen, häufige Änderungen | Key-Value | Redis | Sessions, Caching |
| Analytik/Reports | Spaltenorientiert | ClickHouse, Cassandra | Aggregationen im TB/PB-Bereich |
| Binärdaten/große Dateien | Objektspeicher | S3, MinIO | Bilder, Videos, Audio |
| Beziehungen | Graph | Neo4j | Soziale Netzwerke, Empfehlungen |

## Entscheidungsbaum {#decision-tree}

```rust
Need ACID transactions?
  Yes -> PostgreSQL (or MySQL)
Need flexible schema?
  Yes -> MongoDB
Need high write throughput (>500K TPS)?
  Yes -> Cassandra / ScyllaDB
Need sub-ms latency for simple keys?
  Yes -> Redis
Need full-text search?
  Yes -> Elasticsearch
Need relationship traversal?
  Yes -> Neo4j
Need analytical aggregations?
  Yes -> ClickHouse / BigQuery
```

## Vertiefung zu Datenbanken {#database-deep-dives}

### PostgreSQL {#postgresql}
Hoher Schreibdurchsatz, schnelle Lesezugriffe, JSON/XML-Unterstützung. Erfordert sorgfältiges Schemadesign.
- Einsatz für: Bestellabwicklung, ACID-kritische Daten, OLTP-Workloads
- OLAP-Erweiterungen: Greenplum, ClickHouse für die analytische Schicht

### Redis {#redis}
In-Memory-Key-Value-Speicher. Extrem schnelle Lese- und Schreibzugriffe. Integrierte TTL.
- Einsatz für: Sessions, Caching, Rate Limiting, Ranglisten
- Einschränkung: ressourcenintensiv bei großen Datenmengen (alles liegt im RAM)

### MongoDB / CouchDB {#mongodb-couchdb}
Flexibles Schema (JSON-Dokumente). Schnelle Entwicklung.
- Einsatz für: hierarchische Daten, schnelles Prototyping, Schemaentwicklung
- Einschränkung: nicht ideal für komplexe Transaktionen

### Cassandra {#cassandra}
Column Families, Skalierung im TB/PB-Bereich. Hervorragende horizontale Skalierbarkeit.
- Einsatz für: Analytics, Zeitreihen, IoT-Daten
- Einschränkung: nicht für häufige Schreibvorgänge oder komplexe Transaktionen geeignet

### S3 / MinIO {#s3-minio}
Objektspeicher. Skalierbar, feingranulare Zugriffskontrolle.
- Einsatz für: unstrukturierte Dateien (Bilder, Videos, Dokumente)
- Einschränkung: kann bei großem Umfang teuer werden

## Grundlagen des Datenbankdesigns {#database-design-fundamentals}

### Normalisierung {#normalization}
- **1NF** – atomare Werte, keine wiederholten Gruppen
- **2NF** – alle Nicht-Schlüsselattribute hängen vom gesamten Primärschlüssel ab
- **3NF** – keine transitiven Abhängigkeiten

### Schlüssel {#keys}
- **Primary Key** – eindeutiger Zeilenidentifikator
- **Foreign Key** – Referenz auf den PK einer anderen Tabelle
- **Composite Key** – mehrere Spalten als PK
- **Surrogate** – automatisch generiert (ohne fachliche Bedeutung)
- **Natural** – fachlich bedeutsam (E-Mail, Sozialversicherungsnummer)

### Indizes {#indexes}
| Typ | Geeignet für |
|-----|--------------|
| B-Tree | Bereichsabfragen, Gleichheitsvergleiche (Standard) |
| Hash | Schnelle Gleichheitssuche |
| GIN | Volltextsuche, JSONB |
| Partial | Teilmenge von Zeilen (WHERE-Klausel) |

### ACID-Transaktionen {#acid-transactions}
- **Atomicity** – alles oder nichts
- **Consistency** – von einem gültigen Zustand in einen gültigen Zustand
- **Isolation** – nebenläufige Transaktionen beeinflussen sich nicht gegenseitig
- **Durability** – committete Daten überstehen Ausfälle

### Isolationsstufen {#isolation-levels}
| Stufe | Dirty Reads | Non-Repeatable Reads | Phantom Reads |
|-------|-------------|----------------------|---------------|
| Read Uncommitted | Ja | Ja | Ja |
| Read Committed | Nein | Ja | Ja |
| Repeatable Read | Nein | Nein | Ja |
| Serializable | Nein | Nein | Nein |

Standard in PostgreSQL: Read Committed.

## Überlegungen zum ORM {#orm-considerations}

**Wann einsetzen:** schnelle Entwicklung, Standard-CRUD, Reduzierung von Boilerplate-Code. Eine Migration reduzierte 1500 Klassen manuellen SQL-Codes auf einen Bruchteil (5x weniger Code).

**Wann nicht einsetzen:** Reports (Raw SQL), hochlastkritische Pfade, komplexe analytische Abfragen.

**Hybrider Ansatz:** ORM für die Geschäftslogik, Raw SQL für Reports. Migrationswerkzeuge: Flyway, Liquibase (Java), Entity-Framework-Migrationen (.NET).

## Abfrageoptimierung {#query-optimization}

1. **EXPLAIN ANALYZE** – Ausführungsplan verstehen
2. **Indexnutzung** – sicherstellen, dass Abfragen Indizes verwenden
3. **SELECT * vermeiden** – nur benötigte Spalten abrufen
4. **JOIN-Optimierung** – richtige Reihenfolge, Indizes auf Join-Spalten
5. **Connection Pooling** – PgBouncer für PostgreSQL
6. **Partitionierung** – große Tabellen aufteilen (Range/List/Hash)
7. **Materialized Views** – vorberechnet für komplexe Reports

## Skalierungsmuster {#scaling-patterns}

- **Read Replicas** – Leselast verteilen
- **Sharding** – Daten anhand eines Schlüssels auf mehrere Datenbanken verteilen
- **Partitionierung** – Tabellen innerhalb einer Datenbank aufteilen
- **Hot/Cold Storage** – aktuelle Daten auf SSD, alte Daten auf günstigem Speicher

## Fallstricke {#gotchas}

- **Gemeinsam genutzte Datenbank zwischen Microservices** ist ein Anti-Pattern – enge Kopplung, Probleme bei der Schemakoordination
- **Voreiliges NoSQL** – mit PostgreSQL beginnen, sofern keine klaren NoSQL-Anforderungen bestehen
- **Redis als primärer Speicher** ohne Persistenzkonfiguration = Datenverlust bei einem Neustart
- **N+1-Abfrageproblem** – Lazy Loading im ORM erzeugt in Schleifen N+1 Abfragen. Eager Loading oder Batch-Fetching verwenden
- **Schemamigration ohne Rollback-Plan** – jede Migration benötigt ein zugehöriges Rollback-Skript
- **Sharding mit Replikation verwechseln** – Sharding verteilt Daten auf mehrere Rechner; Replikation kopiert dieselben Daten auf mehrere Rechner

## Siehe auch {#see-also}

- [[solution-architecture-process]] - Datenbankauswahl im Architekturkontext
- [[caching-and-performance]] - Redis als Cache, Connection Pooling
- [[distributed-systems-fundamentals]] - Sharding, Replikation, CAP
- [[bigdata-ml-architecture]] - OLAP, Data Warehousing
- [[devops-cicd]] - Zero-Downtime-Datenbankmigrationen
