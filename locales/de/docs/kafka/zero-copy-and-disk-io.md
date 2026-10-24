---
title: "Zero-Copy und Disk-I/O"
category: concepts
tags: [kafka, zero-copy, sendfile, page-cache, sequential-io, performance]
level: 3
source_sha256: 88aae180d3b60f3350c6e41b2c22164c302bdbb2c5bbc96b700bfa5f84135a48
translation: machine
translated_at: '2026-10-24'
---
# Zero-Copy und Disk-I/O {#zero-copy-and-disk-io}

Kafka erreicht einen hohen Durchsatz durch sequenzielles Disk-I/O, die Nutzung des Page Cache des Betriebssystems und Zero-Copy-Übertragung über `sendfile()`. Dadurch ist die CPU praktisch nie der Engpass.

## Wichtige Fakten {#key-facts}

- Kafka verwendet den Systemaufruf `sendfile()` (Zero-Copy), um Daten von der Festplatte an den Netzwerk-Socket zu übertragen, und umgeht dabei Puffer im Userspace
- Die Daten auf der Festplatte liegen exakt im Netzwerk-Wire-Format vor, eine CPU-Transformation ist nicht nötig
- Sequenzielles Disk-I/O ist im großen Maßstab schneller als zufälliger Speicherzugriff
- Der Datenfluss lautet: Festplatte -> Kernel-Page-Cache -> NIC (Netzwerkkarte) per DMA, die CPU ist nicht beteiligt
- Typische Ausfallkaskade: Zuerst fällt das Netzwerk aus, dann die Festplatte, die CPU fast nie
- Moderne 10-Gbit/s-Netzwerke in Rechenzentren können Dutzende unabhängige Leser pro Topic bedienen
- Mehrere Consumer sind sehr günstig, weil die Daten aus dem Page Cache bereitgestellt werden
- Zero-Copy funktioniert NUR, wenn SSL auf dem Broker-Listener NICHT aktiviert ist
- Nachrichten werden gebündelt und auf Batch-Ebene komprimiert, auf der Festplatte komprimiert gespeichert und von den Consumern dekomprimiert
- Batch-Header speichern den neuesten `CreateTime` der enthaltenen Nachrichten

## Muster {#patterns}

### So funktioniert Zero-Copy {#how-zero-copy-works}

```php
Traditional (without zero-copy):
  Disk -> Kernel Buffer -> User Space Buffer -> Socket Buffer -> NIC
  (4 copies, 4 context switches)

Kafka (with zero-copy / sendfile):
  Disk -> Kernel Page Cache -> NIC (via DMA)
  (2 copies, 0 context switches, CPU uninvolved)
```

### Warum Kafka schnell ist {#why-kafka-is-fast}

```sql
1. Sequential I/O:
   - Append-only writes (no random seeks)
   - Sequential reads (consumers read in order)
   - HDD sequential: 200-300 MB/s vs random: 0.1-1 MB/s

2. Page Cache:
   - OS caches recently written/read data
   - Hot data served from memory without Kafka knowing
   - JVM heap stays clean (no GC pressure from data)

3. Batching:
   - Producer accumulates messages into batches
   - One batch = one disk write, one network send
   - 100 messages = 1 Kafka write

4. Compression:
   - Batch-level compression (lz4/zstd/snappy/gzip)
   - Stored compressed, transferred compressed
   - Consumer decompresses on read
```

### Aufbau der Segmentdateien {#segment-file-structure}

```text
/var/kafka/data/
  orders-0/                          # topic "orders", partition 0
    00000000000000000000.log         # segment file (records)
    00000000000000000000.index       # offset-to-position index
    00000000000000000000.timeindex   # timestamp-to-offset index
    00000000000000123456.log         # next segment (starts at offset 123456)
    leader-epoch-checkpoint
```

- `.log` - eigentliche Nachrichtendaten (batch-komprimiert)
- `.index` - spärliche Zuordnung von Offset zu Byte-Position
- `.timeindex` - spärliche Zuordnung von Zeitstempel zu Offset

## Fallstricke {#gotchas}

- **SSL deaktiviert Zero-Copy** - Bei aktiviertem SSL müssen die Daten im Userspace verschlüsselt werden. Das erhöht die CPU-Last und hebt die Optimierung durch `sendfile()` auf
- **Die JVM-GC betrifft den Datenpfad NICHT** - Kafka speichert Daten im Page Cache (außerhalb des JVM-Heaps). Der GC-Druck entsteht durch Verbindungsverwaltung und Metadaten, nicht durch Daten
- **Page-Cache-Thrashing** - Bedient der Broker zu viele verschiedene Partitionen, die nicht in den RAM passen, führen Verdrängungen aus dem Page Cache zu Festplattenzugriffen. Die Trefferquote des Caches sollte überwacht werden
- **Segment bleibt bei langsamen Schreibern lange offen** - Die tatsächliche Aufbewahrungsdauer kann deutlich länger sein als konfiguriert, da die Aufbewahrung nur für geschlossene Segmente gilt

## Siehe auch {#see-also}

- [[broker-architecture]] - Log-Segmente, Aufbewahrungsrichtlinien, Segment-Rollover
- [[topics-and-partitions]] - Layout auf der Festplatte, Segmentkonfiguration
- [[kafka-producer-fundamentals]] - Batching und Komprimierung auf Producer-Ebene
- [Kafka-Design: Effizienz](https://kafka.apache.org/documentation/#maximizingefficiency)
