---
title: "MirrorMaker 2"
category: reference
tags: [kafka, mirrormaker, replication, cross-cluster, disaster-recovery, active-active, active-passive]
level: 3
source_sha256: 83274fbf2d6ce038ab983cf7563f7b3b489bbe06fe69736147812e16b5f18d04
translation: machine
translated_at: '2026-10-24'
---
# MirrorMaker 2 {#mirrormaker-2}

MirrorMaker 2 (MM2) repliziert Topics zwischen Kafka-Clustern für Disaster Recovery und geografische Verteilung. Es basiert auf Kafka Connect und unterstützt Active-Active-Betrieb, automatische Offset-Synchronisation und das Umbenennen von Topics.

## Key Facts {#key-facts}

- Eingeführt in Kafka 2.4, basiert auf [[kafka-connect]]
- Verwendet dasselbe Consumer-Protokoll wie reguläre Consumer (geringer Implementierungsaufwand)
- Unterstützt Active-Passive- und Active-Active-Replikationsmuster
- Active-Active: bidirektionale Replikation mit Topic-Namenspräfixen (z. B. `DC1.orders`, `DC2.orders`)
- Zyklenvermeidung durch Topic-Präfixe und/oder headerbasierte Nachrichtenfilterung
- Automatische Offset-Synchronisation zwischen Clustern
- Replikationslatenz bedeutet eventuelle Konsistenz zwischen den Clustern
- Replikation verwendet dasselbe Protokoll wie Consumer-Lesezugriffe

## Patterns {#patterns}

### Active-Passive (DR Standby) {#active-passive-dr-standby}

```php
DC1 (primary)  --MM2-->  DC2 (standby)
  writes + reads           receives replicated data
                           on DC1 failure: failover to DC2
```

Einfacher, verschwendet aber Ressourcen im Standby-Betrieb.

### Active-Active (Geo-Distribution) {#active-active-geo-distribution}

```rust
DC1 <--MM2--> DC2 (bidirectional)
  DC1 clients use DC1.* topics
  DC2 clients use DC2.* topics
  On DC loss: ~zero data loss, clients switch to surviving DC
```

Topic-Benennung: `DC1.orders`, `DC2.orders`, um Replikationsschleifen zu verhindern.

### MirrorMaker 2 Configuration {#mirrormaker-2-configuration}

```properties
# Source cluster
clusters = DC1, DC2
DC1.bootstrap.servers = dc1-kafka:9092
DC2.bootstrap.servers = dc2-kafka:9092

# Replication flows
DC1->DC2.enabled = true
DC2->DC1.enabled = true

# Topic filtering
DC1->DC2.topics = .*
DC2->DC1.topics = .*

# Consumer group offset sync
sync.group.offsets.enabled = true
```

## Gotchas {#gotchas}

- **Topic-Benennung mit Präfixen ist für Active-Active nicht ideal** - Clients müssen die rechenzentrumsspezifischen Topic-Namen kennen; Alternativen: Subject Mapping oder Routing-Schichten
- **Replikationsverzögerung = eventuelle Konsistenz** - Daten in DC2 können DC1 um Sekunden bis Minuten hinterherhinken
- **Zyklenvermeidung ist kritisch** - ohne sie werden Nachrichten endlos zwischen den Clustern repliziert; Präfixe oder headerbasierte Filterung verwenden
- **Replikationsverzögerung zwischen Clustern überwachen** - wachsende Verzögerung deutet auf Netzwerk- oder Kapazitätsprobleme hin

## See Also {#see-also}

- [[kafka-connect]] - MM2 basiert auf dem Connect-Framework
- [[kafka-backup-and-dr]] - DR-Planung und Failover-Verfahren
- [[broker-architecture]] - Cluster-Architektur
- [Apache Kafka MirrorMaker Documentation](https://kafka.apache.org/documentation/#georeplication)
