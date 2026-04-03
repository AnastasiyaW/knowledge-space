---
title: Strings and Text Processing
category: concepts
tags: [python, strings, formatting, encoding, bytes, unicode]
---

# Strings and Text Processing

Python strings are immutable sequences of Unicode characters. They support indexing, slicing, and a rich set of methods for text manipulation. Understanding the distinction between `str` (text) and `bytes` (binary data) is essential for file I/O and network programming.

## Key Facts

- Strings are immutable - cannot do `s[0] = 'h'`, must create new string
- Single `'hello'`, double `"hello"`, and triple `'''multi\nline'''` quotes all create strings
- f-strings (Python 3.6+) are the recommended formatting method
- `str` is Unicode text; `bytes` is raw binary data prefixed with `b"..."`
- UTF-8 is the modern standard encoding; always specify encoding explicitly in file I/O

## Patterns

### Indexing and Slicing
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

### Essential String Methods
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

### String Formatting
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

### Checking Methods
```python
s.isdigit()    # all characters are digits
s.isalpha()    # all characters are alphabetic
s.isalnum()    # all alphanumeric
s.isspace()    # all whitespace
s.islower()    # all lowercase
s.isupper()    # all uppercase
```

### Bytes and Encoding
```python
text = "Hello"
encoded = text.encode('utf-8')     # b'Hello'
decoded = encoded.decode('utf-8')  # 'Hello'

# Cyrillic: UTF-8 uses 2 bytes/char, CP1251 uses 1 byte/char
cyrillic = "Привет"
cyrillic.encode('utf-8')    # b'\xd0\x9f\xd1\x80...'
cyrillic.encode('cp1251')   # b'\xcf\xf0...'
```

### Input and Command-Line Arguments
```python
# Interactive input
name = input("Enter name: ")       # always returns str
age = int(input("Enter age: "))    # must convert manually

# Command-line arguments
import sys
sys.argv[0]  # script name
sys.argv[1]  # first argument (always str!)
```

### Input Validation
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

## Gotchas

- `"10" * 4` produces `"10101010"`, not `40` - string repetition vs arithmetic
- `sys.argv` values are always strings - must convert with `int()`/`float()`
- `str.split()` with no args splits on any whitespace and strips empties; `str.split(' ')` splits on single space only
- `isnumeric()` doesn't handle negatives or floats - use try/except for robust validation
- `UnicodeDecodeError` means wrong encoding - try `'cp1252'` or `'latin-1'` as alternatives
- String concatenation with `+=` in a loop is O(n^2) - use `''.join(parts)` instead

## See Also

- [[variables-types-operators]] - type system basics
- [[regular-expressions]] - pattern matching with re module
- [[file-io]] - text file encoding
