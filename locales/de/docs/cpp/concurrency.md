---
title: "Nebenläufigkeit - Threads, Async, Atomics"
category: concepts
tags: [cpp, threads, async, mutex, atomic, concurrency, cpp11, cpp20]
level: 4
source_sha256: d73aeba93ecf607dc4af7f828091b4bedc98fdaeaeb9fd4911f69941b406b667
translation: machine
translated_at: '2026-10-24'
---
# Nebenläufigkeit - Threads, Async, Atomics {#concurrency-threads-async-atomics}

Die standardisierten Threading-Primitive von C++: `std::thread`, `std::async`, `std::mutex`, `std::atomic`, `std::condition_variable`. Portable Abstraktionen über das Betriebssystem-Threading ohne zusätzlichen Overhead.

## Kernfakten {#key-facts}

- `<thread>` - `std::thread`, `std::jthread` (C++20, wird automatisch gejoint)
- `<mutex>` - `mutex`, `recursive_mutex`, `shared_mutex` (C++17), Lock-Guards
- `<atomic>` - lock-freie atomare Operationen, `std::atomic<T>`
- `<future>` - `std::async`, `std::future`, `std::promise`, `std::packaged_task`
- `<condition_variable>` - Thread-Signalisierung, wait/notify
- `std::thread` muss vor der Zerstörung mit `join()` oder `detach()` abgeschlossen werden, sonst wird `std::terminate` aufgerufen
- `std::jthread` (C++20) - joint automatisch im Destruktor und unterstützt kooperatives Abbrechen über `stop_token`
- `std::async(std::launch::async, ...)` garantiert einen neuen Thread; `std::launch::deferred` ist verzögert (lazy)
- Data Race = UB in C++. Mindestens ein Schreibzugriff plus gleichzeitiger Zugriff ohne Synchronisation ist undefiniertes Verhalten
- `std::atomic<T>` - lock-frei für kleine Typen (int, Zeiger), stellt Happens-before-Ordnung sicher
- `std::shared_mutex` (C++17) - mehrere Leser ODER ein einzelner Schreiber

## Muster {#patterns}

### Grundlegendes Threading {#basic-threading}

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

### Mutex und Locks {#mutex-and-locks}

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

### Atomare Operationen {#atomic-operations}

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

### Condition Variable {#condition-variable}

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

## Fallstricke {#gotchas}

- **Problem:** Vergessen, `std::thread` mit `join()` oder `detach()` abzuschließen -> `std::terminate` wird aufgerufen -> **Lösung:** `std::jthread` (C++20) verwenden oder join/detach in allen Codepfaden sicherstellen, einschließlich bei Exceptions
- **Problem:** Mehrere Mutexe in unterschiedlicher Reihenfolge sperren -> Deadlock -> **Lösung:** `std::scoped_lock(m1, m2)` (C++17) verwenden, das einen Deadlock-vermeidenden Algorithmus nutzt
- **Problem:** `std::async` mit der Standardrichtlinie kann verzögert im selben Thread laufen -> **Lösung:** Explizit `std::launch::async` verwenden, wenn ein neuer Thread benötigt wird
- **Problem:** Spurious Wakeups bei Condition Variables -> **Lösung:** Immer die Prädikat-Form verwenden: `cv.wait(lock, predicate)`
- **Problem:** Vermischte Ausgaben von `std::cout` aus mehreren Threads -> verstümmelte Ausgabe -> **Lösung:** `std::osyncstream` (C++20) verwenden oder mit Mutex schützen

## Siehe auch {#see-also}

- [[raii-resource-management]]
- [Fehlerbehandlung - Exceptions und Alternativen](error-handling.md)
- [Performance-Optimierung](performance-optimization.md)
- [cppreference: Thread support](https://en.cppreference.com/w/cpp/thread)
