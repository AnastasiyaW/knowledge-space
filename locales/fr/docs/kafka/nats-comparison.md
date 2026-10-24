---
title: "Comparaison de NATS"
category: reference
tags: [nats, kafka-alternative, jetstream, pub-sub, queue-groups, kv-store]
level: 4
source_sha256: 8620fbed0c175c21a9f3b2a60cbd39d6e7691a919eddbafef10658ed9a89ee78
translation: machine
translated_at: '2026-10-24'
---
# Comparaison de NATS {#nats-comparison}

NATS est un système de messagerie léger comportant trois couches (Core, JetStream, Clustering), offrant une exploitation plus simple et une latence plus faible que Kafka, au prix de garanties d'ordonnancement plus faibles et d'un écosystème plus restreint.

## Points clés {#key-facts}

- NATS Core : messagerie rapide et non persistante ; les messages sont éphémères (ni persistance, ni tampon)
- NATS JetStream : ajoute la persistance avec rejeu, la réplication par quorum et les consommateurs durables
- Format des sujets : `a.b.c.d` (séparés par des points) ; caractères génériques : `*` (un seul jeton), `>` (le reste)
- **Queue Groups** : équilibrage de charge intégré - plusieurs consommateurs s'abonnent avec le nom du queue group, chaque message n'est livré qu'à UN seul consommateur
- **Request/Response** : modèle natif via des abonnements INBOX temporaires
- Clustering : maillage + superclusters (cluster de clusters) + leaf nodes (nœuds de périphérie)
- **Key/Value Store** (table distribuée et versionnée sur JetStream) et **Object Store** (blobs adressés par contenu) intégrés
- NATS Execution Engine (Nex) : sans serveur - déploiement de fonctions JS, WebAssembly, binaires Linux

## Modèles {#patterns}

### NATS vs Kafka {#nats-vs-kafka}

| Aspect | NATS | Kafka |
|--------|------|-------|
| Modèle de base | Messagerie (éphémère par défaut) | Journal distribué (persistant par défaut) |
| Persistance | Optionnelle (JetStream) | Toujours |
| Files de travail | Queue groups intégrés | Consumer groups |
| Request/Reply | Modèle natif | Non natif |
| Store KV | Intégré | Non intégré |
| Ordonnancement | Par sujet (plus faible) | Par partition (strict) |
| Écosystème | Plus restreint | Large écosystème Apache |
| Clustering | Maillage + superclusters + leaf | Cluster de brokers + contrôleur |
| Protocole | Binaire propriétaire, léger | Binaire propriétaire, plus lourd |

### Modes d'acquittement des consommateurs JetStream {#jetstream-consumer-ack-modes}

| Mode | Comportement |
|------|----------|
| Explicit | Le consommateur acquitte chaque message ; les messages non acquittés sont redélivrés après AckWait |
| All | Acquitter le message N acquitte implicitement tous les messages jusqu'à N |
| None | Aucun acquittement requis, envoi sans suivi (fire-and-forget) |

### Quand utiliser NATS ou Kafka {#when-to-use-nats-vs-kafka}

| Exigence | Recommandation |
|-------------|---------------|
| Tolérance à la perte d'événements, débit élevé, livraison simple | NATS |
| Streaming, durabilité élevée, FIFO strict, rejeu | Kafka |
| IoT, latence ultra-faible | NATS |
| Traitement complexe, CDC, event sourcing | Kafka |
| Démarrage rapide, mise en place simple | NATS |
| Large écosystème, nombreux connecteurs | Kafka |

## Pièges courants {#gotchas}

- **Les messages NATS Core sont éphémères** - si aucun abonné n'écoute au moment de la publication, le message est perdu ; JetStream ajoute la persistance
- **L'ordonnancement NATS se fait par sujet, et non par partition** - plus faible que la garantie d'ordonnancement par partition de Kafka
- **Le KV Store a des limites** - valeur plafonnée à 1 Mo, pas de transactions entre clés
- **Les objets de l'Object Store sont immuables** - pas d'écritures partielles, accès séquentiel uniquement

## JetStream : NATS persistant {#jetstream-persistent-nats}

JetStream ajoute la persistance au-dessus de NATS Core avec une sémantique explicite pour les consommateurs :

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

## NATS comme Key/Value Store et Object Store {#nats-as-keyvalue-store-and-object-store}

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

**Limites :**
- KV : 1 Mo par valeur maximum, pas de transactions entre clés
- Object Store : objets immuables, pas d'écritures partielles

## NATS Execution Engine (Nex) {#nats-execution-engine-nex}

Couche sans serveur au-dessus de NATS - déploiement et invocation de fonctions via le routage par sujet :

- Déploiement : fonctions JavaScript, modules WebAssembly, binaires Linux natifs
- Déclenchement par n'importe quel sujet NATS (pub/sub, request-reply)
- Ordonnancement distribué sur les nœuds du cluster
- Aucune infrastructure serverless séparée nécessaire

## Voir aussi {#see-also}

- [[messaging-models]] - comparaison des modèles file, pub-sub et journal
- [[broker-architecture]] - architecture de Kafka pour comparaison
- [Documentation NATS](https://docs.nats.io/)
