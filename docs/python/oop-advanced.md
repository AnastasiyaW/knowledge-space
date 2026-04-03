---
title: OOP Advanced
category: concepts
tags: [python, abc, descriptors, metaclasses, dataclasses, slots, oop]
---

# OOP Advanced

Advanced OOP patterns in Python include Abstract Base Classes for defining interfaces, descriptors for attribute access control, metaclasses for class creation customization, dataclasses for boilerplate reduction, and `__slots__` for memory optimization.

## Key Facts

- ABCs enforce interface contracts - cannot instantiate without implementing all abstract methods
- Descriptors are objects with `__get__`/`__set__`/`__delete__` - they control attribute access when placed as class attributes
- Data descriptors (`__set__`) take priority over instance `__dict__`; non-data descriptors don't
- `__slots__` restricts attributes and saves 30-40% memory per instance (no `__dict__`)
- `@dataclass` auto-generates `__init__`, `__repr__`, `__eq__` from type-annotated fields
- `__init_subclass__` (Python 3.6+) is a simpler alternative to metaclasses for most use cases

## Patterns

### Abstract Base Classes
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

# Shape()  -> TypeError: Can't instantiate abstract class
```

### Descriptors
```python
class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage_name = f'_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage_name, None)

    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError(f"{self.name} must be positive")
        setattr(obj, self.storage_name, value)

class Rectangle:
    width = PositiveNumber()   # descriptor as class attribute
    height = PositiveNumber()

    def __init__(self, width, height):
        self.width = width     # triggers __set__
        self.height = height
```

**Lookup priority:** data descriptor > instance `__dict__` > non-data descriptor > class `__dict__`.

### Metaclasses
```python
class ShapeMeta(type):
    registry = set()

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if name != 'Shape':
            mcs.registry.add(cls)
        return cls

class Shape(metaclass=ShapeMeta):
    pass

class Circle(Shape): pass
class Rect(Shape): pass
# ShapeMeta.registry == {Circle, Rect}
```

### __init_subclass__ (Simpler Alternative)
```python
class Shape:
    registry = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Shape.registry.append(cls)

class Circle(Shape): pass
# Shape.registry == [Circle]
```

### __new__ vs __init__
```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.value = 42
```

- `__new__` creates the instance (called before `__init__`)
- `__init__` initializes the instance (called after `__new__`)

### __slots__
```python
class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
p.z = 3  # AttributeError
```

Benefits: 30-40% less memory, slightly faster access. Trade-off: no dynamic attributes, no `__dict__`.

### Dataclasses (Python 3.7+)
```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    label: str = "origin"
    tags: list = field(default_factory=list)  # mutable default

    def distance(self):
        return (self.x**2 + self.y**2) ** 0.5

p = Point(3.0, 4.0)
print(p)  # Point(x=3.0, y=4.0, label='origin', tags=[])
```

Options: `@dataclass(frozen=True)` for immutable, `@dataclass(order=True)` for comparison operators.

### Combining Patterns
```python
from abc import ABCMeta, abstractmethod

class ValidatedMeta(ABCMeta):
    registry = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if not getattr(cls, '__abstractmethods__', None):
            mcs.registry[name] = cls
        return cls

class Shape(metaclass=ValidatedMeta):
    @property
    @abstractmethod
    def area(self): ...
```

## Gotchas

- `property`, `classmethod`, `staticmethod` are all descriptors under the hood
- `__slots__` does not work with multiple inheritance if both parents define `__slots__`
- Metaclasses are rarely needed - prefer `__init_subclass__` or class decorators
- `@dataclass` with mutable default (list, dict) requires `field(default_factory=list)`
- Abstract methods can have implementations (subclass can call `super().method()`)

## See Also

- [[oop-fundamentals]] - basic OOP concepts
- [[magic-methods]] - dunder method reference
- [[decorators]] - class-based decorators
- [[type-hints]] - Generic classes, Protocol for structural subtyping
