---
title: "Funktionen"
category: concepts
tags: [python, functions, closures, lambda, scope, higher-order]
level: 3
source_sha256: fbb9764bb331c621493aba8080c48f30521266b2a860f2ecdeb5850978ffd094
translation: machine
translated_at: '2026-10-24'
---
# Funktionen {#functions}

Funktionen sind in Python First-Class-Objekte: Sie können als Argumente übergeben, von anderen Funktionen zurückgegeben und in Variablen gespeichert werden. Die Scope-Regeln (LEGB), Closures und Higher-Order-Funktionen sind essenziell, um idiomatisches Python zu schreiben.

## Wichtige Fakten {#key-facts}

- `def` definiert eine Funktion; ohne `return` gibt die Funktion `None` zurück
- Parameterreihenfolge: `def f(pos, *args, key=default, **kwargs)`
- `*args` sammelt zusätzliche Positionsargumente als Tuple; `**kwargs` als Dictionary
- LEGB-Scope: Local, Enclosing, Global, Built-in
- Lambdas sind anonyme Funktionen mit einem einzigen Ausdruck
- `map()` und `filter()` liefern einmalig verwendbare Iteratoren (nach einem Durchlauf erschöpft)

## Muster {#patterns}

### Funktionsdefinition {#function-definition}
```python
def greet(name, greeting="Hello"):
    """Greeting function with optional prefix."""
    return f"{greeting}, {name}!"

greet("Alice")            # "Hello, Alice!"
greet("Alice", "Hi")      # "Hi, Alice!"
```

### *args und **kwargs {#args-and-kwargs}
```python
def my_func(*args, **kwargs):
    for item in args:        # tuple
        print(item)
    for key, val in kwargs.items():  # dict
        print(f"{key}={val}")

my_func(1, 2, fruit='apple', color='red')
```

### LEGB-Scope {#legb-scope}
```python
x = 25          # Global

def outer():
    x = 50      # Enclosing
    def inner():
        x = 75  # Local
        print(x)  # 75
    inner()

outer()
print(x)  # 25 (global unchanged)
```

### global und nonlocal {#global-and-nonlocal}
```python
count = 0
def increment():
    global count    # modify module-level variable
    count += 1

def counter():
    n = 0
    def inc():
        nonlocal n  # modify enclosing scope variable
        n += 1
        return n
    return inc
```

### Closures {#closures}
```python
def make_adder(n):
    def add(x):
        return x + n   # n captured from enclosing scope
    return add

plus_3 = make_adder(3)
plus_3(10)  # 13

# Closure with mutable state
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```

### Lambda {#lambda}
```python
square = lambda x: x ** 2
add = lambda a, b: a + b
classify = lambda x: 'even' if x % 2 == 0 else 'odd'

# Most useful inline
sorted(words, key=lambda w: len(w))
sorted(items, key=lambda x: x[1])  # sort by second element
```

### map() und filter() {#map-and-filter}
```python
list(map(lambda x: x**2, [1, 2, 3]))       # [1, 4, 9]
list(filter(lambda x: x % 2 == 0, range(10)))  # [0, 2, 4, 6, 8]
list(filter(None, [0, '', None, 'hello']))  # ['hello'] (truthy filter)

# Multiple iterables
list(map(pow, [2, 3, 4], [4, 2, 3]))  # [16, 9, 64]
```

### Modul operator (triviale Lambdas vermeiden) {#operator-module-avoid-trivial-lambdas}
```python
import operator
sorted(items, key=operator.itemgetter(1))   # vs lambda x: x[1]
sorted(objs, key=operator.attrgetter('name'))  # vs lambda x: x.name
```

### Mehrere Rückgabewerte {#multiple-return-values}
```python
def min_max(lst):
    return min(lst), max(lst)  # returns tuple

lo, hi = min_max([3, 1, 4, 1, 5])  # unpacking
```

### Frühe Rückgabe {#early-return}
```python
def find_first_even(nums):
    for n in nums:
        if n % 2 == 0:
            return n
    return None
```

### Funktionen als First-Class-Objekte {#functions-as-first-class-objects}
```python
def apply(func, value):
    return func(value)

apply(abs, -5)       # 5
apply(len, "hello")  # 5
```

### Docstrings {#docstrings}
```python
def my_func(param):
    """
    Brief description.

    Args:
        param: description

    Returns:
        description of return value
    """
    pass

# Access: my_func.__doc__ or help(my_func)
```

## Referenz der eingebauten Funktionen {#built-in-functions-reference}

| Kategorie | Funktionen |
|----------|-----------|
| Typkonvertierung | `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()`, `dict()` |
| Mathematik | `abs()`, `round()`, `divmod()`, `pow()`, `min()`, `max()`, `sum()` |
| Iteration | `len()`, `range()`, `enumerate()`, `zip()`, `sorted()`, `reversed()`, `all()`, `any()` |
| Funktional | `map()`, `filter()` |
| Introspektion | `type()`, `isinstance()`, `id()`, `dir()`, `help()`, `callable()` |
| Basiskonvertierung | `hex()`, `oct()`, `bin()`, `ord()`, `chr()` |

### Keyword-only- und Positional-only-Argumente (Python 3.8+) {#keyword-only-and-positional-only-arguments-python-38}

```python
# Everything after * is keyword-only
def tag(name, *, cls=None, id=None):
    ...
tag("div", cls="main")       # OK
tag("div", "main")           # TypeError - cls is keyword-only

# Everything before / is positional-only
def pow(base, exp, /, mod=None):
    ...
pow(2, 10)                   # OK
pow(base=2, exp=10)          # TypeError - base and exp are positional-only

# Combined
def f(pos_only, /, normal, *, kw_only):
    ...
```

### Closure-Falle durch Late Binding {#closure-late-binding-trap}

```python
# WRONG - all lambdas capture the same variable i
funcs = [lambda: i for i in range(5)]
[f() for f in funcs]  # [4, 4, 4, 4, 4] - all return last value!

# FIX - bind current value via default argument
funcs = [lambda i=i: i for i in range(5)]
[f() for f in funcs]  # [0, 1, 2, 3, 4] - each captures its own value
```

### functools.reduce {#functoolsreduce}

```python
from functools import reduce

# reduce(func, iterable, initial) - fold left
product = reduce(lambda a, b: a * b, [1, 2, 3, 4])  # 24
# Equivalent: ((1*2)*3)*4

# With initial value
total = reduce(lambda a, b: a + b, [], 0)  # 0 (empty list, no error)
```

### Funktionsannotationen (zur Laufzeit zugänglich) {#function-annotations-runtime-accessible}

```python
def greet(name: str, times: int = 1) -> str:
    return name * times

greet.__annotations__
# {'name': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}
# Annotations are metadata only - Python does NOT enforce them at runtime
```

## Stolperfallen {#gotchas}

- Eingebaute Namen niemals überschreiben: `list = [1, 2]` bricht die Funktion `list()`
- `map(square, nums)` statt `map(square(), nums)` - das Funktionsobjekt übergeben, ohne es aufzurufen
- Iteratoren von `map()`/`filter()` sind nach einem Durchlauf erschöpft - bei Bedarf in eine Liste umwandeln
- Veränderliche Standardargumente werden über alle Aufrufe hinweg geteilt: stattdessen `def f(x=None): x = x or []` verwenden
- Ohne `return` gibt eine Funktion implizit `None` zurück
- Closures erfassen Variablen per Referenz, nicht per Wert - Falle bei Schleifenvariablen: `lambda: i` erfasst den Namen `i`, nicht dessen aktuellen Wert
- `def f(x=[]): x.append(1)` - die Standardliste wird EINMAL zur Definitionszeit der Funktion erzeugt und über alle Aufrufe geteilt
- `*args` erhält ein Tuple (unveränderlich); `**kwargs` erhält ein Dictionary (veränderlich)
- `f(*[1,2], *[3,4])` ist gültig (mehrfaches Entpacken in einem einzigen Aufruf, Python 3.5+)

## Siehe auch {#see-also}

- [[decorators]] - Funktionen umhüllen
- [[iterators-and-generators]] - Generatorfunktionen mit yield
- [[oop-fundamentals]] - Methoden versus Funktionen
