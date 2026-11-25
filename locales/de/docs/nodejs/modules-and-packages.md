---
title: "Module und Pakete"
category: concepts
tags: [nodejs, modules, commonjs, esm, require, import, package-lock, npm]
level: 3
source_sha256: 8b1418bc62efa5678c6ad4322622a213bdb18cb6e4d817025b0ca724dc9f51ef
translation: machine
translated_at: '2026-10-24'
---
# Module und Pakete {#modules-and-packages}

Node.js unterstützt zwei Modulsysteme: CommonJS (`require`/`module.exports`) und ESM (`import`/`export`). Beide bestehen nebeneinander und werden dies auch auf unbestimmte Zeit tun – das Entfernen von `require` aus Node.js würde eine vollständige Neuschreibung erfordern. Das Modulsystem bietet eingebautes Singleton-Verhalten, DI-Möglichkeiten und Scope-Isolation.

## Wichtige Fakten {#key-facts}

- `require()` ist synchron, `import` ist asynchron
- Node.js bietet eine gute Interoperabilität zwischen beiden Systemen
- Der Modul-Cache in CommonJS sorgt standardmäßig für Singleton-Verhalten – `require()` liefert dieselbe Instanz zurück
- In Node.js gibt es keinen echten globalen Scope für Benutzercode – jedes Modul wird in eine Funktion eingebettet, wodurch ein modulbezogener Scope entsteht
- In browserseitigem JS teilen sich alle Dateien einen Scope, sofern sie nicht in IIFEs eingeschlossen sind oder Module-Bundler verwendet werden
- `import.meta.url` liefert die Datei-URL in ESM; mit `createRequire(import.meta.url)` erhält man `require()` in ESM
- `package-lock.json` sollte immer committet werden – selbst Patch-Versionen können über transitive Abhängigkeiten Probleme verursachen

### Module als DI-Alternative {#modules-as-di-alternative}

Das JavaScript-Modulsystem kann viele DI-Muster ersetzen:
- **Singleton:** Der Modul-Cache liefert dieselbe Instanz zurück
- **Strategy:** Objekt/Map mit Strategie-Implementierungen exportieren
- **Konfiguration:** Konfigurationsobjekt exportieren und dort importieren, wo es benötigt wird
- **Factory:** Factory-Funktionen exportieren

## Muster {#patterns}

### ESM in Node.js mit CommonJS-Interop {#esm-in-nodejs-with-commonjs-interop}

```js
// Using require() inside ESM
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const fs = require('fs'); // CommonJS require inside ESM
```

### Konfiguration als Modul {#config-as-module}

```js
// config.js
module.exports = {
  port: 8000,
  db: { host: 'localhost', port: 5432, database: 'app' },
  crypto: { saltLength: 16, keyLength: 64 },
  session: { timeout: 3600000 },
  transport: 'ws', // 'http' or 'ws'
};

// main.js - dynamic transport loading
const config = require('./config');
const transport = require(`./${config.transport}.js`);
```

### Bedeutung von package-lock.json {#package-lockjson-importance}

`package.json` verwendet Semver-Bereiche. Die Lock-Datei sorgt für deterministische Builds, weil:
- Eine Abhängigkeit kann eine geänderte transitive Abhängigkeit nachziehen
- Mehrere Pakete können widersprüchliche Versionsanforderungen haben
- Ein Bugfix in einem Paket kann das Verhalten ungewollt ändern, von dem ein anderes Paket abhängt

## Fallstricke {#gotchas}

- ESM stammt aus dem Frontend-Ökosystem als Vereinheitlichungsbemühung – CJS und ESM werden in Node.js auf unbestimmte Zeit nebeneinander bestehen
- `require()` liefert beim zweiten Aufruf das gecachte Modul zurück – Mutationen am exportierten Objekt sind überall sichtbar
- Zirkuläre Abhängigkeiten funktionieren in CJS (es wird ein teilweise geladenes Modul zurückgegeben), können aber subtile Fehler verursachen

## Siehe auch {#see-also}

- [[dependency-injection]] – DI vs. Modulsystem zur Entkopplung
- [[application-architecture]] – wie Module in eine geschichtete Architektur passen
- [[solid-and-grasp]] – SRP angewendet auf das Moduldesign
