---
title: "Profilage et optimisation des performances"
category: concepts
tags: [python, profiling, cProfile, optimization, caching, performance, redis]
level: 5
source_sha256: 3e85d59ae206e93e7934e0e687993db42c682125506b787ad196d2d17bc221e7
translation: machine
translated_at: '2026-10-24'
---
# Profilage et optimisation des performances {#profiling-and-performance-optimization}

Ne jamais optimiser sans mesurer. La règle des 80/20 : 80 % du temps d'exécution se concentre souvent dans 20 % du code. Profilez d'abord, puis optimisez l'algorithmique, puis mettez en cache, et seulement ensuite envisagez les astuces de bas niveau.

## Points clés {#key-facts}

- `cProfile` est le profileur CPU intégré ; `line_profiler` permet une analyse ligne par ligne
- `memory_profiler` suit l'utilisation mémoire par ligne
- `@functools.lru_cache` fournit une mémoïsation intégrée
- La méthode `join` sur les chaînes est en O(n), alors que la concaténation `+=` dans une boucle est en O(n^2)
- La recherche dans un `dict`/`set` est en O(1) ; la recherche dans une `list` est en O(n)
- Les expressions génératrices utilisent une mémoire constante, contrairement aux compréhensions de listes

## Modèles d'usage {#patterns}

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

Colonnes de sortie : **ncalls** (nombre d'appels), **tottime** (temps hors sous-appels), **cumtime** (temps incluant les sous-appels).

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

### Méthodologie d'optimisation {#optimization-methodology}
1. **Mesurer** - profiler pour identifier le goulot d'étranglement réel
2. **Algorithmique** - de meilleures structures de données et algorithmes (impact le plus important)
3. **Mise en cache** - éviter les calculs et les E/S redondants
4. **Optimisation des E/S** - regrouper les requêtes, utiliser un pool de connexions, passer en asynchrone
5. **Astuces Python** - compréhensions, générateurs, `__slots__`
6. **Extensions C** - NumPy, Cython (en dernier recours)

### Conseils courants de performance {#common-performance-tips}
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

### Cache en mémoire avec TTL {#in-memory-caching-with-ttl}
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

### Cache externe avec Redis {#redis-external-caching}
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

### Répartition de charge {#load-balancing}
```bash
# Multiple Uvicorn workers
uvicorn app:app --workers 4

# Gunicorn with Uvicorn workers
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

Architecture : Client -> Nginx (reverse proxy) -> Gunicorn -> [workers Uvicorn]

## Pièges à éviter {#gotchas}

- L'optimisation prématurée est la racine de tous les maux : mesurez d'abord
- Les arguments de `@lru_cache` doivent être hachables (pas de listes ni de dictionnaires en argument)
- Redis ajoute de la complexité d'infrastructure, mais s'avère pertinent pour la mise en cache multi-processus et multi-serveurs
- Une expression génératrice ne peut être parcourue qu'une seule fois : convertissez-la en liste si nécessaire
- La surcharge de `cProfile` peut fausser les résultats pour des fonctions très rapides : utilisez `timeit` pour les micro-benchmarks

## Voir aussi {#see-also}

- [[memory-and-internals]] - modèle mémoire de CPython, GC
- [[async-programming]] - E/S asynchrones pour la performance
- [Concurrency - Threading and Multiprocessing](concurrency.md) - exécution parallèle pour les tâches liées au CPU
- [[fastapi-caching-and-tasks]] - mise en cache dans les applications web
