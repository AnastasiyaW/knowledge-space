---
title: "Fenêtrage dans Kafka Streams"
category: concepts
tags: [kafka, streams, windowing, tumbling, hopping, session, sliding, grace-period, watermark]
level: 3
source_sha256: 0b394b6ffbd7119e0d8cf6dec7d2ecb4eaceec1e5bc58f316970f1d8c3b22df4
translation: machine
translated_at: '2026-10-24'
---
# Fenêtrage dans Kafka Streams {#kafka-streams-windowing}

Les opérations de fenêtrage regroupent les enregistrements d'un flux dans des intervalles de temps finis pour l'agrégation. Elles prennent en charge les fenêtres tumbling (non chevauchantes), hopping (chevauchantes), session (basées sur les écarts) et sliding (fenêtres de jointure), avec des périodes de grâce configurables pour les événements arrivant en retard.

## Points clés {#key-facts}

- Les fenêtres sont évaluées en continu à mesure que de nouveaux enregistrements arrivent
- Chaque enregistrement appartient à une ou plusieurs fenêtres selon le type de fenêtre
- La rétention des fenêtres contrôle le nombre de fenêtres passées conservées dans les state stores
- La période de grâce définit le temps supplémentaire après la fermeture d'une fenêtre pendant lequel les enregistrements en retard sont acceptés ; après expiration, les enregistrements en retard sont supprimés
- La rétention doit être >= taille de la fenêtre + période de grâce
- **Temps de flux** : timestamp maximal observé jusqu'à présent sur l'ensemble des enregistrements traités (et non l'horloge murale)
- L'attribution du timestamp est contrôlée par `message.timestamp.type` : `CreateTime` (défini par le producteur) ou `LogAppendTime` (défini par le broker)

## Modèles {#patterns}

### Fenêtre tumbling (fixe, non chevauchante) {#tumbling-window-fixed-non-overlapping}

```java
// 10-minute tumbling windows
stream.groupByKey()
    .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(10)))
    .count()
    .toStream()
    .to("counts");

// With grace period for late events
TimeWindows.ofSizeAndGrace(Duration.ofMinutes(10), Duration.ofMinutes(2))
// Windows: [00:00, 00:10), [00:10, 00:20), ...
// Record at 00:07 -> window [00:00, 00:10)
```

### Fenêtre hopping (fixe, chevauchante) {#hopping-window-fixed-overlapping}

```java
// 10-minute windows advancing every 5 minutes
stream.groupByKey()
    .windowedBy(
        TimeWindows.ofSizeAndGrace(Duration.ofMinutes(10), Duration.ofMinutes(2))
            .advanceBy(Duration.ofMinutes(5))
    )
    .count();
// Windows: [00:00, 00:10), [00:05, 00:15), [00:10, 00:20), ...
// Record at 00:07 -> belongs to BOTH [00:00, 00:10) AND [00:05, 00:15)
```

### Fenêtre de session (dynamique, basée sur les écarts) {#session-window-dynamic-gap-based}

```java
// Sessions close after 5 minutes of inactivity
stream.groupByKey()
    .windowedBy(SessionWindows.ofInactivityGapWithNoGrace(Duration.ofMinutes(5)))
    .count();
// Sessions tracked independently per key
// Session duration varies based on actual activity patterns
```

### Fenêtre sliding (fenêtres de jointure) {#sliding-window-join-windows}

```java
// For stream-stream joins: how far apart events can be joined
KStream<String, String> joined = stream1.join(
    stream2,
    (left, right) -> left + "+" + right,
    JoinWindows.ofTimeDifferenceAndGrace(Duration.ofMinutes(5), Duration.ofMinutes(1))
);
```

### Fenêtrage dans ksqlDB {#ksqldb-windowing}

```sql
-- Tumbling window aggregation
CREATE TABLE pageviews_per_region AS
  SELECT regionid, COUNT(*) FROM pageviews
  WINDOW TUMBLING (SIZE 30 SECONDS)
  GROUP BY regionid
  EMIT CHANGES;

-- Hopping window with retention and grace
CREATE TABLE hourly_counts AS
  SELECT userid, COUNT(*) FROM events
  WINDOW HOPPING (SIZE 1 HOUR, ADVANCE BY 10 MINUTES,
                  RETENTION 7 DAYS, GRACE PERIOD 30 MINUTES)
  GROUP BY userid
  EMIT CHANGES;

-- Session window
SELECT userid, COUNT(*) AS session_count
FROM pageviews WINDOW SESSION (5 MINUTES)
GROUP BY userid EMIT CHANGES;
```

### Sémantique temporelle {#time-semantics}

| Concept temporel | Description |
|-------------|-------------|
| Temps d'événement | Moment où l'enregistrement a été créé à la source |
| Temps d'ingestion | Moment où le broker a stocké l'enregistrement |
| Temps de traitement | Moment où l'application de traitement de flux le traite |
| Temps de flux | Timestamp maximal observé jusqu'à présent |

### Extracteurs de timestamp {#timestamp-extractors}

```java
// Built-in extractors
Consumed.with(Serdes.String(), Serdes.String())
    .withTimestampExtractor(new FailOnInvalidTimestamp());        // throws on invalid
    .withTimestampExtractor(new LogAndSkipOnInvalidTimestamp());  // logs, skips
    .withTimestampExtractor(new WallclockTimestampExtractor());  // uses system time

// Custom: extract from message body
.withTimestampExtractor((record, partitionTime) -> {
    MyEvent event = (MyEvent) record.value();
    return event.getTimestamp();
});
```

## Pièges {#gotchas}

- **La période de grâce par défaut est de 24 heures dans ksqlDB** : cela peut consommer une quantité importante de mémoire ; ajustez-la en fonction des caractéristiques réelles des données en retard
- **Les enregistrements en retard au-delà de la période de grâce sont silencieusement supprimés** : aucune erreur, aucune DLQ ; surveillez les métriques d'enregistrements supprimés
- **La rétention doit être >= taille de la fenêtre + période de grâce** : sinon, les fenêtres sont évincées avant de pouvoir accepter des données en retard
- **Les fenêtres de session peuvent fusionner** : si deux sessions pour la même clé se chevauchent après l'arrivée d'un événement en retard, elles fusionnent en une session plus grande
- **Les heures de début des fenêtres sont alignées sur l'epoch** : les fenêtres tumbling commencent aux bornes de l'epoch Unix, et non au moment du démarrage de l'application
- **Écriture lente = segment ouvert = rétention supérieure à la configuration** : si l'écriture est lente, le segment reste ouvert longtemps, de sorte que la rétention réelle peut être bien plus longue que la valeur configurée

## Voir aussi {#see-also}

- [[kafka-streams]] - topologie de base, opérations, jointures
- [[kafka-streams-state-stores]] - state stores sous-jacents aux agrégations fenêtrées
- [[kafka-streams-time-semantics]] - temps d'événement vs temps de traitement, watermarks
- [[ksqldb]] - syntaxe de fenêtrage SQL
- [Documentation sur le fenêtrage de Kafka Streams](https://kafka.apache.org/documentation/streams/developer-guide/dsl-api.html#windowing)
