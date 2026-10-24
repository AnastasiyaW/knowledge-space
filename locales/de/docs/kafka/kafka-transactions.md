---
title: "Kafka-Transaktionen"
category: concepts
tags: [kafka, transactions, exactly-once, transactional-id, zombie-fencing, isolation-level]
level: 3
source_sha256: c5bfe67406a49fab359097e2aaca97c633996ceeb3b6d79509371510849f1c0b
translation: machine
translated_at: '2026-10-24'
---
# Kafka-Transaktionen {#kafka-transactions}

Kafka-Transaktionen ermöglichen atomare Schreibvorgänge auf mehrere Topics/Partitionen. Entweder werden alle Nachrichten einer Transaktion committed, oder keine ist für `read_committed`-Consumer sichtbar. Damit lässt sich das Read-Process-Write-Exactly-once-Problem innerhalb von Kafka lösen.

## Wichtige Fakten {#key-facts}

- Eine Transaktion erlaubt das atomare Schreiben von Nachrichten in ein oder mehrere Topics
- Da Consumer-Offsets im Topic `__consumer_offsets` gespeichert werden, ist das Committen von Offsets ebenfalls ein Topic-Schreibvorgang. Innerhalb einer Transaktion können Sie daher atomar Ausgabe-Nachrichten senden UND Eingabe-Offsets committen
- Die Konfiguration `transactional.id` ist erforderlich und muss pro logischer Producer-Instanz eindeutig sein
- Das Setzen von `transactional.id` aktiviert automatisch den idempotenten Producer (`enable.idempotence=true`, `acks=all`)
- Transaktionsmetadaten werden im internen Topic `__transaction_state` gespeichert
- Der Standardwert von `isolation.level` ist `read_uncommitted`. Transaktionen haben keine Wirkung, solange der Consumer nicht `read_committed` setzt
- Der Transaktions-Overhead ist **pro Transaktion konstant**, unabhängig von der Nachrichtenanzahl. Größere Transaktionen verteilen den Overhead besser
- Große Transaktionen blockieren die Partition für `read_committed`-Consumer während der gesamten Transaktionsdauer
- `transaction.timeout.ms`: Timeout für den erzwungenen Abort, Standardwert 60 Sekunden
- Offsets in transaktionalen Topics wirken nicht fortlaufend (z. B. 0, 2, 4), da Control-Records (Commit- und Abort-Marker) dazwischen liegen

## Muster {#patterns}

### Transaction-API (Java) {#transaction-api-java}

```java
// Producer config
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "broker1:9092");
props.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "my-transactional-id");
// enable.idempotence and acks=all are auto-set

KafkaProducer<String, String> producer = new KafkaProducer<>(props);
producer.initTransactions();  // Call ONCE after creation

// Read-process-write loop
while (true) {
    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
    producer.beginTransaction();
    try {
        for (ConsumerRecord<String, String> record : records) {
            String result = process(record);
            producer.send(new ProducerRecord<>("output", record.key(), result));
        }
        // Commit input offsets within the transaction
        producer.sendOffsetsToTransaction(
            offsetsToCommit,
            consumer.groupMetadata()
        );
        producer.commitTransaction();
    } catch (Exception e) {
        producer.abortTransaction();
    }
}
```

### Consumer-Konfiguration für Transaktionen {#consumer-config-for-transactions}

```properties
isolation.level=read_committed   # Only see committed messages
enable.auto.commit=false         # Manage offsets via transaction
```

### Zombie-Fencing-Mechanismus {#zombie-fencing-mechanism}

```bash
Scenario without transactions:
  Instance 1 gets messages 1,2 -> processes message 1 -> sends A
  Instance 1 enters long GC pause
  Kafka rebalances -> Instance 2 gets partition
  Instance 2 processes message 2 -> sends B
  Instance 1 wakes up -> processes message 2 again -> sends B
  Result: A, B, B (DUPLICATE)

With transactions (same transactional.id = X):
  When Instance 2 calls initTransactions(t.id = X), epoch increments
  Instance 1 wakes up -> broker rejects (stale epoch)
  Result: A, B (CORRECT)
```

### Interna von Transaktionen (4 Phasen) {#transaction-internals-4-phases}

```sql
1. Producer -> Transaction Coordinator (TC):
   - Register transactional.id
   - TC aborts any active transaction with that ID
   - TC "fences" old producer (epoch increment)
   - Notify TC of each new partition involved
   - Commit/abort sent to TC

2. TC -> Transaction Log (__transaction_state):
   - All actions from step 1 recorded durably

3. Producer -> Topic/Partition:
   - Actual data writes (messages appear but invisible to read_committed)

4. TC -> Topic/Partition (after commit/abort):
   - Write commit/abort markers to all involved partitions
   - Update transaction state to completed
```

### AdminClient-Transaction-API {#adminclient-transaction-api}

```java
AdminClient admin = AdminClient.create(props);
admin.listTransactions();     // Returns: transactionalId, producerId, state
admin.describeTransactions(Collection<String> transactionalIds);
admin.abortTransaction(new AbortTransactionSpec(tp, producerId, epoch, coordEpoch));
```

## Fallstricke {#gotchas}

- **`isolation.level` ist standardmäßig `read_uncommitted`**: der kritischste Fehler. Transaktionen sind für Consumer unsichtbar, sofern sie nicht explizit `read_committed` wählen
- **`read_committed`-Consumer werden durch offene Transaktionen blockiert**: Nachrichten von ALLEN Producern (auch nicht-transaktionalen) in derselben Partition werden verzögert, bis die Transaktion abgeschlossen ist
- **Exactly-once funktioniert NUR für Kafka-zu-Kafka**: Ist ein externes System beteiligt (Datenbank, HTTP), müssen Sie At-least-once mit Deduplizierung verwenden (siehe [[transactional-outbox]])
- **Transaktionale Producer können `acks != all` nicht verwenden**: Das Setzen von `transactional.id` erzwingt `acks=all`. Ein Überschreiben wirft eine `ConfigException`
- **`transactional.id` muss über Neustarts hinweg stabil sein**: Darauf beruht das Zombie-Fencing. Eine neue ID bedeutet eine neue Producer-Identität, und dann findet kein Fencing statt
- **Offset-Commits in Transaktionen erfolgen über den Producer, nicht über den Consumer**: Verwenden Sie `producer.sendOffsetsToTransaction()`, nicht `consumer.commitSync()`

## Siehe auch {#see-also}

- [[idempotent-producer]]: PID- und Sequenznummern-Deduplizierung (Voraussetzung für Transaktionen)
- [[delivery-semantics]]: wie Transaktionen in die Exactly-once-Garantien passen
- [[transactional-outbox]]: Muster für Exactly-once mit externen Datenbanken
- [[kafka-producer-fundamentals]]: Producer-Pipeline und Fehlerbehandlung
- [KIP-98: Exactly-Once-Zustellung und transaktionales Messaging](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
