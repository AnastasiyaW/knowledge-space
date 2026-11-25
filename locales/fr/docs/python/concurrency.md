---
title: "Concurrence - Threading et multiprocessing"
category: concepts
tags: [python, threading, multiprocessing, GIL, concurrent-futures, parallelism]
level: 4
source_sha256: 5f6134a07f64d45c506461bc8411db031082dbc9152076f65d66b1e7aabef6ed
translation: machine
translated_at: '2026-10-24'
---
# Concurrence - Threading et multiprocessing {#concurrency-threading-and-multiprocessing}

Python propose trois modèles de concurrence : `threading` pour les tâches liées aux E/S, `multiprocessing` pour les tâches liées au CPU (contourne le GIL) et `asyncio` pour une forte concurrence d'E/S. Le GIL (Global Interpreter Lock) est la contrainte clé qui détermine le modèle à choisir.

## Points clés {#key-facts}

- Le GIL n'autorise qu'un seul thread à exécuter du bytecode Python à la fois
- Le GIL est libéré lors des E/S, de `time.sleep()` et de certaines extensions C (NumPy)
- Le threading pour des tâches liées au CPU n'apporte AUCUN gain de vitesse (souvent plus lent à cause des changements de contexte)
- `multiprocessing` contourne le GIL en utilisant des processus séparés, chacun avec son propre interpréteur
- `concurrent.futures` fournit les classes de haut niveau `ThreadPoolExecutor` et `ProcessPoolExecutor`
- Les arguments passés à multiprocessing doivent être sérialisables avec pickle

| Approche | Usage recommandé | Impact du GIL | Surcharge |
|----------|----------|------------|----------|
| threading | Liée aux E/S | Limité par le GIL | Faible (mémoire partagée) |
| multiprocessing | Liée au CPU | Contourne le GIL | Élevée (création de processus) |
| asyncio | Liée aux E/S (nombreuses connexions) | Mono-thread | Le plus faible |

## Patterns {#patterns}

### ThreadPoolExecutor (recommandé pour les E/S) {#threadpoolexecutor-recommended-for-io}
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

### Threading de base {#basic-threading}
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

### Synchronisation des threads {#thread-synchronization}
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

### ProcessPoolExecutor (liée au CPU) {#processpoolexecutor-cpu-bound}
```python
from concurrent.futures import ProcessPoolExecutor

def compute(n):
    return sum(i * i for i in range(n))

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compute, [10_000_000] * 8))
```

### Multiprocessing avec Pool {#multiprocessing-with-pool}
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

### Communication inter-processus {#inter-process-communication}
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

### Threads démons {#daemon-threads}
```python
t = threading.Thread(target=background_task, daemon=True)
t.start()
# No need to join - killed when main program exits
```

### Motif d'arrêt anticipé {#early-termination-pattern}
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

### Python « free-threaded » (PEP 703, Python 3.13+) {#free-threaded-python-pep-703-python-313}

Python 3.13 introduit l'option de compilation expérimentale `--disable-gil` :
```bash
python3.13t script.py  # free-threaded build (no GIL)
```
- Véritable parallélisme multi-thread pour le code lié au CPU
- Utilise un comptage de références biaisé et des verrous par objet à la place du GIL
- Les extensions C doivent être mises à jour pour être thread-safe
- Option à activer explicitement, non par défaut : les builds avec GIL restent la norme

### Mémoire partagée (Python 3.8+) {#shared-memory-python-38}

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

### Gestion des erreurs dans les pools {#error-handling-in-pools}

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

### Sémaphore de threading - limitation de débit {#threading-semaphore-rate-limiting}

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

## Pièges {#gotchas}

- Même `counter += 1` n'est pas atomique en Python : protégez toujours l'état mutable partagé avec des verrous
- Multiprocessing : les lambdas et les fonctions imbriquées ne peuvent pas être sérialisées avec pickle ; utilisez des fonctions au niveau du module
- La création de processus est coûteuse : utilisez des pools pour les tâches répétées
- Deadlock avec logging en multiprocessing : si un thread détient le verrou du logging pendant un `fork()`, l'enfant hérite de l'état verrouillé
- Le gestionnaire de contexte `ThreadPoolExecutor` attend la fin de tous les futurs à la sortie
- Sécurité des threads : `list.append()` est atomique dans CPython (grâce au GIL), mais ne vous y fiez pas
- Les workers de `ProcessPoolExecutor` sont créés par `fork` : les imports et l'état global doivent être compatibles avec fork
- `future.result()` bloque jusqu'à la fin : utilisez `as_completed()` pour traiter dans l'ordre de fin
- Les workers de pool qui plantent silencieusement renvoient `None` ou lèvent `BrokenProcessPool` : vérifiez toujours les résultats

## Voir aussi {#see-also}

- [[async-programming]] - asyncio pour la concurrence liée aux E/S
- [[memory-and-internals]] - détails du GIL, internes de CPython
- [[profiling-and-optimization]] - quand paralléliser
