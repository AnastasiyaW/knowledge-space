---
title: "Offsets und Commits"
category: concepts
tags: [kafka, offset, commit, auto-commit, consumer-lag, __consumer_offsets]
level: 3
source_sha256: 1579131de8a94700fcb21bc90a06208c378f0787453a03f20dbb9346473a4a07
translation: machine
translated_at: '2026-10-24'
---
# Offsets und Commits {#offsets-and-commits}

Ein Offset ist eine fortlaufende Nachrichtennummer innerhalb einer Partition, die beim Schreiben vergeben wird. Consumer verfolgen ihre Position anhand von Offsets, die entweder im internen Topic `__consumer_offsets` von Kafka oder in einer externen Datenbank gespeichert werden.

## Wichtige Fakten {#key-facts}

- Ein Offset benötigt nur 8 Byte pro Partition und Consumer. Er ist ein Zeiger, der angibt, wo als Nächstes gelesen werden soll.
- Das Paar `(partition_number, offset)` adressiert eine Nachricht innerhalb eines Topics eindeutig.
- `__consumer_offsets` ist ein internes Topic, das folgende Daten speichert: Consumer-Gruppe + Topic + Partition + **nächster zu lesender Offset** (zuletzt gelesen + 1)
- `__consumer_offsets` verwendet standardmäßig `acks=all` und hat 50 Partitionen.
- Es gibt zwei Ebenen der Nachverfolgung: **broker-seitig** (immer aktiv, erfasst, was gesendet wurde) und **Consumer-Commit** (bestätigt die Verarbeitung).
- Auto-Commit (`enable.auto.commit=true`, Standard) committet alle `auto.commit.interval.ms` (Standard 5000 ms), unabhängig davon, ob die Verarbeitung erfolgreich war.
- Manueller Commit: `commitSync()` (blockierend) oder `commitAsync()` (nicht blockierend, mit Callback).
- Bewährte Praxis: `commitAsync()` während der Verarbeitung, `commitSync()` im `finally`-Block.
- Externe Offset-Speicherung: Offsets zusammen mit den Geschäftsdaten in der Anwendungsdatenbank speichern, um Exactly-once mit externen Systemen zu erreichen (Spark verwendet Checkpoint-Dateien und committet NICHT in `__consumer_offsets`).

## Muster {#patterns}

### Auto-Commit (gefährlicher Standard) {#auto-commit-dangerous-default}

```properties
# Default configuration - auto-commit enabled
enable.auto.commit=true
auto.commit.interval.ms=5000
```

**Problematischer Ablauf**: Consumer empfängt Nachrichten -> Auto-Commit wird ausgelöst -> Consumer stürzt während der Verarbeitung ab -> Nachrichten sind endgültig verloren.

### Manueller Commit (empfohlen) {#manual-commit-recommended}

```java
// Java - manual commit patterns
consumer.subscribe(List.of("orders"));
props.put("enable.auto.commit", "false");

try {
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            processRecord(record);
        }
        // Synchronous commit - blocks, safest
        consumer.commitSync();
    }
} catch (Exception e) {
    log.error("Processing failed", e);
} finally {
    consumer.commitSync();  // Final sync commit
    consumer.close();
}
```

```python
# Python - manual commit
conf = {"enable.auto.commit": False}
consumer = Consumer(conf)

msg = consumer.poll(0.1)
if msg and not msg.error():
    process(msg)
    consumer.commit(msg)
```

### Gezieltes Positionieren auf einen Offset {#seeking-to-specific-offset}

```java
// Read from specific offset
consumer.seek(new TopicPartition("topic", 0), 42L);

// Assign specific partitions (no consumer group coordination)
consumer.assign(List.of(new TopicPartition("topic", 0)));
```

### Strategien zum Zurücksetzen von Offsets {#offset-reset-strategies}

| Strategie | Verhalten | Anwendungsfall |
|-----------|-----------|----------------|
| `auto.offset.reset=latest` | Liest nur neue Nachrichten | Echtzeit-Stream-Verarbeitung |
| `auto.offset.reset=earliest` | Liest ab dem ältesten verfügbaren Eintrag | Fehlersuche, Datenmigration, vollständige Historie |
| `auto.offset.reset=none` | Wirft eine Exception | Explizites Fehlschlagen, wenn ein Offset fehlt |

### Offsets über die CLI zurücksetzen {#resetting-offsets-via-cli}

```bash
# Reset to earliest
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic \
  --reset-offsets --to-earliest --execute

# Reset to specific offset
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic:0 \
  --reset-offsets --to-offset 100 --execute

# Reset to timestamp
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --topic my-topic \
  --reset-offsets --to-datetime 2024-01-01T00:00:00.000 --execute
```

### Überwachung des Consumer-Lags {#consumer-lag-monitoring}

```bash
# Check consumer lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe
```

Consumer-Lag = neuester Offset in der Partition - committeter Offset des Consumers. Ein wachsender Lag bedeutet, dass die Consumer nicht mehr Schritt halten können. Lösungen: Partitionen und Consumer hinzufügen, die Verarbeitung optimieren, `fetch.min.bytes` und `fetch.max.wait.ms` erhöhen.

## Fallstricke {#gotchas}

- **Auto-Commit ist der häufigste Anfängerfehler**: Er committet, bevor die Verarbeitung abgeschlossen ist. Deaktivieren Sie ihn für jede Produktivlast, bei der Datenverlust relevant ist.
- **`auto.commit.interval.ms` muss kleiner sein als `session.timeout.ms`**. Andernfalls hält Kafka den Consumer für tot und löst ein Rebalancing aus, bevor der Commit erfolgt.
- **Ablauf von Offsets**: Ist ein Consumer länger inaktiv als `offsets.retention.minutes` (Broker-Einstellung, Standard 7 Tage), löscht Kafka die gespeicherten Offsets. Beim erneuten Verbinden greift `auto.offset.reset`.
- **Lücke nach Datenbank-Restore**: Nach dem Wiederherstellen einer Datenbank aus einem Backup zeigt der Consumer-Offset in Kafka auf die aktuelle Position. Die Daten aus der Lücke existieren in Kafka, der Consumer hat aber bereits über sie hinaus committet. Lösungen: Offset über die CLI zurücksetzen, eine neue Consumer-Gruppe verwenden oder Offsets in der Anwendungsdatenbank speichern.
- **Beschädigung von `__consumer_offsets`**: Kann bei häufigen Broker-Neustarts während laufender Lesevorgänge auftreten. Versuchen Sie zunächst, die problematischen Topic-Partitionen manuell neu zuzuweisen, bevor Sie die Consumer-Gruppe neu anlegen.

## Siehe auch {#see-also}

- [[consumer-groups]] - Gruppenmechanik und Partitionszuweisung
- [[delivery-semantics]] - wie die Offset-Verwaltung auf Zustellgarantien abgebildet wird
- [[kafka-transactions]] - atomares Committen von Offsets zusammen mit dem Produzieren von Nachrichten
- [Apache Kafka: Verwaltung von Consumer-Offsets](https://kafka.apache.org/documentation/#consumerconfigs)
