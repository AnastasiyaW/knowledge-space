---
title: "Partitionierung und Sharding"
category: concepts
tags: [sql-databases, partitioning, sharding, consistent-hashing, horizontal-partitioning, postgresql, billion-rows]
level: 4
source_sha256: a2a7f417c6821899519786a8c71b76a6ee2b67bd45fdc7ad3beed25dceea1336
translation: machine
translated_at: '2026-10-24'
---
# Partitionierung und Sharding {#partitioning-and-sharding}

Partitionierung teilt eine große Tabelle in kleinere physische Segmente auf demselben Server auf. Sharding verteilt Daten auf mehrere Server. Beides sind Strategien für Tabellen, die über die Kapazität eines einzelnen Servers hinauswachsen.

## Strategiehierarchie (einfachere Ansätze zuerst) {#strategy-hierarchy-prefer-simpler-first}

1. **Datenmodell überarbeiten** - die Tabelle mit einer Milliarde Zeilen ganz vermeiden
2. **Indexierung** - B-Baum-/LSM-Indizes zur Eingrenzung der Suche
3. **Partitionierung** - Tabelle auf demselben Server aufteilen
4. **Sharding** - auf mehrere Server verteilen
5. **MapReduce** - parallele Brute-Force-Verarbeitung (letzte Option)

## Horizontale Partitionierung {#horizontal-partitioning}

```sql
-- PostgreSQL: range partitioning
CREATE TABLE grades (id SERIAL NOT NULL, g INTEGER NOT NULL)
PARTITION BY RANGE (g);

CREATE TABLE g_00_35 PARTITION OF grades FOR VALUES FROM (0) TO (35);
CREATE TABLE g_35_60 PARTITION OF grades FOR VALUES FROM (35) TO (60);
CREATE TABLE g_60_80 PARTITION OF grades FOR VALUES FROM (60) TO (80);
CREATE TABLE g_80_100 PARTITION OF grades FOR VALUES FROM (80) TO (100);

-- Index on partitioned table (applies to all partitions)
CREATE INDEX g_idx ON grades (g);
```

### Partitionstypen {#partition-types}

| Typ | Schlüssel | Geeignet für |
|-----|-----------|--------------|
| Range | Datum, ID-Bereiche | Zeitreihen, Archivierung (alte Partitionen per DROP entfernen) |
| List | Diskrete Werte (Land, Status) | Kategoriale Daten |
| Hash | Hashwert des Spaltenwerts | Gleichmäßige Verteilung unabhängig von Mustern |
| Composite | Range + Hash | Datumsbereich, innerhalb des Bereichs Hash nach Benutzer |

### Partition Pruning {#partition-pruning}
```sql
-- EXPLAIN shows only relevant partition scanned
EXPLAIN ANALYZE SELECT count(*) FROM grades WHERE g = 30;
-- Scans only g_00_35 partition
```

### Vertikale Partitionierung {#vertical-partitioning}
Spalten auf separate Tabellen aufteilen. Häufig abgefragte Spalten in einer Tabelle, große BLOBs/Texte in einer anderen. Verringert die Seitengröße, dadurch passen mehr Zeilen auf eine Seite und es fallen weniger I/Os an.

## Sharding {#sharding}

Daten auf mehrere Datenbankserver verteilen. Jeder Shard besitzt seine eigenen Partitionen und Indizes.

### Consistent Hashing {#consistent-hashing}
```javascript
// Hash key to determine shard
const crypto = require('crypto');
const hash = crypto.createHash('md5').update(urlId).digest('hex');
const shardIndex = parseInt(hash.substring(0, 8), 16) % NUM_SHARDS;
```

Beim Hinzufügen oder Entfernen von Shards werden nur die Schlüssel des benachbarten Shards neu verteilt (nicht alle Schlüssel).

### Auswahl des Sharding-Schlüssels {#sharding-key-selection}
Entscheidend für eine ausgewogene Verteilung. Schlechtes Beispiel: Sharding nach Sprache, wenn 90 % der Benutzer Englisch sprechen - ein Shard erhält die zehnfache Last. Verwenden Sie Schlüssel mit hoher Kardinalität und gleichmäßiger Verteilung.

### Abwägungen beim Sharding {#sharding-trade-offs}

**Vorteile:** Horizontale Skalierung, kleinere Indizes pro Shard, Sicherheitsisolation, Datenlokalität.

**Nachteile:** Komplexität beim Client-Routing, Transaktionen über mehrere Shards (erfordern 2PC oder Eventual Consistency), JOINs über Shards hinweg in SQL nicht möglich, Schemaänderungen auf allen Shards, Hotspot-Shards.

## Wichtige Fakten {#key-facts}

- Der Partitionsschlüssel MUSS in Primärschlüssel und Eindeutigkeitsbedingungen enthalten sein
- Die Erweiterung `pg_partman` automatisiert die Erstellung und Aufbewahrung von Partitionen
- Sharding sollte die letzte Option sein - zuerst prüfen: Read-Replicas, Caching, Pooling, Optimierung, Partitionierung
- Partitionsübergreifende Abfragen scannen ALLE Partitionen (schlechter als unpartitionierte Tabellen ohne Pruning)
- Das Verschieben einer Zeile zwischen Partitionen (UPDATE auf den Partitionsschlüssel) ist aufwendig

## Fallstricke {#gotchas}

- Übermäßige Partitionierung: Zu viele Partitionen bedeuten Metadaten-Overhead und viele kleine Dateien
- PostgreSQL-Fast-Path für schwache Sperren: 16 Slots pro Backend - stark partitionierte Abfragen können dieses Limit überschreiten
- Eindeutigkeitsbedingungen müssen in PostgreSQL den Partitionsschlüssel enthalten
- Fremdschlüssel, die auf partitionierte Tabellen verweisen, haben Einschränkungen
- Resharding erfordert Datenmigration und möglicherweise Ausfallzeiten
- Aggregationen über Shards hinweg (COUNT, SUM) erfordern Abfragen aller Shards und das Zusammenführen der Ergebnisse

## Siehe auch {#see-also}

- [[btree-and-index-internals]] - Indexverhalten bei Partitionen
- [[distributed-databases]] - Citus, CockroachDB für automatisches Sharding
- [[query-optimization-explain]] - Partition Pruning in EXPLAIN
- [[database-storage-internals]] - Auswirkungen der Partitionierung auf Seitenebene
