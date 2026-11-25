---
title: "Saga-Muster"
category: patterns
tags: [kafka, saga, choreography, orchestration, distributed-transactions, microservices, compensation]
level: 3
source_sha256: d019e396ab0090394153312fbd743d415e2157855d7d30cb2b7751a55da10dec
translation: machine
translated_at: '2026-10-24'
---
# Saga-Muster {#saga-pattern}

Das Saga-Muster verwaltet verteilte Transaktionen über Microservices hinweg mithilfe von Kafka, entweder per Choreographie (ereignisgesteuert, dezentral) oder per Orchestrierung (koordinatorgesteuert, zentral), mit Kompensationslogik für Rollbacks bei Fehlern.

## Wichtige Fakten {#key-facts}

- Verteilte Transaktionen über Two-Phase Commit (2PC) sind in Microservice-Architekturen langsam, komplex und fehleranfällig
- Saga ersetzt 2PC durch eine Folge lokaler Transaktionen, die jeweils Ereignisse an Kafka veröffentlichen
- Zwei Varianten: **Choreographie** (dezentral) und **Orchestrierung** (zentraler Koordinator)
- Jeder Schritt hat eine zugehörige **Kompensation** als Rollback-Aktion
- Das Debuggen verteilter Transaktionen erfordert das rückwärts gerichtete Wiedergeben des Kafka-Logs, um den Objektzustand zu rekonstruieren
- Eventual Consistency ist inhärent – starke Konsistenz erfordert verteilte Transaktionen

## Muster {#patterns}

### Choreographie-basierte Saga {#choreography-based-saga}

```php
Order Service -> "OrderCreated" event -> Kafka
  Payment Service consumes -> processes payment -> "PaymentCompleted" event -> Kafka
    Inventory Service consumes -> reserves stock -> "StockReserved" event -> Kafka
      Shipping Service consumes -> schedules delivery -> "OrderFulfilled" event -> Kafka

On failure (e.g., payment fails):
  Payment Service -> "PaymentFailed" event -> Kafka
    Order Service consumes -> compensates (cancel order)
```

- Vorteil: einfache Implementierung, vollständig entkoppelte Services
- Nachteil: schwer zu debuggen und den gesamten Transaktionsablauf zu überwachen; keine zentrale Sicht

### Orchestrierungs-basierte Saga {#orchestration-based-saga}

```php
Saga Coordinator receives "CreateOrder" command
  -> sends "ProcessPayment" to Payment Service
  <- receives "PaymentCompleted"
  -> sends "ReserveStock" to Inventory Service
  <- receives "StockReserved"
  -> sends "ScheduleDelivery" to Shipping Service
  <- receives "DeliveryScheduled"
  -> marks saga as complete

On failure:
  <- receives "StockUnavailable"
  -> sends "RefundPayment" to Payment Service (compensation)
  -> sends "CancelOrder" to Order Service (compensation)
  -> marks saga as failed
```

- Vorteil: klarer Transaktionsablauf, einfaches Debugging, zentraler Kontrollpunkt
- Nachteil: der Koordinator ist ein Single Point of Complexity; er muss selbst ausfallsicher sein

### Implementierung mit Kafka {#implementation-with-kafka}

```java
// Choreography: each service produces events on completion
@KafkaListener(topics = "order-events")
public void handleOrderEvent(OrderEvent event) {
    if (event.getType().equals("OrderCreated")) {
        try {
            processPayment(event.getOrderId());
            kafkaTemplate.send("payment-events", new PaymentCompleted(event.getOrderId()));
        } catch (Exception e) {
            kafkaTemplate.send("payment-events", new PaymentFailed(event.getOrderId(), e.getMessage()));
        }
    }
}
```

### Designüberlegungen {#design-considerations}

- **Partitionierung nach Entitätsschlüssel** (z. B. Bestell-ID) – stellt sicher, dass alle Ereignisse einer Saga in derselben Partition landen und so die Reihenfolge erhalten bleibt
- **Idempotente Kompensation** – Kompensationsaktionen müssen idempotent sein (sie können mehrfach aufgerufen werden)
- **Timeout-Behandlung** – maximale Saga-Dauer festlegen; bei Timeout automatisch kompensieren
- **Zustandsmaschine** – Saga-Zustand verfolgen (STARTED, PAYMENT_DONE, STOCK_RESERVED, COMPLETED, COMPENSATING, FAILED)

## Fallstricke {#gotchas}

- **Choreographie ist im großen Maßstab schwer zu debuggen** – es gibt keinen zentralen Ort, an dem der Saga-Status einsehbar ist; Correlation-IDs und zentrales Logging erwägen
- **Kompensation ist nicht immer möglich** – manche Aktionen sind nicht umkehrbar (versendete E-Mail, physisch versendete Lieferung); Kompensationsaktionen müssen vor der Implementierung der Saga entworfen werden
- **Eventual Consistency verwirrt Nutzer** – Zustände wie „wird verarbeitet“ anzeigen, anstatt auf den Abschluss zu warten
- **Der Orchestrator muss ausfallsicher sein** – stürzt er mitten in einer Saga ab, muss er sich erholen und fortfahren; Saga-Zustand in einer Datenbank oder einem Kafka-Topic speichern

## Siehe auch {#see-also}

- [[event-sourcing]] – Zustandsänderungen als Ereignisse für die Wiedergabe speichern
- [[cqrs-pattern]] – Command- und Query-Pfade trennen
- [[transactional-outbox]] – zuverlässige Ereignisveröffentlidung aus Services
- [[delivery-semantics]] – At-least-once plus Idempotenz für Saga-Schritte
