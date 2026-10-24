---
title: "Go"
description: "Fondamentaux du langage Go, primitives de concurrence (goroutines, canaux), serveurs HTTP, modules, patterns de gestion des erreurs et idiomes de microservices en production."
type: MOC
level: 2
source_sha256: c357d4d8cbeb58f6590c94b0ac5c3fc66e2d2401685b26878e94b39a4973ace9
translation: machine
translated_at: '2026-10-24'
---
# Go {#go}

Go est un langage compilé conçu pour les services réseau concurrents : temps de compilation rapides, bibliothèque standard riche, goroutines et canaux de première classe, et surface d'API minimale. Les articles couvrent le modèle de concurrence (goroutines, canaux, select, primitives de synchronisation), les idiomes de gestion des erreurs qui diffèrent des exceptions, la composition pilotée par les interfaces, la boîte à outils net/http, ainsi que les patterns de production pour les microservices et l'accès aux bases de données. Chaque entrée propose du code prêt à copier-coller, accompagné du piège que l'on ne découvre qu'après la mise en production.

## Fondamentaux {#fundamentals}
- [[modules-packages]] - Modules Go, paquets, gestion des dépendances
- [Gestion des erreurs](error-handling.md) - Patterns de gestion des erreurs, encapsulation, erreurs sentinelles
- [[interfaces-composition]] - Interfaces, embedding, composition plutôt qu'héritage

## Concurrence {#concurrency}
- [[goroutines-channels]] - Goroutines, canaux, select, primitives de synchronisation

## Web & serveurs {#web-servers}
- [[http-servers]] - Serveurs HTTP, routage, middleware, patterns net/http

## Références complémentaires {#additional-references}

- [Concurrence en Go - Goroutines, canaux et synchronisation](concurrency-patterns.md) - Le modèle de concurrence de Go : l'ordonnanceur GMP, canaux, select, primitives de synchronisation, et
- [[database-patterns]] - Patterns de bases de données en production avec Go - PostgreSQL avec pgx, MongoDB avec le driver officiel, Redis
- [[fundamentals]] - Fonctionnalités de base du langage Go - système de types, slices, maps, pointeurs, interfaces, closures, et erreurs
- [[microservices]] - Patterns de microservices Go en production - gRPC avec protobuf, couches d'architecture propre, dépendances
