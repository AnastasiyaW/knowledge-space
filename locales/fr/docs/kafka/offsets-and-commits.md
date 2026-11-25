---
title: "Offsets et commits"
category: concepts
tags: [kafka, offset, commit, auto-commit, consumer-lag, __consumer_offsets]
level: 3
source_sha256: 1579131de8a94700fcb21bc90a06208c378f0787453a03f20dbb9346473a4a07
translation: machine
translated_at: '2026-10-24'
---
# Offsets et commits {#offsets-and-commits}

Un offset est un numéro de message séquentiel au sein d'une partition, attribué à l'écriture. Les consommateurs suivent leur position grâce aux offsets, stockés soit dans le topic interne `__consumer_offsets` de Kafka, soit dans une base de données externe.

## Points clés {#key-facts}

- Un offset ne représente que 8 octets par partition et par consommateur : c'est un pointeur indiquant où lire ensuite
- Le couple `(partition_number, offset)` identifie de manière unique n'importe quel message d'un topic
- `__consumer_offsets` est un topic interne qui stocke : groupe de consommateurs + topic + partition + **prochain offset à lire** (dernier lu + 1)
- `__consumer_offsets` utilise `acks=all` par défaut, avec 50 partitions
- Deux niveaux de suivi : **côté broker** (toujours actif, suit ce qui a été envoyé) et **commit du consommateur** (confirme le traitement)
- L'auto-commit (`enable.auto.commit=true`, valeur par défaut) effectue un commit toutes les `auto.commit.interval.ms` (5000 ms par défaut), indépendamment du succès du traitement
- Commit manuel : `commitSync()` (bloquant) ou `commitAsync()` (non bloquant, avec callback)
- Bonne pratique : `commitAsync()` pendant le traitement, `commitSync()` dans le bloc `finally`
- Stockage externe des offsets : stocker les offsets dans la base de données applicative, à côté des données métier, pour obtenir un exactly-once avec des systèmes externes (Spark utilise des fichiers de checkpoint et ne fait **pas** de commit dans `__consumer_offsets`)

## Patterns {#patterns}

### Auto-commit (valeur par défaut dangereuse) {#auto-commit-dangerous-default}

```properties
# Default configuration - auto-commit enabled
enable.auto.commit=true
auto.commit.interval.ms=5000
```

**Scénario problématique** : le consommateur reçoit les messages -> l'auto-commit se déclenche -> le consommateur plante en plein traitement -> messages perdus définitivement.

### Commit manuel (recommandé) {#manual-commit-recommended}

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

### Positionnement sur un offset précis {#seeking-to-specific-offset}

```java
// Read from specific offset
consumer.seek(new TopicPartition("topic", 0), 42L);

// Assign specific partitions (no consumer group coordination)
consumer.assign(List.of(new TopicPartition("topic", 0)));
```

### Stratégies de réinitialisation d'offset {#offset-reset-strategies}

| Stratégie | Comportement | Cas d'usage |
|----------|----------|----------|
| `auto.offset.reset=latest` | Ne lit que les nouveaux messages | Traitement de flux en temps réel |
| `auto.offset.reset=earliest` | Lit depuis le plus ancien message disponible | Débogage, migration de données, historique complet |
| `auto.offset.reset=none` | Lève une exception | Échec explicite lorsque l'offset est absent |

### Réinitialisation des offsets via la CLI {#resetting-offsets-via-cli}

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

### Suivi du consumer lag {#consumer-lag-monitoring}

```bash
# Check consumer lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe
```

Consumer lag = dernier offset de la partition - offset commité du consommateur. Un lag croissant signifie que les consommateurs n'arrivent pas à suivre le rythme. Solutions : ajouter des partitions et des consommateurs, optimiser le traitement, augmenter `fetch.min.bytes` et `fetch.max.wait.ms`.

## Pièges {#gotchas}

- **L'auto-commit est l'erreur n°1 des débutants** : il commite avant la fin du traitement. Désactivez-le pour toute charge de production où la perte de données est critique
- **`auto.commit.interval.ms` doit être inférieur à `session.timeout.ms`** : sinon Kafka considère le consommateur comme mort et déclenche un rééquilibrage avant le commit
- **Expiration des offsets** : si un consommateur est inactif plus longtemps que `offsets.retention.minutes` (paramètre du broker, 7 jours par défaut), Kafka supprime les offsets stockés. À la reconnexion, `auto.offset.reset` entre en jeu
- **Trou lié à la restauration de la base** : après la restauration d'une base de données à partir d'une sauvegarde, l'offset du consommateur dans Kafka pointe sur la position actuelle. Les données de l'intervalle existent dans Kafka, mais le consommateur a déjà commité au-delà. Solutions : réinitialiser l'offset via la CLI, utiliser un nouveau groupe de consommateurs, ou stocker les offsets dans la base applicative
- **Corruption de `__consumer_offsets`** : peut survenir lors de redémarrages fréquents des brokers pendant une lecture active. Essayez de réassigner manuellement les partitions de topic problématiques avant de recréer le groupe de consommateurs

## Voir aussi {#see-also}

- [[consumer-groups]] - mécanique des groupes et affectation des partitions
- [[delivery-semantics]] - correspondance entre gestion des offsets et garanties de livraison
- [[kafka-transactions]] - commit atomique des offsets avec la production de messages
- [Gestion des offsets du consommateur Apache Kafka](https://kafka.apache.org/documentation/#consumerconfigs)
