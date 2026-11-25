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

MirrorMaker 2 (MM2) réplique des topics entre clusters Kafka à des fins de reprise après sinistre et de distribution géographique. Il repose sur Kafka Connect et prend en charge la réplication active-active, la synchronisation automatique des offsets et le renommage des topics.

## Points clés {#key-facts}

- Introduit dans Kafka 2.4, construit sur [[kafka-connect]]
- Utilise le même protocole consumer que les consumers classiques (peu coûteux à mettre en œuvre)
- Prend en charge les modèles de réplication active-passive et active-active
- Active-active : réplication bidirectionnelle avec préfixes de nommage des topics (par exemple `DC1.orders`, `DC2.orders`)
- Prévention des cycles par préfixage des topics et/ou filtrage des messages basé sur les headers
- Synchronisation automatique des offsets entre clusters
- La latence de réplication implique une cohérence éventuelle entre clusters
- La réplication utilise le même protocole que les lectures des consumers

## Modèles de déploiement {#patterns}

### Active-passive (veille pour reprise après sinistre) {#active-passive-dr-standby}

```php
DC1 (primary)  --MM2-->  DC2 (standby)
  writes + reads           receives replicated data
                           on DC1 failure: failover to DC2
```

Plus simple, mais gaspille les ressources de veille.

### Active-active (distribution géographique) {#active-active-geo-distribution}

```rust
DC1 <--MM2--> DC2 (bidirectional)
  DC1 clients use DC1.* topics
  DC2 clients use DC2.* topics
  On DC loss: ~zero data loss, clients switch to surviving DC
```

Nommage des topics : `DC1.orders`, `DC2.orders` pour éviter les boucles de réplication.

### Configuration de MirrorMaker 2 {#mirrormaker-2-configuration}

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

## Pièges à éviter {#gotchas}

- **Le nommage des topics avec préfixes n'est pas idéal en active-active** : les clients doivent connaître les noms de topics propres à chaque datacenter ; alternatives : mapping de subjects ou couches de routage
- **Latence de réplication = cohérence éventuelle** : les données du DC2 peuvent accuser un retard de quelques secondes à quelques minutes par rapport au DC1
- **La prévention des cycles est essentielle** : sans elle, les messages se répliquent indéfiniment entre clusters ; utilisez des préfixes ou un filtrage basé sur les headers
- **Surveillez la latence de réplication entre clusters** : une latence croissante indique un problème réseau ou de capacité

## Voir aussi {#see-also}

- [[kafka-connect]] - MM2 est construit sur le framework Connect
- [[kafka-backup-and-dr]] - planification de la reprise après sinistre et procédures de bascule
- [[broker-architecture]] - architecture du cluster
- [Documentation Apache Kafka MirrorMaker](https://kafka.apache.org/documentation/#georeplication)
