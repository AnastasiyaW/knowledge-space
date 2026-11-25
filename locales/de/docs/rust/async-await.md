---
title: "Async/Await"
category: concepts
tags: [rust, async, await, tokio, futures, runtime, io-bound]
level: 4
source_sha256: 16fbd11d1ab4f29ca009772c8c4a81f96f29b8a2dc6c6d6d23a7ba2c31f79f41
translation: machine
translated_at: '2026-10-24'
---
# Async/Await {#asyncawait}

Rusts Async-Modell bietet Zero-Cost-Abstraktionen für I/O-gebundene Nebenläufigkeit. Anders als Threads sind async Tasks leichtgewichtig (kein OS-Thread pro Task), weshalb sie sich ideal für die Verarbeitung von Tausenden gleichzeitiger Verbindungen eignen. Die `async`/`await`-Syntax wird zu Zustandsautomaten kompiliert und benötigt zur Ausführung eine Runtime (tokio, async-std).

## Wichtige Fakten {#key-facts}

- `async fn` gibt `impl Future<Output = T>` zurück - lazy, tut nichts, bis es gepollt wird
- `await` hält die Ausführung an, bis das Future abgeschlossen ist, und gibt die Kontrolle an den Executor zurück
- **Keine eingebaute Runtime** - man muss wählen: tokio (am verbreitetsten), async-std, smol
- Futures sind vom Compiler erzeugte Zustandsautomaten - in einfachen Fällen keine Heap-Allokation
- Async eignet sich für I/O-gebundene Arbeit; für CPU-gebundene Arbeit werden Threads verwendet (`spawn_blocking`)
- `Pin<T>` verhindert, dass selbstreferenzielle Futures nach dem ersten Poll verschoben werden

## Tokio Runtime {#tokio-runtime}

```rust
#[tokio::main]
async fn main() {
    let result = fetch_data("https://api.example.com").await;
    println!("{result}");
}

async fn fetch_data(url: &str) -> String {
    let response = reqwest::get(url).await.unwrap();
    response.text().await.unwrap()
}
```

## Muster {#patterns}

### Nebenläufige Tasks {#concurrent-tasks}

```rust
use tokio::task;

// Spawn independent tasks
let handle1 = task::spawn(async { fetch_users().await });
let handle2 = task::spawn(async { fetch_orders().await });

// Wait for both
let (users, orders) = tokio::join!(handle1, handle2);
```

### Select (Erster Abschluss) {#select-first-to-complete}

```rust
tokio::select! {
    result = fetch_from_primary() => handle_primary(result),
    result = fetch_from_backup() => handle_backup(result),
    _ = tokio::time::sleep(Duration::from_secs(5)) => timeout(),
}
```

### Streams (asynchrone Iteratoren) {#streams-async-iterators}

```rust
use tokio_stream::StreamExt;

let mut stream = tokio_stream::iter(vec![1, 2, 3]);
while let Some(value) = stream.next().await {
    println!("{value}");
}
```

## Fallstricke {#gotchas}

- `async` kann nicht direkt in Traits verwendet werden (stabil seit Rust 1.75 mit RPITIT)
- Ein `MutexGuard`, der über einen `.await` hinweg gehalten wird, kann zu einem Deadlock führen - stattdessen `tokio::sync::Mutex` statt `std::sync::Mutex` verwenden
- Für mit `tokio::spawn` gestartete Futures ist die Bedingung `Send` erforderlich - alle erfassten Daten müssen `Send` sein
- Async-Rekursion erfordert `Box::pin()`, um eine unendlich große Future-Größe zu vermeiden

## Siehe auch {#see-also}

- [Nebenläufigkeit](concurrency.md) - threadbasierte Nebenläufigkeit, Send/Sync-Traits
- [Fehlerbehandlung](error-handling.md) - Propagierung von async-Fehlern mit `?`
- [[rust-tooling]] - tokio, reqwest und Crates des async-Ökosystems
