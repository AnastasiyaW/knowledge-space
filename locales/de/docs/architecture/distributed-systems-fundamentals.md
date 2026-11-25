---
title: "Grundlagen verteilter Systeme"
category: concepts
tags: [distributed-systems, cap-theorem, consensus, replication, partitioning]
level: 3
source_sha256: 775f52252832141307b34607da29e9821156c9cfb3c9d84a2ba339093ae4319b
translation: machine
translated_at: '2026-10-24'
---
# Grundlagen verteilter Systeme {#distributed-systems-fundamentals}

Verteilte Systeme bringen Fehlermodi mit sich, die in Single-Process-Systemen nicht existieren: Netzwerkpartitionen, partielle Ausfälle, Clock Skew und Nachrichtenreihenfolge-Vertauschungen. Das Verständnis dieser Grenzen ist für fundierte Architekturentscheidungen unerlässlich.

## Latenzzahlen, die jeder Ingenieur kennen sollte {#latency-numbers-every-engineer-should-know}

| Operation | Latenz |
|-----------|---------|
| L1-Cache-Zugriff | ~1 ns |
| L2-Cache-Zugriff | ~4 ns |
| Hauptspeicherzugriff | ~100 ns |
| SSD-Zufallslesezugriff | ~100 us |
| Distributed-Cache-Get (Redis) | ~1 ms |
| Einfache DB-Abfrage | ~1-10 ms |
| HDD-Seek | ~10 ms |
| Round Trip innerhalb des Rechenzentrums | ~0.5 ms |
| Netzwerk zwischen Regionen | ~50-150 ms |

**Zentrale Erkenntnis:** Netzwerkaufrufe sind 10.000- bis 1.000.000-mal langsamer als Speicherzugriffe. Lokaler App-Cache vs. verteilter Cache: Unterschied in der Größenordnung (100 ns vs. 1 ms).

## CAP-Theorem {#cap-theorem}

In einem verteilten System lassen sich von drei Eigenschaften höchstens zwei garantieren:

- **Consistency** - alle Knoten sehen dieselben Daten
- **Availability** - jede Anfrage erhält eine Antwort
- **Partition Tolerance** - das System funktioniert trotz Netzwerkausfällen

Da Netzwerkpartitionen unvermeidbar sind, lautet die eigentliche Wahl **CP** (konsistent, kann aber während einer Partition Anfragen ablehnen) vs. **AP** (verfügbar, kann aber veraltete Daten liefern).

### Erweiterung: PACELC {#pacelc-extension}

Bei einer **P**artition wählt man zwischen **A**vailability und **C**onsistency. **E**lse (regulärer Betrieb): zwischen **L**atency und **C**onsistency. Auch ohne Partitionen besteht ein Zielkonflikt zwischen Konsistenz und Latenz.

### Praktische Auswirkungen auf das API-Design {#practical-implications-for-api-design}
- **Konsistenz wählen** für: Finanztransaktionen, Bestandsverwaltung
- **Verfügbarkeit wählen** für: Social-Media-Feeds, Empfehlungen
- Die meisten Systeme benötigen an verschiedenen Stellen beides - entsprechend entwerfen

## Konsistenzmodelle {#consistency-models}

| Modell | Garantie | Anwendungsfall |
|-------|-----------|----------|
| **Stark (Linearisierbarkeit)** | Jeder Lesezugriff liefert den neuesten Schreibvorgang | Verteilte Locks, Leader-Election |
| **Kausal** | Kausal zusammenhängende Operationen werden in der richtigen Reihenfolge gesehen | Guter Ausgleich zwischen Korrektheit und Performance |
| **Read-your-writes** | Nutzer sieht eigene Änderungen sofort | Die meisten Webanwendungen |
| **Eventual** | Replikas konvergieren nach hinreichend langer Zeit | DNS, CDN-Caches, Social-Counter |

## Konsens-Algorithmen {#consensus-algorithms}

**Problem:** Wie einigen sich verteilte Knoten trotz Ausfällen auf einen Wert?

**Raft** - leaderbasiert. Leader-Wahl über randomisierte Timeouts. Log-Replikation an Follower. Committed, sobald eine Mehrheit bestätigt. Auf Verständlichkeit ausgelegt. Verwendet in: etcd, CockroachDB, TiKV.

**Paxos** - grundlegend, mathematisch bewiesen. Komplex. Verwendet in: Google Chubby, Spanner.

**Praxishinweis:** Konsens ist teuer (mehrere Round Trips). Nur einsetzen, wenn starke Konsistenz erforderlich ist. In den meisten Fällen reicht Eventual Consistency mit Konfliktauflösung aus.

## Replikationsstrategien {#replication-strategies}

### Single-Leader {#single-leader}
Ein Knoten nimmt Schreibvorgänge entgegen und repliziert sie an Follower. Einfach und konsistent. Der Leader ist ein Engpass und ein SPOF. Verwendet in: PostgreSQL-Streaming-Replikation, MySQL-Replikation.

### Multi-Leader {#multi-leader}
Mehrere Knoten nehmen Schreibvorgänge entgegen und synchronisieren sich untereinander. Bessere Schreibverfügbarkeit für geografisch verteilte Systeme. Herausforderung: Konfliktauflösung (Last-Writer-Wins, Merge-Funktionen, CRDTs).

### Leaderless (Dynamo-artig) {#leaderless-dynamo-style}
Jeder Knoten nimmt Lese- und Schreibzugriffe an. Quorum-basiert: Lesen R + Schreiben W > N Replikas. Verwendet in: Cassandra, DynamoDB, Riak. Herausforderung: Read Repair, Anti-Entropy.

## Partitionierung (Sharding) {#partitioning-sharding}

Daten werden auf mehrere Knoten verteilt, wenn ein einzelner Knoten Volumen oder Durchsatz nicht bewältigen kann.

### Schlüsselbasierte (Hash-)Partitionierung {#key-based-hash-partitioning}
Der Hash des Schlüssels bestimmt die Partition. Gleichmäßige Verteilung, aber keine Bereichsabfragen. Consistent Hashing vermeidet eine vollständige Neuverteilung, wenn sich Knoten ändern.

### Bereichspartitionierung {#range-partitioning}
Zusammenhängende Schlüsselbereiche werden Partitionen zugewiesen. Unterstützt Bereichsabfragen, birgt aber das Risiko von Hot Spots.

### Partitionierung von Sekundärindizes {#secondary-index-partitioning}
- **Lokale Indizes** - jede Partition indiziert ihre eigenen Daten (Scatter-Gather-Abfragen)
- **Globale Indizes** - separat partitioniert (Abfragen auf einer Partition, aber komplexere Schreibvorgänge)

## Resilienzmuster {#resilience-patterns}

### Circuit Breaker {#circuit-breaker}
Verhindert Kaskadenausfälle, indem bei einem ungesunden Downstream-System sofort ein Fehler zurückgegeben wird. Zustände: Closed -> Open -> Half-Open.

### Bulkhead {#bulkhead}
Isoliert Ausfälle durch Partitionierung von Ressourcen (Thread-Pools, Connection-Pools). Ein Ausfall in einer Partition wirkt sich nicht auf andere aus.

### Timeouts und Retries {#timeouts-and-retries}
- **Exponential Backoff** - exponentiell wachsende Wartezeit: 5 s -> 25 s -> 125 s
- **Jitter** - zufällige Variation, um Thundering Herds zu vermeiden
- Nur transiente Fehler (5xx, Timeouts) wiederholen, niemals Client-Fehler (4xx)

### Graceful Degradation {#graceful-degradation}
Nicht kritische Funktionen deaktivieren, um die Kernfunktionalität aufrechtzuerhalten. Feature Flags für dynamisches Ein- und Ausschalten.

## Trugschlüsse der verteilten Datenverarbeitung (Peter Deutsch) {#fallacies-of-distributed-computing-peter-deutsch}

1. Das Netzwerk ist zuverlässig
2. Latenz ist null
3. Bandbreite ist unendlich
4. Das Netzwerk ist sicher
5. Die Topologie ändert sich nicht
6. Es gibt nur einen Administrator
7. Transportkosten sind null
8. Das Netzwerk ist homogen

Jeder Trugschluss wird in der Produktion zu einem Bug.

## Fallstricke {#gotchas}

- **Essenzielle vs. zufällige Komplexität** - verteilte Komplexität nur hinzufügen, wenn sie nötig ist. Einfach beginnen
- **Auslastung über 70-80 %** führt zu überproportional steigenden Antwortzeiten (Hockey-Stick-Kurve der Warteschlangentheorie)
- **Netzwerkaufrufe in Schleifen** - eine scheinbar einfache Schleife mit 100 Iterationen kann über 50 Sekunden dauern, wenn jede einen Netzwerkaufruf enthält
- **Clock Skew** zwischen Knoten macht zeitstempelbasierte Ordnung ohne Vektoruhren oder Hybrid Logical Clocks unzuverlässig

## Siehe auch {#see-also}

- [[queueing-theory]] - Warum Systeme unter Last nichtlinear degradieren
- [[quality-attributes-reliability]] - Verfügbarkeit, Fehlertoleranz, Wiederherstellbarkeit
- [[microservices-communication]] - Saga-, CQRS- und Event-Sourcing-Muster
- [[transactions-and-acid]] - ACID vs. BASE-Abwägungen in verteilten Datenbanken
