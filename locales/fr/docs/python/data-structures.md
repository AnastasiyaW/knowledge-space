---
title: "Structures de données intégrées"
category: concepts
tags: [python, list, tuple, set, dict, collections, data-structures]
level: 3
source_sha256: 52c4d2528bb181c582c89a13a85f68bd93f73d818f675b4943cb04f010965dd3
translation: machine
translated_at: '2026-10-24'
---
# Structures de données intégrées {#built-in-data-structures}

Python fournit quatre types de collections principaux : les listes (ordonnées, modifiables), les tuples (ordonnés, immuables), les ensembles (non ordonnés, sans doublons) et les dictionnaires (correspondance clé-valeur). Le choix de la structure adaptée influence à la fois la justesse et les performances.

## Points clés {#key-facts}

- `x in set` est en O(1) en moyenne ; `x in list` est en O(n) - utilisez les ensembles pour les tests d'appartenance
- Les listes sont modifiables ; les tuples sont immuables (ils peuvent servir de clés de dictionnaire, sont légèrement plus rapides et consomment moins de mémoire)
- `set()` crée un ensemble vide, et non `{}` (qui crée un dictionnaire vide)
- Les dictionnaires conservent l'ordre d'insertion depuis Python 3.7
- Les clés doivent être hachables (immuables) : str, int, float, tuple, frozenset

## Modèles d'utilisation {#patterns}

### Listes {#lists}
```python
lst = [1, 2, 3, "hello", True]   # can mix types

# Adding
lst.append(x)          # add to end
lst.insert(0, x)       # insert at index
lst.extend([4, 5])     # add multiple

# Removing
lst.remove(x)          # first occurrence (ValueError if missing)
lst.pop()              # remove and return last
lst.pop(0)             # remove and return at index
del lst[0]             # delete by index

# Searching
x in lst               # membership O(n)
lst.index(x)           # first index (ValueError if missing)
lst.count(x)           # occurrences

# Sorting
lst.sort()             # in-place
sorted(lst)            # returns new sorted list

# Copying
copy1 = lst.copy()     # shallow copy
copy2 = lst[:]         # shallow copy via slice
import copy
deep = copy.deepcopy(nested_list)  # recursive copy
```

### Compréhensions de listes {#list-comprehensions}
```python
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
flat = [x for row in matrix for x in row]  # flatten
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
```

### Tuples {#tuples}
```python
t = (1, 2, 3)
single = (1,)          # trailing comma required for single element
x, y, z = (1, 2, 3)   # unpacking
first, *rest = (1, 2, 3, 4)  # first=1, rest=[2, 3, 4]

# Functions returning multiple values return tuples
def min_max(lst):
    return min(lst), max(lst)
lo, hi = min_max([3, 1, 4])
```

### Ensembles {#sets}
```python
s = {1, 2, 3, 2, 1}   # {1, 2, 3} - duplicates removed
s = set()              # empty set

s.add(4)
s.discard(2)           # no error if missing
s.remove(2)            # KeyError if missing

# Set operations
a | b                  # union
a & b                  # intersection
a - b                  # difference
a ^ b                  # symmetric difference
a.issubset(b)          # True if a <= b

# Remove duplicates preserving order (Python 3.7+)
unique = list(dict.fromkeys(names))
```

### Dictionnaires {#dictionaries}
```python
d = {"name": "Alice", "age": 30}

d["name"]              # "Alice" (KeyError if missing)
d.get("name")          # "Alice" (None if missing)
d.get("phone", "N/A")  # default if missing
d["email"] = "a@b.com" # add/update
del d["age"]           # delete (KeyError if missing)
d.pop("age", None)     # delete, return None if missing

# Iteration
for key in d: ...                 # keys
for value in d.values(): ...      # values
for key, value in d.items(): ...  # pairs

# Merge (Python 3.9+)
d3 = d1 | d2           # d2 wins on conflicts
d1.update(d2)          # in-place merge
d3 = {**d1, **d2}      # unpacking merge
```

### Compréhensions de dictionnaires {#dict-comprehensions}
```python
squares = {x: x**2 for x in range(6)}
swapped = {v: k for k, v in original.items()}
d = dict(zip(keys, values))  # from two lists
```

### Modèles courants avec les dictionnaires {#common-dict-patterns}
```python
# Counting
from collections import Counter
counts = Counter("mississippi")
counts.most_common(3)  # [('i', 4), ('s', 4), ('p', 2)]

# Grouping with defaultdict
from collections import defaultdict
groups = defaultdict(list)
for name, dept in employees:
    groups[dept].append(name)

# Dispatch table
operations = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
}
result = operations["+"](5, 3)  # 8

# setdefault for grouping
groups = {}
for category, item in items:
    groups.setdefault(category, []).append(item)
```

### Types figés {#frozen-types}
```python
fs = frozenset([1, 2, 3])  # immutable set, can be dict key
# tuples can also be dict keys
coordinates = {(0, 0): "origin", (1, 1): "diagonal"}
```

## Quand utiliser quoi {#when-to-use-what}

| Type | Modifiable | Ordonné | Doublons | Cas d'usage |
|------|------------|---------|----------|-------------|
| list | Oui | Oui | Oui | Collection à usage général |
| tuple | Non | Oui | Oui | Données figées, clés de dictionnaire, valeurs de retour |
| set | Oui | Non | Non | Unicité, appartenance, opérations ensemblistes |
| dict | Oui | Oui* | Clés : Non | Correspondance clé-valeur, recherche |

*Ordonné par ordre d'insertion depuis Python 3.7

### Tuples nommés {#named-tuples}

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
p.x                  # 3 (attribute access)
x, y = p             # still unpacks like a tuple
p._asdict()          # {'x': 3, 'y': 4}
p._replace(x=10)     # Point(x=10, y=4) - returns new instance

# Typing-friendly alternative (Python 3.6+)
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float
    label: str = "origin"
```

### ChainMap - Recherches en couches {#chainmap-layered-lookups}

```python
from collections import ChainMap

defaults = {'color': 'red', 'size': 10}
user_prefs = {'color': 'blue'}
runtime = {'debug': True}

config = ChainMap(runtime, user_prefs, defaults)
config['color']   # 'blue' - first match wins
config['size']    # 10 - falls through to defaults
config['debug']   # True
```

### deque - Ajouts et retraits rapides aux deux extrémités {#deque-fast-appends-and-pops-from-both-ends}

```python
from collections import deque

d = deque(maxlen=5)          # bounded buffer
d.append(1)                  # right end
d.appendleft(0)              # left end - O(1) unlike list.insert(0, x) which is O(n)
d.rotate(2)                  # rotate right by 2

# Sliding window pattern
def sliding_window(iterable, n):
    it = iter(iterable)
    window = deque(maxlen=n)
    for _ in range(n):
        window.append(next(it))
    yield tuple(window)
    for item in it:
        window.append(item)
        yield tuple(window)
```

### Piège de la répétition et des références partagées {#repetition-and-shared-references-trap}

```python
# DANGER: repetition creates shared references for mutable objects
board = [[0] * 3] * 3    # 3 references to SAME inner list
board[0][0] = 1
print(board)              # [[1, 0, 0], [1, 0, 0], [1, 0, 0]] - all rows affected!

# FIX: use comprehension to create independent lists
board = [[0] * 3 for _ in range(3)]
board[0][0] = 1
print(board)              # [[1, 0, 0], [0, 0, 0], [0, 0, 0]] - correct
```

### Opérateur walrus dans les compréhensions (Python 3.8+) {#walrus-operator-in-comprehensions-python-38}

```python
# Avoid computing expensive function twice
results = [y for x in data if (y := expensive(x)) > threshold]
```

## Pièges à éviter {#gotchas}

- `b = a` pour des listes crée une référence partagée, et non une copie - utilisez `a.copy()` ou `a[:]`
- La copie superficielle ne copie que le premier niveau - les listes imbriquées restent partagées
- `list.sort()` renvoie `None` (tri en place) ; `sorted()` renvoie une nouvelle liste
- `{1, 2} | {3}` est une union d'ensembles, et non une fusion de dictionnaires - le contexte compte pour `|`
- Modifier un dictionnaire pendant une itération lève une `RuntimeError` - itérez sur une copie
- `[[0]*3]*3` partage les listes internes - utilisez `[[0]*3 for _ in range(3)]` pour des lignes indépendantes
- Un `tuple` n'est PAS toujours immuable en pratique : `t = ([1, 2],)` - le tuple lui-même est immuable, mais la liste qu'il contient est modifiable
- `dict.fromkeys(['a','b'], [])` partage LA MÊME liste pour toutes les clés - utilisez plutôt une compréhension de dictionnaire
- L'opérateur `in` sur un dictionnaire vérifie les clés, et non les valeurs - utilisez `val in d.values()` pour vérifier une valeur

## Voir aussi {#see-also}

- [[standard-library]] - Counter, defaultdict, ChainMap, OrderedDict
- [[iterators-and-generators]] - séquences paresseuses
- [[oop-fundamentals]] - classes de données personnalisées
