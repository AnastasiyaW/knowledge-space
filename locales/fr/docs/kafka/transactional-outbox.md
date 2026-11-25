---
title: "Outbox et Inbox transactionnels"
category: patterns
tags: [kafka, outbox, inbox, cdc, debezium, exactly-once, idempotent, distributed-transactions]
level: 3
source_sha256: 84ce0c95d5d38c6a7bc7d2330039f950eb34eba247ea16a71540705768e079bb
translation: machine
translated_at: '2026-10-24'
---
# Outbox et Inbox transactionnels {#transactional-outbox-and-inbox}

Le patron Transactional Outbox écrit les événements dans une table outbox au sein de la même transaction de base de données que les données métier, tandis que le patron Inbox assure l'idempotence côté consommateur grâce à des contraintes d'unicité. Ensemble, ils permettent d'atteindre un exactly-once pratique à travers les frontières des systèmes.

## Faits clés {#key-facts}

- **Problème** : comment mettre à jour une base de données ET publier un événement vers Kafka de manière atomique
- **Outbox** : écrire l'événement dans la table outbox, dans la même transaction de base de données que les données métier ; un processeur séparé publie ensuite vers Kafka
- **Inbox** : le service récepteur utilise une table inbox avec une contrainte d'unicité pour dédupliquer les messages entrants
- **Chaîne de garanties complète** : outbox (at-least-once) + file (at-least-once) + inbox (idempotence) = exactly-once pratique
- La livraison « exactly once » est impossible dans les systèmes distribués (problème des deux généraux)
- Exactly-once pratique = at-least-once + idempotence à chaque frontière
- [[kafka-connect]] avec Debezium peut remplacer les processeurs outbox/inbox personnalisés

## Patrons {#patterns}

### Outbox transactionnelle {#transactional-outbox}

```sql
-- Outbox table schema
CREATE TABLE outbox (
    id UUID PRIMARY KEY,
    aggregate_id VARCHAR NOT NULL,
    event_type VARCHAR NOT NULL,
    payload JSONB NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Within business transaction
BEGIN;
  INSERT INTO orders (id, customer_id, amount) VALUES (...);
  INSERT INTO outbox (id, aggregate_id, event_type, payload)
    VALUES (gen_random_uuid(), order_id, 'OrderCreated', '{"amount": 99.99}');
COMMIT;
```

**Processeur Outbox** (service séparé) :
1. Interroger la table outbox pour récupérer les enregistrements non traités
2. Publier vers Kafka
3. Marquer l'enregistrement comme traité après une publication réussie
4. Réessayer en cas d'échec (livraison at-least-once)

### Inbox transactionnelle {#transactional-inbox}

```sql
-- Inbox table schema
CREATE TABLE inbox (
    message_id UUID PRIMARY KEY,  -- unique constraint prevents duplicates
    processed_at TIMESTAMP DEFAULT NOW()
);

-- Consumer processing
BEGIN;
  INSERT INTO inbox (message_id) VALUES (:kafka_message_id);
  -- If unique constraint violation -> already processed, skip
  UPDATE balances SET amount = amount + :delta WHERE account_id = :id;
COMMIT;
```

### Architecture complète {#complete-architecture}

```php
App/1 -> DB1 [Data + Outbox]
    -> Outbox Processor -> Kafka
    -> Inbox Processor -> DB2 [Data + Inbox] -> App/2

Guarantee chain at each boundary:
  App -> DB: single transaction (atomic)
  DB -> Kafka: at-least-once (outbox processor retries)
  Kafka -> Consumer: at-least-once (consumer acks)
  Consumer -> DB: idempotent (inbox unique constraint)
```

### CDC comme alternative à l'outbox {#cdc-as-outbox-alternative}

Plutôt qu'une table outbox explicite, on capture les modifications à partir du WAL de la base de données :

| Approche | Niveau d'intrusion | Charge sur la BD |
|----------|--------------------|------------------|
| Horodatages/versions sur les lignes | Importante (modifications de schéma) | Requêtes supplémentaires |
| Triggers sur les tables | Mineure (transparente pour l'application) | Opérations supplémentaires |
| CDC basé sur le WAL (Debezium) | **Aucun** | **Aucune** |

```json
// Debezium CDC connector
{
  "name": "outbox-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "localhost",
    "database.dbname": "mydb",
    "table.include.list": "public.outbox",
    "transforms": "outbox",
    "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter"
  }
}
```

CDC basé sur le WAL : aucune intrusion dans l'application ni dans le schéma, aucune charge supplémentaire sur la base de données, et capture de toutes les modifications, y compris celles effectuées par d'autres outils ou processus.

## Pièges {#gotchas}

- **Plantage du processeur outbox = at-least-once, pas exactly-once** : si le processeur publie puis plante avant de marquer l'enregistrement comme traité, il republiera au redémarrage ; l'inbox côté consommateur est alors indispensable
- **La table outbox grossit** : elle nécessite un nettoyage périodique (suppression des enregistrements traités) ; on peut aussi utiliser le CDC pour lire l'outbox via le WAL plutôt que par interrogation
- **Le CDC nécessite toujours une inbox côté consommateur** : la capture WAL est at-least-once ; le consommateur doit dédupliquer
- **Debezium nécessite un replication slot** (PostgreSQL) : surveiller le retard du slot ; un retard croissant fait grossir la rétention du WAL, qui peut épuiser le disque

## Voir aussi {#see-also}

- [[kafka-transactions]] - exactly-once au sein de Kafka (sans systèmes externes)
- [[delivery-semantics]] - at-most-once, at-least-once, exactly-once
- [[kafka-connect]] - connecteur Debezium pour le CDC
- [[cqrs-pattern]] - CQRS utilise le patron outbox pour une publication fiable des événements
- [Documentation Debezium](https://debezium.io/documentation/)
