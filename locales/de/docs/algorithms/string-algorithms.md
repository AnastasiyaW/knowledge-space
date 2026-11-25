---
title: "String-Algorithmen"
category: concepts
tags: [strings, pattern-matching, trie, substring]
level: 3
source_sha256: a5a81bf75ac3d3046bd99b5a3db7edf8443bbf845cf4a91fee99cda608ab54b6
translation: machine
translated_at: '2026-10-24'
---
# String-Algorithmen {#string-algorithms}

Algorithmen für Zeichenkettensuche, Mustererkennung und Stringmanipulation. Zentrale Techniken: Brute-Force, KMP, Rabin-Karp, Tries, Suffix-Arrays.

## Key Facts {#key-facts}

- Brute-Force-Mustersuche: O(N*M)
- KMP (Knuth-Morris-Pratt): O(N+M) unter Verwendung der Failure-Funktion
- Rabin-Karp: O(N+M) im Mittel mit Rolling Hash, O(N*M) im schlechtesten Fall
- Trie: O(L) pro Operation, wobei L die Länge der Zeichenkette ist
- Suffix-Array: O(N log N) Aufbau, O(M log N) Suche
- Python-Strings sind unveränderlich – Konkatenation in einer Schleife ist O(N^2), stattdessen `"".join()` verwenden

## Patterns {#patterns}

### KMP-Mustersuche {#kmp-pattern-matching}

```python
def kmp_search(text, pattern):
    def build_lps(pat):
        lps = [0] * len(pat)
        length = 0
        i = 1
        while i < len(pat):
            if pat[i] == pat[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
        return lps

    lps = build_lps(pattern)
    i = j = 0
    matches = []
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and text[i] != pattern[j]:
            if j:
                j = lps[j - 1]
            else:
                i += 1
    return matches
```

### Rabin-Karp (Rolling Hash) {#rabin-karp-rolling-hash}

```python
def rabin_karp(text, pattern):
    base, mod = 256, 101
    m, n = len(pattern), len(text)
    p_hash = t_hash = 0
    h = pow(base, m - 1, mod)

    for i in range(m):
        p_hash = (base * p_hash + ord(pattern[i])) % mod
        t_hash = (base * t_hash + ord(text[i])) % mod

    matches = []
    for i in range(n - m + 1):
        if p_hash == t_hash and text[i:i + m] == pattern:
            matches.append(i)
        if i < n - m:
            t_hash = (base * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
            t_hash = (t_hash + mod) % mod  # ensure positive
    return matches
```

### Trie (Präfixbaum) {#trie-prefix-tree}

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._find(prefix) is not None

    def _find(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

### Längste gemeinsame Teilzeichenkette (DP) {#longest-common-substring-dp}

```python
def longest_common_substring(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0
    end_idx = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_idx = i
    return s1[end_idx - max_len:end_idx]
```

### Palindrom-Prüfung und längstes Palindrom-Teilstring {#palindrome-check-and-longest-palindromic-substring}

```python
def longest_palindrome(s):
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    result = ""
    for i in range(len(s)):
        odd = expand(i, i)
        even = expand(i, i + 1)
        result = max(result, odd, even, key=len)
    return result
```

## Komplexitätsvergleich {#complexity-comparison}

| Algorithmus | Vorverarbeitung | Suche | Speicher |
|-----------|-----------|--------|-------|
| Brute-Force | O(1) | O(NM) | O(1) |
| KMP | O(M) | O(N) | O(M) |
| Rabin-Karp | O(M) | O(N) im Mittel | O(1) |
| Trie-Einfügen | - | O(L) | O(SIGMA*L*N) |
| Suffix-Array | O(N log N) | O(M log N) | O(N) |

## Gotchas {#gotchas}

- **Problem:** Stringkonkatenation in einer Schleife erzeugt O(N^2) Kopien -> **Lösung:** In einer Liste sammeln und am Ende `"".join()` verwenden.
- **Problem:** Hash-Kollision bei Rabin-Karp liefert einen falschen Treffer -> **Lösung:** Bei übereinstimmenden Hashes immer zeichenweise vergleichen. Einen großen Primzahl-Modulus verwenden.
- **Problem:** Failure-Funktion für KMP falsch aufgebaut -> **Lösung:** Die Failure-Funktion `lps[i]` muss die Länge des längsten echten Präfixes von `pattern[0..i]` sein, das zugleich ein Suffix ist. „Echt“ bedeutet, dass nicht die gesamte Zeichenkette gemeint ist.

## Siehe auch {#see-also}

- [[dynamic-programming-fundamentals]] - viele String-Probleme werden mit DP gelöst (Editierdistanz, LCS)
- [[searching-algorithms]] - Stringsuche ist eine spezialisierte Suche
- [[hash-tables]] - Rabin-Karp verwendet Hashing
