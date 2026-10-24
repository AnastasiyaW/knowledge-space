---
title: "Go"
description: "Grundlagen der Sprache Go, Nebenläufigkeitsprimitive (Goroutinen, Channels), HTTP-Server, Module, Fehlerbehandlungsmuster und Idiome für produktive Microservices."
type: MOC
level: 2
source_sha256: c357d4d8cbeb58f6590c94b0ac5c3fc66e2d2401685b26878e94b39a4973ace9
translation: machine
translated_at: '2026-10-24'
---
# Go {#go}

Go ist eine kompilierte Systemsprache für nebenläufige Netzwerkdienste: schnelle Kompilierzeiten, eine umfangreiche Standardbibliothek, erstklassige Goroutinen und Channels sowie eine minimale Oberfläche. Die Artikel behandeln das Nebenläufigkeitsmodell (Goroutinen, Channels, select, Sync-Primitive), Fehlerbehandlungsmuster, die sich von Exceptions unterscheiden, schnittstellengetriebene Komposition, das net/http-Toolkit sowie Produktionsmuster für Microservices und Datenbankzugriff. Jeder Eintrag enthält sofort einsetzbaren Code und die Stolperfalle, die man erst nach dem Deployment kennenlernt.

## Grundlagen {#fundamentals}
- [[modules-packages]] - Go-Module, Pakete, Abhängigkeitsverwaltung
- [Fehlerbehandlung](error-handling.md) - Muster der Fehlerbehandlung, Wrapping, Sentinel-Errors
- [[interfaces-composition]] - Interfaces, Embedding, Komposition statt Vererbung

## Nebenläufigkeit {#concurrency}
- [[goroutines-channels]] - Goroutinen, Channels, select, Sync-Primitive

## Web & Server {#web-servers}
- [[http-servers]] - HTTP-Server, Routing, Middleware, net/http-Muster

## Weiterführende Referenzen {#additional-references}

- [Nebenläufigkeit in Go - Goroutinen, Channels und Sync](concurrency-patterns.md) - Das Nebenläufigkeitsmodell von Go: der GMP-Scheduler, Channels, select, Synchronisationsprimitive und
- [[database-patterns]] - Produktionsmuster für Datenbanken in Go - PostgreSQL mit pgx, MongoDB mit dem offiziellen Treiber, Redis
- [[fundamentals]] - Zentrale Sprachfunktionen von Go - Typsystem, Slices, Maps, Pointer, Interfaces, Closures und Fehler
- [[microservices]] - Produktionsmuster für Go-Microservices - gRPC mit Protobuf, Clean-Architecture-Schichten, Abhängigkeiten
