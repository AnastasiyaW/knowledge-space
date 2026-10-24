---
title: "Speicherverwaltung und CPython-Interna"
category: concepts
tags: [python, cpython, gc, memory, weakref, bytecode, reference-counting, internals]
level: 5
source_sha256: 55632c9fa3ade5b94117f916d76eef6e448e74bfe544c1841189f17814e17033
translation: machine
translated_at: '2026-10-24'
---
# Speicherverwaltung und CPython-Interna {#memory-management-and-cpython-internals}

CPython ist die Referenzimplementierung von Python – eine stapelbasierte virtuelle Maschine, die Bytecode ausführt. Das Verständnis ihres Speichermodells, der Garbage Collection und der internen Darstellungen hilft beim Schreiben effizienten Codes und beim Debuggen von Speicherproblemen.

## Wichtige Fakten {#key-facts}

- Auf C-Ebene ist alles ein `PyObject*`
- Die Referenzzählung ist der primäre Mechanismus der Speicherverwaltung
- Der zyklische Garbage Collector (generationell, 3 Generationen) behandelt zirkuläre Referenzen
- Small Object Allocator (pymalloc): Objekte < 512 Byte verwenden Arenen (256 KB) -> Pools (4 KB) -> Blöcke
- Das GIL erlaubt nur einem Thread gleichzeitig, Bytecode auszuführen
- Integer-Interning: Kleine Ints (-5 bis 256) sind gecachte Singletons
- String-Interning für Bezeichner und kurze Strings

## Muster {#patterns}

### Compilation-Pipeline {#compilation-pipeline}
```python
Source (.py) -> Lexer/Parser -> AST -> Compiler -> Bytecode (.pyc) -> CPython VM
```

### Bytecode-Inspektion {#bytecode-inspection}
```python
import dis
def fib(n):
    return fib(n-1) + fib(n-2) if n > 1 else n

dis.dis(fib)
# LOAD_FAST, LOAD_CONST, COMPARE_OP, CALL_FUNCTION, BINARY_ADD, etc.
```

### Referenzzählung {#reference-counting}
```python
import sys

a = []
sys.getrefcount(a)  # 2 (variable + getrefcount arg)

b = a               # refcount increases
del b               # refcount decreases; at 0 -> freed immediately
```

### Problem zirkulärer Referenzen {#circular-reference-problem}
```python
class A:
    pass

a = A()
b = A()
a.other = b  # a -> b
b.other = a  # b -> a (circular!)

del a, b  # refcounts don't reach 0; GC must collect these
```

### weakref – Zirkuläre Referenzen auflösen {#weakref-breaking-circular-references}
```python
import weakref

b_obj = B()
weak_b = weakref.ref(b_obj)  # does NOT increment refcount
print(weak_b())              # returns B instance if alive

del b_obj
print(weak_b())              # None - object was collected
```

### WeakKeyDictionary (selbstbereinigender Cache) {#weakkeydictionary-auto-cleaning-cache}
```python
import weakref

cache = weakref.WeakKeyDictionary()
obj = MyClass()
cache[obj] = expensive_compute(obj)

del obj  # entry automatically removed from cache
```

### WeakValueDictionary {#weakvaluedictionary}
Werte sind schwache Referenzen – der Eintrag verschwindet, sobald das Wertobjekt eingesammelt wird.

### Speichermodell {#memory-model}
```python
# Variables are references (names) to objects
a = [1, 2, 3]
b = a          # same object
id(a) == id(b) # True
a is b         # True (identity check)

# Integer interning
x = 256
y = 256
x is y  # True (cached singleton)

z = 257
w = 257
z is w  # May be False (not cached)
```

### Flache vs. tiefe Kopie {#shallow-vs-deep-copy}
```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)     # top level copied, nested shared
deep = copy.deepcopy(original)    # everything copied recursively

shallow[0].append(5)
print(original[0])  # [1, 2, 5] - shared!
```

### Steuerung der Garbage Collection {#garbage-collection-control}
```python
import gc

gc.get_threshold()     # (700, 10, 10) - gen0, gen1, gen2 thresholds
gc.collect()           # force collection
gc.disable()           # disable automatic GC (rare, for performance)
gc.get_referrers(obj)  # what references this object
```

## Wichtige Implementierungsdetails {#key-implementation-details}

- `BINARY_ADD` hat einen Fast Path für int (inline) und fällt auf das generische `PyNumber_Add` zurück
- Die Haupt-Eval-Schleife befindet sich in `Python/ceval.c` – ein riesiger Switch über Opcodes
- Jede Instruktion ist 2 Byte groß (Opcode + Argument)
- Performance-kritische Operationen haben inline Fast Paths für gängige Typen

### Interna der dynamischen Typisierung {#dynamic-typing-internals}

Variablen in Python sind Namen, die an Objekte gebunden sind, nicht typisierte Speicherplätze:
```python
a = 3       # a -> int object (3)
a = "hello" # a -> str object ("hello"), int(3) refcount decremented
a = 3.14    # a -> float object, str released if refcount=0
```
Objekte tragen ihren Typ, nicht die Variablen. Deshalb funktioniert `type(x)` – es fragt das Objekt, was es ist, nicht die Variable.

### Details zum String-Interning {#string-interning-details}

```python
a = "hello"
b = "hello"
a is b          # True - Python interns short strings (identifiers)

a = "hello world!"
b = "hello world!"
a is b          # May be False - strings with spaces/special chars not always interned

# Force interning
import sys
a = sys.intern("hello world!")
b = sys.intern("hello world!")
a is b          # True - same object
```
Interning spart Speicher bei wiederholten Strings und beschleunigt den Dict-Schlüsselvergleich (Identitätsprüfung vor Gleichheitsprüfung).

### `__slots__` und Speichereinsparung {#__slots__-memory-savings}

```python
import sys

class Regular:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Slotted:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

sys.getsizeof(Regular(1, 2))    # ~48 bytes + __dict__ (~104 bytes)
sys.getsizeof(Slotted(1, 2))    # ~48 bytes (no __dict__)
# With 1M instances: Regular ~152MB vs Slotted ~48MB
```

### Zeitpunkt der Erkennung zirkulärer Referenzen {#cyclic-reference-detection-timing}

```python
import gc

# Generation thresholds control when GC runs
gc.get_threshold()  # (700, 10, 10)
# Gen 0 collects after 700 allocations - deallocations
# Gen 1 collects after 10 Gen 0 collections
# Gen 2 collects after 10 Gen 1 collections

# Objects surviving collection are promoted to next generation
# Long-lived objects get checked less frequently - efficient for caches
```

## Fallstricke {#gotchas}

- `is` prüft die Identität (dasselbe Objekt), `==` prüft die Gleichheit – `is` niemals für Wertvergleiche verwenden
- Nicht alle Objekte unterstützen schwache Referenzen (eingebaute `int`, `str`, `tuple` und `list` nicht)
- `sys.getrefcount()` zeigt immer +1 (das Funktionsargument selbst ist eine temporäre Referenz)
- `del x` entfernt die Namensbindung, nicht das Objekt – das Objekt wird erst freigegeben, wenn der Referenzzähler 0 erreicht
- Zirkuläre Referenzen ohne `__del__` werden vom GC behandelt; mit `__del__` können sie lecken (Python < 3.4)
- Der Integer-Cache reicht von -5 bis 256 – `a = 257; b = 257; a is b` kann in der REPL False ergeben (in kompilierten .py-Dateien aufgrund von Constant Folding jedoch True)
- `sys.getsizeof()` berücksichtigt die Größen referenzierter Objekte NICHT – für tiefe Messungen `pympler.asizeof` verwenden
- `copy.deepcopy()` behandelt zirkuläre Referenzen über ein Memo-Dict, ist aber langsam – vor dem Einsatz in heißen Pfaden profilen
- Ein leeres `dict` belegt 64 Byte, eine leere `list` 56 Byte – bei Millionen kleiner Datensätze `__slots__` oder numpy-Structured-Arrays in Betracht ziehen

## Siehe auch {#see-also}

- [Concurrency - Threading und Multiprocessing](concurrency.md) - Details zum GIL, Einschränkungen von Threading
- [[profiling-and-optimization]] - Werkzeuge für Speicherprofiling
- [[oop-advanced]] - `__slots__` zur Speicheroptimierung
