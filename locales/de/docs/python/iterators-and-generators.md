---
title: "Iteratoren und Generatoren"
category: concepts
tags: [python, iterators, generators, yield, itertools, lazy-evaluation]
level: 3
source_sha256: 0f1ae9f6643c44467781c6160edec7bf7296c6804f79624f257b21c76c38227b
translation: machine
translated_at: '2026-10-24'
---
# Iteratoren und Generatoren {#iterators-and-generators}

Iteratoren implementieren das Iterationsprotokoll (`__iter__`/`__next__`), während Generatoren mit `yield` eine kompakte Möglichkeit bieten, Iteratoren zu erzeugen. Generatorausdrücke ermöglichen speichereffiziente, verzögerte Auswertung (Lazy Evaluation). Das Modul `itertools` stellt einen Werkzeugkasten aus kombinierbaren Iterator-Bausteinen bereit.

## Wichtige Fakten {#key-facts}

- Iterable: besitzt `__iter__()`. Iterator: besitzt `__next__()` (löst `StopIteration` aus, wenn er erschöpft ist)
- Alle Iteratoren sind Iterables, aber nicht alle Iterables sind Iteratoren (Listen sind iterierbar, aber keine Iteratoren)
- Generatoren sind einmalig verwendbar – nach einer Iteration sind sie erschöpft
- Generatorausdrücke verwenden `()` statt `[]` – unabhängig von der Größe konstanter Speicherbedarf
- `yield` pausiert die Funktion und erhält den lokalen Zustand; `return` beendet die Funktion
- `yield from` delegiert an ein anderes Iterable bzw. einen anderen Generator

## Muster {#patterns}

### Iterationsprotokoll {#iterator-protocol}
```python
# How for-loop actually works:
my_list = [1, 2, 3]
iterator = iter(my_list)       # calls __iter__()
while True:
    try:
        item = next(iterator)  # calls __next__()
    except StopIteration:
        break
```

### Eigener Iterator {#custom-iterator}
```python
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1
```

### Generatorfunktionen {#generator-functions}
```python
def count_up(n):
    i = 1
    while i <= n:
        yield i    # pauses here, returns i
        i += 1     # resumes here on next()

gen = count_up(3)
next(gen)  # 1
next(gen)  # 2
next(gen)  # 3
next(gen)  # StopIteration
```

### yield from {#yield-from}
```python
def flatten(nested):
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

list(flatten([1, [2, [3, 4], 5], 6]))  # [1, 2, 3, 4, 5, 6]
```

### Generatorausdrücke {#generator-expressions}
```python
squares = (x**2 for x in range(1_000_000))  # lazy, ~constant memory
sum(x**2 for x in range(100))               # no extra parentheses in function call
```

### send() – Zweiseitige Generatoren {#send-two-way-generators}
```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

gen = accumulator()
next(gen)        # 0 (must initialize with next() first)
gen.send(10)     # 10
gen.send(20)     # 30
```

### Pipeline-Muster (Unix-Pipes) {#pipeline-pattern-unix-pipes}
```python
def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

def filter_comments(lines):
    for line in lines:
        if not line.startswith('#'):
            yield line

def parse_csv(lines):
    for line in lines:
        yield line.split(',')

# Chained - processes file line by line, minimal memory
pipeline = parse_csv(filter_comments(read_lines("data.csv")))
for row in pipeline:
    process(row)
```

### Unendliche Sequenzen {#infinite-sequences}
```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

from itertools import islice
list(islice(fibonacci(), 10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

## Modul itertools {#itertools-module}

### Unendliche Iteratoren {#infinite-iterators}
```python
from itertools import count, cycle, repeat
count(10, 2)        # 10, 12, 14, 16, ...
cycle([1, 2, 3])    # 1, 2, 3, 1, 2, 3, ...
repeat('x', 3)      # 'x', 'x', 'x'
```

### Endliche Iteratoren {#terminating-iterators}
```python
from itertools import chain, islice, zip_longest, takewhile, dropwhile
from itertools import filterfalse, accumulate, groupby, tee, pairwise

chain([1,2], [3,4])             # [1, 2, 3, 4]
islice(count(), 5)              # [0, 1, 2, 3, 4]
zip_longest([1,2], [3,4,5], fillvalue=0)  # [(1,3), (2,4), (0,5)]
takewhile(lambda x: x < 5, [1,3,5,2])    # [1, 3]
dropwhile(lambda x: x < 5, [1,3,5,2])    # [5, 2]
accumulate([1,2,3,4,5])        # [1, 3, 6, 10, 15]
pairwise([1,2,3,4])            # [(1,2), (2,3), (3,4)]  (Python 3.10+)
```

### Kombinatorische Iteratoren {#combinatoric-iterators}
```python
from itertools import product, permutations, combinations

product([1,2], ['a','b'])       # [(1,'a'), (1,'b'), (2,'a'), (2,'b')]
permutations([1,2,3], 2)       # [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]
combinations([1,2,3,4], 2)     # [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]
```

### groupby (erfordert sortierte Eingabe) {#groupby-requires-sorted-input}
```python
from itertools import groupby
data = sorted(students, key=lambda s: s.grade)
for grade, group in groupby(data, key=lambda s: s.grade):
    print(grade, list(group))
```

### Generator .throw() und .close() {#generator-throw-and-close}

```python
def resilient_reader(path):
    with open(path) as f:
        for line in f:
            try:
                yield line.strip()
            except GeneratorExit:
                print("Cleanup on close")
                return
            except Exception as e:
                print(f"Handling injected: {e}")

gen = resilient_reader("data.txt")
next(gen)
gen.throw(ValueError, "bad data")   # inject exception at yield point
gen.close()                          # raises GeneratorExit inside generator
```

### Delegation an Subgeneratoren mit yield from {#subgenerator-delegation-with-yield-from}

`yield from` ist mehr als syntaktischer Zucker – es delegiert `.send()`, `.throw()` und `.close()` korrekt an den Subgenerator:
```python
def accumulate():
    total = 0
    while True:
        value = yield total
        if value is None:
            return total       # return value becomes StopIteration.value
        total += value

def main():
    result = yield from accumulate()  # delegates send/throw/close
    print(f"Final: {result}")

gen = main()
next(gen)        # prime
gen.send(10)     # 10
gen.send(20)     # 30
gen.send(None)   # triggers return, prints "Final: 30"
```

### Iterator vs. Iterable – das Wiederverwendbarkeitsmuster {#iterator-vs-iterable-the-reusability-pattern}

```python
# Iterable (reusable) - returns new iterator each time
class Sentence:
    def __init__(self, text):
        self.words = text.split()
    def __iter__(self):
        return iter(self.words)   # new iterator each call

s = Sentence("one two three")
list(s)  # ['one', 'two', 'three']
list(s)  # ['one', 'two', 'three'] - works again!

# Iterator (single-use) - IS its own iterator
class WordIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0
    def __iter__(self):
        return self           # returns self = single-use
    def __next__(self):
        if self.index >= len(self.words):
            raise StopIteration
        word = self.words[self.index]
        self.index += 1
        return word
```

### batched() (Python 3.12+) {#batched-python-312}

```python
from itertools import batched

list(batched("ABCDEFG", 3))   # [('A','B','C'), ('D','E','F'), ('G',)]
# Replaces common "chunks" recipe
```

## Stolperfallen {#gotchas}

- Generatoren sind einmalig verwendbar – nach einer Iteration sind sie erschöpft; für eine erneute Iteration muss ein neuer Generator erzeugt werden
- `groupby` gruppiert aufeinanderfolgende gleiche Schlüssel – für eine vollständige Gruppierung ist vorsortierte Eingabe erforderlich
- `len(gen)` lässt sich nicht ermitteln – `sum(1 for _ in gen)` funktioniert, erschöpft den Generator dabei aber
- `tee(iterator, n)` erzeugt n Kopien, wobei das Weiterschalten einer Kopie die anderen nicht weiterschaltet – der Speicherbedarf wächst
- Ein zweites `list(map_result)` liefert eine leere Liste – Iteratoren werden verbraucht
- Generator-`.send()` erfordert zuerst `next(gen)`, um den Generator vorzubereiten – ein Aufruf von `.send(value)` auf einem frischen Generator löst einen TypeError aus
- `yield from` delegiert `.close()` an den Subgenerator – ignoriert dieser GeneratorExit, wird ein RuntimeError ausgelöst
- Eine Listenkomprehension `[x for x in gen]` erschöpft den Generator – danach kann er nicht mehr verwendet werden
- `itertools.chain` akzeptiert Iterables, nicht ausschließlich Iteratoren – übergibt man jedoch einen erschöpften Iterator, trägt dieser nichts bei

## Siehe auch {#see-also}

- [[functions]] - Generatorfunktionen, yield
- [[async-programming]] - asynchrone Generatoren
- [[data-structures]] - Komprehensionen als Alternative
