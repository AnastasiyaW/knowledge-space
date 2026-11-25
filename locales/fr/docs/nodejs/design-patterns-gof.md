---
title: "Patrons de conception (GoF) en JavaScript"
category: patterns
tags: [nodejs, gof, design-patterns, factory, strategy, observer, adapter, facade, proxy, decorator]
level: 3
source_sha256: 4afff7b1532b86f49ea021fb3b5ec2a8dc1b83037d233e80b2311cb63274c55a
translation: machine
translated_at: '2026-10-24'
---
# Patrons de conception (GoF) en JavaScript {#design-patterns-gof-in-javascript}

Les patrons du Gang of Four s'appliquent différemment en JavaScript que dans les langages à classes. Les fonctions de première classe, les closures et le typage dynamique simplifient beaucoup de patrons en simples fonctions ou objets. En programmation fonctionnelle, tous les patrons GoF se réduisent à la composition de fonctions : `G(f(x))`. ~20 % des patrons couvrent ~80 % des cas d'usage réels.

## Patrons de création {#creational-patterns}

### Factory Method {#factory-method}

Remplacez les appels directs à `new` par des invocations de méthodes pour une instanciation polymorphe :

```js
// JavaScript simplified - no abstract classes needed
const creators = {
  electronics: (data) => ({ type: 'electronics', ...data }),
  clothing: (data) => ({ type: 'clothing', ...data }),
};
const create = (type, data) => creators[type](data);

// Factorify - factory from class
const factorify = (Entity) => (...args) => new Entity(...args);
const createUser = factorify(User);
const user = createUser('John', 25); // no `new` needed
```

### Object Pool / AsyncPool {#object-pool-asyncpool}

```js
class AsyncPool {
  constructor(factory, size) {
    this.instances = Array.from({ length: size }, () => factory());
    this.free = new Array(size).fill(true);
    this.queue = [];
  }

  async getInstance() {
    for (let i = 0; i < this.instances.length; i++) {
      if (this.free[i]) { this.free[i] = false; return this.instances[i]; }
    }
    return new Promise((resolve) => this.queue.push(resolve));
  }

  release(instance) {
    const i = this.instances.indexOf(instance);
    if (this.queue.length > 0) this.queue.shift()(instance);
    else this.free[i] = true;
  }
}
```

Conception : la factory est passée au constructeur (et non des instances préfabriquées) afin que le pool puisse grandir à la demande.

### Flyweight (optimisation des timers) {#flyweight-timer-optimization}

Problème : 2 millions d'appels à `setInterval` sont extrêmement coûteux.

```js
class Interval {
  static cache = new Map();
  constructor(duration, callback) {
    const cached = Interval.cache.get(duration);
    if (cached) { cached.callbacks.push(callback); return Object.setPrototypeOf(this, cached); }
    this.callbacks = [callback];
    this.timer = setInterval(() => { for (const cb of this.callbacks) cb(); }, duration);
    Interval.cache.set(duration, this);
  }
}
```

Résultat : 2 millions d'instances, mais seulement 2 appels réels à `setInterval` (un par durée unique). Compromis : dispatch polymorphe dans V8 (2 CMP supplémentaires par `new`).

## Patrons structurels {#structural-patterns}

### Adapter vs Facade vs Proxy {#adapter-vs-facade-vs-proxy}

| Patron | Enveloppe | Interface | Objectif |
|---------|-----------|-----------|----------|
| **Adapter** | UNE abstraction | Modifie l'interface | Convertir des contrats (promisify, callbackify) |
| **Facade** | Un SOUS-SYSTÈME entier | Simplifie l'interface | Masquer les mécanismes internes complexes |
| **Proxy** | UNE abstraction | Même interface | Ajouter un comportement (cache, journalisation, contrôle d'accès) |

L'Adapter est extrêmement courant : la conversion de contrats asynchrones est omniprésente dans Node.js.

### Observer / Observable {#observer-observable}

```js
class Observable {
  #observers = [];
  subscribe(observer) { this.#observers.push(observer); }
  notify(data) { for (const o of this.#observers) o.update(data); }
  complete() { for (const o of this.#observers) o.complete?.(); }
}
```

Simplification JavaScript : utilisez de simples fonctions de rappel au lieu de classes Observer abstraites. Les **Signals** (frameworks modernes) dérivent également d'Observable.

## Patrons comportementaux {#behavioral-patterns}

### Strategy {#strategy}

```js
const renderers = {
  console: (data) => console.table(data),
  web: (data) => `<table>${data.map(r => `<tr><td>${r.name}</td></tr>`).join('')}</table>`,
  markdown: (data) => data.map(r => `| ${r.name} |`).join('\n'),
};
const createContext = (type) => ({ process: (data) => renderers[type](data) });
```

En JS, une stratégie peut être : une fonction, une classe, un objet ou un module.

### State {#state}

```js
const states = {
  idle: { process: () => { /* idle behavior */ }, next: 'processing' },
  processing: { process: () => { /* work */ }, next: 'complete' },
  complete: { process: () => { /* noop */ }, next: 'idle' },
};
```

### Chain of Responsibility {#chain-of-responsibility}

Le middleware dans Express/Fastify en est une implémentation pratique. Chaque gestionnaire décide s'il traite la requête ou la transmet à `next()`.

### Command (avec le modèle Actor) {#command-with-actor-model}

Dans le modèle Actor, les messages sont des commandes ; la file de messages de l'acteur est une file de commandes. Combiné à la capacité d'annulation (undo), il permet un comportement de type transactionnel.

## Équivalents fonctionnels {#fp-equivalents}

| Patron GoF | Équivalent fonctionnel |
|-------------|--------------|
| Strategy | Passer une fonction en argument |
| Observer | Composition de callbacks |
| Decorator | Enveloppement de fonctions |
| Chain of Responsibility | Pipeline de fonctions |

## Pièges {#gotchas}

- Les Facades tendent à se transformer en God Objects avec le temps : il faut de la discipline pour garder une interface minimale
- Un Adapter peut avoir plusieurs entrées/sorties (un adaptateur USB-C vers USB-A + Lightning reste un adaptateur)
- Principe de Pareto : ~20 % des patrons couvrent ~80 % des cas d'usage. Concentrez-vous sur ceux que vous utiliserez réellement
- Tous les paradigmes sont très variables en interne : il n'existe pas de « manière POO » ou de « manière FP » unique

## Voir aussi {#see-also}

- [[solid-and-grasp]] - principes qui guident le choix des patrons
- [[async-patterns]] - promisify/callbackify comme patron Adapter
- [[dependency-injection]] - DI vs patrons du système de modules
- [[closures-and-scope]] - les closures comme fondement de nombreux patrons
