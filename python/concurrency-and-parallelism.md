---
title: Concurrency and Parallelism
category: concepts
tags: [python, threading, multiprocessing, gil, concurrent-futures, parallelism, concurrency]
---

# Concurrency and Parallelism

Python offers three concurrency models: **threading** (concurrent I/O-bound), **multiprocessing** (parallel CPU-bound), and **asyncio** (cooperative I/O-bound). The **GIL** (Global Interpreter Lock) prevents multiple threads from executing Python bytecode simultaneously, making threads suitable for I/O but not for CPU-bound work.

## Key Facts

- The GIL is a mutex that protects CPython's internal state; only one thread executes Python bytecode at a time
- Threading is effective for I/O-bound work (network, disk) because the GIL is released during I/O operations
- Multiprocessing bypasses the GIL by using separate OS processes with separate interpreters
- `concurrent.futures` provides `ThreadPoolExecutor` and `ProcessPoolExecutor` with a unified interface
- `asyncio` is single-threaded cooperative multitasking -- best for many concurrent I/O operations
- Python 3.13 introduces an experimental free-threaded mode (`--disable-gil`, PEP 703)
- `threading.Lock`, `RLock`, `Semaphore`, `Event`, `Condition` for thread synchronization
- `multiprocessing.Queue`, `Pipe`, `Value`, `Array` for inter-process communication
- See [[async-programming]] for asyncio patterns, [[fastapi-fundamentals]] for async endpoints

## Patterns

### `concurrent.futures.ThreadPoolExecutor`

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

def fetch_url(url: str) -> tuple[str, int]:
    response = requests.get(url, timeout=10)
    return url, response.status_code

urls = [f"https://httpbin.org/delay/{i}" for i in range(5)]

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(fetch_url, url): url for url in urls}
    for future in as_completed(futures):
        url, status = future.result()
        print(f"{url}: {status}")
```

### `ProcessPoolExecutor` for CPU-Bound Work

```python
from concurrent.futures import ProcessPoolExecutor
import math

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

numbers = range(10_000_000, 10_000_100)

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(is_prime, numbers))
    primes = [n for n, is_p in zip(numbers, results) if is_p]
```

### Threading with Locks

```python
import threading

class ThreadSafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._count += 1

    @property
    def value(self):
        with self._lock:
            return self._count

counter = ThreadSafeCounter()
threads = [
    threading.Thread(target=lambda: [counter.increment() for _ in range(100_000)])
    for _ in range(10)
]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter.value)  # exactly 1_000_000
```

### Mixing Async with Sync (Thread Pool Bridge)

```python
import asyncio

def blocking_io_operation(path: str) -> str:
    """CPU or blocking I/O that cannot be awaited."""
    import time
    time.sleep(2)
    with open(path) as f:
        return f.read()

async def main():
    # Run blocking code in a thread pool without freezing the event loop
    result = await asyncio.to_thread(blocking_io_operation, "/data/file.txt")
    print(result)
```

### Multiprocessing with Shared State

```python
from multiprocessing import Process, Value, Lock

def worker(shared_counter, lock, iterations):
    for _ in range(iterations):
        with lock:
            shared_counter.value += 1

if __name__ == "__main__":
    counter = Value("i", 0)  # shared integer
    lock = Lock()
    processes = [
        Process(target=worker, args=(counter, lock, 100_000))
        for _ in range(4)
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print(counter.value)  # 400_000
```

### When to Use What

```
I/O-bound, many connections  -> asyncio (single thread, cooperative)
I/O-bound, simple/legacy     -> ThreadPoolExecutor
CPU-bound                    -> ProcessPoolExecutor / multiprocessing
Mixed I/O + CPU              -> asyncio + ProcessPoolExecutor via run_in_executor

# asyncio is best when:
# - You control the entire stack (can use async libraries)
# - You need thousands of concurrent connections
# - You want structured concurrency (TaskGroup)

# Threading is best when:
# - You need to call blocking libraries (requests, psycopg2)
# - You need simple concurrent I/O without rewriting code

# Multiprocessing is best when:
# - You need true parallelism for CPU-bound work
# - Data processing, image manipulation, number crunching
```

## Gotchas

- **GIL does not protect your data structures**: the GIL prevents simultaneous bytecode execution, but operations like `list.append()` or `dict[key] = value` can still interleave between threads. Use `threading.Lock` for compound operations
- **Daemon threads**: `thread.daemon = True` threads are killed abruptly on program exit without cleanup. Use `join()` to wait or use `atexit` for cleanup
- **Multiprocessing pickling**: `ProcessPoolExecutor` sends data between processes via pickle. Lambdas, nested functions, and unpicklable objects (file handles, DB connections) fail. Use module-level functions
- **`asyncio.to_thread` vs `run_in_executor`**: `to_thread` (Python 3.9+) is simpler; `run_in_executor` allows specifying the executor. Both run sync functions in a thread pool
- **Fork safety on macOS**: `multiprocessing` defaults to `fork` on Linux, `spawn` on macOS/Windows. `fork` can deadlock with threads. Use `mp.set_start_method("spawn")` for safety

## See Also

- [concurrent.futures -- Python docs](https://docs.python.org/3/library/concurrent.futures.html)
- [threading -- Python docs](https://docs.python.org/3/library/threading.html)
- [[async-programming]] - asyncio coroutines and event loop
- [[docker-deployment]] - multi-worker deployment with Gunicorn
