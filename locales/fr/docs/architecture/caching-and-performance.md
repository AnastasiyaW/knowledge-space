---
title: "Stratégies de mise en cache et performance"
category: reference
tags: [caching, redis, memcached, cdn, performance, load-balancing]
level: 4
source_sha256: d7ce41e232514e94c8a4f6afcc746d2b125a435000b8fc1c658af62aacfd9cc0
translation: machine
translated_at: '2026-10-24'
---
# Stratégies de mise en cache et performance {#caching-strategies-and-performance}

La mise en cache est l'une des optimisations de performance les plus efficaces. Comprendre les patrons de cache, l'invalidation et l'ensemble de la hiérarchie de cache est essentiel pour les décisions d'architecture.

## Hiérarchie de cache {#cache-hierarchy}

| Couche | Latence | Portée | Exemple |
|-------|---------|-------|---------|
| Cache CPU L1/L2/L3 | 1-10 ns | Cœur/CPU unique | Matériel |
| Cache en mémoire du processus | ~100 ns | Instance unique | HashMap, Guava, Caffeine |
| Cache distribué | ~1 ms | Inter-services | Redis, Memcached |
| Cache CDN | 1-50 ms | Périphérie mondiale | CloudFlare, CloudFront |
| Cache de base de données | 1-10 ms | Base unique | Vues matérialisées |

## Patrons de cache {#cache-patterns}

### Cache-Aside (chargement paresseux) - le plus courant {#cache-aside-lazy-loading-most-common}
L'application consulte d'abord le cache. En cas d'échec (miss), elle lit depuis la base de données et alimente le cache.
- **Avantage :** simple, l'application contrôle la logique de mise en cache
- **Inconvénient :** données périmées jusqu'à l'expiration du TTL ou une invalidation explicite ; un miss = première requête lente

### Read-Through {#read-through}
Le cache se place entre l'application et la base de données. En cas de miss, **c'est le cache lui-même** qui charge les données depuis la base.
- **Avantage :** code applicatif plus simple
- **Inconvénient :** le cache doit connaître la source de données

### Write-Through {#write-through}
Chaque écriture est envoyée au cache ET à la base de données de manière synchrone.
- **Avantage :** forte cohérence, pas de données périmées
- **Inconvénient :** latence d'écriture plus élevée

### Write-Behind (Write-Back) {#write-behind-write-back}
Les écritures vont immédiatement dans le cache, puis sont vidées vers la base de données de manière asynchrone.
- **Avantage :** latence d'écriture la plus faible
- **Inconvénient :** risque de perte de données si le cache tombe en panne avant le vidage

### Refresh-Ahead {#refresh-ahead}
Rafraîchit proactivement les entrées avant leur expiration. Réduit la latence des miss pour les données très sollicitées. Nécessite de prédire les patterns d'accès.

## Stratégies d'invalidation du cache {#cache-invalidation-strategies}

| Stratégie | Mécanisme | Compromis |
|----------|-----------|-----------|
| **TTL** | Les entrées expirent après une durée fixe | Simple, mais sert des données périmées dans la fenêtre |
| **Piloté par événements** | Invalidation lors d'un changement de données (événements, CDC) | Données fraîches, mais plus complexe |
| **Clés versionnées** | Inclure la version dans la clé (`user:123:v5`) | Pas d'invalidation explicite, les anciennes entrées expirent |

### Prévention du cache stampede {#cache-stampede-prevention}
Lorsqu'une clé populaire expire, de nombreuses requêtes frappent simultanément la base de données.
- **Verrouillage** - une seule requête rafraîchit, les autres attendent
- **Expiration anticipée probabiliste** - ajouter une gigue pour que les clés expirent à des moments différents
- **Pré-calcul** - rafraîchir avant l'expiration

## Redis vs Memcached {#redis-vs-memcached}

| Fonctionnalité | Redis | Memcached |
|---------|-------|-----------|
| Types de données | Chaînes, hashes, listes, ensembles, ensembles triés, streams | Clé-valeur uniquement |
| Persistance | Snapshots RDB, journal AOF | Aucune |
| Clustering | Oui | Hachage cohérent |
| Pub/Sub | Oui | Non |
| Threading | Mono-thread (multi-thread à partir de 7.0) | Multi-thread |
| Idéal pour | Données complexes, persistance, pub/sub | Cache simple, grandes valeurs |

**Usages courants de Redis :** magasin de sessions, limitation de débit, classements, analytique temps réel.

## Mise en cache par couche {#caching-at-different-layers}

- **CDN** - ressources statiques (images, CSS, JS), en-têtes Cache-Control, ETags
- **Passerelle API** - cache des réponses API, TTL par endpoint
- **Application** - cache d'objets, cache de résultats de requêtes
- **Page/fragment** - HTML rendu pour CMS, pages produits

## Répartition de charge {#load-balancing}

### Algorithmes {#algorithms}
- **Round Robin** / **Round Robin pondéré** - répartition égale ou proportionnelle
- **Least Connections** - envoi au serveur le moins sollicité
- **IP Hash** - sessions collantes (même client, même serveur)
- **Hachage cohérent** - pour la distribution du cache

### L4 vs L7 {#l4-vs-l7}

| Couche | Niveau | Capacités |
|-------|-------|-------------|
| **L4** | TCP/UDP | Plus rapide, pas d'inspection du contenu |
| **L7** | HTTP | Routage basé sur le contenu, terminaison SSL, cache |

### Vérifications de santé {#health-checks}
- **Active** - sonder périodiquement le backend
- **Passive** - surveiller les erreurs du trafic réel
- Retirer les backends défaillants du pool

### Affinité de session {#session-affinity}
Les sessions collantes simplifient les applications avec état, mais réduisent la répartition uniforme. **Privilégier des backends sans état avec un magasin de sessions externe (Redis).**

## Liste de contrôle pour l'optimisation des performances {#performance-optimization-checklist}

1. **Profiler d'abord** - mesurer, identifier les goulots d'étranglement, optimiser ce qui a le plus d'impact
2. **Base de données** - indexation, EXPLAIN ANALYZE, résolution du N+1, pool de connexions, réplicas en lecture
3. **Pool de connexions** - réutiliser les connexions BD/HTTP, dimensionner le pool selon la concurrence
4. **Compression** - gzip/brotli pour le contenu texte (JSON, HTML, CSS, JS)
5. **Traitement asynchrone** - déporter les traitements lourds vers des files d'attente en arrière-plan, renvoyer immédiatement un identifiant de tâche

## Pièges courants {#gotchas}

- **L'invalidation de cache** est l'un des deux problèmes les plus difficiles en informatique (avec le nommage des choses)
- **Cache périmé après déploiement** - le nouveau code lit les données dans un nouveau format, le cache contient l'ancien format. Vider le cache au déploiement ou utiliser des clés versionnées
- **Préchauffage du cache** - un cache froid après redémarrage signifie que toutes les requêtes frappent la base de données. Préchauffer les clés critiques
- **Réseau du cache distribué** - 1 ms par appel Redis s'accumule. Regrouper les opérations avec des pipelines
- **Empoisonnement du cache CDN** - mettre en cache des réponses d'erreur les sert à tous les utilisateurs. Définir `Cache-Control: no-store` pour les réponses d'erreur

## Voir aussi {#see-also}

- [[distributed-systems-fundamentals]] - Ordres de grandeur de latence, réplication
- [[queueing-theory]] - Pourquoi la charge provoque une dégradation non linéaire
- [[rest-api-advanced]] - En-têtes de cache HTTP, ETag, Cache-Control
- [[quality-attributes-reliability]] - Outils de disponibilité, dont la mise à l'échelle automatique
