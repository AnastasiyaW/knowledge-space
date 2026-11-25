---
title: "Dependency Injection und Kopplung"
category: concepts
tags: [nodejs, dependency-injection, coupling, modules, layer-isolation, di]
level: 2
source_sha256: 333d88eefe170443e5788bd980aa8bb8e91d0b57fccd22d66364a188d1598228
translation: machine
translated_at: '2026-10-24'
---
# Dependency Injection und Kopplung {#dependency-injection-and-coupling}

Kopplung entsteht immer dann, wenn ein Modul Methoden eines anderen Moduls aufruft, Instanzen daraus erzeugt oder auf Eigenschaften der Entitäten eines anderen Moduls lesend bzw. schreibend zugreift. In JavaScript lassen sich viele traditionelle DI-Muster durch das Modulsystem selbst ersetzen. Die Schichtenisolation über sichere Schnittstellen und unidirektionale Kommunikation verhindert, dass Kopplung unbeherrschbar wird.

## Wichtige Fakten {#key-facts}

- **Kopplung** entsteht, wenn ein Modul: die Methode eines anderen aufruft, eine Instanz eines anderen erzeugt, auf Eigenschaften eines anderen lesend/schreibend zugreift
- Der JavaScript-Modul-Cache garantiert eine einzige Instanz pro `require()`/`import` – ein eingebautes Singleton
- Jede Abhängigkeit (import, require, API-Aufruf) erhöht die Kopplung – daher minimieren
- Faustregel: Keine Metaprogrammierung in TypeScript – meta-lastige Bibliotheken in JS schreiben und `.d.ts`-Deklarationen bereitstellen

## Modulsystem als DI {#module-system-as-di}

| Traditionelles DI | JS-Modul-Äquivalent |
|-------------------|---------------------|
| Singleton-Container | Modul-Cache (`require()` liefert dieselbe Instanz) |
| Strategie-Injection | Exportierte Objekte/Maps aus Modulen |
| Konfigurations-Injection | Konfigurationsobjekt exportieren, dort importieren, wo benötigt |
| Factory-Injection | Factory-Funktionen exportieren |
| Constructor-Injection | Modulreferenzen als Konstruktorparameter übergeben |

## Muster {#patterns}

### Schichtenisolation {#layer-isolation}

Schichten sollten über sichere Schnittstellen (Verträge) interagieren:
- **Unidirektional:** Schicht A ruft Schicht B auf, aber nicht umgekehrt
- **Bidirektional:** Beide Schichten rufen einander auf (Events/Callbacks verwenden, um zirkuläre Abhängigkeiten zu vermeiden)

Strukturelle Muster zur Isolation: [Design Patterns (GoF) in JavaScript](design-patterns-gof.md) (Schnittstellen anpassen), Proxy (Zugriff steuern), Facade (Subsystem vereinfachen), Composite (einheitliches Durchlaufen von Bäumen).

### Plattformabstraktion {#platform-abstraction}

Plattformspezifische APIs abstrahieren, damit Implementierungen austauschbar sind:

```js
// Storage abstraction - works on server and browser
const createStorage = (backend) => ({
  async read(key) { return backend.get(key); },
  async write(key, value) { return backend.set(key, value); },
});

// Server: filesystem or S3
const serverStorage = createStorage(new S3Backend(config));
// Browser: OPFS, IndexedDB, or Cache API
const browserStorage = createStorage(new OPFSBackend());
```

Abstrahieren lassen sich: Netzwerkprotokolle (HTTP, WebSocket, gRPC), Datenbanken (PostgreSQL, MongoDB), Kryptografie-Provider, Dateispeicher (lokal, S3, OPFS, IndexedDB), Benachrichtigungsdienste.

### Schemagesteuerte Entwicklung {#schema-driven-development}

Zuerst Schemas definieren, daraus alles generieren:
- Datenbanktabellen
- API-Validatoren
- TypeScript-Typen
- Dokumentation
- Client-SDKs

Schemas als einzige Quelle der Wahrheit verhindern Abweichungen zwischen den Schichten.

## Stolperfallen {#gotchas}

- Singletons über den Modul-Cache bedeuten, dass Mutationen exportierter Objekte überall sichtbar sind – das kann Feature oder Fehler sein
- Zirkuläre Abhängigkeiten funktionieren in CJS (teilweise geladenes Modul wird zurückgegeben), verursachen aber subtile Initialisierungsprobleme
- Überkonstruiertes DI in JavaScript führt zu Java-artigem Boilerplate ohne deren Vorteile – zuerst Module verwenden, DI-Container nur greifen, wenn das Modulsystem nicht ausreicht

## Siehe auch {#see-also}

- [[modules-and-packages]] - CommonJS vs. ESM, Verhalten des Modul-Cache
- [[application-architecture]] - wie DI in eine geschichtete Server-Architektur passt
- [[solid-and-grasp]] - Dependency-Inversion-Prinzip
- [[data-access-patterns]] - Injection von Repositories
