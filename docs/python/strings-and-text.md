---
title: Strings and Text Processing
category: fundamentals
tags: [python, strings, formatting, regex, encoding]
---

# Strings and Text Processing

Strings are immutable sequences of Unicode characters. Created with single `'hello'`, double `"hello"`, or triple `'''multiline'''` quotes.

## Indexing and Slicing

```python
s = "Hello World"
s[0]        # 'H' (first character)
s[-1]       # 'd' (last character)
s[0:5]      # 'Hello' (start:stop, stop exclusive)
s[6:]       # 'World' (from index 6 to end)
s[:5]       # 'Hello' (from start to index 5)
s[::2]      # 'HloWrd' (every 2nd character)
s[::-1]     # 'dlroW olleH' (reversed)
```

Slice syntax: `s[start:stop:step]`. Start defaults to 0, stop to len, step to 1.

## Essential Methods

```python
s.upper() / s.lower() / s.title()
s.strip() / s.lstrip() / s.rstrip()     # remove whitespace
s.split()                                # ['Hello', 'World']
s.split(',')                             # split by delimiter
','.join(['a', 'b'])                     # 'a,b'
s.replace('o', '0')                      # 'Hell0 W0rld'
s.find('World')                          # 6 (-1 if not found)
s.count('l')                             # 3
s.startswith('He') / s.endswith('ld')    # True
s.isdigit() / s.isalpha() / s.isalnum()
len(s)                                   # 11
```

## String Formatting

```python
name, age = "Alice", 30

# f-strings (recommended, Python 3.6+)
f"Name: {name}, Age: {age}"
f"Price: {19.99:.2f}"         # 'Price: 19.99'
f"{'centered':^20}"           # '      centered      '
f"{1000000:,}"                # '1,000,000'

# .format() method
"Name: {}, Age: {}".format(name, age)

# % formatting (legacy)
"Name: %s, Age: %d" % (name, age)
```

## String Checking

```python
s.isdigit()    # all characters are digits
s.isnumeric()  # broader (includes unicode numerals)
s.isalpha()    # all alphabetic
s.isalnum()    # all alphanumeric
s.isspace()    # all whitespace
```

## Encodings

```python
text = "Hello"
encoded = text.encode('utf-8')     # b'Hello'
decoded = encoded.decode('utf-8')  # 'Hello'

# Cyrillic
"Привет".encode('utf-8')   # 2 bytes per char
"Привет".encode('cp1251')  # 1 byte per char
```

**Common encodings**: ASCII (7-bit, 128 chars), CP1251 (Cyrillic, 1 byte/char), UTF-8 (1-4 bytes, universal). UTF-8 is the modern standard.

`UnicodeDecodeError` means wrong encoding - try `encoding='cp1251'` or `encoding='latin-1'`.

## Regular Expressions

```python
import re

re.search(r'\d+', 'abc 123')        # finds '123' anywhere
re.match(r'\d+', '123 abc')         # match at beginning only
re.fullmatch(r'\d+', '123')         # entire string must match
re.findall(r'\d+', 'a1 b22 c333')   # ['1', '22', '333']
re.sub(r'\s+', ' ', 'a  b   c')     # 'a b c'
re.split(r'[,;.]', 'a,b;c.d')       # ['a', 'b', 'c', 'd']
```

### Pattern Syntax

| Pattern | Matches |
|---------|---------|
| `.` | Any char except newline |
| `\d` / `\D` | Digit / non-digit |
| `\w` / `\W` | Word char / non-word |
| `\s` / `\S` | Whitespace / non-whitespace |
| `\b` | Word boundary |
| `[abc]` | Character set |
| `[^abc]` | Negated set |
| `*` / `+` / `?` | 0+, 1+, 0-1 (greedy) |
| `*?` / `+?` | Lazy versions |
| `{n,m}` | Between n and m |
| `^` / `$` | Start / end of string |
| `(...)` | Capturing group |
| `(?:...)` | Non-capturing group |

### Greedy vs Lazy

```python
re.findall(r'<B>.*</B>', '<B>a</B> and <B>b</B>')    # greedy: one match
re.findall(r'<B>.*?</B>', '<B>a</B> and <B>b</B>')   # lazy: two matches
```

### Match Object

```python
m = re.search(r'(\d+)-(\d+)', 'tel: 555-1234')
m.group()    # '555-1234'
m.group(1)   # '555'
m.group(2)   # '1234'
m.span()     # (5, 13)
```

### Flags

`re.I` (case-insensitive), `re.M` (multiline `^`/`$`), `re.S` (`.` matches newline), `re.X` (verbose with comments). Combine with `|`.

### Common Patterns

```python
r'[\w.-]+@[\w.-]+\.\w+'           # email (simplified)
r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'  # IP address
r'https?://[\w./\-?=&#]+'        # URL
r'#[0-9A-Fa-f]{6}'               # hex color
```

Always use raw strings `r'...'` for regex patterns. Pre-compile with `re.compile()` when reusing patterns.

## Gotchas

- Strings are immutable - `s[0] = 'h'` raises TypeError
- `"10" * 4` = `"10101010"` (repetition, not multiplication)
- Always use `r'...'` raw strings for regex to avoid double-escaping
- `str.split()` with no args splits on any whitespace and strips empty strings; `str.split(' ')` splits only on spaces and keeps empty strings
- `re.findall()` with groups returns groups, not full matches

## See Also

- [[variables-types-operators]] - type conversion, truthiness
- [[file-io-and-serialization]] - reading/writing text files
- [[stdlib-essentials]] - collections.Counter for string analysis
