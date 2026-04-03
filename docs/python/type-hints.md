---
title: Type Hints and Static Typing
category: concepts
tags: [python, type-hints, mypy, generics, protocol, typing]
---

# Type Hints and Static Typing

Type hints are optional annotations for documentation, IDE support, and static analysis (mypy). They do NOT enforce types at runtime. Starting with function signatures provides the most value for least effort.

## Key Facts

- Python 3.9+: use built-in `list[str]`, `dict[str, int]` directly (no `typing.List`)
- Python 3.10+: use `int | str` instead of `Union[int, str]`
- `Optional[X]` is shorthand for `X | None`
- `Protocol` enables structural subtyping (duck typing with type checking)
- `TypeVar` creates generic type variables
- mypy is the standard static type checker; run `mypy script.py`

## Patterns

### Basic Annotations
```python
# Variables (Python 3.6+)
name: str = "Alice"
age: int = 30
is_active: bool = True

# Functions (Python 3.5+)
def greet(name: str, times: int = 1) -> str:
    return f"Hello, {name}! " * times
```

### Container Types
```python
# Python 3.9+
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 95}
coords: tuple[float, float] = (1.0, 2.0)
unique: set[int] = {1, 2, 3}

# Python 3.5-3.8 (import from typing)
from typing import List, Dict, Tuple, Set
```

### Optional and Union
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

### Callable
```python
from typing import Callable

def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

callback: Callable[..., None]  # any args, returns None
```

### Generics and TypeVar
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

### Protocol (Structural Subtyping)
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

### Special Types
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

### Type Aliases
```python
Vector = list[float]

# Python 3.12+
type Vector = list[float]
type Matrix = list[Vector]
```

### Flexible Parameter Types
```python
from typing import Sequence, Mapping, Iterable

# Use abstract types for parameters (more flexible)
def process(items: Sequence[int]) -> list[int]:  # accepts list, tuple, str
    return sorted(items)

# Use concrete types for return values (caller knows exactly what they get)
```

## mypy Configuration

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

## Gotchas

- Type hints are NOT enforced at runtime - they are for tools only
- `def f(x: str = None)` should be `def f(x: str | None = None)` - `None` is not `str`
- Avoid `Any` - it disables type checking for that value
- `__annotations__` dict stores raw annotations; use `typing.get_type_hints()` for resolved types
- Circular imports with type hints: use `from __future__ import annotations` or `TYPE_CHECKING`

## See Also

- [[oop-advanced]] - Generic classes, Protocol for structural subtyping
- [[fastapi-pydantic-validation]] - Pydantic uses type hints for runtime validation
- [[testing-with-pytest]] - mypy in CI
