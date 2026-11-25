---
title: "Méthodes magiques (méthodes dunder)"
category: concepts
tags: [python, magic-methods, dunder, operator-overloading, protocols]
level: 3
source_sha256: f48713c5f51289f566a7a87885fc607acdfd252bb09fd4f8faca784aef551398
translation: machine
translated_at: '2026-10-24'
---
# Méthodes magiques (méthodes dunder) {#magic-methods-dunder-methods}

Les méthodes magiques (méthodes à double tiret bas, ou « dunder ») permettent aux classes de s'intégrer aux opérations intégrées de Python : `len()`, `str()`, `+`, `[]`, l'itération, les gestionnaires de contexte, et bien d'autres. Elles définissent le comportement des objets avec les opérateurs et les fonctions intégrées.

## Points clés {#key-facts}

- Les méthodes magiques sont appelées par le fonctionnement interne de Python, et non directement (`len(obj)` appelle `obj.__len__()`)
- `__repr__` s'adresse aux développeurs (sans ambiguïté) ; `__str__` s'adresse aux utilisateurs (lisible)
- `__eq__` permet `==` ; elle est aussi nécessaire pour un comportement correct de `set` et `dict` (avec `__hash__`)
- `__enter__`/`__exit__` implémentent le protocole de gestionnaire de contexte (instruction `with`)
- `__getitem__`/`__setitem__` permettent la syntaxe `obj[key]`
- N'inventez jamais vos propres noms dunder : ils sont réservés à Python

## Patrons {#patterns}

### Représentation sous forme de chaîne {#string-representation}
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):    # for developers, unambiguous
        return f"Point({self.x}, {self.y})"

    def __str__(self):     # for users, readable
        return f"({self.x}, {self.y})"

p = Point(1, 2)
repr(p)  # "Point(1, 2)"
str(p)   # "(1, 2)"
print(p) # "(1, 2)" - uses __str__
```

### Comparaison {#comparison}
```python
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __eq__(self, other):
        return self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __le__(self, other):
        return self.amount <= other.amount

    def __hash__(self):
        return hash(self.amount)
```

Utilisez `@functools.total_ordering` pour générer automatiquement `__le__`, `__gt__` et `__ge__` à partir de `__eq__` et `__lt__`.

### Arithmétique {#arithmetic}
```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):      # self + other
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):     # self * scalar
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):    # scalar * self
        return self.__mul__(scalar)

    def __abs__(self):             # abs(self)
        return (self.x**2 + self.y**2) ** 0.5

    def __len__(self):             # len(self)
        return 2
```

### Protocole de conteneur {#container-protocol}
```python
class DataStore:
    def __init__(self):
        self._data = {}

    def __getitem__(self, key):    # obj[key]
        return self._data[key]

    def __setitem__(self, key, value):  # obj[key] = value
        self._data[key] = value

    def __delitem__(self, key):    # del obj[key]
        del self._data[key]

    def __contains__(self, key):   # key in obj
        return key in self._data

    def __len__(self):             # len(obj)
        return len(self._data)
```

### Objets appelables {#callable-objects}
```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):   # obj(x) - makes instance callable
        return x * self.factor

double = Multiplier(2)
double(5)  # 10
```

### Protocole de gestionnaire de contexte {#context-manager-protocol}
```python
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        return False  # don't suppress exceptions

with Timer() as t:
    heavy_work()
print(t.elapsed)
```

### Protocole d'itérateur {#iterator-protocol}
```python
class Range:
    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        val = self.current
        self.current += 1
        return val
```

## Référence des méthodes magiques courantes {#common-magic-methods-reference}

| Méthode | Déclenchée par | Rôle |
|--------|-------------|---------|
| `__init__` | `Class()` | Initialiser l'instance |
| `__repr__` | `repr()` | Chaîne destinée aux développeurs |
| `__str__` | `str()`, `print()` | Chaîne destinée aux utilisateurs |
| `__len__` | `len()` | Taille de la collection |
| `__getitem__` | `obj[key]` | Accès par index ou clé |
| `__setitem__` | `obj[key] = v` | Affectation par index ou clé |
| `__contains__` | `in` | Test d'appartenance |
| `__iter__` | `for x in obj` | Itération |
| `__next__` | `next()` | Valeur suivante de l'itération |
| `__call__` | `obj()` | Rendre l'objet appelable |
| `__enter__`/`__exit__` | `with` | Gestionnaire de contexte |
| `__eq__` | `==` | Égalité |
| `__lt__` | `<` | Inférieur à |
| `__hash__` | `hash()` | Hachabilité |
| `__add__` | `+` | Addition |
| `__bool__` | `bool()`, `if` | Valeur de vérité |

## Pièges {#gotchas}

- Si vous définissez `__eq__`, Python fixe `__hash__` à `None` (non hachable) : définissez explicitement `__hash__` pour une utilisation dans un `set` ou un `dict`
- `__repr__` sert de solution de repli lorsque `__str__` n'est pas défini
- `__del__` est un finaliseur (et non un destructeur) : son appel n'est pas garanti ; évitez-le pour le nettoyage et privilégiez les gestionnaires de contexte
- `__new__` crée l'objet ; `__init__` l'initialise : il est rarement nécessaire de redéfinir `__new__`

## Voir aussi {#see-also}

- [[oop-fundamentals]] - classes, méthodes, propriétés
- [[oop-advanced]] - descripteurs, métaclasses
- [Gestion des erreurs et gestionnaires de contexte](error-handling.md) - protocole de gestionnaire de contexte
- [[iterators-and-generators]] - protocole d'itérateur
