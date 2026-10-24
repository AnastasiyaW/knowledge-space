---
title: "Nebenläufigkeitsmuster"
category: patterns
tags: [nodejs, actor-model, crdt, blockchain, webrtc, shared-worker, concurrency]
level: 3
source_sha256: 1d3fffcf541f71f424e6b8f5fabddbdfe1f6af233391b2fe8793940f8cb610f4
translation: machine
translated_at: '2026-10-24'
---
# Nebenläufigkeitsmuster {#concurrency-patterns}

Nebenläufigkeit in Node.js geht über async/await hinaus und umfasst das Actor-Modell, CRDTs für verteilten Zustand, SharedWorker zur Koordination von Browser-Tabs sowie eigene Protokolle für Echtzeitanwendungen. Diese Muster lösen die Koordination zwischen unabhängigen Ausführungskontexten.

## Actor-Modell (Single-threaded) {#actor-model-single-threaded}

Laut Alan Kay sollte jede objektorientierte Programmierung dem Actor-Muster ähneln: isolierter Zustand, nachrichtenbasierte Kommunikation.

```js
class Actor {
  #queue = [];
  #processing = false;

  send(message) {
    this.#queue.push(message);
    if (!this.#processing) this.#process();
  }

  async #process() {
    this.#processing = true;
    while (this.#queue.length > 0) {
      const msg = this.#queue.shift();
      await this.handle(msg);
    }
    this.#processing = false;
  }
}
```

Die Single-threaded-Variante verwendet anstelle von `process.send()` / `MessagePort` eine asynchrone Warteschlange. Dieselbe API funktioniert für Single-Thread, Multi-Thread und Multi-Process, indem der Nachrichtentransport ausgetauscht wird.

**Reactor-Muster**: Ereignisschleifen-Modell für kooperatives Multitasking innerhalb eines einzelnen Threads – das Fundament von Node.js.

## CRDT (Conflict-free Replicated Data Types) {#crdt-conflict-free-replicated-data-types}

### Synchronisationsmethoden {#synchronization-methods}

- **State-based:** vollständiger Zustand wird gesendet (größere Nutzlasten, einfacher)
- **Operation-based:** nur Operationen werden übertragen (kleinere Nutzlasten, komplexer)
- **Delta-based:** nur Änderungen werden übertragen (am effizientesten für das Netzwerk)

### Verfügbare Datenstrukturen {#available-data-structures}

- G-Counter (nur wachsend), PN-Counter (positiv-negativ)
- G-Set (nur wachsend), 2P-Set (Zwei-Phasen), OR-Set (observed-remove)
- Graphen, geordnete Listen, Register

### Schemagesteuerte CRDTs {#schema-driven-crdt}

```js
const schema = {
  likes: { type: 'g-counter' },
  tags: { type: '2p-set' },
  inventory: { type: 'pn-counter' },
};
```

## SharedWorker-WebSocket {#sharedworker-websocket}

Eine WebSocket-Verbindung über mehrere Browser-Tabs hinweg teilen:

- 50 geöffnete Tabs, aber nur 1 WebSocket-Verbindung zum Server
- Service Worker agiert als Nachrichtenvermittler zwischen den Tabs
- Alle Tabs synchronisieren ihren Zustand über den Service Worker
- Spart Serverressourcen und Speicher auf dem Client

## Eigenes Binärprotokoll (Metacom) {#custom-binary-protocol-metacom}

- Paketformat mit IDs: positiv = Client-zu-Server, negativ = Server-zu-Client-Ereignisse
- Stream-IDs für Datei-Upload und -Download, multiplext über dieselbe Verbindung
- Binäre Serialisierung übertrifft JSON bei Größe und Geschwindigkeit
- Version 3: zusammengeführte Serializer-Funktionen, einzelne Buffer-Allokation für Stream-Chunks

### Dynamischer API-Client (Gerüst) {#dynamic-api-client-scaffold}

```js
const scaffold = (url, structure) => {
  const api = {};
  for (const [entity, methods] of Object.entries(structure)) {
    api[entity] = {};
    for (const method of methods) {
      api[entity][method] = (...args) =>
        fetch(`${url}/${entity}/${method}`, {
          method: 'POST', body: JSON.stringify(args),
        }).then(r => r.json());
    }
  }
  return api;
};
```

## Deployment-Muster {#deployment-patterns}

### Blue-Green-Deployment {#blue-green-deployment}
Zwei identische Cluster. Die neue Version wird auf einem bereitgestellt; bei Bedarf wird der Traffic sofort umgeschaltet.

### Canary-Release {#canary-release}
Einen Teil der Nutzer auf die neue Version leiten. Probleme erkennen, bevor der vollständige Rollout erfolgt.

### Feature-Toggles {#feature-toggles}
Funktionen dynamisch aktivieren oder deaktivieren, ohne neu zu deployen: Kommandozeilen-Flags, Fernsteuerung über ein Admin-Panel, Kill-Switch bei Fehlerspitzen.

## Fallstricke {#gotchas}

- Ein Single-threaded Actor in JS muss trotzdem Race Conditions im Message-Handler behandeln (mehrere awaits können sich verschränken)
- CRDTs konvergieren schließlich, können aber vorübergehend veraltete Daten anzeigen – nicht geeignet für Anforderungen an starke Konsistenz
- SharedWorker ist nicht in allen Browsern verfügbar – Kompatibilität prüfen

## Siehe auch {#see-also}

- [[async-patterns]] - async/await, EventEmitter als Nebenläufigkeitsprimitive
- [[event-loop-and-architecture]] - Single-threaded-Ausführungsmodell
- [[data-access-patterns]] - Transaktionen als serialisierter Zugriffsmuster
- [[streams]] - Nebenläufigkeit bei streambasierter Datenverarbeitung
