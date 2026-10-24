---
title: "Magische Methoden (Dunder-Methoden)"
category: concepts
tags: [python, magic-methods, dunder, operator-overloading, protocols]
level: 3
source_sha256: f48713c5f51289f566a7a87885fc607acdfd252bb09fd4f8faca784aef551398
translation: machine
translated_at: '2026-10-24'
---
# Magische Methoden (Dunder-Methoden) {#magic-methods-dunder-methods}

Magische Methoden (Methoden mit doppeltem Unterstrich, sogenannte „Dunder“-Methoden) ermöglichen es Klassen, sich in die eingebauten Operationen von Python einzubinden: `len()`, `str()`, `+`, `[]`, Iteration, Kontextmanager und mehr. Sie definieren, wie sich Objekte bei Operatoren und eingebauten Funktionen verhalten.

## Wichtige Fakten {#key-facts}

- Magische Methoden werden von den internen Mechanismen von Python aufgerufen, nicht direkt (`len(obj)` ruft `obj.__len__()` auf)
- `__repr__` für Entwickler (eindeutig); `__str__` für Benutzer (lesbar)
- `__eq__` ermöglicht `==`; zusammen mit `__hash__` ist es außerdem für korrektes Verhalten von `set`/`dict` erforderlich
- `__enter__`/`__exit__` implementieren das Kontextmanager-Protokoll (`with`-Anweisung)
- `__getitem__`/`__setitem__` ermöglichen die Syntax `obj[key]`
- Erfinde niemals eigene Dunder-Namen – sie sind für Python reserviert

## Muster {#patterns}

### Zeichenkettendarstellung {#string-representation}
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):    # for developers, unambiguous
        return f"Point({self.x}, {self.y})"

    def __str__(self):     # for users, readable
        return f"({self.x}, {self.y})"

p = Point(1, 2)
repr(p)  # "Point(1, 2)"
str(p)   # "(1, 2)"
print(p) # "(1, 2)" - uses __str__
```

### Vergleich {#comparison}
```python
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __eq__(self, other):
        return self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __le__(self, other):
        return self.amount <= other.amount

    def __hash__(self):
        return hash(self.amount)
```

Verwende `@functools.total_ordering`, um `__le__`, `__gt__` und `__ge__` aus `__eq__` + `__lt__` automatisch zu generieren.

### Arithmetik {#arithmetic}
```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):      # self + other
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):     # self * scalar
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):    # scalar * self
        return self.__mul__(scalar)

    def __abs__(self):             # abs(self)
        return (self.x**2 + self.y**2) ** 0.5

    def __len__(self):             # len(self)
        return 2
```

### Container-Protokoll {#container-protocol}
```python
class DataStore:
    def __init__(self):
        self._data = {}

    def __getitem__(self, key):    # obj[key]
        return self._data[key]

    def __setitem__(self, key, value):  # obj[key] = value
        self._data[key] = value

    def __delitem__(self, key):    # del obj[key]
        del self._data[key]

    def __contains__(self, key):   # key in obj
        return key in self._data

    def __len__(self):             # len(obj)
        return len(self._data)
```

### Aufrufbare Objekte {#callable-objects}
```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):   # obj(x) - makes instance callable
        return x * self.factor

double = Multiplier(2)
double(5)  # 10
```

### Kontextmanager-Protokoll {#context-manager-protocol}
```python
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        return False  # don't suppress exceptions

with Timer() as t:
    heavy_work()
print(t.elapsed)
```

### Iterator-Protokoll {#iterator-protocol}
```python
class Range:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        val = self.current
        self.current += 1
        return val
```

## Referenz häufiger magischer Methoden {#common-magic-methods-reference}

| Methode | Ausgelöst durch | Zweck |
|--------|-------------|---------|
| `__init__` | `Class()` | Instanz initialisieren |
| `__repr__` | `repr()` | Entwickler-Zeichenkette |
| `__str__` | `str()`, `print()` | Benutzer-Zeichenkette |
| `__len__` | `len()` | Größe der Sammlung |
| `__getitem__` | `obj[key]` | Zugriff per Index/Schlüssel |
| `__setitem__` | `obj[key] = v` | Zuweisung per Index/Schlüssel |
| `__contains__` | `in` | Mitgliedschaftsprüfung |
| `__iter__` | `for x in obj` | Iteration |
| `__next__` | `next()` | Nächster Iterationswert |
| `__call__` | `obj()` | Aufrufbar machen |
| `__enter__`/`__exit__` | `with` | Kontextmanager |
| `__eq__` | `==` | Gleichheit |
| `__lt__` | `<` | Kleiner als |
| `__hash__` | `hash()` | Hashbarkeit |
| `__add__` | `+` | Addition |
| `__bool__` | `bool()`, `if` | Wahrheitswert |

## Fallstricke {#gotchas}

- Wenn du `__eq__` definierst, setzt Python `__hash__` auf `None` (nicht hashbar). Definiere `__hash__` explizit für die Verwendung in `set`/`dict`.
- `__repr__` dient als Fallback, wenn `__str__` nicht definiert ist.
- `__del__` ist ein Finalizer (kein Destruktor). Es ist nicht garantiert, dass er aufgerufen wird; für Aufräumarbeiten besser vermeiden (stattdessen Kontextmanager verwenden).
- `__new__` erzeugt das Objekt, `__init__` initialisiert es. Eine Überschreibung von `__new__` ist selten nötig.

## Siehe auch {#see-also}

- [[oop-fundamentals]] - Klassen, Methoden, Properties
- [[oop-advanced]] - Deskriptoren, Metaklassen
- [Fehlerbehandlung und Kontextmanager](error-handling.md) - Kontextmanager-Protokoll
- [[iterators-and-generators]] - Iterator-Protokoll
