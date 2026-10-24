---
title: "Sémantique temporelle de Kafka Streams"
category: concepts
tags: [kafka, streams, event-time, processing-time, watermark, dataflow-model, late-data]
level: 2
source_sha256: 752eaed42d6b3ebe56cfc8e7afe16125448d3ec1c35572fa3383fe294ba726ea
translation: machine
translated_at: '2026-10-24'
---
# Sémantique temporelle de Kafka Streams {#kafka-streams-time-semantics}

La sémantique temporelle du traitement de flux, fondée sur le modèle Google Dataflow, définit la manière dont les événements sont regroupés selon le temps. Les watermarks estiment la progression du traitement, tandis que les modes de déclenchement et d'accumulation contrôlent le moment et la manière dont les résultats sont émis.

## Points clés {#key-facts}

- **Event time** : moment où l'événement s'est réellement produit dans le monde réel
- **Processing time** : moment où l'événement est observé ou traité par le système
- Ces deux temps peuvent différer considérablement en raison des délais réseau, de la mise en mémoire tampon et du comportement des systèmes distribués
- **Watermark** : estimation par le système de sa progression en event time ; « au processing time X, je considère avoir vu tous les événements jusqu'à l'event time Y »
- Les watermarks sont heuristiques : ils peuvent être erronés, et certaines données peuvent arriver « en retard »
- Dans Kafka Streams, les watermarks sont suivis par partition, à partir des horodatages observés
- **Stream time** dans Kafka Streams : horodatage maximal observé jusqu'ici parmi tous les enregistrements traités
- L'attribution des horodatages est contrôlée par `message.timestamp.type` sur le topic : `CreateTime` (valeur par défaut, définie par le producteur) ou `LogAppendTime` (définie par le broker)

## Patterns {#patterns}

### Stratégies de déclenchement (modèle Dataflow) {#triggering-strategies-dataflow-model}

| Déclencheur | Moment d'émission des résultats |
|-------------|---------------------------------|
| Au watermark | Lorsque le watermark dépasse la fin de la fenêtre |
| Périodique | Toutes les N secondes de processing time |
| Par élément | À chaque nouvel élément (résultats anticipés) |
| Composite | Combinaison de plusieurs stratégies |

### Modes d'accumulation {#accumulation-modes}

| Mode | Comportement | Cas d'usage |
|------|--------------|-------------|
| Discarding | Chaque déclenchement n'émet que les nouvelles données depuis le déclenchement précédent | Résultats indépendants par déclenchement |
| Accumulating | Chaque déclenchement émet le résultat cumulé | Totaux glissants, écrasement en aval |
| Accumulating & Retracting | Émet la rétractation du résultat précédent, puis le nouveau cumul | Pipelines multi-étapes avec regroupement en aval |

**Les rétractations** sont nécessaires lorsque les opérations en aval regroupent selon des clés différentes de celles de l'opération à fenêtrage. Sans rétractations, les agrégations en aval comptent les données en double.

### Surcharge du temps dans ksqlDB {#ksqldb-time-override}

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

### Données bornées et non bornées {#bounded-vs-unbounded-data}

Le modèle Dataflow considère le batch comme un cas particulier du streaming :
- **Bornées** (batch) : jeu de données fini, de taille connue, pouvant être retraité
- **Non bornées** (flux) : infinies, arrivant en continu, doivent être traitées de manière incrémentale
- Les mêmes opérations (fenêtrage, déclenchement, accumulation) s'appliquent aux deux

## Pièges {#gotchas}

- **Event time et processing time peuvent diverger fortement** : un message produit à 14h00 peut être traité à 14h30 à cause du retard du consumer ; agréger selon le processing time produit des résultats incorrects
- **Faire avancer l'horloge système pendant les tests provoque des problèmes de rétention des données** : les messages dont l'horodatage est dans le futur se mélangent aux messages actuels ; aucun segment ne peut être supprimé tant que le message le plus récent n'a pas expiré ; le disque se remplit, et c'est la cause la plus fréquente de plantage de Kafka
- **`LogAppendTime` fait perdre l'event time défini côté producteur** : le broker écrase l'horodatage, ce qui rend impossible le traitement en event time

## Voir aussi {#see-also}

- [[kafka-streams-windowing]] - types de fenêtres et périodes de grâce
- [[kafka-streams]] - topologie, opérations, agrégations
- [Article sur le modèle Dataflow de Google](https://research.google/pubs/pub43864/)
- [Documentation sur le temps dans Kafka Streams](https://kafka.apache.org/documentation/streams/concepts.html#streams_time)
