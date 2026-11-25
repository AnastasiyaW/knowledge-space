---
title: "Fermetures et portée"
category: concepts
tags: [nodejs, javascript, closures, scope, lexical-environment, block-scope, module-scope]
level: 3
source_sha256: 330da0f5fd5c43ceb75c676b8c5ed07375ed1d8fd2bc1d9d7229e4e72f0a7a33
translation: machine
translated_at: '2026-10-24'
---
# Fermetures et portée {#closures-and-scope}

Une fermeture (*closure*) est une fonction qui conserve une référence vers les variables de la portée de sa fonction externe, même après que cette fonction externe a fini de s'exécuter. La fermeture est une structure de données stockée sur le tas (*heap*) à l'intérieur du runtime JS : seule la fonction interne peut lire et écrire ces données. Comprendre la portée et les fermetures est essentiel pour l'encapsulation, les fonctions de fabrique (*factory functions*) et la conception de modules dans Node.js.

## Points clés {#key-facts}

- **Portée (zone de visibilité)** : vue depuis un identifiant - là où il est visible (portée de fonction, de bloc, de module ou globale)
- **Contexte lexical / environnement lexical** : vu depuis une position dans le programme - quels identifiants sont accessibles à cet endroit
- Une fermeture est une structure de données sur le tas ; il n'existe aucune référence externe - seule la fonction interne peut y accéder
- Similaire à `this` dans les objets, mais contrairement à `this`, on ne peut pas ajouter de champs à une fermeture depuis l'extérieur

### Trois conditions pour une fermeture {#three-conditions-for-a-closure}

Les trois doivent être réunies simultanément :
1. Une fonction externe définit des variables
2. Une fonction interne référence ces variables
3. La fonction interne est retournée ou transmise à l'extérieur

Si l'une de ces parties manque, ce n'est pas une fermeture complète. Accéder à une variable globale depuis une fonction n'est **pas** une fermeture.

### Portée de module dans Node.js {#nodejs-module-scope}

- Chaque module est encapsulé dans une fonction, ce qui crée une portée au niveau du module - il n'existe pas de véritable portée globale pour le code utilisateur
- En JavaScript dans le navigateur, tous les fichiers partagent une même portée, sauf s'ils sont encapsulés dans des IIFE ou gérés par des bundlers de modules

## Modèles {#patterns}

### Encapsulation basée sur les fermetures {#closure-based-encapsulation}

```js
function createCounter(initial = 0) {
  let count = initial; // only accessible through returned methods
  return {
    increment() { return ++count; },
    decrement() { return --count; },
    getCount() { return count; },
  };
}

const counter = createCounter(10);
counter.increment(); // 11
// counter.count → undefined (truly private)
```

### Portée de bloc comme héritage {#block-scope-as-inheritance}

```js
function processUser(user) {
  let greeting = 'Hello'; // default "base" behavior
  if (user.isVIP) {
    let greeting = 'Welcome, esteemed'; // "override" in nested scope
    console.log(`${greeting} ${user.name}`);
    return;
  }
  console.log(`${greeting} ${user.name}`);
}
```

### Encapsulation de module (comment Node.js crée la portée) {#module-wrapping-how-nodejs-creates-scope}

```js
// Node.js wraps each module:
// (function(exports, require, module, __filename, __dirname) {
//   ... your module code ...
// });
// This is why top-level variables are module-scoped, not global
```

## Pièges {#gotchas}

- Les fermetures conservent des références vers l'ensemble de l'environnement lexical, et non seulement vers les variables utilisées - cela peut provoquer une rétention mémoire
- Dans les boucles avec `var`, toutes les fermetures partagent la même variable ; utilisez `let` (portée de bloc) pour une portée par itération
- Accéder à une variable globale depuis une fonction n'est **pas** une fermeture - confondre les deux conduit à des erreurs de compréhension architecturale

## Voir aussi {#see-also}

- [[v8-optimization]] - comment V8 stocke les structures de données des fermetures sur le tas
- [[modules-and-packages]] - l'encapsulation des modules crée la portée englobante
- [Design Patterns (GoF) in JavaScript](design-patterns-gof.md) - les fermetures comme fondement de nombreux patrons
- [[solid-and-grasp]] - enregistrements immuables basés sur les fermetures
