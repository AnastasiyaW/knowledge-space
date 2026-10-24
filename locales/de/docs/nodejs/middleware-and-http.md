---
title: "Middleware und HTTP"
category: concepts
tags: [nodejs, middleware, http, fastify, express, transport, static-files]
level: 3
source_sha256: 2ef1ee37fedebc5d5cba67ade6f2c293c864d7177767ac123af825e1b37a75e8
translation: machine
translated_at: '2026-10-24'
---
# Middleware und HTTP {#middleware-and-http}

Die HTTP-Verarbeitung in Node.js reicht von reinen Node.js-Servern bis hin zu framework-basierten Ansätzen (Fastify, NestJS, Metarhia). Middleware implementiert das Chain-of-Responsibility-Muster, und die Transport-Abstraktion ermöglicht den Wechsel zwischen HTTP und WebSocket, ohne die Geschäftslogik zu verändern.

## Key Facts {#key-facts}

- Middleware in Express/Fastify ist Chain of Responsibility: Jeder Handler entscheidet, ob er die Anfrage verarbeitet oder an `next()` weitergibt
- Transport-Abstraktion: HTTP- und WebSocket-Handler teilen sich die Domänenlogik und unterscheiden sich nur im Datentransport
- Auslieferung statischer Dateien: Vor dem Senden immer die Existenz der Datei prüfen (404 vs. 500)
- Dieselbe Anwendung, implementiert in Pure Node.js, Fastify, NestJS und Metarhia, zeigt: Die Domänenlogik ist identisch, nur das Framework-Boilerplate unterscheidet sich

## Patterns {#patterns}

### Multi-Framework-Vergleich {#multi-framework-comparison}

```javascript
metatech-university/
  NodeJS-Pure/         # Pure Node.js (no framework)
  NodeJS-Fastify/      # Fastify - lightweight, good DX
  NodeJS-Nest/         # NestJS - enterprise-grade, TypeScript-first
  NodeJS-Metarhia/     # Metarhia - schema-driven, transport-abstracted

All implement: user registration, authentication, session management,
messaging, file upload, room management, push notifications
```

### Transport-Konfiguration umschalten {#transport-config-switching}

```js
// config.js
module.exports = { transport: 'ws' }; // or 'http'

// main.js - load transport module dynamically
const transport = require(`./${config.transport}.js`);
// Enables: per-environment transport, A/B testing, fallback mechanisms
```

### Gemeinsame ESLint-Konfiguration {#eslint-shared-configuration}

```javascript
eslint-config-metarhia/     # Shared rules package
  index.js                  # Rules in JavaScript (not JSON)
  browser.js                # Browser-specific overrides
  node.js                   # Node-specific overrides
```

Jedes Projekt erweitert die gemeinsame Konfiguration und überschreibt bei Bedarf einzelne Teile. Zentrale Regelverwaltung bei gleichzeitiger Flexibilität pro Repository.

## Gotchas {#gotchas}

- Ein reiner Node.js-Server ist wenig Code, aber im großen Maßstab schwer zu warten
- Die Wahl des Frameworks ist weniger wichtig als die Qualität der Architektur – alle Frameworks können dasselbe Ergebnis liefern
- Der Pull-Request-Workflow für Infrastruktur-Bibliotheken sollte die Struktur stabilisieren, bevor Tests geschrieben werden (vermeidet Test-Churn)

## See Also {#see-also}

- [[application-architecture]] - Transport-Abstraktion, geschichtete Server-Architektur
- [Design Patterns (GoF) in JavaScript](design-patterns-gof.md) - Chain of Responsibility als Middleware-Muster
- [Error Handling](error-handling.md) - Fehlerbehandlung in Request-Pipelines
