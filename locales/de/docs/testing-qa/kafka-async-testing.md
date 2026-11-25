---
title: "Kafka und Tests asynchroner Services"
category: patterns
tags: [kafka, async, message-queue, microservices, consumer, producer, event-driven, integration]
level: 3
source_sha256: a2b1d2380e8016b7ef15f83331baa297923048df2aa7fd30d08c24ea67b3a1a6
translation: machine
translated_at: '2026-10-24'
---
# Kafka und Tests asynchroner Services {#kafka-and-async-service-testing}

Testen asynchroner Microservices, die über Apache Kafka kommunizieren. Behandelt das Erzeugen von Testnachrichten, das Konsumieren und Validieren von Events sowie den Umgang mit eventual consistency.

## Testarchitektur für Kafka-Services {#test-architecture-for-kafka-services}

```php
Test -> API (POST /order) -> Producer -> Kafka Topic -> Consumer -> DB
                                                                    |
Test -> DB Query (verify) <-----------------------------------------+
```

Tests müssen die asynchrone Verzögerung zwischen API-Aufruf und Verarbeitung im Consumer berücksichtigen.

## Kafka-Producer in Tests {#kafka-producer-in-tests}

```python
from kafka import KafkaProducer
import json

@pytest.fixture(scope="session")
def kafka_producer(config):
    producer = KafkaProducer(
        bootstrap_servers=config.kafka_brokers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: k.encode("utf-8") if k else None,
    )
    yield producer
    producer.close()

def test_consumer_processes_order(kafka_producer, db):
    order_data = {"order_id": "test-123", "amount": 99.99, "user_id": "u1"}
    kafka_producer.send("orders", key="test-123", value=order_data)
    kafka_producer.flush()

    # Wait for consumer to process
    wait_for_condition(
        lambda: db.execute(text(
            "SELECT * FROM orders WHERE order_id = :id"
        ), {"id": "test-123"}).fetchone() is not None,
        timeout=10,
    )
```

## Kafka-Consumer in Tests {#kafka-consumer-in-tests}

```python
from kafka import KafkaConsumer

@pytest.fixture
def kafka_consumer(config):
    consumer = KafkaConsumer(
        "order-events",
        bootstrap_servers=config.kafka_brokers,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="latest",
        consumer_timeout_ms=10000,
        group_id=f"test-{uuid4()}",  # unique group per test run
    )
    yield consumer
    consumer.close()

def test_order_produces_event(api_client, kafka_consumer):
    resp = api_client.post("/api/orders", json={"item": "widget", "qty": 1})
    assert resp.status_code == 201
    order_id = resp.json()["id"]

    messages = list(kafka_consumer)
    order_events = [m.value for m in messages if m.value.get("order_id") == order_id]
    assert len(order_events) >= 1
    assert order_events[0]["event_type"] == "order_created"
```

## Hilfsfunktion für Wartebedingungen {#wait-for-condition-helper}

```python
import time

def wait_for_condition(condition_fn, timeout=10, interval=0.5, message=""):
    """Poll until condition returns truthy or timeout."""
    deadline = time.time() + timeout
    last_error = None
    while time.time() < deadline:
        try:
            result = condition_fn()
            if result:
                return result
        except Exception as e:
            last_error = e
        time.sleep(interval)
    raise TimeoutError(
        f"Condition not met within {timeout}s. {message}"
        f"{f' Last error: {last_error}' if last_error else ''}"
    )
```

## Docker Compose mit Kafka {#docker-compose-with-kafka}

```yaml
# docker-compose.test.yml
services:
  kafka:
    image: confluentinc/cp-kafka:7.5.0
    environment:
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@kafka:9093
      CLUSTER_ID: test-cluster-id
    ports:
      - "9092:9092"
    healthcheck:
      test: kafka-topics --bootstrap-server localhost:9092 --list
      interval: 10s
      timeout: 5s
      retries: 5
```

## Tests für Exactly-Once-Semantik {#testing-exactly-once-semantics}

```python
def test_duplicate_message_idempotent(kafka_producer, db):
    order = {"order_id": "dup-test", "amount": 50.0}

    # Send same message twice
    kafka_producer.send("orders", key="dup-test", value=order)
    kafka_producer.send("orders", key="dup-test", value=order)
    kafka_producer.flush()

    time.sleep(5)  # wait for consumer

    # Should have exactly one record
    count = db.execute(
        text("SELECT count(*) FROM orders WHERE order_id = :id"),
        {"id": "dup-test"}
    ).scalar()
    assert count == 1
```

## Validierung von Error-Topics {#error-topic-validation}

```python
def test_invalid_message_goes_to_dlq(kafka_producer, dlq_consumer):
    """Dead Letter Queue: invalid messages should be routed there."""
    invalid = {"order_id": None, "amount": "not-a-number"}
    kafka_producer.send("orders", value=invalid)
    kafka_producer.flush()

    messages = list(dlq_consumer)
    assert any(m.value.get("amount") == "not-a-number" for m in messages)
```

## Stolperfallen {#gotchas}

- **Problem:** Der Test-Consumer verpasst Nachrichten, weil er erst abonniert, nachdem der Producer bereits gesendet hat. **Lösung:** Den Consumer VOR dem Produzieren abonnieren. Außerdem `auto_offset_reset="earliest"` mit einer eindeutigen Consumer-Group pro Test verwenden.

- **Problem:** Tests sind instabil, weil das Kafka-Consumer-Timeout greift – die Nachricht kommt erst nach `consumer_timeout_ms` an. **Lösung:** Das Timeout für CI erhöhen (30 s und mehr). Statt sich auf `consumer_timeout_ms` zu verlassen, eine explizite Polling-Schleife mit `wait_for_condition` verwenden.

- **Problem:** Der Kafka-Container benötigt 20–30 s, bis er betriebsbereit ist, wodurch schnelle Tests fehlschlagen. **Lösung:** Eine session-scoped Fixture mit Warten auf den Healthcheck verwenden. Alternativ `testcontainers-kafka` einsetzen, das die Startwartezeiten selbst übernimmt.

## Siehe auch {#see-also}

- [[docker-test-environments]]
- [[database-testing]]
- [[api-testing-requests]]
