---
title: "Muster der Python-Standardbibliothek - Collections, Itertools, Closures"
category: concepts
tags: [python, collections, itertools, functools, closures, scoping]
level: 3
source_sha256: 8a7385ff49b34a4d91bbbf9d4cf675ccc3c940167a7cb725f227958f5c4d0189
translation: machine
translated_at: '2026-10-24'
---
# Muster der Python-Standardbibliothek - Collections, Itertools, Closures {#python-standard-library-patterns-collections-itertools-closures}

Datenstrukturen und Werkzeuge der Python-Standardbibliothek für funktionale Programmierung - das Modul collections, itertools, functools, heapq, Scoping-Regeln (LEGB) und Closure-Muster.

## Wichtige Fakten {#key-facts}

- `defaultdict` initialisiert fehlende Schlüssel automatisch; `Counter` zählt Häufigkeiten; `deque` ist an beiden Enden O(1)
- `list.pop(0)` ist O(N); `deque.popleft()` ist O(1) - für Queue-Operationen immer `deque` verwenden
- LEGB-Scoping: Local -> Enclosing -> Global -> Built-in
- `nonlocal` verändert den umschließenden Scope; `global` verändert den Modul-Scope
- Closures erfassen Variablen per Referenz (Late Binding) - häufige Falle bei Schleifen
- `functools.lru_cache` stellt einen automatischen Memoization-Decorator bereit

## Muster {#patterns}

### Collections-Modul {#collections-module}

```python
from collections import defaultdict, Counter, deque, namedtuple

# defaultdict - auto-initialize missing keys
graph = defaultdict(list)
graph['A'].append('B')  # no KeyError

# Counter - frequency counting
c = Counter('abracadabra')  # {'a': 5, 'b': 2, ...}
c.most_common(3)             # top 3 elements
c1 + c2                      # combine counters
c1 - c2                      # subtract (drops <= 0)

# deque - O(1) both ends, optional maxlen
d = deque(maxlen=100)  # fixed-size circular buffer
d.appendleft(x)
d.popleft()            # O(1) unlike list.pop(0)
d.rotate(2)            # rotate elements

# namedtuple - lightweight data class
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
p.x, p._asdict(), p._replace(x=3)
```

### itertools {#itertools}

```python
import itertools

itertools.chain(iter1, iter2)           # flatten iterables
itertools.combinations(seq, r)          # r-length combinations
itertools.permutations(seq, r)          # r-length permutations
itertools.groupby(sorted_seq, key)      # group consecutive equal elements
itertools.accumulate(seq, operator.add) # running totals
itertools.product(seq1, seq2)           # Cartesian product
```

### functools {#functools}

```python
import functools

functools.reduce(fn, seq, initial)       # fold left
functools.lru_cache(maxsize=128)         # memoization decorator
functools.partial(fn, arg1)              # partial application
functools.total_ordering                 # class decorator: define __eq__+__lt__, get rest
```

### heapq (Prioritätswarteschlange) {#heapq-priority-queue}

```python
import heapq

heap = []
heapq.heappush(heap, (priority, item))
priority, item = heapq.heappop(heap)    # min-heap by default
heapq.heapify(lst)                      # O(N) in-place

# Max-heap: negate priorities
heapq.heappush(heap, (-priority, item))

heapq.nlargest(k, iterable, key=fn)
heapq.nsmallest(k, iterable, key=fn)
```

### LEGB-Scoping-Regel {#legb-scoping-rule}

Auflösung von Namen in Python: **L**ocal -> **E**nclosing -> **G**lobal -> **B**uilt-in.

```python
x = 'global'

def outer():
    x = 'enclosing'
    def inner():
        x = 'local'
        print(x)  # 'local'
    inner()

# global and nonlocal modify outer scopes
counter = 0
def increment():
    global counter
    counter += 1

def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc
```

### Closures {#closures}

```python
def multiplier(factor):
    def multiply(x):
        return x * factor  # factor is "closed over"
    return multiply

double = multiplier(2)
double(5)  # 10

# Inspect closure cells
double.__closure__[0].cell_contents  # 2
```

### Guard-Clause-Muster {#guard-clause-pattern}

```python
# Nested (avoid)
def process(user):
    if user:
        if user.is_active:
            if user.has_permission:
                return do_work(user)

# Guard clauses (prefer)
def process(user):
    if not user: return None
    if not user.is_active: raise InactiveUserError()
    if not user.has_permission: raise PermissionDenied()
    return do_work(user)
```

## Fallstricke {#gotchas}

- **Late Binding in Closures**: `[lambda: i for i in range(5)]` - alle liefern 4, nicht 0-4. Abhilfe: `[lambda i=i: i for i in range(5)]`
- `groupby` benötigt sortierte Eingaben - es gruppiert nur aufeinanderfolgende gleiche Elemente
- `deque(maxlen=N)` verwirft beim Volllaufen stillschweigend die ältesten Elemente - es wird kein Fehler ausgelöst
- Die Subtraktion bei `Counter` entfernt Null- und negative Zähler; mit `counter.subtract()` bleiben sie erhalten
- `namedtuple` ist unveränderlich; für eine veränderliche Variante `dataclasses.dataclass` verwenden
- Ohne `global` oder `nonlocal` erzeugt eine Zuweisung eine neue lokale Variable, die die äußere verdeckt

## Siehe auch {#see-also}

- [[dynamic-programming]] - Memoization mit `lru_cache`
- [[algorithms/problem-patterns]] - Counter/defaultdict für Häufigkeitsprobleme
- [[data-structures-fundamentals]] - Big O der Operationen der Standardbibliothek
