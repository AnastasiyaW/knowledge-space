---
title: "Variables, types et opérateurs"
category: concepts
tags: [python, types, variables, operators, numbers, booleans]
level: 3
source_sha256: 7c0d74e6cda110a47bb38f9c8d5a448aa6a47457c3202752817bc03e3615350d
translation: machine
translated_at: '2026-10-24'
---
# Variables, types et opérateurs {#variables-types-and-operators}

Python est à typage dynamique : les variables n'ont pas besoin de déclaration de type, et leur type est déterminé à l'exécution. Tout en Python est un objet, et les variables sont des références (pointeurs) vers des objets.

## Vue d'ensemble des types de données {#data-types-overview}

| Type | Exemple | Mutable | Description |
|------|---------|---------|-------------|
| `int` | `42` | Non | Entier, précision arbitraire |
| `float` | `3.14` | Non | Virgule flottante (IEEE 754 64 bits) |
| `str` | `"hello"` | Non | Séquence de texte |
| `bool` | `True/False` | Non | Booléen |
| `NoneType` | `None` | Non | Valeur nulle, absence de valeur |
| `list` | `[1, 2, 3]` | Oui | Séquence ordonnée et modifiable |
| `tuple` | `(1, 2, 3)` | Non | Séquence ordonnée et immuable |
| `dict` | `{"a": 1}` | Oui | Association clé-valeur |
| `set` | `{1, 2, 3}` | Oui | Éléments uniques non ordonnés |

Vérifiez le type avec `type(x)`. Préférez `isinstance(x, int)` à `type(x) == int` : cette forme tient compte de l'héritage.

## Points clés {#key-facts}

- Les entiers Python ont une précision arbitraire : pas de dépassement de capacité (overflow)
- `10 / 2` renvoie `5.0` (float), et non `5`. Utilisez `//` pour la division entière
- `round(2.5)` renvoie `2` (arrondi du banquier, vers le pair le plus proche)
- `0.1 + 0.2 != 0.3` en raison de la représentation IEEE 754 des nombres à virgule flottante
- `id(x)` affiche l'adresse mémoire ; `is` vérifie l'identité (même objet), `==` vérifie l'égalité
- Valeurs falsy : `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`, `None`, `False`

## Modèles courants {#patterns}

### Arithmétique des nombres {#number-arithmetic}
```python
10 + 3    # 13  addition
10 - 3    # 7   subtraction
10 * 3    # 30  multiplication
10 / 3    # 3.333...  true division (always float)
10 // 3   # 3   floor division
10 % 3    # 1   modulo
10 ** 3   # 1000  exponentiation
```

### Précision des nombres à virgule flottante {#floating-point-precision}
```python
0.1 + 0.2 == 0.3               # False!
round(0.1 + 0.2, 1) == 0.3     # True
abs((0.1 + 0.2) - 0.3) < 1e-9  # True (epsilon comparison)

from decimal import Decimal
Decimal('0.1') + Decimal('0.2')  # Decimal('0.3') exactly
```

### Variables et affectation {#variables-and-assignment}
```python
x = 10              # assignment
x = "hello"         # rebinding (dynamic typing)
x, y = 1, 2         # multiple assignment
x, y = y, x         # swap values
a = b = c = 0       # chained assignment
```

### Conversion de types {#type-conversion}
```python
int(3.7)      # 3 (truncates, does NOT round)
float(3)      # 3.0
int("42")     # 42
str(42)       # "42"
bool(0)       # False
bool(1)       # True
```

### Sémantique des références {#reference-semantics}
```python
a = [1, 2, 3]
b = a              # b points to SAME list
b.append(4)
print(a)           # [1, 2, 3, 4] - a changed too!

c = a.copy()       # c is a NEW list
c.append(5)        # only c changed
```

### Opérateurs de comparaison et logiques {#comparison-and-logical-operators}
```python
# Chaining
1 < x < 10  # equivalent to: 1 < x and x < 10

# Short-circuit evaluation - returns actual values
0 or "default"      # "default"
"value" and 42      # 42
None or "fallback"  # "fallback"
```

### Valeurs flottantes spéciales {#special-float-values}
```python
float('inf')    # positive infinity
float('-inf')   # negative infinity
float('nan')    # not a number
```

## Pièges courants {#gotchas}

- Ne nommez jamais une variable comme une fonction native (`list`, `str`, `dict`, `print`) : cela la masque
- `b = a` pour les types mutables crée une référence partagée, et non une copie
- `int("3.14")` lève une `ValueError` : il faut d'abord utiliser `float("3.14")`, puis `int()`
- `math.floor(-2.3)` vaut `-3`, alors que `int(-2.3)` vaut `-2` (troncature vers zéro)

## Voir aussi {#see-also}

- [[strings-and-text]] - opérations et formatage des chaînes de caractères
- [[data-structures]] - listes, tuples, ensembles et dictionnaires
- [[type-hints]] - annotations de types statiques
