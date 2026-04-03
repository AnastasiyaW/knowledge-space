---
title: Magic Methods (Dunder Methods)
category: concepts
tags: [python, magic-methods, dunder, operator-overloading, protocols]
---

# Magic Methods (Dunder Methods)

Magic methods (double-underscore or "dunder" methods) let classes integrate with Python's built-in operations: `len()`, `str()`, `+`, `[]`, iteration, context managers, and more. They define how objects behave with operators and built-in functions.

## Key Facts

- Magic methods are called by Python internals, not directly (`len(obj)` calls `obj.__len__()`)
- `__repr__` for developers (unambiguous); `__str__` for users (readable)
- `__eq__` enables `==`; also required for correct `set`/`dict` behavior (with `__hash__`)
- `__enter__`/`__exit__` implement the context manager protocol (`with` statement)
- `__getitem__`/`__setitem__` enable `obj[key]` syntax
- Never invent your own dunder names - they are reserved for Python

## Patterns

### String Representation
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

### Comparison
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

Use `@functools.total_ordering` to auto-generate `__le__`, `__gt__`, `__ge__` from `__eq__` + `__lt__`.

### Arithmetic
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

### Container Protocol
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

### Callable Objects
```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):   # obj(x) - makes instance callable
        return x * self.factor

double = Multiplier(2)
double(5)  # 10
```

### Context Manager Protocol
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

### Iterator Protocol
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

## Common Magic Methods Reference

| Method | Triggered By | Purpose |
|--------|-------------|---------|
| `__init__` | `Class()` | Initialize instance |
| `__repr__` | `repr()` | Developer string |
| `__str__` | `str()`, `print()` | User string |
| `__len__` | `len()` | Collection size |
| `__getitem__` | `obj[key]` | Index/key access |
| `__setitem__` | `obj[key] = v` | Index/key assignment |
| `__contains__` | `in` | Membership test |
| `__iter__` | `for x in obj` | Iteration |
| `__next__` | `next()` | Next iteration value |
| `__call__` | `obj()` | Make callable |
| `__enter__`/`__exit__` | `with` | Context manager |
| `__eq__` | `==` | Equality |
| `__lt__` | `<` | Less than |
| `__hash__` | `hash()` | Hashability |
| `__add__` | `+` | Addition |
| `__bool__` | `bool()`, `if` | Truthiness |

## Gotchas

- If you define `__eq__`, Python sets `__hash__` to `None` (unhashable) - define `__hash__` explicitly for set/dict use
- `__repr__` is the fallback when `__str__` is not defined
- `__del__` is the finalizer (not destructor) - not guaranteed to be called; avoid for cleanup (use context managers)
- `__new__` creates the object; `__init__` initializes it - rarely need to override `__new__`

## See Also

- [[oop-fundamentals]] - classes, methods, properties
- [[oop-advanced]] - descriptors, metaclasses
- [[error-handling]] - context manager protocol
- [[iterators-and-generators]] - iterator protocol
