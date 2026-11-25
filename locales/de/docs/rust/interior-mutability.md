---
title: "Innere Veränderlichkeit"
category: concepts
tags: [refcell, cell, mutex, unsafe, borrowing]
level: 4
source_sha256: 3ba3b4a331642c0653cc70410e6cd39e5dbf9b3f43117375c4552a923763eaa4
translation: machine
translated_at: '2026-10-24'
---
# Innere Veränderlichkeit {#interior-mutability}

Muster, das die Veränderung von Daten hinter geteilten Referenzen (`&T`) erlaubt. Es umgeht die Borrow-Prüfung zur Compile-Zeit zugunsten von Prüfungen zur Laufzeit. Es wird eingesetzt, wenn der Compiler die Sicherheit einer Ausleihe nicht beweisen kann, der Programmierer aber schon.

## Wichtige Fakten {#key-facts}

- Normales Rust: geteilte Referenz `&T` = nur lesbar, exklusive Referenz `&mut T` = veränderbar
- Innere Veränderlichkeit: Veränderung über `&T` mithilfe von Wrappern mit Prüfung zur Laufzeit
- `Cell<T>`: kopierbasiert, keine Ausleihe. Nur für Typen mit `T: Copy`
- `RefCell<T>`: Borrow-Prüfung zur Laufzeit. Löst bei einer Verletzung eine Panic aus
- `Mutex<T>`: thread-sichere innere Veränderlichkeit über Sperren
- `RwLock<T>`: mehrere Leser ODER ein Schreiber, thread-sicher
- `AtomicT`: sperrenfreie innere Veränderlichkeit für primitive Typen
- `UnsafeCell<T>`: Grundlage aller inneren Veränderlichkeit. Roh, ohne Sicherheitsgarantien

## Cell - Copy-Semantik {#cell-copy-semantics}

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

## RefCell - Borrow-Prüfung zur Laufzeit {#refcell-runtime-borrow-checking}

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

## Häufiges Muster: Rc + RefCell {#common-pattern-rc-refcell}

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

## Thread-sicher: Arc + Mutex {#thread-safe-arc-mutex}

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

## Vergleich {#comparison}

| Typ | Thread-sicher | Overhead | Panics | Anwendungsfall |
|------|------------|----------|--------|----------|
| `Cell<T>` | Nein | Minimal (Kopie) | Nie | Einfache Werte, Zähler |
| `RefCell<T>` | Nein | Borrow-Prüfung zur Laufzeit | Bei Verletzung | Komplexe Veränderung in einem Thread |
| `Mutex<T>` | Ja | Sperrenerwerb | Bei Poisoning | Gemeinsamer Zustand über mehrere Threads |
| `RwLock<T>` | Ja | Sperrenerwerb | Bei Poisoning | Leselastig, mehrere Threads |
| `Atomic*` | Ja | Sperrenfrei | Nie | Zähler, Flags |

## Wann verwenden {#when-to-use}

- **Cell**: einfache `Copy`-Werte, die über `&self` verändert werden müssen
- **RefCell**: komplexe Typen in Single-Thread-Code, in dem der Compiler die Sicherheit nicht beweisen kann
- **Rc<RefCell<T>>**: geteilter Besitz + Veränderung in Single-Thread-Code (Graph-Knoten, Caches)
- **Arc<Mutex<T>>**: geteilter Besitz + Veränderung über Threads hinweg
- **OnceCell/LazyCell**: einmalige Initialisierung (stabil seit Rust 1.80)

## Fallstricke {#gotchas}

- **Problem:** `RefCell::borrow_mut()` wird aufgerufen, während `borrow()` aktiv ist -> Panic zur Laufzeit -> **Lösung:** Ausleih-Gültigkeitsbereiche kurz halten. Blöcke `{}` verwenden, um Ausleihen früh freizugeben. Für eine nicht panikende Variante `try_borrow_mut()` in Betracht ziehen.
- **Problem:** `Mutex`-Poisoning, wenn ein Thread beim Halten der Sperre paniert -> **Lösung:** Mit `lock().unwrap_or_else(|e| e.into_inner())` behandeln, um sich zu erholen, oder die Panic weiterreichen lassen. `parking_lot::Mutex` in Betracht ziehen, das kein Poisoning kennt.
- **Problem:** `RefCell` in Multi-Thread-Code verwenden -> Compilerfehler (`RefCell` ist `!Sync`) -> **Lösung:** `Mutex` oder `RwLock` für thread-sichere innere Veränderlichkeit verwenden.

## Siehe auch {#see-also}

- [[borrowing-and-references]] - Borrow-Regeln zur Compile-Zeit, die die innere Veränderlichkeit lockert
- [Smart Pointers](smart-pointers.md) - Rc, Arc, Box
- [Nebenläufigkeit](concurrency.md) - Mutex, RwLock, Atomics
