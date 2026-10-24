---
title: "Concurrence"
category: concepts
tags: [rust, concurrency, threads, send, sync, arc, mutex, channels, c10k]
level: 4
source_sha256: d73ab3a7ef52b65ab374698b5cab67ed055814fac2b06eea5007c7db477e204e
translation: machine
translated_at: '2026-10-24'
---
# Concurrence {#concurrency}

Le système de types de Rust empêche les data races à la compilation grâce aux marqueurs de traits `Send` et `Sync`. Combiné à `Arc<Mutex<T>>` pour l'état partagé et aux canaux pour le passage de messages, Rust offre une concurrence sans crainte : si ça compile, c'est exempt de data races.

## Points clés {#key-facts}

- **Coût d'un thread :** pile de 2 à 8 MB, ~10 à 20 KB de structures noyau, ~100 us pour la création, ~1 à 10 us par changement de contexte
- Avec 16 GB de RAM et une pile de 2 MB : ~8 000 threads au maximum
- **Problème C10K** (Dan Kegel, 1999) : 10 000 connexions = 20 GB de pile + 50 ms/s de changements de contexte
- Requête HTTP typique : 94 % du temps passé à ATTENDRE les E/S (requêtes BD, lectures de fichiers)
- **Send** = type transférable entre threads (la plupart des types)
- **Sync** = type partageable via `&T` entre threads (la plupart des types)
- `Rc<T>` n'est ni Send ni Sync (utiliser `Arc<T>`)
- `Cell<T>` et `RefCell<T>` sont Send mais PAS Sync

## Problèmes de concurrence {#concurrency-problems}

- **Conditions de course (race conditions) :** le résultat dépend d'un ordre d'exécution imprévisible
- **État incohérent :** lecture pendant une modification incomplète
- **Mises à jour perdues :** deux threads effectuent une lecture-modification-écriture, et l'une est écrasée

## Patterns {#patterns}

### Création de threads {#thread-spawning}

```rust
use std::thread;

let handle = thread::spawn(|| {
    println!("Hello from a thread!");
});
handle.join().unwrap();
```

### Arc + Mutex (état partagé) {#arc-mutex-shared-state}

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    handles.push(thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    }));
}

for handle in handles { handle.join().unwrap(); }
println!("Count: {}", *counter.lock().unwrap());
```

### Canaux (passage de messages) {#channels-message-passing}

```rust
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();
let tx2 = tx.clone();

thread::spawn(move || { tx.send("from thread 1").unwrap(); });
thread::spawn(move || { tx2.send("from thread 2").unwrap(); });

for msg in rx { println!("{msg}"); }
```

### RwLock (plusieurs lecteurs, un seul écrivain) {#rwlock-many-readers-one-writer}

```rust
use std::sync::RwLock;

let lock = RwLock::new(5);
{
    let r1 = lock.read().unwrap();
    let r2 = lock.read().unwrap(); // multiple readers OK
}
{
    let mut w = lock.write().unwrap(); // exclusive writer
    *w += 1;
}
```

## Pièges {#gotchas}

- `Mutex::lock()` peut provoquer un interblocage (deadlock) si vous acquérez plusieurs verrous dans un ordre différent selon les threads
- `Arc::clone()` est peu coûteux (incrémentation d'un compteur atomique), mais `Mutex::lock()` a un surcoût
- Les pointeurs bruts (`*const T`, `*mut T`) ne sont ni Send ni Sync : utilisez `unsafe` pour outrepasser cette restriction si vous savez que c'est sûr
- Mutex empoisonné : si un thread panique en tenant un verrou, le mutex est empoisonné et les appels suivants à `lock()` renvoient `Err`

## Voir aussi {#see-also}

- [[async-await]] - alternative asynchrone aux threads pour les charges liées aux E/S
- [Pointeurs intelligents](smart-pointers.md) - Arc, Rc et comptage de références
- [[ownership-and-move-semantics]] - closures `move` pour la création de threads
