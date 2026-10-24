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

Le modèle async de Rust fournit des abstractions à coût nul pour la concurrence liée aux E/S. Contrairement aux threads, les tâches async sont légères (pas de thread OS par tâche), ce qui les rend idéales pour gérer des milliers de connexions concurrentes. La syntaxe `async`/`await` se compile en machines à états, nécessitant un runtime (tokio, async-std) pour l'exécution.

## Key Facts {#key-facts}

- `async fn` renvoie `impl Future<Output = T>` - paresseux, ne fait rien tant qu'il n'est pas interrogé (polled)
- `await` suspend l'exécution jusqu'à ce que le future soit terminé, en cédant la main à l'executor
- **Pas de runtime intégré** - il faut choisir : tokio (le plus populaire), async-std, smol
- Les futures sont des machines à états générées par le compilateur - aucune allocation sur le tas pour les cas simples
- L'async est destiné aux tâches liées aux E/S ; utiliser des threads (`spawn_blocking`) pour les tâches liées au CPU
- `Pin<T>` empêche de déplacer des futures auto-référencés après le premier poll

## Runtime Tokio {#tokio-runtime}

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

## Motifs {#patterns}

### Tâches concurrentes {#concurrent-tasks}

```rust
use tokio::task;

// Spawn independent tasks
let handle1 = task::spawn(async { fetch_users().await });
let handle2 = task::spawn(async { fetch_orders().await });

// Wait for both
let (users, orders) = tokio::join!(handle1, handle2);
```

### Select (premier à se terminer) {#select-first-to-complete}

```rust
tokio::select! {
    result = fetch_from_primary() => handle_primary(result),
    result = fetch_from_backup() => handle_backup(result),
    _ = tokio::time::sleep(Duration::from_secs(5)) => timeout(),
}
```

### Streams (itérateurs asynchrones) {#streams-async-iterators}

```rust
use tokio_stream::StreamExt;

let mut stream = tokio_stream::iter(vec![1, 2, 3]);
while let Some(value) = stream.next().await {
    println!("{value}");
}
```

## Pièges {#gotchas}

- Impossible d'utiliser `async` directement dans les traits (stable depuis Rust 1.75 avec RPITIT)
- Garder un `MutexGuard` pendant un `.await` peut provoquer un deadlock - utiliser `tokio::sync::Mutex` plutôt que `std::sync::Mutex`
- La borne `Send` est requise pour les futures lancés avec `tokio::spawn` - toutes les données capturées doivent être `Send`
- La récursion async nécessite `Box::pin()` pour éviter une taille de future infinie

## Voir aussi {#see-also}

- [Concurrence](concurrency.md) - concurrence basée sur les threads, traits Send/Sync
- [Gestion des erreurs](error-handling.md) - propagation des erreurs async avec `?`
- [[rust-tooling]] - tokio, reqwest, et crates de l'écosystème async
