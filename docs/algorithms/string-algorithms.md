---
title: String Algorithms
category: concepts
tags: [strings, pattern-matching, trie, substring]
---

# String Algorithms

Algorithms for string searching, matching, and manipulation. Key techniques: brute force, KMP, Rabin-Karp, tries, suffix arrays.

## Key Facts

- Brute-force pattern matching: O(N*M)
- KMP (Knuth-Morris-Pratt): O(N+M) using failure function
- Rabin-Karp: O(N+M) average using rolling hash, O(N*M) worst
- Trie: O(L) per operation where L is string length
- Suffix array: O(N log N) build, O(M log N) search
- Python strings are immutable - concatenation in loop is O(N^2), use `"".join()` instead

## Patterns

### KMP Pattern Matching

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

### Rabin-Karp (Rolling Hash)

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

### Trie (Prefix Tree)

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

### Longest Common Substring (DP)

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

### Palindrome Check and Longest Palindromic Substring

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

## Complexity Comparison

| Algorithm | Preprocess | Search | Space |
|-----------|-----------|--------|-------|
| Brute force | O(1) | O(NM) | O(1) |
| KMP | O(M) | O(N) | O(M) |
| Rabin-Karp | O(M) | O(N) avg | O(1) |
| Trie insert | - | O(L) | O(SIGMA*L*N) |
| Suffix array | O(N log N) | O(M log N) | O(N) |

## Gotchas

- **Issue:** String concatenation in loop creates O(N^2) copies -> **Fix:** Collect in list, use `"".join()` at end.
- **Issue:** Rabin-Karp hash collision gives false match -> **Fix:** Always verify with character-by-character comparison when hashes match. Use large prime modulus.
- **Issue:** KMP failure function built incorrectly -> **Fix:** The failure function `lps[i]` must be the length of the longest proper prefix of `pattern[0..i]` that is also a suffix. "Proper" means not the entire string.

## See Also

- [[dynamic-programming-fundamentals]] - many string problems use DP (edit distance, LCS)
- [[searching-algorithms]] - string search is a specialized search
- [[hash-tables]] - Rabin-Karp uses hashing
