---
title: "POO avancée"
category: concepts
tags: [python, abc, descriptors, metaclasses, dataclasses, slots, oop]
level: 4
source_sha256: 115635a66d6d9781c2c4505a770bb80354fd831cf877707b2a39b9f439d69509
translation: machine
translated_at: '2026-10-24'
---
# POO avancée {#oop-advanced}

Les patrons avancés de POO en Python incluent les classes de base abstraites (ABC) pour définir des interfaces, les descripteurs pour contrôler l'accès aux attributs, les métaclasses pour personnaliser la création des classes, les dataclasses pour réduire le code répétitif, et `__slots__` pour l'optimisation de la mémoire.

## Points clés {#key-facts}

- Les ABC imposent des contrats d'interface : impossible d'instancier une classe sans implémenter toutes les méthodes abstraites
- Les descripteurs sont des objets dotés de `__get__`/`__set__`/`__delete__` : ils contrôlent l'accès aux attributs lorsqu'ils sont placés en tant qu'attributs de classe
- Les descripteurs de données (`__set__`) ont la priorité sur le `__dict__` de l'instance ; les descripteurs sans données ne l'ont pas
- `__slots__` restreint les attributs et économise 30 à 40 % de mémoire par instance (pas de `__dict__`)
- `@dataclass` génère automatiquement `__init__`, `__repr__` et `__eq__` à partir des champs annotés par des types
- `__init_subclass__` (Python 3.6+) est une alternative plus simple aux métaclasses pour la plupart des cas d'usage

## Patrons {#patterns}

### Classes de base abstraites {#abstract-base-classes}
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

### Descripteurs {#descriptors}
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

**Priorité de recherche :** descripteur de données > `__dict__` de l'instance > descripteur sans données > `__dict__` de la classe.

### Métaclasses {#metaclasses}
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

### __init_subclass__ (alternative plus simple) {#init_subclass-simpler-alternative}
```python
class Shape:
    registry = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Shape.registry.append(cls)

class Circle(Shape): pass
# Shape.registry == [Circle]
```

### __new__ et __init__ {#new-vs-init}
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

- `__new__` crée l'instance (appelée avant `__init__`)
- `__init__` initialise l'instance (appelée après `__new__`)

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

Avantages : 30 à 40 % de mémoire en moins, accès légèrement plus rapide. Compromis : pas d'attributs dynamiques, pas de `__dict__`.

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

Options : `@dataclass(frozen=True)` pour l'immutabilité, `@dataclass(order=True)` pour les opérateurs de comparaison.

### Combinaison de patrons {#combining-patterns}
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

## Pièges {#gotchas}

- `property`, `classmethod` et `staticmethod` sont tous des descripteurs sous le capot
- `__slots__` ne fonctionne pas avec l'héritage multiple si les deux parents définissent `__slots__`
- Les métaclasses sont rarement nécessaires : privilégiez `__init_subclass__` ou les décorateurs de classe
- Un `@dataclass` avec une valeur par défaut mutable (liste, dictionnaire) nécessite `field(default_factory=list)`
- Les méthodes abstraites peuvent avoir une implémentation (la sous-classe peut appeler `super().method()`)

## Voir aussi {#see-also}

- [[oop-fundamentals]] - notions de base de la POO
- [[magic-methods]] - référence des méthodes dunder
- [[decorators]] - décorateurs à base de classes
- [[type-hints]] - classes génériques, Protocol pour le sous-typage structurel
