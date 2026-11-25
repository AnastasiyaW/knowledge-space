---
title: "Nebenläufigkeit"
category: concepts
tags: [rust, concurrency, threads, send, sync, arc, mutex, channels, c10k]
level: 4
source_sha256: d73ab3a7ef52b65ab374698b5cab67ed055814fac2b06eea5007c7db477e204e
translation: machine
translated_at: '2026-10-24'
---
# Nebenläufigkeit {#concurrency}

Rusts Typsystem verhindert Data Races zur Compilezeit über die Marker-Traits `Send` und `Sync`. Zusammen mit `Arc<Mutex<T>>` für geteilten Zustand und Channels für den Nachrichtenaustausch bietet Rust furchtlose Nebenläufigkeit: Wenn es kompiliert, ist es frei von Data Races.

## Wichtige Fakten {#key-facts}

- **Thread-Overhead:** 2-8 MB Stack, ~10-20 KB Kernel-Strukturen, ~100 us Erzeugung, ~1-10 us Kontextwechsel
- Bei 16 GB RAM und 2 MB Stack: maximal ~8.000 Threads
- **C10K-Problem** (Dan Kegel, 1999): 10.000 Verbindungen = 20 GB Stack + 50 ms/s Kontextwechsel
- Typische HTTP-Anfrage: 94 % der Zeit wird WARTEND auf I/O verbracht (DB-Abfragen, Dateilesezugriffe)
- **Send** = Typ kann zwischen Threads übertragen werden (die meisten Typen)
- **Sync** = Typ kann über `&T` zwischen Threads geteilt werden (die meisten Typen)
- `Rc<T>` ist weder Send noch Sync (stattdessen `Arc<T>` verwenden)
- `Cell<T>` und `RefCell<T>` sind Send, aber NICHT Sync

## Probleme der Nebenläufigkeit {#concurrency-problems}

- **Race Conditions:** Ergebnis hängt von einer nicht vorhersagbaren Ausführungsreihenfolge ab
- **Inkonsistenter Zustand:** Lesezugriff während einer unvollständigen Änderung
- **Verlorene Updates:** Zwei Threads lesen, modifizieren und schreiben, einer wird überschrieben

## Muster {#patterns}

### Thread-Erzeugung {#thread-spawning}

```rust
use std::thread;

let handle = thread::spawn(|| {
    println!("Hello from a thread!");
});
handle.join().unwrap();
```

### Arc + Mutex (geteilter Zustand) {#arc-mutex-shared-state}

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

### Channels (Nachrichtenaustausch) {#channels-message-passing}

```rust
use std::sync::mpsc;

let (tx, rx) = mpsc::channel();
let tx2 = tx.clone();

thread::spawn(move || { tx.send("from thread 1").unwrap(); });
thread::spawn(move || { tx2.send("from thread 2").unwrap(); });

for msg in rx { println!("{msg}"); }
```

### RwLock (viele Leser, ein Schreiber) {#rwlock-many-readers-one-writer}

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

## Fallstricke {#gotchas}

- `Mutex::lock()` kann zu einem Deadlock führen, wenn mehrere Locks in unterschiedlicher Reihenfolge über Threads hinweg gehalten werden
- `Arc::clone()` ist günstig (atomares Inkrementieren eines Zählers), `Mutex::lock()` hat hingegen Overhead
- Rohe Pointer (`*const T`, `*mut T`) sind weder Send noch Sync – mit `unsafe` lässt sich dies überschreiben, wenn man weiß, dass es sicher ist
- Vergiftetes Mutex: Wenn ein Thread beim Halten eines Locks panikt, wird das Mutex vergiftet – nachfolgende `lock()`-Aufrufe liefern `Err`

## Siehe auch {#see-also}

- [[async-await]] – asynchrone Alternative zu Threads für I/O-lastige Workloads
- [Smart Pointer](smart-pointers.md) – Arc, Rc und Referenzzählung
- [[ownership-and-move-semantics]] – `move`-Closures für das Erzeugen von Threads
