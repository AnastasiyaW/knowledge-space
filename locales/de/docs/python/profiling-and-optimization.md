---
title: "Profiling und Performance-Optimierung"
category: concepts
tags: [python, profiling, cProfile, optimization, caching, performance, redis]
level: 5
source_sha256: 3e85d59ae206e93e7934e0e687993db42c682125506b787ad196d2d17bc221e7
translation: machine
translated_at: '2026-10-24'
---
# Profiling und Performance-Optimierung {#profiling-and-performance-optimization}

Optimiere niemals ohne vorherige Messung. Die 80/20-Regel: Oft entfallen 80 % der Laufzeit auf 20 % des Codes. Zuerst profilen, dann algorithmisch optimieren, danach cachen und erst anschließend low-level-Tricks in Betracht ziehen.

## Wichtige Fakten {#key-facts}

- `cProfile` ist der eingebaute CPU-Profiler; `line_profiler` für die zeilenweise Analyse
- `memory_profiler` erfasst den Speicherverbrauch pro Zeile
- `@functools.lru_cache` bietet eingebaute Memoization
- Stringverkettung mit `join` ist O(n), während `+=` in einer Schleife O(n^2) ist
- Die Suche in einem `dict`/`set` ist O(1); die Suche in einer `list` ist O(n)
- Generatorausdrücke benötigen konstanten Speicher, im Gegensatz zu Listen-Comprehensions

## Muster {#patterns}

### cProfile {#cprofile}
```bash
python -m cProfile -s cumulative my_script.py
```

```python
import cProfile, pstats

cProfile.run('my_function()', 'output.prof')
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative')
stats.print_stats(20)
```

Ausgabespalten: **ncalls** (Anzahl der Aufrufe), **tottime** (Zeit ohne Unteraufrufe), **cumtime** (inklusive Unteraufrufe).

### line_profiler {#line_profiler}
```python
@profile  # decorate target function
def slow_function():
    result = []
    for i in range(10000):
        result.append(i ** 2)
    return sum(result)
```
```bash
kernprof -l -v my_script.py
```

### memory_profiler {#memory_profiler}
```python
from memory_profiler import profile

@profile
def memory_heavy():
    big_list = [i for i in range(1_000_000)]
    del big_list
```
```bash
python -m memory_profiler my_script.py
```

### Optimierungsmethodik {#optimization-methodology}
1. **Messen** - profilen, um den tatsächlichen Engpass zu finden
2. **Algorithmisch** - bessere Datenstrukturen und Algorithmen (größte Wirkung)
3. **Caching** - redundante Berechnungen und I/O vermeiden
4. **I/O-Optimierung** - Abfragen bündeln, Connection-Pooling, Asynchronität
5. **Python-Tricks** - Comprehensions, Generatoren, `__slots__`
6. **C-Erweiterungen** - NumPy, Cython (letzter Ausweg)

### Häufige Performance-Tipps {#common-performance-tips}
```python
# List comprehension > loop with append
squares = [x**2 for x in range(1000)]

# Generator for large sequences
total = sum(x**2 for x in range(1_000_000))

# Set for membership testing
items = set(large_list)  # convert once
if x in items:           # O(1)

# String join > concatenation
result = ''.join(parts)  # O(n) vs O(n^2) for +=

# __slots__ for memory
class Point:
    __slots__ = ['x', 'y']
```

### In-Memory-Caching mit TTL {#in-memory-caching-with-ttl}
```python
import datetime
from functools import lru_cache

_cache = {}

def get_weather(city):
    cached = _cache.get(city)
    if cached and (datetime.datetime.now() - cached['time']).seconds < 300:
        return cached['data']
    data = call_weather_api(city)
    _cache[city] = {'data': data, 'time': datetime.datetime.now()}
    return data

# Built-in memoization
@lru_cache(maxsize=128)
def expensive(n):
    return sum(i**2 for i in range(n))
```

### Externes Caching mit Redis {#redis-external-caching}
```python
import redis, json

r = redis.Redis(host='localhost', port=6379)

def get_data(key):
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    data = fetch_from_db(key)
    r.setex(key, 300, json.dumps(data))  # TTL 300 seconds
    return data
```

### Lastverteilung {#load-balancing}
```bash
# Multiple Uvicorn workers
uvicorn app:app --workers 4

# Gunicorn with Uvicorn workers
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

Architektur: Client -> Nginx (Reverse Proxy) -> Gunicorn -> [Uvicorn-Worker]

## Stolperfallen {#gotchas}

- Vorzeitige Optimierung ist die Wurzel allen Übels - zuerst messen
- Argumente von `@lru_cache` müssen hashbar sein (keine Listen/Dicts als Argumente)
- Redis erhöht die Infrastrukturkomplexität, lohnt sich aber für Caching über mehrere Prozesse oder Server hinweg
- Generatorausdrücke können nicht zweimal iteriert werden - bei Bedarf in eine Liste umwandeln
- Der Overhead von `cProfile` kann die Ergebnisse bei sehr schnellen Funktionen verfälschen - für Mikrobenchmarks `timeit` verwenden

## Siehe auch {#see-also}

- [[memory-and-internals]] - CPython-Speichermodell, GC
- [[async-programming]] - asynchrone I/O für Performance
- [Concurrency - Threading and Multiprocessing](concurrency.md) - parallele Ausführung für CPU-gebundene Arbeit
- [[fastapi-caching-and-tasks]] - Caching in Webanwendungen
