---
title: "NATS-Vergleich"
category: reference
tags: [nats, kafka-alternative, jetstream, pub-sub, queue-groups, kv-store]
level: 4
source_sha256: 8620fbed0c175c21a9f3b2a60cbd39d6e7691a919eddbafef10658ed9a89ee78
translation: machine
translated_at: '2026-10-24'
---
# NATS-Vergleich {#nats-comparison}

NATS ist ein leichtgewichtiges Messaging-System mit drei Schichten (Core, JetStream, Clustering), das einfachere Betriebsabläufe und geringere Latenz als Kafka bietet, dafür aber schwächere Reihenfolgegarantien und ein kleineres Ökosystem.

## Wichtigste Fakten {#key-facts}

- NATS Core: schnelles, nicht persistentes Messaging; Nachrichten sind flüchtig (keine Persistenz, kein Puffer)
- NATS JetStream: ergänzt Persistenz mit Replay, Quorum-Replikation, langlebigen Consumern
- Subject-Format: `a.b.c.d` (durch Punkte getrennt); Wildcards: `*` (einzelnes Token), `>` (Rest)
- **Queue Groups**: integrierter Lastausgleich – mehrere Consumer abonnieren mit einem Queue-Group-Namen, jede Nachricht wird nur an EINEN Consumer zugestellt
- **Request/Response**: natives Muster über temporäre INBOX-Subscriptions
- Clustering: Mesh + Superclusters (Cluster aus Clustern) + Leaf Nodes (Edge-Knoten)
- Integrierter **Key/Value Store** (verteilte, versionierte Map auf JetStream) und **Object Store** (inhaltsadressierte Blobs)
- NATS Execution Engine (Nex): Serverless – Deployment von JS-Funktionen, WebAssembly, Linux-Binaries

## Muster {#patterns}

### NATS vs. Kafka {#nats-vs-kafka}

| Aspekt | NATS | Kafka |
|--------|------|-------|
| Kernmodell | Messaging (standardmäßig flüchtig) | Verteiltes Log (standardmäßig persistent) |
| Persistenz | Optional (JetStream) | Immer |
| Work Queues | Integrierte Queue Groups | Consumer Groups |
| Request/Reply | Natives Muster | Nicht nativ |
| KV Store | Integriert | Nicht integriert |
| Reihenfolge | Pro Subject (schwächer) | Pro Partition (strikt) |
| Ökosystem | Kleiner | Großes Apache-Ökosystem |
| Clustering | Mesh + Superclusters + Leaf | Broker-Cluster + Controller |
| Protokoll | Eigenes Binärprotokoll, leichtgewichtig | Eigenes Binärprotokoll, schwergewichtiger |

### JetStream Consumer-Ack-Modi {#jetstream-consumer-ack-modes}

| Modus | Verhalten |
|-------|-----------|
| Explicit | Consumer bestätigt jede Nachricht; unbestätigte werden nach AckWait erneut zugestellt |
| All | Bestätigung von Nachricht N bestätigt implizit alle bis einschließlich N |
| None | Keine Bestätigungen erforderlich, Fire-and-Forget |

### Wann NATS vs. Kafka verwenden {#when-to-use-nats-vs-kafka}

| Anforderung | Empfehlung |
|-------------|---------------|
| Verlusttoleranz bei Events, hoher Durchsatz, einfache Zustellung | NATS |
| Streaming, hohe Dauerhaftigkeit, strikte FIFO-Reihenfolge, Replay | Kafka |
| IoT, extrem niedrige Latenz | NATS |
| Komplexe Verarbeitung, CDC, Event Sourcing | Kafka |
| Schneller Start, einfaches Setup | NATS |
| Großes Ökosystem, viele Konnektoren | Kafka |

## Fallstricke {#gotchas}

- **NATS-Core-Nachrichten sind flüchtig** – ist beim Veröffentlichen kein Subscriber aktiv, geht die Nachricht verloren; JetStream ergänzt Persistenz
- **NATS-Reihenfolge gilt pro Subject, nicht pro Partition** – schwächer als die Reihenfolgegarantie pro Partition bei Kafka
- **KV Store hat Grenzen** – maximal 1 MB pro Wert, keine schlüsselübergreifenden Transaktionen
- **Objekte im Object Store sind unveränderlich** – keine partiellen Schreibvorgänge, nur sequentieller Zugriff

## JetStream: persistentes NATS {#jetstream-persistent-nats}

JetStream ergänzt NATS Core um Persistenz mit expliziter Consumer-Semantik:

```go
// Connect and create JetStream context
nc, _ := nats.Connect(nats.DefaultURL)
js, _ := nc.JetStream()

// Create a stream (persistent log):
js.AddStream(&nats.StreamConfig{
    Name:     "ORDERS",
    Subjects: []string{"orders.*"},
    MaxAge:   24 * time.Hour,
    Replicas: 3,
})

// Durable consumer (survives reconnects):
js.Subscribe("orders.new", func(msg *nats.Msg) {
    // Process
    msg.Ack()  // explicit ack; unacked redelivered after AckWait
}, nats.Durable("order-processor"), nats.AckExplicit())
```

## NATS als Key/Value Store und Object Store {#nats-as-keyvalue-store-and-object-store}

```go
// KV Store (distributed, versioned):
kv, _ := js.CreateKeyValue(&nats.KeyValueConfig{
    Bucket:   "config",
    MaxBytes: 100 * 1024 * 1024,  // 100MB max
})
kv.Put("feature-flags", []byte(`{"dark_mode": true}`))
entry, _ := kv.Get("feature-flags")

// Object Store (content-addressed blobs):
obs, _ := js.CreateObjectStore(&nats.ObjectStoreConfig{
    Bucket: "artifacts",
})
obs.PutFile("model-v1.pkl", "path/to/file")
```

**Einschränkungen:**
- KV: maximal 1 MB pro Wert, keine schlüsselübergreifenden Transaktionen
- Object Store: unveränderliche Objekte, keine partiellen Schreibvorgänge

## NATS Execution Engine (Nex) {#nats-execution-engine-nex}

Serverless-Schicht auf NATS – Funktionen werden über Subject-Routing bereitgestellt und aufgerufen:

- Deployment: JavaScript-Funktionen, WebAssembly-Module, native Linux-Binaries
- Auslösung über beliebige NATS-Subjects (Pub/Sub, Request-Reply)
- Verteilte Ablaufplanung über Cluster-Knoten
- Keine separate Serverless-Infrastruktur erforderlich

## Siehe auch {#see-also}

- [[messaging-models]] - Vergleich der Modelle Queue, Pub-Sub und logbasiert
- [[broker-architecture]] - Kafkas Architektur zum Vergleich
- [NATS-Dokumentation](https://docs.nats.io/)
