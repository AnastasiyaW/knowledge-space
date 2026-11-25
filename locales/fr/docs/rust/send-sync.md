---
title: "Traits Send et Sync"
category: concepts
tags: [concurrency, thread-safety, marker-traits, auto-traits]
level: 4
source_sha256: 5ba645550b8f5787b171c20376106bc16eaca6664f685cac883565006dd13a7b
translation: machine
translated_at: '2026-10-24'
---
# Traits Send et Sync {#send-and-sync-traits}

Traits marqueurs qui encodent au niveau des types les garanties de sûreté entre threads. Le compilateur s'en sert pour empêcher les data races à la compilation, c'est le mécanisme clé de Rust pour la sûreté de la concurrence.

## Points clés {#key-facts}

- `Send` : le type peut être transféré à un autre thread (transfert de propriété à travers la frontière d'un thread)
- `Sync` : le type peut être partagé entre threads via une référence partagée (`&T` est `Send` si et seulement si `T` est `Sync`)
- Les deux sont des auto-traits : le compilateur les implémente automatiquement lorsque tous les champs sont `Send`/`Sync`
- Les deux sont des traits marqueurs : aucune méthode, uniquement une information à la compilation
- Presque tous les types sont `Send` + `Sync`. Exceptions notables : `Rc<T>`, `RefCell<T>`, les pointeurs bruts
- Implémenter manuellement `Send`/`Sync` est `unsafe` : vous affirmez que les invariants sont respectés

## Règles {#rules}

| T est... | Signification |
|----------|---------------|
| `Send` | Il est sûr de déplacer `T` vers un autre thread |
| `!Send` | Doit rester sur le thread qui l'a créé |
| `Sync` | Il est sûr que plusieurs threads détiennent `&T` simultanément |
| `!Sync` | Un seul thread peut référencer la valeur à la fois |

Règle dérivée : `T: Sync` si et seulement si `&T: Send`

## Types courants {#common-types}

| Type | Send | Sync | Pourquoi |
|------|------|------|----------|
| `i32`, `String`, `Vec<T>` | Oui | Oui | Aucun état mutable partagé |
| `Rc<T>` | Non | Non | Compteur de références non atomique |
| `Arc<T>` | Oui | Oui | Compteur de références atomique |
| `RefCell<T>` | Oui | Non | La vérification des emprunts à l'exécution n'est pas thread-safe |
| `Mutex<T>` | Oui | Oui | Le verrou sérialise les accès |
| `Cell<T>` | Oui | Non | Mutation interne non atomique |
| `*const T`, `*mut T` | Non | Non | Pointeurs bruts : aucune garantie |
| `MutexGuard<T>` | Non | Oui | Doit être déverrouillé sur le même thread |

## Patrons {#patterns}

### Le spawn de thread exige Send {#thread-spawn-requires-send}

```rust
use std::thread;

let data = vec![1, 2, 3];
// Vec is Send, so this works:
thread::spawn(move || {
    println!("{:?}", data);
});

// Rc is !Send, so this fails:
// use std::rc::Rc;
// let rc = Rc::new(42);
// thread::spawn(move || {
//     println!("{}", rc);  // ERROR: Rc<i32> cannot be sent between threads
// });
```

### L'état partagé exige Sync {#shared-state-requires-sync}

```rust
use std::sync::Arc;
use std::thread;

// Arc<T> is Send + Sync when T: Send + Sync
let shared = Arc::new(vec![1, 2, 3]);

let handles: Vec<_> = (0..3).map(|_| {
    let data = Arc::clone(&shared);
    thread::spawn(move || {
        println!("{:?}", data);  // &Vec is Send because Vec is Sync
    })
}).collect();
```

### Closure move et Send {#move-closure-and-send}

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));

let handles: Vec<_> = (0..10).map(|_| {
    let counter = Arc::clone(&counter);
    thread::spawn(move || {
        // Mutex makes interior mutation Sync
        let mut num = counter.lock().unwrap();
        *num += 1;
    })
}).collect();

for h in handles { h.join().unwrap(); }
println!("{}", *counter.lock().unwrap()); // 10
```

### Implémentation unsafe de Send/Sync {#unsafe-sendsync-implementation}

```rust
struct MyWrapper(*mut u8);

// UNSAFE: you guarantee thread-safety invariants
unsafe impl Send for MyWrapper {}
unsafe impl Sync for MyWrapper {}
```

## Implémentations négatives {#negative-implementations}

```rust
// How Rc opts out of Send/Sync (in std):
// impl<T> !Send for Rc<T> {}
// impl<T> !Sync for Rc<T> {}

// You can't write negative impls in stable Rust.
// Use PhantomData to opt out:
use std::marker::PhantomData;
use std::cell::Cell;

struct NotSync {
    _marker: PhantomData<Cell<()>>,  // Cell is !Sync
}
```

## Tableau de décision {#decision-table}

| Besoin | Utiliser |
|--------|----------|
| Données partagées en lecture seule entre threads | `Arc<T>` où `T: Sync` |
| Données partagées et modifiables entre threads | `Arc<Mutex<T>>` ou `Arc<RwLock<T>>` |
| Propriété partagée dans un seul thread | `Rc<T>` |
| Mutabilité interne dans un seul thread | `RefCell<T>` ou `Cell<T>` |
| Transférer la propriété à un thread | Tout type `Send` via une closure `move` |

## Pièges {#gotchas}

- **Problème :** `Rc<T>` à l'intérieur d'une closure passée à `thread::spawn` ne compile pas -> **Solution :** remplacer `Rc` par `Arc`. `Arc` est la version thread-safe, avec compteur de références atomique.
- **Problème :** `RefCell<T>` partagé via `Arc` échoue (`RefCell` est `!Sync`) -> **Solution :** utiliser `Arc<Mutex<T>>` ou `Arc<RwLock<T>>` à la place. `Mutex` fournit une mutabilité interne thread-safe.
- **Problème :** `MutexGuard` conservé à travers un point `.await` dans du code asynchrone -> **Solution :** `MutexGuard` est `!Send`, ce qui empêche les tâches asynchrones de changer de thread. Libérer le guard avant `.await`, ou utiliser `tokio::sync::Mutex`.

## Voir aussi {#see-also}

- [Concurrence](concurrency.md) - threads, canaux, état partagé
- [[interior-mutability]] - Cell, RefCell, Mutex
- [Pointeurs intelligents](smart-pointers.md) - Rc vs Arc
- [[async-await]] - bornes Send dans les contextes asynchrones
