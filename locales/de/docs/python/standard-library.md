---
title: "Grundlagen der Standardbibliothek"
category: concepts
tags: [python, collections, datetime, timedelta, counter, defaultdict, stdlib]
level: 3
source_sha256: a9e1a282887ebe155194d843a9ad34b53423f444b8e083428c265a0885bbd817
translation: machine
translated_at: '2026-10-24'
---
# Grundlagen der Standardbibliothek {#standard-library-essentials}

Die Standardbibliothek von Python bietet leistungsstarke Module für häufige Aufgaben. Dieser Eintrag behandelt `collections` (spezialisierte Datenstrukturen), `datetime` (Verarbeitung von Datum und Uhrzeit) sowie häufig verwendete Hilfsmodule.

## collections-Modul {#collections-module}

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

In Python 3.7+ überflüssig (reguläre Dictionaries sind geordnet), aber weiterhin nützlich für `move_to_end()` und reihenfolgeabhängige Gleichheitsvergleiche.

## datetime-Modul {#datetime-module}

### Grundlegende Typen {#core-types}
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

### timedelta (Dauer) {#timedelta-duration}
```python
from datetime import timedelta

tomorrow = date.today() + timedelta(days=1)
week_ago = datetime.now() - timedelta(weeks=1)
diff = date(2024, 12, 31) - date(2024, 1, 1)
diff.days       # 365
diff.total_seconds()  # everything as seconds (float)
```

### Zeitzonenbehandlung {#timezone-handling}
```python
from zoneinfo import ZoneInfo  # Python 3.9+

eastern = ZoneInfo("America/New_York")
moscow = ZoneInfo("Europe/Moscow")
dt = datetime.now(eastern)
dt_moscow = dt.astimezone(moscow)
```

### Formatcodes {#format-codes}

| Code | Bedeutung | Beispiel |
|------|---------|---------|
| `%Y` | Jahr mit 4 Ziffern | 2024 |
| `%m` | Monat 01-12 | 03 |
| `%d` | Tag 01-31 | 15 |
| `%H` | Stunde 00-23 | 14 |
| `%M` | Minute 00-59 | 30 |
| `%S` | Sekunde 00-59 | 45 |
| `%A` | Vollständiger Wochentag | Freitag |
| `%B` | Vollständiger Monatsname | März |

`strftime` = datetime -> String. `strptime` = String -> datetime.

### Häufige Datumsmuster {#common-date-patterns}
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

## Weitere nützliche Module {#other-useful-modules}

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

## Stolperfallen {#gotchas}

- Die Operatoren `+`/`-` von Counter entfernen Zähler mit Null- oder negativen Werten; `subtract()` behält sie bei
- `defaultdict` erzeugt Einträge beim Zugriff - Iteration kann ungewollte Schlüssel erzeugen
- `datetime.now()` liefert ein naives datetime (ohne Zeitzone); für ein aware datetime `datetime.now(timezone.utc)` verwenden
- `strptime` ist streng - der Formatstring muss exakt zur Eingabe passen
- `timedelta` speichert intern nur Tage/Sekunden/Mikrosekunden - es gibt kein Konzept für Monate/Jahre

## Siehe auch {#see-also}

- [[data-structures]] - eingebaute dict-, list- und set-Operationen
- [[iterators-and-generators]] - itertools-Modul
- [[file-io]] - os, shutil, tempfile
