---
title: "Typhinweise und statische Typisierung"
category: concepts
tags: [python, type-hints, mypy, generics, protocol, typing]
level: 3
source_sha256: 03417ec58b6fc6d69d233d206c277f2ea235262057ee16fd80926bec5be93a40
translation: machine
translated_at: '2026-10-24'
---
# Typhinweise und statische Typisierung {#type-hints-and-static-typing}

Typhinweise sind optionale Annotationen für Dokumentation, IDE-Unterstützung und statische Analyse (mypy). Sie werden zur Laufzeit NICHT erzwungen. Der Einstieg über Funktionssignaturen bringt den größten Nutzen bei dem geringsten Aufwand.

## Wichtige Fakten {#key-facts}

- Python 3.9+: eingebaute `list[str]`, `dict[str, int]` direkt verwenden (kein `typing.List`)
- Python 3.10+: `int | str` statt `Union[int, str]` verwenden
- `Optional[X]` ist eine Kurzform für `X | None`
- `Protocol` ermöglicht strukturelle Subtypisierung (Duck Typing mit Typprüfung)
- `TypeVar` erzeugt generische Typvariablen
- mypy ist der Standard-Typprüfer für statische Analyse; ausführen mit `mypy script.py`

## Muster {#patterns}

### Grundlegende Annotationen {#basic-annotations}
```python
# Variables (Python 3.6+)
name: str = "Alice"
age: int = 30
is_active: bool = True

# Functions (Python 3.5+)
def greet(name: str, times: int = 1) -> str:
    return f"Hello, {name}! " * times
```

### Container-Typen {#container-types}
```python
# Python 3.9+
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 95}
coords: tuple[float, float] = (1.0, 2.0)
unique: set[int] = {1, 2, 3}

# Python 3.5-3.8 (import from typing)
from typing import List, Dict, Tuple, Set
```

### Optional und Union {#optional-and-union}
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

### Generics und TypeVar {#generics-and-typevar}
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

### Protocol (strukturelle Subtypisierung) {#protocol-structural-subtyping}
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

### Spezielle Typen {#special-types}
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

### Typ-Aliase {#type-aliases}
```python
Vector = list[float]

# Python 3.12+
type Vector = list[float]
type Matrix = list[Vector]
```

### Flexible Parametertypen {#flexible-parameter-types}
```python
from typing import Sequence, Mapping, Iterable

# Use abstract types for parameters (more flexible)
def process(items: Sequence[int]) -> list[int]:  # accepts list, tuple, str
    return sorted(items)

# Use concrete types for return values (caller knows exactly what they get)
```

## mypy-Konfiguration {#mypy-configuration}

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

## Fallstricke {#gotchas}

- Typhinweise werden zur Laufzeit NICHT erzwungen – sie sind nur für Werkzeuge gedacht
- `def f(x: str = None)` sollte `def f(x: str | None = None)` lauten – `None` ist kein `str`
- `Any` vermeiden – es deaktiviert die Typprüfung für diesen Wert
- Das `__annotations__`-Dict speichert die rohen Annotationen; für aufgelöste Typen `typing.get_type_hints()` verwenden
- Zirkuläre Importe mit Typhinweisen: `from __future__ import annotations` oder `TYPE_CHECKING` verwenden

## Siehe auch {#see-also}

- [[oop-advanced]] – Generische Klassen, Protocol für strukturelle Subtypisierung
- [[fastapi-pydantic-validation]] – Pydantic verwendet Typhinweise für die Validierung zur Laufzeit
- [[testing-with-pytest]] – mypy in der CI
