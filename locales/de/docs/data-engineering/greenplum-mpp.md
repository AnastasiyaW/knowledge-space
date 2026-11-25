---
title: "Greenplum und MPP-Architektur"
category: tools
tags: [data-engineering, greenplum, mpp, distributed-database, parallel-processing]
level: 3
source_sha256: 163a2870f4d1e311ea5f4a3381738724e756087532a6af0f5cc8d50c4a958aa2
translation: machine
translated_at: '2026-10-24'
---
# Greenplum und MPP-Architektur {#greenplum-and-mpp-architecture}

Greenplum ist eine analytische MPP-Datenbank (Massive Parallel Processing) auf Basis von PostgreSQL. Sie verwendet eine Shared-Nothing-Architektur, bei der jeder Knoten über eigene CPU, eigenen Speicher und eigene Festplatte verfügt.

## Architektur {#architecture}

```php
Client -> Master (QD: Query Dispatcher)
              |
    +---------+---------+
    Segment1  Segment2  Segment3  (QE: Query Executors)
    (mirror)  (mirror)  (mirror)
```

- **Master (QD):** nimmt Abfragen entgegen, erstellt den Plan, verteilt ihn an die Segmente und aggregiert die Ergebnisse. Speichert KEINE Benutzerdaten
- **Segmente (QE):** speichern Daten und führen Abfragen parallel aus. Jedes ist eine PostgreSQL-Instanz
- **Mirrors:** Standby-Kopien zur Ausfallsicherheit

## Motion-Operatoren {#motion-operators}

| Operator | Funktion | Kosten |
|----------|-------------|------|
| **Redistribute Motion** | Neuverteilung der Daten anhand des Hash-Schlüssels | Teuer |
| **Broadcast Motion** | Vollständige Kopie einer kleinen Tabelle auf alle Segmente | Mittel |
| **Gather Motion** | Sammeln der Ergebnisse auf dem Master | Gering |

## Verteilungsstrategien {#distribution-strategies}

```sql
-- Hash distribution (best for JOIN keys)
CREATE TABLE orders (...) DISTRIBUTED BY (order_id);

-- Random (default)
CREATE TABLE logs (...) DISTRIBUTED RANDOMLY;

-- Replicated (small dimension tables)
CREATE TABLE countries (...) DISTRIBUTED REPLICATED;
```

### Wichtige Optimierung {#key-optimization}

Beide Tabellen eines JOINs nach dem Join-Schlüssel zu verteilen, eliminiert die Redistribute Motion:

```sql
ALTER TABLE lineitem SET DISTRIBUTED BY (l_orderkey);
ALTER TABLE orders SET DISTRIBUTED BY (o_orderkey);
-- Redistribute Motion disappears from EXPLAIN plan
```

## ANALYZE (kritisch) {#analyze-critical}

```sql
ANALYZE table_name;
```

**Führen Sie ANALYZE nach jeder größeren Datenänderung immer aus.** Der Greenplum-Optimizer ist auf Statistiken angewiesen. Ohne aktuelle Statistiken nach INSERT/UPDATE verwendet der Optimizer veraltete Schätzungen, was zu suboptimalen Plänen führt.

**PostgreSQL führt Auto-Analyze einigermaßen zuverlässig aus. Greenplum tut dies NICHT – ein explizites ANALYZE ist erforderlich.**

## Greenplum vs. PostgreSQL: Indizes {#greenplum-vs-postgresql-indexes}

- PostgreSQL: Index anlegen -> Optimizer nutzt ihn -> schnellere Abfragen
- Greenplum: Index anlegen -> **Optimizer ignoriert ihn** (bevorzugt einen sequentiellen Scan über die Segmente)

```sql
-- Force index usage (rarely needed)
SET seq_page_cost = 100;
SET random_page_cost = 1;
SET optimizer = off;  -- GPORCA ignores hints
```

In MPP ist ein sequentieller Scan über viele Segmente häufig schneller als ein Index-Lookup.

## Komprimierung (TPC-H lineitem, scale=10) {#compression-tpc-h-lineitem-scale10}

| Speicherung | Größe |
|---------|------|
| Zeilenorientiert (Standard) | 34 GB |
| Zeilenorientiert + Komprimierung | 11 GB |
| Spaltenorientiert + Komprimierung | 7,5 GB |

## Tabellentypen {#table-types}

| Typ | Persistenz | Protokolliert | Sichtbar |
|------|-----------|--------|---------|
| Permanent | Übersteht Neustart | Ja (WAL) | Alle Sitzungen |
| Temporär | Nur Sitzung | Nein | Aktuelle Sitzung |
| Unlogged | Übersteht die Sitzung, geht bei Absturz verloren | Nein | Alle Sitzungen |
| External | Daten außerhalb der DB (S3, HDFS über PXF) | Nicht zutreffend | Alle Sitzungen |

## Stolperfallen {#gotchas}
- Indizes sind in Greenplum selten nützlich – der sequentielle Scan dominiert
- ANALYZE muss nach Massenoperationen manuell ausgeführt werden
- Externe Tabellen haben keine Statistiken – der Optimizer schätzt heuristisch
- Netzwerklatenz zwischen Rechenzentren beeinträchtigt die Clusterleistung stark
- Der GPORCA-Optimizer ignoriert Hints – zum erzwungenen Einsatz von Indizes muss er deaktiviert werden

## Siehe auch {#see-also}
- [[dwh-architecture]] - Kontext zum DWH-Design
- [[cloud-data-platforms]] - moderne Alternativen (Snowflake, BigQuery)
- [[spark-optimization]] - ähnliche Konzepte der verteilten Optimierung
