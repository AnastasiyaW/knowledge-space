---
title: "Structures de contrôle"
category: concepts
tags: [python, loops, conditionals, comprehensions, iteration]
level: 3
source_sha256: 746abd27ed14afbd33b4adbbba5cd5ad53726e645dde86686b2220b66c75157d
translation: machine
translated_at: '2026-10-24'
---
# Structures de contrôle {#control-flow}

Python utilise l'indentation (4 espaces) pour délimiter les blocs de code. Les structures de contrôle comprennent les conditionnelles, les boucles for/while et les compréhensions, qui sont des alternatives concises aux schémas de boucle avec accumulation.

## Points clés {#key-facts}

- L'indentation est significative sur le plan syntaxique : 4 espaces par niveau (PEP 8)
- Les boucles `for` itèrent sur n'importe quel itérable (liste, tuple, chaîne, range, générateur, etc.)
- `range(n)` génère `0, 1, ..., n-1` ; `range(start, stop, step)` pour un contrôle complet
- Les compréhensions (list, dict, set) remplacent les schémas simples de boucle for avec `append`
- `break` interrompt la boucle ; `continue` passe à l'itération suivante ; `pass` est un espace réservé sans effet

## Schémas {#patterns}

### Conditionnelles {#conditionals}
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

### Boucles for {#for-loops}
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

### Boucles while {#while-loops}
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

### Boucles imbriquées {#nested-loops}
```python
for i in range(3):
    for j in range(3):
        print(f"({i},{j})", end=" ")
    print()
```

### Compréhensions de listes {#list-comprehensions}
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

### Compréhensions de dictionnaires et d'ensembles {#dict-and-set-comprehensions}
```python
squares = {x: x**2 for x in range(6)}
even_set = {x for x in range(20) if x % 2 == 0}
```

### Expressions génératrices {#generator-expressions}
```python
# Lazy evaluation - no list in memory
total = sum(x**2 for x in range(1_000_000))
longest = max(len(w) for w in words)
```

## Pièges {#gotchas}

- La logique de compréhension complexe (conditions multiples, ifs imbriqués) nuit à la lisibilité : utilisez plutôt une boucle classique
- Oublier `enumerate()` et suivre manuellement l'index avec `i += 1` n'est pas pythonique
- `range()` renvoie un objet range, et non une liste : utilisez `list(range(n))` si vous avez besoin d'une liste
- `for/else` et `while/else` : le bloc `else` s'exécute lorsque la boucle se termine sans `break` ; rarement utilisé, mais existant

## Voir aussi {#see-also}

- [[iterators-and-generators]] - itération personnalisée, fonctions génératrices
- [[functions]] - découper les boucles en fonctions avec retour anticipé
- [[data-structures]] - cibles des compréhensions (list, dict, set)
