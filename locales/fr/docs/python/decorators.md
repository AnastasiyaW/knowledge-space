---
title: "Décorateurs"
category: concepts
tags: [python, decorators, functools, wraps, metaprogramming]
level: 3
source_sha256: 223bbbfb6d34e77827d6f556843228a555e246b26ac73fff4d856547c93cb18a
translation: machine
translated_at: '2026-10-24'
---
# Décorateurs {#decorators}

Un décorateur est une fonction qui enveloppe une autre fonction afin d'étendre son comportement sans modifier son code source. Les décorateurs sont fondamentaux en Python : ils alimentent `@property`, `@classmethod`, `@staticmethod`, les routes Flask/FastAPI, et bien d'autres motifs.

## Points clés {#key-facts}

- `@decorator` est du sucre syntaxique pour `func = decorator(func)`
- Utiliser systématiquement `@functools.wraps(func)` pour préserver les métadonnées de la fonction d'origine
- Utiliser systématiquement `*args, **kwargs` dans le wrapper et `return func(*args, **kwargs)`
- Les décorateurs empilés s'appliquent de bas en haut : `@bold @italic` équivaut à `bold(italic(func))`
- Les décorateurs avec arguments nécessitent un niveau d'imbrication supplémentaire (fabrique de décorateur)
- Le code du décorateur s'exécute au moment de la définition/de l'import, et non au moment de l'appel

## Motifs {#patterns}

### Modèle de décorateur de base {#basic-decorator-template}
```python
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # code before
        result = func(*args, **kwargs)
        # code after
        return result
    return wrapper
```

### Décorateur avec arguments (fabrique) {#decorator-with-arguments-factory}
```python
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say(msg):
    print(msg)
```

### Empilement de décorateurs {#stacking-decorators}
```python
@bold       # applied second
@italic     # applied first
def greet():
    return "Hello!"
# Equivalent: greet = bold(italic(greet))
```

### Décorateur de chronométrage {#timing-decorator}
```python
import time, functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper
```

### Décorateur de nouvelles tentatives {#retry-decorator}
```python
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def fetch_data(url):
    ...
```

### Mémoïsation / mise en cache {#memoization-caching}
```python
def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

# Built-in alternative:
@functools.lru_cache(maxsize=128)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)
```

### Décorateur de validation {#validation-decorator}
```python
def validate_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if any(arg < 0 for arg in args if isinstance(arg, (int, float))):
            raise ValueError("All numeric arguments must be positive")
        return func(*args, **kwargs)
    return wrapper
```

### Décorateur basé sur une classe (avec état) {#class-based-decorator-with-state}
```python
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello!")
```

### Décorateur de classe (décorant une classe) {#class-decorator-decorating-a-class}
```python
def add_repr(cls):
    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'{cls.__name__}({attrs})'
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### Décorateur à argument optionnel (double mode) {#optional-argument-decorator-dual-mode}

Un décorateur qui fonctionne à la fois avec et sans arguments :
```python
import functools

def decorator(func=None, *, retries=3, delay=1):
    """Works as @decorator or @decorator(retries=5)."""
    if func is None:
        return lambda f: decorator(f, retries=retries, delay=delay)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception:
                if attempt == retries - 1:
                    raise
                time.sleep(delay)
    return wrapper

@decorator           # no parentheses - func passed directly
def task_a(): ...

@decorator(retries=5) # with args - returns decorator
def task_b(): ...
```

### Décorateur de descripteur de méthode {#method-descriptor-decorator}

Lorsqu'un décorateur basé sur une classe enveloppe une méthode d'instance, `self` est perdu car l'instance du décorateur remplace la fonction. Le problème se corrige avec `__get__` :
```python
import functools

class Trace:
    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        print(f"Calling {self.func.__name__}")
        return self.func(*args, **kwargs)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return functools.partial(self.__call__, obj)

class MyClass:
    @Trace
    def method(self):  # now works correctly with self
        return "ok"
```

### Préservation de la signature avec `functools.wraps` {#preserving-signature-with-functoolswraps}

`@functools.wraps` copie `__name__`, `__doc__`, `__module__`, `__qualname__`, `__dict__` et `__wrapped__`. L'attribut `__wrapped__` conserve la fonction d'origine, ce qui permet de contourner le décorateur :
```python
@my_decorator
def process(data):
    ...

# Bypass decorator for testing:
process.__wrapped__(test_data)
```

## Pièges courants {#gotchas}

- Oublier `return func(*args, **kwargs)` fait que la fonction décorée renvoie `None`
- Sans `@functools.wraps`, `func.__name__` devient `'wrapper'`, ce qui gêne le débogage
- Le décorateur s'exécute à l'import : la ligne `@decorator` est évaluée au moment où la fonction est définie
- La décoration manuelle conserve l'accès à l'original : avec `decorated = my_decorator(original)`, `original` reste utilisable
- Un empilement profond de décorateurs ajoute un surcoût d'appel de fonction ; il est généralement négligeable, mais il compte sur les chemins critiques
- Les décorateurs basés sur une classe appliqués à des méthodes perdent `self` : implémenter `__get__` pour renvoyer une méthode liée via `functools.partial`
- `@staticmethod` et `@classmethod` sont des descripteurs ; les empiler avec d'autres décorateurs exige un ordre correct (placer `@staticmethod`/`@classmethod` en haut)
- Les générateurs et coroutines décorés nécessitent un traitement particulier : le wrapper doit utiliser `yield from` ou `async` pour préserver le protocole

## Voir aussi {#see-also}

- [[functions]] - fermetures, fonctions d'ordre supérieur
- [[oop-advanced]] - descripteurs, décorateurs de classe
- [[profiling-and-optimization]] - `@lru_cache` pour les performances
