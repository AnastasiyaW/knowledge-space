---
title: "Cache - Redis et Memcached"
category: concepts
tags: [sql-databases, redis, memcached, caching, cache-aside, write-through, lru, connection-cache]
level: 3
source_sha256: 2d0d8878b573a23944a17ab78f27bbf383626edbf3d2afe513de1cf0535868dc
translation: machine
translated_at: '2026-10-24'
---
# Cache - Redis et Memcached {#caching-redis-and-memcached}

Les couches de cache placées entre l'application et la base de données réduisent considérablement la charge des requêtes. Redis et Memcached sont les deux solutions dominantes, avec des compromis différents.

## Comparaison {#comparison}

| Fonctionnalité | Redis | Memcached |
|---------|-------|-----------|
| Structures de données | Chaînes, listes, ensembles, ensembles triés, hachages, flux | Chaînes clé-valeur uniquement |
| Persistance | Snapshots RDB + AOF | Aucune (RAM uniquement) |
| Threading | Commandes monothread (threads d'E/S depuis la 6.0) | Multithread |
| Taille max. d'une valeur | 512MB | 1MB |
| Pub/Sub | Oui | Non |
| Réplication | Maître-réplica | Aucune intégrée |
| Clustering | Slots de hachage (16384) | Hachage cohérent côté client |

## Modèles de cache {#cache-patterns}

**Cache-Aside (Lazy Loading) :** l'application consulte d'abord le cache. En cas d'absence (cache miss), elle interroge la base de données puis stocke le résultat dans le cache. Simple, mais la première requête atteint toujours la base de données.

**Write-Through :** l'application écrit simultanément dans le cache et dans la base de données. Le cache est toujours à jour, mais la latence d'écriture augmente.

**Write-Behind :** l'application n'écrit que dans le cache. Le cache écrit ensuite de manière asynchrone dans la base de données. Les écritures sont les plus rapides, mais il existe un risque de perte de données si le cache tombe en panne.

**Invalidation du cache :** basée sur un TTL (les données sont périmées pendant la durée du TTL), basée sur des événements (invalidation à chaque écriture) ou basée sur le versionnage.

## Durabilité de Redis {#redis-durability}

**Snapshots RDB :** `save 900 1` (snapshot si 1 clé ou plus a été modifiée en 900 s). `BGSAVE` crée un processus fils qui écrit pendant que le processus parent continue de servir les requêtes.

**AOF (Append-Only File) :**
- `appendfsync always` : le plus sûr, le plus lent
- `appendfsync everysec` : bon compromis (perte de 1 seconde au maximum)
- `appendfsync no` : c'est le système d'exploitation qui décide du moment du vidage sur disque

**Hybride (Redis 4.0+) :** RDB + AOF des modifications survenues depuis le dernier snapshot. Redémarrage rapide et perte de données minimale.

## Architecture de Memcached {#memcached-architecture}

**Allocateur par slabs :** la mémoire est pré-découpée en classes de taille (64B, 128B, 256B, ..., 1MB). Cela réduit la fragmentation. Compromis : fragmentation interne au sein des chunks.

**Éviction LRU :** par classe de slab. Lorsqu'une classe est pleine, l'élément le moins récemment utilisé de CETTE classe est évincé.

**CAS (Compare-And-Swap) :** `gets` renvoie un jeton CAS, et `cas` ne réussit que si le jeton n'a pas changé. Cela évite les mises à jour perdues.

**Distribution :** les serveurs ne se connaissent pas entre eux. Le client implémente le hachage cohérent. L'ajout d'un serveur entraîne la réaffectation d'environ 1/N des clés.

## Points clés {#key-facts}

- Redis en tant que cache : `SETEX key ttl value` pour un cache basé sur un TTL
- Redis Cluster : sharding automatique entre les nœuds, avec 16384 slots de hachage
- Memcached : multithread, mieux adapté à la mise en cache simple clé-valeur à grande échelle
- Un cache local nécessite des sticky sessions au niveau du load balancer ; un cache partagé ajoute de la latence réseau
- Le taux de succès du cache pour les URL populaires est probablement supérieur à 80 % (distribution de Pareto)

## Pièges à éviter {#gotchas}

- L'invalidation du cache est le problème le plus difficile : des données périmées peuvent provoquer des bogues subtils
- Redis est monothread : une commande lente bloque toutes les autres commandes
- Déséquilibre des classes de slabs dans Memcached : évincer des éléments de 256B ne libère pas d'espace pour des éléments de 64B
- La persistance de Redis (RDB+AOF) n'équivaut pas à une véritable sauvegarde de base de données
- La connexion au cache ajoute un saut réseau : ne mettez en cache que si le coût de la requête en base est largement supérieur au coût de la recherche dans le cache
- Cache stampede : de nombreux accès concurrents en cache miss sur une même clé atteignent simultanément la base de données

## Voir aussi {#see-also}

- [[connection-pooling]] - réduire le nombre de connexions à la base de données en complément du cache
- [[query-optimization-explain]] - optimiser les requêtes avant d'ajouter une couche de cache
- [[distributed-databases]] - lorsque le cache ne suffit plus
- [Sécurité des bases de données](database-security.md) - identifiants distincts pour l'accès au cache et à la base de données
