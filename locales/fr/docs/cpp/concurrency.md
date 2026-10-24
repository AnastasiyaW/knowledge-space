---
title: "Concurrence - Threads, Async, Atomics"
category: concepts
tags: [cpp, threads, async, mutex, atomic, concurrency, cpp11, cpp20]
level: 4
source_sha256: d73aeba93ecf607dc4af7f828091b4bedc98fdaeaeb9fd4911f69941b406b667
translation: machine
translated_at: '2026-10-24'
---
# Concurrence - Threads, Async, Atomics {#concurrency-threads-async-atomics}

Primitives de threading standard C++ : `std::thread`, `std::async`, `std::mutex`, `std::atomic`, `std::condition_variable`. Abstractions portables et sans surcoût au-dessus du threading du système d'exploitation.

## Faits clés {#key-facts}

- `<thread>` - `std::thread`, `std::jthread` (C++20, jonction automatique)
- `<mutex>` - `mutex`, `recursive_mutex`, `shared_mutex` (C++17), gardes de verrou
- `<atomic>` - opérations atomiques sans verrou, `std::atomic<T>`
- `<future>` - `std::async`, `std::future`, `std::promise`, `std::packaged_task`
- `<condition_variable>` - signalisation entre threads, wait/notify
- `std::thread` doit avoir subi un `join()` ou un `detach()` avant sa destruction, sinon appel à `std::terminate`
- `std::jthread` (C++20) - se joint automatiquement dans son destructeur, supporte l'annulation coopérative via `stop_token`
- `std::async(std::launch::async, ...)` garantit un nouveau thread ; `std::launch::deferred` est paresseux
- Data race = UB en C++. Au moins une écriture + accès concurrent sans synchronisation = comportement indéfini
- `std::atomic<T>` - sans verrou pour les petits types (int, pointeur), fournit un ordonnancement happens-before
- `std::shared_mutex` (C++17) - plusieurs lecteurs OU un seul écrivain

## Patrons {#patterns}

### Threading de base {#basic-threading}

```cpp
#include <thread>

void worker(int id, const std::string& msg) {
    std::cout << "Thread " << id << ": " << msg << '\n';
}

// Launch threads
std::thread t1(worker, 1, "hello");
std::thread t2(worker, 2, "world");

t1.join();  // wait for completion
t2.join();

// C++20: jthread - auto-joining
std::jthread jt([](std::stop_token st) {
    while (!st.stop_requested()) {
        // do work
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
});
// jt automatically joins when destroyed
```

### Mutex et verrous {#mutex-and-locks}

```cpp
#include <mutex>

std::mutex mtx;
int shared_counter = 0;

void increment() {
    std::lock_guard lock(mtx);  // CTAD, C++17
    ++shared_counter;
}  // automatically unlocked

// Multiple mutexes - avoid deadlock
std::mutex m1, m2;
void safe_swap() {
    std::scoped_lock lock(m1, m2);  // C++17, deadlock-free
    // swap protected data
}

// Reader-writer lock (C++17)
std::shared_mutex rw_mtx;

void reader() {
    std::shared_lock lock(rw_mtx);  // multiple readers OK
    // read shared data
}

void writer() {
    std::unique_lock lock(rw_mtx);  // exclusive access
    // modify shared data
}
```

### async/future {#asyncfuture}

```cpp
#include <future>

// Launch async task
auto future = std::async(std::launch::async, [] {
    std::this_thread::sleep_for(std::chrono::seconds(1));
    return 42;
});

// Do other work...

int result = future.get();  // blocks until ready

// Promise/future pair for manual control
std::promise<int> prom;
std::future<int> fut = prom.get_future();

std::thread t([&prom] {
    prom.set_value(compute_result());
});

int val = fut.get();
t.join();
```

### Opérations atomiques {#atomic-operations}

```cpp
#include <atomic>

std::atomic<int> counter{0};
std::atomic<bool> ready{false};

void producer() {
    // prepare data...
    ready.store(true, std::memory_order_release);
}

void consumer() {
    while (!ready.load(std::memory_order_acquire)) {
        std::this_thread::yield();
    }
    // data is ready
}

// Atomic increment - thread-safe without mutex
void count() {
    counter.fetch_add(1, std::memory_order_relaxed);
    // or simply:
    ++counter;  // uses sequentially consistent ordering
}
```

### Variable de condition {#condition-variable}

```cpp
std::mutex mtx;
std::condition_variable cv;
std::queue<int> work_queue;
bool done = false;

void producer() {
    for (int i = 0; i < 10; ++i) {
        {
            std::lock_guard lock(mtx);
            work_queue.push(i);
        }
        cv.notify_one();
    }
    {
        std::lock_guard lock(mtx);
        done = true;
    }
    cv.notify_all();
}

void consumer() {
    while (true) {
        std::unique_lock lock(mtx);
        cv.wait(lock, [] { return !work_queue.empty() || done; });
        if (work_queue.empty() && done) break;
        int item = work_queue.front();
        work_queue.pop();
        lock.unlock();
        process(item);
    }
}
```

## Pièges courants {#gotchas}

- **Problème :** Oublier de `join()` ou `detach()` un `std::thread` -> appel de `std::terminate` -> **Solution :** Utiliser `std::jthread` (C++20) ou garantir join/detach dans tous les chemins d'exécution, y compris en cas d'exception
- **Problème :** Verrouiller plusieurs mutex dans un ordre différent -> interblocage -> **Solution :** Utiliser `std::scoped_lock(m1, m2)` (C++17), qui emploie un algorithme d'évitement d'interblocage
- **Problème :** `std::async` avec la politique par défaut peut s'exécuter de manière différée (même thread) -> **Solution :** Utiliser explicitement `std::launch::async` si un nouveau thread est nécessaire
- **Problème :** Réveils parasites de la variable de condition -> **Solution :** Toujours utiliser la forme avec prédicat : `cv.wait(lock, predicate)`
- **Problème :** Entrelacement de `std::cout` provenant de plusieurs threads -> sortie corrompue -> **Solution :** Utiliser `std::osyncstream` (C++20) ou protéger l'accès par un mutex

## Voir aussi {#see-also}

- [[raii-resource-management]]
- [Gestion des erreurs - Exceptions et alternatives](error-handling.md)
- [Optimisation des performances](performance-optimization.md)
- [cppreference : Support des threads](https://en.cppreference.com/w/cpp/thread)
