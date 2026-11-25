---
title: "Kontrollfluss"
category: concepts
tags: [python, loops, conditionals, comprehensions, iteration]
level: 3
source_sha256: 746abd27ed14afbd33b4adbbba5cd5ad53726e645dde86686b2220b66c75157d
translation: machine
translated_at: '2026-10-24'
---
# Kontrollfluss {#control-flow}

Python verwendet Einrückungen (4 Leerzeichen), um Codeblöcke abzugrenzen. Zu den Kontrollflusskonstrukten gehören Verzweigungen, `for`- und `while`-Schleifen sowie Comprehensions als prägnante Alternativen zu Mustern aus Schleife und Akkumulation.

## Wichtige Fakten {#key-facts}

- Die Einrückung ist syntaktisch relevant – 4 Leerzeichen pro Ebene (PEP 8)
- `for`-Schleifen iterieren über beliebige Iterables (Liste, Tupel, String, `range`, Generator usw.)
- `range(n)` erzeugt `0, 1, ..., n-1`; `range(start, stop, step)` für volle Kontrolle
- Comprehensions (Liste, Dict, Menge) ersetzen einfache Muster aus for-Schleife mit `append`
- `break` beendet die Schleife; `continue` springt zur nächsten Iteration; `pass` ist ein No-Op-Platzhalter

## Muster {#patterns}

### Verzweigungen {#conditionals}
```python
if condition:
    pass
elif another:
    pass
else:
    pass

# Ternary expression
result = "even" if x % 2 == 0 else "odd"

# Truthy/falsy shortcuts
if my_list:    # True if non-empty
if name:       # True if non-empty string
if count:      # True if non-zero
```

### For-Schleifen {#for-loops}
```python
for item in [1, 2, 3]:
    print(item)

for i in range(5):              # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10, 3):      # 2, 5, 8
    print(i)

for i, val in enumerate(['a', 'b', 'c']):  # index + value
    print(i, val)

for char in "hello":            # iterate string characters
    print(char)
```

### While-Schleifen {#while-loops}
```python
count = 0
while count < 5:
    print(count)
    count += 1

# Infinite loop with break
while True:
    data = input("Enter (q to quit): ")
    if data == 'q':
        break
```

### Verschachtelte Schleifen {#nested-loops}
```python
for i in range(3):
    for j in range(3):
        print(f"({i},{j})", end=" ")
    print()
```

### List Comprehensions {#list-comprehensions}
```python
# [expression for item in iterable]
squares = [x**2 for x in range(10)]

# With filter
evens = [x for x in range(20) if x % 2 == 0]

# With transformation + filter
upper_a = [x.upper() for x in names if x.startswith('A')]

# Nested (flatten)
flat = [x for row in matrix for x in row]

# With if-else (expression, not filter)
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
```

### Dict- und Set-Comprehensions {#dict-and-set-comprehensions}
```python
squares = {x: x**2 for x in range(6)}
even_set = {x for x in range(20) if x % 2 == 0}
```

### Generatorausdrücke {#generator-expressions}
```python
# Lazy evaluation - no list in memory
total = sum(x**2 for x in range(1_000_000))
longest = max(len(w) for w in words)
```

## Fallstricke {#gotchas}

- Komplexe Comprehension-Logik (mehrere Bedingungen, verschachtelte `if`s) beeinträchtigt die Lesbarkeit – verwende stattdessen eine reguläre Schleife
- Wer `enumerate()` vergisst und den Index manuell mit `i += 1` mitzählt, schreibt unpythonischen Code
- `range()` gibt ein Range-Objekt zurück, keine Liste – verwende `list(range(n))`, wenn du eine Liste benötigst
- `for/else` und `while/else`: Der `else`-Block läuft, wenn die Schleife ohne `break` endet – selten verwendet, existiert aber

## Siehe auch {#see-also}

- [[iterators-and-generators]] – benutzerdefinierte Iteration, Generatorfunktionen
- [[functions]] – Schleifen in Funktionen auslagern, mit frühem `return`
- [[data-structures]] – Ziele von Comprehensions (Liste, Dict, Menge)
