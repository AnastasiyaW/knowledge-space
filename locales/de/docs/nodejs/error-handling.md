---
title: "Fehlerbehandlung"
category: concepts
tags: [nodejs, errors, aggregate-error, error-cause, app-error, fail-fast]
level: 3
source_sha256: 1a9f8258b647813f626fa766cf6b7b71b39a83e8da1ce5b4b55feead33377543
translation: machine
translated_at: '2026-10-24'
---
# Fehlerbehandlung {#error-handling}

Eine effektive Fehlerbehandlung in Node.js unterscheidet zwischen Anwendungsfehlern (Verletzungen der Geschäftslogik) und Systemfehlern (Ausfälle der Infrastruktur). Das Fail-Fast-Muster, benutzerdefinierte Fehlerklassen und moderne Funktionen zur Fehlerverkettung (AggregateError, Error.cause) ermöglichen eine strukturierte Weitergabe von Fehlern.

## Wichtige Fakten {#key-facts}

- Anwendungsfehler und Systemfehler müssen immer getrennt werden – Details zu Systemfehlern dürfen niemals an Clients weitergegeben werden
- `AggregateError` fasst mehrere Fehler zu einem einzigen zusammen (fehlende Datei + abgelaufener Cache + ungültiger Schlüssel)
- `Error.cause` verkettet Fehler zur Nachverfolgung von Ursachen (eingeführt in ES2022)
- Beide verbrauchen Speicher – Ketten daher kurz halten
- `EventEmitter({ captureRejections: true })` fängt Fehler in asynchronen Callbacks automatisch ab (nur Node.js)
- Logikfehler (der Code wirft keine Exception, liefert aber falsche Ergebnisse) sind am gefährlichsten – es gibt keine Fehlermeldung, die man suchen könnte

## Fehlertypen {#error-types}

### Anwendungsfehler vs. Systemfehler {#application-errors-vs-system-errors}

```js
class AppError extends Error {
  constructor(message, code) {
    super(message);
    this.code = code;
  }
}

// In request handler:
if (err instanceof AppError) {
  reply(err.code, err.message); // 4xx - safe to expose
} else {
  reply(500, 'Internal error');  // Don't expose system errors
}
```

### Fehlerverkettung {#error-chaining}

```js
// AggregateError - multiple simultaneous failures
throw new AggregateError([err1, err2, err3], 'Multiple failures');

// Error.cause - causal chain
throw new Error('Operation failed', { cause: originalError });
```

## Muster {#patterns}

### Fail Fast / Frühzeitige Rückgabe {#fail-fast-return-early}

```js
async function processUser(id) {
  if (!id) throw new Error('ID required');
  const user = await db.find(id);
  if (!user) throw new Error('User not found');
  // ... proceed with happy path only
}
```

### Vereinfachte Extraktion von Fehlerantworten {#simplified-error-response-extraction}

```js
// Before: duplicated error handling
try {
  const result = await process();
  reply(200, result);
} catch (err) {
  if (err instanceof AppError) reply(err.code, err.message);
  else reply(500, 'Error');
}

// After: extract error code/message pair
const getErrorResponse = (err) =>
  err instanceof AppError
    ? [err.code, err.message]
    : [500, 'Internal error'];
```

### Fehlerisolation in der Sandbox {#sandbox-error-isolation}

```js
const vm = require('vm');
const context = vm.createContext({
  AppError,
  // Only expose safe APIs to untrusted code
});
const result = vm.runInContext(userCode, context, { timeout: 5000 });
// instanceof AppError distinguishes app errors from system errors
```

## Fallstricke {#gotchas}

- Go-artige Fehlerrückgaben `{ error, data }` in JS sind ein Anti-Pattern: Sie gehen die strukturierte Weitergabe von Fehlern verloren und zerstören asynchrone Stack-Traces
- Fest codierte Werte (Dateipfade, Zeilenenden, Puffergrößen) sollten als Parameter übergeben werden, nicht als Magic Strings – ausgenommen sind `-1` für „nicht gefunden“ und `0` für den ersten Index (sprachliche Konventionen)
- AggregateError-Arrays und Fehlerketten müssen beim Debugging aufgelöst werden – daher kurz halten

## Siehe auch {#see-also}

- [[async-patterns]] - Fehlerbehandlung in asynchronem Code, captureRejections
- [[security-and-sandboxing]] - vm-Modul und sichere Weitergabe von Fehlern
- [[application-architecture]] - Ebenen der Fehlerbehandlung in der Serverarchitektur
