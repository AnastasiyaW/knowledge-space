---
title: Concurrency - Threading and Multiprocessing
category: concepts
tags: [python, threading, multiprocessing, GIL, concurrent-futures, parallelism]
---

# Concurrency - Threading and Multiprocessing

Python offers three concurrency models: `threading` for I/O-bound tasks, `multiprocessing` for CPU-bound tasks (bypasses GIL), and `asyncio` for high-concurrency I/O. The GIL (Global Interpreter Lock) is the key constraint that determines which model to choose.

## Key Facts

- GIL allows only one thread to execute Python bytecode at a time
- GIL is released during I/O, `time.sleep()`, and some C extensions (NumPy)
- CPU-bound threading gives NO speedup (often slower due to context switching)
- `multiprocessing` bypasses GIL using separate processes with separate interpreters
- `concurrent.futures` provides high-level `ThreadPoolExecutor` and `ProcessPoolExecutor`
- Arguments to multiprocessing must be picklable (serializable)

| Approach | Best For | GIL Impact | Overhead |
|----------|----------|------------|----------|
| threading | I/O-bound | Limited by GIL | Low (shared memory) |
| multiprocessing | CPU-bound | Bypasses GIL | High (process creation) |
| asyncio | I/O-bound (many connections) | Single-threaded | Lowest |

## Patterns

### ThreadPoolExecutor (Recommended for I/O)
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_url(url):
    response = requests.get(url)
    return url, response.status_code

urls = ["https://api1.com", "https://api2.com", "https://api3.com"]

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(fetch_url, url): url for url in urls}
    for future in as_completed(futures):
        url, status = future.result()
        print(f"{url}: {status}")

# Or ordered results with map:
with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(fetch_url, urls)
```

### Basic Threading
```python
import threading

def worker(name, delay):
    time.sleep(delay)
    print(f"Thread {name} done")

t1 = threading.Thread(target=worker, args=("A", 2))
t2 = threading.Thread(target=worker, args=("B", 1))
t1.start(); t2.start()
t1.join(); t2.join()  # wait for completion
```

### Thread Synchronization
```python
lock = threading.Lock()

def safe_increment(counter):
    with lock:  # acquire/release automatically
        counter.value += 1

# Event for signaling
stop_event = threading.Event()
def worker():
    while not stop_event.is_set():
        do_work()
stop_event.set()  # signal to stop
```

### ProcessPoolExecutor (CPU-bound)
```python
from concurrent.futures import ProcessPoolExecutor

def compute(n):
    return sum(i * i for i in range(n))

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compute, [10_000_000] * 8))
```

### Multiprocessing with Pool
```python
from multiprocessing import Pool

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

with Pool(processes=8) as pool:
    results = pool.map(is_prime, range(100_000, 200_000))
```

### Inter-Process Communication
```python
from multiprocessing import Queue, Value

# Queue
q = Queue()
q.put("data")
data = q.get()

# Shared memory
counter = Value('i', 0)
with counter.get_lock():
    counter.value += 1
```

### Daemon Threads
```python
t = threading.Thread(target=background_task, daemon=True)
t.start()
# No need to join - killed when main program exits
```

### Early Termination Pattern
```python
from multiprocessing import Event

stop = Event()

def check_divisible(args):
    number, start, end = args
    for i in range(start, end):
        if stop.is_set():
            return None
        if number % i == 0:
            stop.set()
            return i
    return None
```

### Free-Threaded Python (PEP 703, Python 3.13+)

Python 3.13 introduces experimental `--disable-gil` build option:
```bash
python3.13t script.py  # free-threaded build (no GIL)
```
- True multi-threaded parallelism for CPU-bound code
- Uses biased reference counting and per-object locks instead of GIL
- C extensions must be updated for thread safety
- Opt-in flag, not default - GIL builds remain standard

### Shared Memory (Python 3.8+)

```python
from multiprocessing import shared_memory
import numpy as np

# Create shared memory from numpy array
a = np.array([1, 2, 3, 4, 5])
shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
shared_arr = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
shared_arr[:] = a[:]  # copy data

# In another process - attach by name
existing_shm = shared_memory.SharedMemory(name=shm.name)
b = np.ndarray(a.shape, dtype=a.dtype, buffer=existing_shm.buf)
# b sees same data without serialization overhead

shm.close()
shm.unlink()  # free shared memory
```

### Error Handling in Pools

```python
from concurrent.futures import ProcessPoolExecutor, as_completed

def risky(n):
    if n == 3:
        raise ValueError(f"bad input: {n}")
    return n * n

with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(risky, i): i for i in range(5)}
    for future in as_completed(futures):
        try:
            result = future.result()
            print(f"{futures[future]} -> {result}")
        except Exception as e:
            print(f"{futures[future]} failed: {e}")
        # Exceptions are re-raised in the calling thread
```

### Threading Semaphore - Rate Limiting

```python
import threading

# Allow max 5 concurrent connections
semaphore = threading.Semaphore(5)

def download(url):
    with semaphore:
        # At most 5 threads execute this block simultaneously
        response = requests.get(url)
        return response.content
```

## Gotchas

- Even `counter += 1` is not atomic in Python - always protect shared mutable state with locks
- Multiprocessing: lambdas and nested functions cannot be pickled - use module-level functions
- Process creation is expensive - use pools for repeated tasks
- Deadlock with logging in multiprocessing: if a thread holds the logging lock during `fork()`, child inherits locked state
- `ThreadPoolExecutor` context manager waits for all futures on exit
- Thread safety: `list.append()` is atomic in CPython (GIL), but don't rely on this
- `ProcessPoolExecutor` workers are forked - imports and global state must be fork-safe
- `future.result()` blocks until complete - use `as_completed()` for earliest-first processing
- Pool workers that crash silently return `None` or raise `BrokenProcessPool` - always check results

## See Also

- [[async-programming]] - asyncio for I/O-bound concurrency
- [[memory-and-internals]] - GIL details, CPython internals
- [[profiling-and-optimization]] - when to parallelize
