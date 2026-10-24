---
title: "Enterprise Integration - ESB, Stile, Patterns"
category: concepts
tags: [integration, esb, eip, api-gateway, service-mesh, ipaas]
level: 3
source_sha256: d1df8f2a961e01e37d3544f46aa2175412051621ca735d6fb759064fad8a27c7
translation: machine
translated_at: '2026-10-24'
---
# Enterprise Integration - ESB, Stile, Patterns {#enterprise-integration-esb-styles-patterns}

Moderne Systeme arbeiten selten isoliert. Gut durchdachte Integration reduziert Latenz, verbessert die Wartbarkeit, ermöglicht Skalierbarkeit und gewährleistet Sicherheit.

## Integrationsstile {#integration-styles}

| Stil | Mechanismus | Kopplung | Latenz | Anwendungsfall |
|-------|-----------|---------|---------|----------|
| **File Transfer** | Gemeinsam genutzte Dateien (CSV, XML, JSON) | Gering | Hoch | Batch-Datenaustausch |
| **Shared Database** | Mehrere Systeme, gleiche DB | Sehr hoch | Gering | In modernen Architekturen vermeiden |
| **Remote Procedure (RPI)** | REST-, gRPC- oder SOAP-Aufrufe | Mittel | Gering | Synchrone Service-zu-Service-Kommunikation |
| **Messaging** | Message Broker (Kafka, RabbitMQ) | Gering | Mittel | Asynchrone, entkoppelte Systeme |

## Enterprise Service Bus (ESB) {#enterprise-service-bus-esb}

Middleware für zentralisierte Integration: Routing, Protokollumwandlung, Nachrichtentransformation, Orchestrierung.

**Kernfunktionen:**
- **Routing** - inhaltsbasiert, regelbasiert, dynamisch
- **Transformation** - XML zu JSON, Schema-Mapping
- **Protokollvermittlung** - SOAP zu REST, JMS zu HTTP
- **Orchestrierung** - mehrstufige Geschäftsprozesse
- **Service-Virtualisierung** - Abstraktion von Standorten und Versionen
- **Monitoring** - zentralisiertes Logging, Metriken, Auditing

**Produkte:** MuleSoft, IBM Integration Bus, Oracle Service Bus, WSO2, Microsoft BizTalk.

### ESB-Anti-Pattern {#esb-anti-pattern}
Geschäftslogik im ESB statt in Services ablegen. Der ESB sollte nur routen, transformieren und vermitteln, nicht aber Domänenlogik enthalten. Dies erzeugt einen monolithischen Engpass.

## Moderne Alternativen zum ESB {#modern-alternatives-to-esb}

### API Gateway {#api-gateway}
Einfacher als ein ESB und auf API-Management fokussiert. Rate Limiting, Authentifizierung, Routing, Transformation.
- Produkte: Kong, AWS API Gateway, Apigee, nginx

### Event-Driven Architecture {#event-driven-architecture}
Services kommunizieren über Events. Ein Event-Broker (Kafka) ersetzt das Routing des ESB. Jeder Service besitzt seine eigene Logik.

### Service Mesh {#service-mesh}
Service-zu-Service-Kommunikation auf Infrastrukturebene. Sidecar-Proxy-Muster.
- Funktionen: mTLS, Lastverteilung, Circuit Breaking, Observability
- Produkte: Istio/Envoy, Linkerd
- Keine Änderungen am Anwendungscode erforderlich

### iPaaS (Integration Platform as a Service) {#ipaas-integration-platform-as-a-service}
Cloudbasierte Integration mit vorgefertigten Konnektoren für SaaS-Anwendungen.
- Produkte: MuleSoft Anypoint, Dell Boomi, Azure Integration Services

## Enterprise Integration Patterns (EIP) {#enterprise-integration-patterns-eip}

### Routing-Patterns {#routing-patterns}
- **Content-Based Router** - Routing anhand des Nachrichteninhalts
- **Message Filter** - unerwünschte Nachrichten entfernen
- **Splitter** - zusammengesetzte Nachricht in Teile zerlegen
- **Aggregator** - zusammengehörige Nachrichten kombinieren
- **Scatter-Gather** - an mehrere Empfänger senden und Antworten aggregieren
- **Routing Slip** - dynamische Liste von Verarbeitungsschritten

### Transformations-Patterns {#transformation-patterns}
- **Envelope Wrapper** - Nachrichten für den Transport ein- bzw. auspacken
- **Content Enricher** - Daten aus einer externen Quelle ergänzen
- **Content Filter** - nicht benötigte Daten entfernen
- **Normalizer** - unterschiedliche Formate in eine kanonische Form überführen

### Fehlerbehandlung {#error-handling}
- **Dead Letter Channel** - nicht verarbeitbare Nachrichten
- **Invalid Message Channel** - fehlerhafte Nachrichten
- **Retry with Backoff** - exponentielle Wiederholungsversuche
- **Idempotent Receiver** - doppelte Nachrichten sicher verarbeiten

## Kanonisches Datenmodell {#canonical-data-model}

Standardisiertes Datenformat, in das alle Systeme übersetzen und aus dem sie übersetzen. Reduziert N-zu-N-Transformationen auf N-zu-1.

```bash
System A -> [transform to canonical] -> Canonical Format
System B -> [transform to canonical] ->     |
System C -> [transform to canonical] ->     v
                                      [transform from canonical] -> Target
```

**Abwägung:** erhöhter Wartungsaufwand, dafür vereinfacht das Hinzufügen neuer Systeme.

## Planungsprozess für Integration {#integration-planning-process}

```php
Gather requirements -> Model in UML -> Choose style -> Define formats ->
  Implement -> Test -> Deploy (return to any step for refinement)
```

**Anforderungscheckliste:** beteiligte Systeme, Datenflüsse (Richtung, Volumen, Häufigkeit), Transformationsbedarf, Fehlerbehandlung, SLA (Latenz, Verfügbarkeit), Sicherheit (Authentifizierung, Verschlüsselung, Datensensibilität).

## Idempotenz in der Integration {#idempotency-in-integration}

Operationen müssen sicher wiederholbar sein, da Nachrichten mehrfach zugestellt werden können. Eindeutige Message-IDs, Prüfung vor dem Schreiben (Check-before-Write) und Upsert-Operationen verwenden.

## Stolperfallen {#gotchas}

- **Shared Database** führt zu enger Kopplung und zu aufwendiger Abstimmung bei Schemaänderungen - in modernen Architekturen vermeiden
- **File Transfer** wirkt einfach, aber die Verwaltung von Polling, Namenskonventionen, gleichzeitigen Zugriffen und Fehlerbehandlung ist komplex
- **Der ESB wird zum monolithischen Engpass**, wenn er Geschäftslogik ansammelt
- **Service Mesh erhöht die Latenz** pro Hop (Sidecar-Proxy) - vor der Einführung messen
- **Overhead des kanonischen Modells** - die Pflege des kanonischen Formats wird zu einer Governance-Herausforderung

## Siehe auch {#see-also}

- [[microservices-communication]] - API Gateway, BFF, Saga-Patterns
- [[message-broker-patterns]] - Pub/Sub, Queue, Zustellgarantien
- [[kafka-architecture]] - Event-Streaming für Integration
- [[distributed-systems-fundamentals]] - CAP, Konsistenz, Replikation
