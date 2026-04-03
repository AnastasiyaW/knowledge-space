---
title: Regular Expressions
category: concepts
tags: [python, regex, re-module, pattern-matching, text-processing]
---

# Regular Expressions

The `re` module provides Perl-style regular expressions for pattern matching, searching, and text manipulation. Always use raw strings `r'...'` for patterns to avoid double-escaping.

## Key Facts

- `re.search()` finds first match anywhere; `re.match()` only at start; `re.fullmatch()` entire string
- `re.findall()` returns list of all matches; `re.finditer()` returns iterator of Match objects
- `re.sub()` replaces matches; `re.split()` splits by pattern
- `re.compile()` pre-compiles pattern for reuse (faster with repeated use)
- Greedy (`*`, `+`) matches as much as possible; lazy (`*?`, `+?`) as little as possible
- Match object: `.group()` full match, `.group(1)` first capture group, `.groups()` all groups

## Patterns

### Core Functions
```python
import re

re.search(r'\d+', 'abc 123 def')     # Match at '123'
re.match(r'\d+', '123 abc')          # Match at '123' (start only)
re.fullmatch(r'\d+', '123')          # Match (entire string)
re.findall(r'\d+', 'a1 b22 c333')    # ['1', '22', '333']
re.sub(r'\s+', ' ', 'a  b   c')      # 'a b c'
re.split(r'[,;.]', 'a,b;c.d')        # ['a', 'b', 'c', 'd']
```

### Match Object
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

### Character Classes

| Pattern | Matches |
|---------|---------|
| `.` | Any char except newline |
| `\d` / `\D` | Digit / non-digit |
| `\w` / `\W` | Word char `[a-zA-Z0-9_]` / non-word |
| `\s` / `\S` | Whitespace / non-whitespace |
| `[abc]` | Any of a, b, c |
| `[a-z]` | Range |
| `[^abc]` | NOT a, b, c |

### Quantifiers

| Pattern | Meaning |
|---------|---------|
| `*` / `*?` | 0+ (greedy / lazy) |
| `+` / `+?` | 1+ (greedy / lazy) |
| `?` / `??` | 0 or 1 (greedy / lazy) |
| `{n}` | Exactly n |
| `{n,m}` | Between n and m |

### Greedy vs Lazy
```python
re.findall(r'<B>.*</B>', '<B>a</B> and <B>b</B>')   # ['<B>a</B> and <B>b</B>']
re.findall(r'<B>.*?</B>', '<B>a</B> and <B>b</B>')  # ['<B>a</B>', '<B>b</B>']
```

### Anchors and Boundaries
```python
# ^ start, $ end, \b word boundary
re.findall(r'\bcat\b', 'the cat scattered cats')  # ['cat']
```

### Groups and Backreferences
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

### Flags
```python
re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
# re.I - case insensitive
# re.M - ^ and $ match line boundaries
# re.S - . matches newline
# re.X - verbose mode (comments, whitespace in pattern)
```

### Common Practical Patterns
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

## Gotchas

- Always use raw strings `r'...'` to avoid `\\d` instead of `\d`
- `re.match()` only matches at string start - use `re.search()` for anywhere
- `findall()` with groups returns groups, not full match - use non-capturing `(?:...)` if needed
- `re.split()` with capturing groups includes the groups in the result
- `re.escape(string)` escapes all metacharacters for use as literal pattern

## See Also

- [[strings-and-text]] - string methods for simple text operations
- [[file-io]] - processing text files with regex
