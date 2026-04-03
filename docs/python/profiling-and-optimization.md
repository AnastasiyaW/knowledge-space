---
title: Profiling and Performance Optimization
category: concepts
tags: [python, profiling, cProfile, optimization, caching, performance, redis]
---

# Profiling and Performance Optimization

Never optimize without measuring. The 80/20 rule: 80% of runtime is often in 20% of the code. Profile first, then optimize algorithmically, then cache, then consider low-level tricks.

## Key Facts

- `cProfile` is the built-in CPU profiler; `line_profiler` for line-by-line analysis
- `memory_profiler` tracks memory usage per line
- `@functools.lru_cache` provides built-in memoization
- String join is O(n) vs concatenation `+=` in loop is O(n^2)
- `dict`/`set` lookup is O(1); `list` search is O(n)
- Generator expressions use constant memory vs list comprehensions

## Patterns

### cProfile
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

Output columns: **ncalls** (call count), **tottime** (time excluding subcalls), **cumtime** (including subcalls).

### line_profiler
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

### memory_profiler
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

### Optimization Methodology
1. **Measure** - profile to find actual bottleneck
2. **Algorithmic** - better data structures/algorithms (biggest impact)
3. **Caching** - avoid redundant computation/IO
4. **I/O optimization** - batch queries, connection pooling, async
5. **Python tricks** - comprehensions, generators, `__slots__`
6. **C extensions** - NumPy, Cython (last resort)

### Common Performance Tips
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

### In-Memory Caching with TTL
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

### Redis External Caching
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

### Load Balancing
```bash
# Multiple Uvicorn workers
uvicorn app:app --workers 4

# Gunicorn with Uvicorn workers
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

Architecture: Client -> Nginx (reverse proxy) -> Gunicorn -> [Uvicorn workers]

## Gotchas

- Premature optimization is the root of all evil - measure first
- `@lru_cache` arguments must be hashable (no lists/dicts as args)
- Redis adds infrastructure complexity but wins for multi-process/multi-server caching
- Generator expressions cannot be iterated twice - convert to list if needed
- `cProfile` overhead can skew results for very fast functions - use `timeit` for micro-benchmarks

## See Also

- [[memory-and-internals]] - CPython memory model, GC
- [[async-programming]] - async I/O for performance
- [[concurrency]] - parallel execution for CPU-bound work
- [[fastapi-caching-and-tasks]] - caching in web applications
