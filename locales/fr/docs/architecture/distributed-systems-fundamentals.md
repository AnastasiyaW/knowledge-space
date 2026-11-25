---
title: "Fondamentaux des systèmes distribués"
category: concepts
tags: [distributed-systems, cap-theorem, consensus, replication, partitioning]
level: 3
source_sha256: 775f52252832141307b34607da29e9821156c9cfb3c9d84a2ba339093ae4319b
translation: machine
translated_at: '2026-10-24'
---
# Fondamentaux des systèmes distribués {#distributed-systems-fundamentals}

Les systèmes distribués introduisent des modes de défaillance inexistants dans les systèmes mono-processus : partitions réseau, défaillances partielles, décalage d'horloges (clock skew), réordonnancement des messages. Comprendre ces limites est indispensable pour prendre des décisions d'architecture éclairées.

## Ordres de grandeur de latence que tout ingénieur devrait connaître {#latency-numbers-every-engineer-should-know}

| Opération | Latence |
|-----------|---------|
| Accès au cache L1 | ~1 ns |
| Accès au cache L2 | ~4 ns |
| Accès à la mémoire principale | ~100 ns |
| Lecture aléatoire sur SSD | ~100 us |
| Lecture dans un cache distribué (Redis) | ~1 ms |
| Requête simple sur base de données | ~1-10 ms |
| Recherche (seek) sur HDD | ~10 ms |
| Aller-retour dans un datacenter | ~0.5 ms |
| Réseau inter-régions | ~50-150 ms |

**Point clé :** les appels réseau sont 10 000 à 1 000 000 fois plus lents qu'un accès mémoire. Cache applicatif local vs cache distribué : un écart d'un ordre de grandeur (100 ns contre 1 ms).

## Théorème CAP {#cap-theorem}

Dans un système distribué, on ne peut garantir que deux propriétés sur trois :

- **Cohérence (Consistency)** : tous les nœuds voient les mêmes données
- **Disponibilité (Availability)** : chaque requête reçoit une réponse
- **Tolérance au partitionnement (Partition tolerance)** : le système fonctionne malgré les défaillances réseau

Les partitions réseau étant inévitables, le choix réel se situe entre **CP** (cohérent, mais pouvant rejeter des requêtes pendant une partition) et **AP** (disponible, mais pouvant renvoyer des données périmées).

### Extension PACELC {#pacelc-extension}

En cas de **P**artition : choisir entre **A**disponibilité et **C**ohérence. **E**lse (fonctionnement normal) : choisir entre **L**atence et **C**ohérence. Même sans partition, il existe un compromis entre cohérence et latence.

### Implications pratiques pour la conception d'API {#practical-implications-for-api-design}
- **Privilégier la cohérence** pour : les transactions financières, la gestion des stocks
- **Privilégier la disponibilité** pour : les fils d'actualité des réseaux sociaux, les recommandations
- La plupart des systèmes ont besoin des deux à différents endroits : concevoir en conséquence

## Modèles de cohérence {#consistency-models}

| Modèle | Garantie | Cas d'usage |
|--------|----------|-------------|
| **Forte (linéarisabilité)** | Chaque lecture retourne la dernière écriture | Verrous distribués, élection de leader |
| **Causale** | Les opérations causalement liées sont vues dans l'ordre | Bon équilibre entre exactitude et performance |
| **Lecture de ses propres écritures (Read-your-writes)** | L'utilisateur voit immédiatement ses propres mises à jour | La plupart des applications web |
| **Éventuelle (Eventual)** | Les réplicas convergent avec le temps | DNS, caches CDN, compteurs de réseaux sociaux |

## Algorithmes de consensus {#consensus-algorithms}

**Problème :** comment des nœuds distribués se mettent-ils d'accord sur une valeur malgré les défaillances ?

**Raft** : basé sur un leader. Élection du leader par timeouts aléatoires. Réplication du journal vers les followers. Validation lorsque la majorité accuse réception. Conçu pour être compréhensible. Utilisé par : etcd, CockroachDB, TiKV.

**Paxos** : fondateur, prouvé mathématiquement. Complexe. Utilisé par : Google Chubby, Spanner.

**Note pratique :** le consensus est coûteux (plusieurs allers-retours). À n'utiliser que lorsqu'une forte cohérence est requise. Dans la plupart des cas, une cohérence éventuelle avec résolution de conflits suffit.

## Stratégies de réplication {#replication-strategies}

### Leader unique (Single-Leader) {#single-leader}
Un seul nœud accepte les écritures et les réplique vers les followers. Simple et cohérent. Le leader constitue un goulot d'étranglement et un SPOF. Utilisé par : la réplication en flux (streaming replication) de PostgreSQL, la réplication MySQL.

### Multi-leader {#multi-leader}
Plusieurs nœuds acceptent les écritures et se synchronisent entre eux. Meilleure disponibilité en écriture pour les systèmes géo-distribués. Difficulté : la résolution de conflits (last-writer-wins, fonctions de fusion, CRDTs).

### Sans leader (style Dynamo) {#leaderless-dynamo-style}
N'importe quel nœud accepte lectures et écritures. Basé sur des quorums : lecture R + écriture W > N réplicas. Utilisé par : Cassandra, DynamoDB, Riak. Difficulté : read repair, anti-entropy.

## Partitionnement (Sharding) {#partitioning-sharding}

Répartir les données entre plusieurs nœuds lorsqu'un seul nœud ne peut pas absorber le volume ou le débit.

### Partitionnement par clé (hachage) {#key-based-hash-partitioning}
Le hachage de la clé détermine la partition. Répartition uniforme, mais pas de requêtes par intervalle. Le hachage cohérent (consistent hashing) évite une redistribution complète lorsque les nœuds changent.

### Partitionnement par intervalle (Range) {#range-partitioning}
Des intervalles continus de clés sont affectés aux partitions. Permet les requêtes par intervalle, mais risque de points chauds (hot spots).

### Partitionnement des index secondaires {#secondary-index-partitioning}
- **Index locaux** : chaque partition indexe ses propres données (requêtes scatter-gather)
- **Index globaux** : indexés séparément (requêtes sur une seule partition, écritures plus complexes)

## Patterns de résilience {#resilience-patterns}

### Circuit Breaker {#circuit-breaker}
Éviter les défaillances en cascade en échouant rapidement lorsque le service aval est défaillant. États : Fermé -> Ouvert -> Semi-ouvert (Half-Open).

### Bulkhead (cloisonnement) {#bulkhead}
Isoler les défaillances en partitionnant les ressources (pools de threads, pools de connexions). Une défaillance dans une partition n'affecte pas les autres.

### Timeouts et réessais {#timeouts-and-retries}
- **Backoff exponentiel** : délai croissant exponentiellement : 5 s -> 25 s -> 125 s
- **Jitter** : variation aléatoire pour éviter l'effet de troupeau (thundering herd)
- Ne réessayer que les erreurs transitoires (5xx, timeouts), jamais les erreurs client (4xx)

### Dégradation gracieuse (Graceful Degradation) {#graceful-degradation}
Désactiver les fonctionnalités non critiques pour maintenir les fonctions essentielles. Feature flags pour une activation/désactivation dynamique.

## Sophismes de l'informatique distribuée (Peter Deutsch) {#fallacies-of-distributed-computing-peter-deutsch}

1. Le réseau est fiable
2. La latence est nulle
3. La bande passante est infinie
4. Le réseau est sécurisé
5. La topologie ne change pas
6. Il y a un seul administrateur
7. Le coût de transport est nul
8. Le réseau est homogène

Chaque sophisme finit par devenir un bug en production.

## Pièges à éviter {#gotchas}

- **Complexité essentielle vs accidentelle** : ne pas ajouter de complexité de système distribué sans nécessité. Commencer simple
- **Utilisation au-delà de 70-80 %** : provoque une hausse disproportionnée des temps de réponse (courbe en crosse de hockey de la théorie des files d'attente)
- **Appels réseau dans des boucles** : une boucle apparemment simple de 100 itérations peut prendre plus de 50 secondes si chaque itération implique un appel réseau
- **Décalage d'horloges (clock skew)** entre les nœuds : rend l'ordonnancement fondé sur les horodatages peu fiable sans horloges vectorielles ou horloges logiques hybrides

## Voir aussi {#see-also}

- [[queueing-theory]] - Pourquoi les systèmes se dégradent de façon non linéaire sous charge
- [[quality-attributes-reliability]] - Disponibilité, tolérance aux pannes, recouvrabilité
- [[microservices-communication]] - Patterns Saga, CQRS, event sourcing
- [[transactions-and-acid]] - Compromis ACID vs BASE dans les bases de données distribuées
