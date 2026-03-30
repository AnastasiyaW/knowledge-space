---
title: Metaclasses and Descriptors
category: concepts
tags: [python, metaclass, descriptor, __get__, __set__, __new__, metaprogramming]
---

# Metaclasses and Descriptors

A **metaclass** is the class of a class -- it controls how classes are created and can modify class attributes at definition time. A **descriptor** is an object defining `__get__`, `__set__`, or `__delete__` that customizes attribute access when placed on a class. Together, they form Python's most powerful metaprogramming primitives.

## Key Facts

- `type` is the default metaclass: `class Foo:` is equivalent to `Foo = type('Foo', (object,), {...})`
- Custom metaclass: `class Meta(type)` overriding `__new__` or `__init__`
- `__new__(mcs, name, bases, namespace)` creates the class object; `__init__` initializes it
- `__prepare__` can return a custom namespace (e.g., `OrderedDict`) for class body execution
- A **data descriptor** defines `__get__` and `__set__` (or `__delete__`); takes priority over instance `__dict__`
- A **non-data descriptor** defines only `__get__`; instance `__dict__` takes priority
- Functions are non-data descriptors -- `func.__get__(obj, type)` returns a bound method
- `property`, `classmethod`, `staticmethod` are implemented as descriptors
- See [[oop-inheritance-and-mro]] for `__init_subclass__` (simpler alternative to metaclasses), [[magic-methods]] for `__new__`

## Patterns

### Custom Metaclass -- Auto-Registry

```python
class PluginMeta(type):
    """Metaclass that auto-registers all subclasses."""
    registry: dict[str, type] = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        if bases:  # skip the base class itself
            PluginMeta.registry[name] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    pass

class ImagePlugin(Plugin):
    pass

class AudioPlugin(Plugin):
    pass

print(PluginMeta.registry)
# {'ImagePlugin': <class 'ImagePlugin'>, 'AudioPlugin': <class 'AudioPlugin'>}
```

### Data Descriptor -- Validated Attribute

```python
class Positive:
    """Descriptor that enforces positive values."""
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        if value <= 0:
            raise ValueError(f"{self.name} must be positive, got {value}")
        setattr(obj, self.private_name, value)

class Product:
    price = Positive()
    quantity = Positive()

    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price        # goes through Positive.__set__
        self.quantity = quantity

p = Product("Widget", 9.99, 100)
# p.price = -5  # ValueError: price must be positive, got -5
```

### Descriptor Lookup Order

```python
# Attribute lookup for obj.attr follows this priority:
# 1. Data descriptor on type(obj) (has __get__ AND __set__)
# 2. Instance __dict__['attr']
# 3. Non-data descriptor on type(obj) (has __get__ only)
# 4. Class __dict__['attr']
# 5. __getattr__ (if defined)

# This is why property (data descriptor) overrides instance __dict__,
# but a regular method (non-data descriptor) does not.
```

### `__prepare__` for Ordered Namespace

```python
class OrderedMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        return {}  # dict is ordered since Python 3.7, but this
                    # hook allows custom namespace objects

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        cls._fields = [
            k for k, v in namespace.items()
            if not k.startswith("_") and not callable(v)
        ]
        return cls

class Config(metaclass=OrderedMeta):
    host = "localhost"
    port = 8080
    debug = True

print(Config._fields)  # ['host', 'port', 'debug']
```

### Simpler Alternative: `__init_subclass__`

```python
# For most metaclass use cases (registration, validation),
# __init_subclass__ (PEP 487) is simpler and sufficient:

class Serializable:
    _formats: dict[str, type] = {}

    def __init_subclass__(cls, format: str = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if format:
            Serializable._formats[format] = cls

class JSONSerializer(Serializable, format="json"):
    pass

class XMLSerializer(Serializable, format="xml"):
    pass

# No metaclass needed!
```

## Gotchas

- **Metaclass conflict**: a class cannot have two metaclasses unless one is a subclass of the other. `class C(A, B)` where A uses MetaA and B uses MetaB raises `TypeError`. Fix: create `class MetaC(MetaA, MetaB)`
- **`__init_subclass__` covers 90% of metaclass use cases**: registration, validation, attribute injection. Use metaclass only when you need `__prepare__` or must intercept class creation before `__init_subclass__` runs
- **`__set_name__` (PEP 487)**: descriptors should implement `__set_name__(self, owner, name)` to auto-discover their attribute name. Without it, the descriptor cannot know its own name
- **Descriptor on instance vs class**: descriptors only work when defined as **class attributes**. Putting a descriptor instance in `__init__` (instance attribute) bypasses the descriptor protocol
- **`property` is a data descriptor**: it has `__get__`, `__set__`, and `__delete__`. This is why assigning `obj.prop = value` calls the setter, not creating an instance attribute

## See Also

- [Descriptor HowTo Guide -- Python docs](https://docs.python.org/3/howto/descriptor.html)
- [PEP 487 -- Simpler customization of class creation](https://peps.python.org/pep-0487/)
- [[oop-inheritance-and-mro]] - `__init_subclass__` pattern
- [[dataclasses-and-pydantic]] - descriptor-based field validation in Pydantic
