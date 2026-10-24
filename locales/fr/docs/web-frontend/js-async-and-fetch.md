---
title: "JavaScript : async et API Fetch"
category: concepts
tags: [web-frontend, javascript, async, promises, fetch, api]
level: 3
source_sha256: 6198f3599f1e50d972cbc6e17e69e612d25b6e1a723b1bd77d123aa06a5d4069
translation: machine
translated_at: '2026-10-24'
---
# JavaScript : async et API Fetch {#javascript-async-and-fetch-api}

JavaScript est mono-thread. Les opérations asynchrones (réseau, minuteurs) s'exécutent en arrière-plan et notifient leur résultat via des callbacks, des Promises ou async/await.

## Event Loop {#event-loop}

1. **Call Stack** : code synchrone
2. **Web APIs** : gèrent l'asynchrone (setTimeout, fetch, événements DOM)
3. **Microtask Queue** : callbacks des Promises (priorité plus élevée)
4. **Task Queue** : callbacks de setTimeout, setInterval
5. **Event Loop** : transfère les tâches vers la pile lorsqu'elle est vide

Les microtâches (Promises) s'exécutent AVANT les macrotâches (setTimeout).

```javascript
setTimeout(() => console.log("timeout"), 0);
Promise.resolve().then(() => console.log("promise"));
console.log("sync");
// Output: sync, promise, timeout
```

## Promises {#promises}

Une Promise représente une valeur future : en attente (pending) -> réalisée (fulfilled) ou rejetée (rejected).

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

### Méthodes statiques {#static-methods}
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

Sucre syntaxique au-dessus des Promises : le code asynchrone a l'apparence d'un code synchrone.

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

### Exécution en parallèle {#parallel-execution}
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

### Objet Response {#response-object}
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

### Gestion des erreurs {#error-handling}
**fetch ne lève pas d'exception sur les erreurs HTTP** (404, 500). Il ne lève une exception qu'en cas d'échec réseau.

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

### Annulation / Timeout {#abort-timeout}
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

### Envoi via FormData {#formdata-upload}
```javascript
const formData = new FormData();
formData.append("file", fileInput.files[0]);
await fetch("/upload", {
  method: "POST",
  body: formData  // Content-Type set automatically
});
```

## Gotchas {#gotchas}

- **fetch ne lève pas d'exception sur 404/500** : il faut vérifier `response.ok` manuellement
- **Corps de la réponse lu une seule fois** : appeler `.json()` deux fois lève une erreur ; stockez le résultat
- **`setTimeout(fn, 0)` n'est pas instantané** : son exécution est différée au prochain tick de la boucle d'événements (après les microtâches)
- **`await` oublié** : oublier `await` renvoie un objet Promise, et non la valeur
- **Conditions de concurrence** : le composant est démonté pendant le fetch ; vérifiez un drapeau d'annulation ou utilisez AbortController
- **Promise.all échoue immédiatement** : un seul rejet fait échouer l'ensemble ; utilisez `allSettled` si vous avez besoin de tous les résultats

## See Also {#see-also}

- [[js-functions]] - Callbacks, fonctions d'ordre supérieur
- [[js-dom-and-events]] - Les événements DOM sont asynchrones
- [[react-state-and-hooks]] - useEffect pour la récupération de données
- [[typescript-fundamentals]] - Typer les fonctions asynchrones
- [[event-loop-and-architecture]] - Modèles asynchrones côté serveur
