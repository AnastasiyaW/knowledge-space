---
title: "Fehlerbehandlung und Kontextmanager"
category: concepts
tags: [python, exceptions, try-except, context-managers, with-statement, eafp]
level: 3
source_sha256: 56806631537f6126accaa0535acc81397dce4672089a0b73e4a21b884383e3e6
translation: machine
translated_at: '2026-10-24'
---
# Fehlerbehandlung und Kontextmanager {#error-handling-and-context-managers}

Pythons Ausnahmebehandlung verwendet try/except-Blöcke und folgt der EAFP-Philosophie (Easier to Ask Forgiveness than Permission, also: einfacher um Verzeihung bitten als um Erlaubnis fragen). Kontextmanager (`with`-Anweisung) sorgen für automatische Ressourcenfreigabe. Eigene Ausnahmen bilden für Anwendungen aussagekräftige Fehlerhierarchien.

## Wichtige Fakten {#key-facts}

- Verwende niemals ein nacktes `except:` - es fängt `SystemExit` und `KeyboardInterrupt` ab
- `finally` wird immer ausgeführt, auch wenn innerhalb von try/except ein `return` steht
- Der `else`-Block wird nur ausgeführt, wenn im `try`-Block keine Ausnahme ausgelöst wurde
- In Python wird EAFP gegenüber LBYL (Look Before You Leap, also: erst prüfen, dann springen) bevorzugt
- Kontextmanager (`with`) garantieren die Bereinigung auch bei Ausnahmen
- Eigene Ausnahmen sollten von `Exception` erben, nicht von `BaseException`

## Muster {#patterns}

### Einfaches try/except {#basic-tryexcept}
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```

### Mehrere Ausnahmetypen {#multiple-exception-types}
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

### else und finally {#else-and-finally}
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

### Ausnahmen auslösen {#raising-exceptions}
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

### Eigene Ausnahmen {#custom-exceptions}
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

### Kontextmanager (with-Anweisung) {#context-managers-with-statement}
```python
# File handling (automatic close)
with open("file.txt") as f:
    data = f.read()

# Multiple context managers
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read())
```

### Eigener Kontextmanager (Klasse) {#custom-context-manager-class}
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

### Eigener Kontextmanager (contextlib) {#custom-context-manager-contextlib}
```python
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield  # code inside 'with' block runs here
    print(f"Elapsed: {time.time() - start:.2f}s")
```

### EAFP vs. LBYL {#eafp-vs-lbyl}
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

### Bestimmte Ausnahmen unterdrücken {#suppress-specific-exceptions}
```python
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("temp.txt")
```

### Ausnahmen protokollieren {#logging-exceptions}
```python
import logging

try:
    process()
except Exception:
    logging.exception("Processing failed")  # logs full traceback
    raise
```

## Ausnahmehierarchie (wichtige Klassen) {#exception-hierarchy-key-classes}

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

### ExceptionGroup und except* (Python 3.11+) {#exceptiongroup-and-except-python-311}

Behandle mehrere gleichzeitige Ausnahmen (nützlich zusammen mit asyncio-`TaskGroup`):
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

### Details zur Ausnahmeverkettung {#exception-chaining-details}

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

### Verschachtelte Kontextmanager mit ExitStack {#nested-context-managers-with-exitstack}

```python
from contextlib import ExitStack

def process_files(filenames):
    with ExitStack() as stack:
        files = [stack.enter_context(open(f)) for f in filenames]
        # All files closed on exit, even if opening one fails
        return [f.read() for f in files]
```

### Asynchroner Kontextmanager {#async-context-manager}

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

## Stolperfallen {#gotchas}

- `except Exception as e` ist akzeptabel; ein nacktes `except:` fängt zu viel ab
- Ausführungsreihenfolge: try -> except (bei Fehler) -> else (ohne Fehler) -> finally (immer)
- `finally` wird auch dann ausgeführt, wenn in try/except ein `return` steht - der Rückgabewert von `finally` setzt sich durch
- Gibt `__exit__` `True` zurück, wird die Ausnahme unterdrückt - sparsam einsetzen
- Wiederholungsschleifen sollten eine maximale Anzahl an Versuchen haben, um Endlosschleifen zu vermeiden
- `except*`-Klauseln sind **nicht** wechselseitig exklusiv - mehrere können auf eine ExceptionGroup passen
- Die Ausnahmevariable `e` in `except ValueError as e` wird nach dem Verlassen des except-Blocks gelöscht (Gültigkeitsregel, um Referenzzyklen aufzubrechen)
- Ausnahmen innerhalb von `__del__` werden stillschweigend ignoriert - verlasse dich niemals auf Ausnahmen in Destruktoren
- `sys.exc_info()` liefert außerhalb von except-Blöcken `(None, None, None)` - verwende `e.__traceback__`, um Tracebacks zu speichern

## Siehe auch {#see-also}

- [[functions]] - Muster für frühe Rückgabe
- [[fastapi-fundamentals]] - HTTP-Ausnahmebehandlung
- [[testing-with-pytest]] - Testen von Ausnahmen
