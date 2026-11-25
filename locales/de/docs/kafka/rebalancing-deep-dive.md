---
title: "Rebalancing im Detail"
category: concepts
tags: [kafka, rebalancing, heartbeat, session-timeout, cooperative, static-membership]
level: 4
source_sha256: eb6d7db9789e65e36f8dbfae202e50b8caf45d50942165e6d8a7f2166a910d1a
translation: machine
translated_at: '2026-10-24'
---
# Rebalancing im Detail {#rebalancing-deep-dive}

Rebalancing ist der Prozess, bei dem Partitionszuweisungen unter den Consumern einer Gruppe neu verteilt werden, ausgelöst durch Änderungen der Gruppenmitgliedschaft. Es ist sowohl Kafkas Mechanismus zur Fehlertoleranz als auch die Hauptursache für Latenzspitzen auf Consumer-Seite.

## Wichtige Fakten {#key-facts}

- Jeder Consumer sendet alle `heartbeat.interval.ms` (Standard 3000 ms) einen Heartbeat an den **Group Coordinator** (einen dafür bestimmten Broker)
- Kommt innerhalb von `session.timeout.ms` kein Heartbeat an (Standard 10000 ms für Java, 45000 ms für librdkafka), wird der Consumer als tot betrachtet
- Der Heartbeat läuft in einem **eigenen Thread**, getrennt von der Nachrichtenverarbeitung
- `max.poll.interval.ms` (Standard 300000 ms = 5 min): maximale Zeit zwischen zwei `poll()`-Aufrufen; wird sie überschritten, löst dies ein Rebalancing aus
- Auslöser für Rebalancing: Consumer tritt bei oder verlässt die Gruppe, Änderung der Subscription, Änderung der Partitionsanzahl
- Wird ein Consumer pausiert (`.pause()`), löst dies **kein** Rebalancing aus, denn ein pausierter Consumer sendet weiterhin Heartbeats

## Muster {#patterns}

### Heartbeat-Tuning {#heartbeat-tuning}

```properties
# Recommended settings to avoid unnecessary rebalances
heartbeat.interval.ms=3000          # 1/3 of session.timeout.ms
session.timeout.ms=10000            # 10s for consumer failure detection
max.poll.interval.ms=300000         # 5 min for long processing
max.poll.records=100                # reduce batch size if processing is slow
```

Faustregel: `heartbeat.interval.ms = session.timeout.ms / 3`. So hat der Consumer drei Chancen, einen Heartbeat zu senden, bevor er als tot gilt.

### Kooperatives Rebalancing (empfohlen) {#cooperative-rebalancing-recommended}

```java
// Java - incremental cooperative rebalancing
props.put("partition.assignment.strategy",
    "org.apache.kafka.clients.consumer.CooperativeStickyAssignor");
```

Kooperatives Rebalancing entzieht und verteilt nur die betroffenen Partitionen neu. Alle übrigen Partitionen werden weiterhin ohne Unterbrechung konsumiert.

### Statische Gruppenmitgliedschaft {#static-group-membership}

```java
// Java - static membership
props.put("group.instance.id", "consumer-host-1");
// Consumer keeps its assignment across restarts
// No rebalance triggered on temporary disconnect
```

Risiko: Stürzt ein Consumer ab, bleibt seine Partition ungelesen, bis er neu gestartet wird (oder bis `session.timeout.ms` abläuft, sofern es sich nicht um ein statisches Mitglied handelt).

### Rebalance-Listener {#rebalance-listener}

```java
// Java - track rebalance events
consumer.subscribe(List.of("orders"), new ConsumerRebalanceListener() {
    @Override
    public void onPartitionsRevoked(Collection<TopicPartition> partitions) {
        // Commit offsets for revoked partitions
        consumer.commitSync(currentOffsets(partitions));
        // Clean up any in-memory state
    }

    @Override
    public void onPartitionsAssigned(Collection<TopicPartition> partitions) {
        // Initialize state for newly assigned partitions
        for (TopicPartition tp : partitions) {
            seekToStoredOffset(tp);
        }
    }
});
```

### Auslöser und Nicht-Auslöser für Rebalancing {#rebalance-triggers-and-non-triggers}

| Ereignis | Löst Rebalancing aus? |
|-------|-------------------|
| Consumer tritt der Gruppe bei | Ja |
| Consumer verlässt die Gruppe oder stürzt ab | Ja |
| Consumer ändert die Subscription | Ja |
| Partitionsanzahl steigt | Ja |
| Consumer ist pausiert (`.pause()`) | Nein |
| Consumer verarbeitet langsam (innerhalb von `max.poll.interval.ms`) | Nein |
| Consumer überschreitet `max.poll.interval.ms` | Ja |

## Fallstricke {#gotchas}

- **Rebalancing-Sturm**: Consumer stoppen und starten das Lesen wiederholt. Ursachen: Verarbeitung dauert länger als `session.timeout.ms`, langsamer Anwendungsstart, häufige Deployments, Netzwerkinstabilität. Abhilfe: Timeouts erhöhen, Batch-Größe reduzieren, CooperativeStickyAssignor verwenden
- **Gesamtes Lesen stoppt bei eagerem Rebalancing**: Beim standardmäßigen eager-Protokoll stoppen ALLE Consumer der Gruppe das Lesen während eines Rebalancings. Langsam startende Anwendungen verschärfen das Problem
- **Lange Verarbeitung + kurzes Timeout = endlose Rebalancing-Schleife**: Der Consumer verarbeitet einen Batch, überschreitet `max.poll.interval.ms`, wird entfernt, tritt erneut bei, erhält denselben Batch und überschreitet das Limit erneut
- **Gemischte Zuweisungsstrategien verursachen globales Rebalancing**: Alle Consumer einer Gruppe müssen dieselbe Partitionszuweisungsstrategie verwenden

## Siehe auch {#see-also}

- [[consumer-groups]] - Gruppenmechanik und Zuweisungsstrategien
- [[consumer-configuration]] - alle Consumer-Konfigurationsparameter mit Standardwerten
- [[kafka-monitoring-and-tuning]] - Überwachung der Rebalancing-Häufigkeit
- [KIP-429: Kafka Consumer Incremental Rebalance Protocol](https://cwiki.apache.org/confluence/display/KAFKA/KIP-429%3A+Kafka+Consumer+Incremental+Rebalance+Protocol)
