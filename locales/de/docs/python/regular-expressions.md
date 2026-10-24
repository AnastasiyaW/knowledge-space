---
title: "Reguläre Ausdrücke"
category: concepts
tags: [python, regex, re-module, pattern-matching, text-processing]
level: 3
source_sha256: 82fb909eff725eddadd26606ec01a283411838bf70fd01cab2a9100b7d613ca4
translation: machine
translated_at: '2026-10-24'
---
# Reguläre Ausdrücke {#regular-expressions}

Das `re`-Modul stellt Perl-artige reguläre Ausdrücke für Mustererkennung, Suche und Textmanipulation bereit. Verwenden Sie für Muster immer Raw-Strings `r'...'`, damit keine doppelte Escapierung nötig wird.

## Wichtige Fakten {#key-facts}

- `re.search()` findet die erste Übereinstimmung an beliebiger Stelle; `re.match()` nur am Anfang; `re.fullmatch()` die gesamte Zeichenkette
- `re.findall()` gibt eine Liste aller Übereinstimmungen zurück; `re.finditer()` gibt einen Iterator von Match-Objekten zurück
- `re.sub()` ersetzt Übereinstimmungen; `re.split()` teilt anhand eines Musters auf
- `re.compile()` kompiliert ein Muster vorab zur Wiederverwendung (bei wiederholter Verwendung schneller)
- Greedy (`*`, `+`) passt so viel wie möglich an; Lazy (`*?`, `+?`) so wenig wie möglich
- Match-Objekt: `.group()` gesamte Übereinstimmung, `.group(1)` erste Capture-Gruppe, `.groups()` alle Gruppen

## Muster {#patterns}

### Kernfunktionen {#core-functions}
```python
import re

re.search(r'\d+', 'abc 123 def')     # Match at '123'
re.match(r'\d+', '123 abc')          # Match at '123' (start only)
re.fullmatch(r'\d+', '123')          # Match (entire string)
re.findall(r'\d+', 'a1 b22 c333')    # ['1', '22', '333']
re.sub(r'\s+', ' ', 'a  b   c')      # 'a b c'
re.split(r'[,;.]', 'a,b;c.d')        # ['a', 'b', 'c', 'd']
```

### Match-Objekt {#match-object}
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

### Zeichenklassen {#character-classes}

| Muster | Entspricht |
|--------|------------|
| `.` | Beliebiges Zeichen außer Zeilenumbruch |
| `\d` / `\D` | Ziffer / Nicht-Ziffer |
| `\w` / `\W` | Wortzeichen `[a-zA-Z0-9_]` / Nicht-Wortzeichen |
| `\s` / `\S` | Leerraum / Nicht-Leerraum |
| `[abc]` | Eines von a, b, c |
| `[a-z]` | Bereich |
| `[^abc]` | NICHT a, b, c |

### Quantifizierer {#quantifiers}

| Muster | Bedeutung |
|--------|-----------|
| `*` / `*?` | 0 oder mehr (greedy / lazy) |
| `+` / `+?` | 1 oder mehr (greedy / lazy) |
| `?` / `??` | 0 oder 1 (greedy / lazy) |
| `{n}` | Genau n |
| `{n,m}` | Zwischen n und m |

### Greedy vs. Lazy {#greedy-vs-lazy}
```python
re.findall(r'<B>.*</B>', '<B>a</B> and <B>b</B>')   # ['<B>a</B> and <B>b</B>']
re.findall(r'<B>.*?</B>', '<B>a</B> and <B>b</B>')  # ['<B>a</B>', '<B>b</B>']
```

### Anker und Grenzen {#anchors-and-boundaries}
```python
# ^ start, $ end, \b word boundary
re.findall(r'\bcat\b', 'the cat scattered cats')  # ['cat']
```

### Gruppen und Rückverweise {#groups-and-backreferences}
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

### Flags {#flags}
```python
re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
# re.I - case insensitive
# re.M - ^ and $ match line boundaries
# re.S - . matches newline
# re.X - verbose mode (comments, whitespace in pattern)
```

### Häufige praktische Muster {#common-practical-patterns}
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

## Fallstricke {#gotchas}

- Verwenden Sie immer Raw-Strings `r'...'`, damit nicht `\\d` statt `\d` entsteht
- `re.match()` passt nur am Anfang der Zeichenkette - verwenden Sie `re.search()` für beliebige Stellen
- `findall()` mit Gruppen gibt die Gruppen zurück, nicht die gesamte Übereinstimmung - verwenden Sie bei Bedarf nicht erfassende Gruppen `(?:...)`
- `re.split()` mit erfassenden Gruppen nimmt die Gruppen in das Ergebnis auf
- `re.escape(string)` escapiert alle Metazeichen, um sie als wörtliches Muster zu verwenden

## Siehe auch {#see-also}

- [[strings-and-text]] - String-Methoden für einfache Textoperationen
- [[file-io]] - Verarbeitung von Textdateien mit regulären Ausdrücken
