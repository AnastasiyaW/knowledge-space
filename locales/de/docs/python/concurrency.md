---
title: "Nebenläufigkeit – Threading und Multiprocessing"
category: concepts
tags: [python, threading, multiprocessing, GIL, concurrent-futures, parallelism]
level: 4
source_sha256: 5f6134a07f64d45c506461bc8411db031082dbc9152076f65d66b1e7aabef6ed
translation: machine
translated_at: '2026-10-24'
---
# Nebenläufigkeit – Threading und Multiprocessing {#concurrency-threading-and-multiprocessing}

Python bietet drei Nebenläufigkeitsmodelle: `threading` für I/O-gebundene Aufgaben, `multiprocessing` für CPU-gebundene Aufgaben (umgeht den GIL) und `asyncio` für hochgradig nebenläufige I/O. Der GIL (Global Interpreter Lock) ist die zentrale Einschränkung, die bestimmt, welches Modell gewählt werden sollte.

## Wichtige Fakten {#key-facts}

- Der GIL erlaubt nur einem Thread gleichzeitig die Ausführung von Python-Bytecode
- Der GIL wird während I/O, `time.sleep()` und bei einigen C-Erweiterungen (NumPy) freigegeben
- CPU-gebundenes Threading bringt KEINEN Geschwindigkeitsgewinn (oft langsamer durch Kontextwechsel)
- `multiprocessing` umgeht den GIL durch separate Prozesse mit eigenen Interpretern
- `concurrent.futures` stellt die übergeordneten Klassen `ThreadPoolExecutor` und `ProcessPoolExecutor` bereit
- Argumente für multiprocessing müssen pickle-bar (serialisierbar) sein

| Ansatz | Geeignet für | Auswirkung des GIL | Overhead |
|--------|--------------|--------------------|----------|
| threading | I/O-gebunden | Durch den GIL begrenzt | Gering (gemeinsamer Speicher) |
| multiprocessing | CPU-gebunden | Umgeht den GIL | Hoch (Prozesserzeugung) |
| asyncio | I/O-gebunden (viele Verbindungen) | Single-Threaded | Am geringsten |

## Muster {#patterns}

### ThreadPoolExecutor (empfohlen für I/O) {#threadpoolexecutor-recommended-for-io}
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

### Einfaches Threading {#basic-threading}
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

### Thread-Synchronisation {#thread-synchronization}
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

### ProcessPoolExecutor (CPU-gebunden) {#processpoolexecutor-cpu-bound}
```python
from concurrent.futures import ProcessPoolExecutor

def compute(n):
    return sum(i * i for i in range(n))

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compute, [10_000_000] * 8))
```

### Multiprocessing mit Pool {#multiprocessing-with-pool}
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

### Interprozesskommunikation {#inter-process-communication}
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

### Daemon-Threads {#daemon-threads}
```python
t = threading.Thread(target=background_task, daemon=True)
t.start()
# No need to join - killed when main program exits
```

### Muster für frühzeitigen Abbruch {#early-termination-pattern}
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

### Free-Threaded Python (PEP 703, Python 3.13+) {#free-threaded-python-pep-703-python-313}

Python 3.13 führt die experimentelle Build-Option `--disable-gil` ein:
```bash
python3.13t script.py  # free-threaded build (no GIL)
```
- Echte multithreaded Parallelität für CPU-gebundenen Code
- Verwendet biased Reference Counting und Sperren pro Objekt anstelle des GIL
- C-Erweiterungen müssen für Thread-Sicherheit angepasst werden
- Opt-in-Flag, nicht der Standard – GIL-Builds bleiben der Standard

### Gemeinsamer Speicher (Python 3.8+) {#shared-memory-python-38}

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

### Fehlerbehandlung in Pools {#error-handling-in-pools}

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

### Threading-Semaphore – Ratenbegrenzung {#threading-semaphore-rate-limiting}

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

## Stolperfallen {#gotchas}

- Selbst `counter += 1` ist in Python nicht atomar – gemeinsam genutzten veränderlichen Zustand immer mit Sperren schützen
- Multiprocessing: Lambdas und verschachtelte Funktionen können nicht pickle-t werden – stattdessen Funktionen auf Modulebene verwenden
- Die Erzeugung von Prozessen ist teuer – für wiederholte Aufgaben Pools verwenden
- Deadlock mit Logging in multiprocessing: Hält ein Thread die Logging-Sperre während `fork()`, erbt das Kind den gesperrten Zustand
- Der Context Manager von `ThreadPoolExecutor` wartet beim Verlassen auf alle Futures
- Thread-Sicherheit: `list.append()` ist in CPython atomar (GIL), aber darauf sollte man sich nicht verlassen
- Worker von `ProcessPoolExecutor` werden geforkt – Importe und globaler Zustand müssen fork-sicher sein
- `future.result()` blockiert bis zur Fertigstellung – für die Verarbeitung in Reihenfolge der Fertigstellung `as_completed()` verwenden
- Pool-Worker, die stillschweigend abstürzen, liefern `None` zurück oder lösen `BrokenProcessPool` aus – Ergebnisse immer prüfen

## Siehe auch {#see-also}

- [[async-programming]] – asyncio für I/O-gebundene Nebenläufigkeit
- [[memory-and-internals]] – Details zum GIL, CPython-Interna
- [[profiling-and-optimization]] – wann parallelisiert werden sollte
