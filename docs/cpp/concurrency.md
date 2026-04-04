---
title: Concurrency - Threads, Async, Atomics
category: concepts
tags: [cpp, threads, async, mutex, atomic, concurrency, cpp11, cpp20]
---

# Concurrency - Threads, Async, Atomics

C++ standard threading primitives: `std::thread`, `std::async`, `std::mutex`, `std::atomic`, `std::condition_variable`. Portable, zero-overhead abstractions over OS threading.

## Key Facts

- `<thread>` - `std::thread`, `std::jthread` (C++20, auto-joining)
- `<mutex>` - `mutex`, `recursive_mutex`, `shared_mutex` (C++17), lock guards
- `<atomic>` - lock-free atomic operations, `std::atomic<T>`
- `<future>` - `std::async`, `std::future`, `std::promise`, `std::packaged_task`
- `<condition_variable>` - thread signaling, wait/notify
- `std::thread` must be `join()`ed or `detach()`ed before destruction, else `std::terminate`
- `std::jthread` (C++20) - auto-joins in destructor, supports cooperative cancellation via `stop_token`
- `std::async(std::launch::async, ...)` guarantees new thread; `std::launch::deferred` is lazy
- Data race = UB in C++. At least one write + concurrent access without synchronization = undefined
- `std::atomic<T>` - lock-free for small types (int, ptr), provides happens-before ordering
- `std::shared_mutex` (C++17) - multiple readers OR single writer

## Patterns

### Basic Threading

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

### Mutex and Locks

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

### async/future

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

### Atomic Operations

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

### Condition Variable

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

## Gotchas

- **Issue:** Forgetting to `join()` or `detach()` `std::thread` -> `std::terminate` called -> **Fix:** Use `std::jthread` (C++20) or ensure join/detach in all code paths including exceptions
- **Issue:** Locking multiple mutexes in different order -> deadlock -> **Fix:** Use `std::scoped_lock(m1, m2)` (C++17) which uses deadlock-avoidance algorithm
- **Issue:** `std::async` with default policy may run deferred (same thread) -> **Fix:** Explicitly use `std::launch::async` if you need a new thread
- **Issue:** Condition variable spurious wakeups -> **Fix:** Always use predicate form: `cv.wait(lock, predicate)`
- **Issue:** `std::cout` interleaving from multiple threads -> garbled output -> **Fix:** Use `std::osyncstream` (C++20) or protect with mutex

## See Also

- [[raii-resource-management]]
- [[error-handling]]
- [[performance-optimization]]
- [cppreference: Thread support](https://en.cppreference.com/w/cpp/thread)
