---
title: "Send- und Sync-Traits"
category: concepts
tags: [concurrency, thread-safety, marker-traits, auto-traits]
level: 4
source_sha256: 5ba645550b8f5787b171c20376106bc16eaca6664f685cac883565006dd13a7b
translation: machine
translated_at: '2026-10-24'
---
# Send- und Sync-Traits {#send-and-sync-traits}

Marker-Traits, die Thread-Sicherheitsgarantien auf Typebene kodieren. Der Compiler nutzt sie, um Data Races zur Compilezeit zu verhindern – Rusts zentraler Mechanismus für Sicherheit bei Nebenläufigkeit.

## Wichtige Fakten {#key-facts}

- `Send`: Ein Typ kann an einen anderen Thread übergeben werden (Ownership-Übergabe über Thread-Grenzen)
- `Sync`: Ein Typ kann über eine Shared Reference zwischen Threads geteilt werden (`&T` ist `Send` genau dann, wenn `T` `Sync` ist)
- Beide sind Auto-Traits: Der Compiler implementiert sie automatisch, wenn alle Felder `Send` bzw. `Sync` sind
- Beide sind Marker-Traits: Sie besitzen keine Methoden und enthalten rein Compile-Zeit-Information
- Nahezu alle Typen sind `Send` + `Sync`. Bemerkenswerte Ausnahmen: `Rc<T>`, `RefCell<T>`, Raw Pointer
- Das manuelle Implementieren von `Send`/`Sync` ist `unsafe` – du sicherst zu, dass die Invarianten gelten

## Regeln {#rules}

| T ist... | Bedeutung |
|---------|---------|
| `Send` | Sicher, `T` an einen anderen Thread zu verschieben |
| `!Send` | Muss auf dem erzeugenden Thread bleiben |
| `Sync` | Sicher, dass mehrere Threads gleichzeitig `&T` halten |
| `!Sync` | Nur ein Thread kann gleichzeitig darauf referenzieren |

Abgeleitete Regel: `T: Sync` genau dann, wenn `&T: Send`

## Häufige Typen {#common-types}

| Typ | Send | Sync | Grund |
|------|------|------|-----|
| `i32`, `String`, `Vec<T>` | Ja | Ja | Kein geteilter veränderlicher Zustand |
| `Rc<T>` | Nein | Nein | Nicht-atomarer Referenzzähler |
| `Arc<T>` | Ja | Ja | Atomarer Referenzzähler |
| `RefCell<T>` | Ja | Nein | Laufzeit-Borrow-Checking ist nicht thread-sicher |
| `Mutex<T>` | Ja | Ja | Das Lock serialisiert den Zugriff |
| `Cell<T>` | Ja | Nein | Nicht-atomare Interior Mutability |
| `*const T`, `*mut T` | Nein | Nein | Raw Pointer: keine Garantien |
| `MutexGuard<T>` | Nein | Ja | Muss auf demselben Thread entsperrt werden |

## Muster {#patterns}

### Thread-Spawn erfordert Send {#thread-spawn-requires-send}

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

### Geteilter Zustand erfordert Sync {#shared-state-requires-sync}

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

### Move-Closure und Send {#move-closure-and-send}

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

### Unsichere Implementierung von Send/Sync {#unsafe-sendsync-implementation}

```rust
struct MyWrapper(*mut u8);

// UNSAFE: you guarantee thread-safety invariants
unsafe impl Send for MyWrapper {}
unsafe impl Sync for MyWrapper {}
```

## Negative Implementierungen {#negative-implementations}

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

## Entscheidungstabelle {#decision-table}

| Bedarf | Verwendung |
|------|------|
| Geteilte, nur lesbare Daten über Threads hinweg | `Arc<T>` mit `T: Sync` |
| Geteilte, veränderliche Daten über Threads hinweg | `Arc<Mutex<T>>` oder `Arc<RwLock<T>>` |
| Geteiltes Ownership innerhalb eines Threads | `Rc<T>` |
| Interior Mutability innerhalb eines Threads | `RefCell<T>` oder `Cell<T>` |
| Ownership an einen Thread übergeben | Alles, was `Send` ist, über eine `move`-Closure |

## Stolperfallen {#gotchas}

- **Problem:** `Rc<T>` innerhalb einer `thread::spawn`-Closure lässt sich nicht kompilieren -> **Lösung:** `Rc` durch `Arc` ersetzen. `Arc` ist die thread-sichere Variante mit atomarem Referenzzähler.
- **Problem:** `RefCell<T>`, geteilt über `Arc`, schlägt fehl (`RefCell` ist `!Sync`) -> **Lösung:** Stattdessen `Arc<Mutex<T>>` oder `Arc<RwLock<T>>` verwenden. `Mutex` bietet thread-sichere Interior Mutability.
- **Problem:** `MutexGuard` wird in asynchronem Code über einen `.await`-Punkt hinweg gehalten -> **Lösung:** `MutexGuard` ist `!Send`, wodurch async Tasks nicht zwischen Threads wechseln können. Den Guard vor `.await` droppen oder `tokio::sync::Mutex` verwenden.

## Siehe auch {#see-also}

- [Concurrency](concurrency.md) - Threads, Channels, geteilter Zustand
- [[interior-mutability]] - Cell, RefCell, Mutex
- [Smart Pointers](smart-pointers.md) - Rc vs. Arc
- [[async-await]] - Send-Bounds in asynchronen Kontexten
