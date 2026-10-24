---
title: "Caching - Redis und Memcached"
category: concepts
tags: [sql-databases, redis, memcached, caching, cache-aside, write-through, lru, connection-cache]
level: 3
source_sha256: 2d0d8878b573a23944a17ab78f27bbf383626edbf3d2afe513de1cf0535868dc
translation: machine
translated_at: '2026-10-24'
---
# Caching - Redis und Memcached {#caching-redis-and-memcached}

Caching-Schichten zwischen Anwendung und Datenbank reduzieren die Abfragelast deutlich. Redis und Memcached sind die beiden dominierenden Lösungen mit unterschiedlichen Trade-offs.

## Vergleich {#comparison}

| Feature | Redis | Memcached |
|---------|-------|-----------|
| Datenstrukturen | Strings, Lists, Sets, Sorted Sets, Hashes, Streams | Nur Key-Value-Strings |
| Persistenz | RDB-Snapshots + AOF | Keine (nur RAM) |
| Threading | Single-threaded Commands (I/O-Threads seit 6.0) | Multi-threaded |
| Maximale Wertgröße | 512MB | 1MB |
| Pub/Sub | Ja | Nein |
| Replikation | Master-Replica | Nicht eingebaut |
| Clustering | Hash-Slots (16384) | Clientseitiges Consistent Hashing |

## Cache-Muster {#cache-patterns}

**Cache-Aside (Lazy Loading):** Die Anwendung prüft zuerst den Cache. Bei einem Miss wird die DB abgefragt und das Ergebnis im Cache gespeichert. Einfach, aber die erste Anfrage trifft immer die DB.

**Write-Through:** Die Anwendung schreibt gleichzeitig in Cache und DB. Der Cache ist stets aktuell, die Schreiblatenz steigt jedoch.

**Write-Behind:** Die Anwendung schreibt nur in den Cache. Der Cache schreibt asynchron in die DB. Die Schreibvorgänge sind am schnellsten, bei einem Absturz des Caches droht jedoch Datenverlust.

**Cache-Invalidierung:** TTL-basiert (veraltet für die Dauer der TTL), ereignisbasiert (Invalidierung beim Schreiben) oder über Versionierung.

## Redis-Dauerhaftigkeit {#redis-durability}

**RDB-Snapshots:** `save 900 1` (Snapshot, wenn mindestens 1 Key in 900s geändert wurde). `BGSAVE` forkt den Prozess; das Kind schreibt, während der Elternprozess weiter Anfragen bedient.

**AOF (Append-Only File):**
- `appendfsync always` - am sichersten, am langsamsten
- `appendfsync everysec` - guter Kompromiss (maximal 1 Sekunde Verlust)
- `appendfsync no` - das Betriebssystem bestimmt den Flush-Zeitpunkt

**Hybrid (Redis 4.0+):** RDB plus AOF der Änderungen seit dem letzten Snapshot. Schneller Neustart bei minimalem Datenverlust.

## Memcached-Architektur {#memcached-architecture}

**Slab-Allocator:** Der Speicher wird im Voraus in Größenklassen unterteilt (64B, 128B, 256B, ..., 1MB). Das reduziert Fragmentierung. Trade-off: interne Fragmentierung innerhalb der Chunks.

**LRU-Eviction:** Pro Slab-Klasse. Ist eine Klasse voll, wird das am längsten nicht genutzte Element aus genau dieser Klasse entfernt.

**CAS (Compare-And-Swap):** `gets` liefert ein CAS-Token, `cas` ist nur erfolgreich, wenn sich das Token nicht geändert hat. Verhindert verlorene Updates.

**Verteilung:** Die Server kennen einander nicht. Der Client implementiert Consistent Hashing. Das Hinzufügen eines Servers führt dazu, dass etwa 1/N der Keys neu zugeordnet werden.

## Wichtige Fakten {#key-facts}

- Redis als Cache: `SETEX key ttl value` für TTL-basiertes Caching
- Redis Cluster: automatisches Sharding über Knoten mit 16384 Hash-Slots
- Memcached: Multi-threaded, besser geeignet für einfaches Key-Value-Caching im großen Maßstab
- Ein lokaler Cache erfordert Sticky Sessions beim Load Balancer; ein geteilter Cache fügt Netzwerklatenz hinzu
- Die Cache-Hit-Rate für beliebte URLs liegt wahrscheinlich bei über 80 % (Pareto-Verteilung)

## Fallstricke {#gotchas}

- Cache-Invalidierung ist das schwierigste Problem; veraltete Daten können subtile Fehler verursachen
- Redis ist single-threaded: ein langsamer Befehl blockiert alle anderen Befehle
- Memcached-Slab-Klassen-Ungleichgewicht: Das Entfernen von 256B-Elementen kann keinen Platz für 64B-Elemente schaffen
- Redis-Persistenz (RDB+AOF) ist kein Ersatz für ein echtes Datenbank-Backup
- Die Verbindung zum Cache fügt einen zusätzlichen Netzwerk-Hop hinzu; cachen lohnt sich nur, wenn die DB-Abfragekosten deutlich über den Cache-Lookup-Kosten liegen
- Cache-Stampede: Viele gleichzeitige Misses für denselben Key treffen alle gleichzeitig die DB

## Siehe auch {#see-also}

- [[connection-pooling]] - Reduzierung von Datenbankverbindungen parallel zum Caching
- [[query-optimization-explain]] - Abfragen optimieren, bevor eine Cache-Schicht hinzugefügt wird
- [[distributed-databases]] - wenn Caching nicht ausreicht
- [Datenbanksicherheit](database-security.md) - getrennte Zugangsdaten für Cache- und DB-Zugriff
