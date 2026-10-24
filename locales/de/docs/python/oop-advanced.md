---
title: "OOP Advanced"
category: concepts
tags: [python, abc, descriptors, metaclasses, dataclasses, slots, oop]
level: 4
source_sha256: 115635a66d6d9781c2c4505a770bb80354fd831cf877707b2a39b9f439d69509
translation: machine
translated_at: '2026-10-24'
---
# Fortgeschrittene OOP {#oop-advanced}

Fortgeschrittene OOP-Muster in Python umfassen Abstrakte Basisklassen zur Definition von Schnittstellen, Deskriptoren zur Steuerung des Attributzugriffs, Metaklassen zur Anpassung der Klassenerzeugung, Dataclasses zur Reduzierung von Boilerplate-Code und `__slots__` zur Speicheroptimierung.

## Key Facts {#key-facts}

- ABCs erzwingen Schnittstellenverträge - eine Instanziierung ist nicht möglich, solange nicht alle abstrakten Methoden implementiert sind
- Deskriptoren sind Objekte mit `__get__`/`__set__`/`__delete__` - sie steuern den Attributzugriff, wenn sie als Klassenattribute definiert sind
- Datendeskriptoren (`__set__`) haben Vorrang vor dem Instanz-`__dict__`; Nicht-Datendeskriptoren haben diesen Vorrang nicht
- `__slots__` beschränkt die Attribute und spart 30-40 % Speicher pro Instanz (kein `__dict__`)
- `@dataclass` generiert `__init__`, `__repr__`, `__eq__` automatisch aus typannotierten Feldern
- `__init_subclass__` (Python 3.6+) ist für die meisten Anwendungsfälle eine einfachere Alternative zu Metaklassen

## Patterns {#patterns}

### Abstrakte Basisklassen {#abstract-base-classes}
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

### Deskriptoren {#descriptors}
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

**Suchpriorität:** Datendeskriptor > Instanz-`__dict__` > Nicht-Datendeskriptor > Klassen-`__dict__`.

### Metaklassen {#metaclasses}
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

### __init_subclass__ (einfachere Alternative) {#init_subclass-simpler-alternative}
```python
class Shape:
    registry = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Shape.registry.append(cls)

class Circle(Shape): pass
# Shape.registry == [Circle]
```

### __new__ vs. __init__ {#new-vs-init}
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

- `__new__` erzeugt die Instanz (wird vor `__init__` aufgerufen)
- `__init__` initialisiert die Instanz (wird nach `__new__` aufgerufen)

### __slots__ {#slots}
```python
class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
p.z = 3  # AttributeError
```

Vorteile: 30-40 % weniger Speicher, etwas schnellerer Zugriff. Nachteil: keine dynamischen Attribute, kein `__dict__`.

### Dataclasses (Python 3.7+) {#dataclasses-python-37}
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

Optionen: `@dataclass(frozen=True)` für unveränderliche Instanzen, `@dataclass(order=True)` für Vergleichsoperatoren.

### Kombination von Mustern {#combining-patterns}
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

## Gotchas {#gotchas}

- `property`, `classmethod` und `staticmethod` sind unter der Haube allesamt Deskriptoren
- `__slots__` funktioniert nicht bei Mehrfachvererbung, wenn beide Elternklassen `__slots__` definieren
- Metaklassen werden selten benötigt - bevorzuge `__init_subclass__` oder Klassendekoratoren
- `@dataclass` mit veränderlichem Standardwert (list, dict) erfordert `field(default_factory=list)`
- Abstrakte Methoden können Implementierungen haben (Subklasse kann `super().method()` aufrufen)

## See Also {#see-also}

- [[oop-fundamentals]] - grundlegende OOP-Konzepte
- [[magic-methods]] - Referenz der Dunder-Methoden
- [[decorators]] - klassenbasierte Dekoratoren
- [[type-hints]] - generische Klassen, Protocol für strukturelle Subtypisierung
