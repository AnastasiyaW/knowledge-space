---
title: "Annotations de types et typage statique"
category: concepts
tags: [python, type-hints, mypy, generics, protocol, typing]
level: 3
source_sha256: 03417ec58b6fc6d69d233d206c277f2ea235262057ee16fd80926bec5be93a40
translation: machine
translated_at: '2026-10-24'
---
# Annotations de types et typage statique {#type-hints-and-static-typing}

Les annotations de types sont des indications facultatives destinées à la documentation, au support des IDE et à l'analyse statique (mypy). Elles ne imposent PAS de types à l'exécution. Commencer par les signatures de fonctions offre le meilleur rapport valeur/effort.

## Points clés {#key-facts}

- Python 3.9+ : utiliser directement les types intégrés `list[str]`, `dict[str, int]` (sans `typing.List`)
- Python 3.10+ : utiliser `int | str` au lieu de `Union[int, str]`
- `Optional[X]` est un raccourci pour `X | None`
- `Protocol` permet le sous-typage structurel (duck typing avec vérification de types)
- `TypeVar` crée des variables de type génériques
- mypy est le vérificateur de types statique de référence ; lancer `mypy script.py`

## Modèles {#patterns}

### Annotations de base {#basic-annotations}
```python
# Variables (Python 3.6+)
name: str = "Alice"
age: int = 30
is_active: bool = True

# Functions (Python 3.5+)
def greet(name: str, times: int = 1) -> str:
    return f"Hello, {name}! " * times
```

### Types conteneurs {#container-types}
```python
# Python 3.9+
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 95}
coords: tuple[float, float] = (1.0, 2.0)
unique: set[int] = {1, 2, 3}

# Python 3.5-3.8 (import from typing)
from typing import List, Dict, Tuple, Set
```

### Optional et Union {#optional-and-union}
```python
def find_user(user_id: int) -> str | None:  # Python 3.10+
    ...

# Pre-3.10
from typing import Optional, Union
def find_user(user_id: int) -> Optional[str]:
    ...
def process(value: Union[int, str]) -> str:
    ...
```

### Callable {#callable}
```python
from typing import Callable

def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

callback: Callable[..., None]  # any args, returns None
```

### Génériques et TypeVar {#generics-and-typevar}
```python
from typing import TypeVar, Generic

T = TypeVar('T')

def first(items: list[T]) -> T:
    return items[0]

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

stack: Stack[int] = Stack()
```

### Protocol (sous-typage structurel) {#protocol-structural-subtyping}
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

def render(shape: Drawable) -> None:
    shape.draw()

render(Circle())  # OK - Circle has draw() method, no inheritance needed
```

### Types spéciaux {#special-types}
```python
from typing import Literal, Final, TypedDict, NewType

# Restrict to specific values
def set_mode(mode: Literal["read", "write"]) -> None: ...

# Constants
MAX_SIZE: Final = 100

# Typed dictionaries
class UserDict(TypedDict):
    name: str
    age: int

# Distinct types
UserId = NewType('UserId', int)
```

### Alias de types {#type-aliases}
```python
Vector = list[float]

# Python 3.12+
type Vector = list[float]
type Matrix = list[Vector]
```

### Types de paramètres flexibles {#flexible-parameter-types}
```python
from typing import Sequence, Mapping, Iterable

# Use abstract types for parameters (more flexible)
def process(items: Sequence[int]) -> list[int]:  # accepts list, tuple, str
    return sorted(items)

# Use concrete types for return values (caller knows exactly what they get)
```

## Configuration de mypy {#mypy-configuration}

```ini
# mypy.ini or pyproject.toml [tool.mypy]
[mypy]
python_version = 3.10
strict = true
warn_return_any = true
disallow_untyped_defs = true
```

```python
x = some_func()  # type: ignore  -- suppress mypy error on this line
```

## Pièges {#gotchas}

- Les annotations de types NE sont PAS imposées à l'exécution : elles sont destinées uniquement aux outils
- `def f(x: str = None)` doit devenir `def f(x: str | None = None)` : `None` n'est pas un `str`
- Éviter `Any` : cela désactive la vérification de types pour cette valeur
- Le dictionnaire `__annotations__` stocke les annotations brutes ; utiliser `typing.get_type_hints()` pour obtenir les types résolus
- Imports circulaires avec annotations de types : utiliser `from __future__ import annotations` ou `TYPE_CHECKING`

## Voir aussi {#see-also}

- [[oop-advanced]] - Classes génériques, Protocol pour le sous-typage structurel
- [[fastapi-pydantic-validation]] - Pydantic utilise les annotations de types pour la validation à l'exécution
- [[testing-with-pytest]] - mypy dans la CI
