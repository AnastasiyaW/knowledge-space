---
title: Kafka Streams Windowing
category: concepts
tags: [kafka, streams, windowing, tumbling, hopping, session, sliding, grace-period, watermark]
---

# Kafka Streams Windowing

Windowed operations group stream records into finite time intervals for aggregation, supporting tumbling (non-overlapping), hopping (overlapping), session (gap-based), and sliding (join) windows with configurable grace periods for late-arriving events.

## Key Facts

- Windows are evaluated continuously as new records arrive
- Each record belongs to one or more windows depending on window type
- Window retention controls how many past windows are kept in state stores
- Grace period defines additional time after window closes to accept late-arriving records; after expiry, late records are dropped
- Retention must be >= window size + grace period
- **Stream time**: maximum timestamp seen so far across all processed records (not wall clock)
- Timestamp assignment controlled by `message.timestamp.type`: `CreateTime` (producer-set) or `LogAppendTime` (broker-set)

## Patterns

### Tumbling Window (Fixed, Non-Overlapping)

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

### Hopping Window (Fixed, Overlapping)

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

### Session Window (Dynamic, Gap-Based)

```java
// Sessions close after 5 minutes of inactivity
stream.groupByKey()
    .windowedBy(SessionWindows.ofInactivityGapWithNoGrace(Duration.ofMinutes(5)))
    .count();
// Sessions tracked independently per key
// Session duration varies based on actual activity patterns
```

### Sliding Window (Join Windows)

```java
// For stream-stream joins: how far apart events can be joined
KStream<String, String> joined = stream1.join(
    stream2,
    (left, right) -> left + "+" + right,
    JoinWindows.ofTimeDifferenceAndGrace(Duration.ofMinutes(5), Duration.ofMinutes(1))
);
```

### ksqlDB Windowing

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

### Time Semantics

| Time Concept | Description |
|-------------|-------------|
| Event time | When the record was created at the source |
| Ingestion time | When the broker stored the record |
| Processing time | When the stream processing app processes it |
| Stream time | Maximum timestamp seen so far |

### Timestamp Extractors

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

## Gotchas

- **Grace period default is 24 hours in ksqlDB** - this can consume significant memory; tune based on actual late-data characteristics
- **Late records after grace period are silently dropped** - no error, no DLQ; monitor dropped record metrics
- **Retention must be >= window size + grace period** - otherwise windows are evicted before they can accept late data
- **Session windows can merge** - if two sessions for the same key overlap after a late event arrives, they merge into one larger session
- **Window start times are aligned to epoch** - tumbling windows start at Unix epoch boundaries, not at application start time
- **Slow writer = open segment = retention exceeds config** - if writing is slow, segment stays open for a long time, so actual retention can be much longer than configured

## See Also

- [[kafka-streams]] - core topology, operations, joins
- [[kafka-streams-state-stores]] - state stores backing windowed aggregations
- [[kafka-streams-time-semantics]] - event time vs processing time, watermarks
- [[ksqldb]] - SQL windowing syntax
- [Kafka Streams Windowing Documentation](https://kafka.apache.org/documentation/streams/developer-guide/dsl-api.html#windowing)
