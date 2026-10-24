---
title: "Gestion des erreurs et gestionnaires de contexte"
category: concepts
tags: [python, exceptions, try-except, context-managers, with-statement, eafp]
level: 3
source_sha256: 56806631537f6126accaa0535acc81397dce4672089a0b73e4a21b884383e3e6
translation: machine
translated_at: '2026-10-24'
---
# Gestion des erreurs et gestionnaires de contexte {#error-handling-and-context-managers}

La gestion des exceptions en Python repose sur les blocs try/except et suit la philosophie EAFP (Easier to Ask Forgiveness than Permission, « il est plus facile de demander pardon que la permission »). Les gestionnaires de contexte (instruction `with`) assurent la libération automatique des ressources. Les exceptions personnalisées permettent de construire des hiérarchies d'erreurs significatives pour les applications.

## Points clés {#key-facts}

- Ne jamais utiliser de `except:` nu : il intercepte `SystemExit` et `KeyboardInterrupt`
- `finally` s'exécute toujours, même si un `return` figure dans le bloc try/except
- Le bloc `else` ne s'exécute que si aucune exception n'a été levée dans `try`
- EAFP est préféré à LBYL (Look Before You Leap, « regarder avant de sauter ») en Python
- Les gestionnaires de contexte (`with`) garantissent le nettoyage, même en cas d'exception
- Les exceptions personnalisées doivent hériter de `Exception`, et non de `BaseException`

## Modèles {#patterns}

### try/except de base {#basic-tryexcept}
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```

### Plusieurs types d'exceptions {#multiple-exception-types}
```python
try:
    value = int(input("Number: "))
    result = 10 / value
except ValueError:
    print("Not a valid number")
except ZeroDivisionError:
    print("Cannot divide by zero")
except (TypeError, AttributeError) as e:
    print(f"Error: {e}")
```

### else et finally {#else-and-finally}
```python
try:
    f = open("file.txt")
    data = f.read()
except FileNotFoundError:
    print("File not found")
else:
    print(f"Read {len(data)} chars")  # only if no exception
finally:
    f.close()  # ALWAYS runs
```

### Lever des exceptions {#raising-exceptions}
```python
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")

# Re-raise current exception
try:
    process()
except ValueError:
    logging.error("Failed")
    raise  # re-raise same exception

# Exception chaining
try:
    value = int(user_input)
except ValueError as e:
    raise RuntimeError("Invalid config") from e
```

### Exceptions personnalisées {#custom-exceptions}
```python
class AppError(Exception):
    """Base exception for application."""
    pass

class ValidationError(AppError):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class InsufficientFundsError(AppError):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Cannot withdraw {amount}, balance is {balance}")
```

### Gestionnaires de contexte (instruction with) {#context-managers-with-statement}
```python
# File handling (automatic close)
with open("file.txt") as f:
    data = f.read()

# Multiple context managers
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read())
```

### Gestionnaire de contexte personnalisé (classe) {#custom-context-manager-class}
```python
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        print(f"Elapsed: {self.elapsed:.2f}s")
        return False  # don't suppress exceptions

with Timer() as t:
    heavy_computation()
```

### Gestionnaire de contexte personnalisé (contextlib) {#custom-context-manager-contextlib}
```python
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield  # code inside 'with' block runs here
    print(f"Elapsed: {time.time() - start:.2f}s")
```

### EAFP et LBYL {#eafp-vs-lbyl}
```python
# EAFP (Pythonic) - try first, handle failure
try:
    value = my_dict[key]
except KeyError:
    value = default

# LBYL (less Pythonic) - check first
if key in my_dict:
    value = my_dict[key]
else:
    value = default
```

### Supprimer des exceptions spécifiques {#suppress-specific-exceptions}
```python
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("temp.txt")
```

### Journalisation des exceptions {#logging-exceptions}
```python
import logging

try:
    process()
except Exception:
    logging.exception("Processing failed")  # logs full traceback
    raise
```

## Hiérarchie des exceptions (classes principales) {#exception-hierarchy-key-classes}

```text
BaseException
 +-- SystemExit, KeyboardInterrupt, GeneratorExit
 +-- Exception
      +-- ArithmeticError (ZeroDivisionError, OverflowError)
      +-- AttributeError
      +-- ImportError (ModuleNotFoundError)
      +-- LookupError (IndexError, KeyError)
      +-- NameError (UnboundLocalError)
      +-- OSError (FileNotFoundError, PermissionError)
      +-- TypeError, ValueError, RuntimeError
```

### ExceptionGroup et except* (Python 3.11+) {#exceptiongroup-and-except-python-311}

Gérer plusieurs exceptions concurrentes (utile avec `TaskGroup` d'asyncio) :
```python
# ExceptionGroup bundles multiple exceptions
eg = ExceptionGroup("errors", [ValueError("bad"), TypeError("wrong")])

try:
    raise eg
except* ValueError as exc_group:
    print(f"Value errors: {exc_group.exceptions}")
except* TypeError as exc_group:
    print(f"Type errors: {exc_group.exceptions}")
# Both except* clauses can match - unlike regular except
```

### Détails du chaînage d'exceptions {#exception-chaining-details}

```python
# Implicit chaining - __context__ set automatically
try:
    1 / 0
except ZeroDivisionError:
    raise ValueError("bad input")
    # ValueError.__context__ = ZeroDivisionError (shown as "During handling...")

# Explicit chaining - __cause__ set with 'from'
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    raise AppError("Invalid config") from e
    # AppError.__cause__ = JSONDecodeError (shown as "was the direct cause")

# Suppress context display
raise AppError("clean message") from None
```

### Gestionnaires de contexte imbriqués avec ExitStack {#nested-context-managers-with-exitstack}

```python
from contextlib import ExitStack

def process_files(filenames):
    with ExitStack() as stack:
        files = [stack.enter_context(open(f)) for f in filenames]
        # All files closed on exit, even if opening one fails
        return [f.read() for f in files]
```

### Gestionnaire de contexte asynchrone {#async-context-manager}

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_connection(url):
    conn = await connect(url)
    try:
        yield conn
    finally:
        await conn.close()

async with managed_connection("db://localhost") as conn:
    await conn.execute(query)
```

## Pièges à éviter {#gotchas}

- `except Exception as e` est acceptable ; un `except:` nu intercepte trop de choses
- Ordre d'exécution : try -> except (en cas d'erreur) -> else (en l'absence d'erreur) -> finally (toujours)
- `finally` s'exécute même avec un `return` dans try/except : c'est la valeur de retour du `finally` qui l'emporte
- Si `__exit__` renvoie `True`, l'exception est supprimée : à utiliser avec précaution
- Les boucles de nouvelle tentative doivent avoir un nombre maximal de tentatives pour éviter les boucles infinies
- Les clauses `except*` ne sont **pas** mutuellement exclusives : plusieurs peuvent correspondre à un même ExceptionGroup
- La variable d'exception `e` dans `except ValueError as e` est supprimée à la sortie du bloc except (règle de portée destinée à rompre les cycles de références)
- Une exception levée dans `__del__` est ignorée silencieusement : ne jamais compter sur les exceptions des destructeurs
- `sys.exc_info()` renvoie `(None, None, None)` en dehors des blocs except : utiliser `e.__traceback__` pour conserver les traceback

## Voir aussi {#see-also}

- [[functions]] - modèles de retour anticipé
- [[fastapi-fundamentals]] - gestion des exceptions HTTP
- [[testing-with-pytest]] - tester la levée d'exceptions
