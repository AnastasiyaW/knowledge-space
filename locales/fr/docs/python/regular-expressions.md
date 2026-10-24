---
title: "Expressions régulières"
category: concepts
tags: [python, regex, re-module, pattern-matching, text-processing]
level: 3
source_sha256: 82fb909eff725eddadd26606ec01a283411838bf70fd01cab2a9100b7d613ca4
translation: machine
translated_at: '2026-10-24'
---
# Expressions régulières {#regular-expressions}

Le module `re` fournit des expressions régulières de style Perl pour la recherche de motifs, la recherche et la manipulation de texte. Utilisez toujours des chaînes brutes `r'...'` pour les motifs afin d'éviter le double échappement.

## Points clés {#key-facts}

- `re.search()` trouve la première correspondance n'importe où ; `re.match()` uniquement au début ; `re.fullmatch()` sur la chaîne entière
- `re.findall()` renvoie la liste de toutes les correspondances ; `re.finditer()` renvoie un itérateur d'objets Match
- `re.sub()` remplace les correspondances ; `re.split()` découpe selon le motif
- `re.compile()` précompile le motif pour le réutiliser (plus rapide en cas d'utilisation répétée)
- Gourmand (`*`, `+`) correspond le plus possible ; paresseux (`*?`, `+?`) le moins possible
- Objet Match : `.group()` correspondance complète, `.group(1)` premier groupe de capture, `.groups()` tous les groupes

## Motifs {#patterns}

### Fonctions principales {#core-functions}
```python
import re

re.search(r'\d+', 'abc 123 def')     # Match at '123'
re.match(r'\d+', '123 abc')          # Match at '123' (start only)
re.fullmatch(r'\d+', '123')          # Match (entire string)
re.findall(r'\d+', 'a1 b22 c333')    # ['1', '22', '333']
re.sub(r'\s+', ' ', 'a  b   c')      # 'a b c'
re.split(r'[,;.]', 'a,b;c.d')        # ['a', 'b', 'c', 'd']
```

### Objet Match {#match-object}
```python
m = re.search(r'(\d+)-(\d+)', 'tel: 555-1234')
m.group()     # '555-1234' (entire match)
m.group(1)    # '555' (first group)
m.group(2)    # '1234' (second group)
m.groups()    # ('555', '1234')
m.start()     # 5
m.end()       # 13
m.span()      # (5, 13)
```

### Classes de caractères {#character-classes}

| Motif | Correspond à |
|---------|---------|
| `.` | N'importe quel caractère sauf le saut de ligne |
| `\d` / `\D` | Chiffre / non-chiffre |
| `\w` / `\W` | Caractère de mot `[a-zA-Z0-9_]` / non-mot |
| `\s` / `\S` | Espace blanc / non-espace blanc |
| `[abc]` | N'importe lequel de a, b, c |
| `[a-z]` | Plage |
| `[^abc]` | Aucun de a, b, c |

### Quantificateurs {#quantifiers}

| Motif | Signification |
|---------|---------|
| `*` / `*?` | 0 ou plus (gourmand / paresseux) |
| `+` / `+?` | 1 ou plus (gourmand / paresseux) |
| `?` / `??` | 0 ou 1 (gourmand / paresseux) |
| `{n}` | Exactement n |
| `{n,m}` | Entre n et m |

### Gourmand ou paresseux {#greedy-vs-lazy}
```python
re.findall(r'<B>.*</B>', '<B>a</B> and <B>b</B>')   # ['<B>a</B> and <B>b</B>']
re.findall(r'<B>.*?</B>', '<B>a</B> and <B>b</B>')  # ['<B>a</B>', '<B>b</B>']
```

### Ancres et délimiteurs {#anchors-and-boundaries}
```python
# ^ start, $ end, \b word boundary
re.findall(r'\bcat\b', 'the cat scattered cats')  # ['cat']
```

### Groupes et références arrière {#groups-and-backreferences}
```python
# Capturing groups
m = re.search(r'((ab)(cd))', 'abcd')
m.group(1)  # 'abcd', m.group(2)  # 'ab', m.group(3)  # 'cd'

# Non-capturing group
re.findall(r'(?:ab)+', 'ababab')  # ['ababab']

# Backreference (find repeated words)
re.findall(r'\b(\w+)\s+\1\b', 'the the cat')  # ['the']

# Sub with backreference
re.sub(r'(\w+) (\w+)', r'\2 \1', 'hello world')  # 'world hello'
```

### Indicateurs {#flags}
```python
re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
# re.I - case insensitive
# re.M - ^ and $ match line boundaries
# re.S - . matches newline
# re.X - verbose mode (comments, whitespace in pattern)
```

### Motifs pratiques courants {#common-practical-patterns}
```python
# Email (simplified)
r'[\w.-]+@[\w.-]+\.\w+'

# Phone
r'\+7-\d{3}-\d{3}-\d{2}-\d{2}'

# IP address
r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# URL
r'https?://[\w./\-?=&#]+'

# Normalize whitespace
re.sub(r'\s+', ' ', text).strip()

# Extract all numbers
numbers = [int(x) for x in re.findall(r'\d+', text)]

# Split by multiple delimiters
re.split(r'[,;.\s]+', text)
```

## Pièges {#gotchas}

- Utilisez toujours des chaînes brutes `r'...'` pour éviter d'écrire `\\d` au lieu de `\d`
- `re.match()` ne correspond qu'au début de la chaîne ; utilisez `re.search()` pour une correspondance n'importe où
- `findall()` avec des groupes renvoie les groupes, et non la correspondance complète ; utilisez des groupes non capturants `(?:...)` si nécessaire
- `re.split()` avec des groupes capturants inclut les groupes dans le résultat
- `re.escape(string)` échappe tous les métacaractères pour un usage en motif littéral

## Voir aussi {#see-also}

- [[strings-and-text]] - méthodes de chaînes pour les opérations de texte simples
- [[file-io]] - traitement de fichiers texte avec des expressions régulières
