---
title: "Entwurfsmuster (GoF) in JavaScript"
category: patterns
tags: [nodejs, gof, design-patterns, factory, strategy, observer, adapter, facade, proxy, decorator]
level: 3
source_sha256: 4afff7b1532b86f49ea021fb3b5ec2a8dc1b83037d233e80b2311cb63274c55a
translation: machine
translated_at: '2026-10-24'
---
# Entwurfsmuster (GoF) in JavaScript {#design-patterns-gof-in-javascript}

Die Muster der Gang of Four lassen sich in JavaScript anders anwenden als in klassenbasierten Sprachen. Funktionen erster Klasse, Closures und dynamische Typisierung reduzieren viele Muster auf einfache Funktionen oder Objekte. In der funktionalen Programmierung lassen sich alle GoF-Muster auf Funktionskomposition zurückführen: `G(f(x))`. ~20 % der Muster decken ~80 % der realen Anwendungsfälle ab.

## Erzeugungsmuster {#creational-patterns}

### Factory Method {#factory-method}

Direkte `new`-Aufrufe durch Methodenaufrufe ersetzen, um polymorphe Instanziierung zu ermöglichen:

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

Entwurf: Die Factory wird an den Konstruktor übergeben (nicht vorgefertigte Instanzen), damit der Pool bei Bedarf wachsen kann.

### Flyweight (Timer-Optimierung) {#flyweight-timer-optimization}

Problem: 2 Millionen `setInterval`-Aufrufe sind extrem teuer.

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

Ergebnis: 2 Millionen Instanzen, aber nur 2 echte `setInterval`-Aufrufe (einer pro eindeutiger Dauer). Kompromiss: polymorphe V8-Dispatch-Kosten (2 zusätzliche CMP pro `new`).

## Strukturmuster {#structural-patterns}

### Adapter vs. Facade vs. Proxy {#adapter-vs-facade-vs-proxy}

| Muster | Kapselt | Schnittstelle | Zweck |
|--------|---------|---------------|-------|
| **Adapter** | EINE Abstraktion | Verändert die Schnittstelle | Verträge konvertieren (promisify, callbackify) |
| **Facade** | Ein gesamtes SUBSYSTEM | Vereinfacht die Schnittstelle | Komplexe interne Details verbergen |
| **Proxy** | EINE Abstraktion | Gleiche Schnittstelle | Verhalten hinzufügen (Caching, Logging, Zugriffskontrolle) |

Der Adapter ist außerordentlich verbreitet – die Konvertierung asynchroner Verträge ist in Node.js allgegenwärtig.

### Observer / Observable {#observer-observable}

```js
class Observable {
  #observers = [];
  subscribe(observer) { this.#observers.push(observer); }
  notify(data) { for (const o of this.#observers) o.update(data); }
  complete() { for (const o of this.#observers) o.complete?.(); }
}
```

JavaScript-Vereinfachung: Statt abstrakter Observer-Klassen einfache Callback-Funktionen verwenden. **Signals** (moderne Frameworks) basieren ebenfalls auf Observable.

## Verhaltensmuster {#behavioral-patterns}

### Strategy {#strategy}

```js
const renderers = {
  console: (data) => console.table(data),
  web: (data) => `<table>${data.map(r => `<tr><td>${r.name}</td></tr>`).join('')}</table>`,
  markdown: (data) => data.map(r => `| ${r.name} |`).join('\n'),
};
const createContext = (type) => ({ process: (data) => renderers[type](data) });
```

In JS kann eine Strategie eine Funktion, eine Klasse, ein Objekt oder ein Modul sein.

### State {#state}

```js
const states = {
  idle: { process: () => { /* idle behavior */ }, next: 'processing' },
  processing: { process: () => { /* work */ }, next: 'complete' },
  complete: { process: () => { /* noop */ }, next: 'idle' },
};
```

### Chain of Responsibility {#chain-of-responsibility}

Middleware in Express/Fastify ist eine praktische Implementierung. Jeder Handler entscheidet, ob er verarbeitet oder an `next()` weitergibt.

### Command (mit Actor-Modell) {#command-with-actor-model}

Im Actor-Modell sind Nachrichten Commands; die Nachrichtenwarteschlange des Actors ist eine Command-Queue. In Kombination mit Undo-Fähigkeit ermöglicht dies transaktionsähnliches Verhalten.

## FP-Äquivalente {#fp-equivalents}

| GoF-Muster | FP-Äquivalent |
|------------|---------------|
| Strategy | Übergabe einer Funktion als Argument |
| Observer | Callback-Komposition |
| Decorator | Funktions-Wrapping |
| Chain of Responsibility | Funktions-Pipeline |

## Stolperfallen {#gotchas}

- Facades wachsen mit der Zeit oft zu God Objects heran – es braucht Disziplin, die Schnittstelle minimal zu halten
- Ein Adapter kann mehrere Ein- und Ausgänge haben (USB-C auf USB-A + Lightning ist trotzdem ein Adapter)
- Pareto-Prinzip: ~20 % der Muster decken ~80 % der Anwendungsfälle ab – konzentriere dich auf die Muster, die du tatsächlich brauchst
- Alle Paradigmen sind intern sehr variabel – es gibt nicht den einen „OOP-Weg" oder den einen „FP-Weg"

## Siehe auch {#see-also}

- [[solid-and-grasp]] - Prinzipien hinter der Musterauswahl
- [[async-patterns]] - promisify/callbackify als Adapter-Muster
- [[dependency-injection]] - DI vs. Modulsystem-Muster
- [[closures-and-scope]] - Closures als Grundlage vieler Muster
