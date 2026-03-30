---
title: Magic Methods (Dunder Methods)
category: concepts
tags: [python, magic-methods, dunder, operator-overloading, protocols, special-methods]
---

# Magic Methods (Dunder Methods)

Magic methods (double-underscore or "dunder" methods) are special methods that Python calls implicitly in response to operators, built-in functions, and language constructs. They define how objects behave with `+`, `[]`, `len()`, `str()`, comparison operators, context managers, iteration, and more.

## Key Facts

- `__init__` initializes an instance; `__new__` creates it (called before `__init__`)
- `__repr__` is for developers (unambiguous), `__str__` is for users (readable); `print()` calls `__str__`, falling back to `__repr__`
- `__eq__` defines `==`; if `__eq__` is defined, `__hash__` is set to `None` (objects become unhashable) unless `__hash__` is explicitly defined
- `__lt__`, `__le__`, `__gt__`, `__ge__` enable comparisons; `@functools.total_ordering` fills in the rest from `__eq__` + one comparison
- `__getitem__`, `__setitem__`, `__delitem__` make objects subscriptable (`obj[key]`)
- `__len__`, `__contains__` support `len()` and `in` operator
- `__call__` makes instances callable: `obj(args)` invokes `obj.__call__(args)`
- `__slots__` restricts instance attributes, saving memory (no `__dict__`)
- See [[oop-inheritance-and-mro]] for `__init_subclass__`, [[context-managers]] for `__enter__`/`__exit__`

## Patterns

### Representation Methods

```python
class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = amount
        self.currency = currency

    def __repr__(self) -> str:
        return f"Money({self.amount!r}, {self.currency!r})"

    def __str__(self) -> str:
        return f"{self.amount:.2f} {self.currency}"

m = Money(42.5, "EUR")
repr(m)  # "Money(42.5, 'EUR')"
str(m)   # "42.50 EUR"
print(m) # "42.50 EUR"
```

### Operator Overloading

```python
from __future__ import annotations

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> Vector:
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vector:
        return self.__mul__(scalar)

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(v1 + v2)     # Vector(4, 6)
print(3 * v1)      # Vector(9, 12) -- __rmul__
print(abs(v1))     # 5.0
```

### Container Protocol

```python
class Config:
    """Dict-like access via magic methods."""
    def __init__(self, data: dict):
        self._data = data

    def __getitem__(self, key: str):
        return self._data[key]

    def __setitem__(self, key: str, value):
        self._data[key] = value

    def __delitem__(self, key: str):
        del self._data[key]

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

cfg = Config({"debug": True, "port": 8000})
cfg["host"] = "0.0.0.0"
print("debug" in cfg)  # True
print(len(cfg))         # 3
```

### `__slots__` for Memory Optimization

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

p = Point(1.0, 2.0)
# p.z = 3.0  # AttributeError: 'Point' has no attribute 'z'
# No __dict__ -- ~40% less memory per instance
```

### `__call__` for Callable Objects

```python
class Validator:
    def __init__(self, min_val: float, max_val: float):
        self.min_val = min_val
        self.max_val = max_val

    def __call__(self, value: float) -> bool:
        return self.min_val <= value <= self.max_val

check_age = Validator(0, 150)
check_age(25)   # True
check_age(-1)   # False
callable(check_age)  # True
```

### Comparison with `total_ordering`

```python
import functools

@functools.total_ordering
class Version:
    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    # __le__, __gt__, __ge__ are auto-generated by @total_ordering
```

## Gotchas

- **`__eq__` breaks hashing**: defining `__eq__` without `__hash__` makes instances unhashable (cannot be dict keys or set members). Always define both together, or set `__hash__ = None` explicitly
- **Returning `NotImplemented` vs raising `NotImplementedError`**: `__eq__`, `__add__` etc. should return `NotImplemented` (a sentinel) to let Python try the reflected method on the other operand. Raising `NotImplementedError` is for abstract methods
- **`__slots__` with inheritance**: slots are not inherited -- each class in the hierarchy must define its own `__slots__`. If a parent lacks `__slots__`, instances still get `__dict__`
- **`__del__` is not `__exit__`**: `__del__` (finalizer) has no guaranteed call timing, is unreliable for cleanup. Use `__enter__`/`__exit__` or `atexit` instead
- **`__repr__` in f-strings**: `f"{obj!r}"` calls `__repr__`, `f"{obj!s}"` calls `__str__`, `f"{obj}"` calls `__format__` then `__str__`

## See Also

- [Data model -- Python docs](https://docs.python.org/3/reference/datamodel.html)
- [functools.total_ordering](https://docs.python.org/3/library/functools.html#functools.total_ordering)
- [[dataclasses-and-pydantic]] - auto-generated `__init__`, `__repr__`, `__eq__`
- [[oop-inheritance-and-mro]] - `__init_subclass__`, `super()`
