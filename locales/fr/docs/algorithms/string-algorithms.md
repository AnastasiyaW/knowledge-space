---
title: "Algorithmes sur les chaînes"
category: concepts
tags: [strings, pattern-matching, trie, substring]
level: 3
source_sha256: a5a81bf75ac3d3046bd99b5a3db7edf8443bbf845cf4a91fee99cda608ab54b6
translation: machine
translated_at: '2026-10-24'
---
# Algorithmes sur les chaînes {#string-algorithms}

Algorithmes de recherche, de correspondance et de manipulation de chaînes de caractères. Techniques principales : force brute, KMP, Rabin-Karp, tries, tableaux des suffixes.

## Points clés {#key-facts}

- Recherche de motif par force brute : O(N*M)
- KMP (Knuth-Morris-Pratt) : O(N+M) à l'aide de la fonction d'échec
- Rabin-Karp : O(N+M) en moyenne grâce au hachage glissant, O(N*M) dans le pire cas
- Trie : O(L) par opération, où L est la longueur de la chaîne
- Tableau des suffixes : construction en O(N log N), recherche en O(M log N)
- Les chaînes Python sont immuables : la concaténation dans une boucle est en O(N^2), utilisez plutôt `"".join()`

## Motifs {#patterns}

### Recherche de motif KMP {#kmp-pattern-matching}

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

### Rabin-Karp (hachage glissant) {#rabin-karp-rolling-hash}

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

### Trie (arbre de préfixes) {#trie-prefix-tree}

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

### Plus longue sous-chaîne commune (programmation dynamique) {#longest-common-substring-dp}

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

### Test de palindrome et plus longue sous-chaîne palindromique {#palindrome-check-and-longest-palindromic-substring}

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

## Comparaison de la complexité {#complexity-comparison}

| Algorithme | Prétraitement | Recherche | Espace |
|-----------|-----------|--------|-------|
| Force brute | O(1) | O(NM) | O(1) |
| KMP | O(M) | O(N) | O(M) |
| Rabin-Karp | O(M) | O(N) en moyenne | O(1) |
| Insertion dans un trie | - | O(L) | O(SIGMA*L*N) |
| Tableau des suffixes | O(N log N) | O(M log N) | O(N) |

## Pièges courants {#gotchas}

- **Problème :** la concaténation de chaînes dans une boucle crée O(N^2) copies -> **Solution :** accumuler dans une liste, puis utiliser `"".join()` à la fin.
- **Problème :** une collision de hachage dans Rabin-Karp produit une fausse correspondance -> **Solution :** toujours vérifier caractère par caractère lorsque les hachages correspondent. Utiliser un grand nombre premier comme modulo.
- **Problème :** fonction d'échec de KMP mal construite -> **Solution :** la fonction d'échec `lps[i]` doit être la longueur du plus long préfixe propre de `pattern[0..i]` qui est aussi un suffixe. « Propre » signifie que ce n'est pas la chaîne entière.

## Voir aussi {#see-also}

- [[dynamic-programming-fundamentals]] - de nombreux problèmes de chaînes utilisent la programmation dynamique (distance d'édition, LCS)
- [[searching-algorithms]] - la recherche de chaînes est une recherche spécialisée
- [[hash-tables]] - Rabin-Karp utilise le hachage
