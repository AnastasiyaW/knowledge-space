---
title: "Kafka Streams Windowing"
category: concepts
tags: [kafka, streams, windowing, tumbling, hopping, session, sliding, grace-period, watermark]
level: 3
source_sha256: 0b394b6ffbd7119e0d8cf6dec7d2ecb4eaceec1e5bc58f316970f1d8c3b22df4
translation: machine
translated_at: '2026-10-24'
---
# Kafka Streams Windowing {#kafka-streams-windowing}

Fensteroperationen gruppieren Stream-Datensätze für Aggregationen in endliche Zeitintervalle. Unterstützt werden Tumbling-Fenster (nicht überlappend), Hopping-Fenster (überlappend), Session-Fenster (lückenbasiert) und Sliding-Fenster (Join-Fenster), jeweils mit konfigurierbaren Grace Periods für verspätet eintreffende Ereignisse.

## Key Facts {#key-facts}

- Fenster werden kontinuierlich ausgewertet, während neue Datensätze eintreffen
- Jeder Datensatz gehört je nach Fenstertyp zu einem oder mehreren Fenstern
- Die Retention steuert, wie viele vergangene Fenster in den State Stores aufbewahrt werden
- Die Grace Period legt die zusätzliche Zeit nach dem Schließen eines Fensters fest, in der verspätet eintreffende Datensätze noch akzeptiert werden; nach Ablauf werden verspätete Datensätze verworfen
- Die Retention muss >= Fenstergröße + Grace Period sein
- **Stream-Zeit**: maximaler Zeitstempel über alle bisher verarbeiteten Datensätze (nicht die Wanduhrzeit)
- Die Zeitstempelvergabe wird über `message.timestamp.type` gesteuert: `CreateTime` (vom Producer gesetzt) oder `LogAppendTime` (vom Broker gesetzt)

## Patterns {#patterns}

### Tumbling Window (fest, nicht überlappend) {#tumbling-window-fixed-non-overlapping}

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

### Hopping Window (fest, überlappend) {#hopping-window-fixed-overlapping}

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

### Session Window (dynamisch, lückenbasiert) {#session-window-dynamic-gap-based}

```java
// Sessions close after 5 minutes of inactivity
stream.groupByKey()
    .windowedBy(SessionWindows.ofInactivityGapWithNoGrace(Duration.ofMinutes(5)))
    .count();
// Sessions tracked independently per key
// Session duration varies based on actual activity patterns
```

### Sliding Window (Join-Fenster) {#sliding-window-join-windows}

```java
// For stream-stream joins: how far apart events can be joined
KStream<String, String> joined = stream1.join(
    stream2,
    (left, right) -> left + "+" + right,
    JoinWindows.ofTimeDifferenceAndGrace(Duration.ofMinutes(5), Duration.ofMinutes(1))
);
```

### ksqlDB Windowing {#ksqldb-windowing}

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

### Zeitsemantik {#time-semantics}

| Zeitkonzept | Beschreibung |
|-------------|-------------|
| Event-Zeit | Zeitpunkt, zu dem der Datensatz an der Quelle erzeugt wurde |
| Ingestion-Zeit | Zeitpunkt, zu dem der Broker den Datensatz gespeichert hat |
| Verarbeitungszeit | Zeitpunkt, zu dem die Stream-Processing-Anwendung den Datensatz verarbeitet |
| Stream-Zeit | Maximaler bisher gesehener Zeitstempel |

### Timestamp Extractors {#timestamp-extractors}

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

## Gotchas {#gotchas}

- **Die Grace Period beträgt in ksqlDB standardmäßig 24 Stunden** - das kann viel Speicher binden; passen Sie den Wert an die tatsächlichen Eigenschaften verspäteter Daten an
- **Verspätete Datensätze nach Ablauf der Grace Period werden stillschweigend verworfen** - kein Fehler, kein DLQ; überwachen Sie die Metriken für verworfene Datensätze
- **Die Retention muss >= Fenstergröße + Grace Period sein** - andernfalls werden Fenster entfernt, bevor sie verspätete Daten akzeptieren können
- **Session-Fenster können verschmelzen** - überlappen sich zwei Sessions desselben Schlüssels, nachdem ein verspätetes Ereignis eingetroffen ist, werden sie zu einer größeren Session zusammengeführt
- **Die Startzeiten der Fenster sind an der Epoche ausgerichtet** - Tumbling-Fenster beginnen an Grenzen der Unix-Epoche und nicht zum Start der Anwendung
- **Langsamer Writer = offenes Segment = Retention überschreitet die Konfiguration** - wenn das Schreiben langsam erfolgt, bleibt das Segment lange offen, sodass die tatsächliche Retention deutlich länger sein kann als konfiguriert

## See Also {#see-also}

- [[kafka-streams]] - Kern-Topologie, Operationen, Joins
- [[kafka-streams-state-stores]] - State Stores, die fensterbasierte Aggregationen unterstützen
- [[kafka-streams-time-semantics]] - Event-Zeit vs. Verarbeitungszeit, Watermarks
- [[ksqldb]] - SQL-Syntax für Windowing
- [Kafka Streams Windowing-Dokumentation](https://kafka.apache.org/documentation/streams/developer-guide/dsl-api.html#windowing)
