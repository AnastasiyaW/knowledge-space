---
title: "Fonctions JavaScript"
category: concepts
tags: [web-frontend, javascript, functions, arrow-functions, callbacks]
level: 3
source_sha256: 8d8784ff92ac0f7a810a6263a2d68bffa9b039376a29f2dcce767446092561ff
translation: machine
translated_at: '2026-10-24'
---
# Fonctions JavaScript {#javascript-functions}

Les fonctions sont des citoyens de première classe en JavaScript : elles peuvent être stockées dans des variables, passées en arguments et retournées par d'autres fonctions.

## Types de déclaration {#declaration-types}

```javascript
// Function declaration (hoisted)
function add(a, b) { return a + b; }

// Function expression (NOT hoisted)
const add = function(a, b) { return a + b; };

// Arrow function
const add = (a, b) => a + b;              // Implicit return
const add = (a, b) => { return a + b; };  // Explicit (block body)
const square = x => x * x;                // Single param: no parens
const greet = () => "Hello!";             // No params
const getUser = () => ({ name: "Alice" }); // Return object: wrap in ()
```

### Fléchées vs classiques {#arrow-vs-regular}

| Caractéristique | Classique | Fléchée |
|-----------------|-----------|---------|
| `this` | Propre (dynamique) | Hérité (lexical) |
| `arguments` | Oui | Non (utiliser `...args`) |
| `new` | Constructeur | Impossible |
| Hoisting | Déclarations oui | Non |
| Idéal pour | Méthodes, constructeurs | Callbacks, programmation fonctionnelle |

## Paramètres {#parameters}

```javascript
// Default
function greet(name = "World") { return `Hello, ${name}!`; }

// Rest (must be last)
function sum(...numbers) { return numbers.reduce((a, b) => a + b, 0); }

// Destructuring
function createUser({ name, age, role = "user" }) {
  return { name, age, role };
}
```

## Valeurs de retour {#return-values}

```javascript
function divide(a, b) {
  if (b === 0) return null;   // Early return
  return a / b;
}
// No explicit return = undefined
```

## Fonctions d'ordre supérieur {#higher-order-functions}

Fonctions qui prennent ou retournent des fonctions :

```javascript
// Takes function as argument
function repeat(n, action) {
  for (let i = 0; i < n; i++) action(i);
}

// Returns function (factory)
function multiplier(factor) {
  return (number) => number * factor;
}
const double = multiplier(2);
double(5);   // 10
```

## Callbacks {#callbacks}

```javascript
function fetchData(callback) {
  setTimeout(() => {
    callback({ name: "Alice" });
  }, 1000);
}
fetchData((data) => console.log(data.name));
```

Les callbacks imbriqués deviennent illisibles (« callback hell »). Résolu par [[js-async-and-fetch|Promises et async/await]].

## IIFE (exécutée immédiatement) {#iife-immediately-invoked}

```javascript
(function() {
  const secret = "hidden";
  console.log("Runs immediately");
})();

(() => { console.log("Arrow IIFE"); })();
```

Crée une isolation de portée. Moins nécessaire avec `let`/`const` et les modules, mais encore utilisée pour une initialisation ponctuelle.

## Fonctions pures {#pure-functions}

```javascript
// Pure: same input = same output, no side effects
function add(a, b) { return a + b; }

// Impure: modifies external state
let total = 0;
function addToTotal(n) { total += n; return total; }
```

Les fonctions pures sont prévisibles, testables et mettables en cache. À privilégier lorsque c'est possible.

## Pièges courants {#gotchas}

- **`this` dans les fléchées** : les fonctions fléchées héritent de `this` du scope englobant, ne pas les utiliser comme méthodes d'objet
- **Appel vs passage** : `onClick={handleClick}` (passage de la référence) vs `onClick={handleClick()}` (appel immédiat)
- **Retour d'un littéral objet** : la fléchée doit entourer l'objet de parenthèses : `() => ({ key: value })`
- **`arguments` dans les fléchées** : n'existe pas ; utiliser les paramètres rest `...args`
- **Paramètres par défaut évalués à l'appel** : `function f(arr = [])` crée un nouveau tableau à chaque appel

## Voir aussi {#see-also}

- [[js-scope-closures-this]] - Chaîne de portée, closures, liaison de `this`
- [[js-arrays]] - Méthodes de tableau comme fonctions d'ordre supérieur
- [[js-async-and-fetch]] - Patterns asynchrones remplaçant les callbacks
- [[react-state-and-hooks]] - Hooks React comme patterns fonctionnels
