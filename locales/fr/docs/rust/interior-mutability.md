---
title: "Mutabilité intérieure"
category: concepts
tags: [refcell, cell, mutex, unsafe, borrowing]
level: 4
source_sha256: 3ba3b4a331642c0653cc70410e6cd39e5dbf9b3f43117375c4552a923763eaa4
translation: machine
translated_at: '2026-10-24'
---
# Mutabilité intérieure {#interior-mutability}

Motif permettant de modifier des données derrière des références partagées (`&T`). Il contourne la vérification des emprunts à la compilation au profit de vérifications à l'exécution. On l'utilise lorsque le compilateur ne peut pas prouver la sûreté de l'emprunt, alors que le programmeur le peut.

## Points clés {#key-facts}

- Rust classique : une référence partagée `&T` est en lecture seule, une référence exclusive `&mut T` est modifiable
- Mutabilité intérieure : modifier à travers un `&T` via des wrappers vérifiés à l'exécution
- `Cell<T>` : fondé sur la copie, sans emprunt. Réservé aux types `T: Copy`
- `RefCell<T>` : vérification des emprunts à l'exécution. Provoque une panique en cas de violation
- `Mutex<T>` : mutabilité intérieure thread-safe par verrouillage
- `RwLock<T>` : plusieurs lecteurs OU un seul écrivain, thread-safe
- `AtomicT` : mutabilité intérieure sans verrou pour les types primitifs
- `UnsafeCell<T>` : fondement de toute mutabilité intérieure. Brut, sans garanties de sûreté

## Cell - Sémantique de copie {#cell-copy-semantics}

```rust
use std::cell::Cell;

let x = Cell::new(42);
// x is not mut, but we can change the inner value
x.set(100);
println!("{}", x.get()); // 100

// Useful in structs behind shared references
struct Counter {
    count: Cell<u32>,
}

impl Counter {
    fn increment(&self) {  // &self, not &mut self
        self.count.set(self.count.get() + 1);
    }
}
```

## RefCell - Vérification des emprunts à l'exécution {#refcell-runtime-borrow-checking}

```rust
use std::cell::RefCell;

let data = RefCell::new(vec![1, 2, 3]);

// Borrow immutably
{
    let borrowed = data.borrow();
    println!("{:?}", *borrowed);
}

// Borrow mutably
{
    let mut borrowed = data.borrow_mut();
    borrowed.push(4);
}

// PANIC: simultaneous mutable + immutable borrow
// let r1 = data.borrow();
// let r2 = data.borrow_mut();  // panics at runtime!
```

## Motif courant : Rc + RefCell {#common-pattern-rc-refcell}

```rust
use std::cell::RefCell;
use std::rc::Rc;

// Shared ownership + interior mutability
let shared = Rc::new(RefCell::new(vec![1, 2, 3]));

let clone1 = Rc::clone(&shared);
let clone2 = Rc::clone(&shared);

clone1.borrow_mut().push(4);
clone2.borrow_mut().push(5);

println!("{:?}", shared.borrow()); // [1, 2, 3, 4, 5]
```

## Thread-safe : Arc + Mutex {#thread-safe-arc-mutex}

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let data = Arc::new(Mutex::new(vec![1, 2, 3]));

let handles: Vec<_> = (0..3).map(|i| {
    let data = Arc::clone(&data);
    thread::spawn(move || {
        let mut lock = data.lock().unwrap();
        lock.push(i);
    })
}).collect();

for h in handles { h.join().unwrap(); }
println!("{:?}", data.lock().unwrap());
```

## Comparaison {#comparison}

| Type | Thread-safe | Surcoût | Paniques | Cas d'usage |
|------|------------|----------|--------|----------|
| `Cell<T>` | Non | Minimal (copie) | Jamais | Valeurs simples, compteurs |
| `RefCell<T>` | Non | Vérification d'emprunt à l'exécution | En cas de violation | Modifications complexes mono-thread |
| `Mutex<T>` | Oui | Acquisition du verrou | En cas d'empoisonnement | État partagé multi-thread |
| `RwLock<T>` | Oui | Acquisition du verrou | En cas d'empoisonnement | Multi-thread à forte proportion de lectures |
| `Atomic*` | Oui | Sans verrou | Jamais | Compteurs, drapeaux |

## Quand l'utiliser {#when-to-use}

- **Cell** : valeurs `Copy` simples que l'on doit modifier à travers `&self`
- **RefCell** : types complexes dans du code mono-thread lorsque le compilateur ne peut pas prouver la sûreté
- **Rc<RefCell<T>>** : propriété partagée + modification en code mono-thread (nœuds de graphe, caches)
- **Arc<Mutex<T>>** : propriété partagée + modification entre threads
- **OnceCell/LazyCell** : initialisation unique (stable depuis Rust 1.80)

## Pièges courants {#gotchas}

- **Problème :** appel de `RefCell::borrow_mut()` alors qu'un `borrow()` est actif -> panique à l'exécution -> **Correctif :** limiter la portée des emprunts. Utiliser des blocs `{}` pour libérer les emprunts tôt. Envisager `try_borrow_mut()` pour une variante qui ne panique pas.
- **Problème :** empoisonnement d'un `Mutex` après qu'un thread a paniqué en détenant le verrou -> **Correctif :** gérer avec `lock().unwrap_or_else(|e| e.into_inner())` pour récupérer, ou laisser l'erreur se propager. Envisager `parking_lot::Mutex`, qui n'a pas d'empoisonnement.
- **Problème :** utilisation de `RefCell` dans du code multi-thread -> erreur de compilation (`RefCell` est `!Sync`) -> **Correctif :** utiliser `Mutex` ou `RwLock` pour une mutabilité intérieure thread-safe.

## Voir aussi {#see-also}

- [[borrowing-and-references]] - règles d'emprunt à la compilation que la mutabilité intérieure assouplit
- [Pointeurs intelligents](smart-pointers.md) - Rc, Arc, Box
- [Concurrence](concurrency.md) - Mutex, RwLock, atomiques
