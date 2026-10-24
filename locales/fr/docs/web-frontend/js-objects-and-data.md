---
title: "Objets et données en JavaScript"
category: concepts
tags: [web-frontend, javascript, objects, json, date]
level: 3
source_sha256: 51eca51086316c034d54a2fd00000a46f7ed75f10009062ff54b97066a66990e
translation: machine
translated_at: '2026-10-24'
---
# Objets et données en JavaScript {#javascript-objects-and-data}

Les objets sont des collections clé-valeur. Avec JSON, Date et Symbol, ils constituent le socle de la gestion des données en JavaScript.

## Création et accès aux objets {#creating-and-accessing-objects}

```javascript
const user = {
  name: "Alice",
  age: 25,
  skills: ["JS", "CSS"],
  address: { city: "New York" },
  greet() { return `Hi, I'm ${this.name}`; }
};

user.name              // "Alice" (dot notation)
user["name"]           // "Alice" (bracket - for dynamic keys)
user?.address?.city    // "New York" (safe with optional chaining)
```

## Modification {#modifying}

```javascript
user.email = "a@b.com";    // Add
user.age = 26;              // Update
delete user.age;            // Delete

const obj = { a: 1 };
obj.a = 2;    // OK (property mutable)
obj = {};     // Error (const prevents reassignment)
```

## Notation abrégée et clés calculées {#shorthand-and-computed-keys}

```javascript
const name = "Alice", age = 25;
const user = { name, age };                  // Shorthand
const key = "email";
const obj = { [key]: "a@b.com" };           // Computed key
const obj = { [`${key}Count`]: 5 };         // { emailCount: 5 }
```

## Déstructuration {#destructuring}

```javascript
const { name, age } = user;
const { name: userName } = user;            // Rename
const { role = "user" } = user;             // Default
const { address: { city } } = user;         // Nested

function greet({ name, age = 0 }) { }      // In parameters
```

## Spread {#spread}

```javascript
const copy = { ...user };                    // Shallow copy
const merged = { ...defaults, ...overrides }; // Merge (right wins)
const updated = { ...user, age: 26 };       // Copy + update
```

**Copie superficielle uniquement** : les objets imbriqués restent des références. Utilisez `structuredClone(obj)` pour une copie profonde.

## Méthodes statiques d'Object {#object-static-methods}

```javascript
Object.keys(user)       // ["name", "age", ...]
Object.values(user)     // ["Alice", 25, ...]
Object.entries(user)    // [["name","Alice"], ["age",25], ...]

for (const [key, value] of Object.entries(user)) {
  console.log(`${key}: ${value}`);
}

Object.assign(target, source)     // Merge (mutates target)
Object.freeze(obj)                // Shallow immutable
Object.seal(obj)                  // Can modify, can't add/delete

"name" in user                    // true (includes inherited)
Object.hasOwn(user, "name")      // true (own only, ES2022)
```

## null et undefined {#null-vs-undefined}

```javascript
undefined  // Not assigned, missing param, missing property
null       // Intentional "no value"

typeof undefined  // "undefined"
typeof null       // "object" (historical bug)
null == undefined  // true (loose)
null === undefined // false (strict)
```

Convention : utilisez `null` pour une absence de valeur explicite, `undefined` signifie « pas encore affecté ».

## JSON {#json}

```javascript
JSON.stringify(user)              // Object -> JSON string
JSON.stringify(user, null, 2)     // Pretty-printed
JSON.parse('{"name":"Alice"}')    // JSON string -> Object

// Deep clone (simple objects only)
const clone = JSON.parse(JSON.stringify(original));
// Modern deep clone (handles more types)
const clone = structuredClone(original);
```

**Règles JSON** : clés entre guillemets doubles, pas de fonctions, `undefined` ni Symbol, pas de virgules finales, pas de commentaires.

## Date {#date}

```javascript
const now = new Date();
const d = new Date(2024, 0, 15);        // Jan 15 (month is 0-indexed!)
const d = new Date("2024-01-15");

now.getFullYear()    // 2024
now.getMonth()       // 0-11 (January = 0!)
now.getDate()        // 1-31
now.getDay()         // 0-6 (Sunday = 0!)
now.getTime()        // Milliseconds since epoch

now.toLocaleDateString()  // Locale-dependent
now.toISOString()         // "2024-01-15T00:00:00.000Z"
Date.now()                // Timestamp (no object)
```

## Symbol {#symbol}

```javascript
const id = Symbol("description");
Symbol("x") === Symbol("x")  // false (always unique)

const SECRET = Symbol("secret");
const obj = { [SECRET]: "hidden", name: "visible" };
Object.keys(obj)   // ["name"] (Symbols not enumerable)
```

Utilisé pour des propriétés réellement privées et pour éviter les collisions de noms.

## Pièges courants {#gotchas}

- **Les mois sont indexés à partir de 0** : janvier = 0, décembre = 11 (le bug le plus fréquent avec Date)
- **Le spread d'objet est superficiel** : les objets et tableaux imbriqués restent des références partagées
- **`typeof null === "object"`** : bug historique, jamais corrigé
- **`JSON.stringify` ignore les fonctions** : ainsi que `undefined` et Symbol
- **`for...in` inclut les propriétés héritées** : utilisez `Object.keys()` ou `Object.hasOwn()`
- **Comparaison d'objets par référence** : `{} === {}` vaut `false`

## Voir aussi {#see-also}

- [[js-arrays]] - Méthodes des tableaux, déstructuration, spread
- [[js-dom-and-events]] - localStorage (sérialisation JSON)
- [[js-async-and-fetch]] - Fetch renvoie du JSON
- [[typescript-fundamentals]] - Interfaces de types pour les objets
