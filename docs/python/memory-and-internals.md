---
title: Memory Management and CPython Internals
category: concepts
tags: [python, cpython, gc, memory, weakref, bytecode, reference-counting, internals]
---

# Memory Management and CPython Internals

CPython is the reference Python implementation - a stack-based virtual machine executing bytecode. Understanding its memory model, garbage collection, and internal representations helps write efficient code and debug memory issues.

## Key Facts

- Everything is a `PyObject*` at the C level
- Reference counting is the primary memory management mechanism
- Cyclic garbage collector (generational, 3 generations) handles circular references
- Small object allocator (pymalloc): objects < 512 bytes use arenas (256KB) -> pools (4KB) -> blocks
- GIL allows only one thread to execute bytecode at a time
- Integer interning: small ints (-5 to 256) are cached singletons
- String interning for identifiers and short strings

## Patterns

### Compilation Pipeline
```python
Source (.py) -> Lexer/Parser -> AST -> Compiler -> Bytecode (.pyc) -> CPython VM
```

### Bytecode Inspection
```python
import dis
def fib(n):
    return fib(n-1) + fib(n-2) if n > 1 else n

dis.dis(fib)
# LOAD_FAST, LOAD_CONST, COMPARE_OP, CALL_FUNCTION, BINARY_ADD, etc.
```

### Reference Counting
```python
import sys

a = []
sys.getrefcount(a)  # 2 (variable + getrefcount arg)

b = a               # refcount increases
del b               # refcount decreases; at 0 -> freed immediately
```

### Circular Reference Problem
```python
class A:
    pass

a = A()
b = A()
a.other = b  # a -> b
b.other = a  # b -> a (circular!)

del a, b  # refcounts don't reach 0; GC must collect these
```

### weakref - Breaking Circular References
```python
import weakref

b_obj = B()
weak_b = weakref.ref(b_obj)  # does NOT increment refcount
print(weak_b())              # returns B instance if alive

del b_obj
print(weak_b())              # None - object was collected
```

### WeakKeyDictionary (Auto-Cleaning Cache)
```python
import weakref

cache = weakref.WeakKeyDictionary()
obj = MyClass()
cache[obj] = expensive_compute(obj)

del obj  # entry automatically removed from cache
```

### WeakValueDictionary
Values are weak refs - entry disappears when value object is collected.

### Memory Model
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

### Shallow vs Deep Copy
```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)     # top level copied, nested shared
deep = copy.deepcopy(original)    # everything copied recursively

shallow[0].append(5)
print(original[0])  # [1, 2, 5] - shared!
```

### Garbage Collection Control
```python
import gc

gc.get_threshold()     # (700, 10, 10) - gen0, gen1, gen2 thresholds
gc.collect()           # force collection
gc.disable()           # disable automatic GC (rare, for performance)
gc.get_referrers(obj)  # what references this object
```

## Key Implementation Details

- `BINARY_ADD` has fast path for int (inlined), falls back to generic `PyNumber_Add`
- The main eval loop is in `Python/ceval.c` - giant switch over opcodes
- Each instruction is 2 bytes (opcode + argument)
- Performance-critical operations have inlined fast paths for common types

### Dynamic Typing Internals

Variables in Python are names bound to objects, not typed memory slots:
```python
a = 3       # a -> int object (3)
a = "hello" # a -> str object ("hello"), int(3) refcount decremented
a = 3.14    # a -> float object, str released if refcount=0
```
Objects carry their type, not variables. This is why `type(x)` works - it asks the object what it is, not the variable.

### String Interning Details

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
Interning saves memory for repeated strings and speeds up dict key comparison (identity check before equality).

### `__slots__` Memory Savings

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

### Cyclic Reference Detection Timing

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

## Gotchas

- `is` checks identity (same object); `==` checks equality - never use `is` for value comparison
- Not all objects support weak references (built-in `int`, `str`, `tuple`, `list` don't)
- `sys.getrefcount()` always shows +1 (the function argument itself is a temporary reference)
- `del x` removes the name binding, not the object - object freed only when refcount reaches 0
- Circular references without `__del__` are handled by GC; with `__del__` they may leak (Python < 3.4)
- Integer cache range is -5 to 256 - `a = 257; b = 257; a is b` may be False in the REPL (but True in compiled .py files due to constant folding)
- `sys.getsizeof()` does NOT include sizes of referenced objects - use `pympler.asizeof` for deep measurement
- `copy.deepcopy()` handles circular references via a memo dict but is slow - profile before using in hot paths
- Empty `dict` uses 64 bytes, empty `list` uses 56 bytes - for millions of small records, consider `__slots__` or numpy structured arrays

## See Also

- [[concurrency]] - GIL details, threading limitations
- [[profiling-and-optimization]] - memory profiling tools
- [[oop-advanced]] - `__slots__` for memory optimization
