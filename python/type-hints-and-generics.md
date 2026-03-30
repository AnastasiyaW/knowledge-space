---
title: Type Hints and Generics
category: concepts
tags: [python, typing, type-hints, generics, mypy, pyright, annotations]
---

# Type Hints and Generics

Python's type hints are optional annotations that enable static type checkers (mypy, pyright) to catch bugs before runtime. Since Python 3.9+, built-in types like `list[int]`, `dict[str, Any]` can be used directly. Generics allow writing type-safe, reusable code parameterized over types.

## Key Facts

- Type hints do not affect runtime behavior -- Python does not enforce them (Pydantic is an exception)
- Python 3.9+: use `list[int]`, `dict[str, int]`, `tuple[str, ...]` directly (no `from typing import`)
- Python 3.10+: use `X | Y` instead of `Union[X, Y]`, and `X | None` instead of `Optional[X]`
- `TypeVar` creates generic type variables; `Generic[T]` makes a class generic
- Python 3.12+: `class Foo[T]:` and `def bar[T](x: T) -> T:` (PEP 695 syntax)
- `Annotated[int, Field(ge=0)]` attaches metadata to types (used by Pydantic, FastAPI)
- `TypeGuard[T]` (PEP 647) narrows types in conditional branches
- `ParamSpec` (PEP 612) preserves function signatures in decorator type hints
- See [[dataclasses-and-pydantic]] for runtime validation, [[fastapi-dependency-injection]] for `Annotated` in FastAPI

## Patterns

### Modern Type Hint Syntax (3.10+)

```python
# Union with |
def process(data: str | bytes) -> str:
    if isinstance(data, bytes):
        return data.decode()
    return data

# Optional is X | None
def find_user(user_id: int) -> User | None:
    return db.get(user_id)

# Built-in generics (3.9+)
def first(items: list[str]) -> str | None:
    return items[0] if items else None

# Complex nested types
Mapping = dict[str, list[tuple[int, float]]]
Callback = Callable[[str, int], bool]
```

### Generic Classes

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)

# Type checker knows s.pop() returns int
s: Stack[int] = Stack()
s.push(42)
value: int = s.pop()
```

### Python 3.12+ Generics Syntax

```python
# PEP 695 -- new syntax (Python 3.12+)
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Generic functions
def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

# Bounded generics
type Number = int | float
def max_val[T: Number](a: T, b: T) -> T:
    return a if a > b else b
```

### `Annotated` for Metadata

```python
from typing import Annotated
from pydantic import Field

# Used by Pydantic/FastAPI for validation metadata
PositiveInt = Annotated[int, Field(gt=0)]
Username = Annotated[str, Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$")]

class UserCreate(BaseModel):
    name: Username
    age: PositiveInt
```

### `ParamSpec` for Decorator Typing

```python
from typing import ParamSpec, TypeVar, Callable
import functools

P = ParamSpec("P")
R = TypeVar("R")

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# Type checker preserves the original signature
greet("Alice")                # OK
greet("Alice", greeting="Hi") # OK
greet(123)                    # Type error caught by mypy/pyright
```

### TypeGuard for Type Narrowing

```python
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(item, str) for item in val)

def process(items: list[object]) -> None:
    if is_str_list(items):
        # Type checker knows items is list[str] here
        print(", ".join(items))
```

## Gotchas

- **`Optional[X]` does not mean "optional parameter"**: `Optional[X]` means `X | None`. A parameter with `Optional[str]` still requires an argument unless it has a default value
- **`list` vs `Sequence`**: `list[int]` is invariant (a `list[bool]` is not a `list[int]`). Use `Sequence[int]` for covariant read-only parameters
- **Forward references**: `def foo() -> "MyClass"` requires quotes (or `from __future__ import annotations` which makes all annotations strings). Python 3.12+ PEP 649 changes evaluation
- **`Any` defeats type checking**: `Any` is compatible with everything -- overusing it removes the benefits of type hints. Prefer `object` when you need a universal type that still requires explicit checks
- **Runtime access to hints**: `get_type_hints(func)` resolves string annotations. `func.__annotations__` may contain raw strings if `from __future__ import annotations` is active

## See Also

- [typing module -- Python docs](https://docs.python.org/3/library/typing.html)
- [PEP 695 -- Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [[dataclasses-and-pydantic]] - runtime validation using type hints
- [[fastapi-dependency-injection]] - `Annotated` for dependency injection
