---
title: "C++20 Coroutines"
description: "Cooperative multitasking with co_yield, co_return, and co_await for lazy generators and async I/O"
---

# C++20 Coroutines

Coroutines provide cooperative multitasking in C++20 - a function that can suspend execution, yield a value, and later resume where it left off. They are fundamentally different from threads and are not about parallelism but about interleaving execution without blocking.

## Core Model

A regular function has a **stack frame** that is created on call and destroyed on return. A coroutine has a **coroutine frame** allocated on the heap that persists across suspensions.

Key distinction from threads:
- **Threads** use preemptive multitasking: the OS decides when to switch
- **Coroutines** use cooperative multitasking: the coroutine voluntarily gives up its turn

When a coroutine suspends, it says "I did a bit of work, I'm prepared to let others go now." When resumed, execution continues exactly where it left off with all local state intact.

## Keywords

C++20 introduces three keywords that make a function a coroutine:

| Keyword | Purpose |
|---------|---------|
| `co_yield expr` | Suspend and produce a value |
| `co_return expr` | Final return (coroutine completes) |
| `co_await expr` | Suspend until an awaitable completes |

Any function containing one of these keywords is automatically treated as a coroutine by the compiler.

## Use Cases

Coroutines excel at:
- **Lazy generators**: produce values one at a time without computing the entire sequence
- **Async I/O**: start reading a file, yield control, resume when data is ready
- **Stream processing**: process elements as they arrive without buffering everything
- **Pipelines**: chain producers and consumers without threads

They are NOT ideal for:
- CPU-bound parallelism (use threads/`std::async` for that)
- Running N identical tasks simultaneously (thread pool is better)

## Generator Pattern

The most common coroutine pattern - a function that produces a sequence of values lazily:

```cpp
#include <coroutine>
#include <iostream>

// Simplified generator (real implementation needs promise_type, etc.)
Generator<int> fibonacci() {
    int a = 0, b = 1;
    while (true) {
        co_yield a;
        auto next = a + b;
        a = b;
        b = next;
    }
}

// Usage: values computed on-demand
auto fib = fibonacci();
for (int i = 0; i < 10; ++i) {
    std::cout << fib.next() << " ";
}
// Output: 0 1 1 2 3 5 8 13 21 34
```

## Coroutine Frame Lifecycle

1. Caller invokes coroutine function
2. Coroutine frame allocated (heap, not stack)
3. Parameters copied into frame
4. Promise object constructed
5. Execution begins
6. On `co_yield`/`co_await`: state saved, control returns to caller
7. On resume: execution continues from suspension point
8. On `co_return` or falling off end: frame destroyed

## Relationship to Other Concurrency Features

| Feature | Model | Overhead | Best For |
|---------|-------|----------|----------|
| `std::thread` | Preemptive, OS-managed | High (OS thread) | CPU parallelism |
| `std::async` | Task-based, may use thread pool | Medium | Fire-and-forget tasks |
| Coroutines | Cooperative, single-thread | Low (heap frame) | I/O, generators, pipelines |

## Gotchas

- **No standard library generator type in C++20.** You must write your own `Generator<T>` with proper `promise_type`, or use a library. C++23 adds `std::generator`.
- **Coroutine frame is heap-allocated.** The compiler may optimize this away (HALO - Heap Allocation eLision Optimization), but it is not guaranteed. For performance-critical tight loops, measure.
- **Dangling references are easy.** If a coroutine captures a reference to a local variable of the caller, and the caller's scope ends before the coroutine resumes, you get undefined behavior.
- **Debugging is difficult.** Stepping through coroutine suspension/resumption in a debugger is not well-supported in most IDEs as of 2024.

## Cross-References

- [[concurrency]] - threads, mutexes, atomic operations
- [[modern-cpp-features]] - other C++20 additions
- [[lambda-expressions]] - often used with coroutines for callbacks
