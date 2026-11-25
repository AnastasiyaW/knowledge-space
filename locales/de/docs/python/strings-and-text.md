---
title: "Strings und Textverarbeitung"
category: concepts
tags: [python, strings, formatting, encoding, bytes, unicode]
level: 3
source_sha256: 528293d0ff72feb17ee8d96adaa065806b5793ecabbe1e8135d23db7e5f68e8d
translation: machine
translated_at: '2026-10-24'
---
# Strings und Textverarbeitung {#strings-and-text-processing}

Python-Strings sind unveränderliche Sequenzen von Unicode-Zeichen. Sie unterstützen Indizierung, Slicing und eine umfangreiche Menge an Methoden zur Textbearbeitung. Der Unterschied zwischen `str` (Text) und `bytes` (Binärdaten) ist für Datei-I/O und Netzwerkprogrammierung unverzichtbar.

## Wichtige Fakten {#key-facts}

- Strings sind unveränderlich. `s[0] = 'h'` ist nicht möglich, stattdessen muss ein neuer String erzeugt werden.
- Einfache `'hello'`, doppelte `"hello"` und dreifache `'''multi\nline'''` Anführungszeichen erzeugen alle Strings.
- f-Strings (Python 3.6+) sind die empfohlene Formatierungsmethode.
- `str` ist Unicode-Text; `bytes` sind rohe Binärdaten mit dem Präfix `b"..."`.
- UTF-8 ist der moderne Standard-Encoding; bei Datei-I/O sollte das Encoding immer explizit angegeben werden.

## Muster {#patterns}

### Indizierung und Slicing {#indexing-and-slicing}
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

### Wichtige String-Methoden {#essential-string-methods}
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

### String-Formatierung {#string-formatting}
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

### Prüfmethoden {#checking-methods}
```python
s.isdigit()    # all characters are digits
s.isalpha()    # all characters are alphabetic
s.isalnum()    # all alphanumeric
s.isspace()    # all whitespace
s.islower()    # all lowercase
s.isupper()    # all uppercase
```

### Bytes und Encoding {#bytes-and-encoding}
```python
text = "Hello"
encoded = text.encode('utf-8')     # b'Hello'
decoded = encoded.decode('utf-8')  # 'Hello'

# Cyrillic: UTF-8 uses 2 bytes/char, CP1251 uses 1 byte/char
cyrillic = "Привет"
cyrillic.encode('utf-8')    # b'\xd0\x9f\xd1\x80...'
cyrillic.encode('cp1251')   # b'\xcf\xf0...'
```

### Eingabe und Kommandozeilenargumente {#input-and-command-line-arguments}
```python
# Interactive input
name = input("Enter name: ")       # always returns str
age = int(input("Enter age: "))    # must convert manually

# Command-line arguments
import sys
sys.argv[0]  # script name
sys.argv[1]  # first argument (always str!)
```

### Eingabevalidierung {#input-validation}
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

## Fallstricke {#gotchas}

- `"10" * 4` ergibt `"10101010"`, nicht `40`. Stringwiederholung und Arithmetik sind verschieden.
- Werte aus `sys.argv` sind immer Strings und müssen mit `int()`/`float()` umgewandelt werden.
- `str.split()` ohne Argumente teilt an beliebigen Leerzeichen und entfernt leere Einträge; `str.split(' ')` teilt nur am einzelnen Leerzeichen.
- `isnumeric()` erkennt weder negative Zahlen noch Gleitkommazahlen. Für robuste Validierung sollte try/except verwendet werden.
- `UnicodeDecodeError` bedeutet ein falsches Encoding. Als Alternativen kommen `'cp1252'` oder `'latin-1'` in Frage.
- Stringverkettung mit `+=` in einer Schleife hat die Laufzeit O(n^2). Stattdessen `''.join(parts)` verwenden.

## Siehe auch {#see-also}

- [[variables-types-operators]] - Grundlagen des Typsystems
- [[regular-expressions]] - Mustererkennung mit dem re-Modul
- [[file-io]] - Text-Dateien und Encoding
