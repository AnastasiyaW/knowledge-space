---
title: "JavaScript Async und Fetch API"
category: concepts
tags: [web-frontend, javascript, async, promises, fetch, api]
level: 3
source_sha256: 6198f3599f1e50d972cbc6e17e69e612d25b6e1a723b1bd77d123aa06a5d4069
translation: machine
translated_at: '2026-10-24'
---
# JavaScript Async und Fetch API {#javascript-async-and-fetch-api}

JavaScript ist single-threaded. Asynchrone Operationen (Netzwerk, Timer) laufen im Hintergrund und benachrichtigen über Callbacks, Promises oder async/await.

## Event Loop {#event-loop}

1. **Call Stack**: synchroner Code
2. **Web APIs**: übernehmen asynchrone Operationen (setTimeout, fetch, DOM-Events)
3. **Microtask Queue**: Promise-Callbacks (höhere Priorität)
4. **Task Queue**: Callbacks von setTimeout und setInterval
5. **Event Loop**: verschiebt Tasks auf den Stack, sobald dieser leer ist

Microtasks (Promises) werden VOR Macrotasks (setTimeout) ausgeführt.

```javascript
setTimeout(() => console.log("timeout"), 0);
Promise.resolve().then(() => console.log("promise"));
console.log("sync");
// Output: sync, promise, timeout
```

## Promises {#promises}

Ein Promise repräsentiert einen zukünftigen Wert: pending -> fulfilled oder rejected.

```javascript
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    if (success) resolve("Data");
    else reject(new Error("Failed"));
  }, 1000);
});

promise
  .then(data => transform(data))
  .then(result => console.log(result))
  .catch(error => console.error(error))
  .finally(() => console.log("Done"));
```

### Statische Methoden {#static-methods}
```javascript
// Wait for ALL to fulfill (or first rejection)
Promise.all([p1, p2, p3]).then(([r1, r2, r3]) => { });

// Wait for ALL to settle
Promise.allSettled([p1, p2]).then(results => {
  results.forEach(r => console.log(r.status, r.value || r.reason));
});

// First to fulfill (ignores rejections unless ALL reject)
Promise.any([p1, p2, p3]);

// First to settle (fulfill or reject)
Promise.race([p1, p2, p3]);

Promise.resolve("value")
Promise.reject(new Error("reason"))
```

## async/await {#asyncawait}

Syntaktischer Zucker über Promises - asynchroner Code sieht synchron aus.

```javascript
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error("Failed:", error);
    throw error;
  }
}
```

### Parallele Ausführung {#parallel-execution}
```javascript
// Sequential (slow)
const user = await fetchUser(1);
const posts = await fetchPosts(1);

// Parallel (fast)
const [user, posts] = await Promise.all([
  fetchUser(1),
  fetchPosts(1)
]);
```

## Fetch API {#fetch-api}

```javascript
// GET
const response = await fetch("https://api.example.com/data");
const data = await response.json();

// POST
await fetch("/api/users", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Alice", age: 25 })
});

// DELETE, PATCH
await fetch("/api/users/1", { method: "DELETE" });
await fetch("/api/users/1", {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name: "Updated" })
});
```

### Response-Objekt {#response-object}
```javascript
response.ok          // true for 200-299
response.status      // HTTP code
response.headers

// Body (can only read ONCE)
await response.json()      // Parse JSON
await response.text()      // Plain text
await response.blob()      // Binary
await response.formData()
```

### Fehlerbehandlung {#error-handling}
**fetch wirft bei HTTP-Fehlern (404, 500) keine Exception.** Eine Exception wird nur bei Netzwerkfehlern geworfen.

```javascript
async function fetchData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (error) {
    if (error instanceof TypeError) console.error("Network error");
    else console.error("Request failed:", error);
  }
}
```

### Abort / Timeout {#abort-timeout}
```javascript
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 5000);

try {
  const response = await fetch(url, { signal: controller.signal });
} catch (error) {
  if (error.name === "AbortError") console.error("Timed out");
} finally {
  clearTimeout(timeout);
}
```

### FormData-Upload {#formdata-upload}
```javascript
const formData = new FormData();
formData.append("file", fileInput.files[0]);
await fetch("/upload", {
  method: "POST",
  body: formData  // Content-Type set automatically
});
```

## Stolperfallen {#gotchas}

- **fetch wirft bei 404/500 keine Exception**: `response.ok` muss manuell geprüft werden
- **Response-Body wird nur einmal gelesen**: ein zweiter Aufruf von `.json()` wirft einen Fehler; das Ergebnis deshalb speichern
- **`setTimeout(fn, 0)` ist nicht sofort**: die Ausführung wird auf den nächsten Tick des Event Loops verschoben (nach den Microtasks)
- **Fehlendes `await`**: wird `await` vergessen, liefert der Aufruf ein Promise-Objekt statt des Werts
- **Race Conditions**: Komponente wird während des Fetch unmounted; Abbruch-Flag prüfen oder AbortController verwenden
- **Promise.all bricht sofort ab**: eine Rejection lehnt alle ab; `allSettled` verwenden, wenn alle Ergebnisse benötigt werden

## Siehe auch {#see-also}

- [[js-functions]] - Callbacks, Higher-Order-Funktionen
- [[js-dom-and-events]] - DOM-Events sind asynchron
- [[react-state-and-hooks]] - useEffect für Datenabruf
- [[typescript-fundamentals]] - Typisierung asynchroner Funktionen
- [[event-loop-and-architecture]] - Serverseitige Async-Muster
