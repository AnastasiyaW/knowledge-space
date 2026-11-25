---
title: "Principes SOLID et GRASP"
category: concepts
tags: [nodejs, solid, grasp, lsp, srp, dip, composition, inheritance]
level: 3
source_sha256: d37c2ac94503201a8d5c0b8b2097edddb7da79a7d4e3cfb56fafefc9d24a7e2d
translation: machine
translated_at: '2026-10-24'
---
# Principes SOLID et GRASP {#solid-and-grasp-principles}

Les principes SOLID et GRASP guident l'organisation du code en JavaScript, mais leur application diffère de celle des langages à base de classes. Les closures, les fonctions de première classe et le système de modules offrent des mécanismes alternatifs permettant d'atteindre les mêmes objectifs. La plupart des développeurs expérimentés acquièrent ces intuitions par la pratique sans connaître les noms formels.

## Points clés {#key-facts}

- Le mot-clé `extends` est trompeur : en théorie des types, une sous-classe devrait *restreindre* le type parent, alors que `extends` suggère un *élargissement*
- **LSP** : une référence à une sous-classe doit pouvoir être substituée partout où la classe parente est attendue
- **Composition vs héritage** : la même fonctionnalité peut être écrite selon plus de 32 paradigmes différents (fonctions pures, classes, prototypes, closures, acteurs, monades, mixins, etc.)
- En programmation fonctionnelle (FP), tous les patterns GoF se ramènent à une composition de fonctions `G(f(x))`
- Angular s'aligne mieux sur GoF/GRASP/SOLID (à base de classes) ; React penche vers le fonctionnel
- Il n'existe pas de ressource complète « GoF pour la FP en JavaScript »
- Le choix entre paradigmes est pragmatique, non dogmatique

## Types algébriques de données (ADT) en JavaScript {#algebraic-data-types-adt-in-javascript}

ADT = types créés via des opérations algébriques (somme, produit) sur d'autres types. Ne pas confondre avec « Abstract Data Types ».

### Enregistrements immuables {#immutable-records}

```js
const record = (schema) => {
  const obj = Object.create(null);
  for (const [key, defaultVal] of Object.entries(schema)) {
    obj[key] = defaultVal;
  }
  return Object.freeze(obj);
};

// Fork: create a modified copy
const fork = (instance, updates) => {
  const copy = Object.create(null);
  for (const key of Object.keys(instance)) {
    copy[key] = Reflect.has(updates, key) ? updates[key] : instance[key];
  }
  if (Object.isFrozen(instance)) Object.freeze(copy);
  return copy;
};
```

- `Object.create(null)` pour une chaîne de prototypes propre
- Les mises à jour ont la priorité sur les valeurs d'instance
- Les types union de TypeScript disparaissent à la compilation : les implémentations runtime des ADT persistent

## Patterns {#patterns}

### Composition vs héritage - Multiples paradigmes {#composition-vs-inheritance-multiple-paradigms}

```js
// 1. Pure functions with composition
const move = (point, dx, dy) => ({ x: point.x + dx, y: point.y + dy });

// 2. Class-based
class Point {
  constructor(x, y) { this.x = x; this.y = y; }
  move(dx, dy) { return new Point(this.x + dx, this.y + dy); }
}

// 3. Closure-based (values hidden in closures)
const createPoint = (x, y) => ({
  move: (dx, dy) => createPoint(x + dx, y + dy),
  toString: () => `(${x}, ${y})`,
});

// 4. Actor model
class PointActor extends Actor {
  #x; #y;
  async handle({ type, dx, dy }) {
    if (type === 'move') { this.#x += dx; this.#y += dy; }
  }
}
```

Chaque paradigme possède des dizaines de sous-approches. Apprendre des patterns permet d'évaluer des compromis, et non d'appliquer des modèles figés.

### Protocoles comme interfaces (programmation par contrat) {#protocols-as-interfaces-contract-programming}

```js
// Built-in JavaScript protocols act as abstract interfaces:
// Iterable: Symbol.iterator → { next() → { value, done } }
// Thenable: .then() method → Promise compatibility
// Async Iterable: Symbol.asyncIterator → async iterator

// Conformance verified by tests, not type system
// All Promises are thenables, not all thenables are Promises
```

Les objets partageant le même contrat (mêmes champs, mêmes types, même ordre) obtiennent les mêmes classes cachées (hidden classes) de V8, ce qui permet une optimisation monomorphe. La programmation par contrat compte pour la performance en JS.

## Deux extrêmes d'architecture {#two-architecture-extremes}

1. **Sur-ingénierie** : SOLID/GRASP/DDD stricts - beaucoup de classes, de couches, de séparations - complexe et verbeux
2. **Minimaliste** : une seule classe gère tout, en violation du SRP - mais davantage de fonctionnalités en moins de code
3. **Juste milieu** : schéma déclaratif + pattern de dépôt (repository) universel

## Pièges à éviter {#gotchas}

- Violer le LSP (ajouter des méthodes incompatibles dans les sous-classes) fait perdre la flexibilité que l'héritage était censé apporter
- Le fichier package-lock.json DOIT être versionné : même les versions de correctif peuvent casser des dépendances transitives
- Les LLM ne savent pas faire la structuration ni l'architecture d'une application : le développeur doit être PLUS compétent que le LLM, en agissant comme architecte senior

## Voir aussi {#see-also}

- [Patterns de conception (GoF) en JavaScript](design-patterns-gof.md) - implémentations concrètes des patterns en JavaScript
- [[dependency-injection]] - le principe d'inversion de dépendances en pratique
- [[closures-and-scope]] - les closures comme alternative à l'encapsulation basée sur les classes
- [[application-architecture]] - l'architecture en couches comme application de SOLID
