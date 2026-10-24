---
title: "Plongée technique dans le rééquilibrage"
category: concepts
tags: [kafka, rebalancing, heartbeat, session-timeout, cooperative, static-membership]
level: 4
source_sha256: eb6d7db9789e65e36f8dbfae202e50b8caf45d50942165e6d8a7f2166a910d1a
translation: machine
translated_at: '2026-10-24'
---
# Plongée technique dans le rééquilibrage {#rebalancing-deep-dive}

Le rééquilibrage est le processus de redistribution des affectations de partitions entre les consommateurs d'un groupe, déclenché par des changements d'appartenance au groupe. C'est à la fois le mécanisme de tolérance aux pannes de Kafka et sa principale source de pics de latence côté consommateur.

## Points clés {#key-facts}

- Chaque consommateur envoie un heartbeat au **coordinateur de groupe** (un broker désigné) toutes les `heartbeat.interval.ms` (3000 ms par défaut)
- Si aucun heartbeat n'est reçu dans un délai de `session.timeout.ms` (10000 ms par défaut pour Java, 45000 ms pour librdkafka), le consommateur est déclaré mort
- Le heartbeat s'exécute dans un **thread séparé** du traitement des messages
- `max.poll.interval.ms` (300000 ms par défaut, soit 5 min) : délai maximal entre deux appels à `poll()` ; le dépasser déclenche un rééquilibrage
- Déclencheurs de rééquilibrage : arrivée ou départ d'un consommateur, changements d'abonnement, changements du nombre de partitions
- Ne se déclenche PAS lorsqu'un consommateur est en pause (`.pause()`) : le consommateur en pause continue d'envoyer ses heartbeats

## Patterns {#patterns}

### Réglage du heartbeat {#heartbeat-tuning}

```properties
# Recommended settings to avoid unnecessary rebalances
heartbeat.interval.ms=3000          # 1/3 of session.timeout.ms
session.timeout.ms=10000            # 10s for consumer failure detection
max.poll.interval.ms=300000         # 5 min for long processing
max.poll.records=100                # reduce batch size if processing is slow
```

Règle : `heartbeat.interval.ms = session.timeout.ms / 3`. Cela laisse au consommateur trois occasions d'envoyer un heartbeat avant d'être déclaré mort.

### Rééquilibrage coopératif (recommandé) {#cooperative-rebalancing-recommended}

```java
// Java - incremental cooperative rebalancing
props.put("partition.assignment.strategy",
    "org.apache.kafka.clients.consumer.CooperativeStickyAssignor");
```

Le rééquilibrage coopératif ne révoque et ne réaffecte que les partitions concernées. Les autres partitions continuent d'être consommées sans interruption.

### Appartenance statique au groupe {#static-group-membership}

```java
// Java - static membership
props.put("group.instance.id", "consumer-host-1");
// Consumer keeps its assignment across restarts
// No rebalance triggered on temporary disconnect
```

Risque : si un consommateur plante, sa partition reste non lue jusqu'à son redémarrage (ou jusqu'à l'expiration de `session.timeout.ms` pour les membres non statiques).

### Listener de rééquilibrage {#rebalance-listener}

```java
// Java - track rebalance events
consumer.subscribe(List.of("orders"), new ConsumerRebalanceListener() {
    @Override
    public void onPartitionsRevoked(Collection<TopicPartition> partitions) {
        // Commit offsets for revoked partitions
        consumer.commitSync(currentOffsets(partitions));
        // Clean up any in-memory state
    }

    @Override
    public void onPartitionsAssigned(Collection<TopicPartition> partitions) {
        // Initialize state for newly assigned partitions
        for (TopicPartition tp : partitions) {
            seekToStoredOffset(tp);
        }
    }
});
```

### Déclencheurs et non-déclencheurs de rééquilibrage {#rebalance-triggers-and-non-triggers}

| Événement | Déclenche un rééquilibrage ? |
|-------|-------------------|
| Un consommateur rejoint le groupe | Oui |
| Un consommateur quitte le groupe ou plante | Oui |
| Un consommateur modifie son abonnement | Oui |
| Le nombre de partitions augmente | Oui |
| Consommateur en pause (`.pause()`) | Non |
| Traitement lent du consommateur (dans `max.poll.interval.ms`) | Non |
| Le consommateur dépasse `max.poll.interval.ms` | Oui |

## Pièges {#gotchas}

- **Tempête de rééquilibrages** : les consommateurs arrêtent et redémarrent la lecture en boucle. Causes : traitement plus long que `session.timeout.ms`, démarrage lent de l'application, déploiements fréquents, instabilité réseau. Remède : augmenter les délais, réduire la taille des lots, utiliser CooperativeStickyAssignor
- **Arrêt total de la lecture pendant un rééquilibrage eager** : avec le protocole eager par défaut, TOUS les consommateurs du groupe arrêtent de lire pendant le rééquilibrage. Des applications à démarrage lent aggravent le problème
- **Traitement long + délai court = boucle de rééquilibrage infinie** : le consommateur traite un lot, dépasse `max.poll.interval.ms`, est exclu, rejoint le groupe, reçoit le même lot, et dépasse à nouveau le délai
- **Mélanger les stratégies d'affectation provoque un rééquilibrage global** : tous les consommateurs d'un groupe doivent utiliser la même stratégie d'affectation des partitions

## Voir aussi {#see-also}

- [[consumer-groups]] - mécanique des groupes et stratégies d'affectation
- [[consumer-configuration]] - tous les paramètres de configuration du consommateur avec leurs valeurs par défaut
- [[kafka-monitoring-and-tuning]] - surveillance de la fréquence des rééquilibrages
- [KIP-429 : Kafka Consumer Incremental Rebalance Protocol](https://cwiki.apache.org/confluence/display/KAFKA/KIP-429%3A+Kafka+Consumer+Incremental+Rebalance+Protocol)
