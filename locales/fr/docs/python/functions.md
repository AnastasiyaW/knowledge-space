---
title: "Fonctions"
category: concepts
tags: [python, functions, closures, lambda, scope, higher-order]
level: 3
source_sha256: fbb9764bb331c621493aba8080c48f30521266b2a860f2ecdeb5850978ffd094
translation: machine
translated_at: '2026-10-24'
---
# Fonctions {#functions}

En Python, les fonctions sont des objets de première classe : on peut les passer en argument, les renvoyer depuis d'autres fonctions et les stocker dans des variables. Comprendre les règles de portée (LEGB), les fermetures (closures) et les fonctions d'ordre supérieur est indispensable pour écrire du Python idiomatique.

## Points clés {#key-facts}

- `def` définit une fonction ; sans `return`, la fonction renvoie `None`
- Ordre des paramètres : `def f(pos, *args, key=default, **kwargs)`
- `*args` collecte les arguments positionnels supplémentaires dans un tuple ; `**kwargs` les collecte dans un dictionnaire
- Portée LEGB : Locale, Englobante (Enclosing), Globale, Intégrée (Built-in)
- Les lambdas sont des fonctions anonymes limitées à une seule expression
- `map()` et `filter()` renvoient des itérateurs à usage unique (épuisés après un seul parcours)

## Motifs {#patterns}

### Définition de fonction {#function-definition}
```python
def greet(name, greeting="Hello"):
    """Greeting function with optional prefix."""
    return f"{greeting}, {name}!"

greet("Alice")            # "Hello, Alice!"
greet("Alice", "Hi")      # "Hi, Alice!"
```

### *args et **kwargs {#args-and-kwargs}
```python
def my_func(*args, **kwargs):
    for item in args:        # tuple
        print(item)
    for key, val in kwargs.items():  # dict
        print(f"{key}={val}")

my_func(1, 2, fruit='apple', color='red')
```

### Portée LEGB {#legb-scope}
```python
x = 25          # Global

def outer():
    x = 50      # Enclosing
    def inner():
        x = 75  # Local
        print(x)  # 75
    inner()

outer()
print(x)  # 25 (global unchanged)
```

### global et nonlocal {#global-and-nonlocal}
```python
count = 0
def increment():
    global count    # modify module-level variable
    count += 1

def counter():
    n = 0
    def inc():
        nonlocal n  # modify enclosing scope variable
        n += 1
        return n
    return inc
```

### Fermetures {#closures}
```python
def make_adder(n):
    def add(x):
        return x + n   # n captured from enclosing scope
    return add

plus_3 = make_adder(3)
plus_3(10)  # 13

# Closure with mutable state
def counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```

### Lambda {#lambda}
```python
square = lambda x: x ** 2
add = lambda a, b: a + b
classify = lambda x: 'even' if x % 2 == 0 else 'odd'

# Most useful inline
sorted(words, key=lambda w: len(w))
sorted(items, key=lambda x: x[1])  # sort by second element
```

### map() et filter() {#map-and-filter}
```python
list(map(lambda x: x**2, [1, 2, 3]))       # [1, 4, 9]
list(filter(lambda x: x % 2 == 0, range(10)))  # [0, 2, 4, 6, 8]
list(filter(None, [0, '', None, 'hello']))  # ['hello'] (truthy filter)

# Multiple iterables
list(map(pow, [2, 3, 4], [4, 2, 3]))  # [16, 9, 64]
```

### Module operator (éviter les lambdas triviales) {#operator-module-avoid-trivial-lambdas}
```python
import operator
sorted(items, key=operator.itemgetter(1))   # vs lambda x: x[1]
sorted(objs, key=operator.attrgetter('name'))  # vs lambda x: x.name
```

### Valeurs de retour multiples {#multiple-return-values}
```python
def min_max(lst):
    return min(lst), max(lst)  # returns tuple

lo, hi = min_max([3, 1, 4, 1, 5])  # unpacking
```

### Retour anticipé {#early-return}
```python
def find_first_even(nums):
    for n in nums:
        if n % 2 == 0:
            return n
    return None
```

### Fonctions comme objets de première classe {#functions-as-first-class-objects}
```python
def apply(func, value):
    return func(value)

apply(abs, -5)       # 5
apply(len, "hello")  # 5
```

### Docstrings {#docstrings}
```python
def my_func(param):
    """
    Brief description.

    Args:
        param: description

    Returns:
        description of return value
    """
    pass

# Access: my_func.__doc__ or help(my_func)
```

## Référence des fonctions intégrées {#built-in-functions-reference}

| Catégorie | Fonctions |
|----------|-----------|
| Conversion de type | `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()`, `dict()` |
| Mathématiques | `abs()`, `round()`, `divmod()`, `pow()`, `min()`, `max()`, `sum()` |
| Itération | `len()`, `range()`, `enumerate()`, `zip()`, `sorted()`, `reversed()`, `all()`, `any()` |
| Fonctionnelles | `map()`, `filter()` |
| Introspection | `type()`, `isinstance()`, `id()`, `dir()`, `help()`, `callable()` |
| Conversion de base | `hex()`, `oct()`, `bin()`, `ord()`, `chr()` |

### Arguments keyword-only et positional-only (Python 3.8+) {#keyword-only-and-positional-only-arguments-python-38}

```python
# Everything after * is keyword-only
def tag(name, *, cls=None, id=None):
    ...
tag("div", cls="main")       # OK
tag("div", "main")           # TypeError - cls is keyword-only

# Everything before / is positional-only
def pow(base, exp, /, mod=None):
    ...
pow(2, 10)                   # OK
pow(base=2, exp=10)          # TypeError - base and exp are positional-only

# Combined
def f(pos_only, /, normal, *, kw_only):
    ...
```

### Piège de la liaison tardive des fermetures {#closure-late-binding-trap}

```python
# WRONG - all lambdas capture the same variable i
funcs = [lambda: i for i in range(5)]
[f() for f in funcs]  # [4, 4, 4, 4, 4] - all return last value!

# FIX - bind current value via default argument
funcs = [lambda i=i: i for i in range(5)]
[f() for f in funcs]  # [0, 1, 2, 3, 4] - each captures its own value
```

### functools.reduce {#functoolsreduce}

```python
from functools import reduce

# reduce(func, iterable, initial) - fold left
product = reduce(lambda a, b: a * b, [1, 2, 3, 4])  # 24
# Equivalent: ((1*2)*3)*4

# With initial value
total = reduce(lambda a, b: a + b, [], 0)  # 0 (empty list, no error)
```

### Annotations de fonction (accessibles à l'exécution) {#function-annotations-runtime-accessible}

```python
def greet(name: str, times: int = 1) -> str:
    return name * times

greet.__annotations__
# {'name': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}
# Annotations are metadata only - Python does NOT enforce them at runtime
```

## Pièges courants {#gotchas}

- Ne jamais masquer les noms intégrés : `list = [1, 2]` casse la fonction `list()`
- `map(square, nums)` et non `map(square(), nums)` : on passe l'objet fonction sans l'appeler
- Les itérateurs `map()`/`filter()` sont épuisés après un parcours : convertir en liste si nécessaire
- Les arguments par défaut mutables sont partagés entre les appels : utiliser `def f(x=None): x = x or []`
- Sans `return`, la fonction renvoie `None` implicitement
- Les fermetures capturent les variables par référence, et non par valeur : piège de la variable de boucle, `lambda: i` capture le nom `i`, et non sa valeur courante
- `def f(x=[]): x.append(1)` : la liste par défaut est créée UNE SEULE FOIS à la définition de la fonction et partagée entre tous les appels
- `*args` reçoit un tuple (immuable) ; `**kwargs` reçoit un dictionnaire (mutable)
- `f(*[1,2], *[3,4])` est valide (déballage multiple dans un même appel, Python 3.5+)

## Voir aussi {#see-also}

- [[decorators]] - envelopper des fonctions
- [[iterators-and-generators]] - fonctions génératrices avec yield
- [[oop-fundamentals]] - méthodes et fonctions
