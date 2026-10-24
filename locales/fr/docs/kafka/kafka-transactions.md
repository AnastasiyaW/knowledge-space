---
title: "Transactions Kafka"
category: concepts
tags: [kafka, transactions, exactly-once, transactional-id, zombie-fencing, isolation-level]
level: 3
source_sha256: c5bfe67406a49fab359097e2aaca97c633996ceeb3b6d79509371510849f1c0b
translation: machine
translated_at: '2026-10-24'
---
# Transactions Kafka {#kafka-transactions}

Les transactions Kafka permettent des écritures atomiques sur plusieurs topics/partitions : soit tous les messages d'une transaction sont validés, soit aucun n'est visible pour les consommateurs `read_committed`. Cela résout le problème de l'exactly-once en lecture-traitement-écriture au sein de Kafka.

## Points clés {#key-facts}

- Une transaction permet d'écrire des messages sur un ou plusieurs topics de manière atomique
- Les offsets des consommateurs sont stockés dans le topic `__consumer_offsets`. Valider des offsets est donc aussi une écriture dans un topic : au sein d'une transaction, vous pouvez atomiquement envoyer les messages de sortie ET valider les offsets d'entrée
- La configuration `transactional.id` est obligatoire et doit être unique pour chaque instance logique de producteur
- Définir `transactional.id` active automatiquement le producteur idempotent (`enable.idempotence=true`, `acks=all`)
- Les métadonnées de transaction sont stockées dans le topic interne `__transaction_state`
- La valeur par défaut de `isolation.level` est `read_uncommitted` : les transactions n'ont aucun effet tant que le consommateur ne définit pas `read_committed`
- Le surcoût d'une transaction est **constant par transaction**, quel que soit le nombre de messages ; les grandes transactions amortissent mieux ce surcoût
- Les grandes transactions bloquent la partition pour les consommateurs `read_committed` pendant toute la durée de la transaction
- `transaction.timeout.ms` : délai au terme duquel la transaction est avortée de force, valeur par défaut de 60 secondes
- Les offsets dans les topics transactionnels apparaissent non séquentiels (par exemple 0, 2, 4) en raison des records de contrôle (marqueurs de validation ou d'annulation)

## Patrons {#patterns}

### API transactionnelle (Java) {#transaction-api-java}

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

### Configuration du consommateur pour les transactions {#consumer-config-for-transactions}

```properties
isolation.level=read_committed   # Only see committed messages
enable.auto.commit=false         # Manage offsets via transaction
```

### Mécanisme de zombie fencing {#zombie-fencing-mechanism}

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

### Fonctionnement interne des transactions (4 phases) {#transaction-internals-4-phases}

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

### API transactionnelle d'AdminClient {#adminclient-transaction-api}

```java
AdminClient admin = AdminClient.create(props);
admin.listTransactions();     // Returns: transactionalId, producerId, state
admin.describeTransactions(Collection<String> transactionalIds);
admin.abortTransaction(new AbortTransactionSpec(tp, producerId, epoch, coordEpoch));
```

## Pièges courants {#gotchas}

- **`isolation.level` vaut `read_uncommitted` par défaut** : c'est l'erreur la plus critique. Les transactions sont invisibles pour les consommateurs, sauf si ceux-ci activent explicitement `read_committed`
- **Les consommateurs `read_committed` sont bloqués par les transactions ouvertes** : les messages de TOUS les producteurs (y compris non transactionnels) sur la même partition sont retardés jusqu'à la fin de la transaction
- **L'exactly-once ne fonctionne QUE de Kafka à Kafka** : si un système externe est impliqué (base de données, HTTP), vous devez utiliser at-least-once avec déduplication (voir [[transactional-outbox]])
- **Les producteurs transactionnels ne peuvent pas utiliser `acks != all`** : définir `transactional.id` force `acks=all`. Tenter de le surcharger lève une `ConfigException`
- **`transactional.id` doit rester stable entre les redémarrages** : c'est ce qui rend le zombie fencing possible. Un nouvel identifiant signifie une nouvelle identité de producteur, donc aucun fencing
- **Les commits d'offsets dans une transaction passent par le producteur, pas par le consommateur** : il faut utiliser `producer.sendOffsetsToTransaction()`, et non `consumer.commitSync()`

## Voir aussi {#see-also}

- [[idempotent-producer]] : déduplication par PID et numéro de séquence (prérequis des transactions)
- [[delivery-semantics]] : place des transactions dans les garanties exactly-once
- [[transactional-outbox]] : patron d'exactly-once avec des bases de données externes
- [[kafka-producer-fundamentals]] : pipeline du producteur et gestion des erreurs
- [KIP-98 : livraison exactly-once et messagerie transactionnelle](https://cwiki.apache.org/confluence/display/KAFKA/KIP-98+-+Exactly+Once+Delivery+and+Transactional+Messaging)
