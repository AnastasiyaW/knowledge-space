---
title: "GraphQL-API-Design"
category: reference
tags: [graphql, api, schema, query, mutation, subscription]
level: 2
source_sha256: 957489e0b3f5a9f101ca3c21bdce7ee72e5647ac78ee4f97deb76135973503d5
translation: machine
translated_at: '2026-10-24'
---
# GraphQL-API-Design {#graphql-api-design}

GraphQL ist eine Abfragesprache und Server-seitige Laufzeitumgebung für APIs. Anders als bei REST, wo der Server die Struktur der Antwort festlegt, kann der Client bei GraphQL genau angeben, welche Felder er abrufen möchte. Ein einziger Endpunkt verarbeitet alle Operationen.

## Architektur {#architecture}

```php
Client -> GraphQL layer -> [Backend Service 1]
                        -> [Backend Service 2]
                        -> [Database]
                        -> [REST API]
```

GraphQL aggregiert Daten aus mehreren Quellen hinter einem einzigen Endpunkt und liefert nur die angeforderten Felder zurück. Protokollunabhängig, wobei HTTP POST am gebräuchlichsten ist.

## Schema (SDL) {#schema-sdl}

Das Schema ist der Vertrag zwischen Client und Server. Clients können nur Felder abfragen, die im Schema definiert sind.

```graphql
type Book {
  id: Int!
  title: String!
  pages: Int
  chapters: Int
}

type Query {
  books: [Book!]
  book(id: Int!): Book
}

type Mutation {
  createBook(title: String!, pages: Int, chapters: Int): Book!
  updateBook(id: Int!, title: String, pages: Int, chapters: Int): Book!
  deleteBook(id: Int!): Boolean!
}
```

- `!`-Suffix = nicht-nullbares Feld/Argument
- `[Book!]` = Liste nicht-nullbarer Book-Objekte
- Felder können Argumente akzeptieren: `book(id: Int!): Book`

## Drei Operationstypen {#three-operation-types}

### 1. Query (Lesen) {#1-query-read}
```graphql
query {
  country(code: "ru") {
    name
    currency
    capital
  }
}
```

### 2. Mutation (Erstellen/Aktualisieren/Löschen) {#2-mutation-createupdatedelete}
```graphql
mutation {
  createCountry(name: "Russia", currency: "RUB", capital: "Moscow") {
    name
  }
}
```

### 3. Subscription (Echtzeit) {#3-subscription-real-time}
Ereignisgesteuerte Aktualisierungen über persistente Verbindungen (typischerweise WebSockets). Der Client abonniert; der Server sendet Daten, sobald Ereignisse auftreten.

## Resolver {#resolvers}

Funktionen, die die Daten für jedes Feld abrufen. Jedes Feld hat einen Resolver, der aus unterschiedlichen Quellen (Datenbanken, REST-APIs, anderen Services) schöpfen kann. Dadurch wird eine flexible Datenaggregation aus heterogenen Backends möglich.

## Vorteile {#advantages}

- **Kein Over- oder Under-Fetching** - Der Client erhält genau das, was er anfordert
- **Einzelner Endpunkt** - eine URL für alle Operationen
- **Starkes Typsystem** - Das Schema ermöglicht IDE-Unterstützung, Validierung und Refactoring
- **Zusammenarbeit im Team** - Das Schema dient als gemeinsamer Vertrag
- **Erweiterbarkeit** - Neue Services lassen sich durch Aktualisierung der Resolver hinzufügen, ohne die API-Oberfläche zu ändern

## Nachteile {#disadvantages}

- **Schwieriges Caching** - Flexible Abfragen erschweren HTTP-Caching
- **Sicherheitsherausforderungen** - Flexible Abfragen können ohne geeignete Authentifizierung sensible Daten offenlegen
- **Performance bei großen Abfragen** - Die Kombination vieler Abfragen kann komplexe Operationen erzeugen
- **Implementierungskomplexität** - Für kleine Projekte ist der Einrichtungsaufwand höher als bei REST

## Wann einsetzen {#when-to-use}

- Komplexe, sich entwickelnde Datenanforderungen
- Mehrere Client-Plattformen (Web, Mobil, Desktop) mit unterschiedlichen Anforderungen
- Microservice-Architekturen, die Daten aus vielen Services aggregieren
- Mobile Anwendungen, bei denen die Bandbreitenoptimierung wichtig ist

## Wann nicht einsetzen {#when-not-to-use}

- Einfache CRUD-APIs
- Kleine Projekte mit geringer Datenkomplexität
- Wenn HTTP-Caching kritisch ist
- Wenn dem Team Erfahrung mit GraphQL fehlt

## Stolperfallen {#gotchas}

- **N+1-Problem** - Naive Resolver können N+1 Datenbankabfragen erzeugen. Verwenden Sie DataLoader für Batching
- **Angriffe über die Abfragetiefe** - Böswillige Clients können tief verschachtelte Abfragen senden. Implementieren Sie Grenzwerte für Abfragetiefe/-komplexität
- **Kein integrierter Datei-Upload** - Erfordert die Multipart-Request-Spezifikation oder einen separaten Endpunkt
- **Fehlerbehandlung** unterscheidet sich von REST - GraphQL liefert auch bei teilweisen Fehlern den Status 200, wobei die Fehler im Antwortkörper stehen

## Siehe auch {#see-also}

- [[http-rest-fundamentals]] - REST-API-Vergleich
- [[grpc-api]] - Alternative API-Stil für hohe Performance
- [[api-documentation-specs]] - GraphQL-Schema als Dokumentation
