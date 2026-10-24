---
title: "Dekoratoren"
category: concepts
tags: [python, decorators, functools, wraps, metaprogramming]
level: 3
source_sha256: 223bbbfb6d34e77827d6f556843228a555e246b26ac73fff4d856547c93cb18a
translation: machine
translated_at: '2026-10-24'
---
# Dekoratoren {#decorators}

Ein Dekorator ist eine Funktion, die eine andere Funktion umschließt, um deren Verhalten zu erweitern, ohne deren Quellcode zu verändern. Dekoratoren sind ein grundlegender Bestandteil von Python – sie stecken hinter `@property`, `@classmethod`, `@staticmethod`, Flask-/FastAPI-Routen und vielen weiteren Mustern.

## Kernfakten {#key-facts}

- `@decorator` ist syntaktischer Zucker für `func = decorator(func)`
- Immer `@functools.wraps(func)` verwenden, um die Metadaten der ursprünglichen Funktion zu erhalten
- Im Wrapper immer `*args, **kwargs` und `return func(*args, **kwargs)` verwenden
- Gestapelte Dekoratoren werden von unten nach oben angewendet: `@bold @italic` entspricht `bold(italic(func))`
- Dekoratoren mit Argumenten benötigen eine zusätzliche Verschachtelungsebene (Dekorator-Fabrik)
- Der Code eines Dekorators läuft zur Definitions- bzw. Importzeit, nicht zur Aufrufzeit

## Muster {#patterns}

### Grundlegende Dekorator-Vorlage {#basic-decorator-template}
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

### Dekorator mit Argumenten (Fabrik) {#decorator-with-arguments-factory}
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

### Dekoratoren stapeln {#stacking-decorators}
```python
@bold       # applied second
@italic     # applied first
def greet():
    return "Hello!"
# Equivalent: greet = bold(italic(greet))
```

### Zeitmessung-Dekorator {#timing-decorator}
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

### Wiederholungs-Dekorator (Retry) {#retry-decorator}
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

### Memoisierung / Caching {#memoization-caching}
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

### Validierungs-Dekorator {#validation-decorator}
```python
def validate_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if any(arg < 0 for arg in args if isinstance(arg, (int, float))):
            raise ValueError("All numeric arguments must be positive")
        return func(*args, **kwargs)
    return wrapper
```

### Klassenbasierter Dekorator (mit Zustand) {#class-based-decorator-with-state}
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

### Klassen-Dekorator (dekoriert eine Klasse) {#class-decorator-decorating-a-class}
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

### Dekorator mit optionalem Argument (Dual-Modus) {#optional-argument-decorator-dual-mode}

Ein Dekorator, der sowohl mit als auch ohne Argumente funktioniert:
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

### Methoden-Deskriptor-Dekorator {#method-descriptor-decorator}

Wenn ein klassenbasierter Dekorator eine Instanzmethode umschließt, geht `self` verloren, weil die Dekorator-Instanz die Funktion ersetzt. Abhilfe schafft `__get__`:
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

### Signatur erhalten mit `functools.wraps` {#preserving-signature-with-functoolswraps}

`@functools.wraps` kopiert `__name__`, `__doc__`, `__module__`, `__qualname__`, `__dict__` und `__wrapped__`. Das Attribut `__wrapped__` speichert die ursprüngliche Funktion und ermöglicht so das Umgehen des Dekorators:
```python
@my_decorator
def process(data):
    ...

# Bypass decorator for testing:
process.__wrapped__(test_data)
```

## Fallstricke {#gotchas}

- Wird `return func(*args, **kwargs)` vergessen, gibt die dekorierte Funktion `None` zurück
- Ohne `@functools.wraps` wird `func.__name__` zu `'wrapper'` – das erschwert die Fehlersuche
- Der Dekorator läuft zur Importzeit – die Zeile `@decorator` wird ausgeführt, sobald die Funktion definiert wird
- Manuelles Dekorieren erhält den Zugriff auf das Original: `decorated = my_decorator(original)` – `original` ist weiterhin nutzbar
- Tiefes Stapeln von Dekoratoren verursacht zusätzlichen Aufrufaufwand – meist vernachlässigbar, aber relevant für performancekritische Pfade
- Klassenbasierte Dekoratoren auf Methoden verlieren `self` – `__get__` implementieren, das eine gebundene Methode über `functools.partial` zurückgibt
- `@staticmethod` und `@classmethod` sind Deskriptoren – beim Stapeln mit anderen Dekoratoren ist die richtige Reihenfolge nötig (`@staticmethod`/`@classmethod` oben platzieren)
- Dekorierte Generatoren und Coroutinen erfordern besondere Behandlung – der Wrapper muss `yield from` bzw. `async` verwenden, um das Protokoll zu erhalten

## Siehe auch {#see-also}

- [[functions]] – Closures, Funktionen höherer Ordnung
- [[oop-advanced]] – Deskriptoren, Klassen-Dekoratoren
- [[profiling-and-optimization]] – `@lru_cache` für Performance
