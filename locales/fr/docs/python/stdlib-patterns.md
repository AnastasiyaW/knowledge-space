---
title: "Modèles de la bibliothèque standard Python - Collections, Itertools, Fermetures"
category: concepts
tags: [python, collections, itertools, functools, closures, scoping]
level: 3
source_sha256: 8a7385ff49b34a4d91bbbf9d4cf675ccc3c940167a7cb725f227958f5c4d0189
translation: machine
translated_at: '2026-10-24'
---
# Modèles de la bibliothèque standard Python - Collections, Itertools, Fermetures {#python-standard-library-patterns-collections-itertools-closures}

Structures de données et outils de programmation fonctionnelle de la bibliothèque standard Python : module collections, itertools, functools, heapq, règles de portée (LEGB) et motifs de fermetures (closures).

## Points clés {#key-facts}

- `defaultdict` initialise automatiquement les clés manquantes ; `Counter` compte les fréquences ; `deque` est en O(1) aux deux extrémités
- `list.pop(0)` est en O(N) ; `deque.popleft()` est en O(1) : utilisez toujours deque pour les opérations de file
- Portée LEGB : Local -> Englobante -> Globale -> Built-in
- `nonlocal` modifie la portée englobante ; `global` modifie la portée du module
- Les fermetures capturent les variables par référence (liaison tardive), piège courant avec les boucles
- `functools.lru_cache` fournit un décorateur de mémoïsation automatique

## Motifs {#patterns}

### Module collections {#collections-module}

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

### heapq (file de priorité) {#heapq-priority-queue}

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

### Règle de portée LEGB {#legb-scoping-rule}

Résolution des noms en Python : **L**ocal -> **E**nglobante -> **G**lobale -> **B**uilt-in.

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

### Fermetures {#closures}

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

### Motif de clause de garde {#guard-clause-pattern}

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

## Pièges {#gotchas}

- **Liaison tardive dans les fermetures** : `[lambda: i for i in range(5)]` renvoie toujours 4 et non 0 à 4. Correction : `[lambda i=i: i for i in range(5)]`
- `groupby` exige une entrée triée : il ne regroupe que les éléments consécutifs égaux
- `deque(maxlen=N)` supprime silencieusement les éléments les plus anciens lorsqu'elle est pleine : aucune erreur n'est levée
- La soustraction de `Counter` supprime les compteurs nuls et négatifs ; utilisez `counter.subtract()` pour les conserver
- `namedtuple` est immuable ; pour une version modifiable, utilisez `dataclasses.dataclass`
- Sans `global` ou `nonlocal`, une affectation crée une nouvelle variable locale qui masque la variable externe

## Voir aussi {#see-also}

- [[dynamic-programming]] - mémoïsation avec `lru_cache`
- [[algorithms/problem-patterns]] - Counter/defaultdict pour les problèmes de fréquence
- [[data-structures-fundamentals]] - complexité en Big O des opérations de la bibliothèque standard
