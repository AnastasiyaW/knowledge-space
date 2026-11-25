---
title: "Chaînes de caractères et traitement de texte"
category: concepts
tags: [python, strings, formatting, encoding, bytes, unicode]
level: 3
source_sha256: 528293d0ff72feb17ee8d96adaa065806b5793ecabbe1e8135d23db7e5f68e8d
translation: machine
translated_at: '2026-10-24'
---
# Chaînes de caractères et traitement de texte {#strings-and-text-processing}

Les chaînes de caractères Python sont des séquences immuables de caractères Unicode. Elles supportent l'indexation, le découpage (slicing) et un ensemble riche de méthodes de manipulation de texte. Comprendre la distinction entre `str` (texte) et `bytes` (données binaires) est essentiel pour les E/S sur fichiers et la programmation réseau.

## Points clés {#key-facts}

- Les chaînes sont immuables : `s[0] = 'h'` est interdit, il faut créer une nouvelle chaîne
- Les guillemets simples `'hello'`, doubles `"hello"` et triples `'''multi\nline'''` créent tous des chaînes
- Les f-strings (Python 3.6+) sont la méthode de formatage recommandée
- `str` est du texte Unicode ; `bytes` est de la donnée binaire brute préfixée par `b"..."`
- L'UTF-8 est l'encodage standard actuel ; spécifiez toujours l'encodage explicitement dans les E/S sur fichiers

## Motifs {#patterns}

### Indexation et découpage {#indexing-and-slicing}
```python
s = "Hello World"
s[0]        # 'H' (first)
s[-1]       # 'd' (last)
s[0:5]      # 'Hello' (stop exclusive)
s[6:]       # 'World'
s[:5]       # 'Hello'
s[::2]      # 'HloWrd' (every 2nd)
s[::-1]     # 'dlroW olleH' (reversed)
```

### Méthodes essentielles des chaînes {#essential-string-methods}
```python
s.upper()              # 'HELLO WORLD'
s.lower()              # 'hello world'
s.strip()              # remove whitespace both ends
s.split()              # ['Hello', 'World']
s.split(',')           # split by delimiter
','.join(['a','b'])    # 'a,b'
s.replace('o', '0')    # 'Hell0 W0rld'
s.find('World')        # 6 (-1 if not found)
s.count('l')           # 3
s.startswith('He')     # True
s.endswith('ld')       # True
s.isdigit()            # False
len(s)                 # 11
```

### Formatage de chaînes {#string-formatting}
```python
name, age = "Alice", 30

# f-strings (recommended)
f"Name: {name}, Age: {age}"
f"Price: {19.99:.2f}"         # 'Price: 19.99'
f"{'centered':^20}"           # '      centered      '
f"{1000000:,}"                # '1,000,000'

# .format()
"Name: {}, Age: {}".format(name, age)

# % formatting (legacy)
"Name: %s, Age: %d" % (name, age)
```

### Méthodes de vérification {#checking-methods}
```python
s.isdigit()    # all characters are digits
s.isalpha()    # all characters are alphabetic
s.isalnum()    # all alphanumeric
s.isspace()    # all whitespace
s.islower()    # all lowercase
s.isupper()    # all uppercase
```

### Bytes et encodage {#bytes-and-encoding}
```python
text = "Hello"
encoded = text.encode('utf-8')     # b'Hello'
decoded = encoded.decode('utf-8')  # 'Hello'

# Cyrillic: UTF-8 uses 2 bytes/char, CP1251 uses 1 byte/char
cyrillic = "Привет"
cyrillic.encode('utf-8')    # b'\xd0\x9f\xd1\x80...'
cyrillic.encode('cp1251')   # b'\xcf\xf0...'
```

### Entrées et arguments de ligne de commande {#input-and-command-line-arguments}
```python
# Interactive input
name = input("Enter name: ")       # always returns str
age = int(input("Enter age: "))    # must convert manually

# Command-line arguments
import sys
sys.argv[0]  # script name
sys.argv[1]  # first argument (always str!)
```

### Validation des entrées {#input-validation}
```python
# EAFP approach (preferred)
try:
    num = int(input("Number: "))
except ValueError:
    print("Not a valid number")

# Check before converting
text = input("Number: ")
if text.isnumeric():   # digits only, no negatives/floats
    num = int(text)
```

## Pièges {#gotchas}

- `"10" * 4` produit `"10101010"`, et non `40` : répétition de chaîne contre arithmétique
- Les valeurs de `sys.argv` sont toujours des chaînes ; il faut les convertir avec `int()`/`float()`
- `str.split()` sans argument découpe sur tout espace blanc et supprime les éléments vides ; `str.split(' ')` ne découpe que sur l'espace simple
- `isnumeric()` ne gère ni les nombres négatifs ni les flottants : utilisez try/except pour une validation robuste
- `UnicodeDecodeError` signifie un mauvais encodage : essayez `'cp1252'` ou `'latin-1'` comme alternatives
- La concaténation avec `+=` dans une boucle est en O(n^2) : utilisez `''.join(parts)` à la place

## Voir aussi {#see-also}

- [[variables-types-operators]] - bases du système de types
- [[regular-expressions]] - correspondance de motifs avec le module re
- [[file-io]] - encodage des fichiers texte
