---
title: "Verteilte SQL-Datenbanken"
category: concepts
tags: [sql-databases, distributed, cockroachdb, citus, greenplum, yugabytedb, mpp, olap, sharding]
level: 4
source_sha256: 1f5d0de7bad695144cf15b81586be3e0326997c5cfce931b67e73dbf901539b1
translation: machine
translated_at: '2026-10-24'
---
# Verteilte SQL-Datenbanken {#distributed-sql-databases}

Wenn ein einzelner PostgreSQL-Server an seine Grenzen stößt, bieten verteilte Datenbanken horizontale Skalierung. Jede hat unterschiedliche Kompromisse hinsichtlich Konsistenz, Komplexität und Eignung für bestimmte Workloads.

## Vergleich {#comparison}

| Merkmal | Citus | CockroachDB | Greenplum | YugabyteDB |
|---------|-------|-------------|-----------|------------|
| Basis | PG-Erweiterung | Eigenentwicklung (PG-Wire) | PG-Fork | Eigenentwicklung (PG-Wire) |
| Konsistenz | Pro Shard | Serialisierbar | Pro Segment | Serialisierbar |
| Ideal für | Multi-Tenant-SaaS | Geo-verteiltes OLTP | Analytik/DWH | Verteiltes OLTP |
| OLTP | Gut | Gut | Schlecht | Gut |
| OLAP | Gut | Mittel | Hervorragend | Mittel |
| Komplexität | Gering (Erweiterung) | Mittel | Hoch (eigenständiges Produkt) | Mittel |

## Citus (PostgreSQL-Erweiterung) {#citus-postgresql-extension}

Von Microsoft übernommen (2019). Wandelt einen einzelnen PostgreSQL-Server in eine verteilte Datenbank um.

### Tabellentypen {#table-types}
- **Verteilt:** Hash-sharded auf die Worker, basierend auf der Verteilungsspalte
- **Referenz:** Auf alle Worker repliziert (Dimensions- bzw. Nachschlagetabellen)
- **Lokal:** Nur auf dem Koordinator

```sql
-- Create distributed table
SELECT create_distributed_table('events', 'tenant_id');

-- Queries automatically routed to relevant shard
SELECT count(*) FROM events WHERE tenant_id = 42;

-- Cross-shard queries supported but slower
SELECT tenant_id, count(*) FROM events GROUP BY tenant_id;
```

**Seit Citus 11.0:** Abfragen können von jedem Knoten aus ausgeführt werden. `citus.shard_replication_factor` ist standardmäßig 1 (keine Ausfallsicherheit).

## CockroachDB {#cockroachdb}

PostgreSQL-kompatibles verteiltes SQL. Multi-Master, automatisches Sharding, serialisierbare Isolation.

```bash
# 3-node cluster
cockroach start --certs-dir=certs --advertise-addr=node1 --join=node1,node2,node3
cockroach init --certs-dir=certs --host=node1
```

Geo-verteilt: 9 Knoten über 3 Regionen. Erfordert Zeitsynchronisation (500 ms Drift-Toleranz). Multi-Master: Schreibvorgänge in einer Region sind in allen anderen sichtbar.

## Greenplum MPP {#greenplum-mpp}

Quelloffenes MPP-RDBMS auf Basis von PostgreSQL. Spaltenorientierte Speicherung, massiv parallele Verarbeitung.

### Architektur {#architecture}
- **Master-Host:** Einstiegspunkt, SQL-Koordinator, keine Benutzerdaten
- **Segment-Hosts:** 2–8 PostgreSQL-Segmente pro Host, jeweils Primary und Mirror
- **Interconnect:** Dediziertes Hochgeschwindigkeitsnetzwerk

### Speichertypen {#storage-types}

| Typ | Ideal für |
|-----|-----------|
| Heap | Gleichzeitige UPDATE-/DELETE-/INSERT-Vorgänge |
| Append-Optimized (AO) | Batch-Ladevorgänge und Analytik, selten aktualisiert |
| Zeilenorientiert | Breite SELECTs, gemischte Workloads |
| Spaltenorientiert | Schmale SELECTs auf breiten Tabellen, Aggregationen |

### Leistungsregeln {#performance-rules}
- Geschwindigkeit = CPU-Kerne / Datenmenge pro Knoten
- 1 Abfrage = maximal 1 Kern pro Segment
- Clustergeschwindigkeit = langsamstes Segment; gleichmäßige Verteilung ist entscheidend
- Insert-only-Modell entwerfen; täglich die Partition truncaten, bevor geladen wird

## OLTP vs. OLAP {#oltp-vs-olap}

**OLTP:** Normalisiert, hohe Insert-/Update-Rate, viele gleichzeitige Benutzer, kleine Transaktionen, indiziert für schnellen Zugriff. Dreischichtige Architektur.

**OLAP:** Historische Datenberichte, spaltenorientierte Speicherung, denormalisierte Faktentabellen mit Dimensionen, seltene Updates, schnelle Lesezugriffe für Aggregationen.

## MPP (Massively Parallel Processing) {#mpp-massive-parallel-processing}

Daten und Rechenleistung sind auf Leader- und Worker-Knoten verteilt. Shared-Nothing-Architektur.

**Vorteile:** Schnelle Verarbeitung großer Datenmengen, einfache horizontale Skalierung, Ausfallsicherheit durch Mirroring.
**Nachteile:** Hoher Ressourcenbedarf, schlecht für viele einfache Abfragen, Ungleichgewicht bei der Segmentverteilung.

## ClickHouse {#clickhouse}

Spaltenorientierte OLAP-Datenbank (C++, Yandex). Vektorisierte Abfrageverarbeitung, effiziente Kompression, integrierte Replikation und Sharding. Umfangreicher SQL-Dialekt mit JSON-, IP-, UUID- und Array-Typen. Integration mit Kafka, MySQL und PostgreSQL.

## Weitere Lösungen {#other-solutions}

- **YugabyteDB:** PG-kompatibles verteiltes SQL mit serialisierbarer Isolation
- **Postgres-BDR / Bucardo:** Multi-Master über logische Replikation
- **Shardman (Postgres Pro):** FDW-basiertes Sharding, nur Hash-Verteilung, erhebliche Einschränkungen
- **Arenadata DB:** Russische kommerzielle Greenplum-Distribution

## Wichtige Fakten {#key-facts}

- PostgreSQL ist NICHT für Big Data ausgelegt: Transaktionen und WAL bremsen große Operationen, kein integriertes Sharding
- Citus ist der einfachste Weg von einem einzelnen PostgreSQL zu einer verteilten Lösung
- CockroachDB bietet die stärkste Konsistenz (serialisierbar) über verteilte Knoten hinweg
- Greenplum eignet sich hervorragend für Analytik, ist für OLTP jedoch schlecht geeignet
- Der Sharding-Schlüssel muss hohe Kardinalität und gleichmäßige Verteilung aufweisen

## Stolperfallen {#gotchas}

- Citus: `shard_replication_factor = 1` (Standard) bedeutet keine Ausfallsicherheit für einzelne Shards
- CockroachDB: 500 ms Zeitdrift-Toleranz – NTP-Synchronisation erforderlich
- Greenplum: 1 Kern pro Abfrage und Segment begrenzt die feingranulare Abfrageparallelität
- Shardman: kein ALTER TABLE (außer Owner/NULL/ADD COLUMN), keine Fremdschlüssel, nur SELECT-Transport
- Multi-Master-Replikation hat komplexe Konfliktauflösung – nur verwenden, wenn wirklich nötig

## Siehe auch {#see-also}

- [[partitioning-and-sharding]] - Konzepte für Partitionierung und Sharding auf einem einzelnen Server
- [[replication-fundamentals]] - Streaming-Replikation als einfachere Alternative
- [[postgresql-ha-patroni]] - Hochverfügbarkeit ohne Verteilung
- [[caching-redis-memcached]] - Caching-Schicht zur Entlastung der Datenbank
