---
title: "Portée, fermetures et this en JavaScript"
category: concepts
tags: [web-frontend, javascript, scope, closures, this]
level: 3
source_sha256: 89fd7a2f9120cec11ed4fa38dee8feb376cbe5ccdbcd6d2878b8dde7e1f43321
translation: machine
translated_at: '2026-10-24'
---
# Portée, fermetures et this en JavaScript {#javascript-scope-closures-and-this}

La portée détermine l'accessibilité des variables. Les fermetures (closures) permettent l'encapsulation des données et la gestion d'état. La liaison de `this` dépend de la manière dont une fonction est appelée.

## Types de portée {#scope-types}

**Globale** : déclarée en dehors de toute fonction ou de tout bloc, accessible partout.
**Fonction** : déclarée à l'intérieur d'une fonction avec `var`, `let` ou `const`.
**Bloc** : déclarée à l'intérieur de `{}` avec `let` ou `const`. `var` ignore la portée de bloc !

```javascript
if (true) {
  let x = 10;    // Block-scoped
  var z = 30;    // Function-scoped (leaks out!)
}
console.log(z);   // 30
console.log(x);   // ReferenceError
```

### Chaîne de portées {#scope-chain}
Recherche de variable : portée courante -> parent -> grand-parent -> global. Elle est déterminée par l'endroit où le code est ÉCRIT (portée lexicale), et non par l'endroit d'où il est appelé.

## Hissage (hoisting) {#hoisting}

```javascript
greet();  // Works (function declarations fully hoisted)
function greet() { console.log("Hi"); }

console.log(x);  // undefined (var hoisted, not initialized)
var x = 5;

console.log(y);  // ReferenceError: TDZ
let y = 5;
```

## Mode strict {#strict-mode}

```javascript
"use strict";  // Top of file or function
// Undeclared variables throw, duplicate params throw, this=undefined in standalone calls
```

Les modules ES et les classes sont toujours en mode strict.

## Fermetures {#closures}

Une fonction « se souvient » des variables de sa portée externe, même après que la fonction externe a retourné sa valeur.

```javascript
function createCounter() {
  let count = 0;
  return {
    increment() { return ++count; },
    decrement() { return --count; },
    getCount() { return count; }
  };
}
const counter = createCounter();
counter.increment();  // 1
counter.increment();  // 2
// count is inaccessible directly - data privacy
```

### Utilisations des fermetures {#closure-uses}
1. **Encapsulation des données** : variables inaccessibles depuis l'extérieur
2. **Conservation d'état** : maintenir un état entre les appels
3. **Fonctions de fabrique** : créer des fonctions spécialisées

```javascript
function createMultiplier(factor) {
  return (number) => number * factor;
}
const double = createMultiplier(2);
```

### Piège de la variable de boucle {#loop-variable-pitfall}
```javascript
// Bug: all callbacks share same 'i'
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Prints: 3, 3, 3

// Fix: use let (new binding per iteration)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Prints: 0, 1, 2
```

## Le mot-clé `this` {#the-this-keyword}

### Règles de liaison (ordre de priorité) {#binding-rules-precedence-order}

**1. `new`** : `this` = objet nouvellement créé
```javascript
function User(name) { this.name = name; }
const u = new User("Alice");  // this = new object
```

**2. Explicite** : `call`, `apply`, `bind`
```javascript
greet.call(user);              // this = user
greet.apply(user, [args]);     // this = user, args as array
const bound = greet.bind(user); // Returns function with fixed this
```

**3. Implicite** : appel de méthode
```javascript
user.greet();  // this = user
const fn = user.greet;
fn();          // this = undefined (method detached!)
```

**4. Par défaut** : appel standalone
```javascript
function test() { console.log(this); }
test();  // window (non-strict) or undefined (strict)
```

### Fonctions fléchées et this {#arrow-functions-and-this}
Les fonctions fléchées n'ont PAS leur propre `this` : elles héritent de celui de la portée englobante.

```javascript
const user = {
  name: "Alice",
  greet: () => console.log(this.name),       // undefined! (inherits from module/global)
  delayedGreet() {
    setTimeout(() => console.log(this.name), 100);  // "Alice" (inherits from method)
  }
};
```

**Règle** : ne pas utiliser de fonctions fléchées comme méthodes d'objet. Les utiliser à l'intérieur de méthodes pour les callbacks.

### call / apply / bind {#call-apply-bind}
```javascript
func.call(thisArg, arg1, arg2);           // Invoke with this + args
func.apply(thisArg, [arg1, arg2]);        // Same, args as array
const boundFn = func.bind(thisArg, arg1); // New function, fixed this
```

## Pièges courants {#gotchas}

- **Détachement de méthode** : `const fn = obj.method; fn()` perd la liaison de `this`
- **Méthodes fléchées** : `{ greet: () => this.name }` - `this` n'est PAS l'objet
- **Bug de fermeture dans les boucles** : `var` dans une boucle partage une seule liaison ; utiliser `let`
- **`this` dans les fonctions imbriquées** : une fonction imbriquée classique a son propre `this` (généralement undefined) ; utiliser une fonction fléchée ou `const self = this`
- **`bind` retourne une nouvelle fonction** : `element.removeEventListener("click", handler.bind(obj))` ne fonctionnera pas - la référence de fonction est différente

## Voir aussi {#see-also}

- [[js-functions]] - Fonctions fléchées et classiques, IIFE
- [[js-objects-and-data]] - Méthodes d'objet et `this`
- [[react-state-and-hooks]] - Les hooks remplacent le `this` des composants de classe
