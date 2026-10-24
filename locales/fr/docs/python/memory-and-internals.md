---
title: "Gestion de la mémoire et internes de CPython"
category: concepts
tags: [python, cpython, gc, memory, weakref, bytecode, reference-counting, internals]
level: 5
source_sha256: 55632c9fa3ade5b94117f916d76eef6e448e74bfe544c1841189f17814e17033
translation: machine
translated_at: '2026-10-24'
---
# Gestion de la mémoire et internes de CPython {#memory-management-and-cpython-internals}

CPython est l'implémentation de référence de Python : une machine virtuelle à pile qui exécute du bytecode. Comprendre son modèle mémoire, son ramasse-miettes et ses représentations internes aide à écrire du code efficace et à diagnostiquer les problèmes de mémoire.

## Points clés {#key-facts}

- Tout est un `PyObject*` au niveau C
- Le comptage de références est le mécanisme principal de gestion de la mémoire
- Le ramasse-miettes cyclique (générationnel, 3 générations) gère les références circulaires
- Allocateur de petits objets (pymalloc) : les objets de moins de 512 octets utilisent des arènes (256 Ko) -> des pools (4 Ko) -> des blocs
- Le GIL n'autorise qu'un seul thread à exécuter du bytecode à la fois
- Internement des entiers : les petits entiers (-5 à 256) sont des singletons mis en cache
- Internement des chaînes pour les identifiants et les chaînes courtes

## Patrons {#patterns}

### Pipeline de compilation {#compilation-pipeline}
```python
Source (.py) -> Lexer/Parser -> AST -> Compiler -> Bytecode (.pyc) -> CPython VM
```

### Inspection du bytecode {#bytecode-inspection}
```python
import dis
def fib(n):
    return fib(n-1) + fib(n-2) if n > 1 else n

dis.dis(fib)
# LOAD_FAST, LOAD_CONST, COMPARE_OP, CALL_FUNCTION, BINARY_ADD, etc.
```

### Comptage de références {#reference-counting}
```python
import sys

a = []
sys.getrefcount(a)  # 2 (variable + getrefcount arg)

b = a               # refcount increases
del b               # refcount decreases; at 0 -> freed immediately
```

### Problème des références circulaires {#circular-reference-problem}
```python
class A:
    pass

a = A()
b = A()
a.other = b  # a -> b
b.other = a  # b -> a (circular!)

del a, b  # refcounts don't reach 0; GC must collect these
```

### weakref - Rompre les références circulaires {#weakref-breaking-circular-references}
```python
import weakref

b_obj = B()
weak_b = weakref.ref(b_obj)  # does NOT increment refcount
print(weak_b())              # returns B instance if alive

del b_obj
print(weak_b())              # None - object was collected
```

### WeakKeyDictionary (cache à nettoyage automatique) {#weakkeydictionary-auto-cleaning-cache}
```python
import weakref

cache = weakref.WeakKeyDictionary()
obj = MyClass()
cache[obj] = expensive_compute(obj)

del obj  # entry automatically removed from cache
```

### WeakValueDictionary {#weakvaluedictionary}
Les valeurs sont des références faibles : l'entrée disparaît lorsque l'objet valeur est collecté.

### Modèle mémoire {#memory-model}
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

### Copie superficielle et copie profonde {#shallow-vs-deep-copy}
```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)     # top level copied, nested shared
deep = copy.deepcopy(original)    # everything copied recursively

shallow[0].append(5)
print(original[0])  # [1, 2, 5] - shared!
```

### Contrôle du ramasse-miettes {#garbage-collection-control}
```python
import gc

gc.get_threshold()     # (700, 10, 10) - gen0, gen1, gen2 thresholds
gc.collect()           # force collection
gc.disable()           # disable automatic GC (rare, for performance)
gc.get_referrers(obj)  # what references this object
```

## Détails d'implémentation essentiels {#key-implementation-details}

- `BINARY_ADD` dispose d'un chemin rapide pour les entiers (intégré en ligne) et se replie sur `PyNumber_Add` générique
- La boucle d'évaluation principale se trouve dans `Python/ceval.c` : un grand `switch` sur les opcodes
- Chaque instruction fait 2 octets (opcode + argument)
- Les opérations critiques pour les performances disposent de chemins rapides intégrés pour les types courants

### Internes du typage dynamique {#dynamic-typing-internals}

En Python, les variables sont des noms liés à des objets, et non des emplacements mémoire typés :
```python
a = 3       # a -> int object (3)
a = "hello" # a -> str object ("hello"), int(3) refcount decremented
a = 3.14    # a -> float object, str released if refcount=0
```
Ce sont les objets qui portent leur type, pas les variables. C'est pourquoi `type(x)` fonctionne : il demande à l'objet ce qu'il est, et non à la variable.

### Détails de l'internement des chaînes {#string-interning-details}

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
L'internement économise de la mémoire pour les chaînes répétées et accélère la comparaison des clés de dictionnaire (vérification d'identité avant l'égalité).

### Économies de mémoire avec `__slots__` {#__slots__-memory-savings}

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

### Moment de détection des références cycliques {#cyclic-reference-detection-timing}

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

## Pièges à éviter {#gotchas}

- `is` teste l'identité (même objet) ; `==` teste l'égalité : n'utilisez jamais `is` pour comparer des valeurs
- Tous les objets ne supportent pas les références faibles (les `int`, `str`, `tuple` et `list` natifs n'en disposent pas)
- `sys.getrefcount()` affiche toujours +1 (l'argument de la fonction est lui-même une référence temporaire)
- `del x` supprime la liaison du nom, pas l'objet : l'objet n'est libéré que lorsque son nombre de références atteint 0
- Les références circulaires sans `__del__` sont gérées par le ramasse-miettes ; avec `__del__`, elles peuvent provoquer des fuites (Python < 3.4)
- La plage du cache d'entiers va de -5 à 256 : `a = 257; b = 257; a is b` peut valoir False dans le REPL (mais True dans les fichiers .py compilés, grâce au repliement de constantes)
- `sys.getsizeof()` n'inclut PAS la taille des objets référencés : utilisez `pympler.asizeof` pour une mesure en profondeur
- `copy.deepcopy()` gère les références circulaires grâce à un dictionnaire mémo, mais il est lent : profilez avant de l'utiliser dans les chemins critiques
- Un `dict` vide occupe 64 octets, une `list` vide 56 octets : pour des millions de petits enregistrements, envisagez `__slots__` ou les tableaux structurés numpy

## Voir aussi {#see-also}

- [Concurrence - Threading et multiprocessing](concurrency.md) - détails sur le GIL, limites du threading
- [[profiling-and-optimization]] - outils de profilage mémoire
- [[oop-advanced]] - `__slots__` pour l'optimisation mémoire
