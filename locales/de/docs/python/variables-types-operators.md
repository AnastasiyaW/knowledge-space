---
title: "Variablen, Typen und Operatoren"
category: concepts
tags: [python, types, variables, operators, numbers, booleans]
level: 3
source_sha256: 7c0d74e6cda110a47bb38f9c8d5a448aa6a47457c3202752817bc03e3615350d
translation: machine
translated_at: '2026-10-24'
---
# Variablen, Typen und Operatoren {#variables-types-and-operators}

Python ist dynamisch typisiert – Variablen benötigen keine Typdeklarationen, und ihr Typ wird zur Laufzeit bestimmt. Alles in Python ist ein Objekt, und Variablen sind Referenzen (Zeiger) auf Objekte.

## Überblick über die Datentypen {#data-types-overview}

| Typ | Beispiel | Veränderlich | Beschreibung |
|------|---------|---------|-------------|
| `int` | `42` | Nein | Ganzzahl, beliebige Genauigkeit |
| `float` | `3.14` | Nein | Gleitkommazahl (64-bit IEEE 754) |
| `str` | `"hello"` | Nein | Textsequenz |
| `bool` | `True/False` | Nein | Boolescher Wert |
| `NoneType` | `None` | Nein | Null/Fehlen eines Werts |
| `list` | `[1, 2, 3]` | Ja | Geordnete, veränderliche Sequenz |
| `tuple` | `(1, 2, 3)` | Nein | Geordnete, unveränderliche Sequenz |
| `dict` | `{"a": 1}` | Ja | Schlüssel-Wert-Zuordnung |
| `set` | `{1, 2, 3}` | Ja | Ungeordnete, eindeutige Elemente |

Den Typ prüft man mit `type(x)`. `isinstance(x, int)` ist `type(x) == int` vorzuziehen – es berücksichtigt Vererbung.

## Wichtige Fakten {#key-facts}

- Python-Ganzzahlen haben beliebige Genauigkeit – kein Überlauf
- `10 / 2` liefert `5.0` (float), nicht `5`. Für ganzzahlige Division `//` verwenden
- `round(2.5)` liefert `2` (Bankers Rundung auf die nächste gerade Zahl)
- `0.1 + 0.2 != 0.3` aufgrund der IEEE-754-Darstellung von Gleitkommazahlen
- `id(x)` zeigt die Speicheradresse; `is` prüft die Identität (dasselbe Objekt), `==` prüft die Gleichheit
- Falsy-Werte: `0`, `0.0`, `""`, `[]`, `()`, `{}`, `set()`, `None`, `False`

## Muster {#patterns}

### Zahlenarithmetik {#number-arithmetic}
```python
10 + 3    # 13  addition
10 - 3    # 7   subtraction
10 * 3    # 30  multiplication
10 / 3    # 3.333...  true division (always float)
10 // 3   # 3   floor division
10 % 3    # 1   modulo
10 ** 3   # 1000  exponentiation
```

### Genauigkeit von Gleitkommazahlen {#floating-point-precision}
```python
0.1 + 0.2 == 0.3               # False!
round(0.1 + 0.2, 1) == 0.3     # True
abs((0.1 + 0.2) - 0.3) < 1e-9  # True (epsilon comparison)

from decimal import Decimal
Decimal('0.1') + Decimal('0.2')  # Decimal('0.3') exactly
```

### Variablen und Zuweisung {#variables-and-assignment}
```python
x = 10              # assignment
x = "hello"         # rebinding (dynamic typing)
x, y = 1, 2         # multiple assignment
x, y = y, x         # swap values
a = b = c = 0       # chained assignment
```

### Typkonvertierung {#type-conversion}
```python
int(3.7)      # 3 (truncates, does NOT round)
float(3)      # 3.0
int("42")     # 42
str(42)       # "42"
bool(0)       # False
bool(1)       # True
```

### Referenzsemantik {#reference-semantics}
```python
a = [1, 2, 3]
b = a              # b points to SAME list
b.append(4)
print(a)           # [1, 2, 3, 4] - a changed too!

c = a.copy()       # c is a NEW list
c.append(5)        # only c changed
```

### Vergleichs- und logische Operatoren {#comparison-and-logical-operators}
```python
# Chaining
1 < x < 10  # equivalent to: 1 < x and x < 10

# Short-circuit evaluation - returns actual values
0 or "default"      # "default"
"value" and 42      # 42
None or "fallback"  # "fallback"
```

### Besondere Gleitkommawerte {#special-float-values}
```python
float('inf')    # positive infinity
float('-inf')   # negative infinity
float('nan')    # not a number
```

## Fallstricke {#gotchas}

- Variablen niemals wie eingebaute Funktionen benennen (`list`, `str`, `dict`, `print`) – sie verdecken diese
- `b = a` erzeugt bei veränderlichen Typen eine gemeinsame Referenz, keine Kopie
- `int("3.14")` löst `ValueError` aus – zuerst `float("3.14")` verwenden, danach `int()`
- `math.floor(-2.3)` ergibt `-3`, `int(-2.3)` ergibt `-2` (Abschneiden in Richtung null)

## Siehe auch {#see-also}

- [[strings-and-text]] - String-Operationen und Formatierung
- [[data-structures]] - Listen, Tupel, Mengen, Dictionaries
- [[type-hints]] - statische Typannotationen
