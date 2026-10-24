---
title: "Dépannage Kafka"
category: gotchas
tags: [kafka, troubleshooting, errors, leader-not-available, rebalancing, data-loss, duplicates]
level: 3
source_sha256: 2d6c9aa3f68fdf81ea4bed734da99e1c72d62dc16e6c4304799620bd4b851696
translation: machine
translated_at: '2026-10-24'
---
# Dépannage Kafka {#kafka-troubleshooting}

Problèmes courants de Kafka, classés par symptôme, cause racine et correctif, pour les problèmes côté producer comme côté consumer.

## Points clés {#key-facts}

- La plupart des problèmes Kafka relèvent de : délais d'élection de leader, tempêtes de rebalancing, bugs de gestion des offsets, erreurs de sérialisation ou saturation du disque
- « Leader Not Available » est l'erreur Kafka la plus courante et se résout généralement d'elle-même en quelques secondes
- L'auto-commit est la première source de perte de données pour les débutants
- La saturation du disque est la première cause de panne opérationnelle
- Les erreurs de sérialisation se propagent en cascade lorsque le schéma change sans coordination avec les consumers

## Modèles {#patterns}

### Problèmes côté producer {#producer-problems}

**Leader Not Available**
- Symptôme : erreur `LEADER_NOT_AVAILABLE` lors de la production
- Causes : le leader est tombé (élection en cours), cluster sous forte charge, nouveau topic en cours de création
- Correctif : se résout généralement seul en quelques secondes ; si cela persiste au-delà de 2 minutes, escalader vers les ops
- Protection : augmenter `retries` avec `retry.backoff.ms` ; implémenter le pattern [[transactional-outbox]]

**ACK perdu (doublons)**
- Symptôme : le même message apparaît deux fois dans le topic
- Cause : le broker stocke le message, le paquet ACK est perdu sur le réseau, le producer réessaie
- Correctif : activer le [[idempotent-producer]] (`enable.idempotence=true`) ; pour les sessions multiples : utiliser les [[kafka-transactions]]

**Batch perdu lors d'un crash du producer**
- Symptôme : des messages disparaissent silencieusement
- Cause : les batches en vol n'existent que dans la mémoire du producer ; un crash avant l'envoi entraîne une perte définitive
- Correctif : pour les données critiques, implémenter un write-ahead log (écrire dans une base locale avant l'envoi vers Kafka)

**Message trop volumineux**
- Symptôme : erreur `MSG_SIZE_TOO_LARGE`
- Cause : la valeur par défaut de `message.max.bytes` côté broker est de 1 Mo
- Correctif : augmenter à la fois la configuration du broker (`message.max.bytes`) et celle du topic (`max.message.bytes`)

### Problèmes côté consumer {#consumer-problems}

**Tempête de rebalancing**
- Symptôme : les consumers s'arrêtent et redémarrent de façon répétée ; le consumer lag augmente
- Causes : traitement supérieur à `session.timeout.ms`, démarrage lent de l'application, déploiements fréquents, instabilité réseau
- Correctif : augmenter `session.timeout.ms` et `max.poll.interval.ms` ; réduire `max.poll.records` ; utiliser CooperativeStickyAssignor

**Perte de données due à l'auto-commit**
- Symptôme : messages perdus sans erreur
- Cause : l'auto-commit se déclenche avant la fin du traitement ; le consumer plante en cours de traitement
- Correctif : `enable.auto.commit=false` ; committer manuellement après un traitement réussi

**Expiration des offsets**
- Symptôme : le consumer relit tout (ou saute directement aux derniers messages) après une indisponibilité
- Cause : inactivité supérieure à `offsets.retention.minutes` (7 jours par défaut) ; Kafka supprime les offsets stockés
- Correctif : configurer `auto.offset.reset` de manière appropriée ; envisager de stocker les offsets en dehors de Kafka

**Erreurs de sérialisation**
- Symptôme : le consumer plante lors de la désérialisation ; `SerializationException`
- Cause : schéma modifié (champ ajouté ou supprimé) sans coordination avec les consumers
- Correctif : implémenter une Dead Letter Queue pour les messages non interprétables ; utiliser le [[schema-registry]] avec des modes de compatibilité

**Écart lié à la restauration de base de données**
- Symptôme : incohérence des données après une restauration de base de données depuis une sauvegarde
- Cause : l'offset du consumer dans Kafka pointe sur la position actuelle ; les données de l'intervalle manquant ont déjà été consommées au-delà
- Correctif : réinitialiser l'offset du consumer group via la CLI ; utiliser un nouveau nom de consumer group ; ou stocker les offsets dans la base de l'application

### Problèmes de cluster {#cluster-problems}

**Saturation du disque**
- Symptôme : le broker ne peut plus écrire, il plante
- Cause : la rétention est configurée mais les segments restent ouverts plus longtemps que prévu ; l'avancement de l'horloge système crée des timestamps futurs qui empêchent la suppression
- Correctif : surveiller l'utilisation du disque (alerte à 80 %) ; ajuster `log.segment.bytes` et `log.roll.hours` pour une fermeture plus rapide des segments
- **Cause la plus fréquente de crash de Kafka** : avancer l'horloge système pendant les tests ; les messages aux timestamps futurs empêchent la suppression de tout segment

**Réduction de l'ISR**
- Symptôme : `UnderReplicatedPartitions > 0` ; pics de `IsrShrinksPerSec`
- Cause : disque lent, problèmes réseau, pauses GC, broker surchargé
- Correctif : vérifier les E/S disque, le réseau et les logs GC de la JVM ; envisager une dégradation manuelle : passer temporairement `acks` de `all` à `1`

## Pièges {#gotchas}

- **« On a mis à jour Kafka, ça ira plus vite maintenant »** : les changements de configuration d'administration sont la cause la plus fréquente des erreurs Leader Not Available en production
- **`flush()` en Python ne lève pas d'exception en cas d'échec de livraison** : il retourne le nombre de messages encore présents dans la file ; vérifier les erreurs dans le callback de livraison, et non dans la valeur de retour de `flush()`
- **La dérive d'horloge TCP casse les connexions** : si les horloges du producer et du broker divergent significativement, la validation des timestamps du handshake TCP échoue
- **Toujours implémenter une Dead Letter Queue** : il peut s'agir d'un topic Kafka, d'une table de base de données ou d'un fichier ; journaliser les octets bruts du message, et non sa forme désérialisée
- **Le client se reconnecte automatiquement en cas de panne d'un broker** : `bootstrap.servers` avec plusieurs brokers permet un failover automatique ; le rafraîchissement des métadonnées découvre les brokers encore actifs

## Voir aussi {#see-also}

- [[kafka-monitoring]] - métriques, seuils d'alerte
- [[delivery-semantics]] - modèles at-most-once, at-least-once, exactly-once
- [[consumer-groups]] - mécanique du rebalancing
- [[broker-architecture]] - rétention, segments, gestion de l'ISR
