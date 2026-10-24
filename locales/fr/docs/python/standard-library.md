---
title: "Principes essentiels de la bibliothèque standard"
category: concepts
tags: [python, collections, datetime, timedelta, counter, defaultdict, stdlib]
level: 3
source_sha256: a9e1a282887ebe155194d843a9ad34b53423f444b8e083428c265a0885bbd817
translation: machine
translated_at: '2026-10-24'
---
# Principes essentiels de la bibliothèque standard {#standard-library-essentials}

La bibliothèque standard de Python fournit des modules puissants pour les tâches courantes. Cette entrée couvre `collections` (structures de données spécialisées), `datetime` (gestion des dates et heures) ainsi que des modules utilitaires couramment utilisés.

## Module collections {#collections-module}

### Counter {#counter}
```python
from collections import Counter

c = Counter('mississippi')  # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})
c.most_common(2)           # [('i', 4), ('s', 4)]
c['nonexistent']           # 0 (no KeyError!)
c.update(['a', 'b', 'a']) # adds counts (unlike dict.update which replaces)

# Operators
c1 + c2    # add counts (excludes zero/negative)
c1 - c2    # subtract counts (excludes zero/negative)
c1 & c2    # intersection (min)
c1 | c2    # union (max)
```

### defaultdict {#defaultdict}
```python
from collections import defaultdict

word_count = defaultdict(int)     # missing key -> 0
for word in text.split():
    word_count[word] += 1

groups = defaultdict(list)        # missing key -> []
for name, dept in employees:
    groups[dept].append(name)
```

### ChainMap {#chainmap}
```python
from collections import ChainMap

d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
cm = ChainMap(d1, d2)
cm['b']          # 1 (first match wins)
cm.new_child()   # new ChainMap with empty dict prepended
```

### OrderedDict {#ordereddict}
```python
from collections import OrderedDict

od = OrderedDict()
od['a'] = 1
od['b'] = 2
od.move_to_end('a')  # move 'a' to end
```

Redondant à partir de Python 3.7 (les dictionnaires ordinaires sont ordonnés), mais toujours utile pour `move_to_end()` et les comparaisons d'égalité sensibles à l'ordre.

## Module datetime {#datetime-module}

### Types principaux {#core-types}
```python
from datetime import date, time, datetime, timedelta, timezone

# Date
today = date.today()
d = date(2024, 12, 25)
d.strftime('%d.%m.%Y')     # '25.12.2024'
d.weekday()                # 0=Monday, 6=Sunday

# DateTime
now = datetime.now()
utc = datetime.now(timezone.utc)
dt = datetime.strptime('15/03/2024 14:30', '%d/%m/%Y %H:%M')  # parse string
dt.strftime('%Y-%m-%d %H:%M:%S')  # format to string
dt.isoformat()             # '2024-03-15T14:30:00'
```

### timedelta (durée) {#timedelta-duration}
```python
from datetime import timedelta

tomorrow = date.today() + timedelta(days=1)
week_ago = datetime.now() - timedelta(weeks=1)
diff = date(2024, 12, 31) - date(2024, 1, 1)
diff.days       # 365
diff.total_seconds()  # everything as seconds (float)
```

### Gestion des fuseaux horaires {#timezone-handling}
```python
from zoneinfo import ZoneInfo  # Python 3.9+

eastern = ZoneInfo("America/New_York")
moscow = ZoneInfo("Europe/Moscow")
dt = datetime.now(eastern)
dt_moscow = dt.astimezone(moscow)
```

### Codes de format {#format-codes}

| Code | Signification | Exemple |
|------|---------------|---------|
| `%Y` | Année sur 4 chiffres | 2024 |
| `%m` | Mois 01-12 | 03 |
| `%d` | Jour 01-31 | 15 |
| `%H` | Heure 00-23 | 14 |
| `%M` | Minute 00-59 | 30 |
| `%S` | Seconde 00-59 | 45 |
| `%A` | Jour de la semaine complet | Friday |
| `%B` | Mois complet | March |

`strftime` = datetime -> chaîne. `strptime` = chaîne -> datetime.

### Schémas courants de manipulation de dates {#common-date-patterns}
```python
# Date range generator
def date_range(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

# Parse multiple formats
formats = ['%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y']
def parse_date(s):
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse: {s}")

# Age calculation
def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age
```

## Autres modules utiles {#other-useful-modules}

### sys {#sys}
```python
import sys
sys.argv       # command-line arguments
sys.path       # module search paths
sys.getrecursionlimit()  # default 1000
sys.getsizeof(obj)       # memory size in bytes
```

### random {#random}
```python
import random
random.randint(1, 10)           # random int in [1, 10]
random.choice(['a', 'b', 'c']) # random element
random.shuffle(my_list)         # shuffle in-place
random.seed(42)                 # reproducible results
```

### functools {#functools}
```python
from functools import lru_cache, partial, reduce

@lru_cache(maxsize=128)  # memoization with LRU eviction
def fib(n): ...

add_five = partial(add, 5)  # partial application
total = reduce(lambda a, b: a + b, [1, 2, 3, 4])  # 10
```

## Pièges à éviter {#gotchas}

- Les opérateurs `+`/`-` de Counter suppriment les compteurs nuls et négatifs ; `subtract()` les conserve
- `defaultdict` crée des entrées à chaque accès : l'itération peut donc créer des clés non désirées
- `datetime.now()` renvoie un datetime naïf (sans fuseau horaire) ; utilisez `datetime.now(timezone.utc)` pour un datetime conscient du fuseau
- `strptime` est strict : la chaîne de format doit correspondre exactement à l'entrée
- `timedelta` ne stocke en interne que les jours, secondes et microsecondes : il n'existe pas de notion de mois ni d'année

## Voir aussi {#see-also}

- [[data-structures]] - opérations intégrées sur dict, list et set
- [[iterators-and-generators]] - module itertools
- [[file-io]] - os, shutil, tempfile
