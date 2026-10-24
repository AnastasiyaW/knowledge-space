---
title: "Gestion des erreurs"
category: concepts
tags: [nodejs, errors, aggregate-error, error-cause, app-error, fail-fast]
level: 3
source_sha256: 1a9f8258b647813f626fa766cf6b7b71b39a83e8da1ce5b4b55feead33377543
translation: machine
translated_at: '2026-10-24'
---
# Gestion des erreurs {#error-handling}

Une gestion efficace des erreurs dans Node.js distingue les erreurs applicatives (violations de la logique métier) des erreurs système (défaillances de l'infrastructure). Le pattern fail-fast, les classes d'erreur personnalisées et les fonctionnalités modernes de chaînage d'erreurs (AggregateError, Error.cause) permettent une propagation structurée des erreurs.

## Points clés {#key-facts}

- Toujours séparer les erreurs applicatives des erreurs système : ne jamais exposer les détails d'une erreur système aux clients
- `AggregateError` regroupe plusieurs erreurs en une seule (fichier manquant + cache expiré + clé invalide)
- `Error.cause` chaîne les erreurs pour le suivi des causes (ajouté en ES2022)
- Les deux consomment de la mémoire : gardez les chaînes courtes
- `EventEmitter({ captureRejections: true })` capture automatiquement les erreurs des callbacks asynchrones (Node.js uniquement)
- Les erreurs logiques (le code s'exécute sans lever d'exception mais produit des résultats incorrects) sont les plus dangereuses : aucun message d'erreur à rechercher

## Types d'erreurs {#error-types}

### Erreurs applicatives et erreurs système {#application-errors-vs-system-errors}

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

### Chaînage d'erreurs {#error-chaining}

```js
// AggregateError - multiple simultaneous failures
throw new AggregateError([err1, err2, err3], 'Multiple failures');

// Error.cause - causal chain
throw new Error('Operation failed', { cause: originalError });
```

## Patterns {#patterns}

### Fail Fast / Retour anticipé {#fail-fast-return-early}

```js
async function processUser(id) {
  if (!id) throw new Error('ID required');
  const user = await db.find(id);
  if (!user) throw new Error('User not found');
  // ... proceed with happy path only
}
```

### Extraction simplifiée de la réponse d'erreur {#simplified-error-response-extraction}

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

### Isolation des erreurs en bac à sable {#sandbox-error-isolation}

```js
const vm = require('vm');
const context = vm.createContext({
  AppError,
  // Only expose safe APIs to untrusted code
});
const result = vm.runInContext(userCode, context, { timeout: 5000 });
// instanceof AppError distinguishes app errors from system errors
```

## Pièges {#gotchas}

- Le renvoi d'erreurs à la manière de Go, sous la forme `{ error, data }`, est un anti-pattern en JS : il fait perdre la propagation structurée des erreurs et casse les traces de pile asynchrones
- Les valeurs codées en dur (chemins de fichiers, fins de ligne, tailles de buffers) doivent être des paramètres et non des chaînes magiques, à l'exception de `-1` pour « non trouvé » et de `0` pour le premier index (conventions du langage)
- Les tableaux `AggregateError` et les chaînes de `cause` doivent être dépliés lors du débogage : gardez-les courts

## Voir aussi {#see-also}

- [[async-patterns]] - gestion des erreurs dans le code asynchrone, captureRejections
- [[security-and-sandboxing]] - module vm et propagation sûre des erreurs
- [[application-architecture]] - couches de gestion des erreurs dans l'architecture serveur
