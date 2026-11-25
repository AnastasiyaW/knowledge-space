---
title: "Kafka Streams Zeitsemantik"
category: concepts
tags: [kafka, streams, event-time, processing-time, watermark, dataflow-model, late-data]
level: 2
source_sha256: 752eaed42d6b3ebe56cfc8e7afe16125448d3ec1c35572fa3383fe294ba726ea
translation: machine
translated_at: '2026-10-24'
---
# Kafka Streams Zeitsemantik {#kafka-streams-time-semantics}

Die auf dem Google-Dataflow-Modell basierende Zeitsemantik für Stream-Processing legt fest, wie Ereignisse nach Zeit gruppiert werden. Watermarks schätzen den Fortschritt, und Trigger- sowie Accumulation-Modi steuern, wann und wie Ergebnisse ausgegeben werden.

## Wichtige Fakten {#key-facts}

- **Event Time**: Zeitpunkt, zu dem das Ereignis in der realen Welt tatsächlich stattgefunden hat
- **Processing Time**: Zeitpunkt, zu dem das Ereignis vom System beobachtet bzw. verarbeitet wird
- Beide können aufgrund von Netzwerkverzögerungen, Pufferung und dem Verhalten verteilter Systeme erheblich voneinander abweichen
- **Watermark**: Schätzung des Systems, wie weit es in der Event Time fortgeschritten ist; sinngemäß „Zum Processing-Zeitpunkt X nehme ich an, alle Ereignisse bis zur Event-Time Y gesehen zu haben“
- Watermarks sind heuristisch, sie können also falsch liegen; manche Daten können „zu spät“ eintreffen
- In Kafka Streams werden Watermarks pro Partition auf Basis der beobachteten Zeitstempel verfolgt
- **Stream Time** in Kafka Streams: maximaler Zeitstempel über alle bislang verarbeiteten Datensätze
- Die Zeitstempelvergabe wird über `message.timestamp.type` am Topic gesteuert: `CreateTime` (Standard, vom Producer gesetzt) oder `LogAppendTime` (vom Broker gesetzt)

## Muster {#patterns}

### Triggerstrategien (Dataflow-Modell) {#triggering-strategies-dataflow-model}

| Trigger | Zeitpunkt der Ausgabe |
|---------|-----------------------|
| Am Watermark | Wenn das Watermark das Ende des Fensters passiert |
| Periodisch | Alle N Sekunden Processing Time |
| Pro Element | Bei jedem neuen Element (frühe Ergebnisse) |
| Zusammengesetzt | Kombination mehrerer Strategien |

### Accumulation-Modi {#accumulation-modes}

| Modus | Verhalten | Anwendungsfall |
|-------|-----------|----------------|
| Discarding | Jeder Trigger gibt nur neue Daten seit dem letzten Trigger aus | Unabhängige Ergebnisse pro Trigger |
| Accumulating | Jeder Trigger gibt das kumulative Ergebnis aus | Laufende Summen, die nachgelagerte Ergebnisse überschreiben |
| Accumulating & Retracting | Gibt die Retraction des vorherigen Ergebnisses sowie das neue kumulative Ergebnis aus | Mehrstufige Pipelines mit nachgelagertem Grouping |

**Retractions** sind erforderlich, wenn nachgelagerte Operationen nach anderen Schlüsseln gruppieren als die Fensteroperation. Ohne Retractions zählen nachgelagerte Aggregationen Werte doppelt.

### Zeitüberschreibung in ksqlDB {#ksqldb-time-override}

```sql
-- Use any field as timestamp
CREATE STREAM events (
    event_id VARCHAR,
    event_time BIGINT,
    data VARCHAR
) WITH (
    KAFKA_TOPIC = 'events',
    VALUE_FORMAT = 'JSON',
    TIMESTAMP = 'event_time'
);

-- With custom timestamp format
WITH (TIMESTAMP = 'event_time', TIMESTAMP_FORMAT = 'yyyy-MM-dd HH:mm:ss')
```

### Begrenzte vs. unbegrenzte Daten {#bounded-vs-unbounded-data}

Das Dataflow-Modell behandelt Batch als Spezialfall von Streaming:
- **Begrenzt** (Batch): endlicher Datensatz, bekannte Größe, kann erneut verarbeitet werden
- **Unbegrenzt** (Stream): unendlich, kontinuierlich eintreffend, muss inkrementell verarbeitet werden
- Dieselben Operationen (Windowing, Triggering, Accumulation) gelten für beide

## Fallstricke {#gotchas}

- **Event Time und Processing Time können stark auseinanderlaufen**: Eine Nachricht, die um 14:00 erzeugt wird, kann durch Consumer-Lag erst um 14:30 verarbeitet werden. Wird für Aggregationen die Processing Time verwendet, entstehen falsche Ergebnisse.
- **Das Vorstellen der Systemzeit während des Testens führt zu Problemen mit der Datenaufbewahrung**: Nachrichten mit Zeitstempeln in der Zukunft vermischen sich mit aktuellen. Kein Segment kann gelöscht werden, bis die neueste Nachricht abläuft. Dadurch füllt sich die Festplatte, und das ist die häufigste Ursache für einen Absturz von Kafka.
- **`LogAppendTime` verliert die producerseitige Event Time**: Der Broker überschreibt den Zeitstempel, wodurch eventzeitbasierte Verarbeitung unmöglich wird.

## Siehe auch {#see-also}

- [[kafka-streams-windowing]] - Fenstertypen und Grace Periods
- [[kafka-streams]] - Topologie, Operationen, Aggregationen
- [Google Dataflow Model Paper](https://research.google/pubs/pub43864/)
- [Kafka Streams Time Documentation](https://kafka.apache.org/documentation/streams/concepts.html#streams_time)
