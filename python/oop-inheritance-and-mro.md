---
title: OOP - Inheritance and MRO
category: concepts
tags: [python, oop, inheritance, mro, super, abc, protocol, polymorphism]
---

# OOP - Inheritance and MRO

Python supports single and multiple inheritance. The **Method Resolution Order (MRO)** determines the order in which base classes are searched when looking up a method. Python uses the **C3 linearization** algorithm to compute MRO, which guarantees a consistent, predictable order that respects both local precedence and monotonicity.

## Key Facts

- `super()` delegates to the next class in the MRO, not necessarily the parent class
- MRO is computed via C3 linearization and can be inspected with `ClassName.__mro__` or `ClassName.mro()`
- `abc.ABC` or `metaclass=ABCMeta` creates abstract base classes; `@abstractmethod` forces subclass implementation
- `typing.Protocol` (PEP 544) provides structural subtyping (duck typing with type checker support) without inheritance
- Diamond inheritance is resolved by MRO -- each class appears only once in the linearization
- `isinstance()` and `issubclass()` follow MRO; `type()` returns the exact class
- Composition over inheritance is preferred for most real-world designs
- See [[magic-methods]] for `__init_subclass__`, [[metaclasses-and-descriptors]] for metaclass-based customization

## Patterns

### MRO and `super()` with Multiple Inheritance

```python
class A:
    def method(self):
        print("A.method")

class B(A):
    def method(self):
        print("B.method")
        super().method()

class C(A):
    def method(self):
        print("C.method")
        super().method()

class D(B, C):
    def method(self):
        print("D.method")
        super().method()

D().method()
# D.method -> B.method -> C.method -> A.method

print(D.__mro__)
# (D, B, C, A, object)
```

### Abstract Base Class

```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get(self, id: int):
        """Must be implemented by subclasses."""
        ...

    @abstractmethod
    def save(self, entity) -> None:
        ...

    def get_or_none(self, id: int):
        """Concrete method -- available to all subclasses."""
        try:
            return self.get(id)
        except KeyError:
            return None

class PostgresRepository(Repository):
    def get(self, id: int):
        return self.db.query(f"SELECT * FROM items WHERE id = {id}")

    def save(self, entity) -> None:
        self.db.insert(entity)

# Repository()  # TypeError: Can't instantiate abstract class
```

### Protocol (Structural Subtyping)

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Renderable(Protocol):
    def render(self) -> str: ...

class HTMLWidget:
    def render(self) -> str:
        return "<div>widget</div>"

class JSONResponse:
    def render(self) -> str:
        return '{"status": "ok"}'

def display(item: Renderable) -> None:
    print(item.render())

# No inheritance needed -- structural match is enough
display(HTMLWidget())   # works
display(JSONResponse()) # works
isinstance(HTMLWidget(), Renderable)  # True (runtime_checkable)
```

### `__init_subclass__` Hook

```python
class Plugin:
    _registry: dict[str, type] = {}

    def __init_subclass__(cls, plugin_name: str = None, **kwargs):
        super().__init_subclass__(**kwargs)
        name = plugin_name or cls.__name__.lower()
        Plugin._registry[name] = cls

class ImagePlugin(Plugin, plugin_name="image"):
    pass

class VideoPlugin(Plugin, plugin_name="video"):
    pass

print(Plugin._registry)  # {'image': <class 'ImagePlugin'>, 'video': <class 'VideoPlugin'>}
```

### Mixin Pattern

```python
class JSONMixin:
    """Mixin adds JSON serialization to any class with __dict__."""
    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__, default=str)

class TimestampMixin:
    """Mixin adds created_at on init."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from datetime import datetime
        self.created_at = datetime.utcnow()

class User(JSONMixin, TimestampMixin):
    def __init__(self, name: str, email: str):
        super().__init__()
        self.name = name
        self.email = email

u = User("Alice", "alice@example.com")
print(u.to_json())     # includes name, email, created_at
print(u.created_at)     # datetime object
```

## Gotchas

- **`super()` is not "parent"**: in multiple inheritance, `super()` follows MRO, which may skip apparent parent classes. Always call `super().__init__()` in cooperative multiple inheritance to ensure all `__init__` methods in the chain are called
- **Inconsistent MRO**: `class X(A, B)` where A and B have conflicting linearization raises `TypeError: Cannot create a consistent method resolution order`. Reorder base classes to fix
- **Forgetting `super()` in `__init__`**: when using mixins, omitting `super().__init__()` in any class breaks the cooperative chain -- downstream classes' `__init__` is never called
- **`isinstance` with Protocol**: requires `@runtime_checkable` decorator; without it, `isinstance()` raises `TypeError`. Static type checkers (mypy, pyright) check Protocol conformance without this decorator
- **ABC does not prevent `__init__` calls via `type.__call__`**: if you bypass `__init__` (e.g., `object.__new__(SomeABC)`), abstract method checks are skipped

## See Also

- [abc module -- Python docs](https://docs.python.org/3/library/abc.html)
- [PEP 544 -- Protocols: Structural subtyping](https://peps.python.org/pep-0544/)
- [[magic-methods]] - `__init_subclass__`, operator overloading
- [[metaclasses-and-descriptors]] - metaclass-based class customization
